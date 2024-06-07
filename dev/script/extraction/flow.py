import pandas as pd
import cv2
from utils.device import Device
from utils.event import InstructionEvent, Action
import numpy as np
from utils.position import Point,Position
import sys,os,csv
import math

ID_VECTOR_TABLE = 0
ID_VECTOR_SCREEN = 1
THRESH_NO_DATA = 60
class DeviceFlow:
    """
    """
    def __init__(self, user, figure):
        self.dataset_path = f'{user.get_dataset_folder()}/{figure}'
        # csvtable = f"{self.dataset_path}/table.csv"
        # csvscreen = f"{self.dataset_path}/screen.csv"
        # csvevents = f"{self.dataset_path}/events.csv"
        # csvinstructions = f"{self.dataset_path}/instruction_events.csv"
        #
        # df_table = pd.DataFrame(pd.read_csv(csvtable))
        # df_screen = pd.DataFrame(pd.read_csv(csvscreen))
        # df_events = pd.DataFrame(pd.read_csv(csvevents))
        # df_instruction = pd.DataFrame(pd.read_csv(csvinstructions))

        self.read_events()
        for ts in self.events.keys():
            gz = self.read_gazepoints(ts)
            flow = self.generate_flow(gz)
            folder = f"{self.dataset_path}/device_events_flow"
            if not os.path.exists(folder):
                os.makedirs(folder)
            csvfile = f"{folder}/before_grasp_{ts}.csv"
            with open(csvfile , 'w',  newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'event', 'device'])
                for event in flow:
                    writer.writerow(event)


    def read_events(self):
        """
        """
        csvinstructions = f"{self.dataset_path}/instruction_events.csv"
        df = pd.DataFrame(pd.read_csv(csvinstructions))
        prev_ts = 0
        for i in df.index:
            ts = int(df.loc[i, "timestamp"])
            if(InstructionEvent(int(df.loc[i,'code'])) == InstructionEvent.START):
                prev_ts = ts
        self.events = {}
        csvevents = f"{self.dataset_path}/events.csv"
        df = pd.DataFrame(pd.read_csv(csvevents))
        prev_grasp = 0
        for i in df.index:
            ts = int(df.loc[i, "timestamp"])
            act = Action(int(df.loc[i, "action"]))
            if(act == Action.GRASP):
                prev_grasp = ts
            elif(act == Action.RELEASE):
                block_id = int(df.loc[i, "block"])
                position = Position(\
                    Point(df.loc[i, "x0"],df.loc[i, "y0"]),\
                    Point(df.loc[i, "x1"],df.loc[i, "y1"]),\
                    Point(df.loc[i, "x3"],df.loc[i, "y3"]),\
                    Point(df.loc[i, "x2"],df.loc[i, "y2"]),\
                )
                self.events[ts] = {"prev_ts":prev_ts, "position":position, "prev_grasp":prev_grasp}
                prev_ts=ts

    def read_gazepoints(self, ts_release):
        """
        """
        gazepoints = {}

        csvtable = f"{self.dataset_path}/table.csv"
        csvscreen = f"{self.dataset_path}/screen.csv"
        df_table = pd.DataFrame(pd.read_csv(csvtable))
        df_screen = pd.DataFrame(pd.read_csv(csvscreen))
        first = self.events[ts_release]['prev_ts']
        idx_screen = 0
        idx_table = 0
        prev_ts = 0
        while (idx_table < df_table.index.stop-1 or \
            idx_screen < df_screen.index.stop-1):
            id_vector = 0
            if(idx_table < df_table.index.stop-1 and \
                idx_screen < df_screen.index.stop-1):
                ts_table = df_table.loc[idx_table, 'timestamp']
                ts_screen = df_screen.loc[idx_screen, 'timestamp']
                ts = ts_screen if ts_screen < ts_table else ts_table
                df = df_screen if ts_screen < ts_table else df_table
                # if(ts_table <= ts_screen):
                #     print(f"{ts_table} {ts}")
                idx = idx_table if ts_table <= ts_screen else idx_screen
                idx_table += 1 if ts_table <= ts_screen else 0
                idx_screen += 1 if ts_screen < ts_table else 0
                id_vector = ID_VECTOR_TABLE if ts_table <= ts_screen else ID_VECTOR_SCREEN
            elif(idx_table < df_table.index.stop-1):
                ts = df_screen.loc[idx_table, 'timestamp']
                df = df_table
                idx = idx_table
                idx_table += 1
                id_vector = ID_VECTOR_TABLE
            else:
                ts = df_screen.loc[idx_screen, 'timestamp']
                df = df_screen
                idx = idx_screen
                idx_screen += 1
                id_vector = ID_VECTOR_SCREEN
            # print(ts)
            if(ts < first):
                prev_ts=ts
                continue
            if(ts > ts_release):
                gazepoints[ts_release-first] = [False, False, False, True]
                # if(gazepoints[prev_ts])
                break
            if(ts >= self.events[ts_release]['prev_grasp'] and \
                prev_ts <= self.events[ts_release]['prev_grasp']):
                gazepoints[self.events[ts_release]['prev_grasp']-first] = [False, False, True, False]

            point = Point(df.loc[idx, 'x'],df.loc[idx, 'y'])
            if(math.isnan(point.x) or math.isnan(point.y)):
                if(not (ts-first) in gazepoints.keys()):
                    gazepoints[ts-first] = [False for i in range(4)]
            else:
                gazepoints[ts-first] = [True if i == id_vector else False for i in range(4)]
            prev_ts=ts
        return gazepoints

    def generate_flow(self,gazepoints):
        flow = []
        last_event = [0,"",""]
        prev_inside = 0
        for ts in gazepoints.keys():
            if(gazepoints[ts][2]):
                flow.append([ts, "grasp", "BLOCK"])
                # prev_ts=ts
                continue
            if(gazepoints[ts][3]):
                flow.append([ts, "release", "BLOCK"])
                if(last_event[1] == "enter" and last_event[2] == "SCREEN"):
                    flow.append([ts+60, "quit", "SCREEN"])
                if(last_event[1] == "enter" and last_event[2] == "TABLE"):
                    flow.append([ts+60, "quit", "TABLE"])
                break
            if(gazepoints[ts][ID_VECTOR_TABLE]):
                prev_inside = ts
                if (last_event[1] == "enter" and last_event[2] == "SCREEN"):
                    flow.append([ts-1, "quit", "SCREEN"])
                    last_event = [ts, "quit", "SCREEN"]
                if (not (last_event[1] == "enter" and last_event[2] == "TABLE")):
                    flow.append([ts, "enter", "TABLE"])
                    last_event = [ts, "enter", "TABLE"]
            else:
                if (last_event[1] == "enter" and last_event[2] == "TABLE" and ts-prev_inside > THRESH_NO_DATA):
                    flow.append([ts, "quit", "TABLE"])
                    last_event = [ts, "quit", "TABLE"]
            if(gazepoints[ts][ID_VECTOR_SCREEN]):
                prev_inside = ts
                if (last_event[1] == "enter" and last_event[2] == "TABLE"):
                    flow.append([ts-1, "quit", "TABLE"])
                    last_event = [ts-1, "quit", "TABLE"]
                if (not (last_event[1] == "enter" and last_event[2] == "SCREEN")):
                    flow.append([ts, "enter", "SCREEN"])
                    last_event = [ts, "enter", "SCREEN"]
            else:
                if (last_event[1] == "enter" and last_event[2] == "SCREEN" and ts-prev_inside > THRESH_NO_DATA):
                    flow.append([ts, "quit", "SCREEN"])
                    last_event = [ts, "quit", "SCREEN"]

        return flow

