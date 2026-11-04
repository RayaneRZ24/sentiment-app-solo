# TP2 individuel : modèle et mesures

Expériences rejouées le 28 octobre 2026. Code repris du projet source cité dans le README.

Le jeu de démonstration contient 290 avis (145 par classe). Le découpage précède la vectorisation : 232 avis d'entraînement, 58 avis de test. F1 macro mesuré : 0.879. La matrice et les erreurs sont dans [l'évaluation](verification/tp2-evaluation-demo.txt).

Les erreurs concernent les avis mitigés : TF-IDF ne comprend pas le retournement d'une phrase malgré les bigrammes. Une représentation contextuelle ou davantage d'avis représentatifs pourraient améliorer le modèle. Le TP4 mesurera l'abstention au lieu de cacher ces erreurs.

L'expérience Allociné a été réussie ; les nouvelles métriques sont enregistrées dans docs/verification/tp2-metrics-allocine.json. Le modèle actif est ensuite réentraîné sur la démonstration pour être identique à celui des tests API et de la CI.

## Complément C6 : explicabilité, 4 novembre 2026

Le module `src/expliquer.py` et ses quatre tests sont repris du complément étudiant d’A. Larhlimi (archive du 2 novembre 2026). Les résultats sont mesurés sur notre modèle de démonstration, sans reprendre le corrigé enseignant.

Les mots-outils « je », « en » et « au » figurent parmi les termes influents : le modèle apprend les tournures du petit jeu de démonstration, pas seulement le sentiment. Sur l’avis mitigé, les contributions positives et négatives se compensent presque ; la décomposition SHAP explique la sortie du modèle, sans constituer une explication causale du monde. Les nombres observés et la vérification de l’additivité figurent dans [la sortie C6](verification/complements-c6-explication.txt).

SHAP est installé par `requirements-dev.txt`, utilisé par la CI ; il ne fait pas partie des dépendances de l’application livrée.
