#!/usr/bin/env python3.8

from conf.position import Position
from enum import Enum

class Shape(Enum):
    """
    Class enumerating block shapes

    G{classtree}
    """
    CUBE = 0 # 2x2 Lego Duplo Block
    BRICK = 1 # 2x4 Lego Duplo Block

class Color(Enum):
    """
    Class enumerating block colors

    G{classtree}
    """
    BLUE = 0
    RED = 1
    GREEN = 2
    YELLOW = 3

class Block:
    """
    Class representing a Lego Duplo Block

    G{classtree}
    """
    def __init__(self, id, color, shape, position):
        """
        Construct a block

        @param id Block ID
        @param color Block Color
        @param shape Block Shape
        """
        self.color = color
        self.shape = shape
        self.id = id
        self.position = position

    def is_cube(self):
        """
        Check if the block is a cube
        """
        return self.shape == Shape.CUBE
