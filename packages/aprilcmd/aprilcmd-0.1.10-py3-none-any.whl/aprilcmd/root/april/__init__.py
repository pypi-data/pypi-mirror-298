from util import *
import os

class AprilManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "april"
        self.type = "April"
        pass

    def check(self):
        return True
        if os.uname().nodename != "ygh":
            return False
        try:
            import speech_recognition
            Aset.set("april.speech_recognition", true)
        except:
            self._info("april with out speech_recognition")
            self._info("april checking ...(failed)")  
            return False
        try:
            import pyttsx3
            Aset.set("april.pyttsx3", true)
        except:
            self._info("april with out pyttsx3")
            self._info("april checking ...(failed)")    
            return False
        self._info("april checking ...(pass)")
        return True
    

manager = AprilManger()

