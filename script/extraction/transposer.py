#!/usr/bin/env python3.8
from utils.position import Point

class Transposer:
    """
    """
    def __init__(self,no,ne,se,ne):
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

        y1 = point.y
        x1 = self.no.x + (self.so.x - self.no.x) * \
            float((y1 - self.no.y)/(self.so.y - self.no.y))

        x2 = self.ne.x - (self.se.x - self.ne.x) * \
            float((y1 - self.ne.y)/(self.se.y - self.ne.y))3

        return Point(\
            float((point.x - x1)/(x2-x1)),\
            float((point.y - self.no.y)/(self.so.y-self.no.y)))

class ScreenTransposer(Transposer):
    """
    """
    def __init__(self):
        Transposer.__init__(\
            Point(float(410/2560), float(400/1440)),\
            Point(float(2150/2560), float(400/1440)),\
            Point(float(2480/2560), float(1350/1440)),\
            Point(float(90/2560), float(1350/1440)))
