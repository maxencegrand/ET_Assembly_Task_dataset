import pandas as pd
from utils.event import Action
from utils.position import Position, Point
from utils.state import State
import numpy as np
import matplotlib.pyplot as plt
import math

class GraspDistance:
    """
    Generate dataviz for distance before grasp
    """
    def __init__(self, user, figure):
        """
        """
        self.user = user
        self.figure = figure
        self.path_data = "../dataset/%s/%s/%d/%s" % \
                (self.user.setup, self.user.position, self.user.id, figure)
        self.path_viz = "../dataviz/%s/%s/%d/%s" % \
                (self.user.setup, self.user.position, self.user.id, figure)
        self.read_grasp_events()
        self.read_distance()
        self.generate_viz_all_block()
        self.generate_distance_to_grasp_histogram()
        self.generate_closest_probability()

    def read_grasp_events(self):
        """
        """
        self.events = {}
        df = pd.DataFrame(pd.read_csv("%s/events.csv"%self.path_data))
        for i in df.index:
            ts = int(df.loc[i, "timestamp"])
            act = Action(int(df.loc[i, "action"]))
            if(act == Action.RELEASE):
                continue
            else:
                block_id = int(df.loc[i, "block"])
                self.events[ts] = block_id

    def read_distance(self):
        """
        """
        self.distances = {}
        for ts_event in self.events:
            df = pd.DataFrame(pd.read_csv(\
                "%s/distances_before_grasp/distance_all_blocks_before_grasp_%d.csv"%\
                (self.path_data, ts_event)))

            self.distances[ts_event] = {}
            for block_id in range(24):
                self.distances[ts_event][block_id] = {}
            for i in df.index:
                ts_dist = int(df.loc[i, "timestamp"])
                for block_id in range(24):
                    dist = df.loc[i, "block_%d"%block_id]
                    self.distances[ts_event][block_id][ts_dist] = dist

    def generate_viz_all_block(self):
        """
        """
        for ts_event in self.events.keys():
            pngfile = f"{self.path_viz}/distance_all_blocks_before_grasp_{ts_event}"
            fig, axs = plt.subplots(5, 5, figsize=(25, 25))
            for i in range(5):
                for j in range(5):
                    if i == 4 and j > 3:
                        axs[i, j].axis('off')
                    else:
                        ax = axs[i, j]
                        block_id = i*5+j
                        to_grasp = self.events[ts_event]
                        abs = []
                        ord = []
                        all_ts=[]
                        for ts in self.distances[ts_event][block_id].keys():
                            if(np.isnan(self.distances[ts_event][block_id][ts])):
                                all_ts.append(ts)
                                continue
                            abs.append(ts)
                            ord.append(10*self.distances[ts_event][block_id][ts])
                        if(block_id == to_grasp):
                            ax.scatter(abs, ord,c='red')
                        else:
                            ax.scatter(abs, ord,c='lightgray')
                        ax.set_xlabel('Time')
                        ax.set_ylabel('Distance (mm)')
                        if(block_id == to_grasp):
                            ax.set_title(f'Block {block_id} (TO GRASP)')
                        else:
                            ax.set_title(f'Block {block_id}')
                        ax.set_xlim(0, 1 if(len(all_ts) == 0) else max(all_ts))
                        ax.set_ylim(-40, 600)
            fig.savefig(pngfile)
            plt.close(fig)

    def generate_distance_to_grasp_histogram(self):
        """
        """
        self.distance_to_grasp = {}
        self.distance_not_to_grasp = {}
        for ts_event in self.events.keys():
            pngfile = f"{self.path_viz}/distances_before_grasp_{ts_event}"
            self.distance_to_grasp[ts_event] = []
            self.distance_not_to_grasp[ts_event] = []
            to_grasp = self.events[ts_event]
            n = 0
            for ts in self.distances[ts_event][to_grasp].keys():
                dist = self.distances[ts_event][to_grasp][ts]
                if(not np.isnan(dist)):
                    self.distance_to_grasp[ts_event].append(10*dist)
                    n += 1
                all_dist = 0
                n_blocks = 0
                for block_id in self.distances[ts_event]:
                    dist = self.distances[ts_event][block_id][ts]
                    if(not np.isnan(dist)):
                        all_dist += dist
                        n_blocks += 1
                if(n_blocks > 0):
                    self.distance_not_to_grasp[ts_event].append(\
                                10*float(all_dist)/n_blocks)
            freq = {}
            freq_not = {}
            interval_width = 8
            for dist in self.distance_to_grasp[ts_event]:
                rounded_dist = round(dist / interval_width) * interval_width
                freq[rounded_dist] = freq.get(rounded_dist, 0) + 1
            for dist in self.distance_not_to_grasp[ts_event]:
                rounded_dist = round(dist / interval_width) * interval_width
                freq_not[rounded_dist] = freq_not.get(rounded_dist, 0) + 1
            for rounded_dist in freq:
                freq[rounded_dist] = (freq[rounded_dist]/n)*100
            for rounded_dist in freq_not:
                freq_not[rounded_dist] = (freq_not[rounded_dist]/n)*100
            bar_width = 4
            plt.bar(freq.keys(), freq.values(),\
                width=bar_width, color='red')
            plt.ylim(0, 80)
            plt.xlim(-30, 600)
            plt.xlabel('Distances (mm)')
            plt.ylabel('Frequency (%)')
            plt.title('Distance Repartition to the Grasped Block ')
            plt.savefig(pngfile)
            plt.close()

    def generate_closest_probability(self):
        self.is_closest = {}
        for ts_event in self.events.keys():
            last_ts = 0
            pngfile = f"{self.path_viz}/is_closest_before_grasp_{ts_event}"
            self.is_closest[ts_event] = {}
            to_grasp = self.events[ts_event]
            for ts in self.distances[ts_event][to_grasp].keys():
                if(ts > last_ts):
                    last_ts = ts
                dist = self.distances[ts_event][to_grasp][ts]
                if(not np.isnan(dist)):
                    self.is_closest[ts_event][ts] = True
                    for block_id in self.distances[ts_event]:
                        if(block_id == to_grasp):
                            continue
                        if(self.distances[ts_event][block_id][ts] < dist):
                            self.is_closest[ts_event][ts] = False
                            break
            is_closest_freq = {}
            n = 0
            n_total = 0

            for ts in self.is_closest[ts_event]:
                n_total += 1
                if(self.is_closest[ts_event][ts]):
                    n += 1
                is_closest_freq[float(ts/last_ts)] = [n, n_total]
            for ts in is_closest_freq:
                is_closest_freq[ts] =\
                    float(is_closest_freq[ts][0]/is_closest_freq[ts][1])*100
            plt.plot(is_closest_freq.keys(),is_closest_freq.values(),\
                        color='red')
            plt.ylim(0, 100)
            plt.xlim(0, 1)
            plt.xlabel('Normalised Time')
            plt.ylabel('Prob (%)')
            plt.title('Probability to be the closest block')
            plt.savefig(pngfile)
            plt.close()
