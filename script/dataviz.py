#!/usr/bin/env python3.8

import traceback
from viz.table import TableViz
from viz.screen import ScreenViz
import sys
from utils.user_group import Mobile, Stationary

def main(argv):
    print("Viz mobile data ...")
    mobile_users = Mobile()
    # for id in mobile_users.get_id_list():
    #     user = mobile_users.get_user(id)
    #     user.print_info()
    #     for figure in ["car", "tb", "house", "sc", "tc", "tsb"]:
    #     # for figure in ["car"]:
    #         try:
    #             print("Viz %s" % figure)
    #             TableViz(user, figure)
    #             ScreenViz(user,figure)
    #         except:
    #             print("Error during data visualization")
    #             # traceback.print_exc()
    #             # sys.exit(1)

    print("Viz stationary data ...")
    stat_users = Stationary()
    for id in stat_users.get_id_list():
        user = stat_users.get_user(id)
        user.print_info()
        # for figure in ["car"]:
        for figure in ["car", "tb", "house", "sc", "tc", "tsb"]:
            try:
                print("Viz %s" % figure)
                TableViz(user, figure)
                ScreenViz(user,figure)
            except:
                print("Error during data visualization")
                traceback.print_exc()
if __name__ == "__main__":
   main(sys.argv[1:])
