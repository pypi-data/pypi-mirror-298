from tool import *


class GlusterManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "gluster"
        self.type = "Gluster"
        pass

    def check(self):
        return False

manager = GlusterManger()