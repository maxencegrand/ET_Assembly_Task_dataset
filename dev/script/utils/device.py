#!/usr/bin/env python3.8

import pandas as pd
from enum import Enum
from utils.position import Position
from utils.position import Point
from utils.exceptions import OutofBoundDeviceException

DEVICE_CSVFILE = "csv/device.csv"
DEVICE_POINT_ID = "id"
DEVICE_ABSTRACT_X = "x"
DEVICE_ABSTRACT_Y = "y"
DEVICE_TABLE_X = "x_mm"
DEVICE_TABLE_Y = "y_mm"
DEVICE_SCREEN_X = "x_pxl"
DEVICE_SCREEN_Y = "y_pxl"

def compute_mid_x(a1,a2,a3,a4,a5):
    return a1-float(((a1-a2)*(a5-a3))/(a4-a3))

class Device(Enum):
    """
    Class enumerating devices

    G{classtree}
    """
    TABLE = 0
    SCREEN = 1
    NO_DEVICE = 2

class DeviceManager():
    """
    Class managing devices

    G{classtree}
    """
    def __init__(self):
        """
        Constructs DeviceManager
        """
        df = pd.DataFrame(data=pd.read_csv(DEVICE_CSVFILE))
        tl = None
        tr = None
        br = None
        nl = None
        for i in df.index:
            if(df[DEVICE_POINT_ID][i] == 0):
                tl = Point(df[DEVICE_ABSTRACT_X][i],df[DEVICE_ABSTRACT_Y][i])
            elif(df[DEVICE_POINT_ID][i] == 1):
                tr = Point(df[DEVICE_ABSTRACT_X][i],df[DEVICE_ABSTRACT_Y][i])
            elif(df[DEVICE_POINT_ID][i] == 2):
                br = Point(df[DEVICE_ABSTRACT_X][i],df[DEVICE_ABSTRACT_Y][i])
            elif(df[DEVICE_POINT_ID][i] == 3):
                bl = Point(df[DEVICE_ABSTRACT_X][i],df[DEVICE_ABSTRACT_Y][i])
        #Discrete Position on the Lego Workplace
        self.abstract_position = Position(tl,tr,bl,br)

        for i in df.index:
            if(df[DEVICE_POINT_ID][i] == 0):
                tl = Point(df[DEVICE_TABLE_X][i],df[DEVICE_TABLE_Y][i])
            elif(df[DEVICE_POINT_ID][i] == 1):
                tr = Point(df[DEVICE_TABLE_X][i],df[DEVICE_TABLE_Y][i])
            elif(df[DEVICE_POINT_ID][i] == 2):
                br = Point(df[DEVICE_TABLE_X][i],df[DEVICE_TABLE_Y][i])
            elif(df[DEVICE_POINT_ID][i] == 3):
                bl = Point(df[DEVICE_TABLE_X][i],df[DEVICE_TABLE_Y][i])
        #Mm Position on the table
        position_table = Position(tl,tr,bl,br)
        for i in df.index:
            if(df[DEVICE_POINT_ID][i] == 0):
                tl = Point(df[DEVICE_SCREEN_X][i],df[DEVICE_SCREEN_Y][i])
            elif(df[DEVICE_POINT_ID][i] == 1):
                tr = Point(df[DEVICE_SCREEN_X][i],df[DEVICE_SCREEN_Y][i])
            elif(df[DEVICE_POINT_ID][i] == 2):
                br = Point(df[DEVICE_SCREEN_X][i],df[DEVICE_SCREEN_Y][i])
            elif(df[DEVICE_POINT_ID][i] == 3):
                bl = Point(df[DEVICE_SCREEN_X][i],df[DEVICE_SCREEN_Y][i])
        #Mm Position on the table
        position_screen = Position(tl,tr,bl,br)

        self.real_position = {}
        self.real_position[Device.TABLE] = position_table
        self.real_position[Device.SCREEN] = position_screen

    def get_relative_from_abstract(self, point):
        """
        Get relative coordinate from abstract coordinate

        @param point Abstract coordinate
        @param device Device on which the coordinate is computed

        @return relative position on device

        @raise OutofBoundDeviceException : raises if point is out of device
        """
        if(not self.abstract_position.contains(point)):
            raise OutofBoundDeviceException()

        x_relative = float((point.x - self.abstract_position.top_left.x)\
                    /( self.abstract_position.top_right.x - self.abstract_position.top_left.x))
        y_relative = float((point.y - self.abstract_position.top_left.y)\
                    /( self.abstract_position.bottom_left.y - self.abstract_position.top_left.y))
        return Point(x_relative, y_relative)

    def get_absolute_from_abstract(self, point, device):
        """
        Get absolute coordinate from abstract coordinate
        Mm for the table
        Pxl for the screen

        @param point Abstract coordinate
        @param device Device on which the coordinate is computed

        @return absolute position on device

        @raise OutofBoundDeviceException : raises if point is out of device
        """
        if(not self.abstract_position.contains(point)):
            raise OutofBoundDeviceException()
        relative = self.get_relative_from_abstract(point)
        return self.get_absolute_from_relative(relative, device)

    def get_abstract_from_relative(self, point, device):
        """
        Get abstract coordinate from relative coordinate

        @param point Relative coordinate
        @param device Device on which the coordinate is computed

        @return abstract position on device

        @raise OutofBoundDeviceException : raises if point is out of device
        """
        if(point.x < 0 or point.x > 1 or point.y < 0 or point.y > 1):
            raise OutofBoundDeviceException()
        x_absolute =self.real_position[device].top_left.x +\
                    (point.y * (self.real_position[device].top_right.x\
                                        -self.real_position[device].top_left.x))
        y_absolute = self.real_position[device].top_left.y + \
                    (point.y * (self.real_position[device].bottom_left.y\
                                        -self.real_position[device].top_left.y))
        return Point(x_absolute, y_absolute)

    def get_abstract_from_absolute(self, point, device):
        """
        Get abstract coordinate from absolute coordinate
        Mm for the table
        Pxl for the screen

        @param point Absolute coordinate
        @param device Device on which the coordinate is computed

        @return abstract position on device

        @raise OutofBoundDeviceException : raises if point is out of device
        """
        if(point.x < 0 or point.x > 1 or point.y < 0 or point.y > 1):
            raise OutofBoundDeviceException()
        relative = self.get_relative_from_absolute(point,device)
        return self.get_abstract_from_relative(relative, device)

    def get_relative_from_absolute(self, point, device):
        """
        Get relative coordinate from absolute coordinate
        Mm for the table
        Pxl for the screen

        @param point Absolute coordinate
        @param device Device on which the coordinate is computed

        @return abstract position on device

        @raise OutofBoundDeviceException : raises if point is out of device
        """
        right_x = compute_mid_x(\
                self.real_position[device].bottom_right.x,\
                self.real_position[device].top_right.x,\
                self.real_position[device].top_right.y,\
                self.real_position[device].bottom_right.y,\
                point.y)

        left_x = compute_mid_x(\
                self.real_position[device].bottom_left.x,\
                self.real_position[device].top_left.x,\
                self.real_position[device].top_left.y,\
                self.real_position[device].bottom_left.y,\
                point.y)

        y_relative = float((point.y) \
                            / (self.real_position[device].bottom_left.y\
                                        -self.real_position[device].top_left.y))
        x_relative = float((point.x-left_x) \
                            / (right_x-left_x))
        return Point(x_relative, y_relative)

    def get_absolute_from_relative(self, point, device):
        """
        Get relative coordinate from absolute coordinate
        Mm for the table
        Pxl for the screen

        @param point Absolute coordinate
        @param device Device on which the coordinate is computed

        @return abstract position on device

        @raise OutofBoundDeviceException : raises if point is out of device
        """
        # print(self.abstract_position)
        # print(point)
        if(point.x < 0 or point.x > 1 or point.y < 0 or point.y > 1):
            raise OutofBoundDeviceException()

        y_absolute = self.real_position[device].top_left.y +\
                    (point.y * (self.real_position[device].bottom_left.y\
                                    -self.real_position[device].top_left.y))

        right_x = compute_mid_x(\
                self.real_position[device].bottom_right.x,\
                self.real_position[device].top_right.x,\
                self.real_position[device].top_right.y,\
                self.real_position[device].bottom_right.y,\
                y_absolute)

        left_x = compute_mid_x(\
                self.real_position[device].bottom_left.x,\
                self.real_position[device].top_left.x,\
                self.real_position[device].top_left.y,\
                self.real_position[device].bottom_left.y,\
                y_absolute)
        x_absolute = left_x + (point.x * (right_x - left_x))

        return Point(x_absolute, y_absolute)
