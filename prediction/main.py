import numpy as np
import math
import os
import time
from datetime import datetime

os.environ["KERAS_BACKEND"] = "torch"
import keras

# Table dimension
largeur = 76
hauteur = 38
dist_min = -largeur / (2 * 48)

# Nb Fixe Zone
taille_zone = 1
nb_area_1 = int((48 / 1) * (24 / 1))
nb_area_2 = int((48 / 2) * (24 / 2))
nb_area_4 = int((48 / 4) * (24 / 4))
nb_area_8 = int((48 / 8) * (24 / 8))

# Read Zone
array_zone1 = np.genfromtxt("csv/zone_1x1.csv", delimiter=",")
array_zone2 = np.genfromtxt("csv/zone_2x2.csv", delimiter=",")
array_zone4 = np.genfromtxt("csv/zone_4x4.csv", delimiter=",")
array_zone8 = np.genfromtxt("csv/zone_8x8.csv", delimiter=",")

from feature_computation import parsingOneSituation
from low_lvl_naif import low_level_naif
from interpretation import interpretation
from analyse import (
    analyseSituation,
    analyseFixeAreaWeak,
    analyseFixeAreaStrong,
    analyseSlidingAreaWeak,
    analyseSlidingAreaStrong,
    analyseMethod,
    trueSemantic,
    analyseSemantic,
    analyseNorme,
    analyseSemanticBis,
)
from tools import (
    quadrillageRelease,
    quadrillageGrasp,
    liste_tenon_bloc,
    saveLog,
    listeTimneAction,
    CurrentWorld,
    savingTime,
    savingFeature,
    savingProba,
    savingInterpretation,
)
from seed import liste_seed

"""
parsingOneSituation parcours la liste des participants,
et pour chaque type de capteur (mobile/fixe),
pour chaque participant, pour chaque figure,
fait les differentes etapes menant aux predictions .
Les resultats sont enregistres dans un dossier de logs/ 
avec le timestamp comme nom

Input
-----
None

Output
-----
None
"""


