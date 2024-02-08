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

    def print_info(self):
        """
        print users info
        """
        print("User %d\n\t Position: %s" % (self.id, self.position))

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

    def print_info(self):
        """
        print users info
        """
        print("Mobile User %d\n\t Position: %s" % (self.id, self.position))

class Mobile:
    """
    Class representing a groupe of mobile users

    G{classtree}
    """
    def __init__(self, csvfile=MOBILE_CSVFILE):
        table = pd.DataFrame(data=pd.read_csv(csvfile))
        self.users = {}
        for i in table.index:
            self.users[i] = MobileUser(\
                int(table.loc[i][ID]),\
                table.loc[i][POSITION],\
                int(table.loc[i][GLASSES]),\
                int(table.loc[i][EYE_0]),\
                int(table.loc[i][EYE_1]),\
                int(table.loc[i][SCREEN]),\
                int(table.loc[i][PUPIL]))

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
