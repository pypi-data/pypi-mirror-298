import sys

from util import *
sys.path.append(getDir(__file__))
from base import *
sys.path.pop()

class Client(Function):
    def __init__(self):
        super().__init__()
        self.keys.extend([
            'username',
            'password',
            'auths'
        ])
        self.name = "client"
        self.type = "Client"
        
    
    def up(self, *args, **kwargs):
        import socket
        bind_ip = self._getroot().host._parent.ip
        bind_port = 10001
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((bind_ip, bind_port))
        print(f"Connected to {bind_ip}:{bind_port}")
        # 发送数据
        data = json.dumps({
            'cmd':'add',
            'data':{
                'ip':self.parent.ip,
                'types':self.parent._getTypes(),
                'ver':self._getroot().ver
            }
        })
        
        s.sendall(data.encode())
        s.close()
        pass
    pass

class Server(Function, YModuleList):
    def __init__(self):
        super().__init__()
        self.name = "server"
        self.type = "Server"
        
    def scan(self):
        pass
    

    