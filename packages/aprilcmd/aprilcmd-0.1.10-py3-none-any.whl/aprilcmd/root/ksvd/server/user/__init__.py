from util import *


class UserManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "user"
        self.type = "User"
        pass

    def check(self):
        return True 

manager = UserManger()