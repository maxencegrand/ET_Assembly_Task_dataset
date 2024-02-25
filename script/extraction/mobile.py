#!/usr/bin/env python3.8
import pandas as pd
from utils.event import InstructionEvent
import json
import numpy as np
import csv
from utils.position import Point
from utils.device import DeviceManager, Device

KEY_SYNC = "start_time_synced_s"
KEY_SYSTEM = "start_time_system_s"

DISPLAY = {"screen":["Screen"], "table":["Assembly","Left","Right"]}
SURFACE = {"Screen":{"offset":0, "width":1},\
            "Left":{"offset":0, "width":float(14/48)},\
            "Assembly":{"offset":float(14/48), "width":float(20/48)},\
            "Right":{"offset":float(34/48), "width":float(14/48)}}
DEVICE = {"screen":Device.SCREEN, "table":Device.TABLE}
def get_code_timestamp(df, value):
    df = df[df["code"] == value]
    idx = df.index[0]
    return df.loc[idx]["timestamp"]

class Extractor:
    """

    """
    def __init__(self, user, figure):
        """

        """
        self.device = DeviceManager()
        self.user = user
        self.figure = figure

        self.path_raw_data = ("../raw_data/%s/%s/%d/%s" % \
                    (self.user.setup, self.user.position, self.user.id, figure))
        self.path_data = ("../dataset/%s/%s/%d/%s" % \
                    ( self.user.setup, self.user.position, self.user.id,figure))

        # Convert pupil frame into system timestamps
        self.extract_timestamps()
        self.transpose_annotations()

        df_instruction_event = pd.DataFrame(data=pd.read_csv(\
                        "%s/instruction_events.csv" % self.path_data))
        self.start = get_code_timestamp(df_instruction_event,\
                InstructionEvent.START.value)
        self.end = get_code_timestamp(df_instruction_event,\
                InstructionEvent.END.value)
        duration = (self.end - self.start) / 1000
        # print("Assembly starts at %d and lasts at %d" % (self.start, duration))
        self.extract("table")
        self.extract("screen")

    def extract(self,display):
        df_surfaces = {}
        for s in DISPLAY[display]:
            csvfile = "%s/exports/000/surfaces/gaze_positions_on_surface_%s.csv" \
                    % (self.path_raw_data, s)
            df_surfaces[s] = pd.DataFrame(data=pd.read_csv (csvfile))
        rows = [["timestamp", \
                "x",\
                "y"]]

        for idx in range(len(self.timestamps)):
            ts = int(self.timestamps[idx])
            if(ts < self.start):
                continue
            if(ts > self.end):
                continue

            no_data = True
            for s in DISPLAY[display]:
                df = df_surfaces[s]
                data = df.loc[df["world_index"] == idx]
                # print(data)

                if(len(data) > 0):
                    i = data.index[0]
                    if(data.at[i,"on_surf"]):
                        no_data = False
                        eye = Point(data.at[i, "x_norm"],data.at[i, "y_norm"])
                        eye.x = SURFACE[s]["offset"]+(eye.x * SURFACE[s]["width"])
                        eye.y = 1-eye.y
                        eye = self.device.get_absolute_from_relative(eye, DEVICE[display])
                        rows.append([ts, eye.x, eye.y])
                        break
            if(no_data):
                rows.append([ts, float("nan"), float("nan")])
        #
        csvfile = "%s/%s.csv" % \
                (self.path_data, display)
        # print(csvfile)
        with open(csvfile , 'w',  newline='') as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)

    def extract_timestamps(self):
        """
        """
        jsonfile = ("%s/info.player.json" % (self.path_raw_data))
        data = json.load(open(jsonfile))
        start_sync = data[KEY_SYNC]
        start_system = data[KEY_SYSTEM]
        self.offset=( start_system - start_sync)
        npyfile = ("%s/world_timestamps.npy" % (self.path_raw_data))
        data = np.load(npyfile)
        self.timestamps = []
        for d in data:
            # print(d)
            self.timestamps.append((d+self.offset)*1000)

    def transpose_annotations(self):
        """
        """
        #Transpose events
        csvfile = ("%s/events_frame.csv" % (self.path_data))
        df = pd.DataFrame(data=pd.read_csv(csvfile))
        rows = [["timestamp","action","block",\
                "x0", "y0", "x1", "y1", "x2", "y2", "x3", "y3",\
                "level", "type"]]
        # print(self.timestamps)
        for frame in df["timestamp"].tolist():
            # print(frame)
            timestamp = self.timestamps[frame]
            action = df.loc[df["timestamp"]==frame]["action"].tolist()[0]
            block = df.loc[df["timestamp"]==frame]["block"].tolist()[0]
            x0 = df.loc[df["timestamp"]==frame]["x0"].tolist()[0]
            y0 = df.loc[df["timestamp"]==frame]["y0"].tolist()[0]
            x1 = df.loc[df["timestamp"]==frame]["x1"].tolist()[0]
            y1 = df.loc[df["timestamp"]==frame]["y1"].tolist()[0]
            x2 = df.loc[df["timestamp"]==frame]["x2"].tolist()[0]
            y2 = df.loc[df["timestamp"]==frame]["y2"].tolist()[0]
            x3 = df.loc[df["timestamp"]==frame]["x3"].tolist()[0]
            y3 = df.loc[df["timestamp"]==frame]["y3"].tolist()[0]
            level = df.loc[df["timestamp"]==frame]["level"].tolist()[0]
            type = df.loc[df["timestamp"]==frame]["type"].tolist()[0]
            rows.append([timestamp,action,block,x0,y0,x1,y1,x2,y2,x3,y3,level,type])
        csvfile = ("%s/events.csv" % (self.path_data))
        with open(csvfile , 'w',  newline='') as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)

        # Transpose instructions
        csvfile = ("%s/instruction_events_frame.csv" % (self.path_data))
        df = pd.DataFrame(data=pd.read_csv(csvfile))
        rows = [["timestamp","code"]]
        for frame in df["timestamp"].tolist():
            timestamp = int(self.timestamps[frame])
            code = df.loc[df["timestamp"]==frame]["code"].tolist()[0]
            rows.append([timestamp,code])
        csvfile = ("%s/instruction_events.csv" % (self.path_data))
        with open(csvfile , 'w',  newline='') as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)
