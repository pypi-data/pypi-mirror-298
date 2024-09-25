from util import *


class ClientManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "client"
        self.type = "Client"
        pass

    def check(self):
        if os.path.exists('/usr/bin/uniface'):
            self._info("ksvd.client checking ...(success)")
            return True
        else:
            self._console("ksvd.client checking ...(failed)")
            return False

manager = ClientManger()