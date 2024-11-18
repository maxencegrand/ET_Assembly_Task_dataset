import numpy as np
import sys
from tools import loadLog
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

nb_predi = 5

def value_eyetracker(i):
    if i == 0:
        return "head_monted"
    else:
        return "remote"

def value_feature(i):
    if i == 2:
        return "linear"
    else:
        return "hyperbolic"
    
if __name__ == "__main__":
    nom_fichier_ML = "ML_5_seeds"
    results_ML, nb_prediction, duree_execution = loadLog(nom_fichier_ML)
    array_results_ML = results_ML.reshape(28, 2, nb_predi, 6001)

    nom_fichier_Mod = "Modele_5_seed"
    results_Mod, nb_prediction, duree_execution = loadLog(nom_fichier_ML)
    array_results_Mod = results_Mod.reshape(28, 2, nb_predi, 6001)

    

    for ax0 in [17,21]: #17 = Grasp Surface Semantique level 2
                        #21 = Release Surface Semantique level 2
        liste_value = []
        liste_approch = []
        liste_eyetracker = []
        liste_feature = []

        for ax1 in [0,1]:#0 = head mount, 1 = remote

            for ax2 in [2,3]:# 2 = linear, 3 = hyperbolic

                for ax3 in range(3001):# On regarde les 3 secondes precedent l'action
                    liste_value.append(array_results_ML[ax0,ax1,ax2,ax3])
                    liste_approch.append("Machine_Learning")
                    liste_eyetracker.append(value_eyetracker(ax1))
                    liste_feature.append(value_feature(ax2))

                    liste_value.append(array_results_Mod[ax0,ax1,ax2,ax3])
                    liste_approch.append("Modele")
                    liste_eyetracker.append(value_eyetracker(ax1))
                    liste_feature.append(value_feature(ax2))


        data = {
            'Taux_bonne_prediction': liste_value,  # Remplir avec les valeurs du taux
            'Approche': liste_approch,  # Remplir avec l'approche correspondant aux valeurs
            'Oculometre': liste_eyetracker,  # Remplir avec le type d'oculomètre correspondant
            'Feature': liste_feature  # Remplir avec le type de feature utilisé
        }
        
        df = pd.DataFrame(data)

        # Création du modèle ANOVA
        model = ols('Taux_bonne_prediction ~ C(Approche) * C(Oculometre) * C(Feature)', data=df).fit()
        anova_table = sm.stats.anova_lm(model, typ=3)

        # Affichage des résultats
        if ax0 == 17:
            print("Grasp Surface Sémantique level 2\n")
        if ax0 == 21:
            print("Release Surface Sémantique level 2\n")

        print(anova_table)
        print("\n")
