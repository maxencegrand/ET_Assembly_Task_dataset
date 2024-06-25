import numpy as np


def liste_seed():
    # Définir la plage de valeurs pour les graines
    min_seed = 1
    max_seed = 10000

    np.random.seed(42)

    # Choisir 5 graines aléatoires
    num_seeds = 5
    selected_seeds = np.random.randint(min_seed, max_seed, size=num_seeds)

    return selected_seeds
