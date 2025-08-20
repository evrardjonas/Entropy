# Chapitre 2 – Équilibre de Nash : Théorie

# 2.1 Jeux stratégiques (Strategic games)

Un **jeu stratégique** est un modèle pour des situations où plusieurs agents (*joueurs*) prennent des décisions de manière indépendante et simultanée, chacun ayant un ensemble de stratégies possibles.

## Définition d’un jeu stratégique

- Un ensemble de joueurs (au moins 2).
- Pour chaque joueur, un ensemble de **stratégies possibles**.
- Pour chaque combinaison de stratégies choisies, une **fonction de gain** (*payoff function*) pour chaque joueur.

### Notations usuelles

- **N** : nombre de joueurs.
- Pour chaque joueur *i*, $S_i$ est l’ensemble de ses stratégies.
- $S = S_1 \times \ldots \times S_N$ : ensemble des profils de stratégies possibles.
- $u_i(s)$ : gain du joueur *i* quand le profil de stratégie $s \in S$ est joué.

---

## Préférences ordinales

Des **préférences ordinales** signifient que l’on sait seulement **classer** les alternatives par ordre de préférence, sans mesurer “combien” on préfère l’une à l’autre.

- On peut dire :  
  “Je préfère A à B, et B à C.”  
  Ou “Je suis indifférent entre D et E.”
- Mais on ne dit pas :  
  “Je préfère A à B deux fois plus que B à C.” (cela serait cardinal, pas ordinal).

### Exemple d’ordre ordinal

Supposons que les stratégies de Alice sont : {A, B, C}.  
Elle attribue la satisfaction suivante :
- $u(A) = 100$
- $u(B) = 10$
- $u(C) = 0$

Cela donne le même ordre ordinal que :
- $v(A) = 3$
- $v(B) = 2$
- $v(C) = 1$

Dans les deux cas, l’ordre des préférences est $A \succ B \succ C$ (A préféré à B, B préféré à C).  
**Ce qui compte, c’est l’ordre, pas l’écart entre les valeurs.**

---

> **Résumé** :  
> Les préférences ordinales permettent de classer les stratégies, sans tenir compte de l’intensité de préférence.  
> En théorie des jeux, l’ordre suffit pour raisonner sur la rationalité et l’équilibre.

##  2.2 Dilemme du Prisonnier – Explication du tableau

|            | Quiet (S2)  | Fink (S2)   |
|:----------:|:-----------:|:-----------:|
| Quiet (S1) | 2 , 2       | 0 , 3       |
| Fink (S1)  | 3 , 0       | 1 , 1       |

- Chaque case montre les gains pour (Suspect 1, Suspect 2).
- "Quiet" = se taire (coopérer). "Fink" = dénoncer (trahir).

**Lecture des cases** :  
- (Quiet, Quiet) → 2,2 : petite peine pour chacun (coopération)
- (Quiet, Fink) → 0,3 : S1 prend tout, S2 est libéré
- (Fink, Quiet) → 3,0 : S1 est libéré, S2 prend tout
- (Fink, Fink) → 1,1 : chacun dénonce, peine moyenne

**Interprétation** :  
- Individuellement, chaque suspect a intérêt à dénoncer ("Fink").
- Mais si les deux dénoncent, ils ont un résultat moins bon que s’ils avaient tous les deux coopéré.

> **(Fink, Fink) = (1,1) est l’équilibre de Nash du jeu.**
## Ex 16.1 : Jeu stratégique : Poissons hermaphrodites 

Deux poissons, chacun préfère jouer le même rôle lors de la reproduction (ex : "mâle").

### Actions possibles
- **Either** : être flexible, accepter n’importe quel rôle
- **Insist** : insister sur son rôle préféré

## Gains
- **H** : gain si j’obtiens mon rôle préféré
- **L** : gain si j’ai l’autre rôle
- **S** : gain si pas de reproduction (je pars chercher ailleurs)

|               | Either (B)        | Insist (B)        |
|:-------------:|:----------------:|:----------------:|
| Either (A)    | ½(H+L), ½(H+L)   | L, H             |
| Insist (A)    | H, L             | S, S             |

- Si les deux sont flexibles, on tire au sort les rôles
- Si un seul insiste, il obtient le rôle voulu
- Si les deux insistent, ils ne s’accouplent pas et partent

### Condition pour que le jeu soit un dilemme du prisonnier :
$$
H > \frac{1}{2}(H+L) > S > L
$$

C'est-à-dire :
- La tentation de "trahir" (insist) paie mieux si l'autre coopère (either)
- La coopération (deux "either") donne un gain intermédiaire
- Si les deux trahissent (insistent), c’est pire que de coopérer, mais mieux que le pire rôle

**l’équilibre de Nash** est **(Insist, Insist)** :

> **Chaque poisson insiste sur son rôle préféré, les deux repartent chercher ailleurs (chacun reçoit S).**
# 2.3 Calcul détaillé de l’équilibre de Nash mixte — Bach ou Stravinsky

## Introduction

Dans "Bach ou Stravinsky", deux joueurs veulent aller ensemble à un concert, mais l’un préfère Bach, l’autre Stravinsky. Chacun préfère être avec l’autre, même si ce n’est pas à son concert préféré.

On cherche ici l’équilibre de Nash en **stratégies mixtes** (c’est-à-dire que chacun choisit "au hasard" selon une certaine probabilité).

# Calcul détaillé de l’équilibre mixte — Bach ou Stravinsky

## Étape 1 : Rappel du jeu

**Tableau des gains**

|                 | Bach (J2) | Stravinsky (J2) |
| :-------------: | :-------: | :-------------: |
| Bach (J1)       | 2 , 1     | 0 , 0           |
| Stravinsky (J1) | 0 , 0     | 1 , 2           |

- J1 préfère Bach (gain max = 2), mais préfère être accompagné.
- J2 préfère Stravinsky (gain max = 2), mais préfère aussi être accompagné.

---

## Étape 2 : Stratégies mixtes

- Joueur 1 joue **Bach** avec proba p, **Stravinsky** avec 1 – p.
- Joueur 2 joue **Bach** avec proba q, **Stravinsky** avec 1 – q.

Chaque joueur choisit sa proba pour rendre l'autre **indifférent** entre ses deux choix.

---

## Étape 3 : Calcul pour Joueur 1

**Espérance de gain pour J1 :**
- Si Bach : E₁(Bach) = 2q
- Si Stravinsky : E₁(Stravinsky) = 1 – q

Pour qu'il randomise, il faut :  
E₁(Bach) = E₁(Stravinsky)

Soit :  
2q = 1 – q  
2q + q = 1  
3q = 1  
q = 1/3

**Donc J2 doit jouer Bach avec proba 1/3 pour rendre J1 indifférent.**

---

## Étape 4 : Calcul pour Joueur 2

