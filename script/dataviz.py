#!/usr/bin/env python3.8

import traceback
from viz.table import TableViz
from viz.screen import ScreenViz
from viz.device import DeviceViz
from viz.binary_map import TableMap, ScreenMap
from viz.distance import GraspDistance
import sys
from utils.user_group import Mobile, Stationary

def main(argv):
    print("Viz mobile data ...")
    mobile_users = Mobile()
    for id in mobile_users.get_id_list():
        user = mobile_users.get_user(id)
        user.print_info()
        if(user.has_data()):
            for figure in ["car", "tb", "house", "sc", "tc", "tsb"]:
                print("Viz %s" % figure)
                if(user.has_figure_data(figure)):
                    # TableViz(user, figure)
                    # ScreenViz(user,figure)
                    # GraspDistance(user, figure)
                    ScreenMap(user, figure)
                    TableMap(user, figure)
                else:
                    print("\tNo Data for the figure")
        else:
            print("\tNo Data for the user")


    print("Viz stationary data ...")
    stat_users = Stationary()
    for id in stat_users.get_id_list():
        user = stat_users.get_user(id)
        user.print_info()
        if(user.has_data()):
            for figure in ["car", "tb", "house", "sc", "tc", "tsb"]:
                print("Viz %s" % figure)
                if(user.has_figure_data(figure)):
                    # TableViz(user, figure)
                    # ScreenViz(user,figure)
                    # GraspDistance(user, figure)
                    ScreenMap(user, figure)
                    TableMap(user, figure)
                else:
                    print("\tNo Data for the figure")
        else:
            print("\tNo Data for the user")

if __name__ == "__main__":
   main(sys.argv[1:])
