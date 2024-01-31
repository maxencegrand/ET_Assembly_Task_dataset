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
