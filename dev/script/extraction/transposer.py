#!/usr/bin/env python3.8
from utils.position import Point
import math

class Transposer:
    """
    """
    def __init__(self,no,ne,se,so):
        """
        """
        self.no = no
        self.ne = ne
        self.se = se
        self.so = so

    def transpose(self, point):
        """
        """
        if(math.isnan(point.x) or math.isnan(point.y)):
            return Point(float("nan"), float("nan"))

        x1 = self.no.x + float(((self.so.x - self.no.x) * \
            (point.y - self.no.y))/(self.so.y - self.no.y))

        y1 = self.ne.y + float(((self.no.y - self.ne.y) * \
            (self.ne.x - point.x))/ (self.ne.x - self.no.x))

        x2 = self.ne.x - float(((self.ne.x - self.se.x) * \
            (point.y - self.ne.y))/(self.se.y - self.ne.y))

        y2 = self.so.y - float(((self.so.y - self.se.y) * \
            (point.x - self.so.x))/ (self.se.x - self.so.x))

        return Point(\
            float((point.x - x1)/(x2-x1)),\
            float((point.y - y1)/(y2-y1)))

class ScreenTransposer(Transposer):
    """
    """
    def __init__(self):
        Transposer.__init__(\
            Point(float(410/2560), float(400/1440)),\
            Point(float(2150/2560), float(400/1440)),\
            Point(float(2480/2560), float(1350/1440)),\
            Point(float(90/2560), float(1350/1440)))
