import csv
import sys

from utils.block import Block

class TestBlock:
    def test():
        print("Test Block")
        test_block = TestBlock()

def test_block():
    try:
        TestBlock.test()
    except AssertionError:
        print("Failed")
