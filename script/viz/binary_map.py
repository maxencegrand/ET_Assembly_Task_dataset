import numpy as np
import csv
import cv2
import pandas as pd
from utils.position import Point
import ast

RED = (0, 0, 255, 255)

def get_blank_image(width, height):
    """
    """
    image = np.zeros((height, width, 3), np.uint8)
    image[:, :, 0] = 255
    image[:, :, 1] = 0
    image[:, :, 2] = 0

    return image


class BinaryMap:
    """
    """
    def __init__(self, user, figure, n_column, n_row):
        """
        """
        self.user = user
        self.figure = figure
        self.n_row = n_row
        self.n_column = n_column
        self.generate_png()

    def get_csv_file(self):
        """
        """
        return ""

    def get_png_file(self):
        """
        """
        return ""

    def generate_png(self):
        """
        """
        img = get_blank_image(self.n_column, self.n_row)
        df = pd.DataFrame(pd.read_csv(self.get_csv_file()))
        for i in range(self.n_row):
            non_zeros = ast.literal_eval(df.loc[i,"non_zero_column"])
            for j in non_zeros:
                cv2.circle(img, (i, j), 1, RED, -1)

        cv2.imwrite(filename=self.get_png_file(), img=img)
        cv2.waitKey(0)

class TableMap(BinaryMap):
    """
    """
    def __init__(self, user, figure):
        """
        """
        BinaryMap.__init__(self, user, figure, 760, 380)

    def get_png_file(self):
        """
        """
        return f"{self.user.get_dataviz_folder()}/{self.figure}/binary_table.png"

    def get_csv_file(self):
        return f"{self.user.get_dataset_folder()}/{self.figure}/binary_table.csv"

class ScreenMap(BinaryMap):
    """
    """
    def __init__(self, user, figure):
        """
        """
        BinaryMap.__init__(self, user, figure, 2560, 1440)

    # def generate_png(self):
    #     """
    #     """
    #     img = get_blank_image(self.n_column, self.n_row)
    #     df = pd.DataFrame(pd.read_csv(self.get_csv_file()))
    #     for i in range(self.n_row):
    #         non_zeros = ast.literal_eval(df.loc[i,"non_zero_column"])
    #         for j in non_zeros:
    #             cv2.circle(img, (i, j), 5, RED, -1)
    #
    #     cv2.imwrite(filename=self.get_png_file(), img=img)
    #     cv2.waitKey(0)

    def get_png_file(self):
        """
        """
        return f"{self.user.get_dataviz_folder()}/{self.figure}/binary_screen.png"

    def get_csv_file(self):
        return f"{self.user.get_dataset_folder()}/{self.figure}/binary_screen.csv"
