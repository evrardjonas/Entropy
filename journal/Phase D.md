# Phase D — Baseline réseau de neurones & calibration probabiliste

## Objectif
Former un modèle supervisé qui **prédit la distribution de probabilité du coup humain parmi les candidats MultiPV**, puis **calibrer** ses sorties (temperature scaling) et **comparer** ses performances au modèle **softmax + β calibré** (Phase C). L’enjeu est double : (i) tester si un modèle “direct” apprend des régularités absentes du simple β(contextuel) ; (ii) produire des probabilités bien calibrées.

## Périmètre
- Cadre d’analyse **PRE** inchangé (avant le coup).
- Apprentissage **listwise** par position (softmax sur les k candidats de la position).
- Comparaisons systématiques :
  - **Référence 1** : softmax(β constant) — Phase A
  - **Référence 2** : softmax(β = f(contexte)) — Phase C
  - **Baseline NN** : MLP listwise (non calibré) + **NN + TS** (temp. scaling) — Phase D
- Aucune donnée d’évaluation hors MultiPV n’est utilisée pour l’entraînement ; ces cas sont **rapportés** en diagnostic.

## Données d’entrée
- `data/processed/runs/<run_id>/{positions,candidates,games}.csv`
- Métadonnées : `data/run/{run_info.json, engine_info.json}`
- **Split** par `game_id` (train/val/test) pour éviter les fuites entre positions d’une même partie.

## Cible et formulation
- Un **groupe** = une position \(t\) avec \(k_t\) candidats (mêmes règles MultiPV que Phase A/B).
- La cible est **le coup joué** \(y_t \in \{1,\dots,k_t\}\).
- Le modèle produit un **score par candidat** \(z_{ti}\); on applique une **softmax par groupe** :
  \[
  \hat p_{ti} = \frac{\exp(z_{ti})}{\sum_{j=1}^{k_t}\exp(z_{tj})}
  \]
- **Perte** : log-loss listwise (moyenne sur les positions), équivalente à la NLL du coup joué.

## Caractéristiques (features)

### Par position (partagées par tous les candidats)
- **Contexte** : Elo au trait (et/ou moyen/écart Elo), phase (ouverture/milieu/finale), numéro de demi-coup (ply).
- **Complexité locale** (si disponible) : \(k_{\text{eff}}\), écart-type des `cp`, gap top1–top2, entropie \(H_{\text{moteur}}\) préalable (option).

### Par candidat (propres au coup i)
- **Évaluation moteur** : `cp_i` bornés (mates → ±1000) — *même politique que Phase A/B*.
- **Deltas** : `cp_i - cp_best`, `rank_i`, indicateur `is_best`.
- **Type de coup** (si dispo dans le parseur) : capture, échec, promotion, prise en passant, roque.
- **Heuristiques** (optionnelles) : variation SAN, matériel capturé, motif “tactique” simple (booléens).

> Recommandation : commencer avec un **jeu de features minimal** (cp_i, deltas, rang, contexte [Elo, phase, ply, k_eff]) pour une comparaison juste avec Phase C ; documenter tout ajout.

## Modèle
- **Architecture** : MLP léger **partageant ses poids** entre candidats (mêmes couches appliquées à \([x_{\text{pos}}, x_{\text{cand}}]\)), puis un score scalaire \(z_{ti}\).
- **Agrégation** : softmax **par position** (masquage des candidats inexistants).
- **Régularisation** : L2, dropout léger ; normalisation des features continues (centrage-réduction).
- **Optimisation** : Adam / L-BFGS sur la log-loss listwise.
- **Batching** : mini-batches de positions (groupes de taille variable, masqués).

## Calibration (post-hoc)
- **Temperature scaling (TS)** sur le **set de validation** :
  \[
  \hat p^{(T)}_{ti} = \frac{\exp(z_{ti}/T)}{\sum_j \exp(z_{tj}/T)},\quad T>0
  \]
  - Estimation de \(T\) par **minimisation de la NLL sur val** (cf. pratique standard).
  - Variantes à tester seulement si besoin : \(T\) par **phase** (3 températures), ou par **couleur** (Blanc/Noir). **Par défaut : \(T\) scalaire unique**.
