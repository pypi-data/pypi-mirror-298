from util import *

class QemuManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "qemu"
        self.type = "Qemu"
        pass

    def isEnable(self):
        return False

    def check(self):
        return False

manager = QemuManger()

