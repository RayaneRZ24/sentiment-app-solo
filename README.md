# sentiment-app-solo

Travail individuel d'**Ahmed Rayane Ramzi** (@RayaneRZ24), adapté le 28 octobre 2026 à la consigne de travail en solo. Étape actuelle : **TP6**.

## Origine du code

Ce dépôt réutilise le code du [projet de binôme](https://github.com/OthmaneW37/OthmaneMoussawi-A---AhmedRayaneRamzi-B), référence `ff79dc84d25fe76e84f79b8348ba8c49ff585b57`, ainsi que les kits étudiants d'A. Larhlimi. Les contributions antérieures d'Othmane Moussawi et d'Ahmed Rayane Ramzi sont reconnues : cette reprise ne revendique pas une écriture entièrement nouvelle du code. Le nouvel historique décrit les adaptations et les vérifications individuelles réellement réalisées, dans l'ordre des TP.

La consigne solo remplace le contrôle de deux auteurs par le contrôle d'un auteur unique dans les tests et le diagnostic. Les seuils du modèle et les autres exigences techniques restent inchangés.

## Installation et tests

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pip install -e ".[ui]"
python src/make_demo.py
python src/train.py
python scripts/check_setup.py
python -m pytest -q
```

`requirements.txt` contient les dépendances nécessaires aux TP atteints, sans installer les bibliothèques des semaines futures. `requirements.lock` conserve les versions du poste Windows. Le modèle et les données générées ne sont jamais commités.

Les résultats de chaque TP sont conservés dans [le journal solo](docs/journal-solo-tp1-tp6.md) et dans `docs/verification/`. Chaque étape validée possède son repère Git (`tp1-valide` à `tp5-valide`, puis `v0.6.0`) et sa propre exécution GitHub Actions.

```powershell
git log --oneline -20
git status
python -m pytest tests/ -v
```

Les erreurs connues du modèle sont documentées en `xfail(strict=True)` à partir du TP4 ; une abstention n'est pas présentée comme une prédiction correcte.
