from util import *

class PackageManger(YManager):
    tags = ["_base"]+YManager.tags
    def __init__(self):
        super().__init__()
        self.name = "package"
        self.type = "Package"
        pass

    def isEnable(self):
        return True

manager = PackageManger()

