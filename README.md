
# Entropie_Échecs — mesurer la complexité décisionnelle aux échecs

## Cadre conceptuel et ancrage psycho-cognitif

### De l’évaluation machine à la difficulté décisionnelle (cadre **PRE**)

Nous modélisons la difficulté d’un coup **avant** qu’il ne soit joué, à partir des évaluations Stockfish en mode **MultiPV** (k meilleurs coups par position). Chaque score moteur sis_isi​ (en centipions, mates mappés en cp) est converti en probabilité de choix via une **softmax** paramétrée par β\betaβ :

pi  ∝  exp⁡(β si),∑ipi=1.p_i \;\propto\; \exp\big(\beta\, s_i\big), \qquad \sum_i p_i = 1.pi​∝exp(βsi​),i∑​pi​=1.

La softmax n’est pas qu’une astuce numérique : c’est un **modèle de choix stochastique** cohérent avec la psychologie de la décision. On peut la dériver (i) comme un **bruit additif** sur les valeurs avant choix, (ii) comme la **distribution de maximum d’entropie** sous contrainte d’espérance, ou (iii) comme un **compromis exploration–exploitation** optimal pour un agent qui veut rester adaptatif dans un environnement variable. Le paramètre β\betaβ mesure alors un **degré d’optimisation/rationalité** : plus β\betaβ est grand, plus la distribution se concentre sur le meilleur coup (moins d’exploration).

À partir de ppp, nous calculons l’**entropie de Shannon**

 H  =  −∑ipilog⁡2pi,H \=\ -\sum_i p_i \log_2 p_i,H=−i∑​pi​log2​pi​,

et son interprétation simple comme **nombre effectif d’options** ≈2H\approx 2^H≈2H. Ainsi, H≃1H\simeq 1H≃1 bit ⇒\Rightarrow⇒ ~2 choix plausibles ; H≃3H\simeq 3H≃3 bits ⇒\Rightarrow⇒ ~8 choix plausibles. Cette lecture “combien de portes restent réellement ouvertes ?” est le fil conducteur de nos figures et tableaux.

Pourquoi **PRE** ? Parce que mesurer après coup surestime la “facilité” d’une position (biais de rétrospection). Le cadre PRE aligne la métrique sur ce que voit un humain **au moment de choisir**.

### β comme signature contextuelle de la rationalité limitée

En pratique, β\betaβ n’est pas une constante universelle : il reflète **le contexte et l’agent**. Deux familles de modèles psychologiques éclairent ce point :

- **Quantal Response / choix bruité** : les acteurs pondèrent mieux les actions plus payantes, mais avec du bruit ; β\betaβ règle l’intensité de réponse. (Interprétation directe via softmax.)
    
- **Cognitive Hierarchy (CH)** : les joueurs diffèrent par **profondeur de raisonnement** (pas τ\tauτ) ; une population mélange “0-step” (aléatoire) à “k-step” (meilleure réponse à des adversaires moins profonds). Cela explique pourquoi, empiriquement, les comportements varient systématiquement d’un individu à l’autre et d’un jeu à l’autre. Notre β\betaβ capte une partie de cette hétérogénéité en la ramenant à un **degré d’optimisation** observable dans les données.
    

Conséquence méthodologique : nous **calibrons β\betaβ** comme une **fonction du contexte** (β=f(Elo, phase, structure de la position, couleur, temps)\beta = f(\text{Elo, phase, structure de la position, couleur, temps})β=f(Elo, phase, structure de la position, couleur, temps)) plutôt que comme un scalaire global. Dans notre code, β\betaβ peut être appris en minimisant la **log-loss** du coup humain (ou la **divergence KL** entre distribution modèle et fréquences observées).

### Etat de l'art : entropie et expertise aux échecs

Des travaux récents sur des **millions de parties** montrent que la **diversité des ouvertures** (une forme d’entropie comportementale) varie **systématiquement avec la force** des joueurs, et que l’on peut détecter et comparer des “familles de répertoires” par **mesures informationnelles**. Ces analyses à grande échelle (bases lichess/FIDE, méthodes d’agrégation robustes) situent l’entropie comme **indicateur de style et d’expertise** au-delà du seul résultat de la partie. Elles offrent un **cadre empirique** pour relier nos mesures HPREH_{\text{PRE}}HPRE​ à des régularités humaines observables.

