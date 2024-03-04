import pandas as pd
from utils.event import Action, InstructionEvent
from utils.position import Position, Point
from utils.state import State
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

def get_code_timestamp(df, value):
    df = df[df["code"] == value]
    idx = df.index[0]
    return df.loc[idx,"timestamp"]

class GraspDistance:
    """
    Generate distance csvfiles before grasp
    """
    def __init__(self, user, figure):
        """
        """
        self.user = user
        self.figure = figure
        self.path_data = "../dataset/%s/%s/%d/%s" % \
                (self.user.setup, self.user.position, self.user.id, figure)
        df_instruction_event = pd.DataFrame(data=pd.read_csv(\
                        "%s/instruction_events.csv" % self.path_data))
        self.start = int(get_code_timestamp(df_instruction_event,\
                InstructionEvent.START.value))
        self.read_events(start_ts=self.start)
        self.read_states()
        self.compute_distance()
        self.write_csv(folder = "%s/distances_before_grasp" % self.path_data)

    def read_events(self, start_ts=0):
        """
        """
        self.events = {}
        df = pd.DataFrame(pd.read_csv("%s/events.csv"%self.path_data))
        prev_ts = start_ts
        for i in df.index:
            ts = int(df.loc[i, "timestamp"])
            act = Action(int(df.loc[i, "action"]))
            if(act == Action.RELEASE):
                prev_ts=ts
            else:
                block_id = int(df.loc[i, "block"])
                self.events[ts] = {"prev_ts":prev_ts, "block_id":block_id}
        df = pd.DataFrame(pd.read_csv("%s/instruction_events.csv"%self.path_data))
        for ts_event in self.events.keys():
            for i in df.index:
                ts = int(df.loc[i, "timestamp"])
                if(ts < ts_event and ts >= self.events[ts_event]['prev_ts']):
                    self.events[ts_event]['prev_ts'] = ts

    def read_states(self):
        """
        """
        self.states = {}
        df = pd.DataFrame(pd.read_csv("%s/states.csv"%self.path_data))
        for i in df.index:
            ts = int(df.loc[i, "timestamp"])
            self.states[ts] = {}
            if(i == df.index.stop-1):
                self.states[ts]["next_ts"] = ts
            else:
                self.states[ts]["next_ts"] = int(df.loc[i+1, "timestamp"])
            for block_id in range(24):
                top_left = Point(\
                    float(df.loc[i, "%d_x0" % block_id]),\
                    float(df.loc[i, "%d_y0" % block_id]))
                top_right = Point(\
                    float(df.loc[i, "%d_x1" % block_id]),\
                    float(df.loc[i, "%d_y1" % block_id]))
                bottom_right = Point(\
                    float(df.loc[i, "%d_x2" % block_id]),\
                    float(df.loc[i, "%d_y2" % block_id]))
                bottom_left = Point(\
                    float(df.loc[i, "%d_x3" % block_id]),\
                    float(df.loc[i, "%d_y3" % block_id]))
                position = Position(top_left,top_right,bottom_left,bottom_right)
                self.states[ts][block_id] = position

    def get_current_state(self, ts):
        """
        """
        for ts_state in self.states.keys():
            if(ts_state <= ts and ts <= self.states[ts_state]["next_ts"]):
                return ts_state
        return None

    def compute_distance(self):
        """
        """
        df = pd.DataFrame(pd.read_csv("%s/table.csv"%self.path_data))
        self.distances = {}
        for ts_event in self.events:
            self.distances[ts_event] = {}
            prev_ts = self.events[ts_event]["prev_ts"]
            for block_id in range(24):
                self.distances[ts_event][block_id] = {}
            masque = (df['timestamp'] >= prev_ts) & (df['timestamp'] <= ts_event)
            for i in df[masque].index:
                ts_gz = int(df[masque].loc[i, "timestamp"])
                ts_state = self.get_current_state(ts_gz)
                for block_id in range(24):
                    block_position = self.states[ts_state][block_id]
                    gz = Point(float(df[masque].loc[i, "x"]),\
                        float(df[masque].loc[i, "y"]))
                    if(np.isnan(gz.x) or np.isnan(gz.y)):
                        self.distances[ts_event][block_id][ts_gz-prev_ts] =\
                            np.nan
                    else:
                        self.distances[ts_event][block_id][ts_gz-prev_ts] = \
                            block_position.distance(gz)

    def write_csv(self, folder):
        """
        """
        if not os.path.exists(folder):
            os.makedirs(folder)

        for ts_event in self.events:
            csvfile = "%s/distance_all_blocks_before_grasp_%d.csv" %\
                        (folder, ts_event)
            with open(csvfile , 'w',  newline='') as f:
                writer = csv.writer(f)
                row = ["timestamp"]
                for block_id in range(24):
                    row.append("block_%s" % block_id)
                writer.writerow(row)
                for ts in self.distances[ts_event][0]:
                    row = [ts]
                    for block_id in range(24):
                        row.append(self.distances[ts_event][block_id][ts])
                    writer.writerow(row)

