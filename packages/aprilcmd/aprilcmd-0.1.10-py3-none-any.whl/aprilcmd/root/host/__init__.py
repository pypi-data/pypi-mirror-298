from util import *
mod_trace(__file__)

class HostManger(YManager):
    tags = ["hacker"]+YManager.tags
    def __init__(self):
        super().__init__()
        self.name = "host"
        self.type = "Hosts"
        pass

    def check(self):
        try:
            self._info("hosts checking ...(pass)")
            return True
        except:
            self._console("hosts checking ...(failed) try pip install scapy")
            return False
       
    

manager = HostManger()
