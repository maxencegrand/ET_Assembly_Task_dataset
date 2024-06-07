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
    image[:, :, 0] = 0
    image[:, :, 1] = 0
    image[:, :, 2] = 0

    return image

def get_color_delta(v_blue,v_red):
    """
    """
    sum = v_blue+v_red

    blue = int(255 * float(v_blue/sum))
    green = 0
    red = int(255 * float(v_red/sum))

    return (blue, green, red, 255)

def get_color(value):
    """
    """
    k1 = .2
    k2 = .2
    k3 = .2
    k4 = .4
    if(value < k1):
        #blue to cyan
        v = (value/k1)

        red = 0
        green = int(v*255)
        blue = 255
    elif(value-k1 < k2):
        #cyan to green
        v = ((value-k1)/k2)
        red = 0
        green = 255
        blue = 255 - int(v*255)
    elif(value-(k1+k2) < k3):
        #green to yellow
        v = ((value-(k1+k2))/k3)
        red = int(v*255)
        green = 255
        blue = 0
    else:
        v = ((value-(k1+k2+k3))/k4)
        red = 255
        green = 255-int(v*255)
        blue = 0
    # if(value < k1+k2):
    #     blue = 255
    #     v = ((value-.1)/.7)
    #     green = int(v*255)
    #     red = 0
    # else:
    #     blue = 0
    #     green = 0
    #     v = ((value-.8)/.2)
    #     red = int(v*255)
    return (blue, green, red, 255)

    # if(value < .5):
    #     return (255-int(value*255),0,int(value*255), 255)
    # else:
    #     return (255-int(value*255),1,int(value*255), 255)

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

    def get_png_delta_file(self, position):
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

    def generate_png_delta(self, red, position='sitting'):
        """
        """
        img = get_blank_image(self.n_column, self.n_row)
        for i in range(self.n_column):
            for j in range(self.n_row):
                v_blue = self.map[i,j]
                v_red = red.map[i,j]
                if(v_blue + v_red > 0):
                    cv2.rectangle(img, (i, j), (i+1, j+1), get_color_delta(v_blue, v_red), -1)
        pngfile = self.get_png_delta_file(position)
        print(f"Generate {pngfile}")
        cv2.imwrite(filename=pngfile, img=img)
        cv2.waitKey(0)

    def add(self, other):
        """
        """
        for i in range(self.n_column):
            for j in range(self.n_row):
                self.map[i,j] += other.map[i,j]
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

    def get_png_delta_file(self, position):
        """
        """
        return f"../data_analysis/delta_table_{position}.png"

    def get_csv_file(self, user, figure):
        return f"{user.get_dataset_folder()}/{figure}/binary_table.csv"

    def read(self, user, figure):
        """
        """
        df = pd.DataFrame(pd.read_csv(self.get_csv_file(user, figure)))
        for i in range(self.n_column):
            non_zeros = ast.literal_eval(df.loc[i,"non_zero_column"])
            for j in non_zeros:
                self.map[i,j] = 1
                for k1 in range(1,3):
                    for k2 in range(1,3):
                        try:
                            self.map[i+k1,j+k2] = 1#1-(4/(k1+k2))
                            self.map[i-k1,j-k2] = 1#1-(4/(k1+k2))
                        except:
                            continue

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

    def get_png_delta_file(self, position):
        """
        """
        return f"../data_analysis/delta_screen_{position}.png"

    def get_csv_file(self, user, figure):
        return f"{user.get_dataset_folder()}/{figure}/binary_screen.csv"

    def read(self, user, figure):
        """
        """
        df = pd.DataFrame(pd.read_csv(self.get_csv_file(user, figure)))
        for i in range(self.n_column):
            non_zeros = ast.literal_eval(df.loc[i,"non_zero_column"])
            for j in non_zeros:
                self.map[i,j] = 1
                for k1 in range(1,5):
                    for k2 in range(1,5):
                        try:
                            self.map[i+k1,j+k2] = 1#1-(4/(k1+k2))
                            self.map[i-k1,j-k2] = 1#1-(4/(k1+k2))
                        except:
                            continue

def device(users):

    positions = ['sitting']
    setups = list(users.keys())
    figures = ['car', 'tb', 'house', 'sc', 'tc', 'tsb']

    for position in positions:
        screen_map = {x:ScreenMap() for x in setups}
        table_map = {x:TableMap() for x in setups}
        n = {x:0 for x in setups}
        for setup in setups:
            for id in users[setup].get_id_list():
                user = users[setup].get_user(id)
                screen = ScreenMap()
                table = TableMap()
                if(user.position != position):
                    continue
                if(not user.has_data()):
                    continue
                user.print_info()
                for figure in figures:
                    if(not user.has_figure_data(figure)):
                        continue
                    screen.read(user, figure)
                    table.read(user, figure)
                n[setup]+=1
                screen_map[setup].add(screen)
                table_map[setup].add(table)
        for setup in setups:
            screen_map[setup].generate_png(n=n[setup], position=position, setup=setup)
            table_map[setup].generate_png(n=n[setup], position=position, setup=setup)
        screen_map['Mobile'].generate_png_delta(screen_map['Stationnary'], position=position)
        table_map['Mobile'].generate_png_delta(table_map['Stationnary'], position=position)
