
# Entropie_Échecs — mesurer la complexité décisionnelle aux échecs

**Stockfish MultiPV → softmax(β) → entropie H → nombre de choix ≈ 2^H (cadre PRE)**  
Avec calibration de β selon le contexte (Elo, phase…) et baseline réseau de neurones pour comparer.

---

## Pourquoi ce projet ?

À l’origine, il y a une intuition pédagogique simple, née dans le cadre de **DédraMathisons (UCL)** : l’**entropie** est un fil conducteur qui traverse aussi bien un jeu de cartes qu’une position d’échecs.  
Puis il y a une question scientifique très concrète : _à quel point une position est-elle “difficile”, avant même que l’humain ne joue ?_

Deux influences ont structuré la démarche :

- Un article récent en sciences du comportement (Nature Human Behaviour) qui met en évidence le lien entre **diversité des choix** et **expertise** dans les ouvertures.
    
- Un retour aux fondamentaux avec **la théorie des jeux** (Osborne) : quand les préférences deviennent probabilistes, la **softmax** et ses équilibres bruités (QRE) offrent un langage précis pour parler de décisions incertaines.
    

Entre les deux, le terrain : des élèves, un atelier, et deux trajectoires.  
Le **jeu de bataille** a donné une réussite pédagogique tangible — code initial rédigé par l’enseignant, code final consolidé par **Eliot (5e)**, qui en est le dépositaire.  
La branche **“échecs”**, plus exigeante, a migré vers un pipeline de recherche : **Stockfish MultiPV → softmax(β) → entropie H → 2^H**, puis **calibration** et **validation**.

---

## Ce que mesure le dépôt

- **Cadre PRE** : tout est calculé **avant** le coup humain, à partir des k meilleurs coups Stockfish (**MultiPV**).
    
- **Transformation softmax(β)** sur les évaluations (centipions), avec β paramétrant le “tranchant” des préférences.
    
- **Entropie de Shannon H** sur la distribution softmax, et **2^H** comme **nombre de coups plausibles**.
    
- **Données dérivées** : rang et probabilité du coup joué, log-loss (bits), agrégats par partie.
    
- **Calibration** (Phase C) : apprendre β = f(contexte) pour coller au comportement humain.
    
- **Baseline NN** (Phase D) : prédire directement la distribution sur les candidats et calibrer (temperature scaling).
    

---

## Un premier résultat en un coup d’œil (run de référence)

- Positions analysées : **61**
    
- Entropie moyenne H : **2,79 bits** → **≈ 7,65 coups plausibles**
    
- Par couleur : **Blanc 2,72** ; **Noir 2,87**
    
- Accord modèle ↔ coup joué : **Top-1 = 59 %**, **Top-3 = 86,9 %**, **Top-5 = 95,1 %**
    
- Relation difficulté–prédictibilité : **corr(H, log-loss) ≈ 0,846** (positive)
    

> Lecture : plus **H** est élevé (plusieurs coups sérieux), plus la probabilité assignée au coup humain baisse et la log-loss augmente — signe que **H_pre** capture bien la difficulté décisionnelle.

Les artefacts complets (CSV, figures, métadonnées) sont versionnés par **`run_id`** : voir `data/run/run_info.json` et `figures/runs/<run_id>/`.

---

## Carte du dépôt

```
src/                  # scripts d’analyse (PRE, MultiPV → softmax → H, 2^H)
data/
  processed/runs/<run_id>/{positions,candidates,games}.csv
  output_tests/       # petits extraits publics
  run/{run_info.json, engine_info.json}
figures/
  runs/<run_id>/*.png # figures versionnées par run
journal/
  Phase-A.md          # cadrage & premiers résultats (clôturé)
  Phase-B.md          # pipeline batch & QA
  Phase-C.md          # calibration β(context) & validation
  Phase-D.md          # baseline NN & calibration probabiliste
notes/
  Bibliographie.md    # bibliographie commentée
teaching/
  README.md           # contexte pédagogique (DédraMathisons/UCL)
  syllabus/Syllabus_Entropie.pdf
  code/bataille.py    # à déposer par l’élève (Eliot)
```

