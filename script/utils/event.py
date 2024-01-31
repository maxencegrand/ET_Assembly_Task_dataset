from enum import Enum

class EventType(Enum):
    """
    Class enumerating Event Types

    G{classtree}
    """
    LEGAL = 0
    ERROR = 1
    CORRECTION = 2

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
    def __init__(self, block, position, action, type):
        """
        Construct an event

        @param block Block ID
        @param position Block Position
        @param action Action Type
        @param type Event Type
        """
        self.block = block
        self.position = position
        self.action = action
        self.type = type