**Espérance de gain pour J2 :**
- Si Bach : E₂(Bach) = p
- Si Stravinsky : E₂(Stravinsky) = 2(1 – p)

On égalise :  
p = 2(1 – p)  
p = 2 – 2p  
3p = 2  
p = 2/3

**Donc J1 doit jouer Bach avec proba 2/3 pour rendre J2 indifférent.**

---

## Étape 5 : Synthèse du résultat

À l'équilibre de Nash en stratégies mixtes :
- Joueur 1 joue Bach avec proba 2/3, Stravinsky avec 1/3
- Joueur 2 joue Bach avec proba 1/3, Stravinsky avec 2/3

---

## Explication importante

> À l’équilibre de Nash en stratégies mixtes, chaque joueur choisit “au hasard” selon une probabilité telle que l’autre joueur n’a aucune raison de changer sa propre répartition.
>
> C’est parce que, pour chaque joueur, le gain moyen (espérance) obtenu en jouant l’une ou l’autre action est exactement le même, étant donné la façon dont l’autre randomise.
# 2.4 Matching Pennies — Calcul de l’équilibre de Nash

## Description du jeu

- **Deux joueurs.**
- Chacun choisit simultanément pile (**P**) ou face (**F**).
- Si les deux choisissent la même face, Joueur 1 gagne (+1), Joueur 2 perd (–1).
- Si les faces sont différentes, Joueur 2 gagne (+1), Joueur 1 perd (–1).
- **Jeu à somme nulle.**

---

## Matrice des gains

|            | P (J2)   | F (J2)   |
| :--------: | :------: | :------: |
| **P (J1)** |  1 , –1  | –1 , 1   |
| **F (J1)** | –1 , 1   |  1 , –1  |

---

## Stratégies mixtes

- Joueur 1 joue Pile avec proba p, Face avec 1 – p.
- Joueur 2 joue Pile avec proba q, Face avec 1 – q.

---

## Calcul pour Joueur 1

**Espérance de gain si J1 joue Pile** :
E₁(P) = q × 1 + (1 – q) × (–1) = q – (1 – q) = 2q – 1

**Espérance de gain si J1 joue Face** :
E₁(F) = q × (–1) + (1 – q) × 1 = –q + (1 – q) = 1 – 2q

À l’équilibre, J1 doit être indifférent :
2q – 1 = 1 – 2q  
2q – 1 = 1 – 2q  
2q + 2q = 1 + 1  
4q = 2  
q = 1/2

**Donc J2 doit randomiser Pile/Face à 50%/50%.**

---

## Calcul pour Joueur 2

**Espérance de gain pour J2 si Pile** :
E₂(P) = p × (–1) + (1 – p) × 1 = –p + (1 – p) = 1 – 2p

**Espérance de gain pour J2 si Face** :
E₂(F) = p × 1 + (1 – p) × (–1) = p – (1 – p) = 2p – 1

On égalise :
1 – 2p = 2p – 1  
1 + 1 = 2p + 2p  
2 = 4p  
p = 1/2

**Donc J1 doit randomiser Pile/Face à 50%/50%.**

---

## Résultat : équilibre de Nash

- Joueur 1 : Pile avec 1/2, Face avec 1/2.
- Joueur 2 : Pile avec 1/2, Face avec 1/2.

---

## Explication

- **Matching Pennies n’a pas d’équilibre de Nash en stratégies pures** (aucun couple (P,P), (F,F), (P,F), (F,P) n’est stable).
- **L’unique équilibre de Nash est mixte** : chaque joueur joue au hasard avec 50%/50%.
- **Intuition** : si un joueur est prévisible, l’autre peut toujours le battre ; randomiser parfaitement rend toute stratégie de l’autre indifférente.

> Dans les jeux à somme nulle simples comme Matching Pennies, l’équilibre de Nash est toujours une stratégie mixte “purement aléatoire”.
## 2.5 stag hunt

- Il existe deux équilibres de Nash en stratégies pures dans le Stag Hunt :
    - (Stag, Stag) : gains 2,2 (optimal mais risqué)
    - (Hare, Hare) : gains 1,1 (sûr mais moins bon)
- Si un joueur doute ou "s'égare" (choisit Hare quand l’autre choisit Stag), le chasseur qui restait sur le cerf obtient 0.
- Après une telle expérience, chacun préfère la sécurité du lièvre : le groupe peut rester "bloqué" sur l’équilibre (Hare, Hare).
- **Le jeu illustre l’importance de la confiance et de la coordination pour atteindre le meilleur résultat collectif.**
- Choisir “Hare” (lièvre), c’est choisir la sécurité : tu es sûr de gagner 1, peu importe ce que fait l’autre.
- Choisir “Stag” (cerf) est plus risqué : tu gagnes plus (2) seulement si l’autre choisit aussi “Stag”, sinon tu gagnes 0.
- Si tu crains que l’autre ne coopère pas, ou si la confiance est faible, tu es poussé à choisir “Hare” pour t’assurer un gain minimal garanti.
- C’est pour ça que “Hare” est dit “plus sûr” : pas de mauvaise surprise, pas de risque de repartir sans rien.
## 2.6 equilibre de nash # Équilibre de Nash — Explication détaillée selon Osborne

## 🧩 1. Jeux stratégiques : rappel du concept fondamental

Un **jeu stratégique** est une représentation formelle d’une situation où plusieurs agents (joueurs) prennent simultanément des décisions, chacun cherchant à maximiser son propre gain. Chaque joueur choisit sa stratégie sans connaître les choix des autres joueurs.

Formellement, un jeu stratégique est défini par :

- Un ensemble de joueurs : \( N = \{1, 2, \dots, n\} \)
- Pour chaque joueur \( i \), un ensemble de stratégies possibles \( S_i \)
- Pour chaque joueur \( i \), une fonction de gain (payoff) :
  \[
  u_i : S_1 \times S_2 \times \dots \times S_n \rightarrow \mathbb{R}
  \]

Chaque joueur \( i \) souhaite maximiser \( u_i \), son propre gain.

---

## 🎯 2. Meilleure réponse : un concept central

La notion essentielle pour comprendre l’équilibre de Nash est celle de **meilleure réponse**.

La **meilleure réponse** du joueur \( i \) à un ensemble donné de stratégies des autres joueurs \( s_{-i} \) est la stratégie \( s_i^* \) qui lui donne le plus haut gain possible :

\[
u_i(s_i^*, s_{-i}) \geq u_i(s_i, s_{-i}) \quad\text{pour toute autre stratégie } s_i \in S_i
\]

Autrement dit :  
> « Si les autres choisissent leurs stratégies et ne changent pas, quelle stratégie me rapporte le plus ? »

---

##   Définition formelle de l’Équilibre de Nash

Un **équilibre de Nash** est un profil de stratégies (c’est-à-dire un choix précis pour chaque joueur) tel que **chaque joueur joue une meilleure réponse aux choix des autres**.