- But : **améliorer la calibration** sans modifier le classement (Top-k inchangés).

## Protocole expérimental
- **Split** : train / val / test **par game_id** (ex. 70/15/15), stratifier si possible par Elo.
- **Équilibrage** : aucun poids de classe (un positif par position) ; l’apprentissage listwise équilibre déjà les groupes.
- **Contrôles** : mêmes QA A–D que Phase B appliqués aux données d’entrée ; journaliser le % de positions où le coup joué **n’est pas** dans la MultiPV.
- **Sélection de modèle** : meilleure NLL sur **validation** avant calibration ; calibration TS ; rapport **test** final.

## Évaluation (test)
- **Pouvoir prédictif** : Top-1 / Top-3 / Top-5 ; NLL (bits) ; Brier score (option).
- **Calibration** : ECE / MCE ; **reliability diagram** (global + par phase/couleur si pertinent).
- **Diagnostics** :
  - Performances **par quartiles de H**.
  - Performances **par phase** et **par Elo**.
  - Sensibilité à \(k_{\text{eff}}\) (nombre de candidats disponibles).
- **Comparaisons** :
  - β **constant** (Phase A) vs β **contextuel** (Phase C) vs **NN** (non calibré) vs **NN+TS** (calibré).
  - Gains **relatifs** en NLL et en ECE.

## Figures à produire
- `nn_vs_softmax_logloss_<tag>.png` : barres NLL (β const, β(context), NN, NN+TS).  
- `reliability_nn_pre_post_TS_<tag>.png` : diagramme de fiabilité avant/après TS.  
- `topk_by_H_quartiles_<tag>.png` : Top-1/3 par quartiles de H (tous modèles).  
- `ece_by_phase_<tag>.png` : ECE par phase (ouverture/milieu/finale).  
- `perf_by_elo_bins_<tag>.png` : NLL et Top-1 par tranches Elo.

Chaque figure précise : **features utilisées**, **taille échantillon**, **tag du modèle** et **run_id** des données.

## Livrables
- **Modèle** : poids/params (format au choix) + **manifeste** des features réellement utilisées.
- **Calibration** : température \(T\) estimée, script/notes d’estimation, avant/après.  
- **Rapport** : `data/nn/report_<tag>.md` (métriques, figures, protocole).  
- **Artefacts** : `data/nn/models/<tag>/…`, `figures/nn/<tag>/*.png`.

## Critères de sortie
- **Amélioration significative** (test) vs β(context) **sur la NLL** (ex. ≥ 2–3 % relatif) **ou** **ECE** (réduction nette), tout en **préservant** ou **améliorant** Top-1/3.  
- **Calibration** améliorée **après TS** (ECE ↓, diagramme de fiabilité rapproché de la diagonale).  
- **Robustesse** : résultats stables sur 2–3 splits ; sans dépendre d’un artifice (pas d’overfit manifeste au val).  
- **Traçabilité** : protocole, features, seeds, run_id, versions moteur documentés.

## Risques et parades
- **Dépendance forte à `cp`** → le NN n’apporte rien au-delà de β(context).  
  *Parade* : (i) prouver la non-infériorité ; (ii) tester des features contextuelles sobres (phase, H, gaps) ; (iii) ablation claire.
- **Sur-apprentissage** (modèle trop grand, features bruitées).  
  *Parade* : MLP léger, L2/dropout, CV stricte par parties, early stopping, ablations.
- **Calibration déjà bonne** (β(context)) → gains ECE marginaux.  
  *Parade* : documenter ; TS sert de garde-fou ; garder le modèle le plus simple qui marche.
- **Variabilité due à k_effectif** (groupes de taille variable).  
  *Parade* : masquage propre, métriques reportées par bins de \(k_{\text{eff}}\), vérifier la couverture MultiPV.

## Décisions attendues en fin de phase
- Conserver **β(context)** comme modèle principal **ou** adopter **NN+TS** s’il apporte un gain robuste (NLL/ECE) sans dégrader Top-k.  
- Figer le **jeu de features** minimal validé.  
- Décider si l’**ensemble** des deux (β(context) pour l’interprétation + NN calibré pour la probabilité) est préférable, selon l’usage visé (article, outil pédagogique, vitrine GitHub).
