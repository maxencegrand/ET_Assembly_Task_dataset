import csv,sys
import pandas as pd
from utils.user_group import Mobile, Stationary
import matplotlib.pyplot as plt
import numpy as np
from utils.event import EventType, InstructionEvent, Action
from utils.position import Point, Position
from extraction.flow import FlowDFA

MOBILE_COLOR = 'blue'
STAT_COLOR = 'red'

PUPIL_COLOR = 'blue'
FOVIO_COLOR = 'red'
TOBII_COLOR = 'orange'

def histogram(fig, ax, r, width, val, xlabel, ylabel,title, png, categories=None, ymax=100):
    print(f"Plot {png}")
    labels = list(val.keys())
    for idx_label, label in enumerate(labels):
        # print(r + (idx_label * width))
        # print(val[label]['values'])
        ax.bar(
            r + (idx_label * width),\
            val[label]['values'],
            width=width,
            color=val[label]['color'],
            label=label)
    if(categories != None):
        ax.set_xticks(r + width/len(categories),categories)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0,ymax)
    # ax.set_title(title)
    ax.legend()
    fig.savefig(png)
    plt.close()

def histogram_percent(fig, ax, r, width, val, xlabel, ylabel,title, png, categories, ymax=100, xmin=0, xmax=10):
    print(f"Plot {png}")
    labels = list(val.keys())
    for idx_label, label in enumerate(labels):
        unique_values, counts = np.unique(val[label]['values'], return_counts=True)
        percentages = (counts / len(val[label]['values'])) * 100
        I=unique_values
        print(unique_values)
        x_ = [r[i]+(idx_label * width) for i in I]
        ax.bar(
            x_,\
            percentages,
            width=width,
            color=val[label]['color'],
            label=label)
    ax.set_xticks(r + width/len(categories),categories)
    ax.set_xticklabels(categories)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(0,ymax)
    # ax.set_title(title)
    ax.legend()
    fig.savefig(png)
    plt.close()

def histogram_percent_interval(fig, ax, r, width, val, xlabel, ylabel,title, png, categories=None, ymax=100, xmin=0, xmax=10, interval_width=10):
    print(f"Plot {png}")
    labels = list(val.keys())
    for idx_label, label in enumerate(labels):
        unique_values, counts = np.unique(val[label]['values'], return_counts=True)
        percentages = (counts / len(val[label]['values'])) * 100
        I=unique_values
        x_ = [r[int(i/interval_width)]+(idx_label * width) for i in I]
        ax.bar(
            x_,\
            percentages,
            width=width,
            color=val[label]['color'],
            label=label)
    # if(categories != None):
    #     ax.set_xticks(r + width/len(categories),categories)
    #     ax.set_xticklabels(categories)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(0,ymax)
    # ax.set_title(title)
    ax.legend()
    fig.savefig(png)
    plt.close()

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

def action_events(users):
    figures = ["car", "tb", "house", "sc", "tc", "tsb"]
    val =[
        {'Mobile':[[],[],[]],'Stationnary':[[],[],[]]},
        {'Mobile':[[],[],[]],'Stationnary':[[],[],[]]}
    ]

    for setup in ['Mobile', 'Stationnary']:
        for id in users[setup].get_id_list():
            user = users[setup].get_user(id)
            if(not user.has_data()):
                continue
            id_position = 0 if user.position == 'sitting' else 1
            e,c,b = [0,0,0]
            for figure in figures:
                if(not user.has_figure_data(figure)):
                    continue
                csvfile = f'{user.get_dataset_folder()}/{figure}/events.csv'
                df = pd.DataFrame(pd.read_csv(csvfile))
                for i in df.index:
                    event_type = EventType(int(df.loc[i,'type']))
                    if(event_type == EventType.ERROR):
                        e+=1
                    elif(event_type == EventType.CORRECTION):
                        c+=1
                    elif(event_type == EventType.BAD_ID):
                        b+=1
            for id_type, type in enumerate([e,c,b]):
                val[id_position][setup][id_type].append(type)

    # print(val)
    for id_position, position in enumerate(['Sitting']):
        for id_type, type in enumerate(["Errors","Corrections","BadID"]):
            n_max = 8
            categories = list(range(n_max+1))
            r = np.arange(len(categories))
            bar_width = .33

            fig, ax = plt.subplots()
            val_pos = {
                'Mobile':{'values':val[id_position]['Mobile'][id_type], 'color':MOBILE_COLOR},
                'Stationnary':{'values':val[id_position]['Stationnary'][id_type], 'color':STAT_COLOR}
            }

            histogram_percent(\
                fig=fig,\
                ax=ax,\
                r=np.arange(len(categories)),\
                width=.33,\
                val=val_pos,\
                xlabel=f'#{type}',\
                ylabel='#Participants (%)',\
                title=f'{position} Participants',\
                png=f'../data_analysis/{type}_{position}.png',\
                categories=categories,\
                ymax=100,\
                xmin=-0.5, xmax=n_max+1)