Formellement, soit $s^* = (s_1^*, s_2^*, \dots, s_n^*)$ un profil de stratégies pour les $n$ joueurs.  
Ce profil est un équilibre de Nash si, pour chaque joueur $i$ :

$$
u_i(s_i^*, s_{-i}^*) \geq u_i(s_i, s_{-i}^*) \quad \text{pour toute stratégie } s_i \in S_i
$$

Autrement dit :

> *Aucun joueur ne peut améliorer son gain en changeant seul de stratégie, tant que les autres joueurs gardent leur choix.*

Un équilibre de Nash est donc un point de **stabilité stratégique** : chacun maximise son propre gain, étant donné ce que font les autres, et aucun n’a intérêt à dévier individuellement.


---

## 🎲 4. Exemples classiques en détail (selon Osborne)

### 📍 **Dilemme du prisonnier (Osborne 2.2)**

| Joueur 1 \ Joueur 2 | Coopère (C) | Trahit (T) |
|---------------------|-------------|------------|
| Coopère (C)         | 2 , 2       | 0 , 3      |
| Trahit (T)          | 3 , 0       | 1 , 1      |

Analyse détaillée :

- Si le joueur 2 coopère, le joueur 1 préfère trahir (gain 3 > 2).
- Si le joueur 2 trahit, le joueur 1 préfère aussi trahir (gain 1 > 0).
- « Trahir » domine strictement « coopérer ».

L'unique équilibre de Nash est donc : **(Trahit, Trahit)**.

Aucun joueur n’a intérêt à dévier seul (car il passerait de 1 à 0). Cependant, ce résultat est collectivement sous-optimal (1,1 contre 2,2).

---

### 📍 **Bach ou Stravinsky (Osborne 2.3)**

| Joueur 1 \ Joueur 2 | Bach (B) | Stravinsky (S) |
|---------------------|----------|----------------|
| Bach (B)            | 2 , 1    | 0 , 0          |
| Stravinsky (S)      | 0 , 0    | 1 , 2          |

Analyse détaillée :

- (Bach, Bach) : Joueur 1 gagne 2, Joueur 2 gagne 1. Personne n'a intérêt à changer seul (ils passeraient tous deux à 0). Donc **(Bach, Bach)** est un équilibre de Nash.
- (Stravinsky, Stravinsky) : De même, chacun perdrait en changeant seul. Donc **(Stravinsky, Stravinsky)** est aussi un équilibre de Nash.
- Les autres profils (B,S) et (S,B) ne sont pas stables : chacun pourrait gagner en changeant.

Il y a donc deux équilibres de Nash distincts ici.

---

### 📍 **Matching Pennies (Osborne 2.4)**

| Joueur 1 \ Joueur 2 | Pile (P) | Face (F) |
|---------------------|----------|----------|
| Pile (P)            | 1 , -1   | -1 , 1   |
| Face (F)            | -1 , 1   | 1 , -1   |

Analyse détaillée :

- Aucun équilibre en stratégies pures, car chaque profil incite toujours un joueur à changer.
- Nash prouve que même dans ce cas, il existe toujours un équilibre en stratégies mixtes.
- Ici, l'équilibre mixte est que chaque joueur choisisse **Pile ou Face avec probabilité 1/2**, rendant l’autre indifférent à son propre choix.

---

## 🔑 5. Propriétés essentielles de l’équilibre de Nash selon Osborne

- **Existence** : Nash (1950) montre que tout jeu stratégique fini possède au moins un équilibre de Nash (en stratégies pures ou mixtes).
- **Multiplicité** : Certains jeux ont plusieurs équilibres de Nash.
- **Stabilité** : À l'équilibre, personne ne peut améliorer sa situation en changeant unilatéralement.
- **Non optimalité collective** : Un équilibre de Nash n’est pas forcément le meilleur résultat global pour l’ensemble des joueurs (exemple typique : dilemme du prisonnier).

---

## 🗨️ 6. Interprétation intuitive (selon Osborne)

Osborne insiste sur l'interprétation intuitive suivante :

- Un équilibre de Nash est un état où les joueurs anticipent correctement les choix des autres joueurs.
- Chaque joueur joue une stratégie optimale (meilleure réponse) par rapport à ces anticipations.
- À l'équilibre, les anticipations se réalisent parfaitement : chacun anticipe correctement ce que font les autres.

Il s'agit d'une **situation auto-confirmante** :
> « Je fais ce que je fais parce que je prévois correctement les choix des autres joueurs, et ils font ce qu'ils font parce qu'ils prévoient correctement les miens. »

---

## 📝 7. Citation directe d’Osborne (traduction fidèle)

> « Un équilibre de Nash est un profil de stratégies où la stratégie de chaque joueur constitue une meilleure réponse aux stratégies choisies par les autres joueurs. À l'équilibre, aucun joueur ne peut obtenir un gain supérieur en choisissant une autre stratégie, en supposant que les autres joueurs gardent inchangées leurs stratégies. »  
> *(Osborne, Chapitre 2.6)*

---

# 2.7 best response function 
# 🎯 Fonction de meilleure réponse (*Best Response Function*)

La notion de **fonction de meilleure réponse** est fondamentale dans l'analyse des jeux stratégiques. Elle joue un rôle crucial dans la définition et l'identification des équilibres de Nash.

---

## 📌 Définition intuitive détaillée

La **meilleure réponse** d'un joueur à un ensemble donné de stratégies choisies par les autres joueurs est la stratégie qui lui offre le **meilleur gain possible**, en tenant compte du choix précis des autres.

Autrement dit :  
> **« Compte tenu du choix exact des autres joueurs, quelle est la stratégie qui me rapporte le plus ? »**

C'est une manière de capturer la rationalité individuelle des joueurs face à une situation stratégique.

---
## ## 📚 Définition formelle complète (selon Osborne)

Soit un jeu stratégique défini par :

