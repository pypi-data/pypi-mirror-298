from util import *
import socket
import threading
class Usrv(YModule):
    keys={
        **YMoudle.keys,
        **{
            'data' = {}
        }
    }
    def __init__(self):
        super().__init__()

    def _init(self):
        self.data = {}

    def table(self):
        table = []
        table.append(["pid","vid","desc","note"])
        for item in self.data:
            node = self.data[item]
            device = node['device']
            table.append([hex(device['idVendor']).zfill(4), hex(device['idProduct']).zfill(4),
            node['desc'],""])

        
        self._console(tabulate(table, headers='firstrow', tablefmt='orgtbl'))

    def summay(self):
        super().summay()

        if len(self.data) == 0:
            self._console("no data")
            return

    def handle_client(self, *args, **kwargs):
        client = args[0]
        request = client.recv(4096)
        cmd = json.loads(request.decode())
        if cmd['cmd'] == "add":
            if cmd['name'] in self.data:
                resp = json.dumps({
                    'ret':'failed',
                    'data':'dump:'+json.dumps(self.data[cmd['name']])
                })
                client.sendall(resp.encode())
                return 

            resp = json.dumps({
                'ret':'success',
                'data':""
            })
            client.sendall(resp.encode())
            request = client.recv(4096)
            node = json.loads(request.decode())
            self.data[node['name']] = node
            self.table()

        else:
            print(cmd.cmd)
        client.close()

    def run(self):
        bind_ip = "127.0.0.1"
        bind_port = 9999
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((bind_ip, bind_port))
        server.listen(5)
        self._console("listening...")
        while True:
            client, addr = server.accept()
            print("accepted %s:%d" % (addr[0],addr[1]))
            client_handler = threading.Thread(target = self.handle_client, args=(client,))
            client_handler.start()