# Analyse des avis clients — version 0.6.1

L’application classe des avis en français en **positifs**, **négatifs** ou **à vérifier**. Elle propose une analyse individuelle, un import CSV, deux graphiques et l’export des résultats. Le traitement s’exécute sur votre ordinateur ; aucun compte n’est nécessaire.

## Installation de la livraison complète

1. Installez Python 3.11 et extrayez entièrement l’archive `sentiment-app-client-0.6.1.zip` dans un dossier où vous pouvez écrire.
2. Ouvrez un terminal dans ce dossier, puis lancez `python installer.py` (ou `py -3.11 installer.py` sous Windows).
3. Au premier lancement, une connexion Internet est nécessaire pour installer les dépendances. Le navigateur s’ouvre ensuite sur l’application locale.

L’installateur crée son environnement `.venv-client`, installe seulement les dépendances de l’application et sélectionne le modèle fourni. Il ne télécharge pas le dépôt ni les outils de développement. Relancez la même commande pour réutiliser l’installation. Gardez le terminal ouvert ; **Ctrl+C** ferme l’application et son service.

## Utilisation

- **Un avis** : saisissez entre 1 et 2 000 caractères, puis cliquez sur **Analyser**.
- **Un fichier d’avis** : importez un CSV UTF-8 contenant une colonne `text`. Le fichier `exemple-avis.csv` permet de découvrir ce format. Le tableau et les graphiques résument les réponses ; **Télécharger les résultats** enregistre le CSV analysé.
- **À vérifier** : la confiance est inférieure à 60 %. Un humain doit relire l’avis avant toute décision. Une confiance élevée ne garantit pas une réponse juste.

Ne fermez pas le terminal pendant l’utilisation. Si un port est occupé : `python installer.py --api-port 18000 --port 18501`. Pour ne pas ouvrir de navigateur automatiquement : `python installer.py --sans-navigateur`.

## Limites et confidentialité

Le modèle est une démonstration entraînée sur 290 avis synthétiques. Il se trompe notamment sur les avis mitigés et les retournements de sens ; consultez la fiche modèle jointe. Il aide au tri, sans prendre de décision sur une personne. Utilisez de préférence des avis sans données personnelles. Les services sont limités à `127.0.0.1` ; l’installation peut contacter les serveurs de paquets, puis l’analyse est locale. Des outils tiers ou votre navigateur peuvent conserver leurs propres traces.

## Installation manuelle de la roue

Pour les personnes qui administrent l’installation, créez un environnement Python 3.11, puis :

```text
python -m pip install "./sentiment_app-0.6.1-py3-none-any.whl[ui]"
```

Définissez `SENTIMENT_MODELE` avec le chemin absolu de `modele/sentiment.joblib`, puis exécutez `sentiment start`. Sous PowerShell : `$env:SENTIMENT_MODELE = (Resolve-Path .\modele\sentiment.joblib).Path`. Sous Linux/macOS : `export SENTIMENT_MODELE="$PWD/modele/sentiment.joblib"`.

Les commandes `sentiment --version`, `sentiment predict "Mon avis"`, `sentiment serve` et `sentiment ui` restent disponibles. Le modèle doit être relu avec scikit-learn 1.5.x, installé automatiquement. La roue ne contient ni données d’entraînement, ni tests, ni journal de développement.

Cette livraison est vérifiée sur Windows et par la CI Linux. Un installateur natif `.exe` ou une compatibilité avec toutes les versions de Python n’est pas revendiqué. L’archive n’installe pas un service hébergé sur Internet.