- $N = \{1, 2, \dots, n\}$ : l'ensemble des joueurs.
- Pour chaque joueur $i$, un ensemble de stratégies possibles $S_i$.
- Pour chaque joueur $i$, une fonction de gain (ou de paiement) :
  $$
  u_i(s_1, s_2, \dots, s_n)
  $$
  qui attribue un gain au joueur $i$ selon la combinaison de stratégies choisies par tous les joueurs.
    - $s_i$ : la stratégie choisie par le joueur $i$.
    - $s_{-i}$ : le profil des stratégies choisies par tous les autres joueurs (c'est-à-dire tous les $s_j$ pour $j \neq i$).

La **fonction de meilleure réponse** du joueur $i$ aux stratégies $s_{-i}$ des autres joueurs est formellement définie par :

$$
B_i(s_{-i}) = \{\, s_i^* \in S_i\ |\ u_i(s_i^*, s_{-i}) \geq u_i(s_i, s_{-i}),\ \text{pour tout } s_i \in S_i \,\}
$$

Autrement dit, $B_i(s_{-i})$ est l'ensemble (parfois réduit à une seule stratégie) des choix optimaux pour le joueur $i$, étant donné ce que font les autres joueurs.


---

## ## 🎲 Exemple détaillé : Dilemme du Prisonnier

Considérons le dilemme classique du prisonnier pour mieux comprendre :

| Joueur 1 \ Joueur 2 | Coopère (C) | Trahit (T) |
|---------------------|-------------|------------|
| Coopère (C)         | 2 , 2       | 0 , 3      |
| Trahit (T)          | 3 , 0       | 1 , 1      |

Analysons en détail la fonction de meilleure réponse de chaque joueur.

### 📍 Pour le Joueur 1 :

- Si le Joueur 2 joue **Coopère (C)** :
  - Joueur 1 gagne 2 s'il coopère, 3 s'il trahit.
  - Donc, la meilleure réponse à « Coopère » est **Trahir (T)**.

- Si le Joueur 2 joue **Trahir (T)** :
  - Joueur 1 gagne 0 s'il coopère, 1 s'il trahit.
  - Donc, la meilleure réponse à « Trahir » est aussi **Trahir (T)**.

En notation formelle, on a donc :

- $B_1(\text{Coopère}) = \{\text{Trahir}\}$  meilleur réponse de J1 si J2 coopère
- $B_1(\text{Trahir}) = \{\text{Trahir}\}$ meilleur réponse de J1 si J2 trahis

Résumé dans un tableau :

| Choix du joueur 2 | Meilleure réponse du joueur 1 $B_1(\cdot)$ |
|-------------------|--------------------------------------------|
| Coopère           | Trahir                                     |
| Trahir            | Trahir                                     |

En bref, $B_1(s_2)$ = Trahir pour tout $s_2$.

### 📍 De même, pour le Joueur 2 (symétriquement) :

- $B_2(\text{Coopère}) = \{\text{Trahir}\}$
- $B_2(\text{Trahir}) = \{\text{Trahir}\}$

| Choix du joueur 1 | Meilleure réponse du joueur 2 $B_2(\cdot)$ |
|-------------------|--------------------------------------------|
| Coopère           | Trahir                                     |
| Trahir            | Trahir                                     |

Donc, $B_2(s_1)$ = Trahir pour tout $s_1$.

Ainsi, on obtient clairement que l’équilibre de Nash est **(Trahir, Trahir)**,  
c'est-à-dire le seul profil $(s_1^*, s_2^*)$ où $s_1^* \in B_1(s_2^*)$ et $s_2^* \in B_2(s_1^*)$.


🎲 Exemple détaillé : Dilemme du Prisonnier

Considérons le dilemme classique du prisonnier pour mieux comprendre :

| Joueur 1 \ Joueur 2 | Coopère (C) | Trahit (T) |
|---------------------|-------------|------------|
| Coopère (C)         | 2 , 2       | 0 , 3      |
| Trahit (T)          | 3 , 0       | 1 , 1      |

Analysons en détail la fonction de meilleure réponse de chaque joueur.

### 📍 Pour le Joueur 1 :

- Si le Joueur 2 joue **Coopère** :
  - Joueur 1 gagne 2 s'il coopère, 3 s'il trahit.
  - Donc, la meilleure réponse à « Coopère » est **Trahir**.

- Si le Joueur 2 joue **Trahir** :
  - Joueur 1 gagne 0 s'il coopère, 1 s'il trahit.
  - Donc, la meilleure réponse à « Trahir » est aussi **Trahir**.

Ainsi, pour le Joueur 1, la fonction de meilleure réponse est :

| Choix du joueur 2 | Meilleure réponse du joueur 1 |
|-------------------|-------------------------------|
| Coopère           | Trahir                        |
| Trahir            | Trahir                        |

En bref, le joueur 1 répond toujours par **Trahir**.

### 📍 De même, pour le Joueur 2 (symétriquement) :

- Il répond toujours par **Trahir**.

Ainsi, on obtient clairement l’équilibre de Nash **(Trahir, Trahir)**.

---

## 📊 Représentation graphique ou conceptuelle (Best Response Function)

La fonction de meilleure réponse peut aussi être représentée graphiquement ou conceptuellement :
- **Axe horizontal** : stratégies possibles des autres joueurs ($s_{-i}$)
- **Axe vertical** : meilleure réponse (stratégie optimale) du joueur étudié ($s_i^*$)

Un équilibre de Nash correspond alors à l’intersection simultanée des fonctions de meilleure réponse de tous les joueurs.

---

## 🔑 Importance conceptuelle de la meilleure réponse

Pourquoi cette notion est-elle si essentielle ?

- Elle permet de déterminer clairement les équilibres de Nash :
  - Un équilibre de Nash est précisément un point où **tous les joueurs choisissent simultanément une meilleure réponse aux choix des autres**.
- Elle illustre précisément le principe de rationalité individuelle :
  - Chaque joueur cherche toujours à faire le meilleur choix possible face à ce que font les autres joueurs.
- Elle clarifie les anticipations rationnelles :
  - La fonction de meilleure réponse traduit l’idée que les joueurs anticipent correctement les choix des autres pour déterminer leur propre stratégie optimale.

---
## 2.8.2 — Utilisation des fonctions de meilleure réponse pour définir l’équilibre de Nash

Un **équilibre de Nash** est un profil d’actions (c’est-à-dire un choix de stratégie pour chaque joueur) tel qu’aucun joueur ne peut obtenir un gain supérieur en modifiant unilatéralement sa propre action, les choix des autres restant inchangés.

En termes de **fonctions de meilleure réponse**, on peut alors dire qu’un équilibre de Nash est un profil dans lequel **chaque joueur joue une meilleure réponse aux actions des autres**.

**Proposition 34.1 — Définition équivalente de l’équilibre de Nash**  
Soit $a^*$ un profil d’actions. Alors $a^*$ est un équilibre de Nash si et seulement si, pour chaque joueur $i$ :
$$
a^*_i \in B_i(a^*_{-i})
$$
C’est-à-dire : l’action $a^*_i$ du joueur $i$ est une meilleure réponse à la combinaison des actions $a^*_{-i}$ des autres joueurs.

Si chaque joueur $i$ possède une **unique** meilleure réponse à chaque choix des autres ($B_i(a_{-i}) = \{b_i(a_{-i})\}$), la condition précédente devient simplement un système d’équations :
$$
a^*_i = b_i(a^*_{-i}) \quad \text{pour chaque joueur } i
$$
Dans un jeu à deux joueurs ($n=2$), ces équations s’écrivent :
$$
a^*_1 = b_1(a^*_2) \\
a^*_2 = b_2(a^*_1)
$$
Un profil $(a^*_1, a^*_2)$ est donc un équilibre de Nash si et seulement si :
- L’action de Joueur 1 est la meilleure réponse à l’action de Joueur 2
- L’action de Joueur 2 est la meilleure réponse à l’action de Joueur 1

---

## 2.8.3 — Utilisation des fonctions de meilleure réponse pour trouver les équilibres de Nash

Cette définition inspire une **méthode systématique** pour identifier les équilibres de Nash dans un jeu fini :

1. **Trouver la fonction de meilleure réponse de chaque joueur** : pour chaque combinaison des autres, déterminer la meilleure (ou les meilleures) action(s).
2. **Rechercher les profils qui satisfont simultanément toutes les conditions ci-dessus** (c’est-à-dire, là où chaque joueur choisit effectivement une meilleure réponse aux autres).

Si chaque joueur a une meilleure réponse unique, il suffit de résoudre le système d’équations ci-dessus. Sinon, il faut lister les profils où tous les joueurs choisissent une meilleure réponse à ce que font les autres.

---

## 📋 **Exemple illustratif — Lecture d’un tableau**

Considérons le jeu suivant (Figure 35.1) :

|       |    L    |    C    |    R    |
|-------|---------|---------|---------|
| **T** | 1, 2★   | 2★, 1   | 1★, 0   |
| **M** | 2★, 1★  | 0, 1★   | 0, 0    |
| **B** | 0, 1    | 0, 0    | 1★, 2★  |

- **Colonnes** : actions du Joueur 2 (L, C, R)
- **Lignes** : actions du Joueur 1 (T, M, B)
- **Premier nombre** : gain de Joueur 1
- **Second nombre** : gain de Joueur 2
- **★** : meilleure réponse pour le joueur concerné

### Étapes pour trouver les équilibres :

1. **Pour chaque colonne (L, C, R)** :  
   Chercher la meilleure réponse de Joueur 1 (plus grand chiffre dans la colonne) → mettre une ★ à côté du gain de J1.
2. **Pour chaque ligne (T, M, B)** :  
   Chercher la meilleure réponse de Joueur 2 (plus grand chiffre dans la ligne) → mettre une ★ à côté du gain de J2.
3. **Chercher les cases où les deux gains sont étoilés** :
   - (M, L) : $2^\star, 1^\star$
   - (B, R) : $1^\star, 2^\star$

Chaque case doublement étoilée correspond à un **équilibre de Nash**.

---

### 📝 Résumé littéraire

> La méthode des fonctions de meilleure réponse permet d’identifier visuellement les équilibres de Nash : ce sont exactement les cases du tableau où chaque joueur joue une meilleure réponse à l’action de l’autre. Ainsi, un équilibre de Nash, c’est un profil où chacun, connaissant le choix de l’autre, n’a rien à gagner à changer son propre choix.

## 🎲 Exemple 37.1 — Une relation synergique (Osborne, §2.8)

Deux individus sont engagés dans une relation synergique.  
- Plus **chacun investit d’effort** dans la relation, mieux ils se portent tous les deux… jusqu’à un certain point :  
- Pour un effort de l’autre fixé, **le gain individuel augmente puis diminue** si on investit trop (effet "courbe en cloche").

### ⚙️ Modélisation du jeu

- **Joueurs :** deux individus (1 et 2)
- **Actions :** chaque joueur choisit un niveau d’effort $a_i$ (nombre réel positif)
- **Préférences :** pour chaque joueur $i$, le gain est donné par :
  
  $$
  u_i(a_i, a_j) = a_i \big(c + a_j - a_i\big)
  $$
  - $a_i$ : effort du joueur $i$
  - $a_j$ : effort de l’autre joueur
  - $c$ : constante positive

---

### 🔎 Analyse — Fonction de meilleure réponse

Pour un effort de l’autre joueur ($a_j$) fixé, le gain $u_i$ est une fonction **quadratique** de $a_i$ :  
- $u_i = a_i(c + a_j - a_i)$  
- Cette fonction vaut 0 pour $a_i = 0$ et pour $a_i = c + a_j$ (donc elle a un maximum entre les deux).

**Le maximum est obtenu pour :**
$$
b_i(a_j) = \frac{1}{2}(c + a_j)
$$

*Si tu connais les dérivées, c’est juste la solution de $\frac{du_i}{da_i} = 0$.*

---

### 📈 Lecture graphique des fonctions de meilleure réponse

- $b_1(a_2)$ : meilleure réponse de J1 à chaque choix de $a_2$ (c’est une droite dans le plan $(a_1, a_2)$).
- $b_2(a_1)$ : meilleure réponse de J2 à chaque $a_1$ (autre droite).

Pour lire :
- **Choisis une valeur de $a_2$ (vertical)**, va à la courbe $b_1$, descends : tu trouves $a_1 = b_1(a_2)$.
- **Choisis une valeur de $a_1$ (horizontal)**, va à la courbe $b_2$, monte : tu trouves $a_2 = b_2(a_1)$.

Un **équilibre de Nash** est un point $(a_1^*, a_2^*)$ où ces deux fonctions se coupent (intersection des deux droites) :
$$
a_1^* = b_1(a_2^*) \qquad\text{et}\qquad a_2^* = b_2(a_1^*)
$$

---

### 🧮 Calcul explicite de l’équilibre de Nash

On a les deux équations suivantes :
- $a_1^* = \frac{1}{2}(c + a_2^*)$
- $a_2^* = \frac{1}{2}(c + a_1^*)$

On remplace l’une dans l’autre :

1. $a_1^* = \frac{1}{2}\left(c + \frac{1}{2}(c + a_1^*)\right)$  
2. $a_1^* = \frac{1}{2}(c + \frac{1}{2}c + \frac{1}{2}a_1^*)$  
3. $a_1^* = \frac{1}{2}c + \frac{1}{4}c + \frac{1}{4}a_1^*$  
4. $a_1^* - \frac{1}{4}a_1^* = \frac{3}{4}c$  
5. $\frac{3}{4}a_1^* = \frac{3}{4}c$  
6. $a_1^* = c$

Pareil pour $a_2^*$ : $a_2^* = \frac{1}{2}(c + a_1^*) = \frac{1}{2}(c + c) = c$

Donc l’**unique équilibre de Nash** est :
$$
(a_1^*, a_2^*) = (c, c)
$$

---

### 🌟 Remarques et généralisation

- **Unicité** : Ici, il n’y a **qu’un seul équilibre**, car les deux droites se croisent en un unique point.
- **Si la fonction de meilleure réponse est "épaisse"** (plusieurs meilleures réponses possibles pour certains choix de l’autre), il peut y avoir **une infinité d’équilibres de Nash** (tous les points d’intersection).
- **Graphiquement**, chaque intersection des deux courbes $b_1$ et $b_2$ correspond à un équilibre de Nash.

---

### 📝 Résumé

- Quand chaque joueur a une meilleure réponse unique à chaque choix de l’autre, il suffit de résoudre le système :
  - $a_1^* = b_1(a_2^*)$
  - $a_2^* = b_2(a_1^*)$
- Ici, **l’effort optimal est $c$ pour chaque joueur**.
- En général, **chaque point d’intersection des fonctions de meilleure réponse** correspond à un équilibre de Nash.

---

> **Ce type d’exemple montre la puissance du formalisme des best response : on n’a même pas besoin de tableau de jeu, il suffit d’écrire les fonctions et de chercher leurs points de croisement.**

# 2.8.4 Contribuer à un bien public : explication détaillée et lecture graphique

## 1️⃣ Le modèle

- Deux joueurs (personnes), chacun choisit combien $c_i$ il contribue à un bien public (ex : propreté d’un parc).
- Plus la somme $c_1 + c_2$ est élevée, plus chacun est satisfait… mais donner coûte (ça fait moins pour les “biens privés”).
- Chaque joueur cherche à maximiser :  
  $u_i(c_1, c_2) = v_i(c_1 + c_2) - c_i$
    - $v_i$ : utilité tirée du bien public, fonction “courbe en cloche” (monte puis descend)
    - $-c_i$ : coût de la contribution

---

## 2️⃣ Fonction de meilleure réponse

- Pour un montant donné $c_2$ de l’autre, **quelle contribution $c_1$ maximise mon bien-être ?**
- Si l’autre ne donne rien, mon “optimum” s’appelle $b_1(0)$ (même chose pour J2 avec $b_2(0)$).
- Si l’autre donne $k$, mon optimum est : $b_1(k) = \max(b_1(0) - k, 0)$.
    - Donc, **plus l’autre donne, moins je suis incité à donner**.

---

## 3️⃣ Interprétation du premier graphique (Figure 41.1)

- **Axe horizontal :** montant donné par J1 ($c_1$)
- **Courbe $u_1(c_1, 0)$** : satisfaction de J1 quand J2 ne donne rien.
    - Monte jusqu’au maximum $b_1(0)$, puis descend (donner trop coûte trop).
- **Courbe $u_1(c_1, k)$** : satisfaction de J1 quand J2 donne $k$.
    - **C’est la courbe précédente, décalée vers la gauche et vers le haut de $k$**.
    - Le maximum se trouve à $b_1(k) = b_1(0) - k$ (s’il reste positif).

**Interprétation** :  
> Plus l’autre donne, moins je suis prêt à donner pour obtenir le même “niveau de bien public”.  
> Si l’autre donne plus que ce que je voulais donner moi-même, ma meilleure réponse devient zéro.

---

## 4️⃣ Interprétation du deuxième graphique (Figure 42.1)

- **Axe horizontal :** $c_1$ (contribution de J1)
- **Axe vertical :** $c_2$ (contribution de J2)
- **Droite noire ($b_1(c_2)$)** : meilleure réponse de J1 selon ce que fait J2 (pente –1, coupe l’axe horizontal en $b_1(0)$)
- **Droite grise ($b_2(c_1)$)** : meilleure réponse de J2 selon ce que fait J1 (pente –1, coupe l’axe vertical en $b_2(0)$)

**L’équilibre de Nash correspond au(x) point(s) où ces deux droites se croisent** :

- Si $b_1(0) > b_2(0)$, l’intersection est $(b_1(0), 0)$ (J1 donne tout, J2 rien)
- Si $b_2(0) > b_1(0)$, c’est $(0, b_2(0))$ (J2 donne tout, J1 rien)
- Si $b_1(0) = b_2(0)$, l’intersection est tout le segment $c_1 + c_2 = b_1(0)$ (partage possible)

---

## 5️⃣ Sens global et enseignement du modèle

- **Le jeu formalise le problème du “passager clandestin” (free-rider problem)** : chacun espère que l’autre paiera la facture du bien collectif.
- **À l’équilibre, seul le plus motivé contribue**, sauf si les deux veulent donner exactement la même chose (cas rare).
- **Graphiquement**, tu peux toujours lire l’équilibre de Nash comme **le point d’intersection des courbes de meilleure réponse**.

---

### ✏️ Résumé

- Plus l’autre contribue, moins je contribue.
- L’équilibre de Nash est là où chacun fait la meilleure réponse à l’autre (intersection des courbes).
- Dans ce modèle, **un seul joueur contribue**, l’autre “profite”, sauf cas parfaitement symétrique.
- - **Quand la droite de meilleure réponse d’un joueur coupe l’axe horizontal ($c_2 = 0$),**  
  ça veut dire que **Joueur 1 donne tout ce qu’il “veut” donner, Joueur 2 ne donne rien**.
  - Point d’équilibre : $(c_1^*, c_2^*) = (b_1(0), 0)$

- **Quand la droite de meilleure réponse de l’autre coupe l’axe vertical ($c_1 = 0$),**  
  ça veut dire que **Joueur 2 donne tout, Joueur 1 ne donne rien**.
  - Point d’équilibre : $(c_1^*, c_2^*) = (0, b_2(0))$

- **Si les deux droites se croisent “au milieu” (c’est rare),**  
  c’est qu’ils sont prêts à donner exactement la même somme et  
  **toutes les répartitions où $c_1^* + c_2^* = b_1(0) = b_2(0)$ sont alors des équilibres**.

---

**En résumé** :
- **Croisement sur l’axe horizontal** : seul le joueur 1 contribue, l’autre rien.
- **Croisement sur l’axe vertical** : seul le joueur 2 contribue, l’autre rien.
- **Croisement “au milieu”** : les deux peuvent partager exactement la somme.


> Les deux graphiques montrent comment la stratégie de chacun s’ajuste à la générosité de l’autre, et pourquoi le financement des biens publics est souvent difficile sans coordination extérieure.

# 2.9 Actions dominées, domination stricte et faible

## 1. Domination stricte

- **Idée intuitive :**  
  Une action est **strictement dominée** si, peu importe ce que font les autres joueurs, il existe une autre action qui donne TOUJOURS un résultat strictement meilleur.

### 🚦 Exemples concrets

- Feu rouge, deux files :  
  La file de gauche (libre) **domine strictement** celle de droite (risque d’être bloqué par un piéton ou une voiture qui tourne).  
  => Mieux d’être toujours à gauche, peu importe ce que font les autres.

- **Définition formelle (Osborne) :**  
  L’action $a_i^{\prime}$ de joueur $i$ **domine strictement** $a_i$ si, pour toute combinaison $a_{-i}$ des autres :
  $$
  u_i(a_i^{\prime}, a_{-i}) > u_i(a_i, a_{-i}) \quad \text{pour tout } a_{-i}
  $$

- **Dans le Dilemme du Prisonnier :**  
  “Trahir” (Fink) domine strictement “Se taire” (Quiet) :  
  Peu importe ce que fait l’autre, “Trahir” rapporte toujours plus.

- **Effet sur l’analyse des jeux :**  
  - **Une action strictement dominée ne sera jamais choisie dans un équilibre de Nash.**
  - On peut donc les **éliminer du jeu** pour simplifier la recherche d’équilibres.

- **Exemples du livre (Figure 44.1, gains de joueur 1) :**

|     | L | R |
|-----|---|---|
| T   | 1 | 0 |
| M   | 2 | 1 |
| B   | 1 | 3 |

Ici, M domine strictement T, mais B est parfois meilleur que M. T est strictement dominée et **ne peut pas apparaître dans un équilibre**.

---

## 2. Domination faible

- **Idée intuitive :**  
  Une action est **faiblement dominée** si elle n’est JAMAIS meilleure, et parfois pire, qu’une autre action.

- **Exemple concret :**  
  Deux files au feu, une voiture dans chaque :  
  Si la voiture de droite ne tourne pas, les files sont équivalentes ;  
  si elle tourne, la file de gauche est meilleure.  
  => La file de gauche **faiblement domine** la droite.

- **Définition formelle (Osborne) :**  
  L’action $a_i^{\prime}$ de joueur $i$ **faiblement domine** $a_i$ si :
  $$
  u_i(a_i^{\prime}, a_{-i}) \geq u_i(a_i, a_{-i}) \ \forall a_{-i},\quad \text{et strictement pour au moins un } a_{-i}
  $$

- **Effet sur l’analyse :**
  - Une action faiblement dominée **peut parfois apparaître dans un équilibre de Nash non-strict** (mais jamais dans un équilibre strict).

---

## 3. Illustration et cas particuliers

- **Figure 45.1 (payoffs de joueur 1)** :

|     | L | R |
|-----|---|---|
| T   | 1 | 0 |
| M   | 2 | 0 |
| B   | 2 | 1 |

Ici,  
- M faiblement domine T,  
- B faiblement domine M,  
- B strictement domine T.

- **Conclusion du livre :**
  - Toute action strictement dominée peut être éliminée, car aucun joueur rationnel ne la jouera.
  - Une action faiblement dominée n’est JAMAIS jouée dans un équilibre strict, mais peut l’être dans un équilibre de Nash “ordinaire”.

---

## 4. Synthèse

- **Stratégie strictement dominée** : Jamais rationnelle, jamais choisie à l’équilibre.
- **Stratégie faiblement dominée** : Pas optimale, mais parfois utilisée à l’équilibre si les autres actions ne sont pas strictement meilleures.

> **Résumé :**  
> Éliminer les stratégies strictement dominées simplifie la recherche d’équilibre.  
> Les stratégies faiblement dominées demandent plus de prudence : elles peuvent parfois survivre dans les équilibres de Nash “non stricts”.

---

## 2.10 Qu’est-ce qu’un équilibre symétrique ?

Un **équilibre symétrique** est un équilibre de Nash dans lequel **tous les joueurs adoptent exactement la même stratégie**.

### 📌 Définition formelle

- Un jeu est **symétrique** si tous les joueurs ont le même ensemble d’actions et la fonction de gain (payoff) est la même pour tous (quand on échange les rôles).
- Un **équilibre symétrique** est alors un équilibre où **chaque joueur choisit la même action ou la même règle de choix (stratégie mixte)**.

### 🧩 Pourquoi c’est utile ?

- Cela réduit souvent le nombre de cas à étudier (on cherche d’abord les équilibres où tout le monde fait pareil).
- Beaucoup de jeux naturels (Dilemme du Prisonnier, Bataille des sexes, certains jeux de coordination…) admettent des équilibres symétriques, parfois en plus d’autres équilibres.

### 📋 Exemples

- **Dilemme du Prisonnier** :  
  L’équilibre (Trahir, Trahir) est **symétrique** (les deux font la même chose).
- **Matching Pennies** :  
  L’équilibre mixte (Pile 1/2, Face 1/2) pour chaque joueur est **symétrique**.
- **Bataille des Sexes (BoS)** :  
  Les équilibres purs (Bach, Bach) et (Stravinsky, Stravinsky) sont **symétriques** si les préférences sont identiques.

### ✏️ À retenir

> Un **équilibre symétrique**, c’est quand “tout le monde joue pareil” dans un jeu où cela a un sens (mêmes règles, mêmes actions, mêmes préférences).

---

**Résumé** :  
- Équilibre symétrique = chaque joueur adopte la même stratégie dans un équilibre de Nash.
- Ça n’existe que dans les jeux “symétriques” (mêmes actions et gains pour tous).

:(-------)
# Chapitre 4 : mixed strategies

# 4.1.1 — États stationnaires stochastiques (“Stochastic steady states”)

## 🧩 Contexte : que veut dire “état stationnaire” ?

- **Un équilibre de Nash** classique correspond à une situation où, si chaque joueur répète toujours la même action optimale, aucun n’a intérêt à changer seul.
- Cela modélise une situation “idéale” où, dans chaque rôle de joueur, on a une **population** (groupe d’individus possibles), et à chaque partie, un individu est tiré au hasard dans chaque population.
- **Dans un état stationnaire** (steady state), les comportements restent constants dans le temps :  
  chaque joueur fait la même chose à chaque partie, et n’a aucune raison de changer car il connaît (par expérience) ce que font les autres.

---

## 🔄 État stationnaire “pur” et “mixte”

- **État stationnaire pur** :  
  Chacun joue **toujours la même action** (tout le monde se comporte pareil dans son groupe), donc chaque partie donne le même profil d’équilibre de Nash.

- **États stationnaires plus généraux** :  
  On permet que les joueurs ou les membres d’une population **varient leur choix**, tant que la “répartition globale” reste constante.
    - Par exemple, une fraction $p$ des joueurs joue une action $a$.
    - Ou alors, chaque joueur tire **au hasard** son action selon une même loi de probabilité (même distribution chaque fois).

- **Ces deux visions sont équivalentes** :
    - Si dans une population, $p$ % des gens choisissent $a$, c’est mathématiquement pareil que si chaque individu choisit $a$ avec probabilité $p$.

---

## 🎲 Lien avec l’équilibre de Nash “mixte”

- **Un “mixed strategy Nash equilibrium” (équilibre de Nash en stratégies mixtes)** modélise précisément ces états stationnaires où les joueurs ne font pas toujours le même choix, mais gardent une distribution stable de comportements.
- En pratique, on retient surtout la vision “probabiliste” :  
  chaque joueur joue chaque action possible **avec une certaine probabilité fixe**, à chaque fois qu’il joue.

- **Un état stationnaire stochastique** (“stochastic steady state”) = situation où, dans le temps, la répartition des choix reste stable, même si les choix individuels changent.

---

### 📝 À retenir

> Un “état stationnaire stochastique”, c’est un modèle où chaque joueur choisit ses actions au hasard, toujours selon la même loi de probabilité, et où ce “tirage” forme un équilibre de Nash mixte : aucun joueur n’a intérêt à changer sa façon de tirer au hasard.

---

**Résumé**
- État stationnaire pur = chaque joueur joue toujours la même action.
- État stationnaire stochastique = chaque joueur joue chaque action selon une même probabilité fixe (stratégie mixte).
- Ces deux notions sont modélisées par les équilibres de Nash (purs ou mixtes).

## 🎲 Exemple simple : Pierre-Feuille-Ciseaux

Prenons le jeu **Pierre-Feuille-Ciseaux** (Rock-Paper-Scissors), joué entre deux joueurs.

- **Tableau des gains** (gagnant = +1, perdant = –1, égalité = 0) :

|             | Pierre | Feuille | Ciseaux |
|-------------|--------|---------|---------|
| **Pierre**  |  0,0   | –1,+1   | +1,–1   |
| **Feuille** | +1,–1  |  0,0    | –1,+1   |
| **Ciseaux** | –1,+1  | +1,–1   |  0,0    |

---

### 🟢 **État stationnaire pur**

- Si chaque joueur **joue toujours Pierre**, alors chaque partie sera (Pierre, Pierre) :  
  c’est un état stationnaire pur (mais ce n’est pas un équilibre de Nash, car changer d’action peut rapporter plus).

---

### 🔄 **État stationnaire stochastique (stratégie mixte)**

- Supposons maintenant que **chaque joueur, à chaque partie, choisit Pierre, Feuille ou Ciseaux avec proba 1/3**.
- Personne ne change sa “façon de tirer” (la distribution reste la même chaque fois).

- **Résultat :**
    - À chaque partie, le résultat est aléatoire,  
      **mais la “répartition globale” (1/3, 1/3, 1/3)** reste stable dans le temps.
    - **Aucun joueur n’a intérêt à changer sa stratégie aléatoire** (c’est un équilibre de Nash mixte : si l’autre joue 1/3–1/3–1/3, ta meilleure réponse est aussi de randomiser à 1/3–1/3–1/3).

---

### 🧠 **Interprétation de la population**

- Imagine que, dans chaque rôle, tu as toute une population de “joueurs potentiels” : à chaque partie, tu tires un joueur au hasard.
- **Si 1/3 de la population choisit Pierre, 1/3 Feuille, 1/3 Ciseaux**,  
  c’est exactement pareil que si chaque joueur individuel tire au hasard avec proba 1/3 chaque fois :  
  la probabilité d’obtenir Pierre face à Ciseaux est la même.

---

### 📝 À retenir

- **État stationnaire stochastique = équilibre de Nash mixte**
    - Les joueurs ne jouent pas toujours la même action, mais la **probabilité** de chaque action reste constante dans le temps.
    - Le système est stable : si tu changes tes probabilités seul, tu ne gagnes rien à long terme.

---

### **Autres exemples**

- **Matching Pennies** : chaque joueur joue Pile ou Face avec proba 1/2, à chaque tour.
- **En économie** : chaque agent choisit d’investir ou non dans un projet avec une certaine probabilité : tant que les proportions restent stables, c’est un état stationnaire stochastique.

---

> **Conclusion** :  
> Un état stationnaire stochastique, c’est quand, même si chaque individu varie son choix à chaque partie,  
> **la “loi des grands nombres” fait que la répartition globale reste la même**, et aucun n’a intérêt à changer ses habitudes probabilistes.

# 4.2 — Jeux stratégiques où les joueurs peuvent randomiser

## 🧩 Pourquoi changer le modèle ?

- Avant (chap. 2), on supposait que chaque joueur choisit **une action “pure”** à chaque partie.
- Pour modéliser les **états stationnaires stochastiques** (stratégies mixtes), il faut autoriser chaque joueur à **randomiser ses choix** : choisir chaque action avec une certaine probabilité.

---

## 🟢 Qu’est-ce qu’un jeu stratégique avec préférences vNM ?

- On étend la définition d’un jeu stratégique :  
  Chaque joueur a des **préférences sur des “loteries”** (distributions de probabilité) sur les profils d’action, et non plus juste sur les résultats certains.
- Ces préférences sont **représentées par l’espérance mathématique d’une fonction de gain dite “payoff function de Bernoulli”**.
    - C’est ce qu’on appelle une **préférence vNM** (von Neumann-Morgenstern).

---

## 🎲 Qu’est-ce que ça change dans le tableau des gains ?

- Les tableaux (matrices) ressemblent à ceux vus en chap. 2,  
  **mais les nombres dans chaque case ne sont plus seulement un “ordre de préférence”** (ordinal),  
  ce sont **des valeurs cardinales** qui représentent la “valeur” réelle de chaque issue ET de chaque loterie.
- **Exemple :**  
  Le gain pour “(Q, Q)” n’est plus seulement “meilleur que (F, F)” —  
  il doit aussi permettre de calculer la valeur attendue d’une loterie (exemple : 50% de (F, Q), 50% de (F, F)).

---

## 🔍 Pourquoi deux tableaux “identiques” au sens ordinal ne sont pas toujours équivalents en vNM ?

- **Même ordre de préférence** (ordinal) ne veut pas dire “même évaluation des loteries” (cardinal).
- **Exemple dans le livre** (figure 104.1, Prisoner’s Dilemma) :

|   | Q       | F       |
|---|---------|---------|
| Q | 2, 2    | 0, 3    |
| F | 3, 0    | 1, 1    |

|   | Q       | F       |
|---|---------|---------|
| Q | 3, 3    | 0, 4    |
| F | 4, 0    | 1, 1    |

- **Dans le tableau de gauche** :
    - Pour Joueur 1, le score de (Q, Q) = 2 = 0.5×3 + 0.5×1 = score attendu de la loterie [(F, Q), (F, F)] avec proba 50/50.
    - Donc J1 est indifférent entre le résultat sûr (Q, Q) et la loterie.
- **Dans le tableau de droite** :
    - Pour Joueur 1, (Q, Q) = 3 > 0.5×4 + 0.5×1 = 2.5 (score attendu de la même loterie).
    - J1 préfère donc le résultat certain (Q, Q) à la loterie.
- **Donc** : mêmes préférences ordonnées, mais **pas la même attitude vis-à-vis du risque** (aversion, indifférence, appétence…).

---

## ✏️ À retenir

- **Pour modéliser des jeux où les joueurs peuvent randomiser leurs choix, il faut raisonner avec des préférences vNM** (c’est-à-dire : prendre en compte la valeur attendue des gains).
- **Deux jeux “équivalents” ordinalement** peuvent être **très différents** quand on autorise les stratégies mixtes.
- **La différence** : la “valeur” d’une loterie dépend de la façon dont les scores (dans les cases) sont définis ; ce n’est pas qu’un simple classement.

---

> **Résumé** :  
> Pour l’étude des stratégies mixtes, il ne suffit plus de classer les issues “du pire au meilleur” : il faut donner un sens à la valeur attendue des loteries,  
> d’où l’importance des préférences vNM et des “payoff functions” de type cardinal.

