from tools import loadLog
import sys
import matplotlib.pyplot as plt
import numpy as np
def main(argument):
    print("Le nom du fichier fourni est:", argument)

def showComparaisonAlgorithm(results, nb_results, linestyles,list_name,method,action,random_min,random_max):
        plt.close()
        fig, ax = plt.subplots(1, 2)

        for ind in [0,1]:

            ax[ind].plot(np.arange(-3000,3001,25),100*results[ind][0][::25]/nb_results[ind][::25], linestyle = linestyles[0] , label = list_name[0])
            ax[ind].plot(np.arange(-3000,3001,25),100*results[ind][1][::25]/nb_results[ind][::25], linestyle = linestyles[1] , label = list_name[1])
            ax[ind].plot(np.arange(-3000,3001,25),100*results[ind][2][::25]/nb_results[ind][::25], linestyle = linestyles[2] , label = list_name[2])
            ax[ind].plot(np.arange(-3000,3001,25),100*results[ind][3][::25]/nb_results[ind][::25], linestyle = linestyles[3] , label = list_name[3])
            ax[ind].plot(np.arange(-3000,3001,25),100*results[ind][4][::25]/nb_results[ind][::25], linestyle = linestyles[4] , label = list_name[4])

            ax[ind].set_title(method[ind],fontsize = 24)
        
        ax[0].hlines(y=50,xmin=-3000,xmax=3000,label = "50%", color = "r")
        ax[1].hlines(y=50,xmin=-3000,xmax=3000,label = "50%", color = "r")

        ax[0].axhspan(ymin=random_min, ymax=random_max, xmin=-3000, xmax=3000,label = "random", color = "gray")
        ax[1].axhspan(ymin=random_min, ymax=random_max, xmin=-3000, xmax=3000,label = "random", color = "gray")

        box = ax[0].get_position()
        ax[0].set_position([box.x0, box.y0 + box.height * 0.1,
                        box.width, box.height * 0.9])
        
        box = ax[1].get_position()
        ax[1].set_position([box.x0, box.y0 + box.height * 0.1,
                        box.width, box.height * 0.9])

        # Put a legend below current axis
        ax[0].legend(loc='upper center', bbox_to_anchor=(1.1, -0.05),
                fancybox=True, shadow=True, ncol=6, fontsize = 20) 

        ax[0].axis(xmin=-3000, xmax=3000, ymin=0, ymax=100)
        ax[1].axis(xmin=-3000, xmax=3000, ymin=0, ymax=100)
        
        ax[0].set_xlabel('Time (ms)', fontsize = 22) 
        ax[0].set_ylabel('Percentage of good prediction', fontsize = 22) 

        ax[1].set_xlabel('Time (ms)', fontsize = 22) 
        ax[1].set_ylabel('Percentage of good prediction', fontsize = 22) 

        
        fig.suptitle(action,fontsize = 30)


        plt.show()

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

        results = results.reshape(26,2,nb_predi,6001)
        nb_prediction = nb_prediction.reshape(26,2,6001)


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
        semantic_grasp_1b = results[18]
        semantic_grasp_2 = results[19]

        semantic_release_0 = results[20]
        semantic_release_1 = results[21]
        semantic_release_1b = results[22]
        semantic_release_2 = results[23]

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
        nb_semantic_grasp_1b = nb_prediction[18]
        nb_semantic_grasp_2 = nb_prediction[19]

        nb_semantic_release_0 = nb_prediction[20]
        nb_semantic_release_1 = nb_prediction[21]
        nb_semantic_release_1b = nb_prediction[22]
        nb_semantic_release_2 = nb_prediction[23]

        nb_block_grasp = nb_prediction[24]
        nb_block_release = nb_prediction[25]

        nb_norme_grasp = nb_prediction[26]
        nb_norme_release = nb_prediction[27]

        linestyles = ["-","--","-.",":",(0, (3, 2, 1, 2, 1, 2))]


        showComparaisonAlgorithm(block_grasp,nb_block_grasp,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions for Grasp",100/24,100/24)
        showComparaisonAlgorithm(block_release,nb_block_release,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Reference Block during Release",100/24,100/24)

        showComparaisonAlgorithm(norme_grasp,nb_norme_grasp,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Norme for Grasp",0,0)
        showComparaisonAlgorithm(norme_release,nb_norme_release,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Norme for Release",0,0)

        showComparaisonAlgorithm(semantic_grasp_0,nb_semantic_grasp_0,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions for Semantic Grasp 0",100/1,100/1)
        showComparaisonAlgorithm(semantic_grasp_1,nb_semantic_grasp_1,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions for Semantic Grasp 1",100/3,100/3)
        showComparaisonAlgorithm(semantic_grasp_1b,nb_semantic_grasp_1b,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions for Semantic Grasp 1",100/3,100/3)
        showComparaisonAlgorithm(semantic_grasp_2,nb_semantic_grasp_2,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions for Semantic Grasp 2",100/5,100/5)
        
        showComparaisonAlgorithm(semantic_release_0,nb_semantic_release_0,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions for Semantic Release 0",100/1,100/1)
        showComparaisonAlgorithm(semantic_release_1,nb_semantic_release_1,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions for Semantic Release 1",100/3,100/3)
        showComparaisonAlgorithm(semantic_release_1b,nb_semantic_release_1b,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions for Semantic Release 1",100/3,100/3)
        showComparaisonAlgorithm(semantic_release_2,nb_semantic_release_2,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions for Semantic Release 2",100/5,100/5)
        
        
        showComparaisonAlgorithm(area4_grasp_weak,nb_area4_grasp_weak,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Grasp Area, Fixe Area 4x4 Weak",100/72,4*100/72)
        showComparaisonAlgorithm(area4_grasp_strong,nb_area4_grasp_strong,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Grasp Area, Fixe Area 4x4 Strong",0,100/72)
        showComparaisonAlgorithm(sliding_area4_grasp_weak,nb_sliding_area4_grasp_weak,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Grasp Area, Overlapping Area 4x4 Weak",25*100/945,35*100/945)
        showComparaisonAlgorithm(sliding_area4_grasp_strong,nb_sliding_area4_grasp_strong,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Grasp Area, Overlapping Area 4x4 Strong",3*100/945,9*100/945)

        showComparaisonAlgorithm(area8_grasp_weak,nb_area8_grasp_weak,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Grasp Area, Fixe Area 8x8 Weak",100/18,4*100/18)
        showComparaisonAlgorithm(area8_grasp_strong,nb_area8_grasp_strong,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Grasp Area, Fixe Area 8x8 Strong",0,100/18)
        showComparaisonAlgorithm(sliding_area8_grasp_weak,nb_sliding_area8_grasp_weak,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Grasp Area, Overlapping Area 8x8 Weak",81*100/697,99*100/697)
        showComparaisonAlgorithm(sliding_area8_grasp_strong,nb_sliding_area8_grasp_strong,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Grasp Area, Overlapping Area 8x8 Strong",35*100/697,49*100/697)


        showComparaisonAlgorithm(area4_release_weak,nb_area4_release_weak,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, Fixe Area 4x4 Weak",100/72,4*100/72)
        showComparaisonAlgorithm(area4_release_strong,nb_area4_release_strong,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, Fixe Area 4x4 Strong",0,100/72)
        showComparaisonAlgorithm(sliding_area4_release_weak,nb_sliding_area4_release_weak,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, Overlapping Area 4x4 Weak",25*100/945,35*100/945)
        showComparaisonAlgorithm(sliding_area4_release_strong,nb_sliding_area4_release_strong,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, Overlapping Area 4x4 Strong",3*100/945,9*100/945)

        showComparaisonAlgorithm(area8_release_weak,nb_area8_release_weak,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, Fixe Area 8x8 Weak",100/18,4*100/18)
        showComparaisonAlgorithm(area8_release_strong,nb_area8_release_strong,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, Fixe Area 8x8 Strong",0,100/18)
        showComparaisonAlgorithm(sliding_area8_release_weak,nb_sliding_area8_release_weak,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, Overlapping Area 8x8 Weak",81*100/697,99*100/697)
        showComparaisonAlgorithm(sliding_area8_release_strong,nb_sliding_area8_release_strong,linestyles,["OT_Count","OT_Distance","AT_Linear_Dist","AT_Inverse_Dist","AT_Fitts"],["Mobile","Stationnary"],"Comparison between the different predictions to find Release Area, Overlapping Area 8x8 Strong",35*100/697,49*100/697)
