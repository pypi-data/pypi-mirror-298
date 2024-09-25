from tool import *


class UniqbprodManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "uniqbprod"
        self.type = "Uniqbprod"
        pass

    def check(self):
        return True  

manager = UniqbprodManger()