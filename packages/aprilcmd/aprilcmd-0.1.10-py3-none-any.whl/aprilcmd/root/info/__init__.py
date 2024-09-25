from util import *
mod_trace(__file__)
class InfoManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "info"
        self.type = "Info"
        pass

    def isHidden(self):
        return True

    def check(self):
        self._info("info checking ...(false)")
        return False

manager = InfoManger()

