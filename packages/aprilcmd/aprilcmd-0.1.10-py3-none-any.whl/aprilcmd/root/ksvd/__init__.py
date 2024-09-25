from util import *

class KsvdManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "ksvd"
        self.type = "Ksvd"
        pass
        
    def check(self):
        self._info("ksvd checking ...(pass)")
        return False

manager = KsvdManger()

