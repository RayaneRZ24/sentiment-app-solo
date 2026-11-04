# Fiche modèle : sentiment-app

## Identité du modèle

TF-IDF et régression logistique, paquet 0.6.0. Modèle de démonstration entraîné le 28 octobre 2026 ; fiche vérifiée le 4 novembre 2026.

## Usage prévu

Aider une équipe de relation client à trier les avis en français : positifs, négatifs ou à vérifier. Le résultat guide une relecture et une réponse.

## Usages exclus

Ne pas analyser les personnes ni prendre de décision automatique sur un client. Ne pas appliquer sans nouvelle évaluation à une autre langue ou à un autre domaine.

## Données d'entraînement

290 avis synthétiques de démonstration : 145 positifs, 145 négatifs ; découpage stratifié, graine 42, avant vectorisation : 232 entraînement et 58 test. Ce corpus ne représente pas toute la clientèle réelle.

## Performances mesurées

`models/metrics.json` : F1 macro **0.879**, rappel négatif **0.931**, exactitude 0.8793. Au seuil 0,60 : 42/58 avis traités (72,4 %), 16 vers un humain, 2 erreurs automatiques contre 7 sans abstention ; exactitude sur les réponses : 40/42 = 95,2 %. Ces mesures portent sur un petit jeu jamais vu à l'entraînement.

## Limites connues

Les 7 erreurs de test concernent les retournements : « Taille trop petite […] sauf que ensuite produit conforme […] » est classé négatif à 0,5335 avant abstention. Sur les 20 avis du jeu d'or : 5 justes, 11 abstentions et 4 erreurs franches déclarées en xfail strict.

## Biais mesurés

17 avis avec retournement : exactitude 0,588, 7 erreurs ; 41 directs : 1,000. Les 10 avis longs sans retournement sont tous corrects : longueur et retournement se confondent ici. À 0,60, 15/17 retournements partent en relecture et deux erreurs subsistent. Aucune équité démographique n'a été mesurée.

## Explicabilité

SHAP explique la sortie linéaire : base −0,0114 + contributions = −0,1343 pour l'avis mitigé ; 20 termes négatifs contre 13 positifs. Les mots-outils « je », « en », « au » révèlent des tournures apprises. Cette décomposition explique le modèle, pas une causalité réelle.

## Conditions d'usage

Un humain relit les avis indéterminés, vérifie les formulations ambiguës et contrôle régulièrement des réponses automatiques. La confiance n'est pas une garantie de justesse ; aucune sanction ni décision sur une personne ne repose sur ce seul classement.

## Maintenance

Suivre erreurs et charge de relecture ; réévaluer avant tout changement de domaine ou réentraînement. Entraîner et relire avec scikit-learn 1.5.x (poste : 1.5.2). Distribuer le modèle séparément, définir SENTIMENT_MODELE et mettre cette fiche à jour avec ses métriques.

Mesures et commandes reproductibles : `docs/verification/complements-c6-*`, `complements-t27a-*`, `tp4-courbe-abstention.txt` et `tp4-bilan-jeu-or.txt` dans le dépôt de développement.
