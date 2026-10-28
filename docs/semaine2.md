# TP2 individuel : modèle et mesures

Expériences rejouées le 28 octobre 2026. Code repris du projet source cité dans le README.

Le jeu de démonstration contient 290 avis (145 par classe). Le découpage précède la vectorisation : 232 avis d'entraînement, 58 avis de test. F1 macro mesuré : 0.879. La matrice et les erreurs sont dans [l'évaluation](verification/tp2-evaluation-demo.txt).

Les erreurs concernent les avis mitigés : TF-IDF ne comprend pas le retournement d'une phrase malgré les bigrammes. Une représentation contextuelle ou davantage d'avis représentatifs pourraient améliorer le modèle. Le TP4 mesurera l'abstention au lieu de cacher ces erreurs.

L'expérience Allociné a été réussie ; les nouvelles métriques sont enregistrées dans docs/verification/tp2-metrics-allocine.json. Le modèle actif est ensuite réentraîné sur la démonstration pour être identique à celui des tests API et de la CI.
