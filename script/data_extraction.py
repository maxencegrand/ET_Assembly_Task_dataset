#!/usr/bin/env python3.8

import extraction.mobile as mobile_extractor
import extraction.stationary as stationary_extractor
from extraction.table_state import TableState, GoalState
from extraction.binary_map import TableMap, ScreenMap
from utils.event import event_extraction, instruction_event_extraction
from extraction.distance import GraspDistance,ReleaseDistance
import sys
from utils.user_group import Mobile, Stationary
from extraction.flow import DeviceFlow
import traceback

def main(argv):
    print("Extracting mobile data ...")
    mobile_users = Mobile()
    for id in mobile_users.get_id_list():
        user = mobile_users.get_user(id)
        user.print_info()
        if(user.has_data()):
            for figure in ["car", "tb", "house", "sc", "tc", "tsb"]:
                print("Extract %s" % figure)
                if(user.has_figure_data(figure)):
                    # event_extraction(user, figure)
                    # instruction_event_extraction(user, figure)
                    # mobile_extractor.Extractor(user, figure)
                    # TableState(user, figure)
                    # GoalState(user,figure)
                    # GraspDistance(user, figure)
                    # ReleaseDistance(user, figure)
                    # DeviceFlow(user, figure)
                    ScreenMap(user, figure)
                    TableMap(user,figure)
                else:
                    print("\tNo Data for the figure")
        else:
            print("\tNo Data for the user")

    print("Extracting stationary data ...")
    stat_users = Stationary()
    for id in stat_users.get_id_list():
        user = stat_users.get_user(id)
        user.print_info()
        if(user.has_data()):
            for figure in ["car", "tb", "house", "sc", "tc", "tsb"]:
                print("Extract %s" % figure)
                if(user.has_figure_data(figure)):
                    # event_extraction(user, figure)
                    # instruction_event_extraction(user, figure)
                    # stationary_extractor.Extractor(user, figure)
                    # TableState(user, figure)
                    # GoalState(user, figure)
                    # GraspDistance(user, figure)
                    # ReleaseDistance(user, figure)
                    # DeviceFlow(user, figure)
                    ScreenMap(user, figure)
                    TableMap(user,figure)
                else:
                    print("\tNo Data for the figure")

if __name__ == "__main__":
   main(sys.argv[1:])