def instructions_events(users):
    figures = ["car", "tb", "house", "sc", "tc", "tsb"]
    val =[
        {'Mobile':[[],[]],'Stationnary':[[],[]]},
        {'Mobile':[[],[]],'Stationnary':[[],[]]}
    ]

    for setup in ['Mobile', 'Stationnary']:
        for id in users[setup].get_id_list():
            user = users[setup].get_user(id)
            if(not user.has_data()):
                continue
            id_position = 0 if user.position == 'sitting' else 1
            n,e = [0,0]
            for figure in figures:
                if(not user.has_figure_data(figure)):
                    continue
                csvfile = f'{user.get_dataset_folder()}/{figure}/instruction_events.csv'
                df = pd.DataFrame(pd.read_csv(csvfile))
                for i in df.index:
                    code = InstructionEvent(int(df.loc[i,'code']))
                    if(code == InstructionEvent.EXTRA_NEXT_ERROR):
                        e+=1
                    elif(code == InstructionEvent.NO_NEXT_ERROR):
                        n+=1
            for id_code, code in enumerate([n,e]):
                val[id_position][setup][id_code].append(code)

    # print(val)
    for id_position, position in enumerate(['Sitting']):
        for id_code, code in enumerate(["NoNextErrors","ExtraNextErrors"]):
            n_max = 12
            categories = list(range(n_max+1))
            r = np.arange(len(categories))
            bar_width = .33

            fig, ax = plt.subplots()
            val_pos = {
                'Mobile':{'values':val[id_position]['Mobile'][id_code], 'color':MOBILE_COLOR},
                'Stationnary':{'values':val[id_position]['Stationnary'][id_code], 'color':STAT_COLOR}
            }

            histogram_percent(\
                fig=fig,\
                ax=ax,\
                r=np.arange(len(categories)),\
                width=.33,\
                val=val_pos,\
                xlabel=f'#{code}',\
                ylabel='#Participants (%)',\
                title=f'{position} Participants',\
                png=f'../data_analysis/{code}_{position}.png',\
                categories=categories,\
                ymax=100,\
                xmin=-0.5, xmax=n_max+1)

def assembly_durations(users):
    figures = ["car", "tb", "house", "sc", "tc", "tsb"]
    val =[
        {'Mobile':{f:[] for f in figures},'Stationnary':{f:[] for f in figures}},
        {'Mobile':{f:[] for f in figures},'Stationnary':{f:[] for f in figures}}
    ]

    interval_width = 10
    for setup in ['Mobile', 'Stationnary']:
        for id in users[setup].get_id_list():
            user = users[setup].get_user(id)
            if(not user.has_data()):
                continue
            id_position = 0 if user.position == 'sitting' else 1
            start,end = [0,0]
            for figure in figures:
                if(not user.has_figure_data(figure)):
                    continue
                csvfile = f'{user.get_dataset_folder()}/{figure}/instruction_events.csv'
                df = pd.DataFrame(pd.read_csv(csvfile))
                for i in df.index:
                    code = InstructionEvent(int(df.loc[i,'code']))
                    if(code == InstructionEvent.START):
                        start = df.loc[i,'timestamp']
                    elif(code == InstructionEvent.END):
                        end = df.loc[i,'timestamp']
                time = round(((end-start)/1000) / interval_width) * interval_width
                val[id_position][setup][figure].append(time)

    for id_position, position in enumerate(['Sitting']):
        for id_fig, figure in enumerate(figures):
            n_max = 200
            categories = [(x * 10) for x in range(int(n_max/interval_width))]
            # r = np.arange(len(categories))
            r = [(x * 10) for x in range(int(n_max/interval_width))]
            # print(categories)
            bar_width = .33

            fig, ax = plt.subplots()
            val_pos = {
                'Mobile':{'values':val[id_position]['Mobile'][figure], 'color':MOBILE_COLOR},
                'Stationnary':{'values':val[id_position]['Stationnary'][figure], 'color':STAT_COLOR}
            }

            histogram_percent_interval(\
                fig=fig,\
                ax=ax,\
                r=r,\
                width=interval_width/3,\
                val=val_pos,\
                xlabel=f'Time (s)',\
                ylabel='#Participants (%)',\
                title=f'{position} Participants',\
                png=f'../data_analysis/duration_{figure}_{position}.png',\
                categories=categories,\
                ymax=100,\
                xmin=-0.5, xmax=n_max+1,\
                interval_width=interval_width)

