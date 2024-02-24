#!/usr/bin/env python3.8
import pandas as pd
import cv2
from utils.block import Color
import math
BACKGROUND = "viz/resources/background.png"
WIDTH=float(1440/76)
HEIGHT=float(720/38)

BLACK = (0, 0, 0, 255)
DARK_GREY = (111, 111, 111, 255)
RED = (0, 0, 255, 255)
GREEN = (0, 255, 0, 255)
BLUE = (255, 0, 0, 255)
PURPLE = (255, 0, 255, 255)
YELLOW = (0, 255, 255, 255)
COLOR = {Color.RED:RED, Color.BLUE:BLUE, Color.YELLOW:YELLOW,Color.GREEN:GREEN}
class TableViz:
    """
    """
    def __init__(self,user,figure):
        """
        """
        self.user = user
        self.figure = figure
        self.blocks = {}
        self.path_data = ("../dataset/%s/%s/%d/%s" % \
                    (self.user.setup, self.user.position, self.user.id, figure))
        self.path_viz = ("../dataviz/%s/%s/%d/%s" % \
                    (self.user.setup, self.user.position, self.user.id, figure))
        self.extract_blocks()
        self.generate_viz()

    def extract_blocks(self):
        """
        """
        df_blocks = pd.DataFrame(data=pd.read_csv("csv/blocks.csv"))
        for i in df_blocks.index:
            # print(i)
            # print(df_blocks.loc[i])
            color = Color(df_blocks.loc[i, "color"])
            self.blocks[df_blocks.loc[i, "id"]] = {"c":color, "p":None, "h":0, "l":0}

    def generate_table_png(self, timestamp, next_timestamp):
        """
        """
        pngfile = "%s/state_%d.png" % (self.path_viz, timestamp)
        frame = cv2.imread(BACKGROUND)
        for level in [0,1,2,3,4]:
            for block in self.blocks.keys():
                if(self.blocks[block]["l"] != level):
                    continue
                start = self.blocks[block]["p"][0]
                end = self.blocks[block]["p"][1]
                color = BLACK
                if(self.blocks[block]["h"] == 1):
                    fillcolor = DARK_GREY
                else:
                    fillcolor = COLOR[self.blocks[block]["c"]]
                frame = cv2.rectangle(frame,start,end,fillcolor,-1)
                frame = cv2.rectangle(frame,start,end,color,2)
        df = pd.DataFrame(data=pd.read_csv("%s/table.csv"%self.path_data))
        for i in df.index:
            ts = df.loc[i, "timestamp"]
            if(ts < timestamp or ts >= next_timestamp):
                continue
            x = df.loc[i, "x"]
            y = df.loc[i, "y"]
            if(math.isnan(x) or math.isnan(y)):
                continue
            print([x*WIDTH,y*HEIGHT])
            frame = cv2.circle(frame, (int(x*WIDTH),int(y*HEIGHT)), radius=15, color=PURPLE, thickness=-1)
            j = i-1
            while(j >= 0):
                ts_prev = df.loc[j, "timestamp"]
                # print(f"{ts} {ts_prev} {ts - ts_prev}")
                if(ts_prev < timestamp):
                    break
                if(ts - ts_prev <= 40):
                    # print("coucou")
                    x_prev = df.loc[j, "x"]
                    y_prev = df.loc[j, "y"]
                    if(math.isnan(x_prev) or math.isnan(y_prev)):
                        j -= 1
                        continue
                    frame = cv2.line(frame, (int(x*WIDTH),int(y*HEIGHT)), (int(x_prev*WIDTH),int(y_prev*HEIGHT)), color=PURPLE, thickness=3)
                j -= 1
        cv2.imwrite(filename=pngfile, img=frame)

    def generate_viz(self):
        """
        """
        df_table = pd.DataFrame(data=pd.read_csv("%s/states.csv"%self.path_data))
        last_idx = df_table.index.stop-1
        for i in df_table.index:
            timestamp = df_table.loc[i,"timestamp"]
            if(i == last_idx):
                next_timestamp = df_table.loc[i,"timestamp"]
            else:
                next_timestamp = df_table.loc[i+1,"timestamp"]
            for block in self.blocks.keys():
                self.read_state(df_table, i, block)
            self.generate_table_png(timestamp, next_timestamp)

    def read_state(self, df, idx, block):
        """
        """
        x0 = round(df.loc[idx, "%d_x0" % block]*WIDTH)
        y0 = round(df.loc[idx, "%d_y0" % block]*HEIGHT)
        x2 = round(df.loc[idx, "%d_x2" % block]*WIDTH)
        y2 = round(df.loc[idx, "%d_y2" % block]*HEIGHT)
        holding = df.loc[idx, "%d_holding" % block]
        level = df.loc[idx, "%d_level" % block]
        self.blocks[block]["p"] = [[x0,y0],[x2,y2]]
        self.blocks[block]["h"] = holding
        self.blocks[block]["l"] = level

        print(self.blocks[block])
