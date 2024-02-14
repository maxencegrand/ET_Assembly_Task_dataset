#!/usr/bin/env python3.8
import pandas as pd
from utils.event import InstructionEvent, Event, EventType, Action, Instruction
from utils.block import Block, Color, Shape
from utils.position import Point, Position
from utils.device import DeviceManager
from utils.state import State
import csv

def get_code_timestamp(df, value):
    df = df[df["code"] == value]
    idx = df.index[0]
    return df.loc[idx]["timestamp"]


class TableState:
    """
    """
    def __init__(self, user, figure):
        """
        """
        self.user = user
        self.figure = figure
        self.blocks = []
        self.path_data = ("../dataset/%s/%s/%d/%s" % \
                    (self.user.setup, self.user.position,  self.user.id, figure))
        df_instruction_event = pd.DataFrame(data=pd.read_csv(\
                        "%s/instruction_events.csv" % self.path_data))
        self.start = int(get_code_timestamp(df_instruction_event,\
                InstructionEvent.START.value))
        self.read_instruction()
        self.extract_initial_state()
        self.extract_states()
        self.write_csv()

    def read_instruction(self):
        df = pd.DataFrame(data=pd.read_csv(\
                    "csv/figures/%s/instructions.csv"%self.figure))

        self.instructions={}
        dm = DeviceManager()
        for i in df.index:
            if(i == 0):
                self.instructions[i]=Instruction(\
                    i,\
                    float("nan"),\
                    Position(\
                            Point(float("nan"), float("nan")),\
                            Point(float("nan"), float("nan")),\
                            Point(float("nan"), float("nan")),\
                            Point(float("nan"), float("nan")),\
                            level=float("nan")))
            else:
                id = int(df.loc[i,"block"])
                level = int(df.loc[i,"level"])
                x0 = int(df.loc[i,"x0"])
                y0 = int(df.loc[i,"y0"])
                tl = Point(x0-0.5, y0-0.5)
                x1 = int(df.loc[i,"x1"])
                y1 = int(df.loc[i,"y1"])
                tr = Point(x1+0.5, y1-0.5)
                x2 = int(df.loc[i,"x2"])
                y2 = int(df.loc[i,"y2"])
                br = Point(x2+0.5, y2+0.5)
                x3 = int(df.loc[i,"x3"])
                y3 = int(df.loc[i,"y3"])
                bl = Point(x3-0.5, y3+0.5)
                tl = dm.get_relative_from_abstract(tl)
                tr = dm.get_relative_from_abstract(tr)
                bl = dm.get_relative_from_abstract(bl)
                br = dm.get_relative_from_abstract(br)
                position = Position(tl,tr,bl,br,level=level)
                self.instructions[i]=Instruction(i,id,position)

        self.instructions[len(self.instructions.keys())]=Instruction(\
            len(self.instructions.keys()),\
            float("nan"),\
            Position(\
                    Point(float("nan"), float("nan")),\
                    Point(float("nan"), float("nan")),\
                    Point(float("nan"), float("nan")),\
                    Point(float("nan"), float("nan")),\
                    level=float("nan")))
    def extract_states(self):
        """
        """
        df_event = pd.DataFrame(data=pd.read_csv(\
                        "%s/events.csv" % self.path_data))
        df_inst = pd.DataFrame(data=pd.read_csv(\
                        "%s/instruction_events.csv" % self.path_data))
        self.raws = [["timestamp"]]
        for id in range(24):
            self.raws[0].append("%d_x0" % id)
            self.raws[0].append("%d_y0" % id)
            self.raws[0].append("%d_x1" % id)
            self.raws[0].append("%d_y1" % id)
            self.raws[0].append("%d_x2" % id)
            self.raws[0].append("%d_y2" % id)
            self.raws[0].append("%d_x3" % id)
            self.raws[0].append("%d_y3" % id)
            self.raws[0].append("%d_level" % id)
            self.raws[0].append("%d_holding" % id)
        self.raws[0].append("block_to_grasp")
        self.raws[0].append("to_grasp_x0")
        self.raws[0].append("to_grasp_y0")
        self.raws[0].append("to_grasp_x1")
        self.raws[0].append("to_grasp_y1")
        self.raws[0].append("to_grasp_x2")
        self.raws[0].append("to_grasp_y2")
        self.raws[0].append("to_grasp_x3")
        self.raws[0].append("to_grasp_y3")
        self.raws[0].append("to_grasp_level")
        self.add_raw(self.start)
        i = 0
        j = 0
        while(i < df_event.index.stop or j < df_inst.index.stop):
            if(i < df_event.index.stop):
                ts_event = int(df_event.loc[i, "timestamp"])
            else:
                ts_event = float('inf')
            if(j < df_inst.index.stop):
                ts_inst = int(df_inst.loc[j, "timestamp"])
            else:
                ts_inst = float("inf")
            if(ts_inst <= ts_event):
                ts = ts_inst
                code = InstructionEvent(int(df_inst.loc[j, "code"]))
                if(code == InstructionEvent.NEXT or\
                        code == InstructionEvent.EXTRA_NEXT_ERROR or\
                        code == InstructionEvent.END):
                    self.current_instruction += 1
                    self.initial_state.set_instruction(\
                        self.instructions[self.current_instruction])
                elif(code == InstructionEvent.PREVIOUS):
                    self.current_instruction -= 1
                    self.initial_state.set_instruction(\
                        self.instructions[self.current_instruction])
                else:
                    j+=1
                    continue
                j+=1
            else:
                ts = ts_event
                action = Action(df_event.loc[i, "action"])
                type = EventType(df_event.loc[i, "type"])
                block = int(df_event.loc[i, "block"])
                position = Position(\
                    Point(df_event.loc[i, "x0"], df_event.loc[i, "y0"]),\
                    Point(df_event.loc[i, "x1"], df_event.loc[i, "y1"]),\
                    Point(df_event.loc[i, "x3"], df_event.loc[i, "y3"]),\
                    Point(df_event.loc[i, "x2"], df_event.loc[i, "y2"]),\
                    level = df_event.loc[i, "level"])
                event = Event(ts, block, position, action, type)
                self.initial_state.apply(event)
                i += 1
            self.add_raw(ts)

    def get_raw(self):
        """
        """
        return self.initial_state.get_raw(list(range(24)))

    def add_raw(self,timestamp):
        """
        """
        raw = [timestamp]
        raw.extend(self.get_raw())
        self.raws.append(raw)

    def write_csv(self):
        """
        """
        csvfile = ("%s/states.csv" % (self.path_data))
        with open(csvfile , 'w',  newline='') as f:
            writer = csv.writer(f)
            for row in self.raws:
                writer.writerow(row)

    def extract_initial_state(self):
        """
        """
        self.current_instruction = 0
        df_blocks = pd.DataFrame(data=pd.read_csv("csv/blocks.csv"))
        df_stock = pd.DataFrame(data=pd.read_csv("csv/stock.csv"))
        df_instruction =pd.DataFrame(data=pd.read_csv(\
                            "csv/figures/%s/instructions.csv" % self.figure))
        dm = DeviceManager()
        id_0 = float(df_instruction.loc[df_instruction.index[0], 'block'])
        x_0 = float(df_instruction.loc[df_instruction.index[0], 'x0'])
        y_0 = float(df_instruction.loc[df_instruction.index[0], 'y0'])
        x_1 = float(df_instruction.loc[df_instruction.index[0], 'x1'])
        y_1 = float(df_instruction.loc[df_instruction.index[0], 'y1'])
        x_2 = float(df_instruction.loc[df_instruction.index[0], 'x2'])
        y_2 = float(df_instruction.loc[df_instruction.index[0], 'y2'])
        x_3 = float(df_instruction.loc[df_instruction.index[0], 'x3'])
        y_3 = float(df_instruction.loc[df_instruction.index[0], 'y3'])
        for idx in df_blocks.index:
            id = df_blocks.loc[idx, "id"]
            shape = Shape(int(df_blocks.loc[idx, "shape"]))
            color = Color(int(df_blocks.loc[idx, "color"]))
            df2 = df_stock[df_stock["block"] == id]
            x = df2.loc[df2.index[0]]["x"]
            y = df2.loc[df2.index[0]]["y"]
            if(id == id_0):
                position = Position(\
                    dm.get_relative_from_abstract(Point(x_0-.5,y_0-.5)),\
                    dm.get_relative_from_abstract(Point(x_1+.5,y_1-.5)),\
                    dm.get_relative_from_abstract(Point(x_3-.5,y_3+.5)),\
                    dm.get_relative_from_abstract(Point(x_2+.5,y_2+.5)))
            else:
                if(shape == Shape.CUBE):
                    position = Position(\
                        dm.get_relative_from_abstract(Point(x-.5,y-.5)),\
                        dm.get_relative_from_abstract(Point(x+1.5,y-.5)),\
                        dm.get_relative_from_abstract(Point(x-.5,y+1.5)),\
                        dm.get_relative_from_abstract(Point(x+1.5,y+1.5)))
                else:
                    position = Position(\
                        dm.get_relative_from_abstract(Point(x-.5,y-.5)),\
                        dm.get_relative_from_abstract(Point(x+1.5,y-.5)),\
                        dm.get_relative_from_abstract(Point(x-.5,y+3.5)),\
                        dm.get_relative_from_abstract(Point(x+1.5,y+3.5)))

            block = Block(id, color, shape, position)
            self.blocks.append(block)
        self.initial_state = State(\
            self.blocks,\
            self.instructions[self.current_instruction])

