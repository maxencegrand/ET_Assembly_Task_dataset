#!/usr/bin/env python3.8

import sys, getopt
import csv, os
import argparse# Create the parser
from utils.event import InstructionEvent

def main():
    parser = argparse.ArgumentParser()# Add an argument
    parser.add_argument('-path', type=str, required=True)
    parser.add_argument('-user', type=str, required=True)
    parser.add_argument('-figure', type=str, required=True)
    parser.add_argument('-setup', type=str, required=True)
    parser.add_argument('-position', type=str, required=True)

    args = parser.parse_args()

    if(args.setup == "mobile"):
        csvfile = ("%s/%s/%s/%s/%s/instruction_events_frame.csv" % (\
                    args.path,\
                    args.setup,\
                    args.position,\
                    args.user,\
                    args.figure))
    else:
        csvfile = ("%s/%s/%s/%s/%s/instruction_events.csv" % (\
                    args.path,\
                    args.setup,\
                    args.position,\
                    args.user,\
                    args.figure))
    data = []

    print("Welcome to the instruction annotation module")
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
        code = int(input("Code %d:Start/%d:Next/%d:Previous/%d:No Next Error/%d:Extra Next Error/%d:Bad Block ID Error " % (\
                InstructionEvent.START.value,InstructionEvent.NEXT.value,InstructionEvent.PREVIOUS.value,InstructionEvent.NO_NEXT_ERROR.value,InstructionEvent.EXTRA_NEXT_ERROR.value, InstructionEvent.BAD_BLOCK_ID_ERROR.value)))
        data.append([ts,code])

    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',\
            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["timestamp", "code"])
        for row in data:
            spamwriter.writerow(row)

    print("Figure %s has been instruction-annotated for the user %s" %\
            (args.figure, args.user))

if __name__ == "__main__":
   main()
