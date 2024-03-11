from analysis.histogram import histogram, histogram_percent
from utils.user_group import Mobile, Stationary
import matplotlib.pyplot as plt
import numpy as np

MOBILE_COLOR = 'blue'
STAT_COLOR = 'red'

PUPIL_COLOR = 'blue'
FOVIO_COLOR = 'red'
TOBII_COLOR = 'orange'

def glasses(users):
    val = {
        'Mobile':{'values' : [[0,0], [0,0]], 'color':MOBILE_COLOR},
        'Stationnary':{'values' : [[0,0], [0,0]], 'color':STAT_COLOR},
    }

    for setup in ['Mobile', 'Stationnary']:
        for id in users[setup].get_id_list():
            user = users[setup].get_user(id)
            position = user.position
            glasses = user.is_wearing_glasses()
            if(glasses):
                val[setup]['values'][0 if position == 'sitting' else 1][0] += 1
            val[setup]['values'][0 if position == 'sitting' else 1][1] += 1

    for setup in ['Mobile', 'Stationnary']:
        val[setup]['values'] = [
            100 * (val[setup]['values'][i][0]/val[setup]['values'][i][1]) \
                if val[setup]['values'][i][1] > 0 else 0 for i in [0,1]
        ]

    fig, ax = plt.subplots()
    histogram(\
        fig=fig,\
        ax=ax,\
        r=np.arange(2),\
        width=.33,\
        val=val,\
        xlabel='Position',\
        ylabel='#Wear Glasses (%)',\
        title='Number of participants wearing glasses or contact lenses',\
        png='../data_analysis/glasses.png',\
        categories=["Sitting", "Standing"])

def calibration(users):
    categories = ['No Data', 'Severe', 'Slight', 'No Issue']
    val = {
        "Pupil":{'values' :{c:[0,0] for c in categories},'color':PUPIL_COLOR},
        "Fovio":{'values' :{c:[0,0] for c in categories},'color':FOVIO_COLOR},
        "Tobii":{'values' :{c:[0,0] for c in categories},'color':TOBII_COLOR},
    }

    for setup in ['Mobile', 'Stationnary']:
        for id in users[setup].get_id_list():
            user = users[setup].get_user(id)
            id_position = 0 if user.position == 'sitting' else 1
            if(setup == 'Mobile'):
                val['Pupil']['values'][categories[user.pupil]][id_position] += 1
            else:
                val['Fovio']['values'][categories[user.fovio]][id_position] += 1
                val['Tobii']['values'][categories[user.tobii]][id_position] += 1

    for e in ["Pupil", "Fovio", "Tobii"]:
        for position in [0,1]:
            values = [val[e]['values'][c][position] for c in categories]
            if(sum(values) > 0):
                for c in categories:
                    val[e]['values'][c][position] =\
                        100*val[e]['values'][c][position]/sum(values)


    for id_position, position in enumerate(['Sitting']):
        fig, ax = plt.subplots()
        val_pos = {
            e:{
                'values':[ val[e]['values'][c][id_position] for c in categories ],\
                'color': val[e]['color']
            }  for e in val.keys()
        }

        histogram(\
            fig=fig,\
            ax=ax,\
            r=np.arange(4),\
            width=.24,\
            val=val_pos,\
            xlabel='Calibration Quality',\
            ylabel='#Participants (%)',\
            title=f'{position} Participants',\
            png=f'../data_analysis/calibration_{position}.png',\
            categories=categories)

def recordings(users):
    categories = ['car', 'tb', 'house', 'sc', 'tc', 'tsb']

    val = {
        "Mobile":{'values' :{c:[0,0] for c in categories},'color':MOBILE_COLOR},
        "Stationnary":{'values' :{c:[0,0] for c in categories},'color':STAT_COLOR}
    }

    for setup in ['Mobile', 'Stationnary']:
        for id in users[setup].get_id_list():
            user = users[setup].get_user(id)
            if(not user.has_data()):
                continue
            for figure in categories:
                id_position = 0 if user.position == 'sitting' else 1
                if(not user.has_figure_data(figure)):
                    val[setup]['values'][figure][id_position] += 1



    for id_position, position in enumerate(['Sitting']):
        fig, ax = plt.subplots()
        val_pos = {
            e:{
                'values':[ val[e]['values'][c][id_position] for c in categories ],\
                'color': val[e]['color']
            }  for e in val.keys()
        }

        histogram(\
            fig=fig,\
            ax=ax,\
            r=np.arange(len(categories)),\
            width=.33,\
            val=val_pos,\
            xlabel='Figure',\
            ylabel='#Participants (%)',\
            title=f'{position} Participants',\
            png=f'../data_analysis/recordings_{position}.png',\
            categories=categories,\
            ymax=5)

def specific_mobile(mobile_users):
    val = [[0,0,0],[0,0,0]]

    for id in mobile_users.get_id_list():
        user = mobile_users.get_user(id)
        if(not user.has_data()):
            continue
        id_position = 0 if user.position == 'sitting' else 1
        if(user.eye0 == 1 and user.eye1 == 1):
            val[id_position][0] += 1
        elif(user.eye0 == 1):
            val[id_position][1] += 1
        else:
            val[id_position][2] += 1

    labels = ["Both Eyes", "Only Eye 0", "Only Eye 1"]
    for id_position, position in enumerate(["Sitting"]):
        fig, ax = plt.subplots()
        ax.pie(val[id_position], labels=labels, autopct='%1.1f%%', startangle=90)
        # ax.set_title(f'{position} Participants')
        png = f"../data_analysis/eyes_{position}.png"
        print(f"Plot {png}")
        fig.savefig(png)

    val = [[0,0,0,0],[0,0,0,0]]

    for id in mobile_users.get_id_list():
        user = mobile_users.get_user(id)
        if(not user.has_data()):
            continue
        id_position = 0 if user.position == 'sitting' else 1
        val[id_position][user.screen-1] += 1

    labels = ["1 Screen Border", "2 Screen Borders", "3 Screen Borders", "4 Screen Borders"]
    for id_position, position in enumerate(["Sitting"]):
        fig, ax = plt.subplots()
        ax.pie(val[id_position], labels=labels, autopct='%1.1f%%', startangle=90)
        # ax.set_title(f'{position} Participants')
        png = f"../data_analysis/screen_border_{position}.png"
        print(f"Plot {png}")
        fig.savefig(png)
