from enum import Enum

class InstructionEvent(Enum):
    """
    Class enumerating Instruction Events

    G{classtree}
    """
    NEXT = 0
    PREVIOUS = 1
    NO_NEXT_ERROR = 2
    EXTRA_NEXT_ERROR = 3
    BAD_BLOCK_ID_ERROR = 4


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
