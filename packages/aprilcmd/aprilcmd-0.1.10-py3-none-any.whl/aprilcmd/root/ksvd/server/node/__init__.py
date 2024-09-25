from tool import *


class NodeManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "node"
        self.type = "Nodes"
        pass

    def check(self):
        return False

manager = NodeManger()