# Calibration β(Elo) & validation

## Objectif
Apprendre une fonction **β = f(contexte)** (ex. Elo, phase de jeu, caractéristiques de position) afin d’améliorer la correspondance entre la distribution softmax et le comportement observé (coup humain) en **cadre PRE**. Évaluer l’apport de la calibration par rapport au β constant de la Phase A.

## Périmètre
- Cadre d’analyse : **PRE** (évaluations Stockfish avant le coup joué).
- Paramètres de base inchangés pour comparabilité : depth = 10, multipv = 10, mate→cp = 1000.
- Calibration sur des positions où le **coup humain appartient à la MultiPV** (gestion des cas manquants décrite ci-dessous).
- β reste **position-dépendant via f(contexte)** mais **commun** aux k candidats d’une même position.

## Données d’entrée
- `data/processed/runs/<run_id>/positions.csv`
- `data/processed/runs/<run_id>/candidates.csv`
- `data/processed/runs/<run_id>/games.csv`
- Métadonnées : `data/run/{run_info.json, engine_info.json}`

### Variables nécessaires (par position)
- **Candidats** : identifiants de coups, `cp` évalués par Stockfish, `k_effective`.
- **Coup joué** : identifiant, rang (si dans MultiPV).
- **Contexte** : 
  - **Elo** (au minimum Elo du joueur au trait ; idéalement Elo moyen, écart Elo).
  - **Phase** (ouverture / milieu / finale), cf. règles simples ci-dessous.
  - (Option) Heuristiques de complexité : `k_effective`, dispersion des `cp` (écart-type, gap top1–top2), `ply`, matériel, etc.

> Si Elo n’est pas dans le PGN, prévoir un champ par défaut et documenter l’absence.

## Méthode de calibration

### 1) Modèle
Pour une position t avec candidats \(i=1..k_t\) et évaluations \(s_{ti}\) (centipions bornés, mates mappés à ±1000) :

\[
p_{ti}(\theta) 
= \frac{\exp\big(\beta(x_t;\theta)\, s_{ti}\big)}{\sum_{j=1}^{k_t} \exp\big(\beta(x_t;\theta)\, s_{tj}\big)} ,
\qquad \beta(x_t;\theta) > 0
\]

où \(x_t\) sont les **features de contexte** (Elo, phase, …).

**Paramétrisation de \(\beta\)** (positive) :
- **Régression log-linéaire** : \(\beta(x;\theta) = \mathrm{softplus}(w^\top x + b)\) ou \(\exp(w^\top x + b)\).
- **Piècewise** (baseline facile) : \(\beta = \beta_{\text{open}}\), \(\beta_{\text{mid}}\), \(\beta_{\text{end}}\) par phase ; éventuellement par tranches d’Elo.
- **MLP léger** (option) : \(\beta(x)=\mathrm{softplus}(\text{MLP}(x))\) pour capter des non-linéarités.

### 2) Fonction objectif
Cible = maximiser la probabilité du **coup humain** observé.  
Sur l’échantillon \(\mathcal{D}\) (positions où le coup humain \(\in\) MultiPV) :

\[
\mathcal{L}(\theta) 
= -\frac{1}{|\mathcal{D}|}\sum_{t\in\mathcal{D}} \log p_{t,y_t}(\theta)
\]

Équivalent : **log-loss moyenne** (en nats ou en bits selon le log).  
Régularisation L2 de \(\theta\) pour limiter le sur-apprentissage.

### 3) Protocole d’estimation
- **Validation croisée par parties** (folds au niveau `game_id` pour éviter les fuites).
- **Optimisation** : L-BFGS/Adam sur \(\mathcal{L} + \lambda \|\theta\|_2^2\), contraintes intégrées via softplus/exp.
- **Normalisation** des features (centrage-réduction) ; one-hot pour la phase.

### 4) Définition de la phase de jeu (règles simples)
- Variante **par ply** : ouverture `ply ≤ 20`, milieu `21–60`, finale `> 60`.  
- Variante **matérielle (préférée si dispo)** : score de phase \(\in[0,1]\) via pondération du matériel (ex. rois exclus, pions faible poids, pièces lourdes fort poids) et seuils {ouverture, milieu, finale}.  
Choisir une règle, la **documenter**, et l’appliquer de manière déterministe.

