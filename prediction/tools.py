import numpy as np
import math

import os
from datetime import datetime
import json
import csv


plot_1 = False
analyse = True
plot_analyse = False

largeur = 76
hauteur = 38
dist_min = -largeur / (2 * 48)

taille_zone = 1
nb_area_1 = int((48 / 1) * (24 / 1))
nb_area_2 = int((48 / 2) * (24 / 2))
nb_area_4 = int((48 / 4) * (24 / 4))
nb_area_8 = int((48 / 8) * (24 / 8))

array_zone1 = np.genfromtxt("csv/zone_1x1.csv", delimiter=",")
array_zone2 = np.genfromtxt("csv/zone_2x2.csv", delimiter=",")
array_zone4 = np.genfromtxt("csv/zone_4x4.csv", delimiter=",")
array_zone8 = np.genfromtxt("csv/zone_8x8.csv", delimiter=",")


# Permet de transformer de le format pour le type de device en int
# 0 -> table, 1 -> screen, 2-> no data
# input : str or int
# output: int
def deviceToInt(dev):
    if dev == "Device.TABLE" or dev == 0:
        return 0
    if dev == "Device.SCREEN" or dev == 1:
        return 1
    return 2


# Function to return the minimum distance
# between a line segment AB and a point E
# x1, y1 for point A
# x2, y2 for point B
# xp, yp for point E
# input : x1,y1,x2,y2,xp,yp (all float)
# output: float
def minDistance(x1, y1, x2, y2, xp, yp):

    # vector AB
    AB = [x2 - x1, y2 - y1]

    # vector BP
    BE = [xp - x2, yp - y2]

    # vector AP
    AE = [xp - x1, yp - y1]

    # Variables to store dot product
    # Calculating the dot product
    BA_BE = -AB[0] * BE[0] + -AB[1] * BE[1]
    AB_AE = AB[0] * AE[0] + AB[1] * AE[1]

    # Minimum distance from
    # point E to the line segment
    reqAns = 0

    # Case 1
    if BA_BE < 0:
        # Finding the magnitude
        y = yp - y2
        x = xp - x2
        reqAns = math.sqrt(x * x + y * y)

    # Case 2
    elif AB_AE < 0:
        y = yp - y1
        x = xp - x1
        reqAns = math.sqrt(x * x + y * y)

    # Case 3
    else:
        # Finding the perpendicular distance
        xAB = AB[0]
        yAB = AB[1]
        xAE = AE[0]
        yAE = AE[1]
        mod = math.sqrt(xAB * xAB + yAB * yAB)
        reqAns = abs(xAB * yAE - yAB * xAE) / mod

    return reqAns


# input : x1,y1 coordonne du point en haut a gauche d'un rectangle (float)
# x3,y3 coordonne du point en bas a droite d'un rectangle (float)
# xp,yp coordonne d'un point (float)
# output: True si le point (xp,yp)  est strictement dans le rectangle
def inRectangle(x1, y1, x3, y3, xp, yp):
    return x1 < xp and xp < x3 and y1 < yp and yp < y3


# Regarde la distance entre un point et les 4 aretes d'un rectangle et renvoie la plus petite des distances
# input : 4 points formant un rectangle et un point (xp,yp), les 10 variables en float
# output: la distance la plus petite en float
def minDistanceRectangleGaze(x1, y1, x2, y2, x3, y3, x4, y4, xp, yp):

    d1 = minDistance(x1, y1, x2, y2, xp, yp)
    d2 = minDistance(x2, y2, x3, y3, xp, yp)
    d3 = minDistance(x3, y3, x4, y4, xp, yp)
    d4 = minDistance(x4, y4, x1, y1, xp, yp)

    dmin = min(d1, d2)
    dmin = min(dmin, d3)
    dmin = min(dmin, d4)

    if inRectangle(x1, y1, x3, y3, xp, yp):
        dmin = -dmin

    return dmin


