import numpy as np
import math
import os
import time
from datetime import datetime

import matplotlib.pyplot as plt

os.environ['KERAS_BACKEND'] = 'torch'
import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense, Reshape


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
from analyse import analyseSituation,analyseRelease,evaluationBestArea,analyseMethod,goodReleaseAreaCoord,goodGraspAreaCoord
from tools import quadrillageRelease,quadrillageGrasp,liste_tenon_bloc,saveLog,listeTimneAction


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

    liste_participant_mobile = []
    liste_participant_sitting = []

    for method_pos,method in enumerate(["mobile", "stationnary"]):
        directory = "../../dataset/" + method + "/sitting/"
        for entry in os.scandir(directory):
            if method == "mobile":
                liste_participant_mobile.append("../../dataset/" + method + "/sitting/" + entry.name)
            else:
                liste_participant_sitting.append("../../dataset/" + method + "/sitting/" + entry.name)
    
    print(liste_participant_mobile)

    left_ds, right_ds = keras.utils.split_dataset(np.array(liste_participant_mobile), left_size=0.8)
    left_ds_numpy = list(left_ds)
    right_ds_numpy = list(right_ds)
    #print(left_ds_numpy, right_ds_numpy)

    for ten in left_ds_numpy:
        print(ten.numpy().decode('utf-8'))

    print("---")

    for ten in right_ds_numpy:
        print(ten.numpy().decode('utf-8'))


    nb_action = 0
    duree_max = 0

    for number in left_ds_numpy:
        participant = number.numpy().decode('utf-8')
        for model in os.scandir(participant):

            print(model.path + "/table.csv")
            gaze_point = np.genfromtxt(
                model.path + "/table.csv", delimiter=","
            )
            world = np.genfromtxt(
                model.path + "/states.csv", delimiter=","
            )

            compte = np.zeros((world.shape[0] - 1))
            nb_action += world.shape[0] - 1


            t_init = gaze_point[1,0]
            indice = 0
            for t in range(1,gaze_point.shape[0]):
                
                t_gaze = gaze_point[t,0]

                if indice < world.shape[0] - 2 and t_gaze >= world[indice+2,0]:
                    indice += 1

                compte[indice] += 1

            if duree_max < compte.max():
                duree_max = compte.max()
                    
                

            

    print(nb_action)
    print(duree_max)

    print("UwUwUwUwU")

    training = np.zeros ((nb_action,int(duree_max),2))
    y_training = np.zeros((nb_action,2,nb_area_1))
    compteur_event = 0
    compteur_y_event = 0

    for number in left_ds_numpy:
        participant = number.numpy().decode('utf-8')
        for model in os.scandir(participant):

            gaze_point = np.genfromtxt(
                model.path + "/table.csv", delimiter=","
            )
            world = np.genfromtxt(
                model.path + "/states.csv", delimiter=","
            )

            t_init = gaze_point[1,0]
            indice = 0
            indice_event = 0
            for t in range(1,gaze_point.shape[0]):
                
                t_gaze = gaze_point[t,0]

                if indice < world.shape[0] - 2 and t_gaze >= world[indice+2,0]:

                        compteur_event += 1
                        indice += 1
                        indice_event = 0
                if str(gaze_point[t,1]) != "nan":
                    training[compteur_event] = gaze_point[t,1:2]
            compteur_event += 1

            for t in range(1,world.shape[0]):
                for id_block in range(24):
                    if world[t, 10 * id_block + 10] == 1:

                        taille_bloc = ((((id_block//3)%2)+1)*4)

                        x0_grasp = round((48/largeur)*world[t, 10 * id_block + 1])
                        y0_grasp = round((24/hauteur)*world[t, 10 * id_block + 2])

                        x2_grasp = round((48/largeur)*world[t, 10 * id_block + 5])
                        y2_grasp = round((48/largeur)*world[t, 10 * id_block + 6])

                        print("x0_grasp =",x0_grasp," // x2_grasp =",x2_grasp)
                        for x_grasp in range(x0_grasp,x2_grasp):
                            for y_grasp in range(y0_grasp,y2_grasp):
                                y_training[compteur_y_event + t - 1][0][x_grasp *24 + y_grasp] += 1 / taille_bloc
                                y_training[compteur_y_event + t ][0][x_grasp *24 + y_grasp] += 1 / taille_bloc

                        x0_release = round((48/largeur)*world[t+1, 10 * id_block + 1])
                        y0_release = round((24/hauteur)*world[t+1, 10 * id_block + 2])

                        x2_release = round((48/largeur)*world[t+1, 10 * id_block + 5])
                        y2_release = round((48/largeur)*world[t+1, 10 * id_block + 6])

                        for x_release in range(x0_release,x2_release):
                            for y_release in range(y0_release,y2_release):
                                y_training[compteur_y_event + t - 1][1][x_release *24 + y_release] += 1 / taille_bloc
                                y_training[compteur_y_event + t][1][x_release *24 + y_release] += 1 / taille_bloc
                if np.sum(y_training[compteur_y_event + t - 1]) == 4:
                    print(t,world.shape[0] - 1)
                    print(model.path + "/table.csv")                    
            compteur_y_event += world.shape[0] - 1
    print(compteur_event)
    print(np.max(np.sum(y_training,axis=(1,2))))


    # Définir le modèle LSTM
    model = Sequential()
    model.add(LSTM(50, input_shape=(duree_max, 2)))
    model.add(Dense(2 * nb_area_1, activation='relu'))  # Modifier la fonction d'activation selon votre problème
    model.add(Reshape((2, nb_area_1))) 
    model.compile(optimizer='adam', loss='mse')  # Choisir l'optimiseur et la fonction de perte appropriés

    # Entraîner le modèle
    history = model.fit(training, y_training, epochs=10, batch_size=32, validation_split=0.2)

    print(model.summary())

    # Extraire l'erreur d'entraînement et de validation
    train_loss = history.history['loss']
    val_loss = history.history['val_loss']  # Assurez-vous que val_loss est disponible dans history

    # Tracer le graphique de l'erreur en fonction des epochs
    epochs = range(1, len(train_loss) + 1)
    plt.plot(epochs, train_loss, 'b', label='Training loss')
    plt.plot(epochs, val_loss, 'r', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()


    return
    # On parcours la liste des dossiers correspondant aux participants
    for method_pos,method in enumerate(["mobile", "stationnary"]):
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

                    temps_debut = time.time()

                    # charge les deux fichiers dans des np.array
                    gaze_point = np.genfromtxt(
                        str(entry.path) + "/" + model + "/table.csv", delimiter=","
                    )
                    world = np.genfromtxt(
                        str(entry.path) + "/" + model + "/states.csv", delimiter=","
                    )
                    
                    duration = int(gaze_point[-1,0] - gaze_point[1,0])+1

                    (
                        feature,
                        timestamp_action,
                        liste_t_value,

                    ) = parsingOneSituation(gaze_point, world)
                    

                    probability1 = low_level_lstm(feature,timestamp_action,liste_t_value)
                    probability = low_level_naif(feature,timestamp_action,liste_t_value)

                    area_prediction,area_best_prediction,liste_predi_id = interpretation(probability,timestamp_action,liste_t_value,world,duration)

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
