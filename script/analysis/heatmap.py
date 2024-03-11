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
    image[:, :, 1] = 255
    image[:, :, 2] = 255

    return image

def get_color(value):
    """
    """
    if(value == 0):
        return (0,0,0,255)
    elif(value <= 1/6):
        return (255,0,0,255)
    elif(value <= 2/6):
        return (255,255,0,255)
    elif(value <= 3/6):
        return (0,255,0,255)
    elif(value <= 4/6):
        return (0,255,255,255)
    elif(value <= 5/6):
        return (0,0,255, 255)
    else:
        return (255,255,255, 255)

class Map:
    """
    """
    def __init__(self, n_column, n_row):
        """
        """
        self.n_row = n_row
        self.n_column = n_column
        self.map = np.zeros((n_column, n_row))

    def read(self, user, figure):
        """
        """
        df = pd.DataFrame(pd.read_csv(self.get_csv_file(user, figure)))
        for i in range(self.n_column):
            non_zeros = ast.literal_eval(df.loc[i,"non_zero_column"])
            for j in non_zeros:
                self.map[i,j] += 1

    def get_csv_file(self, user, figure):
        """
        """
        return ""

    def get_png_file(self, position):
        """
        """
        return ""

    def generate_png(self, position='sitting', setup='Mobile', n=1):
        """
        """
        img = get_blank_image(self.n_column, self.n_row)
        for i in range(self.n_column):
            for j in range(self.n_row):
                v = float(self.map[i,j]/n)
                cv2.rectangle(img, (i, j), (i+1, j+1), get_color(v), -1)
        pngfile = self.get_png_file(setup, position)
        print(f"Generate {pngfile}")
        cv2.imwrite(filename=pngfile, img=img)
        cv2.waitKey(0)

class TableMap(Map):
    """
    """
    def __init__(self):
        """
        """
        Map.__init__(self, 760, 380)

    def get_png_file(self, position, setup):
        """
        """
        return f"../data_analysis/heatmap_table_{setup}_{position}.png"

    def get_csv_file(self, user, figure):
        return f"{user.get_dataset_folder()}/{figure}/binary_table.csv"

class ScreenMap(Map):
    """
    """
    def __init__(self):
        """
        """
        Map.__init__(self, 2560, 1440)

    def get_png_file(self, position, setup):
        """
        """
        return f"../data_analysis/heatmap_screen_{setup}_{position}.png"

    def get_csv_file(self, user, figure):
        return f"{user.get_dataset_folder()}/{figure}/binary_screen.csv"

def device(users):

    positions = ['sitting', 'standing']
    setups = list(users.keys())
    figures = ['car', 'tb', 'house', 'sc', 'tc', 'tsb']

    for position in positions:
        for setup in setups:
            n = 0
            screen = ScreenMap()
            table = TableMap()
            for id in users[setup].get_id_list():
                user = users[setup].get_user(id)
                if(user.position != position):
                    continue
                if(not user.has_data()):
                    continue
                user.print_info()
                for figure in figures:
                    if(not user.has_figure_data(figure)):
                        continue
                    n+=1
                    screen.read(user, figure)
                    table.read(user, figure)
            screen.generate_png(position=position, setup=setup)
            table.generate_png(position=position, setup=setup)
