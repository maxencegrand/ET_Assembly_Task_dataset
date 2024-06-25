from tools import loadLog
import sys
import matplotlib.pyplot as plt
import numpy as np
import pyexcel_ods3


def main(argument):
    print("Le nom du fichier fourni est:", argument)


def showComparaisonAlgorithm(
    results, nb_results, linestyles, list_name, method, action, random_min, random_max
):
    plt.close()
    fig, ax = plt.subplots(1, 2)

    for ind in [0, 1]:

        ax[ind].plot(
            np.arange(-3000, 3001, 25),
            100 * results[ind][0][::25] / nb_results[ind][::25],
            linestyle=linestyles[0],
            label=list_name[0],
        )
        ax[ind].plot(
            np.arange(-3000, 3001, 25),
            100 * results[ind][1][::25] / nb_results[ind][::25],
            linestyle=linestyles[1],
            label=list_name[1],
        )
        ax[ind].plot(
            np.arange(-3000, 3001, 25),
            100 * results[ind][2][::25] / nb_results[ind][::25],
            linestyle=linestyles[2],
            label=list_name[2],
        )
        ax[ind].plot(
            np.arange(-3000, 3001, 25),
            100 * results[ind][3][::25] / nb_results[ind][::25],
            linestyle=linestyles[3],
            label=list_name[3],
        )
        ax[ind].plot(
            np.arange(-3000, 3001, 25),
            100 * results[ind][4][::25] / nb_results[ind][::25],
            linestyle=linestyles[4],
            label=list_name[4],
        )

        indice = FindX(results[ind][2] / nb_results[ind])
        if indice >= 0:
            ax[ind].vlines(
                x=indice - 3000,
                ymin=0,
                ymax=100,
                label="50%",
                linestyle=linestyles[2],
                color="g",
            )
            ax[ind].set_xticks(list(ax[ind].get_xticks()) + [indice - 3000])

        ax[ind].set_title(method[ind], fontsize=24)

    ax[0].hlines(y=50, xmin=-3000, xmax=3000, label="50%", color="r")
    ax[1].hlines(y=50, xmin=-3000, xmax=3000, label="50%", color="r")

    ax[0].axhspan(
        ymin=random_min,
        ymax=random_max,
        xmin=-3000,
        xmax=3000,
        label="random",
        color="gray",
    )
    ax[1].axhspan(
        ymin=random_min,
        ymax=random_max,
        xmin=-3000,
        xmax=3000,
        label="random",
        color="gray",
    )

    box = ax[0].get_position()
    ax[0].set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

    box = ax[1].get_position()
    ax[1].set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

    # Put a legend below current axis
    ax[0].legend(
        loc="upper center",
        bbox_to_anchor=(1.1, -0.05),
        fancybox=True,
        shadow=True,
        ncol=6,
        fontsize=20,
    )

    ax[0].axis(xmin=-3000, xmax=3000, ymin=0, ymax=100)
    ax[1].axis(xmin=-3000, xmax=3000, ymin=0, ymax=100)

    ax[0].set_xlabel("Time (ms)", fontsize=22)
    ax[0].set_ylabel("Percentage of good prediction", fontsize=22)

    ax[1].set_xlabel("Time (ms)", fontsize=22)
    ax[1].set_ylabel("Percentage of good prediction", fontsize=22)

    fig.suptitle(action, fontsize=30)

    plt.show()


def FindX(array):
    for i in range(array.shape[0]):
        if array[i] >= 0.5:
            return i
    return -1


