import pandas as pd
from utils.user_group import Mobile, Stationary
import matplotlib.pyplot as plt
import numpy as np
from utils.event import EventType, InstructionEvent, Action

def distance_analysis(users):
    figures = ["car", "tb", "house", "sc", "tc", "tsb"]
    n_max=100
    val =[
        {'Mobile':[{},{}],'Stationnary':[{},{}]},
        {'Mobile':[{},{}],'Stationnary':[{},{}]}
    ]

    interval_width = 4
    for id_position, position in enumerate(['Sitting', 'Standing']):
        for setup in ['Mobile', 'Stationnary']:
            d = -16
            while d < n_max:
                val[id_position][setup][Action.GRASP.value][d] = []
                val[id_position][setup][Action.RELEASE.value][d] = []
                d += interval_width

    for setup in ['Mobile', 'Stationnary']:
        for id in users[setup].get_id_list():
            user = users[setup].get_user(id)
            # user.print_info()
            if(not user.has_data()):
                continue
            id_position = 0 if user.position == 'sitting' else 1
            start,end = [0,0]
            for figure in figures:
                if(not user.has_figure_data(figure)):
                    continue
                # print(figure)
                csvfile = f'{user.get_dataset_folder()}/{figure}/events.csv'
                df = pd.DataFrame(pd.read_csv(csvfile))
                for i in df.index:
                    ts = int(df.loc[i, 'timestamp'])
                    act = Action(int(df.loc[i, 'action']))
                    distance = {}
                    n = 0
                    if(act == Action.GRASP):
                        csv_gz = f"{user.get_dataset_folder()}/{figure}/distances_before_grasp/distance_all_blocks_before_grasp_{ts}.csv"
                        df_gz = pd.DataFrame(pd.read_csv(csv_gz))
                    else:
                        csv_gz = f"{user.get_dataset_folder()}/{figure}/block_distances_before_release/distance_before_release_{ts}.csv"
                        df_gz = pd.DataFrame(pd.read_csv(csv_gz))

                    for j in df_gz.index:
                        n+=1
                        if(act == Action.GRASP):
                            block_id = df.loc[i,"block"]
                            dist = df_gz.loc[j, f"block_{block_id}"]
                        else:
                            dist = df_gz.loc[j, "distance"]
                        if(not np.isnan(dist)):
                            dist = round(dist / interval_width) * interval_width
                            distance[dist] = distance.get(dist,0)+1
                    for d in val[id_position][setup][act.value].keys():
                        if d in distance.keys():
                            val[id_position][setup][act.value][d].append(100 * distance[d]/n)

    bar_width = (interval_width/3)
    for idx_position, position in enumerate(["Sitting"]):
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        for id_act, act in enumerate([Action.GRASP, Action.RELEASE]):
            #Mob data
            freq = {}
            for d,f in val[id_position]['Mobile'][act.value].items():
                if(len(f) <= 0):
                    freq[d] = 0
                else:
                    freq[d] = sum(f)/len(f)
            r = 0
            axs[id_act].bar([t - r for t in freq.keys()], freq.values(),width=bar_width, label='Mobile', color='blue')
            #Stat data
            freq = {}
            for d,f in val[id_position]['Stationnary'][act.value].items():
                if(len(f) <= 0):
                    freq[d] = 0
                else:
                    freq[d] = sum(f)/len(f)
            r = bar_width/2
            axs[id_act].bar([t - r for t in freq.keys()], freq.values(),width=bar_width, label='Stationnary', color='red')
            axs[id_act].legend()
            axs[id_act].set_xlabel("Distance (mm)")
            axs[id_act].set_ylabel('Time (%)')
            axs[id_act].set_ylim(0,30)
            axs[id_act].set_title(f"{act}")
            fig.savefig(f'../data_analysis/distance_{position}.png')
            plt.close()