---

## Reproduire un run minimal

1. Installer Python 3.x et **Stockfish** (binaire non fourni).
    
2. Ouvrir `src/entropy3.py` (ou `src/entropie.py`) et renseigner :
    
    - `PGN_PATH` : chemin d’un PGN local
        
    - `ENGINE_PATH` : chemin du binaire Stockfish
        
3. Lancer le script.  
    Le programme génère :
    
    - CSV : `data/processed/runs/<run_id>/{positions,candidates,games}.csv`
        
    - Figures : `figures/runs/<run_id>/*.png`
        
    - Métadonnées : `data/run/{run_info.json, engine_info.json}`
        

Paramètres par défaut (comparabilité) : `depth=10`, `multipv=10`, `beta_per_cp=0.01`, `mate→cp=1000`.

> Note : si le coup humain est hors MultiPV, la position est exclue des métriques calibrées et le taux d’exclusion est reporté (voir Phase B/C).

---

## Interpréter les CSV (schéma minimal)

- **positions.csv** : `(run_id, game_id, ply, color, k_effective, H_bits, 2powH, played_san, played_prob, logloss_bits, …)`
    
- **candidates.csv** : `(run_id, game_id, ply, move_san, rank, cp, prob, is_best, …)`
    
- **games.csv** : agrégats par partie `(run_id, game_id, n_positions, H_mean, top1_rate, …)`
    

---

## Journal et feuille de route

- **Phase A** — pipeline PRE et premières figures : `journal/Phase-A.md` (clôturé).
    
- **Phase B** — exécutions batch et QA : `journal/Phase-B.md` (en cours).
    
- **Phase C** — calibration **β = f(contexte)** (Elo, phase, complexité) et validation : `journal/Phase-C.md`.
    
- **Phase D** — baseline **réseau de neurones** + calibration par **temperature scaling** : `journal/Phase-D.md`.
    

---

## Références fondatrices

- **Nature Human Behaviour** : mise en relation de la diversité des choix et de l’expertise dans les ouvertures ; ancre empirique pour relier entropie et niveau de jeu.
    
- **Osborne, _An Introduction to Game Theory_** : cadre des jeux stratégiques, stratégies mixtes et interprétation probabiliste des préférences.
    
- **MacKay, _Information Theory, Inference, and Learning Algorithms_** ; **Cover & Thomas, _Elements of Information Theory_** : fondements entropie/KL/maximum entropy ; justification du recours à la softmax.
    
- **Guo et al., “On Calibration of Modern Neural Networks”** : calibration probabiliste (temperature scaling).
    
- **McKelvey & Palfrey, “Quantal Response Equilibria”** ; **Camerer, Ho & Chong, “Cognitive Hierarchy”** : β comme rationalité bruitée (QRE) et τ comme profondeur de réflexion.
    

La **bibliographie commentée** et ses rôles dans le projet : `notes/Bibliographie.md`.

---

## Licence, citation, contributions

- **Licence** : MIT (code).
    
- **Citation** : voir `CITATION.cff`.
    
- **Contributions** : issues/PR bienvenues. Merci de référencer explicitement le **`run_id`** des résultats commentés et d’actualiser le **journal** et les **figures**.
    

---

## Remerciements

- **DédraMathisons (UCL)** pour l’élan et le cadre.
    
- **Eliot (5e)**, dépositaire du code “bataille” final après plusieurs mois d’apprentissage.
    
- La communauté open source (python-chess, Stockfish) sans laquelle ce projet resterait théorique.
    

---

_Ce dépôt cherche à tenir ensemble deux promesses : une **mesure** claire de la difficulté décisionnelle, et une **histoire** lisible de sa construction — de la classe au pipeline, de l’intuition à la figure._