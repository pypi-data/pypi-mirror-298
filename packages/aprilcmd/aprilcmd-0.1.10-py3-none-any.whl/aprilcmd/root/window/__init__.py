from util import *
mod_trace(__file__)

class WindowManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "window"
        self.type = "Window"
        pass

    def check(self):
        try:
            #return False
            if os.uname().nodename != "ygh":
                return False
            from PyQt5.QtWidgets import QApplication
            self._info("window checking ...(pass)")
            return True
        except:
            self._console("window checking ...(failed),try pip install PyQt5")
            return False
    

manager = WindowManger()