# Parcours les 24 rectangles et renvoie l'id du rectangle le plus proche de (xp,yp) ainsi que la distance
# input : -current_world : np.array[1,251]
#        -xp,yp : les coordonnees d'un point (float)
# output: -id_min : int entre 0 et 23 inclus
#        -distance_min : float
def moreCloseRectangle(current_world, xp, yp):

    distance_min = math.inf
    id_min = -1

    for rect in range(0, 24):
        id = rect
        x1 = current_world[10 * rect + 1]
        y1 = current_world[10 * rect + 2]
        x2 = current_world[10 * rect + 3]
        y2 = current_world[10 * rect + 4]
        x3 = current_world[10 * rect + 5]
        y3 = current_world[10 * rect + 6]
        x4 = current_world[10 * rect + 7]
        y4 = current_world[10 * rect + 8]

        d = minDistanceRectangleGaze(x1, y1, x2, y2, x3, y3, x4, y4, xp, yp)

        if d < distance_min:
            distance_min = d
            id_min = id

    return id_min, distance_min


# input :  -current_world : np.array[1,251]
# output : - bool : True si un bloc est attrape, sinon False
def isHolding(current_world):
    for indice in range(24):
        if current_world[10 * indice + 10] == 1:
            return True
    return False


# prend un point et renvoi la position sur la table le plus proche
# input : -xp,yp (float): coordonne
# output : -x,y (float) : coordonnee de la table le plus proche
def trouverEmplacement(xp, yp):
    d_min = math.inf
    x_min = -1
    y_min = -1
    for x in range(49):
        for y in range(25):
            d = math.sqrt((76 * x / 48 - xp) ** 2 + (38 * y / 24 - yp) ** 2)
            if d < d_min:
                d_min = d
                x_min = 76 * x / 48
                y_min = 38 * y / 24
    return x_min, y_min, d_min


#Renvoi l'etat du monde au temps timestamp
#input: timestamp: int : correspond au timestamp pour lequel on veut l'etat du monde
#       world: array[*,241]: correspond a l'ensemble des etats du monde
#ouput: array de 241 valeur correspondant a l'etat du monde
def CurrentWorld(timestamp, world):
    for i in range(2, world.shape[0]):
        if world[i - 1, 0] <= timestamp and timestamp < world[i, 0]:
            return world[i - 1]
    return world[-1]

#Renvoi la liste des blocs pris ainsi que le timestamp auquel ils sont pris
#input: world : array[-,241] : correspond a l'ensemble des etats du monde
def listeHolding(world):
    liste = []
    liste_t = []
    for i in range(1, world.shape[0]):
        for indice in range(24):
            if world[i, 10 * indice + 10] == 1:
                liste.append(indice)
                liste_t.append(int(world[i, 0] - world[1, 0]) - 1)

    return liste, liste_t

#
#
#
def timeGraspRelease(world, last_time):
    time_grasp = 0
    time_release = 0
    for i in range(1, world.shape[0] - 1):
        holding = False
        for indice in range(24):
            if world[i, 10 * indice + 10] == 1:
                holding = True

        if holding:
            time_release += world[i + 1, 0] - world[i, 0]
        else:
            time_grasp += world[i + 1, 0] - world[i, 0]

    holding = False
    for indice in range(24):
        if world[-1, 10 * indice + 10] == 1:
            holding = True

    if holding:
        time_release += last_time - world[-1, 0]
    else:
        time_grasp += last_time - world[-1, 0]

    return time_grasp, time_release

