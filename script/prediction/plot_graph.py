from tools import loadLog,showComparaisonAlgorithm
import sys

def main(argument):
    print("Le nom du fichier fourni est:", argument)

if __name__ == "__main__":
    # Vérifier si un argument a été fourni
    if len(sys.argv) != 2:
        print("Utilisation: python plot_graph.py <path>")
    else:
        nb_predi = 5
        # Appel de la fonction main avec l'argument fourni
        nom_fichier = sys.argv[1]
        main(nom_fichier)

        results,nb_prediction,duree_execution = loadLog(nom_fichier)

        results = results.reshape(12,2,nb_predi,6001)
        nb_prediction = nb_prediction.reshape(12,2,6001)


        area1_grasp = results[0]
        area1_release = results[4]
        area2_grasp = results[1]
        area2_release = results[5]
        area4_grasp = results[2]
        area4_release = results[6]
        area8_grasp = results[3]
        area8_release = results[7]
        sliding_area_grasp = results[8]
        sliding_area_release = results[9]
        block_grasp = results[10]
        block_release = results[11]

        nb_area1_grasp = nb_prediction[0]
        nb_area1_release = nb_prediction[4]
        nb_area2_grasp = nb_prediction[1]
        nb_area2_release = nb_prediction[5]
        nb_area4_grasp = nb_prediction[2]
        nb_area4_release = nb_prediction[6]
        nb_area8_grasp = nb_prediction[3]
        nb_area8_release = nb_prediction[7]
        nb_sliding_area_grasp = nb_prediction[8]
        nb_sliding_area_release = nb_prediction[9]
        nb_block_grasp = nb_prediction[10]
        nb_block_release = nb_prediction[11]

        linestyles = ["-","--","-.",":",(0, (3, 2, 1, 2, 1, 2))]

        showComparaisonAlgorithm(block_grasp,nb_block_grasp,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions for Grasp")
        showComparaisonAlgorithm(block_release,nb_block_release,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Reference Block during Release")

        showComparaisonAlgorithm(area1_grasp,nb_area1_grasp,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Grasp Area, with size 1x1")
        showComparaisonAlgorithm(area2_grasp,nb_area2_grasp,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Grasp Area, with size 2x2")
        showComparaisonAlgorithm(area4_grasp,nb_area4_grasp,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Grasp Area, with size 4x4")
        showComparaisonAlgorithm(area8_grasp,nb_area8_grasp,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Grasp Area, with size 8x8")

        showComparaisonAlgorithm(area1_release,nb_area1_release,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, with size 1x1")
        showComparaisonAlgorithm(area2_release,nb_area2_release,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, with size 2x2")
        showComparaisonAlgorithm(area4_release,nb_area4_release,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, with size 4x4")
        showComparaisonAlgorithm(area8_release,nb_area8_release,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, with size 8x8")

        showComparaisonAlgorithm(sliding_area_grasp,nb_sliding_area_grasp,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Grasp Sliding Area, with size 8x8")
        showComparaisonAlgorithm(sliding_area_release,nb_sliding_area_release,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Sliding Area, with size 8x8")
