#!/usr/bin/env python3.8
from enum import Enum
import pandas as pd
from utils.device import DeviceManager, Device
from utils.position import Point
import csv

class InstructionEvent(Enum):
    """
    Class enumerating Instruction Events

    G{classtree}
    """
    START = 0
    NEXT = 1
    PREVIOUS = 2
    NO_NEXT_ERROR = 3
    EXTRA_NEXT_ERROR = 4
    END = 5


class Instruction():
    """
    Class representing an Instruction

    G{classtree}
    """
    def __init__(self, id, block, position):
        """
        Construct an instruction

        @param id Instruction ID
        @param block Block Id to grasp
        @param position Position where release the grasped block
        """
        self.id = id
        self.block = block
        self.position = position

    def __str__(self):
        """
        """
        return f"Instruction {self.id}\n\t{self.block}\n\t{self.position}"

    def get_raw(self):
        """
        """
        return [\
            self.block,\
            self.position.top_left.x,\
            self.position.top_left.y,\
            self.position.top_right.x,\
            self.position.top_right.y,\
            self.position.bottom_right.x,\
            self.position.bottom_right.y,\
            self.position.bottom_left.x,\
            self.position.bottom_left.y,\
            self.position.level]

class EventType(Enum):
    """
    Class enumerating Event Types

    G{classtree}
    """
    LEGAL = 0
    ERROR = 1
    BAD_ID = 2
    CORRECTION = 3


class Action(Enum):
    """
    Class enumerating Actions

    G{classtree}
    """
    GRASP = 0
    RELEASE = 1

class Event:
    """
    Class representing an event

    G{classtree}
    """
    def __init__(self, timestamp, block, position, action, type):
        """
        Construct an event

        @param timestamp Event Timestamp
        @param block Block ID
        @param position Block Position
        @param action Action Type
        @param type Event Type
        """
        self.timestamp = timestamp
        self.block = block
        self.position = position
        self.action = action
        self.type = type

    def is_grasp(self):
        """
        """
        return self.action == Action.GRASP

    def is_release(self):
        """
        """
        return self.action == Action.RELEASE

    def get_raw(self):
        """
        Return containing the event at timestamp
        """
        return [self.timestamp, \
            self.action, \
            self.block, \
            self.position.top_left.x, \
            self.position.top_left.y, \
            self.position.top_right.x, \
            self.position.top_right.y, \
            self.position.bottom_right.x, \
            self.position.bottom_right.y, \
            self.position.bottom_left.x, \
            self.position.bottom_left.y, \
            self.position.level, \
            self.type]

def event_extraction(user, figure, rep="../raw_data"):
    '''
    '''
    raw_data = ("%s/%s/%s/%s/%s/events.csv" % \
                (rep, user.setup, user.position, user.id, figure))
    if(user.setup == "mobile"):
        data = ("%s/%s/%s/%s/%s/events_frame.csv" % \
                    ("../dataset", user.setup, user.position, user.id, figure))
    else:
        data = ("%s/%s/%s/%s/%s/events.csv" % \
                    ("../dataset", user.setup, user.position, user.id, figure))
    events = {}
    df = pd.DataFrame(data=pd.read_csv(raw_data))
    device = DeviceManager()
    raws = [["timestamp","action","block","x0","y0","x1","y1","x2","y2","x3","y3","level","type"]]
    for i in df.index:
        ts = int(df.loc[i, "timestamp"])
        action = int(df.loc[i, "action"])
        x0 = float(df.loc[i, "x0"])
        y0 = float(df.loc[i, "y0"])
        point0 = device.get_absolute_from_relative(Point(x0,y0), Device.TABLE)
        x1 = float(df.loc[i, "x1"])
        y1 = float(df.loc[i, "y1"])
        point1 = device.get_absolute_from_relative(Point(x1,y1), Device.TABLE)
        x2 = float(df.loc[i, "x2"])
        y2 = float(df.loc[i, "y2"])
        point2 = device.get_absolute_from_relative(Point(x2,y2), Device.TABLE)
        x3 = float(df.loc[i, "x3"])
        y3 = float(df.loc[i, "y3"])
        point3 = device.get_absolute_from_relative(Point(x3,y3), Device.TABLE)
        level = int(df.loc[i, "level"])
        type = int(df.loc[i, "action"])
        raws.append([ts, action,\
                    point0.x, point0.y,\
                    point1.x, point1.y,\
                    point2.x, point2.y,\
                    point3.x, point3.y, level, type])

    csvfile = (data)
    with open(csvfile , 'w',  newline='') as f:
        writer = csv.writer(f)
        for raw in raws:
            writer.writerow(raw)

def instruction_event_extraction(user, figure, rep="../raw_data"):
    '''
    '''
    raw_data = ("%s/%s/%s/%s/%s/instruction_events.csv" % \
                (rep, user.setup, user.position, user.id, figure))
    if(user.setup == "mobile"):
        data = ("%s/%s/%s/%s/%s/instruction_events_frame.csv" % \
                    ("../dataset", user.setup, user.position, user.id, figure))
    else:
        data = ("%s/%s/%s/%s/%s/instruction_events.csv" % \
                    ("../dataset", user.setup, user.position, user.id, figure))
    events = {}
    df = pd.DataFrame(data=pd.read_csv(raw_data))
    device = DeviceManager()
    raws = [["timestamp","code"]]
    for i in df.index:
        ts = int(df.loc[i, "timestamp"])
        code = int(df.loc[i, "code"])
        raws.append([ts, code,])

    csvfile = (data)
    with open(csvfile , 'w',  newline='') as f:
        writer = csv.writer(f)
        for raw in raws:
            writer.writerow(raw)
