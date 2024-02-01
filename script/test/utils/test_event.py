import csv
import sys

from utils.event import Event, Instruction

class TestEvent:
    def test():
        print("Test Event")
        test_event = TestEvent()

class TestInstruction:
    def test():
        print("Test Instruction")
        test_event = TestInstruction()

def test_event():
    try:
        TestEvent.test()
    except AssertionError:
        print("Failed")

    try:
        TestInstruction.test()
    except AssertionError:
        print("Failed")
