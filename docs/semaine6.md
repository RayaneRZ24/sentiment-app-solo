# TP6 individuel : application installable

## Ce qui appartient à la roue

La roue contient sentiment_app, api et ui ainsi que les métadonnées. Les tests, les données, le modèle et src sont exclus. Le modèle possède son propre cycle de vie ; le code installé le retrouve grâce à SENTIMENT_MODELE. Le contenu réel est consigné dans tp6-contenu-roue.txt.

## Changements dans api/model.py et installation

L'API importe maintenant ModelLabel, charger_modele et predict depuis sentiment_app.predict, sans ajouter src/ dans sys.path. L'import repose sur le paquet installable plutôt que sur l'emplacement du dossier courant. Le fichier de compatibilité src/predict.py renvoie vers le même module : les tests qui modifient predict.MODELE continuent donc de modifier le module réel.

L'installation éditable pointe vers les sources pendant le développement. L'installation d'une roue copie le paquet et doit fonctionner sans le dépôt. Un venv neuf, placé hors du dépôt, a été créé pour installer et tester la roue. Sans la variable, la commande échoue proprement avec le code 1 ; avec le chemin absolu du modèle, elle prédit POSITIVE. La version affichée est 0.6.0.

## Compatibilité du modèle et dépendances

Le modèle a été entraîné avec scikit-learn 1.5.2 ; le paquet impose une version >=1.5,<1.6 et la CI entraîne en 1.5. Un joblib n'est pas un format indépendant des versions de scikit-learn. Aucune panne de version n'a été artificiellement provoquée ici : la vérification hors dépôt utilise la même série 1.5 et réussit. Le chemin du paquet réellement installé et la version de scikit-learn sont enregistrés dans tp6-origine-paquet-installe.txt.

Les deux échecs initiaux du kit et l'échec restant avant branchement de l'API sont conservés dans tp6-t35-avant.txt et tp6-t36-avant-api.txt. La commande serve a été démarrée réellement : /health répond OK, puis le serveur a été arrêté. Les commandes predict et la compatibilité src/predict.py ont été exécutées séparément.

## Complément T41a : fiche modèle, 4 novembre 2026

La [fiche modèle](fiche-modele.md) renseigne les dix rubriques du nouveau modèle étudiant. Le contrôle initial a effectivement produit [13 échecs et un succès](verification/complements-t41a-avant.txt), puis [14 succès](verification/complements-t41a-tests.txt) après rédaction. Les valeurs sont celles de notre modèle et de nos sorties, dont les quatre erreurs connues de notre propre jeu d’or ; le bilan fourni à titre d’exemple par le professeur n’a pas été recopié.

La rubrique la plus délicate est celle des biais : les effectifs sont petits et la longueur est confondue avec les retournements. Le croisement permet de décrire l’écart mesuré sans prétendre démontrer une causalité ni une équité démographique. La fiche explique aussi ce qu’un humain doit vérifier et le coût de l’abstention en relecture.

## Livraison client, version 0.6.1

Le tag v0.6.0 conserve l’étape historique. La version 0.6.1 ajoute le lancement `sentiment start`, l’archive client, l’installateur et les compléments. La roue embarque la notice utilisateur comme description, à la place du README pédagogique. SHAP et les outils qualité restent des dépendances de développement.

La livraison rassemble la roue, le modèle séparé, une notice, la fiche du modèle, un petit CSV d’exemple, les métriques et leurs empreintes. Le client n’a besoin ni du dépôt source ni du journal ni des tests. L’installation extérieure vérifie aussi le démarrage et l’arrêt des services ; sous Windows, il faut arrêter les enfants du lanceur Python du venv, pas seulement son processus parent.
