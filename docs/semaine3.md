# TP3 individuel : API FastAPI

Les six tests HTTP sont exécutés via TestClient. Le modèle est chargé pendant le démarrage et jamais entraîné par l'API.

Un fichier modèle absent fait échouer le démarrage : une instance incapable de prédire ne se déclare donc pas prête. Un 503 sert à signaler une indisponibilité après le démarrage.

La validation HTTP et celle de predict() protègent deux points d'entrée différents. Dans le kit initial, les espaces passent le schéma puis sont refusés par predict() : ils donnent un detail sous forme de chaîne, différent des autres refus Pydantic. Le TP4 doit uniformiser ce refus et vérifier les pannes.
