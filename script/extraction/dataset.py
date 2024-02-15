#!/usr/bin/env python3.8

import pandas as pd
import csv
import math
from utils.device import Device

class Dataset:
    """
    """
    def __init__(self,user,figure):
        """
        """
        self.user = user
        self.figure = figure
        self.path_data = ("../dataset/%s/%s/%d/%s" % \
                    (self.user.setup, self.user.position, self.user.id, figure))
        self.generate_dataset()
        self.write_csv()

    def get_current_state(self, df, ts):
        """
        """
        res = []
        for i in df.index:
            ts_i = df.loc[i, "timestamp"]
            if(ts == ts_i):
                return ts_i
            if(i+1 >= df.index.stop):
                return -1
            i_next = i+1
            ts_next = df.loc[i_next, "timestamp"]
            if(ts > ts_i and ts < ts_next):
                return ts_i


    def generate_dataset(self):
        """
        """
        self.raws = [["timestamp", "x", "y", "device", "idx_table"]]
        df_table = pd.DataFrame(data=pd.read_csv(\
                                        "%s/states.csv" % self.path_data))
        df_gz_table = pd.DataFrame(data=pd.read_csv(\
                                        "%s/table.csv" % self.path_data))
        df_gz_screen = pd.DataFrame(data=pd.read_csv(\
                                        "%s/screen.csv" % self.path_data))
        id_table = 0
        id_gz_table = 0
        id_gz_screen = 0
        while(id_gz_table < df_gz_table.index.stop \
                    or id_gz_screen < df_gz_screen.index.stop):
            raw = []
            if(id_gz_table < df_gz_table.index.stop and\
                id_gz_screen < df_gz_screen.index.stop):
                ts_table = df_gz_table.loc[id_gz_table, "timestamp"]
                ts_screen = df_gz_screen.loc[id_gz_screen, "timestamp"]
                if(ts_table == ts_screen):
                    ts = ts_table
                    x_table = df_gz_table.loc[id_gz_table, "x"]
                    y_table = df_gz_table.loc[id_gz_table, "y"]
                    x_screen = df_gz_screen.loc[id_gz_screen, "x"]
                    y_screen = df_gz_screen.loc[id_gz_screen, "y"]
                    if(math.isnan(x_screen) or math.isnan(y_screen)):
                        if(math.isnan(x_table) or math.isnan(y_table)):
                            x = x_table
                            y = y_table
                            device = Device.NO_DEVICE
                        else:
                            x = x_table
                            y = y_table
                            device = Device.TABLE
                    else:
                        x = x_screen
                        y = y_screen
                        device = Device.SCREEN
                    raw=[ts,x,y,device.value]
                    id_gz_table += 1
                    id_gz_screen += 1
                elif(ts_table < ts_screen):
                    ts = df_gz_table.loc[id_gz_table, "timestamp"]
                    x = df_gz_table.loc[id_gz_table, "x"]
                    y = df_gz_table.loc[id_gz_table, "y"]
                    if(math.isnan(x) or math.isnan(y)):
                        raw = [ts,x,y,Device.NO_DEVICE]
                    else:
                        raw = [ts,x,y,Device.TABLE]
                    id_gz_table += 1
                else:
                    ts = df_gz_screen.loc[id_gz_screen, "timestamp"]
                    x = df_gz_screen.loc[id_gz_screen, "x"]
                    y = df_gz_screen.loc[id_gz_screen, "y"]
                    if(math.isnan(x) or math.isnan(y)):
                        raw = [ts,x,y,Device.NO_DEVICE]
                    else:
                        raw = [ts,x,y,Device.SCREEN]
                    id_gz_screen += 1

            elif(id_gz_table < df_gz_table.index.stop):
                ts = df_gz_table.loc[id_gz_table, "timestamp"]
                x = df_gz_table.loc[id_gz_table, "x"]
                y = df_gz_table.loc[id_gz_table, "y"]
                if(math.isnan(x) or math.isnan(y)):
                    raw = [ts,x,y,Device.NO_DEVICE]
                else:
                    raw = [ts,x,y,Device.TABLE]
                id_gz_table += 1
            else:
                ts = df_gz_screen.loc[id_gz_screen, "timestamp"]
                x = df_gz_screen.loc[id_gz_screen, "x"]
                y = df_gz_screen.loc[id_gz_screen, "y"]
                if(math.isnan(x) or math.isnan(y)):
                    raw = [ts,x,y,Device.NO_DEVICE]
                else:
                    raw = [ts,x,y,Device.SCREEN]
                id_gz_screen += 1

            raw.append(self.get_current_state(df_table, ts))
            self.raws.append(raw)


    def write_csv(self):
        """
        """
        csvfile = ("%s/gazepoints.csv" % (self.path_data))
        with open(csvfile , 'w',  newline='') as f:
            writer = csv.writer(f)
            for row in self.raws:
                writer.writerow(row)
