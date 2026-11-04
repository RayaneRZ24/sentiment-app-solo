"""Installation et lancement local de l'application livrée (Python 3.11 conseillé)."""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import venv
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Installer et ouvrir l'analyse des avis clients.")
    parser.add_argument("--verifier", action="store_true", help="installer et vérifier, puis quitter")
    parser.add_argument("--sans-navigateur", action="store_true")
    parser.add_argument("--api-port", type=int, default=8000)
    parser.add_argument("--port", type=int, default=8501)
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        print("Python 3.11 ou plus récent est nécessaire ; Python 3.11 est conseillé.")
        return 1
    dossier = Path(__file__).resolve().parent
    roues = sorted(dossier.glob("sentiment_app-*.whl"))
    modele = dossier / "modele" / "sentiment.joblib"
    if len(roues) != 1 or not modele.is_file():
        print("Livraison incomplète : extrayez toute l'archive avant de lancer l'installation.")
        return 1
    environnement = dossier / ".venv-client"
    scripts = environnement / ("Scripts" if os.name == "nt" else "bin")
    python = scripts / ("python.exe" if os.name == "nt" else "python")
    commande = scripts / ("sentiment.exe" if os.name == "nt" else "sentiment")
    marque = environnement / "livraison.sha256"
    empreinte = hashlib.sha256(roues[0].read_bytes()).hexdigest()
    try:
        if not python.is_file():
            print("Préparation de votre installation…", flush=True)
            venv.EnvBuilder(with_pip=True).create(environnement)
        if not marque.is_file() or marque.read_text().strip() != empreinte or not commande.is_file():
            print("Installation de l'application et de ses dépendances…", flush=True)
            subprocess.run([str(python), "-m", "pip", "install", f"{roues[0]}[ui]"], check=True)
            marque.write_text(empreinte + "\n", encoding="ascii")
        variables = dict(os.environ, SENTIMENT_MODELE=str(modele), PYTHONUTF8="1")
        if args.verifier:
            subprocess.run([str(python), "-m", "pip", "check"], check=True, env=variables)
            subprocess.run([str(commande), "--version"], check=True, env=variables)
            return subprocess.run([str(commande), "predict", "Livraison rapide, produit conforme, très satisfait"],
                                  env=variables, check=False).returncode
        return subprocess.run([str(commande), "start", "--api-port", str(args.api_port),
                               "--port", str(args.port),
                               *(["--sans-navigateur"] if args.sans_navigateur else [])],
                              env=variables, check=False).returncode
    except KeyboardInterrupt:
        return 0
    except (OSError, subprocess.CalledProcessError) as erreur:
        print(f"Installation impossible : {erreur}. Vérifiez la connexion et l'accès au dossier.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
