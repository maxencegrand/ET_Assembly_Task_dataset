import numpy as np
import math
import os
import time
from datetime import datetime

os.environ['KERAS_BACKEND'] = 'torch'
import keras
from keras.models import Sequential,Model
from keras.layers import LSTM, Dense, Reshape, Input

from feature_computation import parsingOneSituation

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

    for method_pos,side in enumerate(left):   
        nb_action = 0
        duree_max = 0

        for number in side:
            participant = number.numpy().decode('utf-8')
            for model in os.scandir(participant):
                if not(participant.split("/")[-1] == "37931545" and str(model.path).split("/")[-1] == "tsb") and not(participant.split("/")[-1] == "30587763" and str(model.path).split("/")[-1] == "tsb") and os.path.exists(str(model.path) + "/table.csv") and os.path.exists(str(model.path) + "/states.csv"):
                    
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
                        print("Max:", str(model.path))
                        
                

                

        

        print(nb_action)
        print(duree_max)

        duree_max = int(duree_max)

        print("UwUwUwUwU")

        


        


        
        for k in range(nb_predi):
            print('modele'+ str(5*method_pos+k)+'.h5')
            training = np.zeros ((nb_action,int(duree_max),nb_area_1), dtype = np.float32)

            print(training.shape)

            y_training = np.zeros((nb_action,2,nb_area_1), dtype = np.float32)

            taille_octets = training.nbytes

            # Afficher la taille en octets
            print("Taille du tableau en octets:", taille_octets/(1024 ** 3))

            compteur_event = 0
            compteur_y_event = 0

            u = 0 



            for number in side:
                participant = number.numpy().decode('utf-8')
                for model in os.scandir(participant):


                    if not(participant.split("/")[-1] == "37931545" and str(model.path).split("/")[-1] == "tsb") and not(participant.split("/")[-1] == "30587763" and str(model.path).split("/")[-1] == "tsb") and os.path.exists(
                        str(model.path) + "/table.csv"
                    ) and os.path.exists(str(model.path) + "/states.csv"):
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
                                u += 1
                                result, = parsingOneSituation(gaze_point[t])
                                training[compteur_event][indice_event]  = result[k]
                            
                            indice_event += 1

                        compteur_event += 1

                        for t in range(1,world.shape[0]):
                            for id_block in range(24):
                                if world[t, 10 * id_block + 10] == 1:

                                    taille_bloc = ((((id_block//3)%2)+1)*4)

                                    x0_grasp = round((48/largeur)*world[t, 10 * id_block + 1])
                                    y0_grasp = round((24/hauteur)*world[t, 10 * id_block + 2])

                                    x2_grasp = round((48/largeur)*world[t, 10 * id_block + 5])
                                    y2_grasp = round((48/largeur)*world[t, 10 * id_block + 6])

                                    for x_grasp in range(x0_grasp,x2_grasp):
                                        for y_grasp in range(y0_grasp,y2_grasp):
                                            y_training[compteur_y_event + t - 2][0][x_grasp *24 + y_grasp] += 1 / taille_bloc
                                            y_training[compteur_y_event + t -1][0][x_grasp *24 + y_grasp] += 1 / taille_bloc

                                    x0_release = round((48/largeur)*world[t+1, 10 * id_block + 1])
                                    y0_release = round((24/hauteur)*world[t+1, 10 * id_block + 2])

                                    x2_release = round((48/largeur)*world[t+1, 10 * id_block + 5])
                                    y2_release = round((48/largeur)*world[t+1, 10 * id_block + 6])

                                    for x_release in range(x0_release,x2_release):
                                        for y_release in range(y0_release,y2_release):
                                            y_training[compteur_y_event + t][1][x_release *24 + y_release] += 1 / taille_bloc
                                            y_training[compteur_y_event + t - 1][1][x_release *24 + y_release] += 1 / taille_bloc
                            
                        compteur_y_event += world.shape[0] - 1

            print("u:", u)
            print(compteur_event)
            print(np.max(np.sum(y_training,axis=(1,2))))


        

            # Définir la forme de l'entrée
            input_layer = Input(shape=(int(duree_max), nb_area_1))

            # Construire le reste du modèle
            x = LSTM(50)(input_layer)
            x = Dense(2 * nb_area_1, activation='relu')(x)
            x = Reshape((2, nb_area_1))(x)

            # Créer le modèle en spécifiant les entrées et les sorties
            model = Model(inputs=input_layer, outputs=x)
            model.compile(optimizer='adam', loss='mean_squared_error')  # Choisir l'optimiseur et la fonction de perte appropriés

            # Entraîner le modèle
            history = model.fit(training, y_training, epochs=10, batch_size=1, validation_split=0.2)

            model.save('modele'+ str(5*method_pos+k)+'.keras')

            print(model.summary())

    return
    




if __name__ == "__main__":
    parsingAllParticipantOneMethode()
