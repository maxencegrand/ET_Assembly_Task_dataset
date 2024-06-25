import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

os.environ["KERAS_BACKEND"] = "torch"
import keras


from seed import liste_seed


def distri(seed):
    # Obtention de la date et de l'heure actuelle
    date_heure_actuelle = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Nom du fichier avec la date et l'heure
    nom_fichier = f"logs/{date_heure_actuelle}"

    nb_predi = 5

    liste_participant_mobile = []
    liste_participant_sitting = []

    for method_pos, method in enumerate(["mobile", "stationnary"]):
        directory = "../dataset/" + method + "/sitting/"
        for entry in os.scandir(directory):
            if method == "mobile":
                liste_participant_mobile.append(entry.path)
            else:
                liste_participant_sitting.append(entry.path)

    print(liste_participant_mobile)

    left_mobile, right_mobile = keras.utils.split_dataset(
        np.array(liste_participant_mobile), left_size=0.8, seed=seed
    )
    left_mobile_numpy = list(left_mobile)
    right_mobile_numpy = list(right_mobile)

    left_sitting, right_sitting = keras.utils.split_dataset(
        np.array(liste_participant_sitting), left_size=0.8, seed=seed
    )
    left_sitting_numpy = list(left_sitting)
    right_sitting_numpy = list(right_sitting)

    left = [left_mobile_numpy, left_sitting_numpy]
    right = [right_mobile_numpy, right_sitting_numpy]

    liste_duree = []

    for method_pos, side in enumerate(left):
        nb_action = 0
        duree_max = 0
        """
        Premier passing pour trouver l'action la plus grande
        """
        for number in side:
            participant = number.numpy().decode("utf-8")
            for model in os.scandir(participant):
                # On vŕifie que le participant existe et est non problematique (bug dans dataset)
                if (
                    not (
                        participant.split("/")[-1] == "37931545"
                        and str(model.path).split("/")[-1] == "tsb"
                    )
                    and not (
                        participant.split("/")[-1] == "30587763"
                        and str(model.path).split("/")[-1] == "tsb"
                    )
                    and os.path.exists(str(model.path) + "/table.csv")
                    and os.path.exists(str(model.path) + "/states.csv")
                ):

                    # On charge les données
                    gaze_point = np.genfromtxt(model.path + "/table.csv", delimiter=",")

                    world = np.genfromtxt(model.path + "/states.csv", delimiter=",")

                    # Compte de taille nombre d'action
                    compte = np.zeros((world.shape[0] - 1))
                    nb_action += world.shape[0] - 2

                    t_init = gaze_point[1, 0]
                    indice = 0

                    # On mesure la longueur de chaque action
                    for t in range(1, gaze_point.shape[0]):

                        t_gaze = gaze_point[t, 0]

                        if (
                            indice < world.shape[0] - 2
                            and t_gaze >= world[indice + 2, 0]
                        ):
                            indice += 1

                        compte[indice] += 1

                    for u in range(compte.shape[0]):
                        liste_duree.append(compte[u])

                    # Si l'action est plus grande que duree_max, on actualise duree_max
                    if duree_max < compte.max():
                        duree_max = compte.max()
                        print("Max:", str(model.path))

        sorted_data = sorted(liste_duree)

        resultat = [element / (30 * (1 + method_pos)) * 1000 for element in sorted_data]
        sorted_data = resultat

        # Trouvez l'indice correspondant à 95% des valeurs
        good_index = int(0.95 * len(sorted_data))

        # Récupérez la valeur à cet indice
        good_size = int(sorted_data[good_index])

        print("indice 95%", good_size)

        binwidth = 100
        # Tracer l'histogramme
        plt.figure(figsize=(8, 6))
        sns.histplot(
            sorted_data,
            bins=range(int(0), int(max(sorted_data) + binwidth), binwidth),
            kde=True,
            color="skyblue",
        )

        plt.xlabel("Durée de l'action (ms)", fontsize=22)
        plt.ylabel("Nombre d'action", fontsize=22)
        plt.grid(True)
        # Définir les marques sur l'axe x à chaque multiple de 1000
        plt.xticks(range(0, int(max(sorted_data) + 1000), 1000))
        # Sauvegarder les limites actuelles de l'axe y
        ylim_before = plt.ylim()
        # Tracer les lignes verticales
        plt.vlines(x=good_size, ymin=0, ymax=ylim_before[1], label="95%", color="r")
        # Rétablir les limites de l'axe y
        plt.ylim(ylim_before)

        plt.xlim(0, 10000)

        plt.legend(loc="upper center", fancybox=True, shadow=True, ncol=1, fontsize=20)
        plt.tick_params(
            axis="x", labelsize=22
        )  # Taille de la police des ticks sur l'axe des x
        plt.tick_params(axis="y", labelsize=22)
        plt.show()

        # Calculer les statistiques descriptives
        moyenne = np.mean(sorted_data)
        median = np.median(sorted_data)
        ecart_type = np.std(sorted_data)

        print("Moyenne :", moyenne)
        print("Médiane :", median)
        print("Écart-type :", ecart_type)


seeds = liste_seed()
distri(seeds[0])
