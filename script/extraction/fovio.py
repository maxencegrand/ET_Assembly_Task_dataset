#!/usr/bin/env python3.8
from utils.event import InstructionEvent
import pandas as pd
import csv
from utils.util import get_coord, get_code_timestamp
from utils.position import Point
from extraction.transposer import Transposer

WIDTH = 1280
HEIGHT = 720

class Extractor:
    """
    """
    def __init__(self,user,figure):
        """
        """
        self.user = user
        self.figure = figure
        self.path_raw_data = ("../raw_data/%s/%s/%d" % \
                    (self.user.setup, self.user.position, self.user.id))
        self.path_data = ("../dataset/%s/%s/%d/%s" % \
                    (self.user.setup, self.user.position, self.user.id, figure))
        df_instruction_event = pd.DataFrame(data=pd.read_csv(\
                        "%s/instruction_events.csv" % self.path_data))
        self.start = get_code_timestamp(df_instruction_event,\
                InstructionEvent.START.value)
        self.end = get_code_timestamp(df_instruction_event,\
                InstructionEvent.END.value)

        self.read_table_coordinates()
        self.extract()
        self.write_data()

    def read_table_coordinates(self):
        table_coord = "%s/table_coordinates.csv" % (self.path_raw_data)
        with open(table_coord, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                if(row[0] == "NO"):
                    NO = Point(float(row[1]),float(row[2]))
                elif(row[0] == "NE"):
                    NE =Point(float(row[1]),float(row[2]))
                elif(row[0] == "SO"):
                    SO = Point(float(row[1]),float(row[2]))
                elif(row[0] == "SE"):
                    SE = Point(float(row[1]),float(row[2]))
        self.transposer = Transposer(NO,NE,SE,SO)

    def extract(self):
        """
        """
        datacsv = "%s/%s/table.csv" % (self.path_raw_data, self.figure)
        df = pd.DataFrame(data=pd.read_csv(datacsv, sep = "\t", on_bad_lines='skip'))
        self.rows = [["timestamp", "x","y"]]
        # Transpose Fovio data
        for i in range(len(df.index)):
            ts = int(df.at[i, "System Time"]/1000)
            if(ts < self.start):
                continue
            if(ts > self.end):
                continue
            try:
                c_left = Point(float(df.at[i, "Lft X Pos"]),\
                            float(df.at[i, "Lft Y Pos"]))
                c_left = self.transposer.transpose(c_left)
                c_right = Point(float(df.at[i, "Rt X Pos"]),\
                            float(df.at[i, "Rt Y Pos"]))
                c_right = self.transposer.transpose(c_right)
                print(f"{c_left} {c_right}")
                val_left = int(df.at[i,"L Quality"])
                val_right = int(df.at[i,"R Quality"])
                if(val_left > 0 or val_right > 0):
                    x = ((c_left.x*val_left) + (c_right.x*val_right)) \
                        / (val_left + val_right)
                    y = ((c_left.y*val_left) + (c_right.y*val_right)) \
                        / (val_left + val_right)
                    self.rows.append([ts, x, y])
                else:
                    self.rows.append([ts,float("nan"),float("nan")])
            except Exception as inst:
                print(inst)
                self.rows.append([ts,float("nan"),float("nan")])

    def write_data(self):
        """
        """
        data_lifted = "%s/table.csv" % self.path_data

        with open(data_lifted , 'w',  newline='') as f:
            writer = csv.writer(f)
            for row in self.rows:
                writer.writerow(row)
