import numpy as np
import math
import os
import time

from tools import liste_tenon_bloc

from enum import Enum

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

array_zone_table = np.genfromtxt("../csv/zone_table.csv", delimiter=",")

array_zone_left = np.genfromtxt("../csv/zone_left.csv", delimiter=",")
array_zone_middle = np.genfromtxt("../csv/zone_middle.csv", delimiter=",")
array_zone_right = np.genfromtxt("../csv/zone_right.csv", delimiter=",")

array_zone_blue = np.genfromtxt("../csv/zone_blue.csv", delimiter=",")
array_zone_red = np.genfromtxt("../csv/zone_red.csv", delimiter=",")
array_zone_green = np.genfromtxt("../csv/zone_green.csv", delimiter=",")
array_zone_yellow = np.genfromtxt("../csv/zone_yellow.csv", delimiter=",")

array_zone_car = np.genfromtxt("../csv/zone_car.csv", delimiter=",")
array_zone_house = np.genfromtxt("../csv/zone_house.csv", delimiter=",")
array_zone_sc = np.genfromtxt("../csv/zone_sc.csv", delimiter=",")
array_zone_tb = np.genfromtxt("../csv/zone_tb.csv", delimiter=",")
array_zone_tc = np.genfromtxt("../csv/zone_tc.csv", delimiter=",")
array_zone_tsb = np.genfromtxt("../csv/zone_tsb.csv", delimiter=",")

class Level0(Enum):
    TABLE = 1


