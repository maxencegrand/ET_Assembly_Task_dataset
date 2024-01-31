#!/usr/bin/env python3.8

from utils.point import Point

class Position:
    """
    Class representing the 4-points position of an object

    G{classtree}
    """
    def __init__(self, top_left, top_right, bottom_left, bottom_right, level = 0):
        """
        Construct a position

        @param top_left Top Left Point
        @param top_right Top Right Point
        @param bottom_left Bottom Left Point
        @param bottom_right Bottom Right Point
        @param level Object Level
        """
        self.top_right = top_right
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.bottom_left = bottom_left
        self.level = level
