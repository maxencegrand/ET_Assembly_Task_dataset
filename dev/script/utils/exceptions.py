#!/usr/bin/env python3.8

class OutofBoundDeviceException(Exception):
    """
        Exception raised when coordinate are out of the bounds fo a device

        G{classtree}
    """
    def __init__(self, message="", payload=None):
        self.message = message
        self.payload = payload # you could add more args
    def __str__(self):
        return str(self.message) # __str__() obviously expects a string to be returned, so make sure not to send any other data types
