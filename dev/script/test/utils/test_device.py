import csv
import sys

from utils.device import DeviceManager

class TestDevice:

    def test():
        print("Test Device")
        test_device = TestDevice()

def test_device():
    try:
        TestDevice.test()
    except AssertionError:
        print("Failed")
