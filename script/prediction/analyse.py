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

    for t in range(1,len(timestamp_action)):

        for time in range(max(0,timestamp_action[t]-3000),min(timestamp_action[-1],timestamp_action[t] + 3001)):
            if (t - 1) % 2 == 0:
                if history_prediction[0][time] == liste_holding[(t - 1) // 2]:
                    analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
            else:
                
                if history_prediction[1][time] in liste_adjacence_release[(t-1)//2]:
                    analyse_release[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_release[time - (timestamp_action[t] - 3000)] += 1


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

    for t in range(1,len(timestamp_action)):
        for time in range(max(0,timestamp_action[t]-3000),min(quadrillage.shape[1],timestamp_action[t] + 3001)):
            if (t - 1) % 2 == 0:
                if quadrillage[0][time] in liste_good_grasp_zones[(t - 1) // 2]:
                    analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
            else:
                if quadrillage[1][time] in liste_good_release_zones[(t-1)//2]:
                    analyse_release[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_release[time - (timestamp_action[t] - 3000)] += 1

    return analyse_grasp, nb_analyse_grasp, analyse_release, nb_analyse_release


def analyseFixeAreaWeak(prediction,liste_good_grasp_zones, liste_good_release_zones,timestamp_action, nb_bloc):

    nb_area_x = int(2*math.sqrt(nb_bloc/2))
    nb_area_y = int(math.sqrt(nb_bloc/2))

    taille = 48 / nb_area_x

    analyse_grasp = np.zeros((6001))
    nb_analyse_grasp = np.zeros((6001))

    analyse_release = np.zeros((6001))
    nb_analyse_release = np.zeros((6001))

    for t in range(1,len(timestamp_action)):

        
        

        for time in range(max(0,timestamp_action[t]-3000),min(prediction.shape[1],timestamp_action[t] + 3001)):
            if (t - 1) % 2 == 0:

                id_predi = prediction[0][time]


                x0_area = (id_predi // nb_area_y) * taille
                y0_area = (id_predi % nb_area_y) * taille
                x2_area = ((id_predi // nb_area_y) + 1) * taille
                y2_area = ((id_predi % nb_area_y) + 1) * taille
                
                x0_block = round((48*liste_good_grasp_zones[(t - 1) // 2][0]/largeur))
                y0_block = round((24*liste_good_grasp_zones[(t - 1) // 2][1]/hauteur))
                x1_block = round((48*liste_good_grasp_zones[(t - 1) // 2][2]/largeur))
                y1_block = round((24*liste_good_grasp_zones[(t - 1) // 2][3]/hauteur))
                x2_block = round((48*liste_good_grasp_zones[(t - 1) // 2][4]/largeur))
                y2_block = round((24*liste_good_grasp_zones[(t - 1) // 2][5]/hauteur))
                x3_block = round((48*liste_good_grasp_zones[(t - 1) // 2][6]/largeur))
                y3_block = round((24*liste_good_grasp_zones[(t - 1) // 2][7]/hauteur))

                if (
                   (x0_area <= x0_block and x0_block < x2_area and y0_area <= y0_block and y0_block < y2_area)     
                    or (x0_area < x1_block and x1_block <= x2_area and y0_area <= y1_block and y1_block < y2_area) 
                    or (x0_area < x2_block and x2_block <= x2_area and y0_area < y2_block and y2_block <= y2_area) 
                    or (x0_area <= x3_block and x3_block < x2_area and y0_area < y3_block and y3_block <= y2_area) 
                ):
                    analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_grasp[time - (timestamp_action[t] - 3000)] += 1


            else:
                id_predi = prediction[1][time]

                x0_area = (id_predi // nb_area_y) * taille
                y0_area = (id_predi % nb_area_y) * taille
                x2_area = ((id_predi // nb_area_y) + 1) * taille
                y2_area = ((id_predi % nb_area_y) + 1) * taille

                x0_block = round((48*liste_good_release_zones[(t - 1) // 2][0]/largeur))
                y0_block = round((24*liste_good_release_zones[(t - 1) // 2][1]/hauteur))
                x1_block = round((48*liste_good_release_zones[(t - 1) // 2][2]/largeur))
                y1_block = round((24*liste_good_release_zones[(t - 1) // 2][3]/hauteur))
                x2_block = round((48*liste_good_release_zones[(t - 1) // 2][4]/largeur))
                y2_block = round((24*liste_good_release_zones[(t - 1) // 2][5]/hauteur))
                x3_block = round((48*liste_good_release_zones[(t - 1) // 2][6]/largeur))
                y3_block = round((24*liste_good_release_zones[(t - 1) // 2][7]/hauteur))


                #print("t",t)
                #print(liste_good_release_zones[(t - 1) // 2])
                #print("Bloc:")
                #print(x0_block,y0_block)
                #print(x1_block,y1_block)
                #print(x2_block,y2_block)
                #print(x3_block,y3_block)
                #print("Area:")
                #print(x0_area,y0_area)
                #print(x2_area,y2_area)

                if (
                   (x0_area <= x0_block and x0_block < x2_area and y0_area <= y0_block and y0_block < y2_area)     
                    or (x0_area < x1_block and x1_block <= x2_area and y0_area <= y1_block and y1_block < y2_area) 
                    or (x0_area < x2_block and x2_block <= x2_area and y0_area < y2_block and y2_block <= y2_area) 
                    or (x0_area <= x3_block and x3_block < x2_area and y0_area < y3_block and y3_block <= y2_area)
                ):
                    #print("Ok")
                    analyse_release[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_release[time - (timestamp_action[t] - 3000)] += 1


    return analyse_grasp, nb_analyse_grasp, analyse_release, nb_analyse_release

def analyseFixeAreaStrong(prediction,liste_good_grasp_zones, liste_good_release_zones,timestamp_action, nb_bloc):

    nb_area_x = int(2*math.sqrt(nb_bloc/2))
    nb_area_y = int(math.sqrt(nb_bloc/2))

    taille = 48 / nb_area_x

    analyse_grasp = np.zeros((6001))
    nb_analyse_grasp = np.zeros((6001))

    analyse_release = np.zeros((6001))
    nb_analyse_release = np.zeros((6001))

    for t in range(1,len(timestamp_action)):

        
        

        for time in range(max(0,timestamp_action[t]-3000),min(prediction.shape[1],timestamp_action[t] + 3001)):
            if (t - 1) % 2 == 0:

                id_predi = prediction[0][time]

                x0_area = (id_predi // nb_area_y) * taille
                y0_area = (id_predi % nb_area_y) * taille
                x2_area = ((id_predi // nb_area_y) + 1) * taille
                y2_area = ((id_predi % nb_area_y) + 1) * taille
                
                x0_block = round((48*liste_good_grasp_zones[(t - 1) // 2][0]/largeur))
                y0_block = round((24*liste_good_grasp_zones[(t - 1) // 2][1]/hauteur))
                x1_block = round((48*liste_good_grasp_zones[(t - 1) // 2][2]/largeur))
                y1_block = round((24*liste_good_grasp_zones[(t - 1) // 2][3]/hauteur))
                x2_block = round((48*liste_good_grasp_zones[(t - 1) // 2][4]/largeur))
                y2_block = round((24*liste_good_grasp_zones[(t - 1) // 2][5]/hauteur))
                x3_block = round((48*liste_good_grasp_zones[(t - 1) // 2][6]/largeur))
                y3_block = round((24*liste_good_grasp_zones[(t - 1) // 2][7]/hauteur))

                if (
                   (x0_area <= x0_block and x0_block < x2_area and y0_area <= y0_block and y0_block < y2_area)     
                    and (x0_area <= x1_block and x1_block <= x2_area and y0_area <= y1_block and y1_block <= y2_area) 
                    and (x0_area <= x2_block and x2_block <= x2_area and y0_area <= y2_block and y2_block <= y2_area) 
                    and (x0_area <= x3_block and x3_block <= x2_area and y0_area <= y3_block and y3_block <= y2_area) 
                ):
                    analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_grasp[time - (timestamp_action[t] - 3000)] += 1

            else:
                id_predi = prediction[1][time]

                x0_area = (id_predi // nb_area_y) * taille
                y0_area = (id_predi % nb_area_y) * taille
                x2_area = ((id_predi // nb_area_y) + 1) * taille
                y2_area = ((id_predi % nb_area_y) + 1) * taille

                x0_block = round((48*liste_good_release_zones[(t - 1) // 2][0]/largeur))
                y0_block = round((24*liste_good_release_zones[(t - 1) // 2][1]/hauteur))
                x1_block = round((48*liste_good_release_zones[(t - 1) // 2][2]/largeur))
                y1_block = round((24*liste_good_release_zones[(t - 1) // 2][3]/hauteur))
                x2_block = round((48*liste_good_release_zones[(t - 1) // 2][4]/largeur))
                y2_block = round((24*liste_good_release_zones[(t - 1) // 2][5]/hauteur))
                x3_block = round((48*liste_good_release_zones[(t - 1) // 2][6]/largeur))
                y3_block = round((24*liste_good_release_zones[(t - 1) // 2][7]/hauteur))

                if (
                   (x0_area <= x0_block and x0_block <= x2_area and y0_area <= y0_block and y0_block <= y2_area)     
                    and (x0_area <= x1_block and x1_block <= x2_area and y0_area <= y1_block and y1_block <= y2_area) 
                    and (x0_area <= x2_block and x2_block <= x2_area and y0_area <= y2_block and y2_block <= y2_area) 
                    and (x0_area <= x3_block and x3_block <= x2_area and y0_area <= y3_block and y3_block <= y2_area) 
                ):
                    analyse_release[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_release[time - (timestamp_action[t] - 3000)] += 1

    return analyse_grasp, nb_analyse_grasp, analyse_release, nb_analyse_release


def analyseSlidingAreaWeak(prediction,liste_good_grasp_zones, liste_good_release_zones,timestamp_action, nb_bloc):

    nb_area_x = int(2*math.sqrt(nb_bloc/2))
    nb_area_y = int(math.sqrt(nb_bloc/2))

    taille = 48 / nb_area_x


    analyse_grasp = np.zeros((6001))
    nb_analyse_grasp = np.zeros((6001))

    analyse_release = np.zeros((6001))
    nb_analyse_release = np.zeros((6001))

    for t in range(1,len(timestamp_action)):

        
        

        for time in range(max(0,timestamp_action[t]-3000),min(prediction.shape[1],timestamp_action[t] + 3001)):
            if (t - 1) % 2 == 0:

                id_predi = prediction[0][time]

                x0_area = (id_predi // round(math.sqrt( nb_area_1/2)))
                y0_area = (id_predi % round(math.sqrt(nb_area_1/2)))
                x2_area = ((id_predi // round(math.sqrt(nb_area_1/2))) + taille)
                y2_area = ((id_predi % round(math.sqrt(nb_area_1/2))) + taille)
                
                x0_block = round((48*liste_good_grasp_zones[(t - 1) // 2][0]/largeur))
                y0_block = round((24*liste_good_grasp_zones[(t - 1) // 2][1]/hauteur))
                x1_block = round((48*liste_good_grasp_zones[(t - 1) // 2][2]/largeur))
                y1_block = round((24*liste_good_grasp_zones[(t - 1) // 2][3]/hauteur))
                x2_block = round((48*liste_good_grasp_zones[(t - 1) // 2][4]/largeur))
                y2_block = round((24*liste_good_grasp_zones[(t - 1) // 2][5]/hauteur))
                x3_block = round((48*liste_good_grasp_zones[(t - 1) // 2][6]/largeur))
                y3_block = round((24*liste_good_grasp_zones[(t - 1) // 2][7]/hauteur))

                if (
                   (x0_area <= x0_block and x0_block < x2_area and y0_area <= y0_block and y0_block < y2_area)     
                    or (x0_area < x1_block and x1_block <= x2_area and y0_area <= y1_block and y1_block < y2_area) 
                    or (x0_area < x2_block and x2_block <= x2_area and y0_area < y2_block and y2_block <= y2_area) 
                    or (x0_area <= x3_block and x3_block < x2_area and y0_area < y3_block and y3_block <= y2_area) 
                ):
                    analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_grasp[time - (timestamp_action[t] - 3000)] += 1


            else:
                id_predi = prediction[1][time]

                x0_area = (id_predi // round(math.sqrt( nb_area_1/2)))
                y0_area = (id_predi % round(math.sqrt(nb_area_1/2)))
                x2_area = ((id_predi // round(math.sqrt(nb_area_1/2))) + taille)
                y2_area = ((id_predi % round(math.sqrt(nb_area_1/2))) + taille)

                x0_block = round((48*liste_good_release_zones[(t - 1) // 2][0]/largeur))
                y0_block = round((24*liste_good_release_zones[(t - 1) // 2][1]/hauteur))
                x1_block = round((48*liste_good_release_zones[(t - 1) // 2][2]/largeur))
                y1_block = round((24*liste_good_release_zones[(t - 1) // 2][3]/hauteur))
                x2_block = round((48*liste_good_release_zones[(t - 1) // 2][4]/largeur))
                y2_block = round((24*liste_good_release_zones[(t - 1) // 2][5]/hauteur))
                x3_block = round((48*liste_good_release_zones[(t - 1) // 2][6]/largeur))
                y3_block = round((24*liste_good_release_zones[(t - 1) // 2][7]/hauteur))

                if (
                   (x0_area <= x0_block and x0_block < x2_area and y0_area <= y0_block and y0_block < y2_area)     
                    or (x0_area < x1_block and x1_block <= x2_area and y0_area <= y1_block and y1_block < y2_area) 
                    or (x0_area < x2_block and x2_block <= x2_area and y0_area < y2_block and y2_block <= y2_area) 
                    or (x0_area <= x3_block and x3_block < x2_area and y0_area < y3_block and y3_block <= y2_area) 
                ):
                    analyse_release[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_release[time - (timestamp_action[t] - 3000)] += 1

    return analyse_grasp, nb_analyse_grasp, analyse_release, nb_analyse_release

def analyseSlidingAreaStrong(prediction,liste_good_grasp_zones, liste_good_release_zones,timestamp_action, nb_bloc):

    nb_area_x = int(2*math.sqrt(nb_bloc/2))
    nb_area_y = int(math.sqrt(nb_bloc/2))

    taille = 48 / nb_area_x

    analyse_grasp = np.zeros((6001))
    nb_analyse_grasp = np.zeros((6001))

    analyse_release = np.zeros((6001))
    nb_analyse_release = np.zeros((6001))

    for t in range(1,len(timestamp_action)):

        
        

        for time in range(max(0,timestamp_action[t]-3000),min(prediction.shape[1],timestamp_action[t] + 3001)):
            if (t - 1) % 2 == 0:

                id_predi = prediction[0][time]

                x0_area = (id_predi // round(math.sqrt( nb_area_1/2)))
                y0_area = (id_predi % round(math.sqrt(nb_area_1/2)))
                x2_area = ((id_predi // round(math.sqrt(nb_area_1/2))) + taille)
                y2_area = ((id_predi % round(math.sqrt(nb_area_1/2))) + taille)
                
                x0_block = round((48*liste_good_grasp_zones[(t - 1) // 2][0]/largeur))
                y0_block = round((24*liste_good_grasp_zones[(t - 1) // 2][1]/hauteur))
                x1_block = round((48*liste_good_grasp_zones[(t - 1) // 2][2]/largeur))
                y1_block = round((24*liste_good_grasp_zones[(t - 1) // 2][3]/hauteur))
                x2_block = round((48*liste_good_grasp_zones[(t - 1) // 2][4]/largeur))
                y2_block = round((24*liste_good_grasp_zones[(t - 1) // 2][5]/hauteur))
                x3_block = round((48*liste_good_grasp_zones[(t - 1) // 2][6]/largeur))
                y3_block = round((24*liste_good_grasp_zones[(t - 1) // 2][7]/hauteur))

                if (
                   (x0_area <= x0_block and x0_block < x2_area and y0_area <= y0_block and y0_block < y2_area)     
                    and (x0_area <= x1_block and x1_block <= x2_area and y0_area <= y1_block and y1_block <= y2_area) 
                    and (x0_area <= x2_block and x2_block <= x2_area and y0_area <= y2_block and y2_block <= y2_area) 
                    and (x0_area <= x3_block and x3_block <= x2_area and y0_area <= y3_block and y3_block <= y2_area) 
                ):
                    analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_grasp[time - (timestamp_action[t] - 3000)] += 1

            else:
                id_predi = prediction[1][time]

                x0_area = (id_predi // round(math.sqrt( nb_area_1/2)))
                y0_area = (id_predi % round(math.sqrt( nb_area_1/2)))
                x2_area = ((id_predi // round(math.sqrt( nb_area_1/2))) + taille)
                y2_area = ((id_predi % round(math.sqrt( nb_area_1/2))) + taille)

                x0_block = round((48*liste_good_release_zones[(t - 1) // 2][0]/largeur))
                y0_block = round((24*liste_good_release_zones[(t - 1) // 2][1]/hauteur))
                x1_block = round((48*liste_good_release_zones[(t - 1) // 2][2]/largeur))
                y1_block = round((24*liste_good_release_zones[(t - 1) // 2][3]/hauteur))
                x2_block = round((48*liste_good_release_zones[(t - 1) // 2][4]/largeur))
                y2_block = round((24*liste_good_release_zones[(t - 1) // 2][5]/hauteur))
                x3_block = round((48*liste_good_release_zones[(t - 1) // 2][6]/largeur))
                y3_block = round((24*liste_good_release_zones[(t - 1) // 2][7]/hauteur))

                if (
                   (x0_area <= x0_block and x0_block <= x2_area and y0_area <= y0_block and y0_block <= y2_area)     
                    and (x0_area <= x1_block and x1_block <= x2_area and y0_area <= y1_block and y1_block <= y2_area) 
                    and (x0_area <= x2_block and x2_block <= x2_area and y0_area <= y2_block and y2_block <= y2_area) 
                    and (x0_area <= x3_block and x3_block <= x2_area and y0_area <= y3_block and y3_block <= y2_area) 
                ):
                    analyse_release[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_release[time - (timestamp_action[t] - 3000)] += 1

    return analyse_grasp, nb_analyse_grasp, analyse_release, nb_analyse_release









def trueSemantic(world,fig,level):
    if level == 0:
        liste_zone = [array_zone_table]
    if level == 1:
        liste_zone = [array_zone_left,array_zone_middle,array_zone_right]
    if level == 2:
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

    result_zone = np.zeros((world.shape[0]-2))
    for i in range(1, world.shape[0]-1):
        for indice in range(24):
            if world[i, 10 * indice + 10] == 1:

                x0 = (world[i, 10 * indice + 1] * 48) / 76
                y0 = (world[i, 10 * indice + 2] * 48) / 76
                x2 = (world[i, 10 * indice + 5] * 48) / 76
                y2 = (world[i, 10 * indice + 6] * 48) / 76

                x_mean = (x0 + x2)/2
                y_mean = (y0 + y2)/2

                list_dist = np.zeros((len(liste_zone)))
                for zone_id,zone in enumerate(liste_zone):
                    x_centre_zone = (zone[1,0] + zone[1,2])/2
                    y_centre_zone = (zone[1,1] + zone[1,3])/2


                    dist = math.sqrt((x_mean - x_centre_zone)**2 + (y_mean - y_centre_zone)**2)
                    list_dist[zone_id] = dist


                good_zone = list_dist.argmin()

                result_zone[i - 2] = good_zone


                x0 = (world[i + 1, 10 * indice + 1] * 48) / 76
                y0 = (world[i + 1, 10 * indice + 2] * 48) / 76
                x2 = (world[i + 1, 10 * indice + 5] * 48) / 76
                y2 = (world[i + 1, 10 * indice + 6] * 48) / 76

                x_mean = (x0 + x2)/2
                y_mean = (y0 + y2)/2

                list_dist = np.zeros((len(liste_zone)))
                for zone_id,zone in enumerate(liste_zone):
                    x_centre_zone = (zone[1,0] + zone[1,2])/2
                    y_centre_zone = (zone[1,1] + zone[1,3])/2


                    dist = math.sqrt((x_mean - x_centre_zone)**2 + (y_mean - y_centre_zone)**2)
                    list_dist[zone_id] = dist

                good_zone = list_dist.argmin()

                result_zone[i - 1] = good_zone

    return result_zone












def analyseSemantic(world, history_prediction,timestamp_action, fig, level):
    

    # Declaration des variables
    liste_semantic = trueSemantic(world,fig, level)  

    analyse_grasp = np.zeros((6001))
    nb_analyse_grasp = np.zeros((6001))

    analyse_release = np.zeros((6001))
    nb_analyse_release = np.zeros((6001))

    for t in range(1,len(timestamp_action)):

        for time in range(max(0,timestamp_action[t]-3000),min(timestamp_action[-1],timestamp_action[t] + 3001)):
            if (t - 1) % 2 == 0:
                if history_prediction[0][time] == liste_semantic[t - 1]:
                    analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
            else:
                
                if history_prediction[1][time] == liste_semantic[t - 1]:
                    analyse_release[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_release[time - (timestamp_action[t] - 3000)] += 1

    return (
        analyse_grasp,
        nb_analyse_grasp,
        analyse_release,
        nb_analyse_release
    )




def trueSemanticBis(world,fig,level):


    
    if level == 0:
        liste_zone = [[array_zone_table]]
    elif level == 1:
        liste_zone = [[array_zone_left],[array_zone_middle],[array_zone_right]]
    elif level == 2:
        liste_zone = [[array_zone_blue],[array_zone_red],[array_zone_green],[array_zone_yellow]]
        if fig == "car":
            liste_zone.append([array_zone_car])
        if fig == "house":
            liste_zone.append([array_zone_house])
        if fig == "sc":
            liste_zone.append([array_zone_sc])
        if fig == "tb":
            liste_zone.append([array_zone_tb])
        if fig == "tc":
            liste_zone.append([array_zone_tc])
        if fig == "tsb":
            liste_zone.append([array_zone_tsb])
    #Zone semantique 1bis
    else:
        liste_zone = [[array_zone_left,array_zone_right],[array_zone_middle]]
    
    result_zone = np.zeros((world.shape[0]-2)) - 1

    for i in range(1, world.shape[0]-1):
        for indice in range(24):
            if world[i, 10 * indice + 10] == 1:

                x0 = round((world[i, 10 * indice + 1] * 48) / 76)
                y0 = round((world[i, 10 * indice + 2] * 48) / 76)
                x2 = round((world[i, 10 * indice + 5] * 48) / 76)
                y2 = round((world[i, 10 * indice + 6] * 48) / 76)

                x_mean = (x0 + x2)/2
                y_mean = (y0 + y2)/2

                for zones_id,zones in enumerate(liste_zone):
                    for zone_id,zone in enumerate(zones):

                        
                        if zone[1,0] <= x0 \
                            and x0 <= zone[1,2]\
                            and zone[1,1] <= y0\
                            and y0 <= zone[1,3]\
                            and zone[1,0] <= x2\
                            and x2 <= zone[1,2]\
                            and zone[1,1] <= y2\
                            and y2 <= zone[1,3]:

                            result_zone[i - 2] = zones_id




                x0 = round((world[i + 1, 10 * indice + 1] * 48) / 76)
                y0 = round((world[i + 1, 10 * indice + 2] * 48) / 76)
                x2 = round((world[i + 1, 10 * indice + 5] * 48) / 76)
                y2 = round((world[i + 1, 10 * indice + 6] * 48) / 76)

                x_mean = (x0 + x2)/2
                y_mean = (y0 + y2)/2

                for zones_id,zones in enumerate(liste_zone):
                    for zone_id,zone in enumerate(zones):
                        if zone[1,0] <= x0 \
                            and x0 <= zone[1,2]\
                            and zone[1,1] <= y0\
                            and y0 <= zone[1,3]\
                            and zone[1,0] <= x2\
                            and x2 <= zone[1,2]\
                            and zone[1,1] <= y2\
                            and y2 <= zone[1,3]:
                            
                            result_zone[i - 1] = zones_id

    return result_zone

def analyseSemanticBis(world, history_prediction,timestamp_action, fig, level):
    

    # Declaration des variables
    liste_semantic = trueSemanticBis(world,fig,level)
    analyse_grasp = np.zeros((6001))
    nb_analyse_grasp = np.zeros((6001))

    analyse_release = np.zeros((6001))
    nb_analyse_release = np.zeros((6001))

    for t in range(1,len(timestamp_action)):

        for time in range(max(0,timestamp_action[t]-3000),min(timestamp_action[-1],timestamp_action[t] + 3001)):
            if (t - 1) % 2 == 0:
                if history_prediction[0][time] == liste_semantic[t - 1]:
                    analyse_grasp[time - (timestamp_action[t] - 3000)] += 1

                nb_analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
            else:
                
                if history_prediction[1][time] == liste_semantic[t - 1]:
                    analyse_release[time - (timestamp_action[t] - 3000)] += 1
                nb_analyse_release[time - (timestamp_action[t] - 3000)] += 1

    return (
        analyse_grasp,
        nb_analyse_grasp,
        analyse_release,
        nb_analyse_release
    )




def analyseNorme(history_norme,timestamp_action):
    
    analyse_grasp = np.zeros((6001))
    nb_analyse_grasp = np.zeros((6001))

    analyse_release = np.zeros((6001))
    nb_analyse_release = np.zeros((6001))

    for t in range(1,len(timestamp_action)):

        for time in range(max(0,timestamp_action[t]-3000),min(timestamp_action[-1],timestamp_action[t] + 3001)):
            if (t - 1) % 2 == 0:

                analyse_grasp[time - (timestamp_action[t] - 3000)] += history_norme[0,time]
                nb_analyse_grasp[time - (timestamp_action[t] - 3000)] += 1
            else:
                
                analyse_release[time - (timestamp_action[t] - 3000)] += history_norme[1,time]
                nb_analyse_release[time - (timestamp_action[t] - 3000)] += 1

    return (
        analyse_grasp,
        nb_analyse_grasp,
        analyse_release,
        nb_analyse_release
    )














def evaluationBestArea(prediction, liste_good_grasp_area, liste_good_release_area, timestamp_action):

    analyse_grasp = np.zeros((6001))
    nb_analyse_grasp = np.zeros((6001))

    analyse_release = np.zeros((6001))
    nb_analyse_release = np.zeros((6001))

    for t in range(1,len(timestamp_action)):
        for time in range(max(0,timestamp_action[t]-3000),min(timestamp_action[-1]-1,timestamp_action[t] + 3001)):

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

