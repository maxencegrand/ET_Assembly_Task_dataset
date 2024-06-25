from tools import loadLog
import sys
import numpy as np

if __name__ == "__main__":
    # Vérifier si un argument a été fourni
    if len(sys.argv) != 2:
        print("Utilisation: python3 plot_graph.py <log_path>")
    else:
        nb_predi = 5
        # Appel de la fonction main avec l'argument fourni
        nom_fichier = sys.argv[1]

        print("Le nom du fichier fourni est:", nom_fichier)

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

        linestyles = ["-", "--", "-.", ":", (0, (3, 2, 1, 2, 1, 2))]

        color = ["blue", "orange", "green", "red", "purple"]
        style = [" dashed", "dotted", "densely dotted", "densely dashed", "dash dot"]

        with open("mon_graphe.tex", "w") as fichier:
            # Commencer l'écriture
            fichier.write("\\documentclass{article}\n")
            fichier.write("\\usepackage{tikz}\n")
            fichier.write("\\usepackage{subcaption}\n")
            fichier.write("\\usetikzlibrary{matrix}\n")
            fichier.write("\\begin{document}\n")
            fichier.write("\\begin{figure}[htbp]\n")
            fichier.write("\\centering\n")

            for ind in range(2):
                fichier.write("\\begin{subfigure}{0.45\\textwidth}\n")
                fichier.write("\\centering\n")
                fichier.write("\\begin{tikzpicture}[scale=1.5]\n")
                fichier.write("% Axes\n")

                fichier.write("\\draw[->] (-3,3.9) -- (0,3.9) node[right] {$t$};\n")
                fichier.write("\\draw[->] (-3,3.9) -- (-3,6);\n")

                fichier.write("\\draw (-3,3.7) node {$-3$};\n")
                fichier.write("\\draw (0,3.7) node {$0$};\n")

                fichier.write("\\draw (-3.2,3.9) node {$1.3$};\n")
                fichier.write("\\draw (-3.2,6) node {$2$};\n")

                fichier.write("\\draw (-3,6.2) node {$score$};\n")

                fichier.write("% Lignes\n")

                for i in range(0, 3000, 25):
                    for f in range(5):
                        pass
                        fichier.write(
                            "\\draw["
                            + str(color[f])
                            + ", "
                            + str(style[f])
                            + "] ("
                            + str((i - 3000) / 1000)
                            + ","
                            + str((norme_grasp[ind][f][i] / nb_norme_grasp[ind][i]) * 3)
                            + ") -- ("
                            + str((i + 25 - 3000) / 1000)
                            + ","
                            + str(
                                (
                                    norme_grasp[ind][f][i + 25]
                                    / nb_norme_grasp[ind][i + 25]
                                )
                                * 3
                            )
                            + ");\n"
                        )

                fichier.write("\\end{tikzpicture}\n")
                fichier.write("\\caption{Courbes de différentes couleurs et formes.}\n")
                fichier.write("\\end{subfigure}\n")

            for ind in range(2):
                fichier.write("\\begin{subfigure}{0.45\\textwidth}\n")
                fichier.write("\\centering\n")
                fichier.write("\\begin{tikzpicture}[scale=1.5]\n")
                fichier.write("% Axes\n")

                fichier.write("\\draw[->] (-3,3.9) -- (0,3.9) node[right] {$t$};\n")
                fichier.write("\\draw[->] (-3,3.9) -- (-3,6);\n")

                fichier.write("\\draw (-3,3.7) node {$-3$};\n")
                fichier.write("\\draw (0,3.7) node {$0$};\n")

                fichier.write("\\draw (-3.2,3.9) node {$1.3$};\n")
                fichier.write("\\draw (-3.2,6) node {$2$};\n")

                fichier.write("\\draw (-3,6.2) node {$score$};\n")

                fichier.write("% Lignes\n")

                for i in range(0, 3000, 25):
                    for f in range(5):
                        pass
                        fichier.write(
                            "\\draw["
                            + str(color[f])
                            + ", "
                            + str(style[f])
                            + "] ("
                            + str((i - 3000) / 1000)
                            + ","
                            + str(
                                (norme_release[ind][f][i] / nb_norme_release[ind][i])
                                * 3
                            )
                            + ") -- ("
                            + str((i + 25 - 3000) / 1000)
                            + ","
                            + str(
                                (
                                    norme_release[ind][f][i + 25]
                                    / nb_norme_release[ind][i + 25]
                                )
                                * 3
                            )
                            + ");\n"
                        )

                fichier.write("\\end{tikzpicture}\n")
                fichier.write("\\caption{Courbes de différentes couleurs et formes.}\n")
                fichier.write("\\end{subfigure}\n")

            fichier.write(
                "\\caption{Graphiques avec courbes de différentes couleurs et formes.}\n"
            )
            fichier.write("\\end{figure}\n")
            fichier.write("\\end{document}\n")

        print("Le fichier mon_graphe.tex a été créé avec succès !")
