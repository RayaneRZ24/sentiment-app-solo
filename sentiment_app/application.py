"""Démarrage local du service et de son interface, sans ressources de développement."""
from __future__ import annotations

import importlib.util
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

from sentiment_app.predict import chemin_modele


def _port_libre(port: int) -> None:
    if not 1 <= port <= 65535:
        raise ValueError("Le port doit être compris entre 1 et 65535.")
    with socket.socket() as connexion:
        try:
            connexion.bind(("127.0.0.1", port))
        except OSError as erreur:
            raise OSError(f"Le port {port} est déjà utilisé. Choisissez un autre port.") from erreur


def _attendre(url: str, processus: subprocess.Popen, arret: threading.Event) -> None:
    fin = time.monotonic() + 40
    while time.monotonic() < fin:
        if arret.is_set():
            raise InterruptedError
        if processus.poll() is not None:
            raise RuntimeError("Le service n'a pas pu démarrer. Vérifiez le modèle et l'installation.")
        try:
            with urllib.request.urlopen(url, timeout=1) as reponse:
                if reponse.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError):
            pass
        arret.wait(0.2)
    raise RuntimeError("Le démarrage a pris trop de temps. Réessayez ou contactez le support.")


def lancer(api_port: int = 8000, port: int = 8501, *, ouvrir: bool = True,
           arret: threading.Event | None = None) -> int:
    """Lance deux processus locaux et les arrête ensemble, y compris après une panne."""
    arret = arret if arret is not None else threading.Event()
    processus: list[subprocess.Popen] = []
    try:
        if importlib.util.find_spec("streamlit") is None:
            raise RuntimeError('Interface absente : réinstallez le paquet avec son option [ui].')
        if not chemin_modele().is_file():
            raise RuntimeError("Modèle absent : indiquez le modèle fourni dans SENTIMENT_MODELE.")
        if api_port == port:
            raise ValueError("Le service et l'interface doivent utiliser deux ports différents.")
        _port_libre(api_port)
        _port_libre(port)
        environnement = dict(os.environ, API_URL=f"http://127.0.0.1:{api_port}",
                             STREAMLIT_BROWSER_GATHER_USAGE_STATS="false")
        page = Path(__file__).resolve().parents[1] / "ui" / "app.py"
        options = {"env": environnement, "stderr": subprocess.STDOUT,
                   "creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0)}
        with tempfile.TemporaryDirectory(prefix="sentiment-session-") as dossier:
            with (Path(dossier) / "service.log").open("w") as log_api, (Path(dossier) / "interface.log").open("w") as log_ui:
                try:
                    service = subprocess.Popen(
                        [sys.executable, "-m", "uvicorn", "api.main:app", "--host", "127.0.0.1",
                         "--port", str(api_port)], stdout=log_api, **options)
                    processus.append(service)
                    _attendre(f"http://127.0.0.1:{api_port}/health", service, arret)
                    interface = subprocess.Popen(
                        [sys.executable, "-m", "streamlit", "run", str(page),
                         "--server.address", "127.0.0.1", "--server.port", str(port),
                         "--server.headless", "true", "--browser.gatherUsageStats", "false"],
                        stdout=log_ui, **options)
                    processus.append(interface)
                    _attendre(f"http://127.0.0.1:{port}/_stcore/health", interface, arret)
                    adresse = f"http://127.0.0.1:{port}"
                    print(f"Application disponible : {adresse}\nCtrl+C pour fermer.", flush=True)
                    if ouvrir:
                        webbrowser.open(adresse)
                    while not arret.wait(0.25):
                        if any(p.poll() is not None for p in processus):
                            raise RuntimeError("L'application s'est arrêtée. Relancez-la pour continuer.")
                finally:
                    for p in reversed(processus):
                        if p.poll() is None:
                            if os.name == "nt":
                                # Le lanceur du venv Windows a un processus Python enfant.
                                subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"],
                                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                               check=False, creationflags=subprocess.CREATE_NO_WINDOW)
                            else:
                                p.terminate()
                            try:
                                p.wait(timeout=5)
                            except subprocess.TimeoutExpired:
                                p.kill()
                                p.wait(timeout=5)
        return 0
    except (KeyboardInterrupt, InterruptedError):
        return 0
    except (OSError, ValueError, RuntimeError) as erreur:
        print(str(erreur), file=sys.stderr)
        return 1
