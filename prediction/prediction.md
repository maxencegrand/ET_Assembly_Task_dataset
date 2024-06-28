# Prediction

## Launch

* Model-Based:
``main.py``

* ML-Based
``main_lstm.py``

## Features Computation

File : ``feature_computation.py``

## Low Level

### Model Based

  file: ``low_level_naif.py``

### ML Based

  file : ``low_level_lstm.py``

## High Level

  file : ``interpretation.py``

## Results

Results are available in Modele_5_seed and ML_5_seeds (for ML just the Norme is missing and available in ML_Norme)

The 2 main file are results.csv and nb_prediction.csv

### results.csv

This file contains the number of correct predictions for the different eye tracker, for grasp/release, for the different surfaces and for the different features.

axis 0: size = 28, corresponds to the different surfaces and separates grasp/release

Grasp Surfaces Regulières Contigues de taille 4, validation permissive: [0]
Grasp Surfaces Regulières Contigues de taille 4, validation stricte: [8]
Grasp Surfaces Regulières Contigues de taille 8, validation permissive: [1]
Grasp Surfaces Regulières Contigues de taille 8, validation stricte: [9]
Grasp Surfaces Regulières Chevauchantes de taille 4, validation permissive: [2]
Grasp Surfaces Regulières Chevauchantes de taille 4, validation stricte: [10]
Grasp Surfaces Regulières Chevauchantes de taille 8, validation permissive: [3]
Grasp Surfaces Regulières Chevauchantes de taille 8, validation stricte: [11]
Grasp Surface semantique Level 0: [16]
Grasp Surface semantique Level 1: [19]
Grasp Surface semantique Level 2: [17]
Grasp Surface semantique Level 3: [18]
Grasp Surface semantique Level 4 (Block): [24]
Grasp Norme: [26]

Release Surfaces Regulières Contigues de taille 4, validation permissive: [4]
Release Surfaces Regulières Contigues de taille 4, validation stricte: [12]
Release Surfaces Regulières Contigues de taille 8, validation permissive: [5]
Release Surfaces Regulières Contigues de taille 8, validation stricte: [13]
Release Surfaces Regulières Chevauchantes de taille 4, validation permissive: [6]
Release Surfaces Regulières Chevauchantes de taille 4, validation stricte: [14]
Release Surfaces Regulières Chevauchantes de taille 8, validation permissive: [7]
Release Surfaces Regulières Chevauchantes de taille 8, validation stricte: [15]
Release Surface semantique Level 0: [20]
Release Surface semantique Level 1: [23]
Release Surface semantique Level 2: [21]
Release Surface semantique Level 3: [22]
Release Surface semantique Level 4 (Block): [25]
Release Norme: [27]

axis 1: size = 2, corresponds to head-mounted or remote

0 = head-mounted
1 = remote

axis 2: size = 5, corresponds to the differents feature

0 = OT_Count
1 = OT_Distance
2 = AT_Linear
3 = AT_Hyperbolic
4 = AT_Fitts

axis 3: size = 6001, corresponds to the time relative to the event under consideration. 6001 value for looking 3 seconds before and 3 seconds after.

### nb_prediction.csv

This file contains the number of predictions for the different eye tracker, for grasp/release and for the different surfaces.

axis 0 and axis 1 are the same as in results.csv. axis 2 is axis 3 from results.csv.

We have one less axis because all features have the same number of prediction.