def parsingAllParticipantOneMethode():

    # Obtention de la date et de l'heure actuelle
    date_heure_actuelle = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Nom du fichier avec la date et l'heure
    nom_dossier = f"logs/{date_heure_actuelle}"

    os.mkdir(nom_dossier)

    os.mkdir(nom_dossier + "/mobile")
    os.mkdir(nom_dossier + "/stationnary")

    os.mkdir(nom_dossier + "/mobile/sitting/")
    os.mkdir(nom_dossier + "/stationnary/sitting/")

    # Number of Features
    nb_predi = 5

    # Initialise l'emsemble des array permettant de stocker les résultats
    liste_analyse_methode_grasp_temps = [
        [[] for _ in range(nb_predi)] for _ in range(2)
    ]
    liste_analyse_methode_release_temps = [
        [[] for _ in range(nb_predi)] for _ in range(2)
    ]

    total_nb_grasp = [0 for _ in range(2)]
    total_nb_release = [0 for _ in range(2)]
    #4 pour taille 4/8 avec permissive/stricte
    #2 pour head-mounted/remote
    #nb_predi = nb feature
    #6001 pour 3 sec avant/apres l'event
    global_analyse_grasp_area_weak = np.zeros((4, 2, nb_predi, 6001))
    global_nb_analyse_grasp_area_weak = np.zeros((4, 2, 6001))
    global_analyse_release_area_weak = np.zeros((4, 2, nb_predi, 6001))
    global_nb_analyse_release_area_weak = np.zeros((4, 2, 6001))

    global_analyse_grasp_area_strong = np.zeros((4, 2, nb_predi, 6001))
    global_nb_analyse_grasp_area_strong = np.zeros((4, 2, 6001))
    global_analyse_release_area_strong = np.zeros((4, 2, nb_predi, 6001))
    global_nb_analyse_release_area_strong = np.zeros((4, 2, 6001))

    global_analyse_semantic_grasp = np.zeros((4, 2, nb_predi, 6001))
    global_nb_analyse_semantic_grasp = np.zeros((4, 2, 6001))
    global_analyse_semantic_release = np.zeros((4, 2, nb_predi, 6001))
    global_nb_analyse_semantic_release = np.zeros((4, 2, 6001))

    global_analyse_grasp_block = np.zeros((2, nb_predi, 6001))
    global_nb_analyse_grasp_block = np.zeros((2, 6001))
    global_analyse_release_block = np.zeros((2, nb_predi, 6001))
    global_nb_analyse_release_block = np.zeros((2, 6001))

    global_analyse_norme_grasp = np.zeros((2, nb_predi, 6001))
    global_nb_analyse_norme_grasp = np.zeros((2, 6001))
    global_analyse_norme_release = np.zeros((2, nb_predi, 6001))
    global_nb_analyse_norme_release = np.zeros((2, 6001))

    nb_analyse = 0

    norme_grasp = np.zeros((nb_predi))
    norme_release = np.zeros((nb_predi))

    nb_norme_grasp = 0
    nb_norme_release = 0

    duree_execution = [[], []]

    # recupere la liste des participants
    liste_participant_mobile = []
    liste_participant_sitting = []

    for method_pos, method in enumerate(["mobile", "stationnary"]):
        directory = "../dataset/" + method + "/sitting/"
        for entry in os.scandir(directory):
            if method == "mobile":
                liste_participant_mobile.append(entry.path)
            else:
                liste_participant_sitting.append(entry.path)

    liste_seeds = liste_seed()  # Run seeds

    # Pour chaque seed
    for seed in liste_seeds:
        print("seed", seed)
        # Split les participant en 80-20
        left_mobile, right_mobile = keras.utils.split_dataset(
            np.array(liste_participant_mobile),
            left_size=0.8,
            shuffle=True,
            seed=int(seed),
        )

        left_mobile_numpy = list(left_mobile)
        right_mobile_numpy = list(right_mobile)

        left_sitting, right_sitting = keras.utils.split_dataset(
            np.array(liste_participant_sitting),
            left_size=0.8,
            shuffle=True,
            seed=int(seed),
        )

        left_sitting_numpy = list(left_sitting)
        right_sitting_numpy = list(right_sitting)

        left = [left_mobile_numpy, left_sitting_numpy]
        right = [right_mobile_numpy, right_sitting_numpy]

        # On parcours les 20% des participants
        for method_pos, side in enumerate(right):

            if method_pos == 0:
                method = "mobile"
            else:
                method = "stationnary"

            # On parcours les figures faitent par les participants
            for number in side:
                participant = number.numpy().decode("utf-8")
                # os.mkdir(nom_dossier + "/" + method + "/" + "sitting/" + str(participant).split("/")[-1])
                for model in os.scandir(participant):
                    # verifie que les 2 fichiers existent

                    # On vérifie que les fichiers existent
                    if os.path.exists(
                        str(model.path) + "/table.csv"
                    ) and os.path.exists(str(model.path) + "/states.csv"):
                        # Affiche le participant et la figure traiter actuellement
                        print("---------------------------")
                        print(
                            "Partcipant :",
                            str(model.path).split("/")[-2],
                            str(model.path).split("/")[-1],
                            method_pos,
                        )

                        if method_pos == 0:
                            path = (
                                "mobile/sitting/"
                                + str(model.path).split("/")[-2]
                                + "/"
                                + str(model.path).split("/")[-1]
                                + "/"
                            )

                        else:
                            path = (
                                "stationnary/sitting/"
                                + str(model.path).split("/")[-2]
                                + "/"
                                + str(model.path).split("/")[-1]
                                + "/"
                            )

                        # charge les deux fichiers dans des np.array
                        gaze_point = np.genfromtxt(
                            str(model.path) + "/table.csv", delimiter=","
                        )

                        world = np.genfromtxt(
                            str(model.path) + "/states.csv", delimiter=","
                        )

                        # Ground truth / Label
                        proba_juste = np.zeros((world.shape[0] - 1, 2, nb_area_1))
                        # Pour chaque etat du monde
                        for t in range(1, world.shape[0]):
                            # Pour chaque bloc
                            for id_block in range(24):
                                # Si le bloc est held
                                if world[t, 10 * id_block + 10] == 1:

                                    taille_bloc = (((id_block // 3) % 2) + 1) * 4

                                    x0_grasp = round(
                                        (48 / largeur) * world[t, 10 * id_block + 1]
                                    )
                                    y0_grasp = round(
                                        (24 / hauteur) * world[t, 10 * id_block + 2]
                                    )

                                    x2_grasp = round(
                                        (48 / largeur) * world[t, 10 * id_block + 5]
                                    )
                                    y2_grasp = round(
                                        (48 / largeur) * world[t, 10 * id_block + 6]
                                    )

                                    for x_grasp in range(x0_grasp, x2_grasp):
                                        for y_grasp in range(y0_grasp, y2_grasp):
                                            proba_juste[t - 2][0][
                                                x_grasp * 24 + y_grasp
                                            ] += (1 / taille_bloc)
                                            proba_juste[t - 1][0][
                                                x_grasp * 24 + y_grasp
                                            ] += (1 / taille_bloc)

                                    x0_release = round(
                                        (48 / largeur) * world[t + 1, 10 * id_block + 1]
                                    )
                                    y0_release = round(
                                        (24 / hauteur) * world[t + 1, 10 * id_block + 2]
                                    )

                                    x2_release = round(
                                        (48 / largeur) * world[t + 1, 10 * id_block + 5]
                                    )
                                    y2_release = round(
                                        (48 / largeur) * world[t + 1, 10 * id_block + 6]
                                    )
                                    #On parcours les tenons du bloc
                                    for x_release in range(x0_release, x2_release):
                                        for y_release in range(y0_release, y2_release):
                                            proba_juste[t][1][
                                                x_release * 24 + y_release
                                            ] += (1 / taille_bloc)
                                            proba_juste[t - 1][1][
                                                x_release * 24 + y_release
                                            ] += (1 / taille_bloc)

                        duree = (
                            int(
                                max(world[-1, 0], gaze_point[-1, 0])
                                - min(world[1, 0], gaze_point[1, 0])
                            )
                            + 1
                        )

                        nb_gaze = gaze_point.shape[0] - 1

                        # recupere la liste des timestamp des evenements
                        timestamp_action = listeTimneAction(world)

                        all_feature = np.zeros((nb_predi, nb_gaze, nb_area_1))
                        probability_score = np.zeros((nb_predi, 2, nb_gaze, nb_area_1))
                        probability = np.zeros((nb_predi, 2, nb_gaze, nb_area_1))

                        t_init = world[1, 0]

                        indice = 0

                        liste_t_value = []

                        #Stock les meilleure surfaces pour chaque timestamp

                        temp_area4 = np.zeros((nb_predi, 2, nb_gaze))
                        temp_area8 = np.zeros((nb_predi, 2, nb_gaze))

                        temp_area_sliding_4 = np.zeros((nb_predi, 2, nb_gaze))
                        temp_area_sliding_8 = np.zeros((nb_predi, 2, nb_gaze))

                        temp_area_semantic_0 = np.zeros((nb_predi, 2, nb_gaze))
                        temp_area_semantic_1 = np.zeros((nb_predi, 2, nb_gaze))
                        temp_area_semantic_2 = np.zeros((nb_predi, 2, nb_gaze))

                        temp_block = np.zeros((nb_predi, 2, nb_gaze))

                        norme_array = np.zeros((nb_predi, 2, nb_gaze))

                        # On parcours les positions du regard dans l'ordre
                        for i in range(nb_gaze):
                            temps_feature = time.time()
                            # Recupere l'etat du monde correspondant a ce gaze point
                            current_world = CurrentWorld(gaze_point[i, 0], world)

                            gaze_value = gaze_point[i + 1]
                            t = gaze_value[0] - t_init
                            liste_t_value.append(t)

                            # calcul les differents indicateurs
                            (feature,) = parsingOneSituation(gaze_value)  # Compute feat

                            all_feature[:, i, :] = feature

                            temps_low_level = time.time()

                            #On recupère la somme des indicateurs depuis le dernier evenement
                            if i > 0:
                                past_probability_score = probability_score[
                                    :, :, i - 1, :
                                ]
                            else:
                                past_probability_score = probability_score[:, :, i, :]

                            # A partir des indicateurs on calcul la probabilité des tenons de zone
                            # new_indice correspond a l'etat du monde, si new_indice = indice on a pas changer l'etat du monde
                            new_probability, new_probability_score, new_indice = (
                                low_level_naif(
                                    feature,
                                    t,
                                    timestamp_action,
                                    indice,  # World state index
                                    past_probability_score,  # Previous feat sum
                                )
                            )

                            # Pour chaque predi on fait la diff entre le resultat obtenu et le ground truth
                            for f in range(nb_predi):
                                norme_array[f, 0, i] += np.linalg.norm(
                                    proba_juste[max(0, new_indice - 1)][0]
                                    - new_probability[f][0],
                                    ord=1,
                                )
                                norme_array[f, 1, i] += np.linalg.norm(
                                    proba_juste[max(0, new_indice - 1)][1]
                                    - new_probability[f][1],
                                    ord=1,
                                )

                            probability[:, :, i, :] = new_probability  # Proba
                            probability_score[:, :, i, :] = (
                                new_probability_score  # Feat sum
                            )

                            temps_interpretation = time.time()

                            # Retourne l'indice de la meilleure surface pour les différentes surfaces
                            [
                                area4max_indices,
                                area8max_indices,
                                area_best_4,
                                area_best_8,
                                semantic0,
                                semantic1,
                                semantic2,
                                liste_predi_id,
                            ] = interpretation(
                                new_probability,
                                new_indice,
                                world,
                                str(model.path).split("/")[-1],
                            )

                            temps_fin = time.time()

                            #Les variables temp_ ont une valeur par mesure du capteur, on met la meilleur surface correspondant au timestamp
                            temp_area4[:, :, i] = area4max_indices
                            temp_area8[:, :, i] = area8max_indices

                            temp_area_sliding_4[:, :, i] = area_best_4
                            temp_area_sliding_8[:, :, i] = area_best_8

                            temp_area_semantic_0[:, :, i] = semantic0
                            temp_area_semantic_1[:, :, i] = semantic1
                            temp_area_semantic_2[:, :, i] = semantic2

                            temp_block[:, :, i] = liste_predi_id

                            #indice de l'etat du monde
                            indice = new_indice

                            diff_feature = temps_low_level - temps_feature
                            diff_low_level = temps_interpretation - temps_low_level
                            diff_interpretation = temps_fin - temps_interpretation
                            diff_total = temps_fin - temps_feature

                            liste_temps_feature = [diff_feature]
                            liste_temps_low_level = [diff_low_level]
                            liste_temps_interpretation = [diff_interpretation]
                            liste_temps_total = [diff_total]

                            # os.mkdir(nom_dossier + "/" + path + "/" + str(int(gaze_point[i+1,0])))

                            # savingTime(nom_dossier,path,int(gaze_point[i+1,0]),"feature",liste_temps_feature)
                            # savingTime(nom_dossier,path,int(gaze_point[i+1,0]),"low level",liste_temps_low_level)
                            # savingTime(nom_dossier,path,int(gaze_point[i+1,0]),"interpretation",liste_temps_interpretation)
                            # savingTime(nom_dossier,path,int(gaze_point[i+1,0]),"total",liste_temps_total)
                            # savingFeature(nom_dossier,path,int(gaze_point[i+1,0]),all_feature)
                            # savingProba(nom_dossier,path,int(gaze_point[i+1,0]),probability)
                            # savingInterpretation(nom_dossier,path,int(gaze_point[i+1,0]),temp_area4,temp_area8,temp_area_sliding_4,temp_area_sliding_8,temp_block)

                        print(new_indice)

                        #permet d'avoir les meilleurs surface pour chaque ms
                        result_area4 = np.zeros((nb_predi, 2, duree))
                        result_area8 = np.zeros((nb_predi, 2, duree))
                        result_sliding_area4 = np.zeros((nb_predi, 2, duree))
                        result_sliding_area8 = np.zeros((nb_predi, 2, duree))
                        result_semantic_0 = np.zeros((nb_predi, 2, duree))
                        result_semantic_1 = np.zeros((nb_predi, 2, duree))
                        result_semantic_2 = np.zeros((nb_predi, 2, duree))
                        result_block = np.zeros((nb_predi, 2, duree))

                        result_norme = np.zeros((nb_predi, 2, duree))

                        time_indice = 0

                        # On passe des resultat pour chaque timestamp des mesures a une valeur par ms
                        for t in range(duree):
                            if (
                                time_indice < len(liste_t_value)
                                and t == liste_t_value[time_indice]
                            ):

                                result_area4[:, :, t] = temp_area4[:, :, time_indice]
                                result_area8[:, :, t] = temp_area8[:, :, time_indice]
                                result_sliding_area4[:, :, t] = temp_area_sliding_4[
                                    :, :, time_indice
                                ]
                                result_sliding_area8[:, :, t] = temp_area_sliding_8[
                                    :, :, time_indice
                                ]
                                result_semantic_0[:, :, t] = temp_area_semantic_0[
                                    :, :, time_indice
                                ]
                                result_semantic_1[:, :, t] = temp_area_semantic_1[
                                    :, :, time_indice
                                ]
                                result_semantic_2[:, :, t] = temp_area_semantic_2[
                                    :, :, time_indice
                                ]
                                result_block[:, :, t] = temp_block[:, :, time_indice]

                                result_norme[:, :, t] = norme_array[:, :, time_indice]

                                time_indice += 1

                            else:
                                result_area4[:, :, t] = result_area4[:, :, t - 1]
                                result_area8[:, :, t] = result_area8[:, :, t - 1]
                                result_sliding_area4[:, :, t] = result_sliding_area4[
                                    :, :, t - 1
                                ]
                                result_sliding_area8[:, :, t] = result_sliding_area8[
                                    :, :, t - 1
                                ]
                                result_semantic_0[:, :, t] = result_semantic_0[
                                    :, :, t - 1
                                ]
                                result_semantic_1[:, :, t] = result_semantic_1[
                                    :, :, t - 1
                                ]
                                result_semantic_2[:, :, t] = result_semantic_2[
                                    :, :, t - 1
                                ]
                                result_block[:, :, t] = result_block[:, :, t - 1]

                                result_norme[:, :, t] = result_norme[:, :, t - 1]

                        area_prediction = [
                            result_area4,
                            result_area8,
                            result_sliding_area4,
                            result_sliding_area8,
                        ]

                        block_prediction = result_block

                        # Durée d'exécution en secondes

                        duree_execution[method_pos].append(diff_total)

                        # Analyse des résultats

                        total_nb_grasp[method_pos] = (
                            total_nb_grasp[method_pos] + (len(timestamp_action) - 2) / 2
                        )
                        total_nb_release[method_pos] = (
                            total_nb_release[method_pos]
                            + (len(timestamp_action) - 2) / 2
                        )

                        nb_bloc = [nb_area_4, nb_area_8, nb_area_4, nb_area_8]
                        #Analyse zone reguliere contigue
                        for position, predi in enumerate(area_prediction):
                            liste_good_release_zones = quadrillageRelease(
                                world, nb_bloc[position]
                            )
                            liste_good_grasp_zones = quadrillageGrasp(
                                world, nb_bloc[position]
                            )
                            if position < len(area_prediction) / 2:
                                for posi, quadr in enumerate(predi):

                                    (
                                        analyse_area_grasp,
                                        nb_analyse_area_grasp,
                                        analyse_area_release,
                                        nb_analyse_area_release,
                                    ) = analyseFixeAreaWeak(
                                        quadr,
                                        liste_good_grasp_zones,
                                        liste_good_release_zones,
                                        timestamp_action,
                                        nb_bloc[position],
                                    )

                                    global_analyse_grasp_area_weak[position][
                                        method_pos
                                    ][posi] += analyse_area_grasp
                                    global_analyse_release_area_weak[position][
                                        method_pos
                                    ][posi] += analyse_area_release

                                    (
                                        analyse_area_grasp,
                                        nb_analyse_area_grasp,
                                        analyse_area_release,
                                        nb_analyse_area_release,
                                    ) = analyseFixeAreaStrong(
                                        quadr,
                                        liste_good_grasp_zones,
                                        liste_good_release_zones,
                                        timestamp_action,
                                        nb_bloc[position],
                                    )

                                    global_analyse_grasp_area_strong[position][
                                        method_pos
                                    ][posi] += analyse_area_grasp
                                    global_analyse_release_area_strong[position][
                                        method_pos
                                    ][posi] += analyse_area_release

                                global_nb_analyse_grasp_area_weak[position][
                                    method_pos
                                ] += nb_analyse_area_grasp
                                global_nb_analyse_release_area_weak[position][
                                    method_pos
                                ] += nb_analyse_area_release

                                global_nb_analyse_grasp_area_strong[position][
                                    method_pos
                                ] += nb_analyse_area_grasp
                                global_nb_analyse_release_area_strong[position][
                                    method_pos
                                ] += nb_analyse_area_release

                            else:

                                for posi, quadr in enumerate(predi):

                                    (
                                        analyse_area_grasp,
                                        nb_analyse_area_grasp,
                                        analyse_area_release,
                                        nb_analyse_area_release,
                                    ) = analyseSlidingAreaWeak(
                                        quadr,
                                        liste_good_grasp_zones,
                                        liste_good_release_zones,
                                        timestamp_action,
                                        nb_bloc[position],
                                    )

                                    global_analyse_grasp_area_weak[position][
                                        method_pos
                                    ][posi] += analyse_area_grasp
                                    global_analyse_release_area_weak[position][
                                        method_pos
                                    ][posi] += analyse_area_release

                                    (
                                        analyse_area_grasp,
                                        nb_analyse_area_grasp,
                                        analyse_area_release,
                                        nb_analyse_area_release,
                                    ) = analyseSlidingAreaStrong(
                                        quadr,
                                        liste_good_grasp_zones,
                                        liste_good_release_zones,
                                        timestamp_action,
                                        nb_bloc[position],
                                    )

                                    global_analyse_grasp_area_strong[position][
                                        method_pos
                                    ][posi] += analyse_area_grasp
                                    global_analyse_release_area_strong[position][
                                        method_pos
                                    ][posi] += analyse_area_release

                                global_nb_analyse_grasp_area_weak[position][
                                    method_pos
                                ] += nb_analyse_area_grasp
                                global_nb_analyse_release_area_weak[position][
                                    method_pos
                                ] += nb_analyse_area_release

                                global_nb_analyse_grasp_area_strong[position][
                                    method_pos
                                ] += nb_analyse_area_grasp
                                global_nb_analyse_release_area_strong[position][
                                    method_pos
                                ] += nb_analyse_area_release

                        result_semantic_1b = np.where(
                            result_semantic_1 == 2, 0, result_semantic_1
                        )

                        list_semantic = [
                            result_semantic_0,
                            result_semantic_1,
                            result_semantic_2,
                            result_semantic_1b,
                        ]

                        for lvl, semantic in enumerate(list_semantic):
                            for position, prediction in enumerate(semantic):
                                # Analyse max min dist
                                (
                                    analyse_grasp,
                                    nb_analyse_grasp,
                                    analyse_release,
                                    nb_analyse_release,
                                ) = analyseSemanticBis(
                                    world,
                                    prediction,
                                    timestamp_action,
                                    str(model.path).split("/")[-1],
                                    lvl,
                                )

                                global_analyse_semantic_grasp[lvl][method_pos][
                                    position
                                ] = (
                                    global_analyse_semantic_grasp[lvl][method_pos][
                                        position
                                    ]
                                    + analyse_grasp
                                )
                                global_analyse_semantic_release[lvl][method_pos][
                                    position
                                ] = (
                                    global_analyse_semantic_release[lvl][method_pos][
                                        position
                                    ]
                                    + analyse_release
                                )

                            global_nb_analyse_semantic_grasp[lvl][
                                method_pos
                            ] += nb_analyse_grasp
                            global_nb_analyse_semantic_release[lvl][
                                method_pos
                            ] += nb_analyse_release

                        for position, prediction in enumerate(block_prediction):
                            # Analyse max min dist
                            (
                                analyse_grasp,
                                nb_analyse_grasp,
                                analyse_release,
                                nb_analyse_release,
                            ) = analyseSituation(world, prediction, timestamp_action)

                            global_analyse_grasp_block[method_pos][position] = (
                                global_analyse_grasp_block[method_pos][position]
                                + analyse_grasp
                            )
                            global_analyse_release_block[method_pos][position] = (
                                global_analyse_release_block[method_pos][position]
                                + analyse_release
                            )

                        global_nb_analyse_grasp_block[method_pos] += nb_analyse_grasp
                        global_nb_analyse_release_block[
                            method_pos
                        ] += nb_analyse_release

                        print("analyse")
                        for position in range(nb_predi):
                            (
                                analyse_grasp,
                                nb_analyse_grasp,
                                analyse_release,
                                nb_analyse_release,
                            ) = analyseNorme(result_norme[position], timestamp_action)

                            global_analyse_norme_grasp[method_pos][
                                position
                            ] += analyse_grasp
                            global_analyse_norme_release[method_pos][
                                position
                            ] += analyse_release

                        global_nb_analyse_norme_grasp[method_pos] += nb_analyse_grasp
                        global_nb_analyse_norme_release[
                            method_pos
                        ] += nb_analyse_release

    results = np.zeros((28, 2, nb_predi, 6001))

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

    nb_prediction = np.zeros((28, 2, 6001))

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
    nb_prediction[19] = global_nb_analyse_semantic_grasp[3]
    nb_prediction[20] = global_nb_analyse_semantic_release[0]
    nb_prediction[21] = global_nb_analyse_semantic_release[1]
    nb_prediction[22] = global_nb_analyse_semantic_release[2]
    nb_prediction[23] = global_nb_analyse_semantic_release[3]
    nb_prediction[24] = global_nb_analyse_grasp_block
    nb_prediction[25] = global_nb_analyse_release_block
    nb_prediction[26] = global_nb_analyse_norme_grasp
    nb_prediction[27] = global_nb_analyse_norme_release

    nom_dossier = saveLog(nom_dossier, results, nb_prediction, duree_execution)


if __name__ == "__main__":
    parsingAllParticipantOneMethode()
