from utils.device import DeviceManager, Device
from utils.position import Position, Point
import csv

if __name__=="__main__":
    dm = DeviceManager()
    print("Generate 1x1 zone")
    id=0
    raws = [["id","x0","y0","x1","y1","x2","y2","x3","y3"]]
    for i in range(48):
        for j in range(24):
            p1 = Point((i+1)-0.5, (j+1)-0.5)
            p2 = Point((i+1)+0.5, (j+1)-0.5)
            p3 = Point((i+1)-0.5, (j+1)+0.5)
            p4 = Point((i+1)+0.5, (j+1)+0.5)
            p1 = dm.get_absolute_from_abstract(p1, Device.TABLE)
            p2 = dm.get_absolute_from_abstract(p2, Device.TABLE)
            p3 = dm.get_absolute_from_abstract(p3, Device.TABLE)
            p4 = dm.get_absolute_from_abstract(p4, Device.TABLE)
            raws.append([id, p1.x, p1.y, p2.x, p2.y, p4.x, p4.y, p3.x, p3.y] )
            id+=1
            csvfile = ("csv/zone_1x1.csv")
            with open(csvfile , 'w',  newline='') as f:
                writer = csv.writer(f)
                for row in raws:
                    writer.writerow(row)
    print("Generate 2x2 zone")
    id=0
    raws = [["id","x0","y0","x1","y1","x2","y2","x3","y3"]]
    for i in range(24):
        for j in range(12):
            p1 = Point((i*2+1)-0.5, (j*2+1)-0.5)
            p2 = Point((i*2+1)+1.5, (j*2+1)-0.5)
            p3 = Point((i*2+1)-0.5, (j*2+1)+1.5)
            p4 = Point((i*2+1)+1.5, (j*2+1)+1.5)
            p1 = dm.get_absolute_from_abstract(p1, Device.TABLE)
            p2 = dm.get_absolute_from_abstract(p2, Device.TABLE)
            p3 = dm.get_absolute_from_abstract(p3, Device.TABLE)
            p4 = dm.get_absolute_from_abstract(p4, Device.TABLE)
            raws.append([id, p1.x, p1.y, p2.x, p2.y, p4.x, p4.y, p3.x, p3.y] )
            id+=1
            csvfile = ("csv/zone_2x2.csv")
            with open(csvfile , 'w',  newline='') as f:
                writer = csv.writer(f)
                for row in raws:
                    writer.writerow(row)
    print("Generate 4x4 zone")
    id=0
    raws = [["id","x0","y0","x1","y1","x2","y2","x3","y3"]]
    for i in range(12):
        for j in range(6):
            p1 = Point((i*4+1)-0.5, (j*4+1)-0.5)
            p2 = Point((i*4+1)+3.5, (j*4+1)-0.5)
            p3 = Point((i*4+1)-0.5, (j*4+1)+3.5)
            p4 = Point((i*4+1)+3.5, (j*4+1)+3.5)
            p1 = dm.get_absolute_from_abstract(p1, Device.TABLE)
            p2 = dm.get_absolute_from_abstract(p2, Device.TABLE)
            p3 = dm.get_absolute_from_abstract(p3, Device.TABLE)
            p4 = dm.get_absolute_from_abstract(p4, Device.TABLE)
            raws.append([id, p1.x, p1.y, p2.x, p2.y, p4.x, p4.y, p3.x, p3.y] )
            id+=1
            csvfile = ("csv/zone_4x4.csv")
            with open(csvfile , 'w',  newline='') as f:
                writer = csv.writer(f)
                for row in raws:
                    writer.writerow(row)
    print("Generate 8x8 zone")
    id=0
    raws = [["id","x0","y0","x1","y1","x2","y2","x3","y3"]]
    for i in range(6):
        for j in range(3):
            p1 = Point((i*8+1)-0.5, (j*8+1)-0.5)
            p2 = Point((i*8+1)+7.5, (j*8+1)-0.5)
            p3 = Point((i*8+1)-0.5, (j*8+1)+7.5)
            p4 = Point((i*8+1)+7.5, (j*8+1)+7.5)
            p1 = dm.get_absolute_from_abstract(p1, Device.TABLE)
            p2 = dm.get_absolute_from_abstract(p2, Device.TABLE)
            p3 = dm.get_absolute_from_abstract(p3, Device.TABLE)
            p4 = dm.get_absolute_from_abstract(p4, Device.TABLE)
            raws.append([id, p1.x, p1.y, p2.x, p2.y, p4.x, p4.y, p3.x, p3.y] )
            id+=1
            csvfile = ("csv/zone_8x8.csv")
            with open(csvfile , 'w',  newline='') as f:
                writer = csv.writer(f)
                for row in raws:
                    writer.writerow(row)
