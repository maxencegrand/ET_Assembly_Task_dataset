import numpy as np
import math
import os
import time
from datetime import datetime

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

from feature_computation import parsingOneSituation
from low_lvl_naif import low_level_naif
from interpretation import interpretation
from analyse import analyseSituation,analyseRelease,evaluationBestArea,analyseMethod,goodReleaseAreaCoord,goodGraspAreaCoord
from tools import quadrillageRelease,quadrillageGrasp,liste_tenon_bloc,saveLog,listeTimneAction,CurrentWorld,savingTime,savingFeature,savingProba,savingInterpretation


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
    nom_dossier = f"logs/{date_heure_actuelle}"

    os.mkdir(nom_dossier)

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
    #for method_pos,method in enumerate(["mobile"]):    
        directory = "../../dataset/" + method + "/sitting/"
        for entry in os.scandir(directory):

            # Choix du model : car, house, sc, tb, tc, tsb
            list_model = ["car", "house", "sc", "tb", "tc", "tsb"]
            #list_model = ["car"]

            for model in list_model:

                # verifie que les 2 fichiers existent
                if os.path.exists(
                    str(entry.path) + "/" + model + "/table.csv"
                ) and os.path.exists(str(entry.path) + "/car/states.csv"):

                    print("---------------------------")
                    print("Partcipant :", str(entry.path).split("/")[-1],model, method_pos)

                    

                    # charge les deux fichiers dans des np.array
                    gaze_point = np.genfromtxt(
                        str(entry.path) + "/" + model + "/table.csv", delimiter=","
                    )

                    world = np.genfromtxt(
                        str(entry.path) + "/" + model + "/states.csv", delimiter=","
                    )
                    
                    duree = int(max(world[-1,0], gaze_point[-1,0] ) - min(world[1,0], gaze_point[1,0] ) ) + 1

                    nb_gaze = gaze_point.shape[0] - 1

                    timestamp_action = listeTimneAction(world)
                    

                    all_feature = np.zeros((5, nb_gaze, nb_area_1))
                    probability_score = np.zeros((5, 2, nb_gaze, nb_area_1))
                    probability = np.zeros((5, 2, nb_gaze, nb_area_1))

                    t_init = world[1,0]

                    indice = 0

                    liste_t_value = []

                    liste_temps_exec = []

                    temp_area1 = np.zeros((5,2,nb_gaze))
                    temp_area2 = np.zeros((5,2,nb_gaze))
                    temp_area4 = np.zeros((5,2,nb_gaze))
                    temp_area8 = np.zeros((5,2,nb_gaze))

                    temp_area_sliding = np.zeros((5,2,nb_gaze))

                    temp_block = np.zeros((5,2,nb_gaze))

                    for i in range(nb_gaze):
                        temps_debut = time.time()

                        current_world = CurrentWorld(gaze_point[i, 0], world)

                        gaze_value = gaze_point [i + 1]
                        t = gaze_value[0] - t_init
                        liste_t_value.append(t)

                        (
                        feature,
                        ) = parsingOneSituation(gaze_value)

                        all_feature[:,i,:] = feature

                        if i > 0:
                            past_probability_score = probability_score[:,:,i-1,:]
                        else:
                            past_probability_score = probability_score[:,:,i,:]
                            
                        new_probability,new_probability_score,new_indice = low_level_naif(feature,t,timestamp_action,indice,past_probability_score)
                        
                        probability[:,:,i,:] = new_probability
                        probability_score[:,:,i,:] = new_probability_score


                        area1max_indices,area2max_indices,area4max_indices,area8max_indices,area_best,liste_predi_id = interpretation(new_probability,new_indice,world,)
                        
                        temp_area1[:,:,i] = area1max_indices
                        temp_area2[:,:,i] = area2max_indices
                        temp_area4[:,:,i] = area4max_indices
                        temp_area8[:,:,i] = area8max_indices

                        temp_area_sliding[:,:,i] = area_best

                        temp_block[:,:,i] = liste_predi_id

                        indice = new_indice
                        
                        temps_fin = time.time()
                        diff_temps = temps_fin - temps_debut
                        liste_temps_exec.append(diff_temps)

                    participant = method+"_sitting_"+str(entry.path).split("/")[-1]+"_"+model

                    savingTime(nom_dossier,participant,liste_temps_exec)
                    savingFeature(nom_dossier,participant,all_feature)
                    savingProba(nom_dossier,participant,probability)
                    savingInterpretation(nom_dossier,participant,temp_area1,temp_area2,temp_area4,temp_area8,temp_area_sliding,temp_block)

                    for k in range(nb_gaze):
                        if not np.array_equal(temp_area1[:,:,k], probability.argmax(axis=3)[:,:,k]):
                            print("Problem :",k)
                    
                    result_area1 = np.zeros((5, 2, duree))
                    result_area2 = np.zeros((5, 2, duree))
                    result_area4 = np.zeros((5, 2, duree))
                    result_area8 = np.zeros((5, 2, duree))
                    result_sliding_area = np.zeros((5, 2, duree))
                    result_block = np.zeros((5, 2, duree))

                    time_indice = 0

                    for t in range(duree):
                        if time_indice < len(liste_t_value) and t == liste_t_value[time_indice]:

                            result_area1[:,:,t] = temp_area1[:,:,time_indice]
                            result_area2[:,:,t] = temp_area2[:,:,time_indice]
                            result_area4[:,:,t] = temp_area4[:,:,time_indice]
                            result_area8[:,:,t] = temp_area8[:,:,time_indice]
                            result_sliding_area[:,:,t] = temp_area_sliding[:,:,time_indice]
                            result_block[:,:,t] = temp_block[:,:,time_indice]

                            time_indice += 1

                        else:
                            result_area1[:,:,t] = result_area1[:,:,t-1]
                            result_area2[:,:,t] = result_area2[:,:,t-1]
                            result_area4[:,:,t] = result_area4[:,:,t-1]
                            result_area8[:,:,t] = result_area8[:,:,t-1]
                            result_sliding_area[:,:,t] = result_sliding_area[:,:,t-1]
                            result_block[:,:,t] = result_block[:,:,t-1]

                    area_prediction = [result_area1,result_area2,result_area4,result_area8]
                    area_best_prediction = result_sliding_area
                    block_prediction = result_block

                    # Durée d'exécution en secondes
                    delta_temps = temps_fin - temps_debut

                    duree_execution[method_pos].append(delta_temps)

                    total_nb_grasp[method_pos] = total_nb_grasp[method_pos] + (len(timestamp_action)-2)/2
                    total_nb_release[method_pos] = total_nb_release[method_pos] + (len(timestamp_action)-2)/2
                    
                    nb_bloc = [nb_area_1,nb_area_2,nb_area_4,nb_area_8]

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

                    liste_good_grasp_area_coord = goodGraspAreaCoord(world)
                    liste_good_release_area_coord = goodReleaseAreaCoord(world)

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

                    for position, prediction in enumerate(block_prediction):
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

    nom_dossier = saveLog(nom_dossier,results,nb_prediction,duree_execution)




if __name__ == "__main__":
    parsingAllParticipantOneMethode()
