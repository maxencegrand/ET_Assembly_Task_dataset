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

def parsingOneSituation(gaze_value):

    feature = np.zeros((5, nb_area_1)) 

    if str(gaze_value[1]) != "nan":

            

        d_min = math.inf
        i_min = math.inf

        '''
        for z in range(nb_area_1):
            zone = array_zone1[z + 1]
            d = minDistanceRectangleGaze(zone[1],zone[2],zone[3],zone[4],zone[5],zone[6],zone[7],zone[8],gaze_value[1],gaze_value[2])
            feature[2, z] += (dist_max - d)/(dist_max - dist_min)
            feature[3, z] += 1/(d-dist_min)

            K = math.log2((dist_max - dist_min) / (-2*dist_min) + 1)
            feature[4, z] += (K - math.log2((d - dist_min) / (-2*dist_min) + 1))/K
            if d < d_min:
                d_min = d
                i_min = z

        feature[0, i_min] += 1
        feature[1, i_min] += (dist_max - d_min)/(dist_max - dist_min)

        '''
        for z in range(nb_area_1):
            zone = array_zone1[z + 1]
            zone_x_mean = (zone[1] + zone[5])/2
            zone_y_mean = (zone[2] + zone[6])/2
            d = math.sqrt((zone_x_mean - gaze_value[1])**2 + (zone_y_mean - gaze_value[2])**2)
            
            feature[2, z] += (dist_max - d)/(dist_max - dist_min)
            feature[3, z] += 1/(d-dist_min)

            K = math.log2((dist_max - dist_min) / (-2*dist_min) + 1)
            
            feature[4, z] += (K - math.log2((d - dist_min) / (-2*dist_min) + 1))/K

            if d < d_min:
                d_min = d
                i_min = z

        feature[0, i_min] += 1
        feature[1, i_min] += (dist_max - d_min)/(dist_max - dist_min)
        
    return (
        feature,
    )