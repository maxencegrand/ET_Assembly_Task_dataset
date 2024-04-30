import numpy as np
import math
import os
import time

from tools import liste_tenon_bloc

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
bestAreaMax renvoi l'emplacement de la meilleur zone 8x8 

Input

zone: les probabilites des zones 1x1
liste_t_value: l'ensemble des timestamp ou l'on a eu un gaze point (ca ne sert a rien de regarder les autres t)

Output

array: np.array(duration) pour tout t, l'id du tenon en haut a gauche de la zone 8x8 qui maximise les proba
"""
def bestAreaMax(zone):

    somme_min_8 = 0
    indice_min_8 = 0

    somme_min_4 = 0
    indice_min_4 = 0
    for i in range(nb_area_1):
        
        x = i // 24
        y = i % 24

        if x <= 40 and y <= 16:
            # Utilisez des tranches pour obtenir les 8 lignes et 8 colonnes nécessaires pour chaque somme
            rows_8 = [zone[(x+i)*24+y:(x+i)*24+y+8] for i in range(8)]

            # Utilisez np.sum() pour sommer les valeurs de chaque ligne
            somme_8 = np.sum(rows_8)

            if somme_8 > somme_min_8:
                somme_min_8 = somme_8
                indice_min_8 = x * 24 + y

        if x <= 44 and y <= 20:
            rows_4 = [zone[(x+i)*24+y:(x+i)*24+y+4] for i in range(4)]

            # Utilisez np.sum() pour sommer les valeurs de chaque ligne
            somme_4 = np.sum(rows_4)

            if somme_4 > somme_min_4:
                somme_min_4 = somme_4
                indice_min_4 = x * 24 + y
    



    return indice_min_4,indice_min_8

"""
interpretation renvoi les prediction des zones d'action ainsi que les prediction de grasp/ref

Input

probability: np.array((5, 2, duration, nb_area_1)) probabilite qu'un bloc tenon soit important selon les 5 manieres de calculer, sur la duree d'un assamblage, pour tous les tenons. La dimension 2 correspond aux reset grasp ou reset release
timestamp_action: liste des t correspondant aux evenements, avec 0 et le t final inclus
liste_t_value: l'ensemble des timestamp ou l'on a eu un gaze point (ca ne sert a rien de regarder les autres t)
world: np.array(k,241) correspond a l'ensemble des donnes present dans le fichier states.csv

Output
[area1max_indices,area2max_indices,area4max_indices,area8max_indices]: les predictions des zones de release
area_best: la prediction de zone glissante 
liste_predi_id: Prediction de bloc (grasp lors des grasp et ref lors des releases)

