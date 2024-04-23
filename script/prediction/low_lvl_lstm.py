import numpy as np
import math
import os
os.environ['KERAS_BACKEND'] = 'torch'
import keras

from keras.models import Sequential
from keras.layers import LSTM, Dense


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
low_level_naif prend les poids de feature extraction et renvoi les probabilites selon la methode modele

Input

feature: np.array(5,d,nb_tenon), poid pour les 5 manieres de calculer, pour tout t dans la duree de l'assamblage, pour chaque tenon
timestamp_action: liste des t correspondant aux evenements, avec 0 et le t final inclus

Output

probability: np.array((5, 2, duration, nb_area_1)) probabilite qu'un bloc tenon soit important selon les 5 manieres de calculer, sur la duree d'un assamblage, pour tous les tenons. La dimension 2 correspond aux reset grasp ou reset release
"""
def low_level_lstm(input_array,model,timestamp,timestamp_action,timestamp_indice):

    duree,table = input_array.shape

    input_array = input_array.reshape((1,duree,table))

    new_probability = model.predict(input_array, verbose=0)

    new_probability = new_probability.reshape(2,nb_area_1)
    
    #print(timestamp, timestamp_action[timestamp_indice])

    if timestamp_indice < len(timestamp_action)-1 and timestamp == timestamp_action[timestamp_indice]:

        timestamp_indice += 1       

    if np.sum(new_probability[0]) > 0:
        new_probability[0] = new_probability[0]/np.sum(new_probability[0])
    else:
        new_probability[0] = np.ones((nb_area_1))/nb_area_1

    if np.sum(new_probability[1]) > 0:
        new_probability[1] = new_probability[1]/np.sum(new_probability[1])
    else:
        new_probability[1] = np.ones((nb_area_1))/nb_area_1

    return new_probability, timestamp_indice

