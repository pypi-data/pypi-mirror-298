from util import *


class ServerManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "server"
        self.type = "Server"
        pass

    def check(self):
        if os.path.exists('/home/kylin-ksvd'):
            self._info("ksvd.server checking ...(pass)")
            return True
        else:
            self._console("ksvd.server checking ...(failed)")
            return False

manager = ServerManger()