Notre parti-pris est complémentaire : **au niveau micro (par position)**, on transforme la difficulté évaluative du moteur en **incertitude stratégique** (HHH, 2H2^H2H). On retrouve alors des corrélations attendues : plus HHH est élevé, plus le coup humain s’éloigne du Top-1 softmax (log-loss ↑\uparrow↑), ce qui est exactement ce que l’on attend si HPREH_{\text{PRE}}HPRE​ capte la **dureté subjective** de la décision.

### Ce que β capture concrètement

- **Exploration vs exploitation** : β\betaβ haut ⇒\Rightarrow⇒ exploitation (préférence marquée pour le meilleur score) ; β\betaβ bas ⇒\Rightarrow⇒ exploration (distribution plus plate, plus d’originalité/tentatives).
    
- **Échelle des scores** : seule **la différence** de scores compte en softmax ; changer l’échelle des cp peut être compensé par β\betaβ (identifiabilité α↔\alpha \leftrightarrowα↔ échelle). D’où l’intérêt de **journaliser** systématiquement la politique de conversion (mates→cp, normalisation) et β\betaβ.
    
- **Variabilité inter-positions** : deux positions de même Elo peuvent appeler des β\betaβ différents (tactique forcée vs manœuvre tranquille). D’où β=f(phase, tension, rois exposeˊs, structure de pions…)\beta=f(\text{phase, tension, rois exposés, structure de pions…})β=f(phase, tension, rois exposeˊs, structure de pions…).
    

### Traçabilité et reproductibilité par **run_id** (JSON)

Chaque exécution est **versionnée** par un `run_id` et accompagnée de métadonnées **JSON** (moteur, hash binaire, depth, MultiPV, politique mates→cp, mapping des unités, schéma des colonnes, horodatage).  
Objectifs :

1. **Rejouabilité** : un autre lecteur peut reconstruire le même ppp, HHH, 2H2^H2H.
    
2. **Comparabilité** : confronter deux runs devient un problème d’**expérience contrôlée** (seul β\betaβ ou `depth` a changé).
    
3. **Gouvernance des données** : le `run_id` **indexe** les CSV et les figures, pour éviter l’écrasement silencieux et garantir l’alignement figures↔données↔paramètres.
    

---

En synthèse, le pipeline **MultiPV → softmax(β\betaβ) → HHH → 2H2^H2H** fait le pont entre **évaluations algorithmiques** et **psychologie de la décision** : il mesure la **latitude stratégique** perçue par un humain juste avant d’agir, tout en permettant de **calibrer** une “température” β\betaβ **contextuelle** et interprétable (rationalité limitée, profondeur effective, gestion du risque et du style), dans l’esprit des modèles cognitifs modernes.

## Pourquoi ce projet ?

L’idée naît en pédagogie (atelier **DédraMathisons – UCL**) : l’**entropie** est un fil rouge capable d’éclairer aussi bien un jeu de cartes qu’une position d’échecs.  
**Le choix initial de l’entropie s’explique aussi par mon affinité avec la physique statistique** : c’est un champ large que **je maîtrise**, nourri par de nombreuses lectures (entropie, distributions exponentielles, principe de maximum d’entropie).  
Elle prend corps en recherche avec une question précise : _à quel point une position est-elle difficile, avant même que l’humain ne joue ?_

Deux piliers théoriques guident la démarche :

- **Théorie des jeux** (Osborne, QRE de McKelvey–Palfrey, Hiérarchie cognitive de Camerer–Ho–Chong) : modéliser des **préférences bruitées** et contextuelles, où β mesure la “rationalité/fermeté” des choix.
    
- **Théorie de l’information** (Shannon, Cover–Thomas, MacKay) : l’**entropie de Shannon** mesure l’incertitude ; la **KL** (ou log-loss) évalue l’écart entre modèle et choix humain.
    

Ce dépôt réconcilie ces deux cadres avec un pipeline reproductible et lisible :  
**Stockfish MultiPV** fournit des candidats → **softmax(β)** construit une distribution de choix → **H** en donne la complexité → **2^H** en offre une lecture intuitive.

---

## Résumé exécutif

- **Cadre PRE** : tout est calculé **avant** le coup humain.
    
- **Mesure interprétable** : H (bits) et **≈ 2^H** comme “nombre de coups plausibles”.
    