### 5) Gestion des positions où le coup humain n’est pas dans la MultiPV
- **Option retenue (propre)** : **exclure** ces positions de la calibration \(\mathcal{D}\) et **rapporter** leur taux (diagnostic de `multipv`/`depth`).  
- Alternative (si nécessaire) : ajouter une classe “reste” avec masse \(\epsilon\) (censorship), mais cela modifie l’objectif et complique l’interprétation.

## Validation et métriques

### A. Contre le β constant (Phase A)
- **Log-loss moyenne** (bits) ↓ attendu après calibration.  
- **Top-k** (Top-1/3/5) ↑ ou stable.
- **Réduction d’erreur relative** : \(\Delta = (\text{LL}_{\text{const}} - \text{LL}_{\text{cal}}) / \text{LL}_{\text{const}}\).

### B. Calibration probabiliste
- **Fiabilité** (reliability diagram) : probabilité prédite vs fréquence observée.
- **ECE/MCE** (Expected/Maximum Calibration Error) ↓.
- (Option) **Brier score**.

### C. Diagnostics complémentaires
- **Courbe \(\beta\) vs Elo** (monotone non garantie mais attendue ↑ en moyenne).
- **\(\beta\) par phase** (ouverture < milieu ≲ finale, à confirmer empiriquement).
- **\(\beta\) vs complexité locale** (ex. gap top1–top2, k_effective).

## Figures à produire
- `beta_vs_elo_<run_id>.png` : \(\beta\) attendu vs Elo (moyennes par bin + IC).  
- `beta_by_phase_<run_id>.png` : distribution de \(\beta\) par phase.  
- `logloss_comparison_<run_id>.png` : barres (β constant vs β calibré).  
- `reliability_diagram_<run_id>.png` : calibration des probabilités.  
- `topk_vs_H_<run_id>.png` : Top-1/3 selon quartiles de H (avant/après calibration).

## Livrables de la phase
- **Modèle** et paramètres de calibration (fichier `data/calibration/beta_model_<tag>.json` ou équivalent).  
- **Rapport de validation** : `data/calibration/report_<tag>.md` (ou `.pdf`) avec toutes les métriques et figures.  
- **Données annotées** (option) : positions enrichies de \(\beta(x)\) appliqué et des probabilités calibrées.

## Critères de sortie
- **Amélioration significative** de la log-loss vs β constant (valeur-cible à fixer, ex. ≥ 3–5 % relatif).  
- **Stabilité** en validation croisée (variabilité contrôlée).  
- **Calibration** améliorée (ECE ↓) et figures publiées.  
- **Documentation** des hypothèses (phase, features, filtrage des positions hors MultiPV).

## Risques et parades
- **Peu de variance Elo** → \(\beta\) dépend mal d’Elo.  
  *Parade* : ajouter des features de phase/complexité ; collecter plus de parties annotées.
- **Sur-apprentissage** (MLP) → gains non robustes.  
  *Parade* : commencer par régressions simples, CV stricte par parties, régularisation.
- **Biais MultiPV** (coup joué souvent hors MultiPV) → jeu d’apprentissage réduit.  
  *Parade* : augmenter `multipv`/`depth` ou limiter l’échantillon aux positions bien couvertes et **rapporter le taux d’exclusion**.
- **Invariance d’échelle** des `cp` → ambiguïtés d’interprétation de \(\beta\).  
  *Parade* : conserver la même **politique de bornage** des `cp` (mates = ±1000) et la même échelle entre runs.

## Décisions attendues à la fin de la phase
- Valider une **paramétrisation de \(\beta\)** (linéaire, par phase, ou MLP léger) et la **publier**.  
- Figer la **règle de phase** et la liste de **features** retenues.  
- Confirmer les **gains** (log-loss, ECE) et décider de l’extension (ajout d’autres contextes, ex. adversaire, structure matérielle).
