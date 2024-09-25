from util import *

class TestManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "test"
        self.type = "Test"
        pass
        
    def isHidden(self):
        return True

    def check(self):
        self._info("test checking ...true")
        return False

manager = TestManger()

