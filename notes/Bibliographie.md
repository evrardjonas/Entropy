# Bibliographie commentée

## Livres

### Bishop (1995) – _Neural Networks for Pattern Recognition_
- Type : Livre  
- Résumé : Référence pour l’approche probabiliste des réseaux de neurones. Contient les fondements théoriques du softmax et du maximum a posteriori.  
- Intérêt pour le projet : Cadre conceptuel pour justifier l’usage d’une distribution softmax dans un contexte de choix stratégique.  
- BibTeX : `bishop1995nn`

### Martin J. Osborne (2003) – _An Introduction to Game Theory_
- Type : Livre (théorie des jeux)  
- Fichier : `Martin J. Osborne - An Introduction to Game Theory (2003, Oxford University Press, USA) - libgen.li.pdf`  
- Résumé : Ouvrage pédagogique couvrant équilibre de Nash, stratégies mixtes, jeux bayésiens.  
- Intérêt pour le projet : Définitions formelles et rappels pour l’introduction et la méthodologie.  
- À lire : Chap. 2 (Nash), Chap. 4 (Mixed strategies), Chap. 9 (Bayesian games, optionnel)  
- BibTeX : `osborne2003game`

### MacKay (2003) – _Information Theory, Inference, and Learning Algorithms_
- Type : Livre (théorie de l’information)  
- Fichier : `Information Theory, Inference, and Learning Algorithms.pdf`  
- Résumé : Fondements de l’entropie et de la divergence KL ; justification “maximum entropy” ; inférence probabiliste.  
- Intérêt pour le projet : Justification mathématique du recours à softmax/maximum entropy et de la calibration via KL.  
- À lire : Ch. 1–3 (entropie, probabilité, KL) ; Ch. 27 (maximum entropy, softmax) ; Ch. 28 (modèles probabilistes)  
- BibTeX : `mackay2003info`

### Cover & Thomas (2006) – _Elements of Information Theory_ (2e éd.)
- Type : Livre (théorie de l’information)  
- Fichier : à ajouter si besoin (`Cover_Thomas_InfoTheory.pdf`)  
- Résumé : Référence sur entropie, divergence KL, distributions exponentielles, maximum entropy.  
- Intérêt pour le projet : Base formelle pour entropie/KL/softmax.  
- À lire : Ch. 2–3 (Shannon, KL, information mutuelle) ; Ch. 11–12 (maximum entropy, applications)  
- BibTeX : `cover2006info`

### Jaynes (2003) – _Probability Theory: The Logic of Science_ (bonus)
- Type : Livre (inférence bayésienne)  
- Résumé : Approfondit la justification bayésienne de maximum entropy.  
- Intérêt pour le projet : Renforce l’assise théorique de l’approche maximum entropy et des calibrations.  
- BibTeX : `jaynes2003prob`

### Wasserman (2004) – _All of Statistics_
- Type : Livre (statistique appliquée)  
- Résumé : Introduction pratique à l’inférence (MLE, intervalles, tests, bootstrap) et modèles.  
- Intérêt pour le projet : Bonnes pratiques de modélisation et d’évaluation statistique.  
- À lire : MLE, intervalles, bootstrap, modèles linéaires (et mixtes si besoin)  
- BibTeX : `wasserman2004allstats`

---

## Articles scientifiques

### Guo et al. (2017) – _On Calibration of Modern Neural Networks_
- Type : Article (ICML)  
- Fichier : `On Calibration of Modern Neural Networks.pdf`  
- Résumé : Montre la mauvaise calibration fréquente des réseaux modernes et propose le temperature scaling.  
- Intérêt pour le projet : Motive l’ajustement de la “température” (analogue de β) pour produire des probabilités fiables.  
- BibTeX : `guo2017calibration`

### Pearce et al. (2021) – _Understanding Softmax Confidence and Uncertainty_
- Type : Preprint (arXiv)  
- Fichier : `Understanding Softmax Confidence and Uncertainty.pdf`  
- Résumé : Analyse la confiance/incertitude issue du softmax et ses limites.  
- Intérêt pour le projet : Cadre pour discuter l’incertitude de la distribution softmax au-delà de l’argmax.  
- BibTeX : `pearce2021softmax`

### Chowdhary et al. (2023) – _Quantifying human performance in chess_ (Nature Human Behaviour)
- Type : Article (référence empirique, échecs)  
- Fichier : `nature.pdf`  
- Résumé : Mesure l’entropie/diversité des choix d’ouverture par quartiles Elo.  
- Intérêt pour le projet : Inspiration pour relier entropie et expertise ; base comparative pour β(Elo).  
- À relire : Méthodes de catégorisation Elo ; calcul entropie/diversité  
- BibTeX : `chowdhary2023chess`

### Shlens (2014) – _Notes on Kullback–Leibler Divergence_
- Type : Note (arXiv)  
- Fichier : `kl divergence.pdf` (ou `kldivergence2.pdf`)  
- Résumé : Introduction claire à la KL et à son lien avec la vraisemblance moyenne.  
- Intérêt pour le projet : Justifie l’usage de D_KL / log-loss pour la calibration/validation.  
- BibTeX : `shlens2014kl`

### Franke & Degen (2023) – _The Softmax Function: Properties, Motivation, and Interpretation_
- Type : Article (tutoriel)  
- Fichier : `softmax-tutorial.pdf`  
- Résumé : Propriétés de la softmax, justification maximum entropy, interprétation du paramètre α/β.  
- Intérêt pour le projet : Base théorique pour l’usage de la softmax comme modèle de choix et pour le calibrage contextuel de β.  
- À lire en priorité : Sections 2–4 (propriétés, effet de β) ; 6 (interprétation/calibration) ; 7–9 (exploration/exploitation)  
- BibTeX : `franke2023softmax`

### McKelvey & Palfrey (1995) – _Quantal Response Equilibria for Normal Form Games_
- Type : Article (game theory)  
- Fichier : `Quantal Response Equilibria for Normal Form Games.pdf`  
- Résumé : Introduit les QRE, modèles de choix bruités avec paramètre de rationalité λ/β.  
- Intérêt pour le projet : Fondement théorique pour calibrer β ; transition de Nash vers QRE.  
- À cibler : Intro + Sec. 1–2 (QRE, λ/β) ; méthodologie de calibration (MLE/KL)  
- BibTeX : `mckelvey1995qre`

### Camerer, Ho & Chong (2004) – _A Cognitive Hierarchy Model of Games_
- Type : Article (game theory/behavioral)  
- Fichier : `cognitive_hierrarchy_model_of_games.pdf`  
- Résumé : Modèle de hiérarchie cognitive (τ = profondeur de réflexion).  
- Intérêt pour le projet : Distinguer τ (profondeur) de β (rationalité/“piqûre”), utiles pour interpréter la variabilité contextuelle.  
- BibTeX : `camerer2004ch`

---

## Références complémentaires (psychologie & décision)
- Gigerenzer, G. & Selten, R. (2001). _Bounded Rationality_. MIT Press.  
- Kahneman, D. & Tversky, A. (1979). _Prospect Theory: An Analysis of Decision under Risk_.  
- Simon, H. A. (1957). _Models of Man: Social and Rational_.

---

## À lire prochainement
- _Efficient Precision-Adjustable Architecture for Softmax Function_ (fichier présent).  
- Travaux sur la “decision-aware” KL / divergences adaptées à la décision.  
- Articles récents sur la calibration probabiliste du comportement humain.
