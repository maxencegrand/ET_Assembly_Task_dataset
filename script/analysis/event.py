import pandas as pd
from utils.user_group import Mobile, Stationary
from utils.event import EventType, InstructionEvent, Action
import matplotlib.pyplot as plt
import numpy as np
from analysis.histogram import histogram, histogram_percent, histogram_percent_interval

MOBILE_COLOR = 'blue'
STAT_COLOR = 'red'

PUPIL_COLOR = 'blue'
FOVIO_COLOR = 'red'
TOBII_COLOR = 'orange'

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
