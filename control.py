"""Simple example showing how to get gamepad events."""
# create exe : pyinstaller --onefile -w control.py

from __future__ import print_function
import time
from inputs import get_gamepad

import requests

import urllib.request

IP = "192.168.1.88"

GAMEPAD = "XBOX"

""" HIGH_TH = 127 + 8
LOW_TH = 127 - 8 """

CAM_MAX = 20
JOY_MAX = 32767
JOY_MIN = -32767
HIGH_TH = 6000
LOW_TH = -6000
JOY_CAM_RATIO = CAM_MAX / (JOY_MAX - HIGH_TH )


class PTZ():

    def __init__(self):
        self.pan = 0
        self.pan_ori = "left"
        self.tilt = 0
        self.tilt_ori = "up"
        self.zoom = 0
        self.zoom_ori = "zoomin"
        self.Preset = 0
        self.absolute_switch = {
            "ABS_PAN" : self.update_pan,
            "ABS_TILT" : self.update_tilt,
            "ABS_ZOOM" : self.update_zoom,
            "ABS_FOCUS_IN" : self.update_focus_in,
            "ABS_FOCUS_OUT" : self.update_focus_out      
        }

        self.btn_switch = {
            "BTN_PRESET0" : self.manage_preset,
            "BTN_PRESET1" : self.manage_preset,
            "BTN_PRESET2" : self.manage_preset,
            "BTN_PRESET3" : self.manage_preset,
        }        

        self.map_XBOX = {
            "BTN_NORTH" : "BTN_PRESET0",
            "BTN_SOUTH" : "BTN_PRESET1",
            "BTN_EAST" : "BTN_PRESET2",
            "BTN_WEST" : "BTN_PRESET3",

            "ABS_RX" : "ABS_PAN",
            "ABS_RY" : "ABS_TILT",
            "ABS_Y" : "ABS_ZOOM",    
            "ABS_RZ" : "ABS_FOCUS_IN",
            "ABS_Z" : "ABS_FOCUS_OUT"       
        }

        self.map_CPE = {
            "BTN_THUMB" : "BTN_PRESET0",
            "BTN_THUMB" : "BTN_PRESET1",
            "BTN_TOP"   : "BTN_PRESET2",
            "BTN_TRIGGER" : "BTN_PRESET3",

            "ABS_RX" : "ABS_PAN",
            "ABS_RZ" : "ABS_TILT",
            "ABS_Y" : "ABS_ZOOM"            
        }        

        self.map = {
            "XBOX" : self.map_XBOX,
            "CPE"  : self.map_CPE
        }

        self.ori_pan = {
            "+" : "right",
            "-" : "left"
        }

        self.ori_tilt = {
            "+" : "up",
            "-" : "down"
        }   

        self.ori_zoom = {
            "+" : "zoomin",
            "-" : "zoomout"
        } 

        self.ori_focus = {
            "+" : "focusin",
            "-" : "focusout"
        }                       
     
        

    def update_axis_cmd(self, val):
        if(val > HIGH_TH ):
            axis = min((val - HIGH_TH) * JOY_CAM_RATIO, CAM_MAX)
            axis_ori = '+'
        elif(val < LOW_TH ):
            axis = min(abs(val - LOW_TH) * JOY_CAM_RATIO, CAM_MAX)
            axis_ori = '-'
        else:
            axis = 0  
            axis_ori = '+'

        return int(axis), axis_ori



    def update_pan(self, val):
        self.pan, ori = self.update_axis_cmd(val)  
        self.pan_ori = self.ori_pan[ori]
        
        if self.pan != 0 :
            p = requests.get("http://"+ IP + "/cgi-bin/ptzctrl.cgi?ptzcmd&{0}&{1}&{2}".format(self.pan_ori, self.pan, self.tilt) )
            print("pan : ", self.pan)    
        
        elif self.tilt == 0:
            p = requests.get("http://"+ IP + "/cgi-bin/ptzctrl.cgi?ptzcmd&{0}&{1}&{2}".format("ptzstop", self.pan, self.tilt) )



    def update_tilt(self, val):
        self.tilt, ori = self.update_axis_cmd(val)  
        self.tilt_ori = self.ori_tilt[ori]   
        
        if self.tilt != 0 :
            p = requests.get("http://"+ IP + "/cgi-bin/ptzctrl.cgi?ptzcmd&{0}&{1}&{2}".format(self.tilt_ori, self.pan, self.tilt) )
            print("tilt : ", self.tilt)
        
        elif self.pan == 0:
            p = requests.get("http://"+ IP + "/cgi-bin/ptzctrl.cgi?ptzcmd&{0}&{1}&{2}".format("ptzstop", self.pan, self.tilt) )


    def update_zoom(self, val):
        self.zoom, ori = self.update_axis_cmd(val)  
        self.zoom_ori = self.ori_zoom[ori]    
        
        if self.zoom != 0 :
            p = requests.get("http://"+ IP + "/cgi-bin/ptzctrl.cgi?ptzcmd&{0}&{1}".format(self.zoom_ori, self.zoom) )
            print("zoom : ", self.zoom)  
        else:
            p = requests.get("http://"+ IP + "/cgi-bin/ptzctrl.cgi?ptzcmd&{0}&{1}".format("zoomstop", self.zoom) )


    def update_focus_in(self, val):

        if(abs(val) > 20 ):
            axis = min((val - 20) * (20/(255-20)), 20)
            axis_ori = '+'
        else:
            axis = 0  
            axis_ori = '+'

        self.focus = int(axis)
        self.focus_ori = self.ori_focus[axis_ori]    
        
        if self.focus != 0 :
            p = requests.get("http://"+ IP + "/cgi-bin/ptzctrl.cgi?ptzcmd&{0}&{1}".format(self.focus_ori, self.focus) )
            print("focus : ", self.focus)  
        else:
            p = requests.get("http://"+ IP + "/cgi-bin/ptzctrl.cgi?ptzcmd&{0}&{1}".format("focusstop", self.focus) )
            print("stop focus : ", self.focus)    


    def update_focus_out(self, val):

        if(abs(val) > 20 ):
            axis = min((val - 20) * (20/(255-20)), 20)
            axis_ori = '-'
        else:
            axis = 0  
            axis_ori = '-'

        self.focus = int(axis)
        self.focus_ori = self.ori_focus[axis_ori]    
        
        if self.focus != 0 :
            p = requests.get("http://"+ IP + "/cgi-bin/ptzctrl.cgi?ptzcmd&{0}&{1}".format(self.focus_ori, self.focus) )
            print("focus : ", self.focus)  
        else:
            p = requests.get("http://"+ IP + "/cgi-bin/ptzctrl.cgi?ptzcmd&{0}&{1}".format("focusstop", self.focus) )
            print("stop focus : ", self.focus)     



    def manage_preset(self, btn, val):
        print("preset")

        if( val == 1):
            self.BTN_t0 = time.time()
        else:
            BTN_t1 = time.time()
            BTN_dt = BTN_t1 - self.BTN_t0
            print(BTN_dt)
            if (BTN_dt < 2):
                print("short")
                pos = "poscall"
            else:
                print("long")
                pos = "posset"

            if(btn == "BTN_PRESET0"):
                self.Preset = 0
            elif(btn == "BTN_PRESET1"):
                self.Preset = 1
            elif(btn == "BTN_PRESET2"):
                self.Preset = 2
            elif(btn == "BTN_PRESET3"):
                self.Preset = 3  
            p = requests.get("http://"+ IP + "/cgi-bin/ptzctrl.cgi?ptzcmd&" + pos + "&" + str(self.Preset))
  


    def manage_common_btn(self, val):
        print("common_btn")
        pass      


    def main(self):
        """Just print out some event infomation when the gamepad is used."""
        while 1:
            events = get_gamepad()
            for event in events:

                if(event.ev_type == "Absolute" ):

                    if event.code in self.map[GAMEPAD].keys():
                        self.absolute_switch[ self.map[GAMEPAD][event.code] ](event.state)


                if(event.ev_type == "Key" ):

                    if event.code in self.map[GAMEPAD].keys():
                        self.btn_switch[ self.map[GAMEPAD][event.code] ](self.map[GAMEPAD][event.code], event.state)
                        



                #print(event.ev_type, event.code, event.state)




if __name__ == "__main__":
    ptz = PTZ()
    ptz.main()