#renvoi vrai si les blocs i et j sont adjacents, faux sinon
#current_world: array[241]
#i,j : int: id de bloc
#output: bool
def adjacent(current_world, i, j):

    i_x0 = current_world[10 * i + 1]
    i_y0 = current_world[10 * i + 2]
    i_x1 = current_world[10 * i + 3]
    i_y1 = current_world[10 * i + 4]
    i_x2 = current_world[10 * i + 5]
    i_y2 = current_world[10 * i + 6]
    i_x3 = current_world[10 * i + 7]
    i_y3 = current_world[10 * i + 8]

    j_x0 = current_world[10 * j + 1]
    j_y0 = current_world[10 * j + 2]
    j_x1 = current_world[10 * j + 3]
    j_y1 = current_world[10 * j + 4]
    j_x2 = current_world[10 * j + 5]
    j_y2 = current_world[10 * j + 6]
    j_x3 = current_world[10 * j + 7]
    j_y3 = current_world[10 * j + 8]

    count = 0

    d_j_0 = minDistanceRectangleGaze(
        i_x0, i_y0, i_x1, i_y1, i_x2, i_y2, i_x3, i_y3, j_x0, j_y0
    )
    if d_j_0 <= 0:
        count += 1
    d_j_1 = minDistanceRectangleGaze(
        i_x0, i_y0, i_x1, i_y1, i_x2, i_y2, i_x3, i_y3, j_x1, j_y1
    )
    if d_j_1 <= 0:
        count += 1
    d_j_2 = minDistanceRectangleGaze(
        i_x0, i_y0, i_x1, i_y1, i_x2, i_y2, i_x3, i_y3, j_x2, j_y2
    )
    if d_j_2 <= 0:
        count += 1
    d_j_3 = minDistanceRectangleGaze(
        i_x0, i_y0, i_x1, i_y1, i_x2, i_y2, i_x3, i_y3, j_x3, j_y3
    )
    if d_j_3 <= 0:
        count += 1

    d_i_0 = minDistanceRectangleGaze(
        j_x0, j_y0, j_x1, j_y1, j_x2, j_y2, j_x3, j_y3, i_x0, i_y0
    )
    if d_i_0 <= 0:
        count += 1
    d_i_1 = minDistanceRectangleGaze(
        j_x0, j_y0, j_x1, j_y1, j_x2, j_y2, j_x3, j_y3, i_x1, i_y1
    )
    if d_i_1 <= 0:
        count += 1
    d_i_2 = minDistanceRectangleGaze(
        j_x0, j_y0, j_x1, j_y1, j_x2, j_y2, j_x3, j_y3, i_x2, i_y2
    )
    if d_i_2 <= 0:
        count += 1
    d_i_3 = minDistanceRectangleGaze(
        j_x0, j_y0, j_x1, j_y1, j_x2, j_y2, j_x3, j_y3, i_x3, i_y3
    )
    if d_i_3 <= 0:
        count += 1

    if count > 2:
        return True

    if count == 2 and not (
        (i_x0 == j_x2 and i_y0 == j_y2)
        or (i_x1 == j_x3 and i_y1 == j_y3)
        or (i_x2 == j_x0 and i_y2 == j_y0)
        or (i_x3 == j_x1 and i_y3 == j_y1)
    ):
        return True

    return False

#renvoi pour chaque etat du monde la liste de bloc adjacent au bloc posé par l'humain
def listeAdjacentRelease(world):
    liste_adjacent = []
    for i in range(2, world.shape[0]):
        for indice in range(24):
            if world[i - 1, 10 * indice + 10] == 1:
                liste_adjacent_i = []
                for rect in range(24):
                    if rect != indice and adjacent(world[i], rect, indice):
                        liste_adjacent_i.append(rect)
                liste_adjacent.append(liste_adjacent_i)
    return liste_adjacent