- **Calibration** : β peut devenir **β = f(contexte)** (Elo, phase, structure), plutôt qu’un scalaire global.
    
- **Traçabilité forte** : chaque exécution a un **`run_id`** ; ses paramètres et l’environnement moteur sont journalisés dans  
    `data/run/run_info.json` et `data/run/engine_info.json`.
    
- **Reproductibilité** : données et figures **versionnées par `run_id`**.
    

---

## Ce que ce dépôt apporte

1. **Un angle théorie des jeux assumé**  
    La softmax est une **règle de choix** cohérente avec les équilibres bruités (QRE). Le paramètre **β** prend un sens opérationnel : _plus β est élevé, plus l’agent privilégie le meilleur coup_.
    
2. **Une mesure ex ante**  
    Le **PRE** (avant le coup) isole la **difficulté décisionnelle** du bruit post hoc. H devient une propriété de la **position** (et de la MultiPV retenue), pas une conséquence du coup humain.
    
3. **Une lecture immédiate de la complexité**  
    **2^H** offre une échelle “nombre de coups plausibles” parlante pour joueurs, coachs et chercheurs.
    
4. **Des résultats déjà convaincants**  
    La corrélation positive observée entre **H** et la **log-loss** du coup humain confirme que la mesure capte une ambiguïté pertinente _ex ante_.
    
5. **Une traçabilité soignée**  
    Les **JSON** de run embarquent tout le nécessaire pour rejouer et auditer : profondeur, MultiPV, β, politique mate→cp, source PGN, version moteur.
    

---

## Résultats récents (run de référence)

Paramètres : `depth=10`, `multipv=10`, `beta_per_cp=0.01`, `mate→cp=1000`, **cadre PRE**.

- Positions analysées : **61**
    
- Entropie moyenne : **H = 2,79 bits** → **≈ 7,65 coups plausibles**
    
- Par couleur : **Blanc 2,72** ; **Noir 2,87**
    
- Accord modèle ↔ coup joué : **Top-1 = 59 %**, **Top-3 = 86,9 %**, **Top-5 = 95,1 %**
    
- Relation difficulté–prédictibilité : **corr(H, log-loss) ≈ 0,846** (positive)
    

**Lecture**  
Quand **H** augmente (divers bons candidats), la probabilité du coup humain **diminue** et sa **log-loss** augmente ; l’inverse se produit pour des positions quasi forcées (H bas). Ce comportement est attendu si **H_pre** quantifie bien l’ambiguïté stratégique.

> Artefacts versionnés par **`run_id`** :  
> CSV sous `data/processed/runs/<RUN_ID>/…`, figures sous `figures/runs/<RUN_ID>/…`, métadonnées sous `data/run/…`.

---

## Méthodologie (vue d’ensemble)

1. **Extraction PRE** : pour chaque position avant le coup humain, récupération de **k** candidats via Stockfish (**MultiPV**).
    
2. **Échelle** : annonces de mat → **±1000 cp** (politique fixée).
    
3. **Distribution de choix** : softmax(β·cp) sur les candidats.
    
4. **Mesures** : entropie **H** (bits), **2^H**, rang et probabilité du **coup humain**, **log-loss**.
    
5. **Agrégats** : par couleur, par partie, par phase ; figures standardisées.
    

**Calibration (Phase C)**  
Apprendre **β = f(contexte)** (Elo, phase, complexité locale) en minimisant la log-loss/KL sur les positions couvertes par la MultiPV.

**Baseline NN (Phase D)**  
Prédire directement la distribution sur les candidats (listwise) et **calibrer** (temperature scaling), puis comparer à **softmax + β(contextuel)**.

---

## Traçabilité et reproductibilité (JSON)

- `data/run/run_info.json`  
    `run_id`, `timestamp_utc`, `analysis_frame="pre"`, `depth`, `multipv`, `beta_per_cp`, `mate_cp`, `source_pgn`, `n_games`, `n_positions`.
    
- `data/run/engine_info.json`  
    Nom/version du moteur, options (threads, hash), empreinte de l’environnement.
    

Ces fichiers servent de **manifestes de calcul**. Toute figure/CSV cite un **`run_id`**.

---

## Carte du dépôt

