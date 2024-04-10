import numpy as np
import math
import os

from tools import liste_tenon_bloc

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

"""
bestAreaMax renvoi l'emplacement de la meilleur zone 8x8 

Input

zone: les probabilites des zones 1x1
liste_t_value: l'ensemble des timestamp ou l'on a eu un gaze point (ca ne sert a rien de regarder les autres t)

Output

array: np.array(duration) pour tout t, l'id du tenon en haut a gauche de la zone 8x8 qui maximise les proba
"""
def bestAreaMax(zone,liste_t_value):

    array = np.zeros((zone.shape[0]))
    for t in range(zone.shape[0]):
        somme_min = 0
        indice_min = 0
        for i in range(240,912):
            
            x = i // 24
            y = i % 24

            if x <= 40 and y <= 16:
                # Utilisez des tranches pour obtenir les 8 lignes et 8 colonnes nécessaires pour chaque somme
                rows = [zone[t, (x+i)*24+y:(x+i)*24+y+8] for i in range(8)]

                # Utilisez np.sum() pour sommer les valeurs de chaque ligne
                somme = np.sum(rows)

                if somme > somme_min:
                    somme_min = somme
                    indice_min = x * 24 + y
    
        array[t] = indice_min


    return array

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
def interpretation(probability, timestamp_action,liste_t_value,world,temps):
    duration = probability.shape[2]

    ################################################
    ############# Prediction Zone Fixe #############
    ################################################

    area1 = np.reshape(probability, (5, 2, duration, 48, 24))

    # Somme des carrés de 2x2
    area2 = area1[:, :, :, ::2, ::2] + area1[:, :, :, ::2, 1::2] + area1[:, :, :, 1::2, ::2] + area1[:, :, :, 1::2, 1::2]
    area4 = area2[:, :, :, ::2, ::2] + area2[:, :, :, ::2, 1::2] + area2[:, :, :, 1::2, ::2] + area2[:, :, :, 1::2, 1::2]
    area8 = area4[:, :, :, ::2, ::2] + area4[:, :, :, ::2, 1::2] + area4[:, :, :, 1::2, ::2] + area4[:, :, :, 1::2, 1::2]
    
    area1 = np.reshape(area1, (5, 2, duration, 48 * 24))
    area2 = np.reshape(area2, (5, 2, duration, 24 * 12))
    area4 = np.reshape(area4, (5, 2, duration, 12 * 6))
    area8 = np.reshape(area8, (5, 2, duration, 6 * 3))

    area1max_indices = np.argmax(area1, axis=3)
    area2max_indices = np.argmax(area2, axis=3)
    area4max_indices = np.argmax(area4, axis=3)
    area8max_indices = np.argmax(area8, axis=3)

    ################################################
    ########### Prediction Zone Glissante ##########
    ################################################

    area_best = np.zeros((5, 2, duration))
    #area_best[0][0] = bestAreaMax(area1[0][0],liste_t_value)
    #area_best[1][0] = bestAreaMax(area1[1][0],liste_t_value)
    #area_best[2][0] = bestAreaMax(area1[2][0],liste_t_value)
    #area_best[3][0] = bestAreaMax(area1[3][0],liste_t_value)
    #area_best[4][0] = bestAreaMax(area1[4][0],liste_t_value)

    #area_best[0][1] = bestAreaMax(area1[0][1],liste_t_value)
    #area_best[1][1] = bestAreaMax(area1[1][1],liste_t_value)
    #area_best[2][1] = bestAreaMax(area1[2][1],liste_t_value)
    #area_best[3][1] = bestAreaMax(area1[3][1],liste_t_value)
    #area_best[4][1] = bestAreaMax(area1[4][1],liste_t_value)

    ################################################
    ############### Prediction Grasp ###############
    ################################################

    liste_resultat = liste_tenon_bloc(world)

    indice_timestamp_action = 0


    liste_predi_id = np.zeros((5,2,duration))

    for t in range(duration):
        if indice_timestamp_action < len(timestamp_action) - 1 and liste_t_value[t] > timestamp_action[indice_timestamp_action + 1]:
                indice_timestamp_action += 1


            
        proba = np.zeros((5,2,24))
        for r in range(24):
            for tendon in liste_resultat[max(0,indice_timestamp_action - 1)][r]:
                proba[0,(max(0,indice_timestamp_action - 1)) % 2,r] += probability[0,(max(0,indice_timestamp_action - 1)) % 2,t,tendon]
                proba[1,(max(0,indice_timestamp_action - 1)) % 2,r] += probability[1,(max(0,indice_timestamp_action - 1)) % 2,t,tendon]
                proba[2,(max(0,indice_timestamp_action - 1)) % 2,r] += probability[2,(max(0,indice_timestamp_action - 1)) % 2,t,tendon]
                proba[3,(max(0,indice_timestamp_action - 1)) % 2,r] += probability[3,(max(0,indice_timestamp_action - 1)) % 2,t,tendon]
                proba[4,(max(0,indice_timestamp_action - 1)) % 2,r] += probability[4,(max(0,indice_timestamp_action - 1)) % 2,t,tendon]
                
            for tendon in liste_resultat[indice_timestamp_action][r]:
                proba[0,(indice_timestamp_action) % 2,r] += probability[0,(indice_timestamp_action) % 2,t,tendon]
                proba[1,(indice_timestamp_action) % 2,r] += probability[1,(indice_timestamp_action) % 2,t,tendon]
                proba[2,(indice_timestamp_action) % 2,r] += probability[2,(indice_timestamp_action) % 2,t,tendon]
                proba[3,(indice_timestamp_action) % 2,r] += probability[3,(indice_timestamp_action) % 2,t,tendon]
                proba[4,(indice_timestamp_action) % 2,r] += probability[4,(indice_timestamp_action) % 2,t,tendon]

            proba[0,0,r] = proba[0,0,r] / ((((r//3)%2)+1)*3)
            proba[1,0,r] = proba[1,0,r] / ((((r//3)%2)+1)*3)
            proba[2,0,r] = proba[2,0,r] / ((((r//3)%2)+1)*3)
            proba[3,0,r] = proba[3,0,r] / ((((r//3)%2)+1)*3)
            proba[4,0,r] = proba[4,0,r] / ((((r//3)%2)+1)*3)

            proba[0,1,r] = proba[0,1,r] / ((((r//3)%2)+1)*3)
            proba[1,1,r] = proba[1,1,r] / ((((r//3)%2)+1)*3)
            proba[2,1,r] = proba[2,1,r] / ((((r//3)%2)+1)*3)
            proba[3,1,r] = proba[3,1,r] / ((((r//3)%2)+1)*3)
            proba[4,1,r] = proba[4,1,r] / ((((r//3)%2)+1)*3)
            
        liste_predi_id[0,0,t] = proba[0,0,:].argmax()
        liste_predi_id[1,0,t] = proba[1,0,:].argmax()
        liste_predi_id[2,0,t] = proba[2,0,:].argmax()
        liste_predi_id[3,0,t] = proba[3,0,:].argmax()
        liste_predi_id[4,0,t] = proba[4,0,:].argmax()

        liste_predi_id[0,1,t] = proba[0,1,:].argmax()
        liste_predi_id[1,1,t] = proba[1,1,:].argmax()
        liste_predi_id[2,1,t] = proba[2,1,:].argmax()
        liste_predi_id[3,1,t] = proba[3,1,:].argmax()
        liste_predi_id[4,1,t] = proba[4,1,:].argmax()




    result_area1 = np.zeros((5, 2, temps))
    result_area2 = np.zeros((5, 2, temps))
    result_area4 = np.zeros((5, 2, temps))
    result_area8 = np.zeros((5, 2, temps))
    result_sliding_area = np.zeros((5, 2, temps))
    result_block = np.zeros((5, 2, temps))

    indice = 0

    for t in range(temps):
        if t == liste_t_value[indice]:
            result_area1[:,:,t] = area1max_indices[:,:,indice]
            result_area2[:,:,t] = area2max_indices[:,:,indice]
            result_area4[:,:,t] = area4max_indices[:,:,indice]
            result_area8[:,:,t] = area8max_indices[:,:,indice]
            result_sliding_area[:,:,t] = area_best[:,:,indice]
            result_block[:,:,t] = liste_predi_id[:,:,indice]

            indice += 1

        else:
            result_area1[:,:,t] = result_area1[:,:,t-1]
            result_area2[:,:,t] = result_area2[:,:,t-1]
            result_area4[:,:,t] = result_area4[:,:,t-1]
            result_area8[:,:,t] = result_area8[:,:,t-1]
            result_sliding_area[:,:,t] = result_sliding_area[:,:,t-1]
            result_block[:,:,t] = result_block[:,:,t-1]


    return [result_area1,result_area2,result_area4,result_area8],result_sliding_area,result_block