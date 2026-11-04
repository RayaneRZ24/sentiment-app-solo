"""Installe la livraison hors dépôt et vérifie les services issus de la roue."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from zipfile import ZipFile

SONDE = r'''
import json, socket, sys, threading, time, urllib.request
from pathlib import Path
import sentiment_app
from sentiment_app.application import lancer

def libre():
    with socket.socket() as s:
        s.bind(('127.0.0.1',0))
        return s.getsockname()[1]

pret, fin = map(Path,sys.argv[1:3])
a,b=libre(),libre()
while b==a: b=libre()
stop=threading.Event()
codes=[]
t=threading.Thread(target=lambda: codes.append(lancer(a,b,ouvrir=False,arret=stop)),daemon=True)
t.start()
try:
    limite=time.monotonic()+60
    while time.monotonic()<limite:
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{b}/_stcore/health',timeout=1) as r:
                if r.status==200: break
        except (OSError,TimeoutError): pass
        assert t.is_alive(), 'le lancement a echoue'
        time.sleep(.2)
    else: raise RuntimeError('interface indisponible')
    observations={}
    for nom,texte in [('positif','Livraison rapide, produit conforme, tr\u00e8s satisfait'),('inconnu','xqzvb wlkptr grombu')]:
        req=urllib.request.Request(f'http://127.0.0.1:{a}/predict',data=json.dumps({'text':texte}).encode(),headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=5) as r: observations[nom]={'status':r.status,'body':json.load(r)}
    assert observations['positif']['body']['label']=='POSITIVE'
    assert observations['inconnu']['body']['label']=='INDETERMINE'
    origine=Path(sentiment_app.__file__).resolve()
    assert origine.is_relative_to(Path(sys.prefix).resolve()), str(origine)
    result={'version':sentiment_app.__version__,'origine_paquet':str(origine),'prefix':sys.prefix,'api_url':f'http://127.0.0.1:{a}','ui_url':f'http://127.0.0.1:{b}','predictions':observations}
    pret.write_text(json.dumps(result),encoding='utf-8')
    limite=time.monotonic()+180
    while not fin.exists() and time.monotonic()<limite: time.sleep(.2)
finally:
    stop.set()
    t.join(timeout=15)
assert not t.is_alive() and codes==[0], codes
for port in (a,b):
    with socket.socket() as s: assert s.connect_ex(('127.0.0.1',port))!=0
print('ARRET_DES_DEUX_SERVICES_OK',flush=True)
'''


def executer(args: list[str], dossier: Path, env: dict) -> subprocess.CompletedProcess:
    r = subprocess.run(args, cwd=dossier, env=env, text=True, encoding="utf-8",
                       errors="replace", capture_output=True, timeout=600)
    print(r.stdout, end="", flush=True)
    if r.stderr:
        print(r.stderr, end="", flush=True)
    if r.returncode:
        raise RuntimeError(f"Commande en échec ({r.returncode}) : {args[:3]}")
    return r


def captures_navigateur(args, livraison: Path, observation: dict) -> dict:
    sys.path.insert(0, str(args.playwright_lib))
    from playwright.sync_api import sync_playwright

    dossier = args.captures.resolve()
    dossier.mkdir(parents=True, exist_ok=True)
    resultat = {}
    with sync_playwright() as p:
        navigateur = p.chromium.launch(executable_path=str(args.chromium), headless=True)
        page = navigateur.new_page(viewport={"width": 1440, "height": 1800}, locale="fr-FR")
        page.goto(observation["ui_url"])
        page.get_by_text("Service d’analyse disponible.", exact=True).wait_for(timeout=30000)
        page.screenshot(path=str(dossier / "client-accueil.png"), full_page=True)
        for nom, texte, verdict in [
            ("positif", "Livraison rapide, produit conforme, très satisfait", "Avis positif"),
            ("a-verifier", "xqzvb wlkptr grombu", "Je ne sais pas : à faire vérifier par un humain")]:
            page.get_by_label("Avis client").fill(texte)
            page.get_by_role("button", name="Analyser", exact=True).click()
            page.get_by_text(verdict, exact=True).wait_for()
            page.screenshot(path=str(dossier / f"client-avis-{nom}.png"), full_page=True)
        page.get_by_role("tab", name="Un fichier d'avis", exact=True).click()
        page.locator('input[type=file]').set_input_files(str(livraison / "exemple-avis.csv"))
        page.get_by_role("button", name="Télécharger les résultats", exact=True).wait_for()
        page.get_by_text("Répartition des verdicts", exact=True).wait_for()
        page.get_by_text("Confiance du modèle, par tranche", exact=True).wait_for()
        page.get_by_test_id("stVegaLiteChart").first.wait_for()
        resultat["graphiques"] = page.get_by_test_id("stVegaLiteChart").count()
        assert resultat["graphiques"] == 2, "deux graphiques attendus"
        texte = page.inner_text("body")
        for interne in ("src/train.py", "uvicorn", "models/sentiment.joblib", "TP2", "Deploy"):
            assert interne not in texte
        resultat["resume"] = page.get_by_text("3 positifs · 2 négatifs · 1 à vérifier", exact=False).inner_text()
        page.screenshot(path=str(dossier / "tp5-t34a-graphiques.png"), full_page=True)
        with page.expect_download() as telechargement:
            page.get_by_role("button", name="Télécharger les résultats", exact=True).click()
        fichier = dossier.parent / "verification/client-resultats-exemple.csv"
        telechargement.value.save_as(str(fichier))
        resultat["csv_resultats"] = fichier.name
        page.locator('input[type=file]').set_input_files({"name": "illisible.csv", "mimeType": "text/csv", "buffer": b'\xff\xfe\x00'})
        page.get_by_text("Fichier illisible : utilisez un CSV UTF-8 avec une colonne text.", exact=True).wait_for()
        page.screenshot(path=str(dossier / "client-csv-refuse.png"), full_page=True)
        navigateur.close()
    return resultat


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--rapport", type=Path)
    parser.add_argument("--captures", type=Path)
    parser.add_argument("--playwright-lib", type=Path)
    parser.add_argument("--chromium", type=Path)
    args = parser.parse_args()
    env = dict(os.environ, PYTHONUTF8="1")
    env.pop("PYTHONPATH", None)
    env.pop("SENTIMENT_MODELE", None)
    with tempfile.TemporaryDirectory(prefix="sentiment-livraison-") as temporaire:
        livraison = Path(temporaire) / "application"
        livraison.mkdir()
        with ZipFile(args.archive.resolve()) as archive:
            for nom in archive.namelist():
                if not (livraison / nom).resolve().is_relative_to(livraison.resolve()):
                    raise ValueError(nom)
            archive.extractall(livraison)
        manifeste = json.loads((livraison / "MANIFESTE.json").read_text(encoding="utf-8"))
        for nom, sha in manifeste["sha256"].items():
            assert hashlib.sha256((livraison / nom).read_bytes()).hexdigest() == sha
        executer([sys.executable, str(livraison / "installer.py"), "--verifier"], livraison, env)
        python = livraison / ".venv-client" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        controles = executer([str(python), "-c", "import importlib.util,json; noms=['pytest','shap','ruff','mypy','hypothesis']; r={n:bool(importlib.util.find_spec(n)) for n in noms}; print(json.dumps(r)); assert not any(r.values())"], livraison, env)
        sans_modele = subprocess.run([str(python), "-c", "from sentiment_app.cli import main; raise SystemExit(main(['predict','Un avis']))"], cwd=temporaire, env=env, capture_output=True, text=True, encoding="utf-8")
        assert sans_modele.returncode == 1 and "SENTIMENT_MODELE" in sans_modele.stderr
        print("Sans modèle configuré : refus attendu, code 1.", flush=True)
        sonde = Path(temporaire) / "sonde.py"
        sonde.write_text(SONDE, encoding="utf-8")
        pret, arret = Path(temporaire) / "pret.json", Path(temporaire) / "arret"
        client_env = dict(env, SENTIMENT_MODELE=str(livraison / "modele/sentiment.joblib"))
        with (Path(temporaire) / "sonde.log").open("w", encoding="utf-8") as log:
            processus = subprocess.Popen([str(python), str(sonde), str(pret), str(arret)],
                                         cwd=temporaire, env=client_env, stdout=log, stderr=subprocess.STDOUT,
                                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            try:
                limite = time.monotonic() + 90
                while time.monotonic() < limite:
                    if pret.exists():
                        try:
                            observation = json.loads(pret.read_text(encoding="utf-8"))
                            break
                        except json.JSONDecodeError:
                            pass
                    if processus.poll() is not None:
                        raise RuntimeError((Path(temporaire) / "sonde.log").read_text(encoding="utf-8"))
                    time.sleep(0.2)
                else:
                    raise RuntimeError("Délai d'installation et de démarrage dépassé")
                if args.captures:
                    observation["navigateur"] = captures_navigateur(args, livraison, observation)
            finally:
                arret.write_text("stop", encoding="ascii")
                processus.wait(timeout=70)
        sortie = (Path(temporaire) / "sonde.log").read_text(encoding="utf-8")
        print(sortie, end="", flush=True)
        assert processus.returncode == 0 and "ARRET_DES_DEUX_SERVICES_OK" in sortie
        observation.update({"archive": args.archive.name, "sha256_archive": hashlib.sha256(args.archive.read_bytes()).hexdigest(),
                            "outils_developpement_installes": json.loads(controles.stdout),
                            "sans_modele_code": sans_modele.returncode, "arret_deux_services": True})
        if args.rapport:
            args.rapport.write_text(json.dumps(observation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(observation, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
