import numpy as np
import math
import os

plot_1 = False
analyse = True
plot_analyse = False

largeur = 76
hauteur = 38
dist_min = -largeur/(2*48)
dist_max = math.sqrt((largeur)**2+(hauteur)**2)

taille_zone = 1
nb_bloc_1 = int((48/1)*(24/1))
nb_bloc_2 = int((48/2)*(24/2))
nb_bloc_4 = int((48/4)*(24/4))
nb_bloc_8 = int((48/8)*(24/8))

array_zone1 = np.genfromtxt("../csv/zone_1x1.csv", delimiter=",")
array_zone2 = np.genfromtxt("../csv/zone_2x2.csv", delimiter=",")
array_zone4 = np.genfromtxt("../csv/zone_4x4.csv", delimiter=",")
array_zone8 = np.genfromtxt("../csv/zone_8x8.csv", delimiter=",")

from tools import CurrentWorld, isHolding, moreCloseRectangle, minDistanceRectangleGaze



"""
parsingOneSituation does blah blah blah.

Input

gaze_point: np.array(x,3) correspond a l'ensemble des donnes present dans le fichier tables.csv
world: np.array(k,241) correspond a l'ensemble des donnes present dans le fichier states.csv
ax: ax de plt.subplot

Output

list_timestamp: np.array(k) 1D qui contient l'ensemble des timestamp correspondant a un  capture d'eye tracking sur la table, les donnees sont dans l'ordre croissant
list_id: np.array(k) 1D qui contient pour chaque capture d'eye tracking sur la table, l'id du rectangle le plus proche
list_dist: np.array(k) 1D qui contient pour chaque capture d'eye tracking sur la table, la distance entre cette capture et le rectangle le plus proche
    list_timestamp[i], list_id[i] et list_dist[i] correspondent a la meme capture


max_compteur: np.array(x) pour chacun des timestamp de max_compteur_time donne l'id du rectangle qui a ete le plus present pour la derniere action
max_compteur_time: np.array(x) donne l'ensemble des timestamps de capture pour la derniere action 
    max_compteur_time[i] et max_compteur[i] correspondent a la meme capture

timestamp_action: TODO

history_prediction: np.array(y) np array de taille gaze_point[-1,0] - gaze_point[1,0], pour chaque i on a soit pour les grasp l'id du bloc de l'on predit qui va etre prit
                                                                                                          soit pour le srelease l'id d'un bloc adjacent a
"""

def parsingOneSituation(gaze_point, world):
    # memorise le timestamp initial
    t_init = gaze_point[1, 0]

    duration = gaze_point[-1, 0] - gaze_point[1, 0]

    feature = np.zeros((5, int(duration) + 1, nb_bloc_1)) 

    timestamp_action = [0]

    liste_data_t = []

    # Variable pour savoir si un bloc est en etat holding, commence a False
    holding = False

    # Pour chaque ligne correspondant a une donne de l'eye tracker
    for i in range(1, gaze_point.shape[0]):

        # On prend le temps depuis le debut
        t = int(gaze_point[i, 0] - t_init)

        # On extrait l'etat actuel de la table
        current_world = CurrentWorld(gaze_point[i, 0], world)


        # Si aucun holding avant et maintenant holding alors on est sur un grasp
        if holding == False and isHolding(current_world):

            holding = True

            timestamp_action.append(t)

        # Si holding avant et maintenant aucun holding alors on est sur un release
        if holding == True and isHolding(current_world) == False:

            holding = False

            timestamp_action.append(t)


        if str(gaze_point[i, 1]) != "nan":

            liste_data_t.append(t)

            # On recupere le rectangle le plus proche
            id, dist = moreCloseRectangle(
                current_world, gaze_point[i, 1], gaze_point[i, 2]
            )         

            d_min = math.inf
            i_min = math.inf


            for z in range(nb_bloc_1):
                zone = array_zone1[z + 1]
                d = minDistanceRectangleGaze(zone[1],zone[2],zone[3],zone[4],zone[5],zone[6],zone[7],zone[8],gaze_point[i,1],gaze_point[i,2])
                feature[2, t, z] += dist_max - d
                feature[3, t, z] += 1/(d-dist_min)

                K = math.log2((dist_max - dist_min) / (-2*dist_min) + 1)
                feature[4, t, z] += (K - math.log2((d - dist_min) / (-2*dist_min) + 1))/K
                if d < d_min:
                    d_min = d
                    i_min = z

            feature[0, t, i_min] += 1
            feature[1, t, i_min] += (dist_max - d_min)/(dist_max - dist_min)

    timestamp_action.append(t)

    liste_data_t = liste_data_t + timestamp_action
    liste_data_t.sort()
    return (
        feature,
        timestamp_action,
        liste_data_t,
    )