from util import *

class ModuleManger(YManager):
    tags = ["_base"]+YManager.tags
    def __init__(self):
        super().__init__()
        self.name = "module"
        self.type = "Module"
        pass

    def isEnable(self):
        return True
        
manager = ModuleManger()

