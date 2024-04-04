import numpy as np
import math
import os
import time
from datetime import datetime

import matplotlib.pyplot as plt


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

from feature_computation import parsingOneSituation
from low_lvl_naif import low_level_naif
from interpretation import interpretation
from analyse import analyseSituation,analyseRelease,evaluationBestArea,analyseMethod,goodReleaseAreaCoord,goodGraspAreaCoord
from tools import quadrillageRelease,quadrillageGrasp,liste_tenon_bloc,saveLog


"""
parsingOneSituation parcours la liste des participants, et pour chaque type de capteur (mobile/fixe), pour chaque participant, pour chaque figure, fait les differentes etapes menant aux predictions .

Input

None

Output

None
"""
def parsingAllParticipantOneMethode():

    # Obtention de la date et de l'heure actuelle
    date_heure_actuelle = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Nom du fichier avec la date et l'heure
    nom_fichier = f"logs/{date_heure_actuelle}"

    nb_predi = 5

    liste_analyse_methode_grasp_temps = [[[] for _ in range(nb_predi)] for _ in range(2)]
    liste_analyse_methode_release_temps = [[[] for _ in range(nb_predi)] for _ in range(2)]

    total_nb_grasp = [0 for _ in range(2)]
    total_nb_release = [0 for _ in range(2)]

    global_analyse_area_grasp = np.zeros((4,2,nb_predi,6001))
    global_nb_analyse_area_grasp = np.zeros((4,2,6001))
    global_analyse_area_release = np.zeros((4,2,nb_predi,6001))
    global_nb_analyse_area_release = np.zeros((4,2,6001))

    global_analyse_sliding_area_grasp = np.zeros((2,nb_predi,6001))
    global_nb_analyse_sliding_area_grasp = np.zeros((2,6001))
    global_analyse_sliding_area_release = np.zeros((2,nb_predi,6001))
    global_nb_analyse_sliding_area_release = np.zeros((2,6001))

    global_analyse_grasp = np.zeros((2,nb_predi,6001))
    global_nb_analyse_grasp = np.zeros((2,6001))
    global_analyse_release = np.zeros((2,nb_predi,6001))
    global_nb_analyse_release = np.zeros((2,6001))

    nb_analyse = 0

    duree_execution = [[],[]]

    # On parcours la liste des dossiers correspondant aux participants
    for method_pos,method in enumerate(["mobile", "stationnary"]):
        directory = "../../dataset/" + method + "/sitting/"
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

                    temps_debut = time.time()

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

                    ) = parsingOneSituation(gaze_point, world)

                    probability = low_level_naif(feature,timestamp_action)

                    area_prediction,area_best_prediction,liste_predi_id = interpretation(probability,timestamp_action,liste_t_value,world)

                    temps_fin = time.time()

                    # Durée d'exécution en secondes
                    delta_temps = temps_fin - temps_debut

                    duree_execution[method_pos].append(delta_temps)

                    total_nb_grasp[method_pos] = total_nb_grasp[method_pos] + (len(timestamp_action)-2)/2
                    total_nb_release[method_pos] = total_nb_release[method_pos] + (len(timestamp_action)-2)/2
                    
                    nb_bloc = [nb_bloc_1,nb_bloc_2,nb_bloc_4,nb_bloc_8]

                    for position, quadri in enumerate(area_prediction):
                        liste_good_release_zones = quadrillageRelease(world,nb_bloc[position])
                        liste_good_grasp_zones = quadrillageGrasp(world,nb_bloc[position])
                        for posi,quadr in enumerate(quadri):

                            (
                            analyse_area_grasp,
                            nb_analyse_area_grasp,
                            analyse_area_release,
                            nb_analyse_area_release
                            ) = analyseRelease(quadr, liste_good_grasp_zones, liste_good_release_zones,timestamp_action)

                            global_analyse_area_grasp[position][method_pos][posi] += analyse_area_grasp
                            global_analyse_area_release[position][method_pos][posi] += analyse_area_release

                        global_nb_analyse_area_grasp[position][method_pos] += nb_analyse_area_grasp
                        global_nb_analyse_area_release[position][method_pos] += nb_analyse_area_release

                    liste_good_release_area_coord = goodReleaseAreaCoord(world)
                    liste_good_grasp_area_coord = goodGraspAreaCoord(world)
                    for posi,predi in enumerate(area_best_prediction):
                        (
                        analyse_area_grasp,
                        nb_analyse_area_grasp,
                        analyse_area_release,
                        nb_analyse_area_release
                        ) = evaluationBestArea(predi,liste_good_grasp_area_coord,liste_good_release_area_coord,timestamp_action)

                        global_analyse_sliding_area_grasp[method_pos][posi] += analyse_area_grasp
                        global_analyse_sliding_area_release[method_pos][posi] += analyse_area_release

                    global_nb_analyse_sliding_area_grasp[method_pos] += nb_analyse_area_grasp
                    global_nb_analyse_sliding_area_release[method_pos] += nb_analyse_area_release

                    for position, prediction in enumerate(liste_predi_id):
                        # Analyse max min dist
                        (

                            analyse_grasp,
                            nb_analyse_grasp,
                            analyse_release,
                            nb_analyse_release,
                        ) = analyseSituation(world, prediction, timestamp_action)
                        
                        global_analyse_grasp[method_pos][position] = global_analyse_grasp[method_pos][position] + analyse_grasp
                        global_analyse_release[method_pos][position] = global_analyse_release[method_pos][position] + analyse_release

                    global_nb_analyse_grasp[method_pos] += nb_analyse_grasp
                    global_nb_analyse_release[method_pos] += nb_analyse_release


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


    results = np.zeros((12,2,nb_predi,6001))

    results[0] = global_analyse_area_grasp[0]
    results[1] = global_analyse_area_grasp[1]
    results[2] = global_analyse_area_grasp[2]
    results[3] = global_analyse_area_grasp[3]
    results[4] = global_analyse_area_release[0]
    results[5] = global_analyse_area_release[1]
    results[6] = global_analyse_area_release[2]
    results[7] = global_analyse_area_release[3]
    results[8] = global_analyse_sliding_area_grasp
    results[9] = global_analyse_sliding_area_release
    results[10] = global_analyse_grasp
    results[11] = global_analyse_release

    nb_prediction = np.zeros((12,2,6001))

    nb_prediction[0] = global_nb_analyse_area_grasp[0]
    nb_prediction[1] = global_nb_analyse_area_grasp[1]
    nb_prediction[2] = global_nb_analyse_area_grasp[2]
    nb_prediction[3] = global_nb_analyse_area_grasp[3]
    nb_prediction[4] = global_nb_analyse_area_release[0]
    nb_prediction[5] = global_nb_analyse_area_release[1]
    nb_prediction[6] = global_nb_analyse_area_release[2]
    nb_prediction[7] = global_nb_analyse_area_release[3]
    nb_prediction[8] = global_nb_analyse_sliding_area_grasp
    nb_prediction[9] = global_nb_analyse_sliding_area_release
    nb_prediction[10] = global_nb_analyse_grasp
    nb_prediction[11] = global_nb_analyse_release

    nom_fichier = saveLog(nom_fichier,results,nb_prediction,duree_execution)




if __name__ == "__main__":
    parsingAllParticipantOneMethode()
