from tool import *


class MpcdManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "mpcd"
        self.type = "Mpcd"
        pass

    def check(self):
        return True
        

manager = MpcdManger()