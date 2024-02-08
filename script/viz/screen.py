#!/usr/bin/env python3.8
import pandas as pd
import cv2
from utils.block import Color
import math
from utils.event import InstructionEvent

WIDTH=2560
HEIGHT=1440
PURPLE = (255, 0, 255, 255)

class ScreenViz:
    """
    """
    def __init__(self,user,figure):
        """
        """
        self.user = user
        self.figure = figure
        self.blocks = {}
        self.path_data = ("../dataset/mobile/%s/%d/%s" % \
                    (self.user.position, self.user.id, figure))
        self.path_viz = ("../dataviz/mobile/%s/%d/%s" % \
                    (self.user.position, self.user.id, figure))
        self.generate_viz()

    def generate_viz(self):
        """
        """
        df_inst = pd.DataFrame(data=pd.read_csv("%s/instruction_events.csv"%self.path_data))
        last_idx = df_inst.index.stop-1
        id_slide = 0
        for i in df_inst.index:
            if(i == last_idx):
                continue
            timestamp = int(df_inst.loc[i,"timestamp"])
            next_timestamp = int(df_inst.loc[i+1,"timestamp"])
            code = InstructionEvent(int(df_inst.loc[i, "code"]))
            if(code == InstructionEvent.NEXT \
                    or code == InstructionEvent.EXTRA_NEXT_ERROR):
                id_slide += 1
            elif(code == InstructionEvent.PREVIOUS):
                id_slide -= 1
            self.generate_screen_png(id_slide, timestamp, next_timestamp)

    def generate_screen_png(self, id_slide, timestamp, next_timestamp):
        """
        """
        pngfile = "%s/instruction_%d.png" % (self.path_viz, timestamp)

        if(id_slide == 0):
            background = "viz/resources/instructions/%s/figure.png" % (self.figure)
        else:
            background = "viz/resources/instructions/%s/step%d.png" % (self.figure, id_slide)

        frame = cv2.imread(background)
        df = pd.DataFrame(data=pd.read_csv("%s/screen.csv"%self.path_data))
        for i in df.index:
            ts = df.loc[i, "timestamp"]
            if(ts < timestamp or ts >= next_timestamp):
                continue
            x = df.loc[i, "x"]
            y = df.loc[i, "y"]
            if(math.isnan(x) or math.isnan(y)):
                continue
            frame = cv2.circle(frame, (int(x*WIDTH),int(y*HEIGHT)), radius=5, color=PURPLE, thickness=-1)
        # print(pngfile)
        cv2.imwrite(filename=pngfile, img=frame)
