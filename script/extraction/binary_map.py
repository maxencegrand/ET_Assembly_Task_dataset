import numpy as np
import csv
import pandas as pd
from utils.position import Point

class BinaryMap:
    """
    """
    def __init__(self, user, figure, n_column, n_row):
        """
        """
        self.map = np.zeros((n_row, n_column))
        self.user = user
        self.figure = figure
        self.read_gazepoint()
        self.write_csv()

    def read_gazepoint(self):
        """
        """
        return

    def get_csv_file(self):
        """
        """
        return ""

    def get_gz_file(self):
        """
        """
        return ""

    def read_gazepoint(self):
        """
        """
        df = pd.DataFrame(pd.read_csv(self.get_gz_file()))
        for i in df.index:
            point = Point(float(df.loc[i,'x']),float(df.loc[i,'y']))
            if(not np.isnan(point.x) and not np.isnan(point.y) ):
                self.add(int(point.x), int(point.y))

    def get_n_column(self):
        """
        """
        _, n_col = self.map.shape
        return n_col

    def get_n_row(self):
        """
        """
        n_row, _ = self.map.shape
        return n_row

    def add(self,i,j):
        """
        """
        try:
            self.map[i,j]=1
        except:
            pass

    def write_csv(self):
        """
        """
        with open(self.get_csv_file() , 'w',  newline='') as f:
            writer = csv.writer(f)
            r = ["row", "non_zero_column"]
            writer.writerow(r)
            for i in range(self.get_n_row()):
                r = [i]
                non_zeros = []
                for j in range(self.get_n_column()):
                    if(self.map[i,j] > 0):
                        non_zeros.append(j)
                r.append(non_zeros)
                writer.writerow(r)

class TableMap(BinaryMap):
    """
    """
    def __init__(self, user, figure):
        """
        """
        BinaryMap.__init__(self, user, figure, 760, 380)

    def get_gz_file(self):
        """
        """
        return f"{self.user.get_dataset_folder()}/{self.figure}/table.csv"

    def get_csv_file(self):
        return f"{self.user.get_dataset_folder()}/{self.figure}/binary_table.csv"

    def read_gazepoint(self):
        """
        """
        df = pd.DataFrame(pd.read_csv(self.get_gz_file()))
        for i in df.index:
            point = Point(float(df.loc[i,'x']),float(df.loc[i,'y']))
            if(not np.isnan(point.x) and not np.isnan(point.y) ):
                self.add(int(point.x*10), int(point.y*10))


class ScreenMap(BinaryMap):
    """
    """
    def __init__(self, user, figure):
        """
        """
        BinaryMap.__init__(self, user, figure, 2560, 1440)

    def get_gz_file(self):
        """
        """
        return f"{self.user.get_dataset_folder()}/{self.figure}/screen.csv"

    def get_csv_file(self):
        return f"{self.user.get_dataset_folder()}/{self.figure}/binary_screen.csv"
