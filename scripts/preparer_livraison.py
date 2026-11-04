"""Assemble la livraison client, sans les ressources de développement du dépôt."""
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

RACINE = Path(__file__).resolve().parents[1]


def main() -> int:
    from sentiment_app import __version__

    dist = RACINE / "dist"
    roue = dist / f"sentiment_app-{__version__}-py3-none-any.whl"
    modele = RACINE / "models/sentiment.joblib"
    with ZipFile(roue) as archive:
        for nom in archive.namelist():
            racine = nom.split("/", 1)[0]
            if racine not in {"sentiment_app", "api", "ui"} and not racine.endswith(".dist-info"):
                raise ValueError(f"Ressource inattendue dans la roue : {nom}")
        metadata = next(n for n in archive.namelist() if n.endswith(".dist-info/METADATA"))
        texte = archive.read(metadata).decode("utf-8")
        for outil in ("pytest", "shap", "ruff", "mypy", "hypothesis", "pre-commit"):
            if any(ligne.lower().startswith("requires-dist: " + outil) for ligne in texte.splitlines()):
                raise ValueError(f"Dépendance de développement dans la roue : {outil}")
        if "captures-tp1-tp6" in texte or "Journal de bord individuel" in texte:
            raise ValueError("Le journal de développement est embarqué dans les métadonnées")
    fiche = (RACINE / "docs/fiche-modele.md").read_text(encoding="utf-8")
    fiche = fiche.split("\nMesures et commandes reproductibles", 1)[0].rstrip() + "\n"
    fichiers = {
        roue.name: roue.read_bytes(),
        "modele/sentiment.joblib": modele.read_bytes(),
        "NOTICE.md": (RACINE / "docs/notice-utilisateur.md").read_bytes(),
        "FICHE-MODELE.md": fiche.encode("utf-8"),
        "installer.py": (RACINE / "distribution/installer.py").read_bytes(),
        "exemple-avis.csv": (RACINE / "data/avis_exemple.csv").read_bytes(),
        "METRIQUES.json": (RACINE / "models/metrics.json").read_bytes(),
    }
    manifeste = {"application": "sentiment-app", "version": __version__,
                 "modele_separe": True, "python_conseille": "3.11",
                 "sha256": {n: hashlib.sha256(b).hexdigest() for n, b in fichiers.items()}}
    fichiers["MANIFESTE.json"] = (json.dumps(manifeste, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    fichiers["SHA256SUMS.txt"] = "".join(
        f"{hashlib.sha256(b).hexdigest()}  {n}\n" for n, b in fichiers.items()).encode("ascii")
    cible = dist / f"sentiment-app-client-{__version__}.zip"
    with ZipFile(cible, "w", ZIP_DEFLATED) as archive:
        for nom, contenu in fichiers.items():
            archive.writestr(nom, contenu)
    print(json.dumps({"livraison": str(cible), "octets": cible.stat().st_size,
                      "fichiers": list(fichiers), "sha256": hashlib.sha256(cible.read_bytes()).hexdigest()},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
