#!/usr/bin/env python3.8

import extraction.mobile as mobile_extractor
import extraction.stationary as stationary_extractor
from extraction.table_state import TableState, GoalState
import sys
from utils.user_group import Mobile, Stationary
from extraction.dataset import Dataset
import traceback

def main(argv):
    print("Extracting mobile data ...")
    mobile_users = Mobile()
    for id in mobile_users.get_id_list():
        user = mobile_users.get_user(id)
        user.print_info()
        # for figure in ["car"]:
        for figure in ["car", "tb", "house", "sc", "tc", "tsb"]:
            print("Extract %s" % figure)
            try:
                mobile_extractor.Extractor(user, figure)
                TableState(user, figure)
                GoalState(user,figure)
                Dataset(user,figure)
            except:
                print("Error during extraction")
                # traceback.print_exc()
                # sys.exit(1)

    print("Extracting stationary data ...")
    stat_users = Stationary()
    for id in stat_users.get_id_list():
        user = stat_users.get_user(id)
        user.print_info()
        # for figure in ["car"]:
        for figure in ["car", "tb", "house", "sc", "tc", "tsb"]:
            try:
                print("Extract %s" % figure)
                stationary_extractor.Extractor(user, figure)
                TableState(user, figure)
                Dataset(user,figure)
            except:
                print("Error during extraction")

if __name__ == "__main__":
   main(sys.argv[1:])
