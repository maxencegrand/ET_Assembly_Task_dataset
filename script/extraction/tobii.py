#!/usr/bin/env python3.8
from utils.event import InstructionEvent
import pandas as pd
import csv
import math
from utils.util import get_coord, get_code_timestamp

class Extractor:
    """
    """
    def __init__(self,user,figure):
        """
        """
        self.user = user
        self.figure = figure
        self.path_raw_data = ("../raw_data/%s/%s/%d/%s" % \
                    (self.user.setup, self.user.position, self.user.id, figure))
        self.path_data = ("../dataset/%s/%s/%d/%s" % \
                    (self.user.setup, self.user.position, self.user.id, figure))
        df_instruction_event = pd.DataFrame(data=pd.read_csv(\
                        "%s/instruction_events.csv" % self.path_data))
        self.start = get_code_timestamp(df_instruction_event,\
                InstructionEvent.START.value)
        self.end = get_code_timestamp(df_instruction_event,\
                InstructionEvent.END.value)
        self.extract()
        self.write_data()

    def extract(self):
        """
        """
        # Open Tobii data csv
        data = "%s/instructions.csv" % self.path_raw_data

        # Read csv file
        self.rows = [["timestamp", \
                "x",\
                "y"]]
        all_ts = []
        with open(data, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
            first = True
            for row in spamreader:
                if first:
                    first = False
                    continue
                ts = int(row[18])
                if(ts < self.start):
                    continue
                if(ts > self.end):
                    continue
                if(ts in all_ts):
                    continue
                all_ts.append(ts)
                c_left = get_coord(row[2])
                val_left = int(row[6])
                c_right = get_coord(row[10])
                val_right = int(row[14])
                if(val_left == 1 and val_right == 1):
                    x = float((c_left[0] + c_right[0])/2)
                    y = float((c_left[1] + c_right[1])/2)
                    self.rows.append([ts, x, y])
                elif(val_left == 1 and val_right == 0):
                    self.rows.append([ts, c_left[0], c_left[1]])
                elif(val_left == 0 and val_right == 1):
                    self.rows.append([ts, c_right[0], c_right[1]])
                else:
                    self.rows.append([ts, float("nan"), float("nan")])

    def write_data(self):
        """
        """
        data_lifted = "%s/screen.csv" % self.path_data

        with open(data_lifted , 'w',  newline='') as f:
            writer = csv.writer(f)
            for row in self.rows:
                writer.writerow(row)
