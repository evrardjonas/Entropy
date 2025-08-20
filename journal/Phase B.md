# Phase B — Pipeline stabilisé & contrôle qualité (QA)

## Objectif
Rendre l’analyse reproductible à l’échelle (lot de parties) et fiabiliser les sorties par des contrôles automatisés. Publier un jeu d’échantillons stable et des figures “batch” pour documenter la difficulté décisionnelle.

## Périmètre
- Cadre d’analyse inchangé : **PRE** (avant le coup).
- Paramètres normalisés pour comparabilité (valeurs par défaut) :
  - depth = 10, multipv = 10, beta_per_cp = 0.01, mate→cp = 1000.
- Exécutions sur un lot de parties, sorties versionnées par `run_id`.

## Données d’entrée et sorties attendues
- Entrées : un ensemble de fichiers **PGN** (source non publique si droits incertains).
- Sorties par exécution (`<run_id>` visible dans `data/run/run_info.json`) :
  - `data/processed/runs/<run_id>/{positions,candidates,games}.csv`
  - `data/run/{run_info.json, engine_info.json}`
  - `figures/runs/<run_id>/*.png`
- Échantillons publics (petits extraits) :
  - `data/output_tests/positions_small.csv`
  - `data/output_tests/candidates_small.csv`

## Pipeline batch (résumé)
1. Pour chaque partie, extraire **MultiPV** avant le coup joué.
2. Transformer les évaluations en probabilités via **softmax(β)**.
3. Calculer `H` (bits) et `2^H` par position ; enrichir avec rang du coup joué, probabilité du coup joué, log-loss (bits).
4. Écrire `positions.csv`, `candidates.csv`, `games.csv` (schéma inchangé par rapport à la Phase A).
5. Générer les figures “batch” (cf. section dédiée).
6. Lancer les **contrôles QA** ; enregistrer le rapport sous `data/QA/<run_id>_qa.json` (ou `.md`).
7. Marquer le run comme **accepté** ou **rejeté** selon les seuils ci-dessous.

## Plan de contrôle qualité (QA)
Contrôles exécutés pour chaque `(game_id, ply)` et agrégés par `<run_id>`.

### A. Invariants probabilistes
- Somme des probabilités par position : `|sum_prob − 1|`  
  - maximum ≤ 1e−12 ; moyenne ≤ 1e−14.
- Bornes d’entropie : `0 ≤ H ≤ log2(k_effective)` ; violations = 0.

### B. Cohérence candidats/positions
- `k_effective` = nombre de lignes candidates pour la position (égalité stricte).
- Unicité du meilleur : exactement un `is_best = True`, et `cp_best = max(cp)` de la position.
- Rangs complets : présence exacte de `rank ∈ {1, …, k_effective}` sans trous ni doublons.

### C. Champ “coup joué”
- Si le coup joué est dans la MultiPV :
  - `played_prob ∈ (0, 1]`, `logloss_bits ≥ 0`.
- Si non présent : champ `in_multipv = False` et `rank = NaN` (ou champ équivalent), log-loss selon convention du script (exclusion du calcul agrégé si non comparable).

### D. Intégrité des identifiants et métadonnées
- Clé `(game_id, ply, side_to_move)` unique dans `positions.csv`.
- `run_id` présent dans tous les enregistrements des trois CSV.
- Alignement `games.csv` ↔ `positions.csv` (nombre de plies par partie).

### E. Indicateurs descriptifs (non bloquants)
- Taux Top-k (Top-1/Top-3/Top-5) global et par couleur.
- Corrélation `H` ↔ `logloss_bits` (attendue positive).
- Distribution de `k_effective` (pour détecter une MultiPV trop courte).

**Gating (acceptation du run).**  
Un run est **accepté** si A, B, C, D sont satisfaits (zéro violation) ; E est descriptif et doit être reporté dans le QA.

## Figures “batch” à produire
- `H_by_ply_mean_std_<run_id>.png` : courbe de `H` moyen par demi-coup avec bande d’écart-type.  
- `hist_2powH_<run_id>.png` : histogramme de `2^H` (troncature éventuelle en queue).  
- `top1_by_H_quartiles_<run_id>.png` : taux Top-1 par quartiles de `H` (global, puis variante par couleur).  
- `H_vs_logloss_<run_id>.png` : nuage `H` vs `logloss_bits` + ligne de tendance.  
- `choices_by_color_<run_id>.png` : `2^H` moyen par demi-coup, séparé Blanc/Noir.

Chaque figure doit préciser : paramètres (depth/multipv/β), taille de l’échantillon `n`, et le `run_id`.

## Livrables de la phase
- Données :
  - `data/processed/runs/<run_id>/{positions,candidates,games}.csv`
  - `data/output_tests/*` (extraits mis à jour)
  - `data/run/{run_info.json, engine_info.json}`
  - `data/QA/<run_id>_qa.json` (ou `.md`)
- Figures : `figures/runs/<run_id>/*.png` (toutes les figures “batch”).

## Critères de sortie
- Analyse réalisée sur **un lot de N parties** (N à fixer ici, ex. 30–50) avec paramètres constants.  
- **0 violation** sur les contrôles A–D pour tous les `<run_id>` retenus.  
- Publication des figures “batch” et des échantillons `output_tests`.  
- Rapport QA présent pour chaque `<run_id>` publié.

## Traçabilité et index des runs
- Chaque exécution conserve ses artefacts sous `runs/<run_id>`.  
- Un index minimal des runs peut être maintenu dans `data/run/index.csv` (ou `.md`) avec :  
  `run_id, timestamp_utc, depth, multipv, beta_per_cp, n_games, n_positions, qa_status`.

## Risques et parades
- **MultiPV trop courte / depth insuffisant** : candidates manquants → Top-k biaisé.  
  *Parade* : vérifier la distribution de `k_effective` et augmenter `multipv`/`depth` si nécessaire.
- **β inadapté** : entropies écrasées ou trop élevées.  
  *Parade* : conserver β constant en Phase B ; calibration en Phase C.
- **PGN hétérogènes** : formats ou métadonnées incohérents.  
  *Parade* : normaliser en amont (chemins, encodage), logguer les erreurs parsing.

## Décisions attendues à la fin de la phase
- Valider la stabilité des métriques (Top-k, `H`, `2^H`, corrélations) sur un lot de parties.  
- Fixer les features contextuelles à extraire pour la **calibration de β** (Phase C).  
- Confirmer la configuration par défaut (depth, multipv, β) pour les futurs runs de référence.
