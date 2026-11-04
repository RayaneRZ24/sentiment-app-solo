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

Attendu avec les compléments et le lancement client : **137 passed, 4 xfailed**, couverture API au moins 95 %. Les quatre xfail sont des erreurs connues conservées dans le jeu d'or ; elles ne sont pas des réussites du modèle.

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

Attendu : version 0.6.1, POSITIVE puis INDETERMINE. Le tag v0.6.0 conserve le checkpoint initial du TP6. Les preuves de la roue installée dans un venv neuf hors dépôt, sans puis avec SENTIMENT_MODELE, sont dans docs/verification/tp6-hors-depot-*.txt. La roue est générée localement dans dist/ et reste ignorée par Git.

Les liens vers les six exécutions CI réussies figurent dans le journal. Le dépôt est actuellement public (vérification du 4 novembre 2026) ; le professeur peut consulter directement ces liens.

Pour tout rejouer en une commande : `.\scripts\verifier.ps1 -Detail`.

## Compléments du 2 novembre, vérifiés le 4 novembre

```powershell
python src/expliquer.py
python -m pytest tests/test_explicabilite.py -q
python src/biais.py
python -m pytest tests/test_biais.py -q
python -m pytest tests/test_graphiques.py tests/test_interface.py -q
python -m pytest tests/test_fiche_modele.py -q
```

Attendus : 4 tests SHAP, 8 tests de biais, 9 tests de graphiques et de page, 14 tests de fiche modèle. Afficher `docs/fiche-modele.md`, expliquer le F1 0,879 et les écarts entre 17 avis avec retournement et 41 avis directs.

## Application client et installation neuve

Depuis le dépôt : `sentiment start` ouvre l'application et son service en une commande. Montrer les deux graphiques du CSV. Ctrl+C ferme les deux services. Les anciens modes serve et ui restent utilisables pour une démonstration séparée de l'API.

```powershell
python -m build --wheel
python scripts/preparer_livraison.py
python scripts/verifier_livraison.py dist/sentiment-app-client-0.6.1.zip
```

La dernière commande extrait la livraison dans un dossier temporaire, exécute son installateur, vérifie l'absence d'outils de développement, teste la vraie API et la page, puis ferme les deux services. Le modèle utilisé vient de l'archive, pas du dossier du projet. Pour un utilisateur final, extraire l'archive puis lancer `python installer.py`. Lire [la notice utilisateur](notice-utilisateur.md).
