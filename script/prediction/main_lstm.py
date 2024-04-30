import numpy as np
import math
import os
import time
from datetime import datetime

os.environ['KERAS_BACKEND'] = 'torch'
import keras
from keras.models import load_model
from keras.layers import LSTM, Dense, Reshape
from keras import backend



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
from low_lvl_lstm import low_level_lstm
from interpretation import interpretation
from analyse import analyseSituation,analyseMethod,analyseFixeAreaWeak,analyseFixeAreaStrong,analyseSlidingAreaWeak,analyseSlidingAreaStrong
from tools import quadrillageRelease,quadrillageGrasp,saveLog,listeTimneAction, CurrentWorld, savingFeature,savingInterpretation,savingProba,savingTime


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

    global_analyse_grasp_area_weak = np.zeros((4,2,nb_predi,6001))
    global_nb_analyse_grasp_area_weak = np.zeros((4,2,6001))
    global_analyse_release_area_weak = np.zeros((4,2,nb_predi,6001))
    global_nb_analyse_release_area_weak = np.zeros((4,2,6001))

    global_analyse_grasp_area_strong = np.zeros((4,2,nb_predi,6001))
    global_nb_analyse_grasp_area_strong = np.zeros((4,2,6001))
    global_analyse_release_area_strong = np.zeros((4,2,nb_predi,6001))
    global_nb_analyse_release_area_strong = np.zeros((4,2,6001))

    global_analyse_grasp_block = np.zeros((2,nb_predi,6001))
    global_nb_analyse_grasp_block = np.zeros((2,6001))
    global_analyse_release_block = np.zeros((2,nb_predi,6001))
    global_nb_analyse_release_block = np.zeros((2,6001))

    nb_analyse = 0

    duree_execution = [[],[]]

    liste_participant_mobile = []
    liste_participant_sitting = []

    for method_pos,method in enumerate(["mobile", "stationnary"]):
        directory = "../../dataset/" + method + "/sitting/"
        for entry in os.scandir(directory):
            if method == "mobile":
                liste_participant_mobile.append(entry.path)
            else:
                liste_participant_sitting.append(entry.path)
    
    print(liste_participant_mobile)

    left_mobile, right_mobile = keras.utils.split_dataset(np.array(liste_participant_mobile), left_size=0.8)
    left_mobile_numpy = list(left_mobile)
    right_mobile_numpy = list(right_mobile)

    left_sitting, right_sitting = keras.utils.split_dataset(np.array(liste_participant_sitting), left_size=0.8)
    left_sitting_numpy = list(left_sitting)
    right_sitting_numpy = list(right_sitting)

    left = [left_mobile_numpy,left_sitting_numpy]
    right = [right_mobile_numpy,right_sitting_numpy]

    model0 = load_model('modele0_LSTM.keras')
    model1 = load_model('modele1_LSTM.keras')
    model2 = load_model('modele2_LSTM.keras')
    model3 = load_model('modele3_LSTM.keras')
    model4 = load_model('modele4_LSTM.keras')

    model5 = load_model('modele5_LSTM.keras')
    model6 = load_model('modele6_LSTM.keras')
    model7 = load_model('modele7_LSTM.keras')
    model8 = load_model('modele8_LSTM.keras')
    model9 = load_model('modele8_LSTM.keras')

    list_model = [[model0,model1,model2,model3,model4],[model5,model6,model7,model8,model9]]
                  
    print(model0.summary())

    if backend.backend() == "tensorflow":
        print("TF")
    elif backend.backend() == "jax":
        print("Jax")
    elif backend.backend() == "torch":
        print("Torch")
    elif backend.backend() == "numpy":
        print("Numpy")

    input_dims = model0.input_shape[1]
    print(input_dims)

    for method_pos,side in enumerate(right):
            if method_pos == 1:
                continue
            for number in side:
                participant = number.numpy().decode('utf-8')
                print(participant)
                for model in os.scandir(participant):
                    print("Path :" , model.path)
                    # verifie que les 2 fichiers existent


                    if not(str(model.path).split("/")[-2] == "30587763" and str(model.path).split("/")[-1] == "tsb") and os.path.exists(
                        str(model.path) + "/table.csv"
                    ) and os.path.exists(str(model.path) + "/states.csv"):

                        print("---------------------------")
                        print("Partcipant :", str(model.path).split("/")[-2], str(model.path).split("/")[-1], method_pos)
                                          



                        # charge les deux fichiers dans des np.array
                        gaze_point = np.genfromtxt(
                            str(model.path) + "/table.csv", delimiter=","
                        )

                        world = np.genfromtxt(
                            str(model.path) + "/states.csv", delimiter=","
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

                        temp_area4 = np.zeros((5,2,nb_gaze))
                        temp_area8 = np.zeros((5,2,nb_gaze))

                        temp_area_sliding_4 = np.zeros((5,2,nb_gaze))
                        temp_area_sliding_8 = np.zeros((5,2,nb_gaze))

                        temp_block = np.zeros((5,2,nb_gaze))

                        input_array = np.zeros((nb_predi,input_dims,1152))
                        input_indice = 0

                        print(input_array.shape)

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

                            input_array[:,input_indice,:] = feature

                            for k in range(nb_predi):
                                temps_debut = time.time()
                                new_probability,new_indice = low_level_lstm(input_array[k],list_model[method_pos][k],t,timestamp_action,indice)
                                temps_fin = time.time()
                                delta_temps = temps_fin - temps_debut
                                probability[k,:,i,:] = new_probability

                            input_indice += 1
                                
                            if indice != new_indice:
                                input_array = np.zeros((nb_predi,input_dims,1152))
                                input_indice = 0

                            


                            area4max_indices,area8max_indices,area_best_4,area_best_8,liste_predi_id = interpretation(probability[:,:,i,:],new_indice,world,)
                            
                            temp_area4[:,:,i] = area4max_indices
                            temp_area8[:,:,i] = area8max_indices

                            temp_area_sliding_4[:,:,i] = area_best_4
                            temp_area_sliding_8[:,:,i] = area_best_8

                            temp_block[:,:,i] = liste_predi_id

                            indice = new_indice
                            
                            temps_fin = time.time()
                            diff_temps = temps_fin - temps_debut
                            liste_temps_exec.append(diff_temps)



                        if  method_pos == 0:
                            path = "mobile/sitting/"+str(model.path).split("/")[-2]+"/"+str(model.path).split("/")[-1]+"/"

                        else:
                            path = "stationnary/sitting/"+str(model.path).split("/")[-2]+"/"+str(model.path).split("/")[-1]+"/"

                        savingTime(nom_dossier,path,liste_temps_exec)
                        savingFeature(nom_dossier,path,all_feature)
                        savingProba(nom_dossier,path,probability)
                        savingInterpretation(nom_dossier,path,temp_area4,temp_area8,temp_area_sliding_4,temp_area_sliding_8,temp_block)
                        

                        result_area4 = np.zeros((5, 2, duree))
                        result_area8 = np.zeros((5, 2, duree))
                        result_sliding_area4 = np.zeros((5, 2, duree))
                        result_sliding_area8 = np.zeros((5, 2, duree))
                        result_block = np.zeros((5, 2, duree))

                        time_indice = 0

                        for t in range(duree):
                            if time_indice < len(liste_t_value) and t == liste_t_value[time_indice]:

                                result_area4[:,:,t] = temp_area4[:,:,time_indice]
                                result_area8[:,:,t] = temp_area8[:,:,time_indice]
                                result_sliding_area4[:,:,t] = temp_area_sliding_4[:,:,time_indice]
                                result_sliding_area8[:,:,t] = temp_area_sliding_8[:,:,time_indice]
                                result_block[:,:,t] = temp_block[:,:,time_indice]

                                time_indice += 1

                            else:
                                result_area4[:,:,t] = result_area4[:,:,t-1]
                                result_area8[:,:,t] = result_area8[:,:,t-1]
                                result_sliding_area4[:,:,t] = result_sliding_area4[:,:,t-1]
                                result_sliding_area8[:,:,t] = result_sliding_area8[:,:,t-1]
                                result_block[:,:,t] = result_block[:,:,t-1]

                        area_prediction = [result_area4,result_area8,result_sliding_area4,result_sliding_area8]

                        block_prediction = result_block

                        # Durée d'exécution en secondes
                        delta_temps = temps_fin - temps_debut

                        duree_execution[method_pos].append(delta_temps)

                        total_nb_grasp[method_pos] = total_nb_grasp[method_pos] + (len(timestamp_action)-2)/2
                        total_nb_release[method_pos] = total_nb_release[method_pos] + (len(timestamp_action)-2)/2
                        
                        nb_bloc = [nb_area_4,nb_area_8,nb_area_4,nb_area_8]

                        for position, predi in enumerate(area_prediction):
                            liste_good_release_zones = quadrillageRelease(world,nb_bloc[position])
                            liste_good_grasp_zones = quadrillageGrasp(world,nb_bloc[position])
                            if position < len(area_prediction)/2:
                                for posi,quadr in enumerate(predi):

                                    (
                                    analyse_area_grasp,
                                    nb_analyse_area_grasp,
                                    analyse_area_release,
                                    nb_analyse_area_release
                                    ) = analyseFixeAreaWeak(quadr, liste_good_grasp_zones, liste_good_release_zones,timestamp_action,nb_bloc[position])

                                    global_analyse_grasp_area_weak[position][method_pos][posi] += analyse_area_grasp
                                    global_analyse_release_area_weak[position][method_pos][posi] += analyse_area_release

                                    (
                                    analyse_area_grasp,
                                    nb_analyse_area_grasp,
                                    analyse_area_release,
                                    nb_analyse_area_release
                                    ) = analyseFixeAreaStrong(quadr,liste_good_grasp_zones,liste_good_release_zones,timestamp_action,nb_bloc[position])

                                    global_analyse_grasp_area_strong[position][method_pos][posi] += analyse_area_grasp
                                    global_analyse_release_area_strong[position][method_pos][posi] += analyse_area_release

                                global_nb_analyse_grasp_area_weak[position][method_pos] += nb_analyse_area_grasp
                                global_nb_analyse_release_area_weak[position][method_pos] += nb_analyse_area_release

                                global_nb_analyse_grasp_area_strong[position][method_pos] += nb_analyse_area_grasp
                                global_nb_analyse_release_area_strong[position][method_pos] += nb_analyse_area_release

                            else:

                                for posi,quadr in enumerate(predi):

                                    (
                                    analyse_area_grasp,
                                    nb_analyse_area_grasp,
                                    analyse_area_release,
                                    nb_analyse_area_release
                                    ) = analyseSlidingAreaWeak(quadr, liste_good_grasp_zones, liste_good_release_zones,timestamp_action,nb_bloc[position])

                                    global_analyse_grasp_area_weak[position][method_pos][posi] += analyse_area_grasp
                                    global_analyse_release_area_weak[position][method_pos][posi] += analyse_area_release

                                    (
                                    analyse_area_grasp,
                                    nb_analyse_area_grasp,
                                    analyse_area_release,
                                    nb_analyse_area_release
                                    ) = analyseSlidingAreaStrong(quadr,liste_good_grasp_zones,liste_good_release_zones,timestamp_action,nb_bloc[position])

                                    global_analyse_grasp_area_strong[position][method_pos][posi] += analyse_area_grasp
                                    global_analyse_release_area_strong[position][method_pos][posi] += analyse_area_release

                                global_nb_analyse_grasp_area_weak[position][method_pos] += nb_analyse_area_grasp
                                global_nb_analyse_release_area_weak[position][method_pos] += nb_analyse_area_release

                                global_nb_analyse_grasp_area_strong[position][method_pos] += nb_analyse_area_grasp
                                global_nb_analyse_release_area_strong[position][method_pos] += nb_analyse_area_release




                        for position, prediction in enumerate(block_prediction):
                            # Analyse max min dist
                            (
                                analyse_grasp,
                                nb_analyse_grasp,
                                analyse_release,
                                nb_analyse_release,
                            ) = analyseSituation(world, prediction, timestamp_action)
                            
                            global_analyse_grasp_block[method_pos][position] = global_analyse_grasp_block[method_pos][position] + analyse_grasp
                            global_analyse_release_block[method_pos][position] = global_analyse_release_block[method_pos][position] + analyse_release

                        global_nb_analyse_grasp_block[method_pos] += nb_analyse_grasp
                        global_nb_analyse_release_block[method_pos] += nb_analyse_release


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


    results = np.zeros((18,2,nb_predi,6001))

    results[0] = global_analyse_grasp_area_weak[0]
    results[1] = global_analyse_grasp_area_weak[1]
    results[2] = global_analyse_grasp_area_weak[2]
    results[3] = global_analyse_grasp_area_weak[3]
    results[4] = global_analyse_release_area_weak[0]
    results[5] = global_analyse_release_area_weak[1]
    results[6] = global_analyse_release_area_weak[2]
    results[7] = global_analyse_release_area_weak[3]
    results[8] = global_analyse_grasp_area_strong[0]
    results[9] = global_analyse_grasp_area_strong[1]
    results[10] = global_analyse_grasp_area_strong[2]
    results[11] = global_analyse_grasp_area_strong[3]
    results[12] = global_analyse_release_area_strong[0]
    results[13] = global_analyse_release_area_strong[1]
    results[14] = global_analyse_release_area_strong[2]
    results[15] = global_analyse_release_area_strong[3]
    results[16] = global_analyse_grasp_block
    results[17] = global_analyse_release_block

    nb_prediction = np.zeros((18,2,6001))

    nb_prediction[0] = global_nb_analyse_grasp_area_weak[0]
    nb_prediction[1] = global_nb_analyse_grasp_area_weak[1]
    nb_prediction[2] = global_nb_analyse_grasp_area_weak[2]
    nb_prediction[3] = global_nb_analyse_grasp_area_weak[3]
    nb_prediction[4] = global_nb_analyse_release_area_weak[0]
    nb_prediction[5] = global_nb_analyse_release_area_weak[1]
    nb_prediction[6] = global_nb_analyse_release_area_weak[2]
    nb_prediction[7] = global_nb_analyse_release_area_weak[3]
    nb_prediction[8] = global_nb_analyse_grasp_area_strong[0]
    nb_prediction[9] = global_nb_analyse_grasp_area_strong[1]
    nb_prediction[10] = global_nb_analyse_grasp_area_strong[2]
    nb_prediction[11] = global_nb_analyse_grasp_area_strong[3]
    nb_prediction[12] = global_nb_analyse_release_area_strong[0]
    nb_prediction[13] = global_nb_analyse_release_area_strong[1]
    nb_prediction[14] = global_nb_analyse_release_area_strong[2]
    nb_prediction[15] = global_nb_analyse_release_area_strong[3]
    nb_prediction[16] = global_nb_analyse_grasp_block
    nb_prediction[17] = global_nb_analyse_release_block

    nom_dossier = saveLog(nom_dossier,results,nb_prediction,duree_execution)




if __name__ == "__main__":
    parsingAllParticipantOneMethode()
