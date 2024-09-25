from util import *

class ToolManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "tool"
        self.type = "Tool"
        pass
        
    def check(self):
        self._info("tool checking ...true")
        return True

manager = ToolManger()

