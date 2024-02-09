#!/usr/bin/env python3.8

import extraction.mobile as mobile_extractor
import extraction.stationary as stationary_extractor
from extraction.table_state import TableState
import sys
from utils.user_group import Mobile, Stationary

def main(argv):
    print("Extracting mobile data ...")
    # mobile_users = Mobile()
    # for id in mobile_users.get_id_list():
    #     user = mobile_users.get_user(id)
    #     user.print_info()
    #     # for figure in ["car"]:
    #     for figure in ["car", "tb", "house", "sc", "tc", "tsb"]:
    #         print("Extract %s" % figure)
    #         mobile_extractor.Extractor(user, figure)
    #         TableState(user, figure)

    print("Extracting stationary data ...")
    stat_users = Stationary()
    for id in stat_users.get_id_list():
        user = stat_users.get_user(id)
        user.print_info()
        # for figure in ["car"]:
        for figure in ["car", "tb"]:
            print("Extract %s" % figure)
            stationary_extractor.Extractor(user, figure)
            TableState(user, figure)

if __name__ == "__main__":
   main(sys.argv[1:])
