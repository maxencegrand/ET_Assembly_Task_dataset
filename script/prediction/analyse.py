import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.widgets import Slider
import os

plot_1 = False
analyse = True
plot_analyse = False

largeur = 76
hauteur = 38
dist_min = -largeur/(2*48)

taille_zone = 1
nb_bloc_1 = int((48/1)*(24/1))
nb_bloc_2 = int((48/2)*(24/2))
nb_bloc_4 = int((48/4)*(24/4))
nb_bloc_8 = int((48/8)*(24/8))

array_zone1 = np.genfromtxt("../../data/ET_Assembly_Task_dataset/script/csv/zone_1x1.csv", delimiter=",")
array_zone2 = np.genfromtxt("../../data/ET_Assembly_Task_dataset/script/csv/zone_2x2.csv", delimiter=",")
array_zone4 = np.genfromtxt("../../data/ET_Assembly_Task_dataset/script/csv/zone_4x4.csv", delimiter=",")
array_zone8 = np.genfromtxt("../../data/ET_Assembly_Task_dataset/script/csv/zone_8x8.csv", delimiter=",")

from tools import listeHolding,listeRelease


def showComparaisonAlgorithm(liste_temps, total_nb_grasp,linestyles,list_name,method,action):
        plt.close()
        fig, ax = plt.subplots(1, 2)

        for ind in [0,1]:
            for u in range(len(liste_temps[ind])):
                l_y = []
                l_x = []
                if len(liste_temps[ind][u]) > 0:
                    for i in range(-3000, 25, 25):
                        q = np.array(liste_temps[ind][u])
                        qwerty = q[q <= i]
                        val = 100 * len(qwerty) / total_nb_grasp[ind]
                        l_y.append(val)
                        l_x.append(i)

                    for i in range(0, 3025, 25):

                        q = np.array(liste_temps[ind][u])
                        qwerty = q[q >= i]
                        val = 100 * len(qwerty) / total_nb_grasp[ind]
                        l_y.append(val)
                        l_x.append(i)

                else:
                    l = np.zeros((61))
                ax[ind].plot(l_x, l_y, linestyle = linestyles[u] , label = list_name[u])

            ax[ind].set_title(method[ind],fontsize = 24)
        
        ax[0].hlines(y=50,xmin=-3000,xmax=3000,label = "50%", color = "r")
        ax[1].hlines(y=50,xmin=-3000,xmax=3000,label = "50%", color = "r")

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

"""
analyseSituation does blah blah blah.

Input

method: str correspond a la methode actuellement analyse (mobile ou stationnary)
analyse_methode_good_grasp_prediction: int nombre de bonnes predictions lors des grasp (sur l'ensemble de l'action)
analyse_methode_nb_grasp_prediction: int nombre de prediction lors des grasp
analyse_methode_good_last_grasp_prediction: int pour les actions grasp, le nombre pour lequelles la derniere prediction est correct
analyse_methode_nb_last_grasp_prediction: int nombre de grasp (normalement autant de grasp que de release)
liste_analyse_methode_grasp_temps: liste contenant pour chaque action grasp dont la derniere prediction est correct, depuis combien de temps est-ce qu'elle etait correct (en ms)
analyse_methode_good_release_prediction: int nombre de bonnes predictions lors des releases (sur l'ensemble de l'action)
analyse_methode_nb_release_prediction: int nombre de prediction lors des release
analyse_methode_good_last_release_prediction: int pour les actions release, le nombre pour lequelles la derniere prediction est correct
analyse_methode_nb_last_release_prediction: int nombre de release (normalement autant de grasp que de release)
liste_analyse_methode_release_temps: liste contenant pour chaque action release dont la derniere prediction est correct, depuis combien de temps est-ce qu'elle etait correct (en ms)
total_nb_grasp: int nombre de grasp (normalement autant de grasp que de release)

Output

None

TODO analyse_methode_nb_last_grasp_prediction,analyse_methode_nb_last_release_prediction,total_nb_grasp sont equivalent

"""
def analyseMethod(
    method,

    liste_analyse_methode_grasp_temps,
    liste_analyse_methode_release_temps,
    total_nb_grasp,
):
    
    print("TODO")