if __name__ == "__main__":
    # Vérifier si un argument a été fourni
    if len(sys.argv) != 2:
        print("Utilisation: python3 plot_graph.py <path>")
    else:
        nb_predi = 5
        # Appel de la fonction main avec l'argument fourni
        nom_fichier = sys.argv[1]
        main(nom_fichier)

        results, nb_prediction, duree_execution = loadLog(nom_fichier)

        results = results.reshape(28, 2, nb_predi, 6001)
        nb_prediction = nb_prediction.reshape(28, 2, 6001)

        area4_grasp_weak = results[0]
        area4_release_weak = results[4]
        area4_grasp_strong = results[8]
        area4_release_strong = results[12]

        area8_grasp_weak = results[1]
        area8_release_weak = results[5]
        area8_grasp_strong = results[9]
        area8_release_strong = results[13]

        sliding_area4_grasp_weak = results[2]
        sliding_area4_release_weak = results[6]
        sliding_area4_grasp_strong = results[10]
        sliding_area4_release_strong = results[14]

        sliding_area8_grasp_weak = results[3]
        sliding_area8_release_weak = results[7]
        sliding_area8_grasp_strong = results[11]
        sliding_area8_release_strong = results[15]

        semantic_grasp_0 = results[16]
        semantic_grasp_1 = results[17]
        semantic_grasp_1b = results[19]
        semantic_grasp_2 = results[18]

        semantic_release_0 = results[20]
        semantic_release_1 = results[21]
        semantic_release_1b = results[23]
        semantic_release_2 = results[22]

        block_grasp = results[24]
        block_release = results[25]

        norme_grasp = results[26]
        norme_release = results[27]

        nb_area4_grasp_weak = nb_prediction[0]
        nb_area4_release_weak = nb_prediction[4]
        nb_area4_grasp_strong = nb_prediction[8]
        nb_area4_release_strong = nb_prediction[12]

        nb_area8_grasp_weak = nb_prediction[1]
        nb_area8_release_weak = nb_prediction[5]
        nb_area8_grasp_strong = nb_prediction[9]
        nb_area8_release_strong = nb_prediction[13]

        nb_sliding_area4_grasp_weak = nb_prediction[2]
        nb_sliding_area4_release_weak = nb_prediction[6]
        nb_sliding_area4_grasp_strong = nb_prediction[10]
        nb_sliding_area4_release_strong = nb_prediction[14]

        nb_sliding_area8_grasp_weak = nb_prediction[3]
        nb_sliding_area8_release_weak = nb_prediction[7]
        nb_sliding_area8_grasp_strong = nb_prediction[11]
        nb_sliding_area8_release_strong = nb_prediction[15]

        nb_semantic_grasp_0 = nb_prediction[16]
        nb_semantic_grasp_1 = nb_prediction[17]
        nb_semantic_grasp_1b = nb_prediction[19]
        nb_semantic_grasp_2 = nb_prediction[18]

        nb_semantic_release_0 = nb_prediction[20]
        nb_semantic_release_1 = nb_prediction[21]
        nb_semantic_release_1b = nb_prediction[23]
        nb_semantic_release_2 = nb_prediction[22]

        nb_block_grasp = nb_prediction[24]
        nb_block_release = nb_prediction[25]

        nb_norme_grasp = nb_prediction[26]
        nb_norme_release = nb_prediction[27]

        print(norme_grasp.max() + norme_release.max())
        print(nb_norme_grasp.max() + nb_norme_release.max())

        print(block_grasp.shape, nb_sliding_area4_grasp_weak.shape)
        for cam in range(0):
            for f in range(5):
                print("Feature", f + 1)
                print(
                    "t-3",
                    block_grasp[cam][f][0] / nb_block_grasp[cam][0],
                    "t-2",
                    block_grasp[cam][f][1000] / nb_block_grasp[cam][1000],
                    "t-1",
                    block_grasp[cam][f][2000] / nb_block_grasp[cam][2000],
                    "t-0.5",
                    block_grasp[cam][f][2500] / nb_block_grasp[cam][2500],
                    "t",
                    block_grasp[cam][f][3000] / nb_block_grasp[cam][3000],
                )
                print(
                    "t-3",
                    block_release[cam][f][0] / nb_block_release[cam][0],
                    "t-2",
                    block_release[cam][f][1000] / nb_block_release[cam][1000],
                    "t-1",
                    block_release[cam][f][2000] / nb_block_release[cam][2000],
                    "t-0.5",
                    block_release[cam][f][2500] / nb_block_release[cam][2500],
                    "t",
                    block_release[cam][f][3000] / nb_block_release[cam][3000],
                )
                print(
                    "t-3",
                    semantic_grasp_0[cam][f][0] / nb_semantic_grasp_0[cam][0],
                    "t-2",
                    semantic_grasp_0[cam][f][1000] / nb_semantic_grasp_0[cam][1000],
                    "t-1",
                    semantic_grasp_0[cam][f][2000] / nb_semantic_grasp_0[cam][2000],
                    "t-0.5",
                    semantic_grasp_0[cam][f][2500] / nb_semantic_grasp_0[cam][2500],
                    "t",
                    semantic_grasp_0[cam][f][3000] / nb_semantic_grasp_0[cam][3000],
                )
                print(
                    "t-3",
                    semantic_grasp_1[cam][f][0] / nb_semantic_grasp_1[cam][0],
                    "t-2",
                    semantic_grasp_1[cam][f][1000] / nb_semantic_grasp_1[cam][1000],
                    "t-1",
                    semantic_grasp_1[cam][f][2000] / nb_semantic_grasp_1[cam][2000],
                    "t-0.5",
                    semantic_grasp_1[cam][f][2500] / nb_semantic_grasp_1[cam][2500],
                    "t",
                    semantic_grasp_1[cam][f][3000] / nb_semantic_grasp_1[cam][3000],
                )
                print(
                    "t-3",
                    semantic_grasp_1b[cam][f][0] / nb_semantic_grasp_1b[cam][0],
                    "t-2",
                    semantic_grasp_1b[cam][f][1000] / nb_semantic_grasp_1b[cam][1000],
                    "t-1",
                    semantic_grasp_1b[cam][f][2000] / nb_semantic_grasp_1b[cam][2000],
                    "t-0.5",
                    semantic_grasp_1b[cam][f][2500] / nb_semantic_grasp_1b[cam][2500],
                    "t",
                    semantic_grasp_1b[cam][f][3000] / nb_semantic_grasp_1b[cam][3000],
                )
                print(
                    "t-3",
                    semantic_grasp_2[cam][f][0] / nb_semantic_grasp_2[cam][0],
                    "t-2",
                    semantic_grasp_2[cam][f][1000] / nb_semantic_grasp_2[cam][1000],
                    "t-1",
                    semantic_grasp_2[cam][f][2000] / nb_semantic_grasp_2[cam][2000],
                    "t-0.5",
                    semantic_grasp_2[cam][f][2500] / nb_semantic_grasp_2[cam][2500],
                    "t",
                    semantic_grasp_2[cam][f][3000] / nb_semantic_grasp_2[cam][3000],
                )
                print(
                    "t-3",
                    semantic_release_0[cam][f][0] / nb_semantic_release_0[cam][0],
                    "t-2",
                    semantic_release_0[cam][f][1000] / nb_semantic_release_0[cam][1000],
                    "t-1",
                    semantic_release_0[cam][f][2000] / nb_semantic_release_0[cam][2000],
                    "t-0.5",
                    semantic_release_0[cam][f][2500] / nb_semantic_release_0[cam][2500],
                    "t",
                    semantic_release_0[cam][f][3000] / nb_semantic_release_0[cam][3000],
                )
                print(
                    "t-3",
                    semantic_release_1[cam][f][0] / nb_semantic_release_1[cam][0],
                    "t-2",
                    semantic_release_1[cam][f][1000] / nb_semantic_release_1[cam][1000],
                    "t-1",
                    semantic_release_1[cam][f][2000] / nb_semantic_release_1[cam][2000],
                    "t-0.5",
                    semantic_release_1[cam][f][2500] / nb_semantic_release_1[cam][2500],
                    "t",
                    semantic_release_1[cam][f][3000] / nb_semantic_release_1[cam][3000],
                )
                print(
                    "t-3",
                    semantic_release_1b[cam][f][0] / nb_semantic_release_1b[cam][0],
                    "t-2",
                    semantic_release_1b[cam][f][1000]
                    / nb_semantic_release_1b[cam][1000],
                    "t-1",
                    semantic_release_1b[cam][f][2000]
                    / nb_semantic_release_1b[cam][2000],
                    "t-0.5",
                    semantic_release_1b[cam][f][2500]
                    / nb_semantic_release_1b[cam][2500],
                    "t",
                    semantic_release_1b[cam][f][3000]
                    / nb_semantic_release_1b[cam][3000],
                )
                print(
                    "t-3",
                    semantic_release_2[cam][f][0] / nb_semantic_release_2[cam][0],
                    "t-2",
                    semantic_release_2[cam][f][1000] / nb_semantic_release_2[cam][1000],
                    "t-1",
                    semantic_release_2[cam][f][2000] / nb_semantic_release_2[cam][2000],
                    "t-0.5",
                    semantic_release_2[cam][f][2500] / nb_semantic_release_2[cam][2500],
                    "t",
                    semantic_release_2[cam][f][3000] / nb_semantic_release_2[cam][3000],
                )
                print(
                    "t-3",
                    area4_grasp_weak[cam][f][0] / nb_area4_grasp_weak[cam][0],
                    "t-2",
                    area4_grasp_weak[cam][f][1000] / nb_area4_grasp_weak[cam][1000],
                    "t-1",
                    area4_grasp_weak[cam][f][2000] / nb_area4_grasp_weak[cam][2000],
                    "t-0.5",
                    area4_grasp_weak[cam][f][2500] / nb_area4_grasp_weak[cam][2500],
                    "t",
                    area4_grasp_weak[cam][f][3000] / nb_area4_grasp_weak[cam][3000],
                )
                print(
                    "t-3",
                    area4_grasp_strong[cam][f][0] / nb_area4_grasp_strong[cam][0],
                    "t-2",
                    area4_grasp_strong[cam][f][1000] / nb_area4_grasp_strong[cam][1000],
                    "t-1",
                    area4_grasp_strong[cam][f][2000] / nb_area4_grasp_strong[cam][2000],
                    "t-0.5",
                    area4_grasp_strong[cam][f][2500] / nb_area4_grasp_strong[cam][2500],
                    "t",
                    area4_grasp_strong[cam][f][3000] / nb_area4_grasp_strong[cam][3000],
                )
                print(
                    "t-3",
                    sliding_area4_grasp_weak[cam][f][0]
                    / nb_sliding_area4_grasp_weak[cam][0],
                    "t-2",
                    sliding_area4_grasp_weak[cam][f][1000]
                    / nb_sliding_area4_grasp_weak[cam][1000],
                    "t-1",
                    sliding_area4_grasp_weak[cam][f][2000]
                    / nb_sliding_area4_grasp_weak[cam][2000],
                    "t-0.5",
                    sliding_area4_grasp_weak[cam][f][2500]
                    / nb_sliding_area4_grasp_weak[cam][2500],
                    "t",
                    sliding_area4_grasp_weak[cam][f][3000]
                    / nb_sliding_area4_grasp_weak[cam][3000],
                )
                print(
                    "t-3",
                    sliding_area4_grasp_strong[cam][f][0]
                    / nb_sliding_area4_grasp_strong[cam][0],
                    "t-2",
                    sliding_area4_grasp_strong[cam][f][1000]
                    / nb_sliding_area4_grasp_strong[cam][1000],
                    "t-1",
                    sliding_area4_grasp_strong[cam][f][2000]
                    / nb_sliding_area4_grasp_strong[cam][2000],
                    "t-0.5",
                    sliding_area4_grasp_strong[cam][f][2500]
                    / nb_sliding_area4_grasp_strong[cam][2500],
                    "t",
                    sliding_area4_grasp_strong[cam][f][3000]
                    / nb_sliding_area4_grasp_strong[cam][3000],
                )
                print(
                    "t-3",
                    area8_grasp_weak[cam][f][0] / nb_area8_grasp_weak[cam][0],
                    "t-2",
                    area8_grasp_weak[cam][f][1000] / nb_area8_grasp_weak[cam][1000],
                    "t-1",
                    area8_grasp_weak[cam][f][2000] / nb_area8_grasp_weak[cam][2000],
                    "t-0.5",
                    area8_grasp_weak[cam][f][2500] / nb_area8_grasp_weak[cam][2500],
                    "t",
                    area8_grasp_weak[cam][f][3000] / nb_area8_grasp_weak[cam][3000],
                )
                print(
                    "t-3",
                    area8_grasp_strong[cam][f][0] / nb_area8_grasp_strong[cam][0],
                    "t-2",
                    area8_grasp_strong[cam][f][1000] / nb_area8_grasp_strong[cam][1000],
                    "t-1",
                    area8_grasp_strong[cam][f][2000] / nb_area8_grasp_strong[cam][2000],
                    "t-0.5",
                    area8_grasp_strong[cam][f][2500] / nb_area8_grasp_strong[cam][2500],
                    "t",
                    area8_grasp_strong[cam][f][3000] / nb_area8_grasp_strong[cam][3000],
                )
                print(
                    "t-3",
                    sliding_area8_grasp_weak[cam][f][0]
                    / nb_sliding_area8_grasp_weak[cam][0],
                    "t-2",
                    sliding_area8_grasp_weak[cam][f][1000]
                    / nb_sliding_area8_grasp_weak[cam][1000],
                    "t-1",
                    sliding_area8_grasp_weak[cam][f][2000]
                    / nb_sliding_area8_grasp_weak[cam][2000],
                    "t-0.5",
                    sliding_area8_grasp_weak[cam][f][2500]
                    / nb_sliding_area8_grasp_weak[cam][2500],
                    "t",
                    sliding_area8_grasp_weak[cam][f][3000]
                    / nb_sliding_area8_grasp_weak[cam][3000],
                )
                print(
                    "t-3",
                    sliding_area8_grasp_strong[cam][f][0]
                    / nb_sliding_area8_grasp_strong[cam][0],
                    "t-2",
                    sliding_area8_grasp_strong[cam][f][1000]
                    / nb_sliding_area8_grasp_strong[cam][1000],
                    "t-1",
                    sliding_area8_grasp_strong[cam][f][2000]
                    / nb_sliding_area8_grasp_strong[cam][2000],
                    "t-0.5",
                    sliding_area8_grasp_strong[cam][f][2500]
                    / nb_sliding_area8_grasp_strong[cam][2500],
                    "t",
                    sliding_area8_grasp_strong[cam][f][3000]
                    / nb_sliding_area8_grasp_strong[cam][3000],
                )
                print(
                    "t-3",
                    area4_release_weak[cam][f][0] / nb_area4_release_weak[cam][0],
                    "t-2",
                    area4_release_weak[cam][f][1000] / nb_area4_release_weak[cam][1000],
                    "t-1",
                    area4_release_weak[cam][f][2000] / nb_area4_release_weak[cam][2000],
                    "t-0.5",
                    area4_release_weak[cam][f][2500] / nb_area4_release_weak[cam][2500],
                    "t",
                    area4_release_weak[cam][f][3000] / nb_area4_release_weak[cam][3000],
                )
                print(
                    "t-3",
                    area4_release_strong[cam][f][0] / nb_area4_release_strong[cam][0],
                    "t-2",
                    area4_release_strong[cam][f][1000]
                    / nb_area4_release_strong[cam][1000],
                    "t-1",
                    area4_release_strong[cam][f][2000]
                    / nb_area4_release_strong[cam][2000],
                    "t-0.5",
                    area4_release_strong[cam][f][2500]
                    / nb_area4_release_strong[cam][2500],
                    "t",
                    area4_release_strong[cam][f][3000]
                    / nb_area4_release_strong[cam][3000],
                )
                print(
                    "t-3",
                    sliding_area4_release_weak[cam][f][0]
                    / nb_sliding_area4_release_weak[cam][0],
                    "t-2",
                    sliding_area4_release_weak[cam][f][1000]
                    / nb_sliding_area4_release_weak[cam][1000],
                    "t-1",
                    sliding_area4_release_weak[cam][f][2000]
                    / nb_sliding_area4_release_weak[cam][2000],
                    "t-0.5",
                    sliding_area4_release_weak[cam][f][2500]
                    / nb_sliding_area4_release_weak[cam][2500],
                    "t",
                    sliding_area4_release_weak[cam][f][3000]
                    / nb_sliding_area4_release_weak[cam][3000],
                )
                print(
                    "t-3",
                    sliding_area4_release_strong[cam][f][0]
                    / nb_sliding_area4_release_strong[cam][0],
                    "t-2",
                    sliding_area4_release_strong[cam][f][1000]
                    / nb_sliding_area4_release_strong[cam][1000],
                    "t-1",
                    sliding_area4_release_strong[cam][f][2000]
                    / nb_sliding_area4_release_strong[cam][2000],
                    "t-0.5",
                    sliding_area4_release_strong[cam][f][2500]
                    / nb_sliding_area4_release_strong[cam][2500],
                    "t",
                    sliding_area4_release_strong[cam][f][3000]
                    / nb_sliding_area4_release_strong[cam][3000],
                )
                print(
                    "t-3",
                    area8_release_weak[cam][f][0] / nb_area8_release_weak[cam][0],
                    "t-2",
                    area8_release_weak[cam][f][1000] / nb_area8_release_weak[cam][1000],
                    "t-1",
                    area8_release_weak[cam][f][2000] / nb_area8_release_weak[cam][2000],
                    "t-0.5",
                    area8_release_weak[cam][f][2500] / nb_area8_release_weak[cam][2500],
                    "t",
                    area8_release_weak[cam][f][3000] / nb_area8_release_weak[cam][3000],
                )
                print(
                    "t-3",
                    area8_release_strong[cam][f][0] / nb_area8_release_strong[cam][0],
                    "t-2",
                    area8_release_strong[cam][f][1000]
                    / nb_area8_release_strong[cam][1000],
                    "t-1",
                    area8_release_strong[cam][f][2000]
                    / nb_area8_release_strong[cam][2000],
                    "t-0.5",
                    area8_release_strong[cam][f][2500]
                    / nb_area8_release_strong[cam][2500],
                    "t",
                    area8_release_strong[cam][f][3000]
                    / nb_area8_release_strong[cam][3000],
                )
                print(
                    "t-3",
                    sliding_area8_release_weak[cam][f][0]
                    / nb_sliding_area8_release_weak[cam][0],
                    "t-2",
                    sliding_area8_release_weak[cam][f][1000]
                    / nb_sliding_area8_release_weak[cam][1000],
                    "t-1",
                    sliding_area8_release_weak[cam][f][2000]
                    / nb_sliding_area8_release_weak[cam][2000],
                    "t-0.5",
                    sliding_area8_release_weak[cam][f][2500]
                    / nb_sliding_area8_release_weak[cam][2500],
                    "t",
                    sliding_area8_release_weak[cam][f][3000]
                    / nb_sliding_area8_release_weak[cam][3000],
                )
                print(
                    "t-3",
                    sliding_area8_release_strong[cam][f][0]
                    / nb_sliding_area8_release_strong[cam][0],
                    "t-2",
                    sliding_area8_release_strong[cam][f][1000]
                    / nb_sliding_area8_release_strong[cam][1000],
                    "t-1",
                    sliding_area8_release_strong[cam][f][2000]
                    / nb_sliding_area8_release_strong[cam][2000],
                    "t-0.5",
                    sliding_area8_release_strong[cam][f][2500]
                    / nb_sliding_area8_release_strong[cam][2500],
                    "t",
                    sliding_area8_release_strong[cam][f][3000]
                    / nb_sliding_area8_release_strong[cam][3000],
                )
                input()

        data = []

        for cam in range(2):
            for f in range(5):
                sheet_name = f"Cam{cam+1}_Feature{f+1}"  # Nom de la feuille

                # Créer une liste pour les données de la feuille actuelle
                sheet_data = []

                # Ajouter les valeurs à la liste des données de la feuille actuelle
                sheet_data.append(
                    ["Header1", "Header2", "Header3", "Header4", "Header5"]
                )  # En-tête des colonnes

                data.append(
                    [
                        area4_grasp_strong[cam][f][0] / nb_area4_grasp_strong[cam][0],
                        area4_grasp_strong[cam][f][1000]
                        / nb_area4_grasp_strong[cam][1000],
                        area4_grasp_strong[cam][f][2000]
                        / nb_area4_grasp_strong[cam][2000],
                        area4_grasp_strong[cam][f][2500]
                        / nb_area4_grasp_strong[cam][2500],
                        area4_grasp_strong[cam][f][3000]
                        / nb_area4_grasp_strong[cam][3000],
                    ]
                )

                data.append(
                    [
                        area4_grasp_weak[cam][f][0] / nb_area4_grasp_weak[cam][0],
                        area4_grasp_weak[cam][f][1000] / nb_area4_grasp_weak[cam][1000],
                        area4_grasp_weak[cam][f][2000] / nb_area4_grasp_weak[cam][2000],
                        area4_grasp_weak[cam][f][2500] / nb_area4_grasp_weak[cam][2500],
                        area4_grasp_weak[cam][f][3000] / nb_area4_grasp_weak[cam][3000],
                    ]
                )

                data.append(
                    [
                        area8_grasp_strong[cam][f][0] / nb_area8_grasp_strong[cam][0],
                        area8_grasp_strong[cam][f][1000]
                        / nb_area8_grasp_strong[cam][1000],
                        area8_grasp_strong[cam][f][2000]
                        / nb_area8_grasp_strong[cam][2000],
                        area8_grasp_strong[cam][f][2500]
                        / nb_area8_grasp_strong[cam][2500],
                        area8_grasp_strong[cam][f][3000]
                        / nb_area8_grasp_strong[cam][3000],
                    ]
                )

                data.append(
                    [
                        area8_grasp_weak[cam][f][0] / nb_area8_grasp_weak[cam][0],
                        area8_grasp_weak[cam][f][1000] / nb_area8_grasp_weak[cam][1000],
                        area8_grasp_weak[cam][f][2000] / nb_area8_grasp_weak[cam][2000],
                        area8_grasp_weak[cam][f][2500] / nb_area8_grasp_weak[cam][2500],
                        area8_grasp_weak[cam][f][3000] / nb_area8_grasp_weak[cam][3000],
                    ]
                )

                data.append(
                    [
                        sliding_area4_grasp_strong[cam][f][0]
                        / nb_sliding_area4_grasp_strong[cam][0],
                        sliding_area4_grasp_strong[cam][f][1000]
                        / nb_sliding_area4_grasp_strong[cam][1000],
                        sliding_area4_grasp_strong[cam][f][2000]
                        / nb_sliding_area4_grasp_strong[cam][2000],
                        sliding_area4_grasp_strong[cam][f][2500]
                        / nb_sliding_area4_grasp_strong[cam][2500],
                        sliding_area4_grasp_strong[cam][f][3000]
                        / nb_sliding_area4_grasp_strong[cam][3000],
                    ]
                )

                data.append(
                    [
                        sliding_area4_grasp_weak[cam][f][0]
                        / nb_sliding_area4_grasp_weak[cam][0],
                        sliding_area4_grasp_weak[cam][f][1000]
                        / nb_sliding_area4_grasp_weak[cam][1000],
                        sliding_area4_grasp_weak[cam][f][2000]
                        / nb_sliding_area4_grasp_weak[cam][2000],
                        sliding_area4_grasp_weak[cam][f][2500]
                        / nb_sliding_area4_grasp_weak[cam][2500],
                        sliding_area4_grasp_weak[cam][f][3000]
                        / nb_sliding_area4_grasp_weak[cam][3000],
                    ]
                )

                data.append(
                    [
                        sliding_area8_grasp_strong[cam][f][0]
                        / nb_sliding_area8_grasp_strong[cam][0],
                        sliding_area8_grasp_strong[cam][f][1000]
                        / nb_sliding_area8_grasp_strong[cam][1000],
                        sliding_area8_grasp_strong[cam][f][2000]
                        / nb_sliding_area8_grasp_strong[cam][2000],
                        sliding_area8_grasp_strong[cam][f][2500]
                        / nb_sliding_area8_grasp_strong[cam][2500],
                        sliding_area8_grasp_strong[cam][f][3000]
                        / nb_sliding_area8_grasp_strong[cam][3000],
                    ]
                )

                data.append(
                    [
                        sliding_area8_grasp_weak[cam][f][0]
                        / nb_sliding_area8_grasp_weak[cam][0],
                        sliding_area8_grasp_weak[cam][f][1000]
                        / nb_sliding_area8_grasp_weak[cam][1000],
                        sliding_area8_grasp_weak[cam][f][2000]
                        / nb_sliding_area8_grasp_weak[cam][2000],
                        sliding_area8_grasp_weak[cam][f][2500]
                        / nb_sliding_area8_grasp_weak[cam][2500],
                        sliding_area8_grasp_weak[cam][f][3000]
                        / nb_sliding_area8_grasp_weak[cam][3000],
                    ]
                )

                data.append(
                    [
                        semantic_grasp_0[cam][f][0] / nb_semantic_grasp_0[cam][0],
                        semantic_grasp_0[cam][f][1000] / nb_semantic_grasp_0[cam][1000],
                        semantic_grasp_0[cam][f][2000] / nb_semantic_grasp_0[cam][2000],
                        semantic_grasp_0[cam][f][2500] / nb_semantic_grasp_0[cam][2500],
                        semantic_grasp_0[cam][f][3000] / nb_semantic_grasp_0[cam][3000],
                    ]
                )

                data.append(
                    [
                        semantic_grasp_1[cam][f][0] / nb_semantic_grasp_1[cam][0],
                        semantic_grasp_1[cam][f][1000] / nb_semantic_grasp_1[cam][1000],
                        semantic_grasp_1[cam][f][2000] / nb_semantic_grasp_1[cam][2000],
                        semantic_grasp_1[cam][f][2500] / nb_semantic_grasp_1[cam][2500],
                        semantic_grasp_1[cam][f][3000] / nb_semantic_grasp_1[cam][3000],
                    ]
                )

                data.append(
                    [
                        semantic_grasp_1b[cam][f][0] / nb_semantic_grasp_1b[cam][0],
                        semantic_grasp_1b[cam][f][1000]
                        / nb_semantic_grasp_1b[cam][1000],
                        semantic_grasp_1b[cam][f][2000]
                        / nb_semantic_grasp_1b[cam][2000],
                        semantic_grasp_1b[cam][f][2500]
                        / nb_semantic_grasp_1b[cam][2500],
                        semantic_grasp_1b[cam][f][3000]
                        / nb_semantic_grasp_1b[cam][3000],
                    ]
                )

                data.append(
                    [
                        semantic_grasp_2[cam][f][0] / nb_semantic_grasp_2[cam][0],
                        semantic_grasp_2[cam][f][1000] / nb_semantic_grasp_2[cam][1000],
                        semantic_grasp_2[cam][f][2000] / nb_semantic_grasp_2[cam][2000],
                        semantic_grasp_2[cam][f][2500] / nb_semantic_grasp_2[cam][2500],
                        semantic_grasp_2[cam][f][3000] / nb_semantic_grasp_2[cam][3000],
                    ]
                )

                data.append(
                    [
                        block_grasp[cam][f][0] / nb_block_grasp[cam][0],
                        block_grasp[cam][f][1000] / nb_block_grasp[cam][1000],
                        block_grasp[cam][f][2000] / nb_block_grasp[cam][2000],
                        block_grasp[cam][f][2500] / nb_block_grasp[cam][2500],
                        block_grasp[cam][f][3000] / nb_block_grasp[cam][3000],
                    ]
                )

                """release"""

                data.append(
                    [
                        area4_release_strong[cam][f][0]
                        / nb_area4_release_strong[cam][0],
                        area4_release_strong[cam][f][1000]
                        / nb_area4_release_strong[cam][1000],
                        area4_release_strong[cam][f][2000]
                        / nb_area4_release_strong[cam][2000],
                        area4_release_strong[cam][f][2500]
                        / nb_area4_release_strong[cam][2500],
                        area4_release_strong[cam][f][3000]
                        / nb_area4_release_strong[cam][3000],
                    ]
                )

                data.append(
                    [
                        area4_release_weak[cam][f][0] / nb_area4_release_weak[cam][0],
                        area4_release_weak[cam][f][1000]
                        / nb_area4_release_weak[cam][1000],
                        area4_release_weak[cam][f][2000]
                        / nb_area4_release_weak[cam][2000],
                        area4_release_weak[cam][f][2500]
                        / nb_area4_release_weak[cam][2500],
                        area4_release_weak[cam][f][3000]
                        / nb_area4_release_weak[cam][3000],
                    ]
                )

                data.append(
                    [
                        area8_release_strong[cam][f][0]
                        / nb_area8_release_strong[cam][0],
                        area8_release_strong[cam][f][1000]
                        / nb_area8_release_strong[cam][1000],
                        area8_release_strong[cam][f][2000]
                        / nb_area8_release_strong[cam][2000],
                        area8_release_strong[cam][f][2500]
                        / nb_area8_release_strong[cam][2500],
                        area8_release_strong[cam][f][3000]
                        / nb_area8_release_strong[cam][3000],
                    ]
                )

                data.append(
                    [
                        area8_release_weak[cam][f][0] / nb_area8_release_weak[cam][0],
                        area8_release_weak[cam][f][1000]
                        / nb_area8_release_weak[cam][1000],
                        area8_release_weak[cam][f][2000]
                        / nb_area8_release_weak[cam][2000],
                        area8_release_weak[cam][f][2500]
                        / nb_area8_release_weak[cam][2500],
                        area8_release_weak[cam][f][3000]
                        / nb_area8_release_weak[cam][3000],
                    ]
                )

                data.append(
                    [
                        sliding_area4_release_strong[cam][f][0]
                        / nb_sliding_area4_release_strong[cam][0],
                        sliding_area4_release_strong[cam][f][1000]
                        / nb_sliding_area4_release_strong[cam][1000],
                        sliding_area4_release_strong[cam][f][2000]
                        / nb_sliding_area4_release_strong[cam][2000],
                        sliding_area4_release_strong[cam][f][2500]
                        / nb_sliding_area4_release_strong[cam][2500],
                        sliding_area4_release_strong[cam][f][3000]
                        / nb_sliding_area4_release_strong[cam][3000],
                    ]
                )

                data.append(
                    [
                        sliding_area4_release_weak[cam][f][0]
                        / nb_sliding_area4_release_weak[cam][0],
                        sliding_area4_release_weak[cam][f][1000]
                        / nb_sliding_area4_release_weak[cam][1000],
                        sliding_area4_release_weak[cam][f][2000]
                        / nb_sliding_area4_release_weak[cam][2000],
                        sliding_area4_release_weak[cam][f][2500]
                        / nb_sliding_area4_release_weak[cam][2500],
                        sliding_area4_release_weak[cam][f][3000]
                        / nb_sliding_area4_release_weak[cam][3000],
                    ]
                )

                data.append(
                    [
                        sliding_area8_release_strong[cam][f][0]
                        / nb_sliding_area8_release_strong[cam][0],
                        sliding_area8_release_strong[cam][f][1000]
                        / nb_sliding_area8_release_strong[cam][1000],
                        sliding_area8_release_strong[cam][f][2000]
                        / nb_sliding_area8_release_strong[cam][2000],
                        sliding_area8_release_strong[cam][f][2500]
                        / nb_sliding_area8_release_strong[cam][2500],
                        sliding_area8_release_strong[cam][f][3000]
                        / nb_sliding_area8_release_strong[cam][3000],
                    ]
                )

                data.append(
                    [
                        sliding_area8_release_weak[cam][f][0]
                        / nb_sliding_area8_release_weak[cam][0],
                        sliding_area8_release_weak[cam][f][1000]
                        / nb_sliding_area8_release_weak[cam][1000],
                        sliding_area8_release_weak[cam][f][2000]
                        / nb_sliding_area8_release_weak[cam][2000],
                        sliding_area8_release_weak[cam][f][2500]
                        / nb_sliding_area8_release_weak[cam][2500],
                        sliding_area8_release_weak[cam][f][3000]
                        / nb_sliding_area8_release_weak[cam][3000],
                    ]
                )

                data.append(
                    [
                        semantic_release_0[cam][f][0] / nb_semantic_release_0[cam][0],
                        semantic_release_0[cam][f][1000]
                        / nb_semantic_release_0[cam][1000],
                        semantic_release_0[cam][f][2000]
                        / nb_semantic_release_0[cam][2000],
                        semantic_release_0[cam][f][2500]
                        / nb_semantic_release_0[cam][2500],
                        semantic_release_0[cam][f][3000]
                        / nb_semantic_release_0[cam][3000],
                    ]
                )

                data.append(
                    [
                        semantic_release_1[cam][f][0] / nb_semantic_release_1[cam][0],
                        semantic_release_1[cam][f][1000]
                        / nb_semantic_release_1[cam][1000],
                        semantic_release_1[cam][f][2000]
                        / nb_semantic_release_1[cam][2000],
                        semantic_release_1[cam][f][2500]
                        / nb_semantic_release_1[cam][2500],
                        semantic_release_1[cam][f][3000]
                        / nb_semantic_release_1[cam][3000],
                    ]
                )

                data.append(
                    [
                        semantic_release_1b[cam][f][0] / nb_semantic_release_1b[cam][0],
                        semantic_release_1b[cam][f][1000]
                        / nb_semantic_release_1b[cam][1000],
                        semantic_release_1b[cam][f][2000]
                        / nb_semantic_release_1b[cam][2000],
                        semantic_release_1b[cam][f][2500]
                        / nb_semantic_release_1b[cam][2500],
                        semantic_release_1b[cam][f][3000]
                        / nb_semantic_release_1b[cam][3000],
                    ]
                )

                data.append(
                    [
                        semantic_release_2[cam][f][0] / nb_semantic_release_2[cam][0],
                        semantic_release_2[cam][f][1000]
                        / nb_semantic_release_2[cam][1000],
                        semantic_release_2[cam][f][2000]
                        / nb_semantic_release_2[cam][2000],
                        semantic_release_2[cam][f][2500]
                        / nb_semantic_release_2[cam][2500],
                        semantic_release_2[cam][f][3000]
                        / nb_semantic_release_2[cam][3000],
                    ]
                )

                data.append(
                    [
                        block_release[cam][f][0] / nb_block_release[cam][0],
                        block_release[cam][f][1000] / nb_block_release[cam][1000],
                        block_release[cam][f][2000] / nb_block_release[cam][2000],
                        block_release[cam][f][2500] / nb_block_release[cam][2500],
                        block_release[cam][f][3000] / nb_block_release[cam][3000],
                    ]
                )

                data.append([-2, -2, -2, -2, -2])

                # Répétez pour chaque ensemble de données

                # Ajouter la liste des données de la feuille actuelle à la liste des données générales
                # data.append((sheet_name, sheet_data))

        # Spécifier le chemin du fichier de sortie
        output_file = "output_Model.ods"

        nb_chiffres_significatifs = 1

        liste_de_listes_en_string = [
            [
                format(100 * float(nombre), ".{}f".format(nb_chiffres_significatifs))
                for nombre in liste
            ]
            for liste in data
        ]

        # Écrire les données dans le fichier ODS
        pyexcel_ods3.save_data(output_file, {"Feuille 1": liste_de_listes_en_string})

        linestyles = ["-", "--", "-.", ":", (0, (3, 2, 1, 2, 1, 2))]

        showComparaisonAlgorithm(
            block_grasp,
            nb_block_grasp,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions for Grasp",
            100 / 24,
            100 / 24,
        )
        showComparaisonAlgorithm(
            block_release,
            nb_block_release,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Reference Block during Release",
            100 / 24,
            100 / 24,
        )

        showComparaisonAlgorithm(
            norme_grasp,
            nb_norme_grasp,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Norme for Grasp",
            0,
            0,
        )
        showComparaisonAlgorithm(
            norme_release,
            nb_norme_release,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Norme for Release",
            0,
            0,
        )

        showComparaisonAlgorithm(
            semantic_grasp_0,
            nb_semantic_grasp_0,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions for Semantic Grasp 0",
            100 / 1,
            100 / 1,
        )
        showComparaisonAlgorithm(
            semantic_grasp_1,
            nb_semantic_grasp_1,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions for Semantic Grasp 1",
            100 / 3,
            100 / 3,
        )
        showComparaisonAlgorithm(
            semantic_grasp_1b,
            nb_semantic_grasp_1b,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions for Semantic Grasp 1 bis",
            100 / 2,
            100 / 2,
        )
        showComparaisonAlgorithm(
            semantic_grasp_2,
            nb_semantic_grasp_2,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions for Semantic Grasp 2",
            100 / 5,
            100 / 5,
        )

        showComparaisonAlgorithm(
            semantic_release_0,
            nb_semantic_release_0,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions for Semantic Release 0",
            100 / 1,
            100 / 1,
        )
        showComparaisonAlgorithm(
            semantic_release_1,
            nb_semantic_release_1,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions for Semantic Release 1",
            100 / 3,
            100 / 3,
        )
        showComparaisonAlgorithm(
            semantic_release_1b,
            nb_semantic_release_1b,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions for Semantic Release 1 bis",
            100 / 2,
            100 / 2,
        )
        showComparaisonAlgorithm(
            semantic_release_2,
            nb_semantic_release_2,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions for Semantic Release 2",
            100 / 5,
            100 / 5,
        )

        showComparaisonAlgorithm(
            area4_grasp_weak,
            nb_area4_grasp_weak,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Grasp Area, Fixe Area 4x4 Weak",
            100 / 72,
            4 * 100 / 72,
        )
        showComparaisonAlgorithm(
            area4_grasp_strong,
            nb_area4_grasp_strong,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Grasp Area, Fixe Area 4x4 Strong",
            0,
            100 / 72,
        )
        showComparaisonAlgorithm(
            sliding_area4_grasp_weak,
            nb_sliding_area4_grasp_weak,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Grasp Area, Overlapping Area 4x4 Weak",
            25 * 100 / 945,
            35 * 100 / 945,
        )
        showComparaisonAlgorithm(
            sliding_area4_grasp_strong,
            nb_sliding_area4_grasp_strong,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Grasp Area, Overlapping Area 4x4 Strong",
            3 * 100 / 945,
            9 * 100 / 945,
        )

        showComparaisonAlgorithm(
            area8_grasp_weak,
            nb_area8_grasp_weak,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Grasp Area, Fixe Area 8x8 Weak",
            100 / 18,
            4 * 100 / 18,
        )
        showComparaisonAlgorithm(
            area8_grasp_strong,
            nb_area8_grasp_strong,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Grasp Area, Fixe Area 8x8 Strong",
            0,
            100 / 18,
        )
        showComparaisonAlgorithm(
            sliding_area8_grasp_weak,
            nb_sliding_area8_grasp_weak,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Grasp Area, Overlapping Area 8x8 Weak",
            81 * 100 / 697,
            99 * 100 / 697,
        )
        showComparaisonAlgorithm(
            sliding_area8_grasp_strong,
            nb_sliding_area8_grasp_strong,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Grasp Area, Overlapping Area 8x8 Strong",
            35 * 100 / 697,
            49 * 100 / 697,
        )

        showComparaisonAlgorithm(
            area4_release_weak,
            nb_area4_release_weak,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Release Area, Fixe Area 4x4 Weak",
            100 / 72,
            4 * 100 / 72,
        )
        showComparaisonAlgorithm(
            area4_release_strong,
            nb_area4_release_strong,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Release Area, Fixe Area 4x4 Strong",
            0,
            100 / 72,
        )
        showComparaisonAlgorithm(
            sliding_area4_release_weak,
            nb_sliding_area4_release_weak,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Release Area, Overlapping Area 4x4 Weak",
            25 * 100 / 945,
            35 * 100 / 945,
        )
        showComparaisonAlgorithm(
            sliding_area4_release_strong,
            nb_sliding_area4_release_strong,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Release Area, Overlapping Area 4x4 Strong",
            3 * 100 / 945,
            9 * 100 / 945,
        )

        showComparaisonAlgorithm(
            area8_release_weak,
            nb_area8_release_weak,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Release Area, Fixe Area 8x8 Weak",
            100 / 18,
            4 * 100 / 18,
        )
        showComparaisonAlgorithm(
            area8_release_strong,
            nb_area8_release_strong,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Release Area, Fixe Area 8x8 Strong",
            0,
            100 / 18,
        )
        showComparaisonAlgorithm(
            sliding_area8_release_weak,
            nb_sliding_area8_release_weak,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Release Area, Overlapping Area 8x8 Weak",
            81 * 100 / 697,
            99 * 100 / 697,
        )
        showComparaisonAlgorithm(
            sliding_area8_release_strong,
            nb_sliding_area8_release_strong,
            linestyles,
            [
                "OT_Count",
                "OT_Distance",
                "AT_Linear_Dist",
                "AT_Inverse_Dist",
                "AT_Fitts",
            ],
            ["Mobile", "Stationnary"],
            "Comparison between the different predictions to find Release Area, Overlapping Area 8x8 Strong",
            35 * 100 / 697,
            49 * 100 / 697,
        )
