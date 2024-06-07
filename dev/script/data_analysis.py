from utils.user_group import Mobile, Stationary

import analysis.user as user
import analysis.event as event
import analysis.distance as distance
import analysis.flow as flow

import analysis.heatmap as heatmap

def main():
    users = {'Mobile':Mobile(),'Stationnary':Stationary()}
    # user.glasses(users)
    # user.calibration(users)
    # user.recordings(users)
    # user.specific_mobile(users['Mobile'])
    # event.action_events(users)
    # event.instructions_events(users)
    # event.assembly_durations(users)
    # event.action_events_durations(users)
    # distance.distance_analysis(users)
    # flow.behavior(users)
    heatmap.device(users)


if __name__ == "__main__":
    main()
