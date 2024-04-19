
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os


import numpy as np

# Créer un tableau NumPy à enregistrer
data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Spécifier le chemin du fichier CSV
nom_fichier = "donnees.csv"

# Enregistrer le tableau NumPy dans un fichier CSV
np.savetxt(nom_fichier, data, delimiter=',')
