from util import *
import socket
import threading
class Asrv(YModule):
    def __init__(self):
        super().__init__()

    def handle_client(self, *args, **kwargs):
        client = args[0]
        (ip, port) = args[1]
        request = client.recv(4096)
        cmd = json.loads(request.decode())
        if cmd['cmd'] == "add":
            print(cmd['data'])
            print(ip)
            name = self._getroot().host._getName(ip=ip)
            try:
                host = self._getroot().host.scan._getChild(name)
                try:
                    host.summay()
                    host.addDesc(**cmd['data'])
                    from datetime import datetime
                    time = datetime.now().strftime("%Y-%m-%d %H")
                    print(time)
                    host.addDesc(time=time)
                except:
                    traceback.print_exc()
            except:
                print('name not in host')
                pass
        else:
            print(cmd)
        client.close()

    def run(self):
        bind_ip = "0.0.0.0"
        bind_port = 10001
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((bind_ip, bind_port))
        server.listen(5)
        self._console("listening...")
        while True:
            client, addr = server.accept()
            print("accepted %s:%d" % (addr[0],addr[1]))
            client_handler = threading.Thread(target = self.handle_client, args=(client,addr,))
            client_handler.start()