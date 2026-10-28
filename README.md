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

## Résultats par étape

| Étape | Tests locaux | Repère | CI |
| --- | --- | --- | --- |
| TP1 | 38 passed in 2.04s | `tp1-valide` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40731654315) |
| TP2 | 42 passed in 2.23s | `tp2-valide` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40731888889) |
| TP3 | 48 passed, 1 warning in 3.09s | `tp3-valide` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40732096196) |
| TP4 | 87 passed, 4 xfailed, 1 warning in 7.02s | `tp4-valide` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40732610139) |
| TP5 | 99 passed, 4 xfailed, 1 warning in 11.28s | `tp5-valide` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40733058617) |
| TP6 | 105 passed, 4 xfailed, 1 warning in 10.99s | `v0.6.0` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40733697516) |

Le dossier de travail personnel est `C:\Users\NITRO 5\Downloads\sentiment-app-solo`. [Présenter le projet au professeur](docs/presenter-au-prof.md).

```powershell
python -m pip install -e ".[ui]"
sentiment --version
sentiment predict "Livraison rapide, produit conforme, très satisfait"
sentiment serve
# Dans un autre terminal activé : sentiment ui
```

Le TP6 est terminé : paquet 0.6.0, roue vérifiée dans un environnement neuf hors dépôt et étape CI de la roue réussie. Le modèle reste extérieur au paquet ; utiliser `SENTIMENT_MODELE` hors du dossier source. La fiche de choix d'un projet d'agent IA est un livrable séparé et n'est pas remplie avec un numéro de sujet inventé.