"""
def interpretation(probability, timestamp_indice,world):

    ################################################
    ############# Prediction Zone Fixe #############
    ################################################

    area1 = np.reshape(probability, (5, 2, 48, 24))

    # Somme des carrés de 2x2
    area2 = area1[:, :, ::2, ::2] + area1[:, :, ::2, 1::2] + area1[:, :, 1::2, ::2] + area1[:, :, 1::2, 1::2]
    area4 = area2[:, :, ::2, ::2] + area2[:, :, ::2, 1::2] + area2[:, :, 1::2, ::2] + area2[:, :, 1::2, 1::2]
    area8 = area4[:, :, ::2, ::2] + area4[:, :, ::2, 1::2] + area4[:, :, 1::2, ::2] + area4[:, :, 1::2, 1::2]
    
    area1 = np.reshape(area1, (5, 2, 48 * 24))
    area2 = np.reshape(area2, (5, 2, 24 * 12))
    area4 = np.reshape(area4, (5, 2, 12 * 6))
    area8 = np.reshape(area8, (5, 2, 6 * 3))

    area4max_indices = np.argmax(area4, axis=2)
    area8max_indices = np.argmax(area8, axis=2)

    ################################################
    ########### Prediction Zone Glissante ##########
    ################################################

    area_best_4 = np.zeros((5, 2))
    area_best_8 = np.zeros((5, 2))
    
    area_best_4[0][0],area_best_8[0][0] = bestAreaMax(area1[0][0])
    area_best_4[1][0],area_best_8[1][0] = bestAreaMax(area1[1][0])
    area_best_4[2][0],area_best_8[2][0] = bestAreaMax(area1[2][0])
    area_best_4[3][0],area_best_8[3][0] = bestAreaMax(area1[3][0])
    area_best_4[4][0],area_best_8[4][0] = bestAreaMax(area1[4][0])

    area_best_4[0][1], area_best_8[0][1] = bestAreaMax(area1[0][1])
    area_best_4[1][1], area_best_8[1][1] = bestAreaMax(area1[1][1])
    area_best_4[2][1], area_best_8[2][1] = bestAreaMax(area1[2][1])
    area_best_4[3][1], area_best_8[3][1] = bestAreaMax(area1[3][1])
    area_best_4[4][1], area_best_8[4][1] = bestAreaMax(area1[4][1])

    ################################################
    ############### Prediction Grasp ###############
    ################################################

    liste_resultat = liste_tenon_bloc(world)



    liste_predi_id = np.zeros((5,2))
        
    proba = np.zeros((5,2,24))

    #print(timestamp_indice, timestamp_indice % 2)

    for r in range(24):
        #On regarde l'etat precedent pour voir l'evolution post event
        for tendon in liste_resultat[max(0,timestamp_indice - 2)][r]:
            proba[0,timestamp_indice % 2,r] += probability[0,(timestamp_indice) % 2,tendon]
            proba[1,timestamp_indice % 2,r] += probability[1,(timestamp_indice) % 2,tendon]
            proba[2,timestamp_indice % 2,r] += probability[2,(timestamp_indice) % 2,tendon]
            proba[3,timestamp_indice % 2,r] += probability[3,(timestamp_indice) % 2,tendon]
            proba[4,timestamp_indice % 2,r] += probability[4,(timestamp_indice) % 2,tendon]
        
        #On regarde l'etat precedent pour voir l'evolution post event
        for tendon in liste_resultat[max(0,timestamp_indice - 1)][r]:
            proba[0,(timestamp_indice - 1) % 2,r] += probability[0,(timestamp_indice - 1) % 2,tendon]
            proba[1,(timestamp_indice - 1) % 2,r] += probability[1,(timestamp_indice - 1) % 2,tendon]
            proba[2,(timestamp_indice - 1) % 2,r] += probability[2,(timestamp_indice - 1) % 2,tendon]
            proba[3,(timestamp_indice - 1) % 2,r] += probability[3,(timestamp_indice - 1) % 2,tendon]
            proba[4,(timestamp_indice - 1) % 2,r] += probability[4,(timestamp_indice - 1) % 2,tendon]

        taille_bloc = ((((r//3)%2)+1)*4)

        proba[0,0,r] = proba[0,0,r] / taille_bloc
        proba[1,0,r] = proba[1,0,r] / taille_bloc
        proba[2,0,r] = proba[2,0,r] / taille_bloc
        proba[3,0,r] = proba[3,0,r] / taille_bloc
        proba[4,0,r] = proba[4,0,r] / taille_bloc

        proba[0,1,r] = proba[0,1,r] / taille_bloc
        proba[1,1,r] = proba[1,1,r] / taille_bloc
        proba[2,1,r] = proba[2,1,r] / taille_bloc
        proba[3,1,r] = proba[3,1,r] / taille_bloc
        proba[4,1,r] = proba[4,1,r] / taille_bloc
        
    liste_predi_id[0,0] = proba[0,0,:].argmax()
    liste_predi_id[1,0] = proba[1,0,:].argmax()
    liste_predi_id[2,0] = proba[2,0,:].argmax()
    liste_predi_id[3,0] = proba[3,0,:].argmax()
    liste_predi_id[4,0] = proba[4,0,:].argmax()

    liste_predi_id[0,1] = proba[0,1,:].argmax()
    liste_predi_id[1,1] = proba[1,1,:].argmax()
    liste_predi_id[2,1] = proba[2,1,:].argmax()
    liste_predi_id[3,1] = proba[3,1,:].argmax()
    liste_predi_id[4,1] = proba[4,1,:].argmax()


    return area4max_indices,area8max_indices,area_best_4,area_best_8,liste_predi_id