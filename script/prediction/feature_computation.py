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
nb_area_1 = int((48/1)*(24/1))
nb_area_2 = int((48/2)*(24/2))
nb_area_4 = int((48/4)*(24/4))
nb_area_8 = int((48/8)*(24/8))

array_zone1 = np.genfromtxt("../csv/zone_1x1.csv", delimiter=",")
array_zone2 = np.genfromtxt("../csv/zone_2x2.csv", delimiter=",")
array_zone4 = np.genfromtxt("../csv/zone_4x4.csv", delimiter=",")
array_zone8 = np.genfromtxt("../csv/zone_8x8.csv", delimiter=",")

from tools import CurrentWorld, isHolding, moreCloseRectangle, minDistanceRectangleGaze



"""
parsingOneSituation prend les gaze point d'un participant pour une figure et retourne les poids pour tout t ainsi que l'ensemble des timestamps auquels il y a une action.

Input

gaze_point: np.array(x,3) correspond a l'ensemble des donnes present dans le fichier tables.csv
world: np.array(k,241) correspond a l'ensemble des donnes present dans le fichier states.csv

Output

feature: np.array(5,d,nb_tenon), poid pour les 5 manieres de calculer, pour tout t dans la duree de l'assamblage, pour chaque tenon
timestamp_action: liste des t correspondant aux evenements, avec 0 et le t final inclus
liste_data_t: liste des t correspondant a un gaze point non nul
"""

def parsingOneSituation(gaze_point, world):
    # memorise le timestamp initial
    t_init = gaze_point[1, 0]

    duration = gaze_point[-1, 0] - gaze_point[1, 0]

    feature = np.zeros((5, int(duration) + 1, nb_area_1)) 

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

            d_min = math.inf
            i_min = math.inf

            '''
            for z in range(nb_area_1):
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
            '''

            for z in range(nb_area_1):
                zone = array_zone1[z + 1]
                zone_x_mean = (zone[1] + zone[5])/2
                zone_y_mean = (zone[2] + zone[6])/2
                d = math.sqrt((zone_x_mean - gaze_point[i,1])**2 + (zone_y_mean - gaze_point[i,2])**2)
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