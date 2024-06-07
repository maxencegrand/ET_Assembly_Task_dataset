import csv
import sys

from utils.state import State

class TestState:
    def test():
        print("Test State")
        test_state = TestState()

def test_state():
    try:
        TestState.test()
    except AssertionError:
        print("Failed")
