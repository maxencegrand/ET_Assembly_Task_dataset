#!/usr/bin/env python3.8

import numpy as np

class Point:
    """
    Class to create a point

    G{classtree}
    """
    def __init__(self,x,y):
        """
        Construct a point

        @param x the x coordinate
        @param y the y coordinate
        """
        self.x = x
        self.y = y

    def __str__(self):
        """
        The string representing the point

        @return a string
        """
        return "(%f, %f)" % (self.x, self.y)

    def distance(self, other):
        """
        Compute the distance between two points

        @param other A point
        @return The distance with the other point
        """
        return np.linalg.norm(np.array((self.x, self.y)) - np.array((other.x, other.y)))

    def get_vector(self):
        """
        Represent the point as a vector

        @return a vector
        """
        return np.array([self.x,self.y])

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

    def contains(self, point):
        """
        Check if a point is inside the 4-point position

        @param point to test

        @return true if point is inside the 4-point position
        """
        if(point.x < self.top_left.x or point.x < self.bottom_left.x):
            return False
        if(point.x > self.top_right.x or point.x > self.bottom_right.x):
            return False
        if(point.y > self.bottom_right.y or point.y > self.bottom_left.y):
            return False
        if(point.y < self.top_right.y or point.y < self.top_left.y):
            return False
        return True

    def __str__(self):
        str = "["
        str += f"{self.top_left},"
        str += f"{self.top_right},"
        str += f"{self.bottom_right},"
        str += f"{self.bottom_left}]"
        return str
