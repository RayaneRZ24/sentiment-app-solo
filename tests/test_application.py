"""Le lancement client démarre les vrais services et nettoie ses propres processus."""
import socket
import threading
import time
from pathlib import Path

import httpx
import pytest

from sentiment_app.application import lancer

RACINE = Path(__file__).resolve().parents[1]
pytestmark = pytest.mark.skipif(not (RACINE / "models/sentiment.joblib").exists(),
                                reason="modèle de démonstration absent")


def port_libre():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def test_le_lancement_ne_remplace_pas_un_service_existant(capsys):
    with socket.socket() as occupe:
        occupe.bind(("127.0.0.1", 0))
        assert lancer(occupe.getsockname()[1], port_libre(), ouvrir=False) == 1
        assert occupe.getsockname()[1] > 0
    assert "déjà utilisé" in capsys.readouterr().err


def test_application_reelle_et_arret_des_deux_services():
    api_port, ui_port = port_libre(), port_libre()
    while ui_port == api_port:
        ui_port = port_libre()
    stop = threading.Event()
    codes = []
    t = threading.Thread(target=lambda: codes.append(
        lancer(api_port, ui_port, ouvrir=False, arret=stop)), daemon=True)
    t.start()
    try:
        fin = time.monotonic() + 60
        while time.monotonic() < fin:
            try:
                if httpx.get(f"http://127.0.0.1:{ui_port}/_stcore/health", timeout=1).status_code == 200:
                    break
            except httpx.TransportError:
                pass
            assert t.is_alive(), "le lancement a échoué"
            time.sleep(0.2)
        else:
            pytest.fail("interface non disponible dans le délai")
        r = httpx.post(f"http://127.0.0.1:{api_port}/predict", timeout=5,
                       json={"text": "Livraison rapide, produit conforme, très satisfait"})
        assert r.status_code == 200 and r.json()["label"] == "POSITIVE"
    finally:
        stop.set()
        t.join(timeout=15)
    assert not t.is_alive() and codes == [0]
    for port in (api_port, ui_port):
        with socket.socket() as s:
            assert s.connect_ex(("127.0.0.1", port)) != 0
