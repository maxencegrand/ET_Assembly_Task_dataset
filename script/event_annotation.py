#!/usr/bin/env python3.8

import sys, getopt
import csv, os
import argparse# Create the parser
from utils.event import EventType, Action, Event
from utils.block import Shape
from utils.device import DeviceManager, Device
from utils.position import Point, Position

def main():
    device = DeviceManager()
    parser = argparse.ArgumentParser()# Add an argument
    parser.add_argument('-path', type=str, required=True)
    parser.add_argument('-user', type=str, required=True)
    parser.add_argument('-figure', type=str, required=True)
    parser.add_argument('-setup', type=str, required=True)
    parser.add_argument('-position', type=str, required=True)

    args = parser.parse_args()

    csvfile = ("%s/%s/%s/%s/%s/events.csv" % (\
                args.path,\
                args.setup,\
                args.position,\
                args.user,\
                args.figure))
    data = []

    print("Welcome to the event annotation module")
    print("User ID: %s" % args.user)
    print("Figure: %s" % args.figure)
    print("\nData will be save in the file: %s"%csvfile)

    cont = "y"
    while(cont == "" or cont == "y" or cont == "Y"):
        cont = input("Add new event? (y/n)")
        if(cont == "n" or cont == "N"):
            break
        elif(not(cont == "" or cont == "y" or cont == "Y")):
            cont = ""
            continue
        ts = int(input("Timestamp: "))
        id = int(input("Block ID:"))
        action = int(input("Action %d:Grasp/%d:Release " % (Action.GRASP.value, Action.RELEASE.value)))
        type = int(input("Type %d:Legal/%d:Error/%d:Bad Id/%d:Correction " % (\
                EventType.LEGAL.value,EventType.ERROR.value,EventType.BAD_ID.value,EventType.CORRECTION.value)))
        x = int(input("Top Left x: "))
        y = int(input("Top Left y: "))
        o = int(input("Orientation 0:Vertical/1:Horizontal "))
        shape = int(input("Shape %d:Cube/%d:Brick " % (Shape.CUBE.value, Shape.BRICK.value)))
        level = int(input("level: "))

        #Compute position
        tl = Point(x-0.5, y-0.5)
        bl = None
        tr = None
        br = None
        if(shape == Shape.CUBE):
            tr = Point(tl.x+2, tl.y)
            br = Point(tl.x+2, tl.y+2)
            bl = Point(tl.x, tl.y+2)
        else:
            if(o == 0):
                tr = Point(tl.x+2, tl.y)
                br = Point(tl.x+2, tl.y+4)
                bl = Point(tl.x, tl.y+4)
            else:
                tr = Point(tl.x+4, tl.y)
                br = Point(tl.x+4, tl.y+2)
                bl = Point(tl.x, tl.y+2)
        tl = device.get_relative_from_abstract(tl)
        tr = device.get_relative_from_abstract(tr)
        bl = device.get_relative_from_abstract(bl)
        br = device.get_relative_from_abstract(br)

        position = Position(tl, tr, bl, br)
        print(position)
        #Create event and add raw
        event = Event(ts, id, position, action, type)
        data.append(event.get_raw())

    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',\
            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["timestamp", "action", "block",\
                "x0", "y0","x1", "y1","x2", "y2","x3", "y3","type"])
        for row in data:
            spamwriter.writerow(row)

    print("Figure %s has been event-annotated for the user %s" %\
            (args.figure, args.user))

if __name__ == "__main__":
   main()
