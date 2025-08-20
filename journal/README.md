# Journal de projet

Ce dossier rassemble le suivi du projet par **phases** (A → D), les décisions prises et les pointeurs vers les artefacts (données, figures, modèles). Il constitue la trace publique des méthodes et résultats intermédiaires.

## Finalité du journal
- Offrir une vue d’ensemble du quoi/pourquoi/comment.
- Assurer la traçabilité des exécutions via un `run_id` unique.
- Séparer le cadrage, le pipeline/QA, la calibration et les modèles pour une lecture progressive.

## Organisation
- `Phase-A.md` — Cadrage et premiers résultats (clôturée). Contexte pédagogique : DédraMathisons (UCL).
- `Phase-B.md` — Pipeline stabilisé et contrôle qualité (QA) sur lot de parties.
- `Phase-C.md` — Calibration de β en fonction du contexte (Elo, phase…) et validation.
- `Phase-D.md` — Baseline réseau de neurones, calibration probabiliste et comparaison.
- `archive/` — Éventuels journaux détaillés ou brouillons.

## Conventions et traçabilité
- **Cadre PRE** : toutes les mesures sont calculées avant le coup humain (MultiPV Stockfish).
- **Identifiant d’exécution** : `run_id` (clé de traçabilité).
  - Métadonnées : `data/run/run_info.json`, `data/run/engine_info.json`.
  - Données : `data/processed/runs/<run_id>/{positions,candidates,games}.csv`.
  - Figures : `figures/runs/<run_id>/*.png`.
- **Paramètres par défaut (comparabilité)** : `depth=10`, `multipv=10`, `beta_per_cp=0.01`, `mate→cp=1000`.
- **Indicateurs principaux** :
  - `H` (bits) : entropie de Shannon sur la distribution softmax des candidats.
  - `2^H` : nombre de coups plausibles (échelle lisible).
  - `logloss_bits` : difficulté du coup joué vue par le modèle.
  - Attendu : corrélation positive entre `H` et `logloss_bits`.

## Lecture recommandée
1. **Phase A** — comprendre le pipeline minimal et l’interprétation de `H` et `2^H`.
2. **Phase B** — vérifier la robustesse sur lot de parties (QA, figures “batch”).
3. **Phase C** — suivre la construction de β = f(contexte) et les gains vs β constant.
4. **Phase D** — comparer au modèle NN (avec calibration par temperature scaling).

## Mise à jour du journal
- Lancer une analyse et relever le `run_id`.
- Déposer les CSV et figures sous `data/processed/runs/<run_id>/` et `figures/runs/<run_id>/`.
- Documenter la phase concernée (résultats, décisions, risques) en citant explicitement le `run_id`.
- Archiver, si besoin, les versions longues dans `journal/archive/`.

## Statut synthétique des phases
- Phase A : clôturée (pipeline PRE + premières figures, contexte DédraMathisons/UCL).
- Phase B : en cours (exécutions par lot et QA).
- Phase C : à venir (calibration β contextuelle et validation).
- Phase D : à venir (baseline NN, calibration et comparaison).

Pour les détails, se reporter aux fichiers de phase correspondants.
