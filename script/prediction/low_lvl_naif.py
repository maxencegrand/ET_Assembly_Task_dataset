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
nb_area_1 = int((48/1)*(24/1))
nb_area_2 = int((48/2)*(24/2))
nb_area_4 = int((48/4)*(24/4))
nb_area_8 = int((48/8)*(24/8))

array_zone1 = np.genfromtxt("../csv/zone_1x1.csv", delimiter=",")
array_zone2 = np.genfromtxt("../csv/zone_2x2.csv", delimiter=",")
array_zone4 = np.genfromtxt("../csv/zone_4x4.csv", delimiter=",")
array_zone8 = np.genfromtxt("../csv/zone_8x8.csv", delimiter=",")


"""
low_level_naif prend les poids de feature extraction et renvoi les probabilites selon la methode modele

Input

feature: np.array(5,d,nb_tenon), poid pour les 5 manieres de calculer, pour tout t dans la duree de l'assamblage, pour chaque tenon
timestamp_action: liste des t correspondant aux evenements, avec 0 et le t final inclus

Output

probability: np.array((5, 2, duration, nb_area_1)) probabilite qu'un bloc tenon soit important selon les 5 manieres de calculer, sur la duree d'un assamblage, pour tous les tenons. La dimension 2 correspond aux reset grasp ou reset release
"""
def low_level_naif(feature,timestamp,timestamp_action,timestamp_indice,past_probability_score):

    new_probability = np.zeros((5, 2, nb_area_1))
    new_probability_score = np.zeros((5, 2, nb_area_1))
        
    if timestamp_indice < len(timestamp_action)-1 and timestamp == timestamp_action[timestamp_indice]:


        new_probability_score[0, (timestamp_indice + 1) % 2] = past_probability_score[0, (timestamp_indice + 1) % 2] + feature[0]
        new_probability_score[1, (timestamp_indice + 1) % 2] = past_probability_score[1, (timestamp_indice + 1) % 2] + feature[1]
        new_probability_score[2, (timestamp_indice + 1) % 2] = past_probability_score[2, (timestamp_indice + 1) % 2] + feature[2]
        new_probability_score[3, (timestamp_indice + 1) % 2] = past_probability_score[3, (timestamp_indice + 1) % 2] + feature[3]
        new_probability_score[4, (timestamp_indice + 1) % 2] = past_probability_score[4, (timestamp_indice + 1) % 2] + feature[4]

        new_probability_score[0, timestamp_indice % 2] = feature[0]
        new_probability_score[1, timestamp_indice % 2] = feature[1]
        new_probability_score[2, timestamp_indice % 2] = feature[2]
        new_probability_score[3, timestamp_indice % 2] = feature[3]
        new_probability_score[4, timestamp_indice % 2] = feature[4]

        timestamp_indice += 1

    else:

        new_probability_score[0, 0] = past_probability_score[0, 0] + feature[0]
        new_probability_score[1, 0] = past_probability_score[1, 0] + feature[1]
        new_probability_score[2, 0] = past_probability_score[2, 0] + feature[2]
        new_probability_score[3, 0] = past_probability_score[3, 0] + feature[3]
        new_probability_score[4, 0] = past_probability_score[4, 0] + feature[4]

        new_probability_score[0, 1] = past_probability_score[0, 1] + feature[0]
        new_probability_score[1, 1] = past_probability_score[1, 1] + feature[1]
        new_probability_score[2, 1] = past_probability_score[2, 1] + feature[2]
        new_probability_score[3, 1] = past_probability_score[3, 1] + feature[3]
        new_probability_score[4, 1] = past_probability_score[4, 1] + feature[4]


        


    for m in range(5):
        if np.sum(new_probability_score[m,0]) > 0:
            new_probability[m, 0] = new_probability_score[m, 0]/np.sum(new_probability_score[m, 0])

        else:
            new_probability[m, 0] = np.ones((nb_area_1))/nb_area_1

        if np.sum(new_probability_score[m,1]) > 0:
            new_probability[m, 1] = new_probability_score[m, 1]/np.sum(new_probability_score[m, 1])

        else:
            new_probability[m, 1] = np.ones((nb_area_1))/nb_area_1

    return new_probability, new_probability_score, timestamp_indice