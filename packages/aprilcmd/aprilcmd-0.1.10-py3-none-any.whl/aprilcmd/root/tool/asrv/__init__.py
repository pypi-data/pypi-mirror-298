from util import *

class AsrvManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "asrv"
        self.type = "Asrv"
        pass
        
    def check(self):     
        self._info("asrv checking ...(pass)")
        return True

manager = AsrvManger()

