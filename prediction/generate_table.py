from tools import loadLog
import sys
import numpy as np

if __name__ == "__main__":
    # Vérifier si un argument a été fourni
    if len(sys.argv) != 3:
        print("Utilisation: python3 plot_graph.py <path>")
    else:
        nb_predi = 5
        # Appel de la fonction main avec l'argument fourni
        nom_fichier = sys.argv[1]
        ML_nom_fichier = sys.argv[2]
        
        print("Le nom du fichier fourni est:", nom_fichier)

        results,nb_prediction,duree_execution = loadLog(nom_fichier)

        results = results.reshape(28,2,nb_predi,6001)
        nb_prediction = nb_prediction.reshape(28,2,6001)


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

        ML_results,ML_nb_prediction,ML_duree_execution = loadLog(ML_nom_fichier)

        print("Le nom du fichier fourni est:", ML_nom_fichier)

        ML_results = ML_results.reshape(28,2,nb_predi,6001)
        ML_nb_prediction = ML_nb_prediction.reshape(28,2,6001)


        ML_area4_grasp_weak = ML_results[0]
        ML_area4_release_weak = ML_results[4]
        ML_area4_grasp_strong = ML_results[8]
        ML_area4_release_strong = ML_results[12]

        ML_area8_grasp_weak = ML_results[1]
        ML_area8_release_weak = ML_results[5]
        ML_area8_grasp_strong = ML_results[9]
        ML_area8_release_strong = ML_results[13]

        ML_sliding_area4_grasp_weak = ML_results[2]
        ML_sliding_area4_release_weak = ML_results[6]
        ML_sliding_area4_grasp_strong = ML_results[10]
        ML_sliding_area4_release_strong = ML_results[14]

        ML_sliding_area8_grasp_weak = ML_results[3]
        ML_sliding_area8_release_weak = ML_results[7]
        ML_sliding_area8_grasp_strong = ML_results[11]
        ML_sliding_area8_release_strong = ML_results[15]

        ML_semantic_grasp_0 = ML_results[16]
        ML_semantic_grasp_1 = ML_results[17]
        ML_semantic_grasp_1b = ML_results[19]
        ML_semantic_grasp_2 = ML_results[18]

        ML_semantic_release_0 = ML_results[20]
        ML_semantic_release_1 = ML_results[21]
        ML_semantic_release_1b = ML_results[23]
        ML_semantic_release_2 = ML_results[22]

        ML_block_grasp = ML_results[24]
        ML_block_release = ML_results[25]

        ML_norme_grasp = ML_results[26]
        ML_norme_release = ML_results[27]


        ML_nb_area4_grasp_weak = ML_nb_prediction[0]
        ML_nb_area4_release_weak = ML_nb_prediction[4]
        ML_nb_area4_grasp_strong = ML_nb_prediction[8]
        ML_nb_area4_release_strong = ML_nb_prediction[12]

        ML_nb_area8_grasp_weak = ML_nb_prediction[1]
        ML_nb_area8_release_weak = ML_nb_prediction[5]
        ML_nb_area8_grasp_strong = ML_nb_prediction[9]
        ML_nb_area8_release_strong = ML_nb_prediction[13]

        ML_nb_sliding_area4_grasp_weak = ML_nb_prediction[2]
        ML_nb_sliding_area4_release_weak = ML_nb_prediction[6]
        ML_nb_sliding_area4_grasp_strong = ML_nb_prediction[10]
        ML_nb_sliding_area4_release_strong = ML_nb_prediction[14]

        ML_nb_sliding_area8_grasp_weak = ML_nb_prediction[3]
        ML_nb_sliding_area8_release_weak = ML_nb_prediction[7]
        ML_nb_sliding_area8_grasp_strong = ML_nb_prediction[11]
        ML_nb_sliding_area8_release_strong = ML_nb_prediction[15]

        ML_nb_semantic_grasp_0 = ML_nb_prediction[16]
        ML_nb_semantic_grasp_1 = ML_nb_prediction[17]
        ML_nb_semantic_grasp_1b = ML_nb_prediction[19]
        ML_nb_semantic_grasp_2 = ML_nb_prediction[18]

        ML_nb_semantic_release_0 = ML_nb_prediction[20]
        ML_nb_semantic_release_1 = ML_nb_prediction[21]
        ML_nb_semantic_release_1b = ML_nb_prediction[23]
        ML_nb_semantic_release_2 = ML_nb_prediction[22]

        ML_nb_block_grasp = ML_nb_prediction[24]
        ML_nb_block_release = ML_nb_prediction[25]

        ML_nb_norme_grasp = ML_nb_prediction[26]
        ML_nb_norme_release = ML_nb_prediction[27]


        liste_feature = ["OT\\_Count","OT\\_Distance","AT\\_Linear\\_Dist","AT\\_Inverse\\_Dist","AT\\_Fitts"]
        liste_zone = ["\\multirow{5}{*}{Régulières Contiguë 4}",
                      "\\multirow{5}{*}{Régulières Contiguë 8}",
                      "\\multirow{5}{*}{Régulières Chevauchante 4}",
                      "\\multirow{5}{*}{Régulières Chevauchante 8}",
                      "\\multirow{5}{*}{Sémantique level 0}",
                      "\\multirow{5}{*}{Sémantique level 1}",
                      "\\multirow{5}{*}{Sémantique level 2}",
                      "\\multirow{5}{*}{Sémantique level 3}",
                      "\\multirow{5}{*}{Sémantique level 4 (Bloc)}"]

        with open("mon_tableau_grasp.tex", "w") as fichier:
            fichier.write("\\begin{table}[htbp]\n")
            fichier.write("\\centering\n")
            fichier.write("\\resizebox{0.7\\textheight}{!}{\n")
            fichier.write("\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|}\n")
            fichier.write("\\hline\n")
            fichier.write("Surface & Feature & \\multicolumn{5}{c|}{\\textbf{Modele}} & \\multicolumn{5}{c|}{\\textbf{Machine Learning}}\\\\\n")
            fichier.write("\\hline\n")
            fichier.write("& & t-3 & t-2 & t-1 & t-0.5 & t & t-3 & t-2 & t-1 & t-0.5 & t\\\\\n")
            fichier.write("\\hline\n")
            for indice_zone,zone_predi in enumerate([[[area4_grasp_strong,nb_area4_grasp_strong],[ML_area4_grasp_strong,ML_nb_area4_grasp_strong]],
                               [[area8_grasp_strong,nb_area8_grasp_strong],[ML_area8_grasp_strong,ML_nb_area8_grasp_strong]],
                               [[sliding_area4_grasp_strong,nb_sliding_area4_grasp_strong],[ML_sliding_area4_grasp_strong,ML_nb_sliding_area4_grasp_strong]],
                               [[sliding_area8_grasp_strong,nb_sliding_area8_grasp_strong],[ML_sliding_area8_grasp_strong,ML_nb_sliding_area8_grasp_strong]],
                               [[semantic_grasp_0,nb_semantic_grasp_0],[ML_semantic_grasp_0,ML_nb_semantic_grasp_0]],
                               [[semantic_grasp_1b,nb_semantic_grasp_1b],[ML_semantic_grasp_1b,ML_nb_semantic_grasp_1b]],
                               [[semantic_grasp_1,nb_semantic_grasp_1],[ML_semantic_grasp_1,ML_nb_semantic_grasp_1]],
                               [[semantic_grasp_2,nb_semantic_grasp_2],[ML_semantic_grasp_2,ML_nb_semantic_grasp_2]],
                               [[block_grasp,nb_block_grasp],[ML_block_grasp,ML_nb_block_grasp]]]):
                fichier.write(liste_zone[indice_zone])
                for f in range(5):
                    fichier.write(" & " + liste_feature[f])
                    for nb_good_zone_predi,nb_zone_predi in zone_predi:
                        for timestamp in [0,1000,2000,2500,3000]:
                            fichier.write(" & " + "{:.1f}".format(100*nb_good_zone_predi[0][f][timestamp]/nb_zone_predi[0][timestamp]))
                    fichier.write("\\\\ \n")
                fichier.write("\\hline\n")
            fichier.write("\\end{tabular}\n")
            fichier.write("}\n")
            fichier.write("\\end{table}\n")

        with open("mon_tableau_release.tex", "w") as fichier:
            fichier.write("\\begin{table}[htbp]\n")
            fichier.write("\\centering\n")
            fichier.write("\\resizebox{0.7\\textheight}{!}{\n")
            fichier.write("\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|}\n")
            fichier.write("\\hline\n")
            fichier.write("Surface & Feature & \\multicolumn{5}{c|}{\\textbf{Modele}} & \\multicolumn{5}{c|}{\\textbf{Machine Learning}}\\\\\n")
            fichier.write("\\hline\n")
            fichier.write("& & t-3 & t-2 & t-1 & t-0.5 & t & t-3 & t-2 & t-1 & t-0.5 & t\\\\\n")
            fichier.write("\\hline\n")
            for indice_zone,zone_predi in enumerate([[[area4_release_strong,nb_area4_release_strong],[ML_area4_release_strong,ML_nb_area4_release_strong]],
                                                    [[area8_release_strong,nb_area8_release_strong],[ML_area8_release_strong,ML_nb_area8_release_strong]],
                                                    [[sliding_area4_release_strong,nb_sliding_area4_release_strong],[ML_sliding_area4_release_strong,ML_nb_sliding_area4_release_strong]],
                                                    [[sliding_area8_release_strong,nb_sliding_area8_release_strong],[ML_sliding_area8_release_strong,ML_nb_sliding_area8_release_strong]],
                                                    [[semantic_release_0,nb_semantic_release_0],[ML_semantic_release_0,ML_nb_semantic_release_0]],
                                                    [[semantic_release_1b,nb_semantic_release_1b],[ML_semantic_release_1b,ML_nb_semantic_release_1b]],
                                                    [[semantic_release_1,nb_semantic_release_1],[ML_semantic_release_1,ML_nb_semantic_release_1]],
                                                    [[semantic_release_2,nb_semantic_release_2],[ML_semantic_release_2,ML_nb_semantic_release_2]],
                                                    [[block_release,nb_block_release],[ML_block_release,ML_nb_block_release]]]):
                fichier.write(liste_zone[indice_zone])
                for f in range(5):
                    fichier.write(" & " + liste_feature[f])
                    for nb_good_zone_predi,nb_zone_predi in zone_predi:
                        for timestamp in [0,1000,2000,2500,3000]:
                            fichier.write(" & " + "{:.1f}".format(100*nb_good_zone_predi[0][f][timestamp]/nb_zone_predi[0][timestamp]))
                    fichier.write("\\\\ \n")
                fichier.write("\\hline\n")
            fichier.write("\\end{tabular}\n")
            fichier.write("}\n")
            fichier.write("\\end{table}\n")