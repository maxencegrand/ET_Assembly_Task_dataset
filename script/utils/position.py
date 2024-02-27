#!/usr/bin/env python3.8

import numpy as np
from utils.util import min

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

    def distance_to_segment(self, point1, point2):
        """
        Compute the distance between the current point and a line segment defined by two points.

        @param point1: First point of the segment.
        @param point2: Second point of the segment.
        @return: The distance between the point and the line segment.
        """
        x_p, y_p = self.x, self.y
        x_A, y_A = point1.x, point1.y
        x_B, y_B = point2.x, point2.y

        segment_length = np.sqrt((x_B - x_A)**2 + (y_B - y_A)**2)

        if segment_length == 0:
            # A and B are the same point, so distance is the distance to that single point
            return np.sqrt((x_p - x_A)**2 + (y_p - y_A)**2)

        # Use the formula for the distance from a point to a line segment
        distance = np.abs((x_B - x_A) * (y_A - y_p) - (x_A - x_p) * (y_B - y_A)) / segment_length

        return distance

    def is_above(self, point1, point2):
        """
        Check if the current point is above the line defined by two points.

        Warning: the origin is at the top left

        @param point1: First point of the line.
        @param point2: Second point of the line.
        @return: True if the point is above the line, False otherwise.
        """
         # Calculate the expected y value on the line for the horizontal position of the point
        expected_y = ((self.x - point1.x) / (point2.x - point1.x)) * (point2.y - point1.y) + point1.y

        # Check if the point is above the line
        return self.y <= expected_y

    def is_below(self, point1, point2):
        """
        Check if the current point is below the line defined by two points.

        Warning: the origin is at the top left

        @param point1: First point of the line.
        @param point2: Second point of the line.
        @return: True if the point is below the line, False otherwise.
        """
         # Calculate the expected y value on the line for the horizontal position of the point
        expected_y = ((self.x - point1.x) / (point2.x - point1.x)) * (point2.y - point1.y) + point1.y

        # Check if the point is below the line
        return self.y >= expected_y

    def is_point_right_of_segment(self, point1, point2):
        """
        Check if the current point is to the right of a line segment defined by two points.

        Warning: the origin is at the top left

        @param point1: The first point of the line segment.
        @param point2: The second point of the line segment.
        @return: True if the point is to the right, False otherwise.
        """
        expected_x = (point1.x - point2.x) * ((point2.y-point1.y) / (point2.y - self.y)) + point2.x

        return self.y >= expected_x

    def is_point_left_of_segment(self, point1, point2):
        """
        Check if the current point is to the left of a line segment defined by two points.

        Warning: the origin is at the top left

        @param point1: The first point of the line segment.
        @param point2: The second point of the line segment.
        @return: True if the point is to the right, False otherwise.
        """
        expected_x = (point1.x - point2.x) * ((point2.y-point1.y) / (point2.y - self.y)) + point2.x

        return self.y <= expected_x

    def distance_to_segment(self, point1, point2):
        """
        Compute the distance between the current point and a line segment defined by two points.

        Warning: the origin is at the top left

        @param point1: First point of the segment.
        @param point2: Second point of the segment.
        @return: The distance between the point and the line segment.
        """
        x_p, y_p = self.x, self.y
        x_A, y_A = point1.x, point1.y
        x_B, y_B = point2.x, point2.y

        segment_length = np.sqrt((x_B - x_A)**2 + (y_B - y_A)**2)

        if segment_length == 0:
            # A and B are the same point, so distance is the distance to that single point
            return np.sqrt((x_p - x_A)**2 + (y_p - y_A)**2)

        # Use the formula for the distance from a point to a line segment
        distance = np.abs((x_B - x_A) * (y_A - y_p) - (x_A - x_p) * (y_B - y_A)) / segment_length

        return distance

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
        Check if a point is inside the position.

        @param point: The point to check.
        @return: True if the point is inside, False otherwise.
        """
        # Check if the point is to the left of the right side and to the right of the left side
        is_inside_horizontal = (
            point.is_point_left_of_segment(self.top_right, self.bottom_right) and
            point.is_point_right_of_segment(self.top_left, self.bottom_left)
        )

        # Check if the point is below the top side and above the bottom side
        is_inside_vertical = (
            point.is_below(self.top_left, self.top_right) and
            point.is_above(self.bottom_left, self.bottom_right)
        )

        # The point is inside the position if it satisfies both horizontal and vertical conditions
        return is_inside_horizontal and is_inside_vertical

    def distance(self, point):
        """
        The distance between the current position and the point
        The distance is the minimal distance between the point and each side
        If the point is inside the position, the distance is negative

        @param point: The point
        @return: The distance
        """
        # Calculate the distance to each side
        # distances = [
        #     point.distance_to_segment(self.top_left, self.top_right),
        #     point.distance_to_segment(self.top_right, self.bottom_right),
        #     point.distance_to_segment(self.bottom_right, self.bottom_left),
        #     point.distance_to_segment(self.bottom_left, self.top_left)
        # ]
        distances = [
            point.distance(self.top_left),
            point.distance(self.top_right),
            point.distance(self.bottom_left),
            point.distance(self.bottom_right)
        ]

        # If the point is inside the position, return the minimum distance with a negative sign
        if self.contains(point):
            return -min(distances)
        else:
            # Otherwise, return the minimum distance
            return min(distances)

    def __str__(self):
        """
        """
        str = "["
        str += f"{self.top_left},"
        str += f"{self.top_right},"
        str += f"{self.bottom_right},"
        str += f"{self.bottom_left}]"
        return str
