
# Données — structure, schéma et traçabilité

Ce dossier contient les artefacts produits par le pipeline **PRE** (avant le coup humain) :
extraction Stockfish **MultiPV**, transformation **softmax(β)**, entropie **H** et nombre de choix **≈ 2^H**,
plus les métadonnées de run et, si présents, des rapports QA.

## Arborescence


data/  
├─ processed/  
│ └─ runs/  
│ └─ <RUN_ID>/  
│ ├─ positions.csv  
│ ├─ candidates.csv  
│ └─ games.csv  
├─ output_tests/  
│ ├─ positions_small.csv  
│ └─ candidates_small.csv  
├─ run/  
│ ├─ run_info.json  
│ └─ engine_info.json  
└─ QA/ # optionnel  
└─ <RUN_ID>_qa.json # ou .md```

- **processed/runs/\<RUN_ID>/** : sorties complètes et versionnées (clé = `run_id`).
- **output_tests/** : extraits publics minimalistes (quelques lignes) pour illustrer le format.
- **run/** : journalisation des paramètres et de l’environnement (voir ci-dessous).
- **QA/** : contrôle qualité automatisé (si activé en Phase B).

## Métadonnées de run

- **`run/run_info.json`** : identifiant, horodatage UTC, paramètres d’analyse.
  - Champs typiques : `run_id`, `timestamp_utc`, `analysis_frame="pre"`, `depth`, `multipv`,
    `beta_per_cp` (β par centipion), `mate_cp=1000`, `source_pgn`, `n_games`, `n_positions`.
- **`run/engine_info.json`** : version du moteur, options, threads, hash, etc.

> Les horodatages sont en UTC (format ISO 8601), l’encodage des fichiers est **UTF-8**.

## Schéma des CSV

### 1) `positions.csv` — une ligne par demi-coup (position avant le coup humain)
Clé logique : `(run_id, game_id, ply)`.

| Colonne          | Type      | Description |
|------------------|-----------|-------------|
| `run_id`         | string    | Identifiant unique de l’exécution (traçabilité). |
| `game_id`        | string    | Identifiant de la partie (provenant du PGN ou généré). |
| `ply`            | int       | Numéro de demi-coup (1, 2, …). |
| `color`          | string    | Joueur au trait (`W` / `B`). |
| `k_effective`    | int       | Nombre de candidats effectivement extraits (≤ `multipv`). |
| `H_bits`         | float     | Entropie de Shannon (bits) sur la distribution softmax des candidats. |
| `two_pow_H`      | float     | Nombre de choix plausibles, défini comme `2^H_bits`. |
| `played_san`     | string    | Coup humain joué (SAN). |
| `in_multipv`     | bool      | `True` si `played_san` figure parmi les candidats. |
| `played_rank`    | float     | Rang du coup joué (1 = top1), `NaN` si hors MultiPV. |
| `played_prob`    | float     | Probabilité softmax du coup joué, `NaN` si hors MultiPV. |
| `logloss_bits`   | float     | `-log2(played_prob)` ; `NaN` si hors MultiPV. |
| `sum_prob`       | float     | Somme des probabilités des candidats (≈ 1, contrôle). |
| `notes`          | string    | Optionnel (diagnostic, anomalies). |

**Unités et conventions**
- Évaluations moteur en **centipions** (`cp`). Les annonces de mat sont mappées à **±1000 cp** avant softmax.
- β est appliqué en **1/cp** : `p_i ∝ exp(β * cp_i)`, avec `β = beta_per_cp` (constante en Phase A/B).
- `H_bits ∈ [0, log2(k_effective)]`. `two_pow_H` ≈ nombre de coups sérieux.

### 2) `candidates.csv` — une ligne par coup candidat (par position)
Clé logique : `(run_id, game_id, ply, rank)`.

| Colonne        | Type    | Description |
|----------------|---------|-------------|
| `run_id`       | string  | Identifiant d’exécution. |
| `game_id`      | string  | Partie associée. |
| `ply`          | int     | Demi-coup associé. |
| `rank`         | int     | Rang du candidat (1 = meilleur selon le moteur). |
| `move_san`     | string  | Coup candidat en SAN. |
| `cp`           | float   | Évaluation moteur (centipions ; mates → ±1000). |
| `prob`         | float   | Probabilité softmax après application de β. |
| `is_best`      | bool    | `True` si `rank == 1`. |
| `is_played`    | bool    | `True` si `move_san == played_san` de la position. |
| `delta_cp`     | float   | `cp - cp_best` (optionnel si disponible). |

**Invariants attendus**
- Par `(game_id, ply)`, les `rank` couvrent exactement `1..k_effective` sans trous ni doublons.
- La somme des `prob` par position est ≈ 1 (voir `sum_prob` dans `positions.csv`).

### 3) `games.csv` — agrégats par partie
Clé logique : `(run_id, game_id)`.

| Colonne            | Type   | Description |
|--------------------|--------|-------------|
| `run_id`           | string | Identifiant d’exécution. |
| `game_id`          | string | Partie. |
| `white`, `black`   | string | Noms (si présents dans le PGN). |
| `white_elo`, `black_elo` | int | Elo des joueurs (si présents). |
| `result`           | string | Résultat (PGN). |
| `n_positions`      | int    | Nombre de positions analysées. |
| `H_mean`, `H_std`  | float  | Moyenne/écart-type de `H_bits`. |
| `two_pow_H_mean`   | float  | Moyenne de `2^H`. |
| `top1_rate`        | float  | Taux où le coup joué est rank=1 et `in_multipv=True`. |
| `top3_rate`, `top5_rate` | float | Taux Top-k (k=3/5) conditionnés à `in_multipv=True`. |
| `coverage_rate`    | float  | Part des positions où `in_multipv=True`. |

> Les champs manquants du PGN (Elo, noms) peuvent être vides. Les taux sont ignorés si `in_multipv=False`.

## Formats et encodage

- **CSV** : séparateur virgule, décimale point, encodage **UTF-8**.
- **JSON** : UTF-8, timestamps en **UTC** (`YYYY-MM-DDTHH:MM:SSZ`).
- Valeurs manquantes : `NaN` dans les CSV pour les champs non définis.

## Reproduire les fichiers

1. Ouvrir `src/entropy3.py` (ou `src/entropie.py`) et renseigner :
   - `PGN_PATH` : chemin vers un PGN local.
   - `ENGINE_PATH` : binaire Stockfish (non versionné).
2. Exécuter le script.
3. Les CSV sont générés sous `data/processed/runs/<RUN_ID>/`, les métadonnées sous `data/run/`,
   et les figures sous `figures/runs/<RUN_ID>/`.

Paramètres par défaut : `depth=10`, `multipv=10`, `beta_per_cp=0.01`, `mate_cp=1000`.

## Contrôles de cohérence (résumé)

- Probabilités : `|sum_prob − 1|` max ≤ 1e-12 (par position).
- Bornes d’entropie : `0 ≤ H_bits ≤ log2(k_effective)`.
- Cohérence candidats/positions : `k_effective` = nombre de lignes candidates ; `rank` sans trous.
- Champ “coup joué” : si `in_multipv=True`, alors `played_prob ∈ (0,1]` et `logloss_bits ≥ 0`.

Un rapport automatisé peut être exporté dans `data/QA/<RUN_ID>_qa.json` (Phase B).

## Bonnes pratiques de publication

- Ne pas versionner de PGN privés ou non libres ; publier des **échantillons** uniquement.
- Journaliser systématiquement `run_info.json` et `engine_info.json`.
- Citer explicitement le `run_id` lorsque vous commentez des chiffres ou figures.

## FAQ

- **Pourquoi PRE plutôt que POST ?**  
  Pour mesurer la **difficulté ex ante** : H caractérise l’ambiguïté **avant** le coup humain.

- **Que faire si le coup humain n’apparaît pas dans la MultiPV ?**  
  Marquer `in_multipv=False` et laisser `played_rank`, `played_prob`, `logloss_bits` à `NaN`.  
  En Phase C (calibration), ces positions sont exclues de l’optimisation ; le **taux d’exclusion** est reporté.

- **Que signifie `beta_per_cp` ?**  
  C’est le coefficient β appliqué aux centipions dans la softmax (`p ∝ exp(β·cp)`). En Phase A/B, β est **constant** pour toutes les positions d’un run.

