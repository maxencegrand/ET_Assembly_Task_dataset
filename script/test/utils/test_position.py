import csv
import sys

from utils.position import Position, Point

class TestPoint():
    def test_constructor(self):
        print("\tTest Constructor")
        with open('test/resources/points/constructor.csv') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                x = float(row[0])
                y = float(row[1])
                point = Point(x, y)
                try:
                    assert x == point.x
                    assert y == point.y
                except AssertionError:
                    print('Test Constructor Failed p:%s x:%s y:%s' % (p,row[1],row[2]), file=sys.stderr)
                    raise AssertionError

    def test_distance(self):
        print("\tTest Distance")
        with open('test/resources/points/distance.csv') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                x1 = float(row[0])
                y1 = float(row[1])
                x2 = float(row[2])
                y2 = float(row[3])
                p1 = Point(x1,y1)
                p2 = Point(x2,y2)
                try:
                    assert p1.distance(p2) == float(row[4])
                    assert p2.distance(p1) == float(row[4])
                except AssertionError:
                    print('Test Distance Failed p1:%s p2:%s distance:%f expected:%s' % (p1,p2,p1.distance(p2),row[4]), file=sys.stderr)
                    raise AssertionError

    def test():
        print("Test Point")
        test_point = TestPoint()
        test_point.test_constructor()
        test_point.test_distance()

class TestPosition:

    def test():
        print("Test Position")
        test_position = TestPosition()

def test_position():
    try:
        TestPoint.test()
    except AssertionError:
        print("Failed")

    try:
        TestPosition.test()
    except AssertionError:
        print("Failed")
