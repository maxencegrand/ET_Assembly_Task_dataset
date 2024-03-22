import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.widgets import Slider
import os
import time


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

from feature_computation import parsingOneSituation
from low_lvl_naif import low_level_naif
from interpretation import interpretation
from analyse import showComparaisonAlgorithm,analyseSituation,analyseRelease,evaluationBestArea,analyseMethod,goodAreaCoord
from tools import quadrillageRelease,liste_tenon_bloc,saveLog,loadLog


"""
parsingOneSituation does blah blah blah.

Input

method: str correspond a la methode actuellement analyse (mobile ou stationnary)

Output

None
"""
def parsingAllParticipantOneMethode():

    nb_predi = 5

    liste_analyse_methode_grasp_temps = [[[] for _ in range(nb_predi)] for _ in range(2)]
    liste_analyse_methode_release_temps = [[[] for _ in range(nb_predi)] for _ in range(2)]

    total_nb_grasp = [0 for _ in range(2)]
    total_nb_release = [0 for _ in range(2)]

    analyse_zone_release_prediction = [[[0] * nb_predi for _ in range(2)] for _ in range(4)]
    analyse_last_zone_release_prediction = [[[0] * nb_predi for _ in range(2)] for _ in range(4)]
    analyse_zone_total_release_prediction = [[[0] * nb_predi for _ in range(2)] for _ in range(4)]
    liste_analyse_zone_release_temps = [[[[] for _ in range(nb_predi)]  for _ in range(2)] for _ in range(4)]

    analyse_best_zone_release_prediction = [[0] * nb_predi for _ in range(2)]
    analyse_last_best_zone_release_prediction = [[0] * nb_predi for _ in range(2)] 
    analyse_best_zone_total_release_prediction = [[0] * nb_predi for _ in range(2)]
    liste_analyse_best_zone_release_temps = [[[] for _ in range(nb_predi)]  for _ in range(2)]

    X = [[] for _ in range(2)]

    global_analyse_grasp = np.zeros((2,nb_predi,6001))

    nb_analyse = 0

    temps_debut = time.time()

    # On parcours la liste des dossiers correspondant aux participants
    for method_pos,method in enumerate(["mobile", "stationnary"]):
        directory = "../../data/ET_Assembly_Task_dataset/dataset/" + method + "/sitting/"
        for entry in os.scandir(directory):

            # Choix du model : car, house, sc, tb, tc, tsb
            #list_model = ["car", "house", "sc", "tb", "tc", "tsb"]
            list_model = ["car"]

            for model in list_model:

                # verifie que les 2 fichiers existent
                if os.path.exists(
                    str(entry.path) + "/" + model + "/table.csv"
                ) and os.path.exists(str(entry.path) + "/car/states.csv"):

                    print("---------------------------")
                    print("Partcipant :", str(entry.path).split("/")[-1],model, method_pos)

                    # ferme le plot actuel et creer un subplot
                    plt.close()
                    fig, ax = plt.subplots(2, 1)

                    # charge les deux fichiers dans des np.array
                    gaze_point = np.genfromtxt(
                        str(entry.path) + "/" + model + "/table.csv", delimiter=","
                    )
                    world = np.genfromtxt(
                        str(entry.path) + "/" + model + "/states.csv", delimiter=","
                    )
                    
                    (
                        feature,
                        timestamp_action,
                        liste_t_value,

                    ) = parsingOneSituation(gaze_point, world, ax)
                    
                    #X[method_pos].append(feature.tolist())

                    probability = low_level_naif(feature,timestamp_action)

                    area_prediction,area_best_prediction,liste_predi_id = interpretation(probability,timestamp_action,liste_t_value,world)

                    total_nb_grasp[method_pos] = total_nb_grasp[method_pos] + (len(timestamp_action)-2)/2
                    total_nb_release[method_pos] = total_nb_release[method_pos] + (len(timestamp_action)-2)/2
                    
                    nb_bloc = [nb_bloc_1,nb_bloc_2,nb_bloc_4,nb_bloc_8]

                    for position, quadri in enumerate(area_prediction):
                        liste_good_zones = quadrillageRelease(world,nb_bloc[position])
                        for posi,quadr in enumerate(quadri):


                            zone_good_release_prediction,zone_total_release_prediction,last_zone_release_prediction, last_zone_release_temps = analyseRelease(quadr,liste_good_zones,timestamp_action)

                            analyse_last_zone_release_prediction[position][method_pos][posi] += zone_good_release_prediction
                            analyse_zone_total_release_prediction[position][method_pos][posi] += zone_total_release_prediction
                            analyse_zone_release_prediction[position][method_pos][posi] += last_zone_release_prediction
                            liste_analyse_zone_release_temps[position][method_pos][posi] =  liste_analyse_zone_release_temps[position][method_pos][posi] + last_zone_release_temps

                    liste_good_area_coord = goodAreaCoord(world)
                    for posi,predi in enumerate(area_best_prediction):
                        zone_good_release_prediction,zone_total_release_prediction,last_zone_release_prediction, last_zone_release_temps = evaluationBestArea(predi,liste_good_area_coord,timestamp_action)

                        analyse_last_best_zone_release_prediction[method_pos][posi] += zone_good_release_prediction
                        analyse_best_zone_total_release_prediction[method_pos][posi] += zone_total_release_prediction
                        analyse_best_zone_release_prediction[method_pos][posi] += last_zone_release_prediction
                        liste_analyse_best_zone_release_temps[method_pos][posi] =  liste_analyse_best_zone_release_temps[method_pos][posi] + last_zone_release_temps

                    for position, prediction in enumerate(liste_predi_id):
                        # Analyse max min dist
                        (
                            
                            list_time_good_grasp_predi,
                            list_time_good_release_predi,
                            analyse_grasp
                            
                        ) = analyseSituation(world, gaze_point, prediction, timestamp_action)

                        # Mise a jour des variables pour comparaison entre methode

                        liste_analyse_methode_grasp_temps[method_pos][position] = liste_analyse_methode_grasp_temps[method_pos][position] + list_time_good_grasp_predi
                        liste_analyse_methode_release_temps[method_pos][position] = liste_analyse_methode_release_temps[method_pos][position] + list_time_good_release_predi

                        global_analyse_grasp[method_pos][position] = global_analyse_grasp[method_pos][position] + analyse_grasp






        if analyse:
            for position in range(nb_predi):
                print("***")
                print("Predi",position)
                analyseMethod(
                    method,
                    liste_analyse_methode_grasp_temps[method_pos][position],
                    liste_analyse_methode_release_temps[method_pos][position],
                    total_nb_grasp[method_pos],
                )



        #plt.close()
        #plt.plot(np.arange(6001)-3000,100*global_analyse_grasp[method_pos][0]/total_nb_grasp[method_pos])
        #plt.plot(np.arange(6001)-3000,100*global_analyse_grasp[method_pos][1]/total_nb_grasp[method_pos])
        #plt.plot(np.arange(6001)-3000,100*global_analyse_grasp[method_pos][2]/total_nb_grasp[method_pos])
        #plt.plot(np.arange(6001)-3000,100*global_analyse_grasp[method_pos][3]/total_nb_grasp[method_pos])
        #plt.plot(np.arange(6001)-3000,100*global_analyse_grasp[method_pos][4]/total_nb_grasp[method_pos])
        #plt.show()


    # Temps d'arrêt
    temps_fin = time.time()

    # Durée d'exécution en secondes
    duree_execution = temps_fin - temps_debut

    nom_fichier = saveLog(liste_analyse_zone_release_temps,liste_analyse_best_zone_release_temps,liste_analyse_methode_grasp_temps,liste_analyse_methode_release_temps,total_nb_grasp,duree_execution,X)

    









if __name__ == "__main__":
    parsingAllParticipantOneMethode()
