#!/usr/bin/env python3.8
import pandas as pd

ID = "id"
POSITION = "position"
GLASSES = "glasses"
EYE_0 = "eye0"
EYE_1 = "eye1"
SCREEN = "screen"
PUPIL = "pupil"
TOBII = "tobii"
FOVIO = "fovio"

MOBILE_CSVFILE = "../dataset/users_mobile.csv"
STATIONARY_CSVFILE = "../dataset/users_stationary.csv"



class User:
    """
    Class representing an User

    G{classtree}
    """
    def __init__(self, id, position, glasses):
        """
        Construct an user

        @param id User ID
        @param position User's position
        @param glasses 1 if the user wear glasses
        """
        self.id = id
        self.position = position
        self.time = {"car":0, "tb":0, "house":0, "sc":0, "tc":0, "tsb":0}
        self.error = {"car":0, "tb":0, "house":0, "sc":0, "tc":0, "tsb":0}
        self.setup = ""
        self._has_data = True
        self._has_figure_data = \
            {"car":True, "tb":True, "house":True, "sc":True, "tc":True, "tsb":True}
        self.glasses = (glasses == 1)

    def is_wearing_glasses(self):
        """
        """
        return self.glasses

    def print_info(self):
        """
        print users info
        """
        print("User %d\n\t Position: %s" % (self.id, self.position))

    def has_data(self):
        """
        Check if data exist for the user

        @return True if data exist for the user
        """
        return self._has_data

    def has_figure_data(self, figure):
        """
        Check if figure data exist for the user

        @param figure Figure to check
        @return True if figure data exist for the user
        """
        return self._has_figure_data[figure]

    def get_dataset_folder(self):
        """
        """
        return f"../dataset/{self.setup}/{self.position}/{self.id}"

    def get_dataviz_folder(self):
        """
        """
        return f"../dataviz/{self.setup}/{self.position}/{self.id}"

    def get_raw_data_folder(self):
        """
        """
        return f"../raw_data/{self.setup}/{self.position}/{self.id}"
class Group:
    """
    Class representing a group of users

    G{classtree}
    """
    def __init__(self):
        """
        Constructs a group of users
        """
        self.users={}

    def get_id_list(self):
        """
        @return The list of mobile users id
        """
        return self.users.keys()

    def get_user(self,id):
        """
        @return
        """
        return self.users[id]
class MobileUser(User):
    """
    Class representing a mobile user

    G{classtree}
    """
    def __init__(self, id, position, glasses, eye0, eye1, screen, pupil):
        """
        Constructs a mobile user

        @param id User ID
        @param position User's position
        @param glasses 1 if the user wear glasses
        @param eye0 1 if eye0 was used
        @param eye1 1 if eye1 was used
        @param screen number of screen border seen
        @param pupil Calibration score for the pupil tracker
        """
        User.__init__(self, id, position, glasses)
        self.eye0 = eye0
        self.eye1 = eye1
        self.screen = screen
        self.pupil = pupil
        self.setup = "mobile"
        self._has_data = pupil > 0

    def print_info(self):
        """
        print users info
        """
        print("Mobile User %d\n\t Position: %s" % (self.id, self.position))

class Mobile(Group):
    """
    Class representing a groupe of mobile users

    G{classtree}
    """
    def __init__(self, csvfile=MOBILE_CSVFILE):
        Group.__init__(self)
        table = pd.DataFrame(data=pd.read_csv(csvfile))
        for i in table.index:
            self.users[i] = MobileUser(\
                int(table.loc[i][ID]),\
                table.loc[i][POSITION],\
                int(table.loc[i][GLASSES]),\
                int(table.loc[i][EYE_0]),\
                int(table.loc[i][EYE_1]),\
                int(table.loc[i][SCREEN]),\
                int(table.loc[i][PUPIL]))
            for f in ["car", "tb", "house", "sc", "tc", "tsb"]:
                self.users[i]._has_figure_data[f] = (int(table.loc[i][f]) == 1)


class StationaryUser(User):
    """
    Class representing a stationary user

    G{classtree}
    """
    def __init__(self, id, position, glasses, fovio, tobii):
        """
        Constructs a mobile user

        @param id User ID
        @param position User's position
        @param glasses 1 if the user wear glasses
        @param fovio Calibration score for the fovio tracker
        @param tobii Calibration score for the tobii tracker
        """
        User.__init__(self, id, position, glasses)
        self.tobii = tobii
        self.fovio = fovio
        self.setup = "stationnary"
        self._has_data = (tobii > 0 and fovio > 0)

    def print_info(self):
        """
        print users info
        """
        print("Stationary User %d\n\t Position: %s" % (self.id, self.position))

class Stationary(Group):
    """
    Class representing a groupe of stationary users

    G{classtree}
    """
    def __init__(self, csvfile=STATIONARY_CSVFILE):
        Group.__init__(self)
        table = pd.DataFrame(data=pd.read_csv(csvfile))
        for i in table.index:
            self.users[i] = StationaryUser(\
                int(table.loc[i][ID]),\
                table.loc[i][POSITION],\
                int(table.loc[i][GLASSES]),\
                int(table.loc[i][FOVIO]),\
                int(table.loc[i][TOBII]))
            for f in ["car", "tb", "house", "sc", "tc", "tsb"]:
                self.users[i]._has_figure_data[f] = (int(table.loc[i][f]) == 1)
