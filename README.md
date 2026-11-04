# sentiment-app-solo

Travail individuel d'**Ahmed Rayane Ramzi** (@RayaneRZ24), adapté le 28 octobre 2026 à la consigne de travail en solo. Étape actuelle : **TP6 et compléments du 2 novembre — application client 0.6.1**, vérifiés le 4 novembre 2026.

[Voir les captures par TP](#captures-tp1-tp6)

## Utiliser l’application client

[Télécharger la livraison 0.6.1](https://github.com/RayaneRZ24/sentiment-app-solo/releases/tag/v0.6.1) · [Notice utilisateur](docs/notice-utilisateur.md) · [Fiche du modèle](docs/fiche-modele.md)

Extraire l’archive `sentiment-app-client-0.6.1.zip`, puis lancer `python installer.py` avec Python 3.11. L’installation initiale nécessite Internet ; les analyses s’exécutent ensuite localement. Le navigateur s’ouvre automatiquement. Ctrl+C ferme l’application et son service.

La livraison contient seulement l’application, son modèle séparé, la notice, la fiche, un exemple CSV et les métriques. Les tests, SHAP, les scripts d’entraînement, le journal et les captures restent dans le dépôt destiné au développement et à l’évaluation.

![Application client installée : avis positif](docs/captures/client-avis-positif.png)

## Compléments vérifiés le 4 novembre 2026

| Contrôle | Ajout | Vérification locale |
| --- | --- | --- |
| C6 — TP2 | Explications SHAP | [4 tests réussis](docs/verification/complements-c6-tests.txt) |
| T27a — TP4 | Performances par groupes et biais | [8 tests réussis](docs/verification/complements-t27a-tests.txt) |
| T34a — TP5 | Deux graphiques dans la page | [9 tests de graphiques et de page réussis](docs/verification/complements-t34a-tests.txt) |
| T41a — TP6 | Fiche modèle renseignée | [14 tests réussis](docs/verification/complements-t41a-tests.txt) |

Bilan de la suite : **137 passed, 4 xfailed**, couverture API **97,59 %**. Les quatre erreurs connues du modèle restent déclarées. [Résultat intégral](docs/verification/complements-tests-complets.txt).

Le paquet a été installé et utilisé dans un environnement neuf hors dépôt, sans outils de développement : [preuve d’installation](docs/verification/client-installation-externe.json). Les deux graphiques, l’export CSV, l’abstention et le refus d’un fichier illisible ont été vérifiés dans un navigateur sur cette installation. La [CI de la livraison](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/41876000516) a aussi réussi l’installation sur Linux. [Historique des cinq validations](docs/verification/complements-checkpoints-ci.json).

## Origine du code

Ce dépôt réutilise le code du [projet de binôme](https://github.com/OthmaneW37/OthmaneMoussawi-A---AhmedRayaneRamzi-B), référence `ff79dc84d25fe76e84f79b8348ba8c49ff585b57`, ainsi que les kits étudiants d'A. Larhlimi. Les contributions antérieures d'Othmane Moussawi et d'Ahmed Rayane Ramzi sont reconnues : cette reprise ne revendique pas une écriture entièrement nouvelle du code. Le nouvel historique décrit les adaptations et les vérifications individuelles réellement réalisées, dans l'ordre des TP.

La consigne solo remplace le contrôle de deux auteurs par le contrôle d'un auteur unique dans les tests et le diagnostic. Les seuils du modèle et les autres exigences techniques restent inchangés.

## Développement et vérifications

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pip install -e ".[ui]"
python src/make_demo.py
python src/train.py
python scripts/check_setup.py
python -m pytest -q
```

`requirements.txt` contient les dépendances nécessaires aux TP atteints, sans installer les bibliothèques des semaines futures. `requirements.lock` conserve les versions du poste Windows. Le modèle et les données générées ne sont jamais commités.

Les résultats de chaque TP sont conservés dans [le journal solo](docs/journal-tp1-tp6.md) et dans `docs/verification/`. Chaque étape validée possède son repère Git (`tp1-valide` à `tp5-valide`, puis `v0.6.0`) et sa propre exécution GitHub Actions.

```powershell
git log --oneline -20
git status
python -m pytest tests/ -v
```

Les erreurs connues du modèle sont documentées en `xfail(strict=True)` à partir du TP4 ; une abstention n'est pas présentée comme une prédiction correcte.

## Checkpoints historiques du 28 octobre 2026

| Étape | Tests locaux | Repère | CI |
| --- | --- | --- | --- |
| TP1 | 38 passed in 2.04s | `tp1-valide` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40731654315) |
| TP2 | 42 passed in 2.23s | `tp2-valide` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40731888889) |
| TP3 | 48 passed, 1 warning in 3.09s | `tp3-valide` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40732096196) |
| TP4 | 87 passed, 4 xfailed, 1 warning in 7.02s | `tp4-valide` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40732610139) |
| TP5 | 99 passed, 4 xfailed, 1 warning in 11.28s | `tp5-valide` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40733058617) |
| TP6 | 105 passed, 4 xfailed, 1 warning in 10.99s | `v0.6.0` | [CI réussie](https://github.com/RayaneRZ24/sentiment-app-solo/actions/runs/40733697516) |

Le dossier de travail personnel est `C:\Users\NITRO 5\Downloads\sentiment-app-solo`. [Présenter le projet au professeur](docs/presenter-au-prof.md).

```powershell
python -m pip install -e ".[ui]"
sentiment --version
sentiment predict "Livraison rapide, produit conforme, très satisfait"
sentiment start
```

Le tag v0.6.0 conserve le checkpoint initial du TP6. La livraison actuelle est en 0.6.1, avec les compléments et le lancement client. Le modèle reste extérieur au paquet ; utiliser `SENTIMENT_MODELE` hors du dossier source. La fiche de choix d'un projet d'agent IA est un livrable séparé et n'est pas remplie avec un numéro de sujet inventé.

Les scripts et tests des compléments SHAP, biais, graphiques et fiche modèle proviennent du kit étudiant `complements-lot1.zip` fourni le 2 novembre 2026 par A. Larhlimi. Les interprétations, la fiche remplie, le lancement client et les mesures sont adaptés à ce dépôt ; les corrigés enseignants ne sont pas distribués.

## Fichier à joindre au formulaire

Déposer [docs/journal-tp1-tp6.md](docs/journal-tp1-tp6.md), qui reprend le modèle du professeur, ses contrôles et ses annexes, avec les résultats de cette reprise solo.

<!-- captures-tp:start -->
<a id="captures-tp1-tp6"></a>

## Captures des TP1 à TP6

Les preuves visuelles sont aussi intégrées ici pour être consultables directement depuis le README. Ouvrir le TP souhaité pour afficher ses captures.

Les images de navigateur montrent l’application ou l’API. Les autres images présentent les rapports de résultats enregistrés ou les relevés CI ; leur nature est précisée sous chaque titre.

[Consulter le journal complet](docs/journal-tp1-tp6.md) · [Ouvrir toutes les images](docs/captures/)

<details>
<summary><strong>Préparation du poste individuel — 1 capture(s)</strong></summary>

**Poste individuel**

*Rapport de résultats enregistrés*

![Poste individuel](docs/captures/tp0-poste-membre-a.png)

</details>

<details>
<summary><strong>TP1 — Cadrage, environnement et Git — 8 capture(s)</strong></summary>

**T0 · La structure du kit (solo)**

*Rapport de résultats enregistrés*

![T0 · La structure du kit (solo)](docs/captures/tp1-t0-structure.png)

**T1 · L'environnement et le point de départ (solo)**

*Rapport de résultats enregistrés*

![T1 · L'environnement et le point de départ (solo)](docs/captures/tp1-t1-pytest.png)

**T2 · Les fiches de cadrage (solo)**

*Rapport de résultats enregistrés*

![T2 · Les fiches de cadrage (solo)](docs/captures/tp1-t2-cadrage.png)

**T3 · Le dépôt GitHub et le premier push (solo)**

*Rapport de résultats enregistrés*

![T3 · Le dépôt GitHub et le premier push (solo)](docs/captures/tp1-t3-depot-github.png)

**T5 · Un commit par membre (membres B puis A)**

*Rapport de résultats enregistrés*

![T5 · Un commit par membre (membres B puis A)](docs/captures/tp1-t5-shortlog.png)

**T6 · La vérification finale (solo)**

*Rapport de résultats enregistrés*

![T6 · La vérification finale (solo)](docs/captures/tp1-t6-pytest.png)

**T6 · La vérification finale (solo)**

*Rapport de vérification GitHub Actions*

![T6 · La vérification finale (solo)](docs/captures/tp1-t6-actions.png)

**T7 · Le clone frais**

*Rapport de résultats enregistrés*

![T7 · Le clone frais](docs/captures/tp1-t7-clone-frais.png)

</details>

<details>
<summary><strong>TP2 — Données, entraînement et évaluation — 6 capture(s)</strong></summary>

**C1 · Le kit installé (solo)**

*Rapport de résultats enregistrés*

![C1 · Le kit installé (solo)](docs/captures/tp2-c1-pytest.png)

**C2 · Le jeu de démonstration**

*Rapport de résultats enregistrés*

![C2 · Le jeu de démonstration](docs/captures/tp2-c2-make-demo.png)

**C3 · L'entraînement**

*Rapport de résultats enregistrés*

![C3 · L'entraînement](docs/captures/tp2-c3-train.png)

**C4 · L'évaluation**

*Rapport de résultats enregistrés*

![C4 · L'évaluation](docs/captures/tp2-c4-evaluate.png)

**C5 · Le vrai jeu de données, les tests, le push**

*Rapport de vérification GitHub Actions*

![C5 · Le vrai jeu de données, les tests, le push](docs/captures/tp2-c5-allocine.png)

**C6 · Ce que regarde le modèle**

*Rapport de résultats enregistrés*

![C6 · Ce que regarde le modèle](docs/captures/tp2-c6-expliquer.png)

</details>

<details>
<summary><strong>TP3 — API FastAPI — 7 capture(s)</strong></summary>

**T14 · Le kit installé (solo)**

*Rapport de résultats enregistrés*

![T14 · Le kit installé (solo)](docs/captures/tp3-t14-pytest.png)

**T15 · /health**

*Capture navigateur — application ou API*

![T15 · /health](docs/captures/tp3-t15-health.png)

**T16 · Un avis positif**

*Rapport de résultats enregistrés*

![T16 · Un avis positif](docs/captures/tp3-t16-positif.png)

**T17 · Un avis négatif**

*Rapport de résultats enregistrés*

![T17 · Un avis négatif](docs/captures/tp3-t17-negatif.png)

**T18 · Les refus**

*Rapport de résultats enregistrés*

![T18 · Les refus](docs/captures/tp3-t18-refus.png)

**T19 · La CI**

*Rapport de vérification GitHub Actions*

![T19 · La CI](docs/captures/tp3-t19-actions.png)

**T20 · L'API sans modèle**

*Rapport de résultats enregistrés*

![T20 · L'API sans modèle](docs/captures/tp3-t20-sans-modele.png)

</details>

<details>
<summary><strong>TP4 — Limites, abstention et qualité — 10 capture(s)</strong></summary>

**T21 · Le kit installé et le point de départ (solo)**

*Rapport de résultats enregistrés*

![T21 · Le kit installé et le point de départ (solo)](docs/captures/tp4-t21-couverture.png)

**T22 · Le contrat d'entrée corrigé**

*Rapport de résultats enregistrés*

![T22 · Le contrat d'entrée corrigé](docs/captures/tp4-t22-espaces.png)

**T23 · Les propriétés**

*Rapport de résultats enregistrés*

![T23 · Les propriétés](docs/captures/tp4-t23-proprietes.png)

**T24 · L'abstention**

*Rapport de résultats enregistrés*

![T24 · L'abstention](docs/captures/tp4-t24-courbe.png)

**T24 · L'abstention**

*Capture navigateur — application ou API*

![T24 · L'abstention](docs/captures/tp4-t24-indetermine.png)

**T25 · Le jeu d'or**

*Rapport de résultats enregistrés*

![T25 · Le jeu d'or](docs/captures/tp4-t25-jeu-or.png)

**T26 · L'intégration et la couverture**

*Rapport de résultats enregistrés*

![T26 · L'intégration et la couverture](docs/captures/tp4-t26-couverture.png)

**T27 · Qualité statique, crochet et CI**

*Rapport de résultats enregistrés*

![T27 · Qualité statique, crochet et CI](docs/captures/tp4-t27-pre-commit.png)

**T27 · Qualité statique, crochet et CI**

*Rapport de vérification GitHub Actions*

![T27 · Qualité statique, crochet et CI](docs/captures/tp4-t27-actions.png)

**T27a · Performances par groupes**

*Rapport de résultats enregistrés*

![T27a · Performances par groupes](docs/captures/tp4-t27a-biais.png)

</details>

<details open>
<summary><strong>TP5 — Interface Streamlit — 10 capture(s)</strong></summary>

**T28 · Le kit installé (solo)**

*Rapport de résultats enregistrés*

![T28 · Le kit installé (solo)](docs/captures/tp5-t28-pytest.png)

**T29 · La page ouverte, l'API prête**

*Capture navigateur — application ou API*

![T29 · La page ouverte, l'API prête](docs/captures/tp5-t29-page.png)

**T30 · Les verdicts**

*Capture navigateur — application ou API*

![T30 · Les verdicts](docs/captures/tp5-t30-positif.png)

**T30 · Les verdicts**

*Capture navigateur — application ou API*

![T30 · Les verdicts](docs/captures/tp5-t30-negatif.png)

**T31 · L'abstention**

*Capture navigateur — application ou API*

![T31 · L'abstention](docs/captures/tp5-t31-abstention.png)

**T32 · Les erreurs**

*Capture navigateur — application ou API*

![T32 · Les erreurs](docs/captures/tp5-t32-refus.png)

**T32 · Les erreurs**

*Capture navigateur — application ou API*

![T32 · Les erreurs](docs/captures/tp5-t32-injoignable.png)

**T33 · Un fichier d'avis**

*Capture navigateur — application ou API*

![T33 · Un fichier d'avis](docs/captures/tp5-t33-lot.png)

**T34 · Compte rendu, push, CI**

*Rapport de vérification GitHub Actions*

![T34 · Compte rendu, push, CI](docs/captures/tp5-t34-actions.png)

**T34a · Les deux graphiques du client installé**

*Capture navigateur — application ou API*

![T34a · Les deux graphiques du client installé](docs/captures/tp5-t34a-graphiques.png)

</details>

<details open>
<summary><strong>TP6 — Paquet installable et roue — 8 capture(s)</strong></summary>

**T35 · Le kit installé (solo)**

*Rapport de résultats enregistrés*

![T35 · Le kit installé (solo)](docs/captures/tp6-t35-pytest.png)

**T36 · predict.py dans le paquet**

*Rapport de résultats enregistrés*

![T36 · predict.py dans le paquet](docs/captures/tp6-t36-deplacement.png)

**T37 · L'API branchée sur le paquet**

*Rapport de résultats enregistrés*

![T37 · L'API branchée sur le paquet](docs/captures/tp6-t37-api.png)

**T38 · La commande sentiment**

*Rapport de résultats enregistrés*

![T38 · La commande sentiment](docs/captures/tp6-t38-commande.png)

**T39 · La roue**

*Rapport de résultats enregistrés*

![T39 · La roue](docs/captures/tp6-t39-roue.png)

**T40 · La roue hors du dépôt**

*Rapport de résultats enregistrés*

![T40 · La roue hors du dépôt](docs/captures/tp6-t40-ailleurs.png)

**T41 · Version, étiquette, push**

*Rapport de vérification GitHub Actions*

![T41 · Version, étiquette, push](docs/captures/tp6-t41-actions.png)

**T41a · Fiche du modèle et conditions d’usage**

*Rapport de résultats enregistrés*

![T41a · Fiche du modèle et conditions d’usage](docs/captures/tp6-t41a-fiche-modele.png)

</details>

<!-- captures-tp:end -->