"""
analyseSituation does blah blah blah.

Input

world: np.array(k,241) correspond a l'ensemble des donnes present dans le fichier states.csv
gaze_point: np.array(x,3) correspond a l'ensemble des donnes present dans le fichier tables.csv
history_prediction: np.array(y) np array de taille gaze_point[-1,0] - gaze_point[1,0], pour chaque i on a soit pour les grasp l'id du bloc de l'on predit qui va etre prit
                                                                                                          soit pour le srelease l'id d'un bloc adjacent a

Output

good_grasp_prediction: int nombre de bonnes predictions lors des grasp (sur l'ensemble de l'action)
time_grasp: int nombre de prediction lors des grasp
good_release_prediction: int nombre de bonnes predictions lors des releases (sur l'ensemble de l'action)
time_release: int nombre de prediction lors des release
good_last_grasp_prediction: int pour les actions grasp, le nombre pour lequelles la derniere prediction est correct
len(liste_holding): int nombre de grasp
good_last_release_prediction: int pour les actions release, le nombre pour lequelles la derniere prediction est correct
len(liste_adjacence_release): int nombre de release
list_time_good_grasp_predi: liste contenant pour chaque action grasp dont la derniere prediction est correct, depuis combien de temps est-ce qu'elle etait correct (en ms)
list_time_good_release_predi: liste contenant pour chaque action release dont la derniere prediction est correct, depuis combien de temps est-ce qu'elle etait correct (en ms)
"""
def analyseSituation(world, gaze_point, history_prediction,timestamp_action):
    
    
    if analyse:
        plt.close()
        # Declaration des variables
        liste_holding, liste_holding_t = listeHolding(world)
        
        
        liste_adjacence_release = listeRelease(world)
        
        liste_adjacence_release_t = []

        list_time_good_grasp_predi = []
        list_time_good_release_predi = []

        timestamp_action_indice = 1

        grasp_result = np.zeros((history_prediction.shape[1]))
        find_result = np.zeros((history_prediction.shape[1]))


        for i in range(history_prediction.shape[1]):

            if (timestamp_action_indice-1)//2 < len(liste_holding) and history_prediction[0][i] == liste_holding[(timestamp_action_indice-1)//2]:
                grasp_result[i] += 1

                

                if i == timestamp_action[timestamp_action_indice] and timestamp_action_indice %2 == 1:
                    
                    time_predi_end = i
                    time_predi_start = i

                    while time_predi_start >= 0 and history_prediction[0][time_predi_start] == liste_holding[(timestamp_action_indice-1)//2]:
                        time_predi_start -= 1

                    list_time_good_grasp_predi.append(time_predi_start - time_predi_end)

                    time_predi_end = i
                    time_predi_start = i

                    while time_predi_start < history_prediction.shape[1] and history_prediction[0][time_predi_start] == liste_holding[(timestamp_action_indice-1)//2]:
                        time_predi_start += 1
                    
                    list_time_good_grasp_predi.append(time_predi_start - time_predi_end)

            
            if (timestamp_action_indice)//2 < len(liste_adjacence_release) and history_prediction[1][i] in liste_adjacence_release[(timestamp_action_indice-1)//2]:
                find_result[i] += 1

                

                if i == timestamp_action[timestamp_action_indice] and timestamp_action_indice %2 == 0:
                    time_predi_end = i
                    time_predi_start = i

                    while time_predi_start >= 0 and history_prediction[1][time_predi_start] in liste_adjacence_release[(timestamp_action_indice-1)//2]:
                        time_predi_start -= 1

                    list_time_good_release_predi.append(time_predi_start - time_predi_end )

                    time_predi_end = i
                    time_predi_start = i

                    while time_predi_start < history_prediction.shape[1] and history_prediction[1][time_predi_start] in liste_adjacence_release[(timestamp_action_indice-1)//2]:
                        time_predi_start += 1
                    
                    list_time_good_release_predi.append(time_predi_start - time_predi_end)
            
            if (
                i < history_prediction.shape[1] - 1
                and history_prediction[timestamp_action_indice%2][i] != -1
                and history_prediction[timestamp_action_indice%2][i + 1] == -1
            ):
                liste_adjacence_release_t.append(int(i))


            if timestamp_action_indice < len(timestamp_action) - 1 and i+1 > timestamp_action[timestamp_action_indice]:
                timestamp_action_indice += 1


            
    """
    # Analyse des predictions de grasp lorsqu'on a un grasp (prediction juste et depuis cbm de temps)
    good_last_grasp_prediction = 0
    for i in range(len(liste_holding)):
        if liste_holding[i] == history_prediction[0][liste_holding_t[i]-1]:
            good_last_grasp_prediction += 1

            time_predi_end = liste_holding_t[i]-1
            time_predi_start = liste_holding_t[i]-1
            while history_prediction[0][time_predi_start] == liste_holding[i]:
                time_predi_start -= 1
            list_time_good_grasp_predi.append(time_predi_start - time_predi_end - 1)

            time_predi_end = liste_holding_t[i]-1
            time_predi_start = liste_holding_t[i]-1
            while history_prediction[0][time_predi_start] == liste_holding[i]:
                time_predi_start += 1
            list_time_good_grasp_predi.append(time_predi_start - time_predi_end - 1)

    """
    # Analyse des predictions de release lorsqu'on a un release (prediction juste et depuis cbm de temps)



    grasp_ind = 1
    analyse_grasp = np.zeros((6001))
    while grasp_ind < len(timestamp_action)-1:
        grasp_action_indice = timestamp_action[grasp_ind]
        for i in range(grasp_action_indice-3000,grasp_action_indice+3001,1):
            if i >=0 and i<len(grasp_result):
                analyse_grasp[int(i-(grasp_action_indice-3000))] += grasp_result[i]

        grasp_ind += 2

    #print(len(list_time_good_grasp_predi),len(list_time_good_release_predi))

    return (
        list_time_good_grasp_predi,
        list_time_good_release_predi,
        analyse_grasp,
    )


def analyseRelease(quadrillage,liste_good_zones,timestamp_action):
    good = 0
    last_good = 0
    total = 0

    list_t = []

    timestamp_action_indice = 2

    for i in range(1,quadrillage.shape[0]):
        

        if quadrillage[i] >= 0:
            if int((timestamp_action_indice-2)/2) >= len(liste_good_zones):
                print(i,timestamp_action,quadrillage.shape[0])
            elif quadrillage[i] in liste_good_zones[int((timestamp_action_indice-2)/2)]:
                good += 1
            total +=1

                

           

            if i == timestamp_action[timestamp_action_indice] and int((timestamp_action_indice-2)/2) < len(liste_good_zones) and quadrillage[i] in liste_good_zones[int((timestamp_action_indice-2)/2)]:
                last_good+=1

                t_start = i - 1
                t_end = i - 1
                while t_start >= 0 and quadrillage[t_start] in liste_good_zones[int((timestamp_action_indice-2)/2)]:
                    t_start -= 1
                list_t.append(t_start - t_end )

                t_start = i - 1
                t_end = i - 1
                while t_start < quadrillage.shape[0] and quadrillage[t_start] in liste_good_zones[int((timestamp_action_indice-2)/2)]:
                    t_start += 1
                list_t.append(t_start - t_end)

        if i+1 > timestamp_action[timestamp_action_indice]:
            if timestamp_action_indice + 2 < len(timestamp_action):
                timestamp_action_indice += 2
    return good,total,last_good,list_t




def evaluationBestArea(prediction, liste_good_area, timestamp_action):

    good = 0 
    total = 0
    last_good = 0
    timestamp_action_indice = 2
    list_t = []



    for i in range(prediction.shape[0]):
        total += 1

        if prediction[i] >= 0:
            
            x0 = round((48/largeur)*liste_good_area[int((timestamp_action_indice-2)/2)][0])
            y0 = round((24/hauteur)*liste_good_area[int((timestamp_action_indice-2)/2)][1])
            x2 = round((48/largeur)*liste_good_area[int((timestamp_action_indice-2)/2)][2])
            y2 = round((24/hauteur)*liste_good_area[int((timestamp_action_indice-2)/2)][3])
            x = prediction[i] // 24
            y = prediction[i] % 24

            if x2 - 8 <= x and x <= x0 and y2 - 8 <= y and y <= y0:
                good += 1

                if i == timestamp_action[timestamp_action_indice]:
                    last_good+=1

                    t_start = i - 1
                    t_end = i - 1
                    while t_start >= 0 and x2 - 8 <= (prediction[t_start] // 24) and (prediction[t_start] // 24) <= x0 and y2 - 8 <= (prediction[t_start] % 24) and (prediction[t_start] % 24) <= y0:
                        t_start -= 1
                    list_t.append(t_start - t_end )

                    t_start = i - 1
                    t_end = i - 1
                    while t_start < prediction.shape[0] and x2 - 8 <= (prediction[t_start] // 24) and (prediction[t_start] // 24) <= x0 and y2 - 8 <= (prediction[t_start] % 24) and (prediction[t_start] % 24) <= y0:
                        t_start += 1
                    list_t.append(t_start - t_end)

        
        if i+1 > timestamp_action[timestamp_action_indice]:
            if timestamp_action_indice + 2 < len(timestamp_action):
                timestamp_action_indice += 2

    return good,total,last_good,list_t

def goodAreaCoord(world):

    liste = []
    for i in range(2, world.shape[0]):
        for indice in range(24):
            if world[i - 1, 10 * indice + 10] == 1:
                sub_liste = []
                sub_liste.append(world[i, 10 * indice + 1])
                sub_liste.append(world[i, 10 * indice + 2])

                sub_liste.append(world[i, 10 * indice + 5])
                sub_liste.append(world[i, 10 * indice + 6])
                liste.append(sub_liste)

    return liste