#renvoi pour chaque etat du monde la liste de bloc de reference lors des releases
def listeRelease(world):
    liste_release = []

    liste_adjacent = listeAdjacentRelease(world)

    for i in range(2, world.shape[0]):
        for indice in range(24):
            if world[i - 1, 10 * indice + 10] == 1:

                d_min = math.inf
                for rect in range(24):
                    if d_min > 0 and rect != indice:
                        d1 = minDistanceRectangleGaze(
                            world[i, 10 * rect + 1],
                            world[i, 10 * rect + 2],
                            world[i, 10 * rect + 3],
                            world[i, 10 * rect + 4],
                            world[i, 10 * rect + 5],
                            world[i, 10 * rect + 6],
                            world[i, 10 * rect + 7],
                            world[i, 10 * rect + 8],
                            world[i, 10 * indice + 1],
                            world[i, 10 * indice + 2],
                        )

                        d2 = minDistanceRectangleGaze(
                            world[i, 10 * rect + 1],
                            world[i, 10 * rect + 2],
                            world[i, 10 * rect + 3],
                            world[i, 10 * rect + 4],
                            world[i, 10 * rect + 5],
                            world[i, 10 * rect + 6],
                            world[i, 10 * rect + 7],
                            world[i, 10 * rect + 8],
                            world[i, 10 * indice + 3],
                            world[i, 10 * indice + 4],
                        )

                        d3 = minDistanceRectangleGaze(
                            world[i, 10 * rect + 1],
                            world[i, 10 * rect + 2],
                            world[i, 10 * rect + 3],
                            world[i, 10 * rect + 4],
                            world[i, 10 * rect + 5],
                            world[i, 10 * rect + 6],
                            world[i, 10 * rect + 7],
                            world[i, 10 * rect + 8],
                            world[i, 10 * indice + 5],
                            world[i, 10 * indice + 6],
                        )

                        d4 = minDistanceRectangleGaze(
                            world[i, 10 * rect + 1],
                            world[i, 10 * rect + 2],
                            world[i, 10 * rect + 3],
                            world[i, 10 * rect + 4],
                            world[i, 10 * rect + 5],
                            world[i, 10 * rect + 6],
                            world[i, 10 * rect + 7],
                            world[i, 10 * rect + 8],
                            world[i, 10 * indice + 7],
                            world[i, 10 * indice + 8],
                        )

                        d = max(0, min(d1, min(d2, min(d3, d4))))

                        if d < d_min:
                            d_min = d

                liste_adjacent_i = []

                if d_min > 0:
                    for rect in range(24):
                        if rect != indice and (
                            minDistanceRectangleGaze(
                                world[i, 10 * rect + 1],
                                world[i, 10 * rect + 2],
                                world[i, 10 * rect + 3],
                                world[i, 10 * rect + 4],
                                world[i, 10 * rect + 5],
                                world[i, 10 * rect + 6],
                                world[i, 10 * rect + 7],
                                world[i, 10 * rect + 8],
                                world[i, 10 * indice + 1],
                                world[i, 10 * indice + 2],
                            )
                            < d_min + 0.1
                            or minDistanceRectangleGaze(
                                world[i, 10 * rect + 1],
                                world[i, 10 * rect + 2],
                                world[i, 10 * rect + 3],
                                world[i, 10 * rect + 4],
                                world[i, 10 * rect + 5],
                                world[i, 10 * rect + 6],
                                world[i, 10 * rect + 7],
                                world[i, 10 * rect + 8],
                                world[i, 10 * indice + 3],
                                world[i, 10 * indice + 4],
                            )
                            < d_min + 0.1
                            or minDistanceRectangleGaze(
                                world[i, 10 * rect + 1],
                                world[i, 10 * rect + 2],
                                world[i, 10 * rect + 3],
                                world[i, 10 * rect + 4],
                                world[i, 10 * rect + 5],
                                world[i, 10 * rect + 6],
                                world[i, 10 * rect + 7],
                                world[i, 10 * rect + 8],
                                world[i, 10 * indice + 5],
                                world[i, 10 * indice + 6],
                            )
                            < d_min + 0.1
                            or minDistanceRectangleGaze(
                                world[i, 10 * rect + 1],
                                world[i, 10 * rect + 2],
                                world[i, 10 * rect + 3],
                                world[i, 10 * rect + 4],
                                world[i, 10 * rect + 5],
                                world[i, 10 * rect + 6],
                                world[i, 10 * rect + 7],
                                world[i, 10 * rect + 8],
                                world[i, 10 * indice + 7],
                                world[i, 10 * indice + 8],
                            )
                            < d_min + 0.1
                        ):
                            liste_adjacent_i.append(rect)

                else:
                    liste_adjacent_i = liste_adjacent[len(liste_release)]
                liste_release.append(liste_adjacent_i)
    return liste_release

#renvoi les coordonnées des blocs grasp
def quadrillageGrasp(world, nb_bloc):
    l = []
    for i in range(1, world.shape[0] - 1):
        for indice in range(24):
            if world[i + 1, 10 * indice + 10] == 1:
                l.append(
                    [
                        world[i, 10 * indice + 1],
                        world[i, 10 * indice + 2],
                        world[i, 10 * indice + 3],
                        world[i, 10 * indice + 4],
                        world[i, 10 * indice + 5],
                        world[i, 10 * indice + 6],
                        world[i, 10 * indice + 7],
                        world[i, 10 * indice + 8],
                    ]
                )

    return l

#renvoi les coordonnées des blocs release
def quadrillageRelease(world, nb_bloc):
    l = []
    for i in range(2, world.shape[0]):
        for indice in range(24):
            if world[i - 1, 10 * indice + 10] == 1:
                l.append(
                    [
                        world[i, 10 * indice + 1],
                        world[i, 10 * indice + 2],
                        world[i, 10 * indice + 3],
                        world[i, 10 * indice + 4],
                        world[i, 10 * indice + 5],
                        world[i, 10 * indice + 6],
                        world[i, 10 * indice + 7],
                        world[i, 10 * indice + 8],
                    ]
                )

    return l

