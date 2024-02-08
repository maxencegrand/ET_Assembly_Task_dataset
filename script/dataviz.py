#!/usr/bin/env python3.8

from viz.table import TableViz
import sys
from utils.user_group import Mobile

def main(argv):
    print("Viz mobile data ...")
    mobile_users = Mobile()
    for id in mobile_users.get_id_list():
        user = mobile_users.get_user(id)
        user.print_info()
        for figure in ["car", "tb", "house", "sc", "tc", "tsb"]:
        # for figure in ["car"]:
            print("Viz %s" % figure)
            # mobile_extractor.Extractor(user, figure)
            TableViz(user, figure)

    print("Viz stationary data ...")

if __name__ == "__main__":
   main(sys.argv[1:])
