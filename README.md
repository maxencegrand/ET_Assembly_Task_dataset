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

### Dependencies and requirements

Without python env

    python version>=3.9.2
    pip install -r prediction/requirements.txt

With python env

    python -m venv prediction/environnement_prediction
    source prediction/environnement_prediction/bin/activate
    pip install -r prediction/requirements.txt


### Getting Start

    cd prediction
    python main.py # Model Based Approach
    python main_lstm.py # ML Based Approach
    python plot_graph.py path/to/the/log/files # Plot Surface Figures
    python plot_norme.py path/to/the/log/files # Plot Norme Figures

## Contact
For questions or more information, please contact:
- Maxence Grand
- Maxence.Grand@univ-grenoble-alpes.fr
- Université Grenoble Alpes, Laboratoire d'Informatique de Grenoble, Equipes Marvin/M-PSI
