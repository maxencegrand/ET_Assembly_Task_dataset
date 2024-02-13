import pandas as pd
import cv2
from utils.device import Device
from utils.event import InstructionEvent, Action
import numpy as np

HEIGHT=800
RED = (0, 0, 255, 255)
GREEN = (0, 255, 0, 255)
BLUE = (255, 0, 0, 255)
BLACK = (0, 0, 0, 255)

def get_code_timestamp(df, value):
    df = df[df["code"] == value]
    idx = df.index[0]
    return df.loc[idx]["timestamp"]

def get_blank_image(width):
    """
    """
    image = np.zeros((HEIGHT, width, 3), np.uint8)
    image[:, :, 0] = 255
    image[:, :, 1] = 255
    image[:, :, 2] = 255

    return image

class DeviceViz:
    """
    """
    def __init__(self,user,figure):
        """
        """
        self.user = user
        self.figure = figure
        self.blocks = {}
        self.path_data = ("../dataset/%s/%s/%d/%s" % \
                    (self.user.setup, self.user.position, self.user.id, figure))
        self.path_viz = ("../dataviz/%s/%s/%d/%s" % \
                    (self.user.setup, self.user.position, self.user.id, figure))
        self.df_instruction_event = pd.DataFrame(data=pd.read_csv(\
                        "%s/instruction_events.csv" % self.path_data))
        self.start = get_code_timestamp(self.df_instruction_event,\
                InstructionEvent.START.value)
        self.end = get_code_timestamp(self.df_instruction_event,\
                InstructionEvent.END.value)
        self.generate_viz()



    def generate_viz(self):
        """
        """
        width = int((self.end - self.start)/10)
        img = get_blank_image(width)

        df = pd.DataFrame(data=pd.read_csv(\
                        "%s/gazepoints.csv" % self.path_data))
        current_device = Device(df.loc[df.index[0], "device"])
        current_ts = df.loc[df.index[0], "timestamp"]

        #Draw device
        for i in df.index:
            device = Device(df.loc[i, "device"])
            ts = df.loc[i, "timestamp"]
            if(device == current_device):
                continue
            if(current_device == Device.NO_DEVICE):
                color = RED
            elif(current_device == Device.TABLE):
                color = BLUE
            else:
                color = GREEN
            x1 = int((current_ts - self.start)/10)
            x2 = int((ts - self.start)/10)
            img = cv2.rectangle(img,(x1,100), (x2,700),color,-1)
            current_ts = ts
            current_device = device

        #Draw instruction Event
        for i in self.df_instruction_event.index:
            code = self.df_instruction_event.loc[i, "code"]
            ts = self.df_instruction_event.loc[i, "timestamp"]
            x = int((ts - self.start)/10)
            y = HEIGHT-20
            event = InstructionEvent(code)
            event_str = ""
            if(event == InstructionEvent.NEXT):
                event_str = "Next"
            elif(event == InstructionEvent.EXTRA_NEXT_ERROR):
                event_str = "Next"
            elif(event == InstructionEvent.PREVIOUS):
                event_str = "Previous"
            else:
                continue
            img = cv2.line(img, (x,100), (x,HEIGHT-50),BLACK, 7)
            img = cv2.putText(img, event_str,(x, y),cv2.FONT_HERSHEY_SIMPLEX, 2, BLACK, 10)

        #Draw action events
        df = pd.DataFrame(data=pd.read_csv(\
                        "%s/events.csv" % self.path_data))
        for i in df.index:
            type = df.loc[i, "action"]
            ts = df.loc[i, "timestamp"]
            x = int((ts - self.start)/10)
            y = 50
            action = Action(type)
            event_str = ""
            if(action == Action.GRASP):
                event_str = "grasp"
            else:
                event_str = "release"
            img = cv2.line(img, (x,50), (x,700),BLACK, 7)
            img = cv2.putText(img, event_str,(x, y),cv2.FONT_HERSHEY_SIMPLEX, 2, BLACK, 10)
        pngfile = "%s/device.png" % (self.path_viz)
        cv2.imwrite(filename=pngfile, img=img)
        cv2.waitKey(0)