class GoalState(TableState):
    """
    """
    def __init__(self, user, figure):
        """
        """
        self.user = user
        self.figure = figure
        self.blocks = []
        self.path_data = ("../dataset/%s/%s/%d/%s" % \
                    (self.user.setup, self.user.position,  self.user.id, figure))
        df_instruction_event = pd.DataFrame(data=pd.read_csv(\
                        "%s/instruction_events.csv" % self.path_data))
        self.start = int(get_code_timestamp(df_instruction_event,\
                InstructionEvent.START.value))
        self.extract_goal_state()
        self.write_csv()

    def get_raw(self):
        """
        """
        return self.initial_state.get_raw_only_position(list(range(24)))

    def add_raw(self):
        """
        """
        raw = []
        raw.extend(self.get_raw())
        self.raws.append(raw)

    def extract_goal_state(self):
        """
        """
        self.raws = [[]]
        for id in range(24):
            self.raws[0].append("%d_x0" % id)
            self.raws[0].append("%d_y0" % id)
            self.raws[0].append("%d_x1" % id)
            self.raws[0].append("%d_y1" % id)
            self.raws[0].append("%d_x2" % id)
            self.raws[0].append("%d_y2" % id)
            self.raws[0].append("%d_x3" % id)
            self.raws[0].append("%d_y3" % id)
            self.raws[0].append("%d_level" % id)
        df_blocks = pd.DataFrame(data=pd.read_csv("csv/blocks.csv"))
        df_stock = pd.DataFrame(data=pd.read_csv("csv/stock.csv"))
        df_instruction =pd.DataFrame(data=pd.read_csv(\
                            "csv/figures/%s/instructions.csv" % self.figure))
        dm = DeviceManager()
        self.read_instruction()
        self.extract_initial_state()

        for i in df_instruction.index:
            id = float(df_instruction.loc[df_instruction.index[i], 'block'])
            x_0 = float(df_instruction.loc[df_instruction.index[i], 'x0'])
            y_0 = float(df_instruction.loc[df_instruction.index[i], 'y0'])
            x_1 = float(df_instruction.loc[df_instruction.index[i], 'x1'])
            y_1 = float(df_instruction.loc[df_instruction.index[i], 'y1'])
            x_2 = float(df_instruction.loc[df_instruction.index[i], 'x2'])
            y_2 = float(df_instruction.loc[df_instruction.index[i], 'y2'])
            x_3 = float(df_instruction.loc[df_instruction.index[i], 'x3'])
            y_3 = float(df_instruction.loc[df_instruction.index[i], 'y3'])
            level = float(df_instruction.loc[df_instruction.index[i], 'level'])

            position = Position(\
                dm.get_relative_from_abstract(Point(x_0-.5,y_0-.5)),\
                dm.get_relative_from_abstract(Point(x_1+.5,y_1-.5)),\
                dm.get_relative_from_abstract(Point(x_3-.5,y_3+.5)),\
                dm.get_relative_from_abstract(Point(x_2+.5,y_2+.5)),\
                level=level)
            self.initial_state.release(id, position)
        self.add_raw()

    def write_csv(self):
        """
        """
        csvfile = ("%s/goal.csv" % (self.path_data))
        with open(csvfile , 'w',  newline='') as f:
            writer = csv.writer(f)
            for row in self.raws:
                writer.writerow(row)
