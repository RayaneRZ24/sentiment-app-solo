# TP5 individuel : interface HTTP

Les 7 tests du client et les 5 tests de la page Streamlit sont rejoués avec succès. Des essais réels ont également été réalisés dans un navigateur ; les captures et le CSV téléchargé se trouvent dans docs/captures/ et docs/verification/.

La page appelle l'API par HTTP via ui/client.py ; elle n'importe pas le modèle. L'API conserve la validation, la correspondance des étiquettes et l'abstention. Un modèle remplacé côté service ne nécessite pas de changer le client.

Un texte inconnu reçoit INDETERMINE : la page affiche « Je ne sais pas : à faire vérifier par un humain » et explique le seuil. Cela préserve l'incertitude au lieu de forcer une étiquette. Les espaces sont traduits en avertissement, le 503 en message de modèle non chargé, et une API arrêtée en message « API injoignable ».

Le fichier avis_exemple.csv comporte six avis : trois positifs, deux négatifs, une abstention ; un avis sur six nécessite une relecture. La page affiche le tableau, le résumé et le téléchargement CSV.

## Complément T34a : deux graphiques, 4 novembre 2026

Le module `ui/graphiques.py` et ses quatre tests sont repris du complément étudiant d’A. Larhlimi. La page affiche la répartition des verdicts et l’histogramme des confiances, calculés depuis les réponses HTTP. Les catégories vides restent à zéro et les refus ne sont pas comptés comme des confiances.

Les [neuf tests de graphiques et de page](verification/complements-t34a-tests.txt) vérifient le fichier d’exemple : 3 positifs, 2 négatifs et 1 avis à vérifier ; les tranches de confiance contiennent respectivement 1, 1, 3, 1 et 0 avis. L’histogramme montre combien de résultats sont proches du seuil de décision ; la confiance n’est pas une garantie de justesse.
