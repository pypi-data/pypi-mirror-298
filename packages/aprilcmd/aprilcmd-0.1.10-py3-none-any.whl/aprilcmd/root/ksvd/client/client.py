from util import *

class Client(YModule):
    def __init__(self):
        super().__init__()
        pass

    def heart(self):
        import socket
        bind_ip = "10.30.8.36"
        bind_port = 10001
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((bind_ip, bind_port))
        print(f"Connected to {bind_ip}:{bind_port}")
        # 发送数据
        data = json.dumps({
            'cmd':'heart',
            'name':""
        })
        
        s.sendall(data.encode())
        s.close()

