import numpy as np
import csv

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


def generateTableZone():
    x0 = 0
    y0 = 2

    x2 = 48
    y2 = 20

    data = [["x0", "y0", "x2", "y2"], [x0, y0, x2, y2]]

    # Écrire les données dans le fichier CSV
    with open("csv/zone_table.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def generateLeftZone():
    x0 = 0
    y0 = 2

    x2 = 10
    y2 = 20

    data = [["x0", "y0", "x2", "y2"], [x0, y0, x2, y2]]

    # Écrire les données dans le fichier CSV
    with open("csv/zone_left.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def generateMiddleZone():
    x0 = 14
    y0 = 4

    x2 = 34
    y2 = 18

    data = [["x0", "y0", "x2", "y2"], [x0, y0, x2, y2]]
    # Écrire les données dans le fichier CSV
    with open("csv/zone_middle.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def generateRightZone():
    x0 = 38
    y0 = 2

    x2 = 48
    y2 = 20

    data = [["x0", "y0", "x2", "y2"], [x0, y0, x2, y2]]

    # Écrire les données dans le fichier CSV
    with open("csv/zone_right.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def generateBlueZone():
    x0 = 0
    y0 = 2

    x2 = 10
    y2 = 10

    data = [["x0", "y0", "x2", "y2"], [x0, y0, x2, y2]]

    # Écrire les données dans le fichier CSV
    with open("csv/zone_blue.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def generateRedZone():
    x0 = 0
    y0 = 12

    x2 = 10
    y2 = 20

    data = [["x0", "y0", "x2", "y2"], [x0, y0, x2, y2]]

    # Écrire les données dans le fichier CSV
    with open("csv/zone_red.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def generateGreenZone():
    x0 = 38
    y0 = 2

    x2 = 48
    y2 = 10

    data = [["x0", "y0", "x2", "y2"], [x0, y0, x2, y2]]

    # Écrire les données dans le fichier CSV
    with open("csv/zone_green.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def generateYellowZone():
    x0 = 38
    y0 = 12

    x2 = 48
    y2 = 20

    data = [["x0", "y0", "x2", "y2"], [x0, y0, x2, y2]]

    # Écrire les données dans le fichier CSV
    with open("csv/zone_yellow.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def generateCarZone():
    x0 = 21
    y0 = 8

    x2 = 27
    y2 = 16

    data = [["x0", "y0", "x2", "y2"], [x0, y0, x2, y2]]

    # Écrire les données dans le fichier CSV
    with open("csv/zone_car.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def generateHouseZone():
    x0 = 19
    y0 = 4

    x2 = 27
    y2 = 16

    data = [["x0", "y0", "x2", "y2"], [x0, y0, x2, y2]]

    # Écrire les données dans le fichier CSV
    with open("csv/zone_house.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def generateScZone():
    x0 = 19
    y0 = 8

    x2 = 31
    y2 = 14

    data = [["x0", "y0", "x2", "y2"], [x0, y0, x2, y2]]

    # Écrire les données dans le fichier CSV
    with open("csv/zone_sc.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def generateTbZone():
    x0 = 23
    y0 = 8

    x2 = 29
    y2 = 10

    data = [["x0", "y0", "x2", "y2"], [x0, y0, x2, y2]]

    # Écrire les données dans le fichier CSV
    with open("csv/zone_tb.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def generateTcZone():
    x0 = 19
    y0 = 6

    x2 = 29
    y2 = 12

    data = [["x0", "y0", "x2", "y2"], [x0, y0, x2, y2]]

    # Écrire les données dans le fichier CSV
    with open("csv/zone_tc.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def generateTsbZone():
    x0 = 23
    y0 = 8

    x2 = 33
    y2 = 14

    data = [["x0", "y0", "x2", "y2"], [x0, y0, x2, y2]]

    # Écrire les données dans le fichier CSV
    with open("csv/zone_tsb.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


generateTableZone()
generateLeftZone()
generateMiddleZone()
generateRightZone()
generateBlueZone()
generateRedZone()
generateGreenZone()
generateYellowZone()
generateCarZone()
generateHouseZone()
generateScZone()
generateTbZone()
generateTcZone()
generateTsbZone()
