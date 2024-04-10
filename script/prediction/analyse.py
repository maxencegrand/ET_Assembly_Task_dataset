import numpy as np
import math

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

array_zone1 = np.genfromtxt("../csv/zone_1x1.csv", delimiter=",")
array_zone2 = np.genfromtxt("../csv/zone_2x2.csv", delimiter=",")
array_zone4 = np.genfromtxt("../csv/zone_4x4.csv", delimiter=",")
array_zone8 = np.genfromtxt("../csv/zone_8x8.csv", delimiter=",")

from tools import listeHolding,listeRelease




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
def analyseSituation(world, history_prediction,timestamp_action):
    

    # Declaration des variables
    liste_holding, liste_holding_t = listeHolding(world)
    
    
    liste_adjacence_release = listeRelease(world)


    analyse_grasp = np.zeros((6001))
    nb_analyse_grasp = np.zeros((6001))

    analyse_release = np.zeros((6001))
    nb_analyse_release = np.zeros((6001))

    for t in range(1,len(timestamp_action)-1):
        for time in range(max(0,timestamp_action[t]-3000),min(timestamp_action[-1],timestamp_action[t] + 3001)):
            if (t - 1) % 2 == 0:
                if history_prediction[0][time] == liste_holding[(t - 1) // 2]:
                    analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
            else:
                if history_prediction[1][time] in liste_adjacence_release[(t-1)//2]:
                    analyse_release[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_release[time - (timestamp_action[t] - 3000)] += 1


    #print(len(list_time_good_grasp_predi),len(list_time_good_release_predi))

    return (
        analyse_grasp,
        nb_analyse_grasp,
        analyse_release,
        nb_analyse_release
    )


def analyseRelease(quadrillage,liste_good_grasp_zones, liste_good_release_zones,timestamp_action):

    analyse_grasp = np.zeros((6001))
    nb_analyse_grasp = np.zeros((6001))

    analyse_release = np.zeros((6001))
    nb_analyse_release = np.zeros((6001))

    for t in range(1,len(timestamp_action)-1):
        for time in range(max(0,timestamp_action[t]-3000),min(timestamp_action[-1],timestamp_action[t] + 3001)):
            if (t - 1) % 2 == 0:
                if quadrillage[0][time] in liste_good_grasp_zones[(t - 1) // 2]:
                    analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
            else:
                if quadrillage[1][time] in liste_good_release_zones[(t-1)//2]:
                    analyse_release[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_release[time - (timestamp_action[t] - 3000)] += 1

    return analyse_grasp, nb_analyse_grasp, analyse_release, nb_analyse_release




def evaluationBestArea(prediction, liste_good_grasp_area, liste_good_release_area, timestamp_action):

    analyse_grasp = np.zeros((6001))
    nb_analyse_grasp = np.zeros((6001))

    analyse_release = np.zeros((6001))
    nb_analyse_release = np.zeros((6001))

    for t in range(1,len(timestamp_action)-1):
        for time in range(max(0,timestamp_action[t]-3000),min(timestamp_action[-1],timestamp_action[t] + 3001)):
            

            if (t - 1) % 2 == 0:
                x = prediction[0][time] // 24
                y = prediction[0][time] % 24
            
                x0 = round((48/largeur)*liste_good_grasp_area[int((t-1)//2)][0])
                y0 = round((24/hauteur)*liste_good_grasp_area[int((t-1)//2)][1])
                x2 = round((48/largeur)*liste_good_grasp_area[int((t-1)//2)][2])
                y2 = round((24/hauteur)*liste_good_grasp_area[int((t-1)//2)][3])

                if x2 - 8 <= x and x <= x0 and y2 - 8 <= y and y <= y0:
                    analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_grasp[time - (timestamp_action[t] - 3000)] += 1

            else:
                x = prediction[1][time] // 24
                y = prediction[1][time] % 24

                x0 = round((48/largeur)*liste_good_release_area[int((t-1)//2)][0])
                y0 = round((24/hauteur)*liste_good_release_area[int((t-1)//2)][1])
                x2 = round((48/largeur)*liste_good_release_area[int((t-1)//2)][2])
                y2 = round((24/hauteur)*liste_good_release_area[int((t-1)//2)][3])

                if x2 - 8 <= x and x <= x0 and y2 - 8 <= y and y <= y0:
                    analyse_release[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_release[time - (timestamp_action[t] - 3000)] += 1

    return (analyse_grasp,
        nb_analyse_grasp,
        analyse_release,
        nb_analyse_release)


def goodGraspAreaCoord(world):
    liste = []
    for i in range(1, world.shape[0]-1):
        for indice in range(24):
            if world[i + 1, 10 * indice + 10] == 1:
                sub_liste = []
                sub_liste.append(world[i, 10 * indice + 1])
                sub_liste.append(world[i, 10 * indice + 2])

                sub_liste.append(world[i, 10 * indice + 5])
                sub_liste.append(world[i, 10 * indice + 6])
                liste.append(sub_liste)

    return liste


def goodReleaseAreaCoord(world):
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

