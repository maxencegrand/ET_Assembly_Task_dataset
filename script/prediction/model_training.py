import numpy as np
import math
import os
import time
from datetime import datetime
import pickle

os.environ['KERAS_BACKEND'] = 'torch'
import keras
from keras.models import Sequential,Model
from keras.layers import GRU, LSTM, Dense, Reshape, Input

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


    liste_duree = []

    for method_pos,side in enumerate(left):   
        nb_action = 0
        duree_max = 0
        """
        Premier passing pour trouver l'action la plus grande
        """
        for number in side:
            participant = number.numpy().decode('utf-8')
            for model in os.scandir(participant):
                #On vŕifie que le participant existe et est non problematique (bug dans dataset)
                if not(participant.split("/")[-1] == "37931545" and str(model.path).split("/")[-1] == "tsb") and not(participant.split("/")[-1] == "30587763" and str(model.path).split("/")[-1] == "tsb") and os.path.exists(str(model.path) + "/table.csv") and os.path.exists(str(model.path) + "/states.csv"):
                    
                    #On charge les données
                    gaze_point = np.genfromtxt(
                        model.path + "/table.csv", delimiter=","
                    )
                    
                    world = np.genfromtxt(
                        model.path + "/states.csv", delimiter=","
                    )


                    
                    #Compte de taille nombre d'action
                    compte = np.zeros((world.shape[0] - 1))
                    nb_action += world.shape[0] - 2

                    t_init = gaze_point[1,0]
                    indice = 0

                    #On mesure la longueur de chaque action
                    for t in range(1,gaze_point.shape[0]):
                        
                        t_gaze = gaze_point[t,0]

                        if indice < world.shape[0] - 2 and t_gaze >= world[indice+2,0]:
                            indice += 1

                        compte[indice] += 1

                    for u in range(compte.shape[0]):
                        liste_duree.append(compte[u])

                    #Si l'action est plus grande que duree_max, on actualise duree_max
                    if duree_max < compte.max():
                        duree_max = compte.max()
                        print("Max:", str(model.path))
                        
                

                
        sorted_data = sorted(liste_duree)
    
        # Trouvez l'indice correspondant à 90% des valeurs
        good_index = int(0.95 * len(sorted_data))
        
        # Récupérez la valeur à cet indice
        good_size = int(sorted_data[good_index])
        
        print("indice 95%",good_size)

        print(nb_action)
        print(duree_max)

        duree_max = int(duree_max)

        print("UwUwUwUwU")

        


        


        """
        deuxieme passing pour recuperer l'ensemble des actions (découpage par action) + faire la matrice des proba theorique

        On le fait en nb_predi fois afin de limiter l'utilisation d ela ram au detriment du temps
        """
        for k in range(nb_predi):
            print('modele'+ str(5*method_pos+k)+'.h5')
            #float32 -> 7 chiffres significatif, cela devrait etre suffissant
            training = np.zeros ((nb_action,int(good_size),nb_area_1), dtype = np.float32)

            print(training.shape)

            y_training = np.zeros((nb_action,nb_area_1), dtype = np.float32)

            taille_octets = training.nbytes

            # Afficher la taille en octets
            print("Taille du tableau en octets:", taille_octets/(1024 ** 3))

            compteur_event = 0
            compteur_y_event = 0

            """
            debut deuxieme passing 
            """
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

                        indice = 0

                        #Pour chaque gaze point
                        for t in range(1,gaze_point.shape[0]):
                            #On recupere le timestamp
                            t_gaze = gaze_point[t,0]

                            #On vérifie si on n'est pas passé a l'action suivante
                            if indice < world.shape[0] - 3 and t_gaze >= world[indice+2,0]:
                                    #compteur d'action (global)
                                    compteur_event += 1
                                    #compteur d'action (local, cad sur ce participant/cette figure)
                                    indice += 1
                                    #compteur gaze point lors de cette action
                                    indice_event = 0

                                    previous_data = gaze_point[max(0,t - good_size):t]

                                    if previous_data.shape[0] < good_size:
                                        previous_data = np.pad(previous_data,((good_size - previous_data.shape[0],0),*[(0, 0)] * (previous_data.ndim - 1)),mode="constant",constant_values=0)

                                    for u in range(previous_data.shape[0]):
                                        result, = parsingOneSituation(previous_data[u])
                                        training[compteur_event][u]  = result[k]
                                    

                        compteur_event += 1

                        #construction de y_training

                        #Pour chaque action
                        for t in range(1,world.shape[0]):
                            #Je parcours la liste des blocs
                            for id_block in range(24):
                                #Si l'un d'eux est holding
                                if world[t, 10 * id_block + 10] == 1:
                                    #Alors a l'instant t on a l'emplacement du grasp
                                    #Et a l'instant t+1 on a l'emplacement du release

                                    taille_bloc = ((((id_block//3)%2)+1)*4)

                                    #Pour t (grasp) 
                                    #Passage coordonnees a emplacement tenon/coord matrice
                                    x0_grasp = round((48/largeur)*world[t, 10 * id_block + 1])
                                    y0_grasp = round((24/hauteur)*world[t, 10 * id_block + 2])

                                    x2_grasp = round((48/largeur)*world[t, 10 * id_block + 5])
                                    y2_grasp = round((48/largeur)*world[t, 10 * id_block + 6])
                                    
                                    #on change l'emplacement du bloc par 1/taille du bloc
                                    for x_grasp in range(x0_grasp,x2_grasp):
                                        for y_grasp in range(y0_grasp,y2_grasp):
                                            y_training[compteur_y_event + t - 2][x_grasp *24 + y_grasp] += 1 / taille_bloc


                                    #Pour t+1 (release)
                                    x0_release = round((48/largeur)*world[t+1, 10 * id_block + 1])
                                    y0_release = round((24/hauteur)*world[t+1, 10 * id_block + 2])

                                    x2_release = round((48/largeur)*world[t+1, 10 * id_block + 5])
                                    y2_release = round((48/largeur)*world[t+1, 10 * id_block + 6])

                                    for x_release in range(x0_release,x2_release):
                                        for y_release in range(y0_release,y2_release):
                                            y_training[compteur_y_event + t - 1][x_release *24 + y_release] += 1 / taille_bloc
                            
                        compteur_y_event += world.shape[0] - 2




        

            # Définir la forme de l'entrée
            input_layer = Input(shape=(int(good_size), nb_area_1))

            # Construire le reste du modèle
            x = LSTM(int(good_size))(input_layer)
            x = Dense(nb_area_1, activation='relu')(x)

            # Créer le modèle en spécifiant les entrées et les sorties
            model = Model(inputs=input_layer, outputs=x)
            model.compile(optimizer='adam', loss='mean_squared_error')  # Choisir l'optimiseur et la fonction de perte appropriés

            # Entraîner le modèle
            history = model.fit(training, y_training, epochs=10, batch_size=32, validation_split=0.2)

            model.save('test_modele'+ str(5*method_pos+k)+'_LSTM.keras')

            # Enregistrer l'historique dans un fichier
            with open('history_'+str(k)+'.pkl', 'wb') as f:
                pickle.dump(history.history, f)

            print(model.summary())


    return
    


if __name__ == "__main__":
    parsingAllParticipantOneMethode()
