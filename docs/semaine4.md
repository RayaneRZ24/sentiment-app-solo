# TP4 individuel : défauts et qualité

Mesures rejouées le 28 octobre 2026 dans le projet solo. Les fichiers du projet source sont réutilisés pour les corrections, avec leur origine reconnue dans le README.

La couverture et les remarques initiales sont dans `docs/verification/tp4-couverture-avant.txt`, `tp4-ruff-avant.txt` et `tp4-mypy-avant.txt`. Les tests limites et intégration ajoutés avant les corrections révèlent le refus non uniforme des blancs, la conversion d'une panne ValueError en 422 et l'absence de vérification des classes du modèle. La sortie initiale est conservée dans `tp4-defauts-avant.txt`.

Les corrections sont un validateur de blancs utilisant str.strip(), des réponses 500 génériques pour les pannes, et une correspondance typée des étiquettes vérifiée au démarrage. La couverture finale de l'API dépasse 95 % sans exclusion de lignes. Les 11 tests aux limites, dont les deux propriétés Hypothesis, passent trois fois de suite.

Sur les 58 avis de test, le seuil 0,60 répond à 42 avis, envoie 16 avis vers un humain et laisse 2 erreurs automatiques contre 7 au seuil 0,50. Monter à 0,70 envoie 21 avis vers un humain et ne laisse aucune erreur sur ce petit jeu. Le seuil 0,60 limite la charge de relecture, sans garantir la fiabilité sur un autre domaine.

Les 20 avis de référence sont repris du projet source et leurs étiquettes ont été relues ; ils ne sont pas présentés comme nouvellement écrits par deux personnes. Le bilan est conservé dans `tp4-bilan-jeu-or.txt` : 5 justes, 11 abstentions et 4 erreurs franches déclarées. Ces erreurs restent visibles avec xfail strict ; les textes et les attentes ne sont pas modifiés pour améliorer le résultat.

Ruff et mypy ne détectaient pas ces défauts de comportement ; les tests exécutés sont indispensables en plus du contrôle de types et du lint. Le crochet local est installé, et la CI exécute ruff, mypy et pytest avec 95 % de couverture minimale.
