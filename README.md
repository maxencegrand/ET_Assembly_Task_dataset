# Eye Tracking Assembly Task dataset

This work is a part of the LIG-SIC Eyes-Of-Cobot Project.

> This work is under development. All data and code will soon be migrated to the [Eyes-of-Cobot gricad group](https://gricad-gitlab.univ-grenoble-alpes.fr/eyesofcobot/eyesofcobot).

This project contains a dataset of oculometric data obtained during figure assembly using [Lego Duplo](https://www.lego.com/fr-fr/themes/duplo?consent-modal=show&age-gate=grown_up).

This dataset was built to study the ocular behavior of human operators during assembly tasks, with the aim of predicting future actions of a human operator in the context of human-cobot collaboration.

## Data Acquisition

The data were acquired by involving 80 psychology students in a study conducted at the LIG. The full protocol is available on the [protocol](docs/protocol.md) page.

## Dataset

The dataset contains ocular data collected during the assembly of figures using Lego Duplo. Complete documentation of the dataset can be found on the [documentation](docs/dataset.md) page.

## Prediction

### Dependencies

    pip3 install tensorflow

### Getting Start

    python3 main.py pour l'approche modele
    python3 main_lstm.py pour l'approche ML
    python3 plot_graph.py chemin_relatif_logs pour plots les figures surfaces
    python3 plot_norme.py chemin_relatif_logs pour plots les figures normes

## Contact
For questions or more information, please contact:
- Maxence Grand
- Maxence.Grand@univ-grenoble-alpes.fr
- Université Grenoble Alpes, Laboratoire d'Informatique de Grenoble, Equipes Marvin/M-PSI
