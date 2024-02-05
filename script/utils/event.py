#!/usr/bin/env python3.8
from enum import Enum

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
    BAD_BLOCK_ID_ERROR = 5


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
            self.type]
