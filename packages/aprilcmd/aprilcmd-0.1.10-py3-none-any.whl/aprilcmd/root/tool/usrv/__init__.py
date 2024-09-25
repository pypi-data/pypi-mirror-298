from util import *

class UsrvManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "usrv"
        self.type = "Usrv"
        pass
        
    def check(self):     
        self._info("usrv checking ...(pass)")
        return True

manager = UsrvManger()

