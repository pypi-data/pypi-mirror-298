from util import *

class ItemManger(YManager):
    tags = ["_base"]+YManager.tags
    def __init__(self):
        super().__init__()
        self.name = "item"
        self.type = "Item"
        pass

    def isEnable(self):
        return True
        
manager = ItemManger()

