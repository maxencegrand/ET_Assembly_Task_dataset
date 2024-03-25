from tools import loadLog,showComparaisonAlgorithm
import sys

def main(argument):
    print("Le nom du fichier fourni est:", argument)

if __name__ == "__main__":
    # Vérifier si un argument a été fourni
    if len(sys.argv) != 2:
        print("Utilisation: python plot_graph.py <path>")
    else:
        # Appel de la fonction main avec l'argument fourni
        nom_fichier = sys.argv[1]
        main(nom_fichier)

        liste_area1, liste_area2, liste_area4, liste_area8, liste_area_best, liste_grasp, liste_release, total_nb_grasp ,duree, features = loadLog(nom_fichier)

        print(total_nb_grasp)

        linestyles = ["-","--","-.",":",(0, (3, 2, 1, 2, 1, 2))]

        showComparaisonAlgorithm(liste_grasp,total_nb_grasp,linestyles,["Score1","Score2","Score3","Score4","Score5"],["Mobile","Stationnary"],"Comparison between the different predictions for Grasp")
        showComparaisonAlgorithm(liste_release,total_nb_grasp,linestyles,["Score1","Score2","Score3","Score4","Score5"],["Mobile","Stationnary"],"Comparison between the different predictions to find reference block during Release")

        showComparaisonAlgorithm(liste_area1,total_nb_grasp,linestyles,["Score1","Score2","Score3","Score4","Score5"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, with size 1x1")
        showComparaisonAlgorithm(liste_area2,total_nb_grasp,linestyles,["Score1","Score2","Score3","Score4","Score5"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, with size 2x2")
        showComparaisonAlgorithm(liste_area4,total_nb_grasp,linestyles,["Score1","Score2","Score3","Score4","Score5"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, with size 4x4")
        showComparaisonAlgorithm(liste_area8,total_nb_grasp,linestyles,["Score1","Score2","Score3","Score4","Score5"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, with size 8x8")

        showComparaisonAlgorithm(liste_area_best,total_nb_grasp,linestyles,["Score1","Score2","Score3","Score4","Score5"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, with size 8x8")
