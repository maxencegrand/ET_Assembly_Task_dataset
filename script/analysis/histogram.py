import csv,sys
import pandas as pd
from utils.user_group import Mobile, Stationary
import matplotlib.pyplot as plt
import numpy as np
from utils.event import EventType, InstructionEvent, Action
from utils.position import Point, Position
from extraction.flow import FlowDFA

def histogram(fig, ax, r, width, val, xlabel, ylabel,title, png, categories=None, ymax=100):
    print(f"Plot {png}")
    labels = list(val.keys())
    for idx_label, label in enumerate(labels):
        ax.bar(
            r + (idx_label * width),\
            val[label]['values'],
            width=width,
            color=val[label]['color'],
            label=label)
    if(categories != None):
        ax.set_xticks(r + width/len(categories),categories)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0,ymax)
    ax.legend()
    fig.savefig(png)
    plt.close()

def histogram_percent(fig, ax, r, width, val, xlabel, ylabel,title, png, categories, ymax=100, xmin=0, xmax=10):
    print(f"Plot {png}")
    labels = list(val.keys())
    for idx_label, label in enumerate(labels):
        unique_values, counts = np.unique(val[label]['values'], return_counts=True)
        percentages = (counts / len(val[label]['values'])) * 100
        I=unique_values
        print(unique_values)
        x_ = [r[i]+(idx_label * width) for i in I]
        ax.bar(
            x_,\
            percentages,
            width=width,
            color=val[label]['color'],
            label=label)
    ax.set_xticks(r + width/len(categories),categories)
    ax.set_xticklabels(categories)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(0,ymax)
    ax.legend()
    fig.savefig(png)
    plt.close()

def histogram_percent_interval(fig, ax, r, width, val, xlabel, ylabel,title, png, categories=None, ymax=100, xmin=0, xmax=10, interval_width=10):
    print(f"Plot {png}")
    labels = list(val.keys())
    for idx_label, label in enumerate(labels):
        unique_values, counts = np.unique(val[label]['values'], return_counts=True)
        percentages = (counts / len(val[label]['values'])) * 100
        I=unique_values
        x_ = [r[int(i/interval_width)]+(idx_label * width) for i in I]
        ax.bar(
            x_,\
            percentages,
            width=width,
            color=val[label]['color'],
            label=label)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(0,ymax)
    ax.legend()
    fig.savefig(png)
    plt.close()
