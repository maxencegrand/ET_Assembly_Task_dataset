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
from analyse import analyseSituation,analyseMethod,analyseFixeAreaWeak,analyseFixeAreaStrong,analyseSlidingAreaWeak,analyseSlidingAreaStrong,analyseSemantic,analyseSemanticBis,analyseNorme
from tools import quadrillageRelease,quadrillageGrasp,saveLog,listeTimneAction, CurrentWorld, savingFeature,savingInterpretation,savingProba,savingTime
from seed import liste_seed

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

    global_analyse_semantic_grasp = np.zeros((4,2,nb_predi,6001))
    global_nb_analyse_semantic_grasp = np.zeros((4,2,6001))
    global_analyse_semantic_release = np.zeros((4,2,nb_predi,6001))
    global_nb_analyse_semantic_release = np.zeros((4,2,6001))

    global_analyse_norme_grasp = np.zeros((2,nb_predi,6001))
    global_nb_analyse_norme_grasp = np.zeros((2,6001))
    global_analyse_norme_release = np.zeros((2,nb_predi,6001))
    global_nb_analyse_norme_release = np.zeros((2,6001))

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

    liste_seeds = liste_seed()
    
    for seed in liste_seeds:

        print("seed", seed)

        left_mobile, right_mobile = keras.utils.split_dataset(np.array(liste_participant_mobile), left_size=0.8, shuffle=True, seed = int(seed))
        left_mobile_numpy = list(left_mobile)
        right_mobile_numpy = list(right_mobile)

        left_sitting, right_sitting = keras.utils.split_dataset(np.array(liste_participant_sitting), left_size=0.8, shuffle=True, seed = int(seed))
        left_sitting_numpy = list(left_sitting)
        right_sitting_numpy = list(right_sitting)

        left = [left_mobile_numpy,left_sitting_numpy]
        right = [right_mobile_numpy,right_sitting_numpy]

        model0 = load_model(str(seed)+'_modele0_LSTM.keras')
        model1 = load_model(str(seed)+'_modele1_LSTM.keras')
        model2 = load_model(str(seed)+'_modele2_LSTM.keras')
        model3 = load_model(str(seed)+'_modele3_LSTM.keras')
        model4 = load_model(str(seed)+'_modele4_LSTM.keras')

        model5 = load_model(str(seed)+'_modele5_LSTM.keras')
        model6 = load_model(str(seed)+'_modele6_LSTM.keras')
        model7 = load_model(str(seed)+'_modele7_LSTM.keras')
        model8 = load_model(str(seed)+'_modele8_LSTM.keras')
        model9 = load_model(str(seed)+'_modele9_LSTM.keras')



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

        

        for method_pos,side in enumerate(right):

                input_dims = list_model[method_pos][0].input_shape[1]
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

                            proba_juste = np.zeros((world.shape[0] - 1,2,nb_area_1))

                            for t in range(1,world.shape[0]):
                                #Pour chaque bloc
                                for id_block in range(24):
                                    #Si le bloc est grasp
                                    if world[t, 10 * id_block + 10] == 1:

                                        taille_bloc = ((((id_block//3)%2)+1)*4)

                                        x0_grasp = round((48/largeur)*world[t, 10 * id_block + 1])
                                        y0_grasp = round((24/hauteur)*world[t, 10 * id_block + 2])

                                        x2_grasp = round((48/largeur)*world[t, 10 * id_block + 5])
                                        y2_grasp = round((48/largeur)*world[t, 10 * id_block + 6])

                                        for x_grasp in range(x0_grasp,x2_grasp):
                                            for y_grasp in range(y0_grasp,y2_grasp):
                                                if t-2 <0:
                                                    print("bdm;lbdfklnbdnfkl")
                                                proba_juste[t - 2][0][x_grasp *24 + y_grasp] += 1 / taille_bloc
                                                proba_juste[t - 1][0][x_grasp *24 + y_grasp] += 1 / taille_bloc

                                        x0_release = round((48/largeur)*world[t+1, 10 * id_block + 1])
                                        y0_release = round((24/hauteur)*world[t+1, 10 * id_block + 2])

                                        x2_release = round((48/largeur)*world[t+1, 10 * id_block + 5])
                                        y2_release = round((48/largeur)*world[t+1, 10 * id_block + 6])

                                        for x_release in range(x0_release,x2_release):
                                            for y_release in range(y0_release,y2_release):
                                                if t == world.shape[0]:
                                                    print("Probleme")
                                                proba_juste[t][1][x_release *24 + y_release] += 1 / taille_bloc
                                                proba_juste[t - 1][1][x_release *24 + y_release] += 1 / taille_bloc
                            
                            duree = int(max(world[-1,0], gaze_point[-1,0] ) - min(world[1,0], gaze_point[1,0] ) ) + 1

                            nb_gaze = gaze_point.shape[0] - 1

                            timestamp_action = listeTimneAction(world)
                            

                            all_feature = np.zeros((5, nb_gaze, nb_area_1))

                            probability = np.zeros((5, 2, nb_gaze, nb_area_1))

                            t_init = world[1,0]

                            indice = 0

                            liste_t_value = []

                            liste_temps_exec = []

                            temp_area4 = np.zeros((5,2,nb_gaze))
                            temp_area8 = np.zeros((5,2,nb_gaze))

                            temp_area_sliding_4 = np.zeros((5,2,nb_gaze))
                            temp_area_sliding_8 = np.zeros((5,2,nb_gaze))

                            temp_area_semantic_0 = np.zeros((5,2,nb_gaze))
                            temp_area_semantic_1 = np.zeros((5,2,nb_gaze))
                            temp_area_semantic_2 = np.zeros((5,2,nb_gaze))

                            temp_block = np.zeros((5,2,nb_gaze))

                            input_array = np.zeros((nb_predi,input_dims,1152))
                            input_indice = 0

                            norme_array = np.zeros((nb_predi,2,nb_gaze))

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

                                input_array = all_feature[:,max(0, i - input_dims + 1):i+1,:]
                                

                                if input_array.shape[1] < input_dims:
                                    #padding de 0 en avant de la 2eme dimension
                                    input_array = np.pad(input_array,(*[(0, 0)] * (1),(input_dims - input_array.shape[1],0),*[(0, 0)] * (input_array.ndim - 2)))


                                for k in range(nb_predi):
                                    temps_debut = time.time()
                                    new_probability,new_indice = low_level_lstm(input_array[k],list_model[method_pos][k],t,timestamp_action,indice)
                                    temps_fin = time.time()
                                    delta_temps = temps_fin - temps_debut
                                    probability[k,:,i,:] = new_probability

                                for f in range(nb_predi):
                                    if(max(0,new_indice - 1) % 2 == 0):
                                        norme_array[f,0,i] += np.linalg.norm(proba_juste[new_indice - 1][0] - probability[f,0,i,:], ord=1)
                                        norme_array[f,1,i] += np.linalg.norm(proba_juste[new_indice - 1][1] - probability[f,1,i,:], ord=1)
                                        

                                    else:
                                        norme_array[f,0,i] += np.linalg.norm(proba_juste[new_indice - 1][0] - probability[f,0,i,:], ord=1)
                                        norme_array[f,1,i] += np.linalg.norm(proba_juste[new_indice - 1][1] - probability[f,1,i,:], ord=1)

                                input_indice += 1
                                    
                                if indice != new_indice:
                                    input_array = np.zeros((nb_predi,input_dims,1152))
                                    input_indice = 0

                                


                                area4max_indices,area8max_indices,area_best_4,area_best_8,semantic0,semantic1,semantic2,liste_predi_id = interpretation(probability[:,:,i,:],new_indice,world,str(model.path).split("/")[-1],)
                                
                                temp_area4[:,:,i] = area4max_indices
                                temp_area8[:,:,i] = area8max_indices

                                temp_area_sliding_4[:,:,i] = area_best_4
                                temp_area_sliding_8[:,:,i] = area_best_8

                                temp_area_semantic_0[:,:,i] = semantic0
                                temp_area_semantic_1[:,:,i] = semantic1
                                temp_area_semantic_2[:,:,i] = semantic2

                                temp_block[:,:,i] = liste_predi_id

                                indice = new_indice
                                
                                temps_fin = time.time()
                                diff_temps = temps_fin - temps_debut
                                liste_temps_exec.append(diff_temps)



                            if  method_pos == 0:
                                path = "mobile/sitting/"+str(model.path).split("/")[-2]+"/"+str(model.path).split("/")[-1]+"/"

                            else:
                                path = "stationnary/sitting/"+str(model.path).split("/")[-2]+"/"+str(model.path).split("/")[-1]+"/"

                            #savingTime(nom_dossier,path,liste_temps_exec)
                            #savingFeature(nom_dossier,path,all_feature)
                            #savingProba(nom_dossier,path,probability)
                            #savingInterpretation(nom_dossier,path,temp_area4,temp_area8,temp_area_sliding_4,temp_area_sliding_8,temp_block)
                            

                            result_area4 = np.zeros((5, 2, duree))
                            result_area8 = np.zeros((5, 2, duree))
                            result_sliding_area4 = np.zeros((5, 2, duree))
                            result_sliding_area8 = np.zeros((5, 2, duree))
                            result_semantic_0 = np.zeros((5, 2, duree))
                            result_semantic_1 = np.zeros((5, 2, duree))
                            result_semantic_2 = np.zeros((5, 2, duree))
                            result_block = np.zeros((5, 2, duree))

                            result_norme = np.zeros((5, 2, duree))

                            time_indice = 0

                            for t in range(duree):
                                if time_indice < len(liste_t_value) and t == liste_t_value[time_indice]:

                                    result_area4[:,:,t] = temp_area4[:,:,time_indice]
                                    result_area8[:,:,t] = temp_area8[:,:,time_indice]
                                    result_sliding_area4[:,:,t] = temp_area_sliding_4[:,:,time_indice]
                                    result_sliding_area8[:,:,t] = temp_area_sliding_8[:,:,time_indice]
                                    result_semantic_0[:,:,t] = temp_area_semantic_0[:,:,time_indice]
                                    result_semantic_1[:,:,t] = temp_area_semantic_1[:,:,time_indice]
                                    result_semantic_2[:,:,t] = temp_area_semantic_2[:,:,time_indice]
                                    result_block[:,:,t] = temp_block[:,:,time_indice]

                                    result_norme[:,:,t] = norme_array[:,:,time_indice]

                                    time_indice += 1

                                else:
                                    result_area4[:,:,t] = result_area4[:,:,t-1]
                                    result_area8[:,:,t] = result_area8[:,:,t-1]
                                    result_sliding_area4[:,:,t] = result_sliding_area4[:,:,t-1]
                                    result_sliding_area8[:,:,t] = result_sliding_area8[:,:,t-1]
                                    result_semantic_0[:,:,t] = result_semantic_0[:,:,t-1]
                                    result_semantic_1[:,:,t] = result_semantic_1[:,:,t-1]
                                    result_semantic_2[:,:,t] = result_semantic_2[:,:,t-1]
                                    result_block[:,:,t] = result_block[:,:,t-1]

                                    result_norme[:,:,t] = result_norme[:,:,t-1]

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

                            result_semantic_1b = np.where(result_semantic_1 == 2, 0, result_semantic_1)

                            list_semantic = [result_semantic_0, result_semantic_1, result_semantic_2, result_semantic_1b]

                            for lvl,semantic in enumerate(list_semantic):
                                for position, prediction in enumerate(semantic):
                                    # Analyse max min dist
                                    (
                                        analyse_grasp,
                                        nb_analyse_grasp,
                                        analyse_release,
                                        nb_analyse_release,
                                    ) = analyseSemanticBis(world, prediction, timestamp_action,str(model.path).split("/")[-1],lvl)
                                    
                                    global_analyse_semantic_grasp[lvl][method_pos][position] = global_analyse_semantic_grasp[lvl][method_pos][position] + analyse_grasp
                                    global_analyse_semantic_release[lvl][method_pos][position] = global_analyse_semantic_release[lvl][method_pos][position] + analyse_release

                                global_nb_analyse_semantic_grasp[lvl][method_pos] += nb_analyse_grasp
                                global_nb_analyse_semantic_release[lvl][method_pos] += nb_analyse_release

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

                            for position in range(nb_predi):
                                (
                                    analyse_grasp,
                                    nb_analyse_grasp,
                                    analyse_release,
                                    nb_analyse_release,
                                ) = analyseNorme(result_norme[position], timestamp_action)

                                global_analyse_norme_grasp[method_pos][position] += analyse_grasp
                                global_analyse_norme_release[method_pos][position] += analyse_release

                            global_nb_analyse_norme_grasp[method_pos] += nb_analyse_grasp
                            global_nb_analyse_norme_release[method_pos] += nb_analyse_release

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


    results = np.zeros((28,2,nb_predi,6001))

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
    results[16] = global_analyse_semantic_grasp[0]
    results[17] = global_analyse_semantic_grasp[1]
    results[18] = global_analyse_semantic_grasp[2]
    results[19] = global_analyse_semantic_grasp[3]
    results[20] = global_analyse_semantic_release[0]
    results[21] = global_analyse_semantic_release[1]
    results[22] = global_analyse_semantic_release[2]
    results[23] = global_analyse_semantic_release[3]
    results[24] = global_analyse_grasp_block
    results[25] = global_analyse_release_block
    results[26] = global_analyse_norme_grasp
    results[27] = global_analyse_norme_release

    nb_prediction = np.zeros((28,2,6001))

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
    nb_prediction[16] = global_nb_analyse_semantic_grasp[0]
    nb_prediction[17] = global_nb_analyse_semantic_grasp[1]
    nb_prediction[18] = global_nb_analyse_semantic_grasp[2]
    nb_prediction[19] = global_nb_analyse_semantic_grasp[2]
    nb_prediction[20] = global_nb_analyse_semantic_release[0]
    nb_prediction[21] = global_nb_analyse_semantic_release[1]
    nb_prediction[22] = global_nb_analyse_semantic_release[2]
    nb_prediction[23] = global_nb_analyse_semantic_release[2]
    nb_prediction[24] = global_nb_analyse_grasp_block
    nb_prediction[25] = global_nb_analyse_release_block
    nb_prediction[26] = global_nb_analyse_norme_grasp
    nb_prediction[27] = global_nb_analyse_norme_release

    nom_dossier = saveLog(nom_dossier,results,nb_prediction,duree_execution)



if __name__ == "__main__":
    parsingAllParticipantOneMethode()