class ReleaseDistance(GraspDistance):
    """
    Generate distance csvfiles before release
    """
    def __init__(self, user, figure):
        """
        """
        self.user = user
        self.figure = figure
        self.path_data = "../dataset/%s/%s/%d/%s" % \
                (self.user.setup, self.user.position, self.user.id, figure)
        df_instruction_event = pd.DataFrame(data=pd.read_csv(\
                        "%s/instruction_events.csv" % self.path_data))
        self.start = int(get_code_timestamp(df_instruction_event,\
                InstructionEvent.START.value))
        self.read_events(start_ts=self.start)
        self.compute_distance()
        self.write_csv(folder = "%s/block_distances_before_release" % self.path_data)

    def read_events(self, start_ts=0):
        """
        """
        self.events = {}
        df = pd.DataFrame(pd.read_csv("%s/events.csv"%self.path_data))
        prev_ts = start_ts
        for i in df.index:
            ts = int(df.loc[i, "timestamp"])
            act = Action(int(df.loc[i, "action"]))
            if(act == Action.RELEASE):
                block_id = int(df.loc[i, "block"])
                position = Position(\
                    Point(df.loc[i, "x0"],df.loc[i, "y0"]),\
                    Point(df.loc[i, "x1"],df.loc[i, "y1"]),\
                    Point(df.loc[i, "x3"],df.loc[i, "y3"]),\
                    Point(df.loc[i, "x2"],df.loc[i, "y2"]),\
                )
                self.events[ts] = {"prev_ts":prev_ts, "position":position}
                prev_ts=ts
        df = pd.DataFrame(pd.read_csv("%s/instruction_events.csv"%self.path_data))
        for ts_event in self.events.keys():
            for i in df.index:
                ts = int(df.loc[i, "timestamp"])
                if(ts < ts_event and ts >= self.events[ts_event]['prev_ts']):
                    self.events[ts_event]['prev_ts'] = ts

    def compute_distance(self):
        """
        """
        df = pd.DataFrame(pd.read_csv("%s/table.csv"%self.path_data))
        self.distances = {}
        for ts_event in self.events:
            self.distances[ts_event] = {}
            prev_ts = self.events[ts_event]["prev_ts"]
            position = self.events[ts_event]["position"]
            masque = (df['timestamp'] >= prev_ts) & (df['timestamp'] <= ts_event)
            for i in df[masque].index:
                ts_gz = int(df[masque].loc[i, "timestamp"])
                gz = Point(float(df[masque].loc[i, "x"]),\
                    float(df[masque].loc[i, "y"]))
                if(np.isnan(gz.x) or np.isnan(gz.y)):
                    self.distances[ts_event][ts_gz-prev_ts] = np.nan
                else:
                    self.distances[ts_event][ts_gz-prev_ts] = position.distance(gz)

    def write_csv(self, folder):
        """
        """
        if not os.path.exists(folder):
            os.makedirs(folder)

        for ts_event in self.events:
            csvfile = "%s/distance_before_release_%d.csv" %\
                        (folder, ts_event)
            with open(csvfile , 'w',  newline='') as f:
                writer = csv.writer(f)
                row = ["timestamp", 'distance']
                writer.writerow(row)
                for ts in self.distances[ts_event]:
                    row = [ts, self.distances[ts_event][ts]]
                    writer.writerow(row)
