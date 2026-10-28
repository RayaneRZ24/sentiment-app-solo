# Journal individuel : TP1 à TP6

**Auteur : Ahmed Rayane Ramzi (@RayaneRZ24).** Expériences rejouées le 28 octobre 2026 dans le nouveau dépôt personnel, à partir d'un clone effectif du projet de binôme et des kits étudiants d'A. Larhlimi.

## Origine et consigne individuelle

Le projet de départ est cité dans le README avec sa révision exacte. Le code et les trois fiches ne sont pas présentés comme entièrement nouveaux. Ce nouvel historique décrit leur reprise, leur adaptation au solo et les tests réellement exécutés. Le contrôle d'historique attend explicitement un auteur unique ; les seuils du modèle et les autres assertions du cours sont conservés.

Aucun commit sous une autre identité, aucune date antérieure inventée et aucune exécution sur un autre ordinateur ne sont attribués à cette reprise. Tous les checkpoints ont été construits et testés dans l'ordre, puis poussés séparément après validation locale. Le checkpoint suivant n'a été commencé qu'après succès de la CI du précédent.

## Checkpoints réels

| Étape | Résultat local | Repère Git | Vérification sur GitHub |
| --- | --- | --- | --- |
| TP1 | 38 passed in 2.04s | `tp1-valide` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40731654315) |
| TP2 | 42 passed in 2.23s | `tp2-valide` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40731888889) |
| TP3 | 48 passed, 1 warning in 3.09s | `tp3-valide` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40732096196) |
| TP4 | 87 passed, 4 xfailed, 1 warning in 7.02s | `tp4-valide` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40732610139) |
| TP5 | 99 passed, 4 xfailed, 1 warning in 11.28s | `tp5-valide` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40733058617) |
| TP6 | 105 passed, 4 xfailed, 1 warning in 10.99s | `v0.6.0` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40733697516) |

Les sorties complètes sont dans `docs/verification/tpN-*.txt`. Les repères permettent de consulter le véritable état des fichiers à chaque étape et les résultats de cette étape, sans reconstruire un historique fictif après coup.

## TP1 — Cadrage et environnement

Environnement Python 3.11 propre au dossier solo ; dépendances nécessaires aux TP concernés, sans les bibliothèques des semaines futures. Les trois fiches sont reprises du projet source et vérifiées. Le diagnostic affiche 0 erreur et 0 avertissement. Les tests exigent un auteur solo et refusent un modèle ou un environnement versionné.

## TP2 — Entraînement et évaluation

290 avis de démonstration, dont 145 positifs et 145 négatifs ; séparation des 232 avis d'entraînement et 58 de test avant vectorisation. F1 macro 0,879 et matrice [[27, 2], [5, 24]]. L'expérience Allociné a été rejouée sur 20 000 avis et ses métriques sont conservées. Le modèle actif est ensuite reconstruit sur la démonstration pour les tests des TP suivants.

## TP3 — API initiale

Le kit initial FastAPI est installé et ses six tests sont validés avant les corrections du TP4. Il ne s'agit pas de copier immédiatement l'état final : les erreurs du kit ont ensuite été reproduites sur cette API.

## TP4 — Défauts et corrections

La mesure initiale de couverture et les remarques de ruff et mypy sont enregistrées. Les tests aux limites et d'intégration complétés donnent initialement 5 échecs et 13 réussites : refus non uniforme des espaces et des blancs Unicode, panne ValueError traitée à tort en 422, et classes inconnues acceptées. Les sorties avant correction restent accessibles.

Après correction, les propriétés passent trois fois de suite ; ruff et mypy ne signalent plus d'erreur, et la couverture API dépasse 95 % sans exclusion abusive. Le seuil 0,60 envoie 16 avis de test sur 58 vers un humain et réduit les erreurs automatiques de 7 à 2.

Les vingt avis du jeu d'or sont repris de la source avec attribution. Les attentes sont conservées : 5 réponses justes, 11 abstentions et 4 erreurs franches connues. Les quatre xfail stricts ne représentent pas quatre prédictions correctes. Les exemples ne sont pas présentés comme vingt nouveaux avis écrits manuellement par l'étudiant.

## TP5 — Client et page

Sept tests de client et cinq tests de page supplémentaires. La page passe par HTTP, affiche verdict, confiance, abstention et erreurs, puis traite un CSV de six avis avec 3 positifs, 2 négatifs et 1 abstention. Les éventuels essais de navigateur effectivement exécutés et leurs captures sont conservés dans les fichiers du TP5 ; les tests AppTest sont toujours rejoués.

## TP6 — Paquet, commandes et roue

Le fichier predict.py est déplacé avec git mv vers sentiment_app ; le fichier de compatibilité conserve l'ancien import predict et les tests de cache et de panne. L'API importe le paquet sans sys.path. SENTIMENT_MODELE permet de choisir un fichier modèle extérieur.

Les deux échecs initiaux du kit TP6, puis l'échec restant avant branchement de l'API, sont enregistrés. La version 0.6.0, les commandes predict (positif et inconnu), serve et ui sont vérifiées. Les serveurs temporaires sont arrêtés à la fin.

La roue contient api, sentiment_app et ui, sans tests, données, src ni modèle. Elle est installée dans un venv neuf et exécutée hors du dépôt : absence de variable, code 1 et message clair ; chemin de modèle fourni, prédiction POSITIVE. La version de scikit-learn et le chemin du paquet réellement chargé sont enregistrés. La CI reconstruit et réinstalle également cette roue hors dépôt.

## Démonstration et accès du professeur

Suivre [le pas-à-pas de présentation](presenter-au-prof.md), ou lancer `scripts/verifier.ps1 -Detail` après installation. Le dépôt est privé ; son propriétaire doit donner au professeur les droits de lecture nécessaires. Aucune invitation n'est envoyée automatiquement.
