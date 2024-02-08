#!/usr/bin/env python3.8
from utils.block import Block

import cv2
from mss import mss
from PIL import Image

DARK_GREY = (0, 0, 255, 255)
RED = (0, 0, 255, 255)
GREEN = (0, 255, 0, 255)
BLUE = (255, 0, 0, 255)
YELLOW = (0, 255, 255, 255)

class State():
    """
    Class implementing a state

    G{classtree}
    """
    def __init__(self, blocks):
        """
        """
        self.blocks = {}
        for b in blocks:
            self.blocks[b.id] = {"block":b,"holding":0}

    def apply(self, event):
        """
        """
        if(event.is_grasp()):
            self.grasp(event.block)
        else:
            self.release(event.block, event.position)

    def grasp(self, id):
        """
        """
        self.blocks[id]["holding"]=1

    def release(self, id, position):
        """
        """
        self.blocks[id]["holding"]=0
        self.blocks[id]["block"].position = position

    def get_raw(self, ids):
        """
        """
        raw = []
        for id in ids:
            raw.append(self.blocks[id]["block"].position.top_left.x)
            raw.append(self.blocks[id]["block"].position.top_left.y)
            raw.append(self.blocks[id]["block"].position.top_right.x)
            raw.append(self.blocks[id]["block"].position.top_right.y)
            raw.append(self.blocks[id]["block"].position.bottom_right.x)
            raw.append(self.blocks[id]["block"].position.bottom_right.y)
            raw.append(self.blocks[id]["block"].position.bottom_left.x)
            raw.append(self.blocks[id]["block"].position.bottom_left.y)
            raw.append(self.blocks[id]["block"].position.level)
            raw.append(self.blocks[id]["holding"])
        return raw

    def get_png(self, pngfile):
        width = 240
        height = 480
