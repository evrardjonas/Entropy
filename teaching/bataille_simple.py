import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.special import comb

# Fonction pour calculer l'entropie
def calculate_entropy(n1, n2, remaining_cards):
    if remaining_cards == 0 or n1 == 0 or n2 == 0:
        return 0  # Si l'un des joueurs a toutes les cartes, l'entropie est 0
    combinations = comb(remaining_cards, n1)
    entropy = math.log2(combinations)
    return entropy

# Fonction pour simuler une partie de Bataille
def simulate_battle():
    # Initialisation
    total_cards = 40
    player1_cards = total_cards // 2  # Chaque joueur commence avec 26 cartes
    player2_cards = total_cards // 2
    entropy_values = []
    rounds = 0

    # Calcul de l'entropie initiale
    initial_entropy = calculate_entropy(player1_cards, player2_cards, total_cards)
    entropy_values.append(initial_entropy)

    # Simulation des tours
    while player1_cards > 0 and player2_cards > 0:
        rounds += 1

        # Chaque joueur joue une carte
        if np.random.rand() > 0.5:
            # Joueur 1 gagne le tour
            player1_cards += 1
            player2_cards -= 1
        else:
            # Joueur 2 gagne le tour
            player1_cards -= 1
            player2_cards += 1

        remaining_cards = player1_cards + player2_cards

        # Calcul de l'entropie après chaque tour
        entropy = calculate_entropy(player1_cards, player2_cards, remaining_cards)
        entropy_values.append(entropy)

    return entropy_values, rounds

# Simulation et affichage des résultats
entropy_values, total_rounds = simulate_battle()

# Graphique de l'évolution de l'entropie
plt.figure(figsize=(10, 6))
plt.plot(range(len(entropy_values)), entropy_values, marker='o', label="Entropie")
plt.title("Évolution de l'entropie dans une partie de Bataille")
plt.xlabel("Numéro du tour")
plt.ylabel("Entropie (bits)")
plt.legend()
plt.grid()
plt.show()

print(f"Nombre total de tours joués : {total_rounds}")