class Level1(Enum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3

class Level2(Enum):
    BLUE = 1
    RED = 2
    GREEN = 3
    YELLOW = 4
    FIG = 5

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


def semantic_prediction_level0(zone):
    score = np.zeros((1))
    liste_zone = [array_zone_table]
    for zone_id,zone_coord in enumerate(liste_zone):
        x0 = zone_coord[1,0]
        y0 = zone_coord[1,1]

        x1 = zone_coord[1,2]
        y1 = zone_coord[1,3]

        somme = 0
        count = 0

        for x in range(int(x0),int(x1)):
            for y in range(int(y0),int(y1)):
                indice = x * 24 + y
                somme += zone[indice]
                count += 1

        score[zone_id] = somme / count

    return score.argmax()

def semantic_prediction_level1(zone):
    score = np.zeros((3))
    liste_zone = [array_zone_left,array_zone_middle,array_zone_right]
    for zone_id,zone_coord in enumerate(liste_zone):
        x0 = zone_coord[1,0]
        y0 = zone_coord[1,1]

        x1 = zone_coord[1,2]
        y1 = zone_coord[1,3]

        somme = 0
        count = 0

        for x in range(int(x0),int(x1)):
            for y in range(int(y0),int(y1)):
                indice = x * 24 + y
                somme += zone[indice]
                count += 1

        score[zone_id] = somme / count

    return score.argmax()

def semantic_prediction_level2(zone,fig):
    score = np.zeros((5))
    liste_zone = [array_zone_blue,array_zone_red,array_zone_green,array_zone_yellow]
    if fig == "car":
        liste_zone.append(array_zone_car)
    if fig == "house":
        liste_zone.append(array_zone_house)
    if fig == "sc":
        liste_zone.append(array_zone_sc)
    if fig == "tb":
        liste_zone.append(array_zone_tb)
    if fig == "tc":
        liste_zone.append(array_zone_tc)
    if fig == "tsb":
        liste_zone.append(array_zone_tsb)

    for zone_id,zone_coord in enumerate(liste_zone):
        x0 = zone_coord[1,0]
        y0 = zone_coord[1,1]

        x1 = zone_coord[1,2]
        y1 = zone_coord[1,3]

        somme = 0
        count = 0

        for x in range(int(x0),int(x1)):
            for y in range(int(y0),int(y1)):
                indice = x * 24 + y
                somme += zone[indice]
                count += 1

        score[zone_id] = somme / count

    return score.argmax()


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
def interpretation(probability, timestamp_indice,world,fig):

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
    
    #area_best_4[0][0],area_best_8[0][0] = bestAreaMax(area1[0][0])
    #area_best_4[1][0],area_best_8[1][0] = bestAreaMax(area1[1][0])
    #area_best_4[2][0],area_best_8[2][0] = bestAreaMax(area1[2][0])
    #area_best_4[3][0],area_best_8[3][0] = bestAreaMax(area1[3][0])
    #area_best_4[4][0],area_best_8[4][0] = bestAreaMax(area1[4][0])

    #area_best_4[0][1], area_best_8[0][1] = bestAreaMax(area1[0][1])
    #area_best_4[1][1], area_best_8[1][1] = bestAreaMax(area1[1][1])
    #area_best_4[2][1], area_best_8[2][1] = bestAreaMax(area1[2][1])
    #area_best_4[3][1], area_best_8[3][1] = bestAreaMax(area1[3][1])
    #area_best_4[4][1], area_best_8[4][1] = bestAreaMax(area1[4][1])

    ################################################
    ########### Prediction Zone Semantic 0 #########
    ################################################

    area_semantique_0 = np.zeros((5, 2))
    area_semantique_1 = np.zeros((5, 2))
    area_semantique_2 = np.zeros((5, 2))

    
    area_semantique_0[0][0] = semantic_prediction_level0(area1[0][0])
    area_semantique_0[1][0] = semantic_prediction_level0(area1[1][0])
    area_semantique_0[2][0] = semantic_prediction_level0(area1[2][0])
    area_semantique_0[3][0] = semantic_prediction_level0(area1[3][0])
    area_semantique_0[4][0] = semantic_prediction_level0(area1[4][0])

    area_semantique_0[0][1] = semantic_prediction_level0(area1[0][1])
    area_semantique_0[1][1] = semantic_prediction_level0(area1[1][1])
    area_semantique_0[2][1] = semantic_prediction_level0(area1[2][1])
    area_semantique_0[3][1] = semantic_prediction_level0(area1[3][1])
    area_semantique_0[4][1] = semantic_prediction_level0(area1[4][1])

    area_semantique_1[0][0] = semantic_prediction_level1(area1[0][0])
    area_semantique_1[1][0] = semantic_prediction_level1(area1[1][0])
    area_semantique_1[2][0] = semantic_prediction_level1(area1[2][0])
    area_semantique_1[3][0] = semantic_prediction_level1(area1[3][0])
    area_semantique_1[4][0] = semantic_prediction_level1(area1[4][0])

    area_semantique_1[0][1] = semantic_prediction_level1(area1[0][1])
    area_semantique_1[1][1] = semantic_prediction_level1(area1[1][1])
    area_semantique_1[2][1] = semantic_prediction_level1(area1[2][1])
    area_semantique_1[3][1] = semantic_prediction_level1(area1[3][1])
    area_semantique_1[4][1] = semantic_prediction_level1(area1[4][1])

    area_semantique_2[0][0] = semantic_prediction_level2(area1[0][0],fig)
    area_semantique_2[1][0] = semantic_prediction_level2(area1[1][0],fig)
    area_semantique_2[2][0] = semantic_prediction_level2(area1[2][0],fig)
    area_semantique_2[3][0] = semantic_prediction_level2(area1[3][0],fig)
    area_semantique_2[4][0] = semantic_prediction_level2(area1[4][0],fig)

    area_semantique_2[0][1] = semantic_prediction_level2(area1[0][1],fig)
    area_semantique_2[1][1] = semantic_prediction_level2(area1[1][1],fig)
    area_semantique_2[2][1] = semantic_prediction_level2(area1[2][1],fig)
    area_semantique_2[3][1] = semantic_prediction_level2(area1[3][1],fig)
    area_semantique_2[4][1] = semantic_prediction_level2(area1[4][1],fig)

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


    return area4max_indices,area8max_indices,area_best_4,area_best_8, area_semantique_0, area_semantique_1, area_semantique_2, liste_predi_id