class FlowDFA:
    """
    """
    def __init__(self, id_setup=0):
        self.data = {
            'states':{
                'NO_DEVICE':{0:[[],[]],1:[[],[]],2:[[],[]]},
                'TABLE':{0:[[],[]],1:[[],[]],2:[[],[]]},
                'SCREEN':{0:[[],[]],1:[[],[]],2:[[],[]]}
            },
            'transitions':{
                'NO_DEVICE':{
                    0:{
                        'NO_DEVICE':{'id':1,'event':'grasp','prob':[0,0]},
                        'TABLE':{'id':0,'event':'enter','prob':[0,0]},
                        'SCREEN':{'id':0,'event':'enter','prob':[0,0]}
                    },
                    1:{
                        'NO_DEVICE':{'id':2,'event':'release','prob':[0,0]},
                        'TABLE':{'id':1,'event':'enter','prob':[0,0]},
                        'SCREEN':{'id':1,'event':'enter','prob':[0,0]}
                    }
                },
                'TABLE':{
                    0:{
                        'NO_DEVICE':{'id':0,'event':'quit','prob':[0,0]},
                        'TABLE':{'id':1,'event':'grasp','prob':[0,0]}
                    },
                    1:{
                        'NO_DEVICE':{'id':1,'event':'quit','prob':[0,0]},
                        'TABLE':{'id':2,'event':'release','prob':[0,0]}
                    },
                    2:{
                        'NO_DEVICE':{'id':2,'event':'quit','prob':[0,0]}
                    }
                },
                'SCREEN':{
                    0:{
                        'NO_DEVICE':{'id':0,'event':'quit','prob':[0,0]},
                        'SCREEN':{'id':1,'event':'grasp','prob':[0,0]}
                    },
                    1:{
                        'NO_DEVICE':{'id':1,'event':'quit','prob':[0,0]},
                        'SCREEN':{'id':2,'event':'release','prob':[0,0]}
                    },
                    2:{
                        'NO_DEVICE':{'id':2,'event':'quit','prob':[0,0]}
                    }
                }
            }
        }
        self.current = {'device':'NO_DEVICE','id':0}
        self.id_setup = id_setup

    def reset_current(self):
        """
        """
        self.current = {'device':'NO_DEVICE','id':0}

    def apply(self, event, device, time):
        """
        """
        # print(time)
        cur_dev = self.current['device']
        cur_id = self.current['id']
        self.data['states'][cur_dev][cur_id][self.id_setup].append(time)
        if(event == 'quit' or event == 'enter'):
            next_dev = device
            next_id = self.data['transitions'][cur_dev][cur_id][device]['id']
            self.data['transitions'][cur_dev][cur_id][device]['prob'][self.id_setup]+=1
            self.current['device'] = next_dev
            self.current['id'] = next_id
        else:
            self.data['transitions'][cur_dev][cur_id][cur_dev]['prob'][self.id_setup]+=1
            self.current['id'] += 1

    def write_csv(self, csv_states, csv_transitions):
        #Write states
        with open(csv_states , 'w',  newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['device', 'id', 'mobile', 'stationary'])
            for device in self.data['states'].keys():
                for id in self.data['states'][device].keys():
                    r = [device,id]
                    r.extend(self.data['states'][device][id])
                    writer.writerow(r)

        #write transitions
        with open(csv_transitions , 'w',  newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['device_out', 'id_out','device_in', 'id_in', 'event', 'mobile', 'stationary'])
            for device_out in self.data['transitions'].keys():
                for id_out in self.data['transitions'][device_out].keys():
                    for device_in in self.data['transitions'][device_out][id_out].keys():
                        id_in = self.data['transitions'][device_out][id_out][device_in]['id']
                        event = self.data['transitions'][device_out][id_out][device_in]['event']
                        r = [device_out, id_out, device_in, id_in, event]
                        r.extend(self.data['transitions'][device_out][id_out][device_in]['prob'])
                        writer.writerow(r)

    def mean_state_time(self):
        """
        """
        #states
        for device in self.data['states'].keys():
            for id in self.data['states'][device].keys():
                for i in range(2):
                    times = self.data['states'][device][id][i]
                    if(len(times) <= 0):
                        self.data['states'][device][id][i] = 0
                    else:
                        self.data['states'][device][id][i] = sum(times)/len(times)

    def percent_transitions(self):
        """
        """
        for device_out in self.data['transitions'].keys():
            for id_out in self.data['transitions'][device_out].keys():
                for i in range(2):
                    s = 0
                    #Sum prob
                    for device_in in self.data['transitions'][device_out][id_out].keys():
                        p = self.data['transitions'][device_out][id_out][device_in]['prob'][i]
                        s += p
                    #Compute prob as percent
                    for device_in in self.data['transitions'][device_out][id_out].keys():
                        p = self.data['transitions'][device_out][id_out][device_in]['prob'][i]
                        self.data['transitions'][device_out][id_out][device_in]['prob'][i] = \
                                                                    100*(p/s) if s > 0 else 0

    def convert_as_participant_mean(self, n):
        """
        """
        #states
        for device in self.data['states'].keys():
            for id in self.data['states'][device].keys():
                for i in range(2):
                    tmp = self.data['states'][device][id][i]
                    self.data['states'][device][id][i] = tmp/n

        #transitions
        for device_out in self.data['transitions'].keys():
            for id_out in self.data['transitions'][device_out].keys():
                for device_in in self.data['transitions'][device_out][id_out].keys():
                    for i in range(2):
                        p = self.data['transitions'][device_out][id_out][device_in]['prob'][i]
                        self.data['transitions'][device_out][id_out][device_in]['prob'][i] = p/n

    def add_dfa(self, other_dfa):
        """
        """
        #states
        for device in self.data['states'].keys():
            for id in self.data['states'][device].keys():
                for i in range(2):
                    tmp = other_dfa.data['states'][device][id][i]
                    self.data['states'][device][id][i] += tmp
        #transitions
        for device_out in self.data['transitions'].keys():
            for id_out in self.data['transitions'][device_out].keys():
                for device_in in self.data['transitions'][device_out][id_out].keys():
                    for i in range(2):
                        tmp = other_dfa.data['transitions'][device_out][id_out][device_in]['prob'][i]
                        self.data['transitions'][device_out][id_out][device_in]['prob'][i] += tmp