```
src/                  # scripts PRE (MultiPV → softmax(β) → H, 2^H) + figures
data/
  processed/runs/<RUN_ID>/{positions,candidates,games}.csv
  output_tests/       # extraits publics
  run/{run_info.json, engine_info.json}
figures/
  runs/<RUN_ID>/*.png # figures versionnées par run
journal/
  Phase-A.md          # cadrage & premiers résultats (clôturé, avec contexte UCL)
  Phase-B.md          # pipeline batch & QA
  Phase-C.md          # calibration β(contextuel) & validation
  Phase-D.md          # baseline NN & calibration
notes/
  Bibliographie.md    # bibliographie commentée (game theory + info theory)
teaching/
  README.md           # contexte pédagogique (DédraMathisons/UCL)
  syllabus/Syllabus_Entropie.pdf
  code/bataille.py    # à déposer par l’élève (Eliot)
```

---

## Démarrer rapidement

1. Installer Python 3.x et **Stockfish** (binaire non fourni).
    
2. Ouvrir `src/entropy3.py` (ou `src/entropie.py`) et renseigner :
    
    - `PGN_PATH` : chemin d’un PGN local
        
    - `ENGINE_PATH` : chemin du binaire Stockfish
        
3. Exécuter le script.  
    Sorties :
    
    - CSV : `data/processed/runs/<RUN_ID>/{positions,candidates,games}.csv`
        
    - Figures : `figures/runs/<RUN_ID>/*.png`
        
    - Métadonnées : `data/run/{run_info.json, engine_info.json}`
        

Paramètres par défaut : `depth=10`, `multipv=10`, `beta_per_cp=0.01`, `mate→cp=1000`.

---

## Interpréter H et 2^H

- **H ≈ 0–1 bit** → 1–2 coups plausibles : positions quasi forcées / tactiques nettes.
    
- **H ≈ 2–3 bits** → 4–8 coups plausibles : vrais choix de plan, arbitrages initiative/structure.
    
- **H > 3 bits** → ≥ 8 coups plausibles : zones très ouvertes, plusieurs bons récits positionnels.
    

> **Attention** : H dépend de `depth` et de la **couverture MultiPV**. Augmenter `multipv` découvre plus de candidats et peut accroître H.

---

## Roadmap (Phases)

- **Phase A (clôturée)** : pipeline PRE minimal + premières figures + manifeste JSON.
    
- **Phase B (en cours)** : exécutions sur lot de parties, **QA** automatique (probas, bornes H, cohérence rangs/couverture).
    
- **Phase C (à venir)** : **β = f(contexte)** (Elo, phase, complexité) et validation par log-loss/KL.
    
- **Phase D (à venir)** : **baseline NN** listwise + **calibration** (temperature scaling) et comparaison exhaustive.
    

Les détails, décisions et risques sont consignés dans `journal/`.

---

## Références fondatrices

- **Osborne — An Introduction to Game Theory** : cadre formel, stratégies mixtes.
    
- **McKelvey & Palfrey — Quantal Response Equilibria** : β comme rationalité bruitée.
    
- **Camerer, Ho & Chong — Cognitive Hierarchy** : τ comme profondeur de réflexion.
    
- **Cover & Thomas ; MacKay** : entropie, KL, maximum d’entropie, justification de softmax.
    
- **Calibration probabiliste** : temperature scaling (Guo et al.).
    
- **Échecs et diversité des choix** : travaux empiriques récents sur l’entropie et l’expertise.
    

Bibliographie commentée : `notes/Bibliographie.md`.

---

## Licence, citation, contributions

- **Licence** : MIT (code). Les documents pédagogiques peuvent suivre une licence adaptée (par ex. CC BY-NC).
    
- **Citation** : `CITATION.cff` à la racine (intégration GitHub ; DOI Zenodo recommandé à la première release).
    
- **Contributions** : issues/PR bienvenues. Merci de référencer explicitement le **`run_id`** lorsque vous commentez des chiffres, et d’actualiser le **journal** et les **figures**.
    

---

## Remerciements

- **DédraMathisons (UCL)** pour l’élan et le cadre.
    
- **Eliot (5e)**, dépositaire du code “bataille” final après plusieurs mois d’apprentissage.
    
- La communauté open source (python-chess, Stockfish) pour l’infrastructure logicielle.
    

---

_De la salle de classe au pipeline, de la théorie des jeux à la théorie de l’information, ce dépôt propose une mesure claire de la difficulté décisionnelle — et une façon transparente de la reconstruire._
