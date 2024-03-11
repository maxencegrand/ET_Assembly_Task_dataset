import csv
import pandas as pd
from utils.user_group import Mobile, Stationary
import numpy as np
from utils.event import EventType, InstructionEvent, Action
from utils.position import Point, Position
from extraction.flow import FlowDFA

MOBILE_COLOR = 'blue'
STAT_COLOR = 'red'

PUPIL_COLOR = 'blue'
FOVIO_COLOR = 'red'
TOBII_COLOR = 'orange'

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