def action_events_durations(users):
    figures = ["car", "tb", "house", "sc", "tc", "tsb"]
    val =[
        {'Mobile':{f:[[],[]] for f in figures},'Stationnary':{f:[[],[]] for f in figures}},
        {'Mobile':{f:[[],[]] for f in figures},'Stationnary':{f:[[],[]] for f in figures}}
    ]

    interval_width = 1
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
                    if(act == Action.GRASP):
                        csv_gz = f"{user.get_dataset_folder()}/{figure}/distances_before_grasp/distance_all_blocks_before_grasp_{ts}.csv"
                        df_gz = pd.DataFrame(pd.read_csv(csv_gz))
                    else:
                        csv_gz = f"{user.get_dataset_folder()}/{figure}/block_distances_before_release/distance_before_release_{ts}.csv"
                        df_gz = pd.DataFrame(pd.read_csv(csv_gz))
                    try:
                        time = int(df_gz.loc[df_gz.index.stop-1, 'timestamp'])
                        time = round((time/1000) / interval_width) * interval_width
                        val[id_position][setup][figure][act.value].append(time)
                    except:
                        print(csv_gz)
    # print(val)
    for id_position, position in enumerate(['Sitting']):
        for id_fig, figure in enumerate(figures):
            for act in [Action.GRASP, Action.RELEASE]:
                n_max = 20
                categories = np.arange(n_max)
                r = np.arange(n_max)

                fig, ax = plt.subplots()
                val_pos = {
                    'Mobile':{'values':val[id_position]['Mobile'][figure][act.value], 'color':MOBILE_COLOR},
                    'Stationnary':{'values':val[id_position]['Stationnary'][figure][act.value], 'color':STAT_COLOR}
                }

                histogram_percent(\
                    fig=fig,\
                    ax=ax,\
                    r=r,\
                    width=interval_width/3,\
                    val=val_pos,\
                    xlabel=f'Time (s)',\
                    ylabel='#Participants (%)',\
                    title=f'{position} Participants',\
                    png=f'../data_analysis/duration_{act}_{figure}_{position}.png',\
                    categories=categories,\
                    ymax=100,\
                    xmin=-0.5, xmax=n_max+1)

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
            d = -32
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
        fig, axs = plt.subplots(1, 2, figsize=(12, 8))
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

def behavior(users, position='sitting'):
    figures = ["car", "tb", "house", "sc", "tc", "tsb"]
    # figures = ["car"]
    dfa = FlowDFA()
    dfa.mean_state_time()
    csv_states = f"../data_analysis/behavior_data_states_{position}.csv"
    csv_transitions = f"../data_analysis/behavior_data_transitions_{position}.csv"
    count=[0,0]
    for id_setup, setup in enumerate(['Mobile', 'Stationnary']):
        for id in users[setup].get_id_list():
            user = users[setup].get_user(id)
            if(user.has_data()):
                if(user.position == position):
                    for figure in figures:
                        if(user.has_figure_data(figure)):
                            count[id_setup]+=1

    for id_setup, setup in enumerate(['Mobile', 'Stationnary']):
        for id in users[setup].get_id_list():
            user = users[setup].get_user(id)
            if(not user.has_data()):
                continue
            if(not user.position == position):
                continue
            for figure in figures:
                if(not user.has_figure_data(figure)):
                    continue

                df_events = pd.DataFrame(pd.read_csv(\
                    f"{user.get_dataset_folder()}/{figure}/events.csv"))
                n=0
                dfa_user = FlowDFA(id_setup)
                dfa_user.mean_state_time()
                for i in df_events.index:
                    ts = int(df_events.loc[i,'timestamp'])
                    act = Action(df_events.loc[i,'action'])
                    if(act == Action.GRASP):
                        continue
                    df = pd.DataFrame(pd.read_csv(\
                        f"{user.get_dataset_folder()}/{figure}/device_events_flow/before_grasp_{ts}.csv"))
                    prev = 0
                    time = 0
                    dfa_user_release = FlowDFA(id_setup)
                    n += 1
                    for j in df.index:
                        ts_event = df.loc[j,'timestamp']
                        event = df.loc[j,'event']
                        device = 'NO_DEVICE' if event == 'quit' else df.loc[j,'device']
                        time = ts_event - prev
                        prev = ts_event
                        dfa_user_release.apply(event, device, time)
                    dfa_user_release.mean_state_time()
                    dfa_user.add_dfa(dfa_user_release)
                # dfa_user.mean_state_time()
                dfa_user.convert_as_participant_mean(count[id_setup])
                dfa_user.convert_as_participant_mean(n)
                # dfa_user.write_csv(csv_states, csv_transitions)
                dfa.add_dfa(dfa_user)
    dfa.percent_transitions()
    dfa.write_csv(csv_states, csv_transitions)


def main():
    users = {'Mobile':Mobile(),'Stationnary':Stationary()}
    # glasses(users)
    # calibration(users)
    # recordings(users)
    # specific_mobile(users['Mobile'])
    # action_events(users)
    # instructions_events(users)
    # assembly_durations(users)
    # action_events_durations(users)
    # distance_analysis(users)
    behavior(users)


if __name__ == "__main__":
    main()