#renvoi la surface reguliere contigue dans laquelle se situe le bloc dent on donne les coordonnees en entrée
def BlockToZoneID(x0, y0, x1, y1, x2, y2, x3, y3, nb_bloc):

    nb_bloc_x = int(2 * math.sqrt(nb_bloc / 2))
    nb_bloc_y = int(math.sqrt(nb_bloc / 2))

    taille = 48 / nb_bloc_x

    # id bloc contenant x0,y0
    bloc_x0 = int((48 * x0 / largeur) // taille)
    bloc_y0 = int((24 * y0 / hauteur) // taille)
    id_x0 = nb_bloc_y * bloc_x0 + bloc_y0

    # id bloc contenant x1,y1
    bloc_x1 = int((48 * x1 / largeur) // taille)
    bloc_y1 = int((24 * y1 / hauteur) // taille)
    id_x1 = nb_bloc_y * bloc_x1 + bloc_y1

    # id bloc contenant x2,y2
    bloc_x2 = int((48 * x2 / largeur) // taille)
    bloc_y2 = int((24 * y2 / hauteur) // taille)
    id_x2 = nb_bloc_y * bloc_x2 + bloc_y2

    # id bloc contenant x3,y3
    bloc_x3 = int((48 * x3 / largeur) // taille)
    bloc_y3 = int((24 * y3 / hauteur) // taille)
    id_x3 = nb_bloc_y * bloc_x3 + bloc_y3

    # Si le s4 coins sont dans la meme zone
    if id_x0 == id_x1 and id_x0 == id_x2 and id_x0 == id_x3:
        return [id_x0]

    # Sinon on rajoute les zone contenant le centre du bloc (on regarde 4 points proche du centrepour si le centre est sur la jonction entre 2 zones => probeleme d'arrondi on aurait qu'une zone)
    else:
        x_mean = (x0 + x1 + x2 + x3) / 4
        y_mean = (y0 + y1 + y2 + y3) / 4

        bloc_x_mean_0 = int((48 * (x_mean - 0.1) / largeur) // taille)
        bloc_y_mean_0 = int((24 * (y_mean - 0.1) / hauteur) // taille)
        id_x_mean_0 = nb_bloc_y * bloc_x_mean_0 + bloc_y_mean_0

        bloc_x_mean_1 = int((48 * (x_mean + 0.1) / largeur) // taille)
        bloc_y_mean_1 = int((24 * (y_mean - 0.1) / hauteur) // taille)
        id_x_mean_1 = nb_bloc_y * bloc_x_mean_1 + bloc_y_mean_1

        bloc_x_mean_2 = int((48 * (x_mean + 0.1) / largeur) // taille)
        bloc_y_mean_2 = int((24 * (y_mean + 0.1) / hauteur) // taille)
        id_x_mean_2 = nb_bloc_y * bloc_x_mean_2 + bloc_y_mean_2

        bloc_x_mean_3 = int((48 * (x_mean - 0.1) / largeur) // taille)
        bloc_y_mean_3 = int((24 * (y_mean + 0.1) / hauteur) // taille)
        id_x_mean_3 = nb_bloc_y * bloc_x_mean_3 + bloc_y_mean_3

        l = [id_x_mean_0]

        if id_x_mean_1 not in l:
            l.append(id_x_mean_1)

        if id_x_mean_2 not in l:
            l.append(id_x_mean_2)

        if id_x_mean_3 not in l:
            l.append(id_x_mean_3)

        return l


# Liste des tenons (pour zone 1x1) sur lesquelles sont les blocs
def liste_tenon_bloc(world):

    liste_result = [[[] for _ in range(24)] for _ in range(world.shape[0] - 1)]

    for i in range(1, world.shape[0]):
        for r in range(24):
            x0 = round((48 / largeur) * world[i, r * 10 + 1])
            y0 = round((24 / hauteur) * world[i, r * 10 + 2])
            x2 = round((48 / largeur) * world[i, r * 10 + 5])
            y2 = round((24 / hauteur) * world[i, r * 10 + 6])

            for x in range(x0, x2):
                for y in range(y0, y2):
                    liste_result[i - 1][r].append(x * 24 + y)

    return liste_result

#Sauvegarde les resultats dans le dossier nom_fichier
def saveLog(nom_fichier, results, nb_prediction, duree_execution):

    np.savetxt(
        nom_fichier + "/results.csv", results.reshape(28, -1), delimiter=",", fmt="%.4f"
    )
    np.savetxt(
        nom_fichier + "/nb_prediction.csv",
        nb_prediction.reshape(28, -1),
        delimiter=",",
        fmt="%.4f",
    )

    with open(nom_fichier + "/time.csv", "w", newline="") as fichier_csv:
        writer = csv.writer(fichier_csv)

        # Écrire chaque sous-liste dans une ligne du fichier CSV
        for sous_liste in duree_execution:
            writer.writerow(sous_liste)

    return nom_fichier

#Charge les resultats du dossier nom_fichier
def loadLog(nom_fichier):
    results = np.genfromtxt(nom_fichier + "/results.csv", delimiter=",")
    nb_prediction = np.genfromtxt(nom_fichier + "/nb_prediction.csv", delimiter=",")
    # duree_execution = np.genfromtxt(nom_fichier + "_time.csv", delimiter=",")
    duree_execution = []
    with open(nom_fichier + "/time.csv", "r", newline="") as fichier_csv:
        reader = csv.reader(fichier_csv)

        # Lire chaque ligne du fichier CSV
        for ligne in reader:
            # Convertir les éléments de la ligne en int si nécessaire
            ligne = [float(element) for element in ligne]
            # Ajouter la ligne lue à la liste de données lues
            duree_execution.append(ligne)
    return results, nb_prediction, duree_execution

#Renvoi la durée entre 2 evenements pour toutes les evenements d'un assemblage
def listeTimneAction(world):
    liste = []
    t_init = world[1, 0]
    for t in range(1, world.shape[0]):
        k = world[t, 0]
        liste.append(int(k - t_init))

    return liste

#Sauvergarde la durée d'exec
def savingTime(nom_dossier, participant, timestamp, type_time, duree):

    with open(
        nom_dossier
        + "/"
        + participant
        + str(timestamp)
        + "/time_"
        + type_time
        + ".csv",
        "w",
        newline="",
    ) as fichier_csv:
        writer = csv.writer(fichier_csv)

        writer.writerow(duree)

    return

#Sauvergarde la durée d'exec pour calcul indicateur
def savingFeature(nom_dossier, participant, timestamp, feature):

    np.savetxt(
        nom_dossier + "/" + participant + str(timestamp) + "/" + "feature.csv",
        feature[:, :, :].reshape(5, -1),
        delimiter=",",
        fmt="%.4f",
    )

    return

#Sauvergarde la durée d'exec pour calcul bas niveau
def savingProba(nom_dossier, participant, timestamp, proba):

    np.savetxt(
        nom_dossier + "/" + participant + str(timestamp) + "/probability.csv",
        proba.reshape(10, -1),
        delimiter=",",
        fmt="%.4f",
    )

    return

#Sauvergarde la durée d'exec pour calcul haut niveau
def savingInterpretation(
    nom_dossier,
    participant,
    timestamp,
    temp_area4,
    temp_area8,
    temp_area_sliding_4,
    temp_area_sliding_8,
    temp_block,
):

    np.savetxt(
        nom_dossier + "/" + participant + str(timestamp) + "/inter_area4.csv",
        temp_area4.reshape(10, -1),
        delimiter=",",
        fmt="%.4f",
    )
    np.savetxt(
        nom_dossier + "/" + participant + str(timestamp) + "/inter_area8.csv",
        temp_area8.reshape(10, -1),
        delimiter=",",
        fmt="%.4f",
    )

    np.savetxt(
        nom_dossier + "/" + participant + str(timestamp) + "/inter_area_sliding.csv",
        temp_area_sliding_4.reshape(10, -1),
        delimiter=",",
        fmt="%.4f",
    )
    np.savetxt(
        nom_dossier + "/" + participant + str(timestamp) + "/inter_area_sliding.csv",
        temp_area_sliding_8.reshape(10, -1),
        delimiter=",",
        fmt="%.4f",
    )

    np.savetxt(
        nom_dossier + "/" + participant + str(timestamp) + "/inter_block.csv",
        temp_block.reshape(10, -1),
        delimiter=",",
        fmt="%.4f",
    )

    return
