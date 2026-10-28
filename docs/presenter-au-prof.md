# Présenter le projet solo

## Préparer PowerShell

```powershell
cd "C:\Users\NITRO 5\Downloads\sentiment-app-solo"
.\.venv\Scripts\Activate.ps1
```

Si l'activation est refusée, remplacer python par `.\.venv\Scripts\python.exe` et sentiment par `.\.venv\Scripts\sentiment.exe`. Sur un nouveau clone : créer .venv, installer requirements.txt et requirements-dev.txt, puis `python -m pip install -e ".[ui]"`.

## Avancement et résultats des vrais checkpoints

```powershell
git log --oneline -20
git tag --list
git status
git shortlog -sn --all
git show tp1-valide:docs/verification/tp1-tests.txt
git show tp2-valide:docs/verification/tp2-tests.txt
git show tp3-valide:docs/verification/tp3-tests.txt
git show tp4-valide:docs/verification/tp4-tests.txt
git show tp5-valide:docs/verification/tp5-tests.txt
git show v0.6.0:docs/verification/tp6-tests.txt
```

Les tags pointent vers les étapes réellement poussées et testées. La règle d'un auteur est l'adaptation déclarée à la consigne solo ; les contributions du projet source restent attribuées dans le README.

## Refaire tous les tests aujourd'hui

```powershell
python scripts/check_setup.py
python src/make_demo.py
python src/train.py
python -m pytest -q
python -m pytest tests/ -v
ruff check .
mypy api
python -m pytest -q --cov=api --cov-report=term-missing --cov-fail-under=95
```

Attendu au TP6 : **105 passed, 4 xfailed**, couverture API au moins 95 %. Les quatre xfail sont des erreurs connues conservées dans le jeu d'or ; elles ne sont pas des réussites du modèle.

## Montrer les tests de chaque TP

```powershell
python -m pytest tests/test_cadrage.py tests/test_environment.py tests/test_git_history.py -q
python -m pytest tests/test_model.py -q
python -m pytest tests/test_api.py -q
python -m pytest tests/test_limites.py tests/test_integration.py tests/test_abstention.py tests/test_jeu_or.py -q
python -m pytest tests/test_client.py tests/test_interface.py -q
python -m pytest tests/test_packaging.py -q
```

Les fichiers sont cumulés au fur et à mesure des étapes ; les journaux des tags montrent leurs comptes respectifs avant les ajouts suivants.

## Démonstration API et Streamlit

Premier terminal activé :

```powershell
sentiment serve
```

Ouvrir http://127.0.0.1:8000/docs et tester /health puis /predict. Dans un deuxième terminal, même dossier et environnement activé :

```powershell
sentiment ui
```

Ouvrir http://localhost:8501. Montrer un avis positif, un négatif, le texte inconnu `xqzvb wlkptr grombu`, trois espaces et le fichier data/avis_exemple.csv. Montrer le téléchargement et le résumé : 3 positifs, 2 négatifs, 1 abstention. Arrêter l'API puis recharger la page pour montrer l'erreur d'indisponibilité.

## Démonstration TP6

```powershell
sentiment --version
sentiment predict "Livraison rapide, produit conforme, très satisfait"
sentiment predict "xqzvb wlkptr grombu"
python -m build --wheel
```

Attendu : version 0.6.0, POSITIVE puis INDETERMINE. Les preuves de la roue installée dans un venv neuf hors dépôt, sans puis avec SENTIMENT_MODELE, sont dans docs/verification/tp6-hors-depot-*.txt. La roue est générée localement dans dist/ et reste ignorée par Git.

Les liens vers les six exécutions CI réussies figurent dans le journal. Le professeur doit disposer d'un accès au dépôt privé pour les consulter.

Pour tout rejouer en une commande : `.\scripts\verifier.ps1 -Detail`.
