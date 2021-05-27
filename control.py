"""Simple example showing how to get gamepad events."""
# create exe : pyinstaller --onefile -w control.py

from __future__ import print_function
import time
from inputs import get_gamepad

HIGH_TH = 127 + 8
LOW_TH = 127 - 8

class PTZ():

    def __init__(self):
        self.pan = 0
        self.absolute_switch = {
            "ABS_RX" : self.update_pan,
            "ABS_RZ" : self.update_tilt,

            "ABS_Y" : self.update_zoom
        }
        self.btn_switch = {
            "BTN_THUMB" : self.manage_preset,
            "BTN_THUMB2" : self.manage_preset,
            "BTN_TOP" : self.manage_preset,
            "BTN_TRIGGER" : self.manage_preset,

            "BTN_BASE" : self.manage_common_btn,
            "BTN_BASE2" : self.manage_common_btn,

        }        





    def update_pan(self, val):
        print("pan")
        
        if(val > HIGH_TH ):
            self.pan = (val - HIGH_TH) / 6.4
        elif(val < LOW_TH ):
            self.pan = -(HIGH_TH - val) / 6.4
        else:
            self.pan = 0

    def update_tilt(self, val):
        print("tilt")
        pass

    def update_zoom(self, val):
        print("zoom")
        pass    

    def update_focus(self, val):
        print("focus")
        pass   



    def manage_preset(self, btn, val):
        print("preset")

        if(btn == "BTN_THUMB"):
            if( val == 1):
                self.BTN_THUMB_t0 = time.time()
            else:
                BTN_THUMB_t1 = time.time()
                BTN_THUMB_dt = BTN_THUMB_t1 - self.BTN_THUMB_t0
                print(BTN_THUMB_dt)
                if (BTN_THUMB_dt < 2.5):
                    print("short")
                else:
                    print("long")
        pass   


    def manage_common_btn(self, val):
        print("common_btn")
        pass      


    def main(self):
        """Just print out some event infomation when the gamepad is used."""
        while 1:
            events = get_gamepad()
            for event in events:

                if(event.ev_type == "Absolute" ):

                    if event.code in self.absolute_switch.keys():
                        self.absolute_switch[event.code](event.state)

                if(event.ev_type == "Key" ):

                    if event.code in self.btn_switch.keys():
                        self.btn_switch[event.code](event.code, event.state)



                #print(event.ev_type, event.code, event.state)




if __name__ == "__main__":
    ptz = PTZ()
    ptz.main()