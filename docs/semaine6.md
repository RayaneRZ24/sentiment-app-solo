# TP6 individuel : application installable

## Ce qui appartient à la roue

La roue contient sentiment_app, api et ui ainsi que les métadonnées. Les tests, les données, le modèle et src sont exclus. Le modèle possède son propre cycle de vie ; le code installé le retrouve grâce à SENTIMENT_MODELE. Le contenu réel est consigné dans tp6-contenu-roue.txt.

## Développement et installation

L'installation éditable pointe vers les sources pendant le développement. L'installation d'une roue copie le paquet et doit fonctionner sans le dépôt. Un venv neuf, placé hors du dépôt, a été créé pour installer et tester la roue. Sans la variable, la commande échoue proprement avec le code 1 ; avec le chemin absolu du modèle, elle prédit POSITIVE. La version affichée est 0.6.0.

## Compatibilité du modèle et dépendances

Le modèle a été entraîné avec scikit-learn 1.5.2 ; le paquet impose une version >=1.5,<1.6 et la CI entraîne en 1.5. Un joblib n'est pas un format indépendant des versions de scikit-learn. Aucune panne de version n'a été artificiellement provoquée ici : la vérification hors dépôt utilise la même série 1.5 et réussit. Le chemin du paquet réellement installé et la version de scikit-learn sont enregistrés dans tp6-origine-paquet-installe.txt.

Les deux échecs initiaux du kit et l'échec restant avant branchement de l'API sont conservés dans tp6-t35-avant.txt et tp6-t36-avant-api.txt. La commande serve a été démarrée réellement : /health répond OK, puis le serveur a été arrêté. Les commandes predict et la compatibilité src/predict.py ont été exécutées séparément.
