#  Cadrage & premiers résultats (Clôturée)

## Objectif
Définir l’architecture du dépôt et mettre en place une analyse PRE (avant le coup) : Stockfish MultiPV → transformation softmax(β) → entropie de Shannon H et nombre de choix 2^H. Publier des sorties de données et des figures minimales pour la vitrine du projet.

## Périmètre
- Analyse PRE sur un premier PGN avec paramètres constants.  
- Export des résultats en CSV, journalisation des métadonnées (moteur, profondeur, MultiPV, β, source).  
- Figures de base illustrant H, 2^H et la difficulté décisionnelle.

## Données et paramètres du run
- analysis_frame: pre  
- depth: 10  
- multipv: 10  
- beta_per_cp: 0.01  
- Politique mate→cp: 1000  
- Run ID : voir `data/run/run_info.json` (run_id)

**Données :**
- `data/processed/{positions,candidates,games}.csv`  
- Échantillons : `data/output_tests/*`  
- Métadonnées : `data/run/{run_info.json, engine_info.json}`

**Figures (versionnées par run) :**
- `figures/runs/<RUN_ID>/H_per_ply_<RUN_ID>.png`  
- `figures/runs/<RUN_ID>/top1_by_quartile_<RUN_ID>.png`  
- `figures/runs/<RUN_ID>/H_vs_logloss_<RUN_ID>.png`  
- `figures/runs/<RUN_ID>/choices_by_color_<RUN_ID>.png`

## Méthode (résumé)
- Extraction MultiPV (k=10) avant le coup joué pour chaque position.  
- Conversion des évaluations en centipions en probabilités via softmax(β).  
- Calcul de l’entropie H et du nombre de choix ≈ 2^H.  
- Repérage du coup joué (rang, probabilité, log-loss en bits).  
- Agrégats par partie.

### Contexte pédagogique
Cette phase s’inscrit dans le cadre de **DédraMathisons** avec l’**UCL**, où l’entropie a servi de fil conducteur : assez vaste pour susciter l’exploration, assez précis pour apprendre à mesurer. Deux trajectoires ont été menées en parallèle.

**Jeu de bataille (pédagogie).**  
Le code initial a été écrit par l’enseignant pour amorcer l’atelier. Le code final, abouti, est l’œuvre d’**Eliot (5e)**, dépositaire de cette version. Il résulte de plusieurs mois d’apprentissage (Python, génération de nombres aléatoires) et de consolidation. Eliot sera invité à déposer sa version finale dans ce dépôt, sous son nom.

**Échecs (recherche).**  
L’enthousiasme de l’école pour les échecs a fourni l’élan, mais la complexité du problème a freiné la motivation en classe. La piste a donc été poursuivie hors classe et structurée ici en **pipeline de recherche** : Stockfish MultiPV → softmax paramétrée → H, 2^H → calibration. Ce pipeline « entropie aux échecs » a été développé par l’auteur du dépôt.

## Résultats clés de l’analyse
- Positions analysées : 61  
- Entropie moyenne H : 2,79 bits  
- Moyenne de 2^H : 7,65  
- Par couleur : Blanc 2,72 bits ; Noir 2,87 bits  
- Accord modèle ↔ coup joué : Top-1 = 59 %, Top-3 = 86,9 %, Top-5 = 95,1 %  
- Relation difficulté–prédictibilité : corr(H, log-loss) ≈ 0,846 (positive)

**Lecture.** Quand H augmente (plusieurs coups plausibles), la probabilité assignée au coup humain diminue et la log-loss augmente ; inversement, H bas correspond à des décisions plus forcées où le coup humain coïncide plus souvent avec le Top-1. Ce comportement est attendu si H_pre capte bien la difficulté décisionnelle.

## Journal d’activité (synthèse)
- **Cadrage et architecture du dépôt.** Arborescence claire (données brutes vs traitées, figures versionnées par run, notes/biblio, journal par phases).  
- **Environnement et documentation.** Rôles des dossiers (`data/`, `figures/`, `src/`, `notes/`, `journal/`) et formats d’export (CSV lisibles, parquet optionnel).  
- **Implémentation des briques de base.** softmax(β), entropie H, interface Stockfish MultiPV, conventions centipions/mates.  
- **Positionnement méthodologique.** Entropie comme mesure d’ambiguïté décisionnelle ; β contextuel préférable à une grille Elo par quartiles.  
- **Clarifications conceptuelles.** β (rationalité/“piqûre” du softmax, QRE) vs τ (profondeur de réflexion, hiérarchie cognitive).  
- **Esquisse de calibration.** Contexte → β (régression/MLP), objectif log-loss/KL ; comparaison au modèle non calibré et à une baseline supervisée.  
- **Arbitrages.** Batch reporté ; maintien d’un run propre et interprétable pour la vitrine.

## Décisions de clôture
- Conserver le cadre PRE comme base d’analyse.  
- Journaliser systématiquement les paramètres de run et versionner données/figures par `run_id`.  
- Déporter le contrôle qualité approfondi en Phase B.

## Passage de relais — Phase B
- Étendre l’analyse à un lot de parties (paramètres constants), conserver chaque exécution par `run_id`.  
- Mettre en place les scripts QA (somme des probabilités, bornes de H, cohérence candidats/positions, rangs, champs “joué”).  
- Produire des figures batch (H moyen par ply + dispersion, distribution de 2^H, Top-1 par quartiles de H global et par couleur).
