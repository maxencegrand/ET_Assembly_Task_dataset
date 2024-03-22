import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.widgets import Slider
import os

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



def low_level_naif(feature, timestamp_action):
    duration = feature.shape[1]

    probability = np.zeros((5, 2, duration, nb_bloc_1))

    timestamp_indice = 0


    for t in range(duration):
        if timestamp_indice < len(timestamp_action) and t > timestamp_action[timestamp_indice]:

            probability[0, (timestamp_indice + 1) % 2, t] = probability[0, (timestamp_indice + 1) % 2, t-1] + feature[0, t]
            probability[1, (timestamp_indice + 1) % 2, t] = probability[1, (timestamp_indice + 1) % 2, t-1] + feature[1, t]
            probability[2, (timestamp_indice + 1) % 2, t] = probability[2, (timestamp_indice + 1) % 2, t-1] + feature[2, t]
            probability[3, (timestamp_indice + 1) % 2, t] = probability[3, (timestamp_indice + 1) % 2, t-1] + feature[3, t]
            probability[4, (timestamp_indice + 1) % 2, t] = probability[4, (timestamp_indice + 1) % 2, t-1] + feature[4, t]

            

            probability[0, timestamp_indice % 2, t] = feature[0, t]
            probability[1, timestamp_indice % 2, t] = feature[1, t]
            probability[2, timestamp_indice % 2, t] = feature[2, t]
            probability[3, timestamp_indice % 2, t] = feature[3, t]
            probability[4, timestamp_indice % 2, t] = feature[4, t]

            timestamp_indice += 1



        else:

            probability[0, 0, t] = probability[0, 0, t-1] + feature[0, t]
            probability[1, 0, t] = probability[1, 0, t-1] + feature[1, t]
            probability[2, 0, t] = probability[2, 0, t-1] + feature[2, t]
            probability[3, 0, t] = probability[3, 0, t-1] + feature[3, t]
            probability[4, 0, t] = probability[4, 0, t-1] + feature[4, t]

            probability[0, 1, t] = probability[0, 1, t-1] + feature[0, t]
            probability[1, 1, t] = probability[1, 1, t-1] + feature[1, t]
            probability[2, 1, t] = probability[2, 1, t-1] + feature[2, t]
            probability[3, 1, t] = probability[3, 1, t-1] + feature[3, t]
            probability[4, 1, t] = probability[4, 1, t-1] + feature[4, t]
                
    for t in range(duration):

        for m in range(5):
            if np.sum(probability[m,0,t]) > 0:
                probability[m, 0, t] = probability[m, 0, t]/np.sum(probability[m, 0, t])


            else:
                probability[m, 0, t] = np.ones((nb_bloc_1))/nb_bloc_1


            if np.sum(probability[m,1,t]) > 0:
                probability[m, 1, t] = probability[m, 1, t]/np.sum(probability[m, 1, t])


            else:
                probability[m, 1, t] = np.ones((nb_bloc_1))/nb_bloc_1


    return probability