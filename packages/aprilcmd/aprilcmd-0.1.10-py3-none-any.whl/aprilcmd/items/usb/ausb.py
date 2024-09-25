
from util import *
import socket

class Uparser:
    def __init__(self):
        self.child = None
        self.len = 0

    def readData(self, data):
        self.len = len(data)
        i = 0
        self.child = Descriptor()
        self.child.parent = self
        tmp = self.child
        tmp.setData(data)
        tmp = tmp.gogogo()
        i+=tmp.len
        while(i < self.len):
            tmp.next = Descriptor()
            tmp.next.prev = tmp
            tmp = tmp.next
            tmp.setData(data[i:])
            tmp = tmp.gogogo()            
            i+= tmp.len
            if (tmp.len <= 0):
                break
            
    def hvars(self):
        import json
        ret = {}
        if self.child:
            ret['child'] = []
            ret['child'].append(self.child.hvars())
            thenext = self.child.next
            while thenext:
                ret['child'].append(thenext.hvars())
                thenext = thenext.next
        return ret
    def dump(self):
        ret = self.hvars()
        print(json.dumps(ret,indent =2))


class Descriptor:
    def __init__(self):
        self.type = 'Descriptor'
        self.bLength = 0
        self.bDescriptorType = 0
        self.len = 0
        self.parent = None
        self.next = None
        self.child = None
        self.prev = None
        self.data =None

    def setData(self, data):
        self.bLength = data[0]  
        self.bDescriptorType = data[1]
        self.len = self.bLength
        self.data = data

    def match(node):
        return False

    def addchild(self, child):
        if not self.child:
            self.child = child
            child.parent = self
        else:
            tmp = self.child
            while tmp.next:
                tmp = tmp.next
            tmp.next = child
            child.prev = tmp

    
    def detach(self):
        self.parent = None
        self.next = None
        self.child = None
        self.prev = None

    def gogogo(self):
        table = {
            0x02:Config,
            0x04:Interface,
            0x0b:InterfaceAss
        }
        thenew = None
        if self.bDescriptorType in table and \
            not type(self) == table[self.bDescriptorType]:
            thenew = table[self.bDescriptorType]()
            thenew.setData(self.data)
        if thenew:
            if self.parent:
                self.parent.child = thenew
                thenew.parent = self.parent
            if self.prev:
                self.prev.next = thenew
                thenew.prev = self.prev
            return thenew.gogogo()
        return self

    def vars(self):
        tmp = vars(self)
        ret = {}
        for i in tmp:
            if i in ['parent','prev','child','next','data']:
                continue
            ret[i] = tmp[i]
        return ret
    
    def hvars(self):
        ret = self.vars()
        if self.child:
            ret['child'] = []
            ret['child'].append(self.child.hvars())
            thenext = self.child.next
            while thenext:
                ret['child'].append(thenext.hvars())
                thenext = thenext.next
        return ret
            
    def dump(self):
        print("dump")
        print(self.hvars())
    pass

class Config(Descriptor):
    def __init__(self):
        super().__init__()
        self.type = 'Config'

    def setData(self, data):
        super().setData(data)
        self.wTotalLength = data[2]+data[3]*256
        self.bNumInterfaces = data[4]
        self.bConfigurationValue = data[5]
        self.iConfiguration = data[6]
        self.bmAttributes = data[7]
        self.bMaxPower = data[8]
        while not self.len == self.wTotalLength:
            tmp = Descriptor()
            tmp.setData(data[self.len:])
            tmp = tmp.gogogo()
            self.len += tmp.len
            self.addchild(tmp)

    def match(node):
        return True
    pass

class InterfaceAss(Descriptor):
    def setData(self, data):
        self.type = 'InterfaceAss'
        super().setData(data)
        self.bFirstInterface = data[2]
        self.bInterfaceCount = data[3]
        self.bFunctionClass = data[4]
        self.bFunctionSubClass = data[5]
        self.bFunctionProtocol = data[6]
        self.iFunction = data[7]
        i = 0
        while i < self.bInterfaceCount:
            tmp = Descriptor()
            tmp.setData(data[self.len:])
            tmp = tmp.gogogo()
            self.len += tmp.len
            self.addchild(tmp)
            i += 1

    def gogogo(self):
        #super().gogogo()
        if not self.prev:
            return self
        if type(self.prev) == Config:
            prev = self.prev
            self.detach()
            prev.addchild(self)
            return self.gogogo()
        return self

    def match(node):
        return True
    pass

class Interface(Descriptor):
    def setData(self, data):
        super().setData(data)
        self.type = 'Interface'
        self.bInterfaceNumber = data[2]
        self.bAlternateSetting = data[3]
        self.bNumEndpoints = data[4]
        self.bInterfaceClass = data[5]
        self.bInterfaceSubClass = data[6]
        self.bInterfaceProtocol = data[7]
        self.iInterface = data[8]
        i = 0
        while i < self.bNumEndpoints:
            tmp = Descriptor()
            tmp.setData(data[self.len:])
            tmp = tmp.gogogo()
            self.len += tmp.len
            self.addchild(tmp)
            i += 1

    def gogogo(self):
        if not self.prev:
            return self
        if type(self.prev) == Config or type(self.prev) == InterfaceAss:
            prev = self.prev
            self.detach()
            prev.addchild(self)
            return self.gogogo()
        return self

    def match(node):
        return True

class Usb(YModuleItem):
    keys = {
        **YModuleItem.keys,
        **{'device':None}
    }

    def __init__(self):
        super().__init__()
        self.desc = ""

        
    def str():
        return "Usb"

    def _type(self):
        return Usb
        
    def _listHead():
        return ["name","vid","pid","desc","note"]
    
    def _listItem(self):
        return [self.name, pvid2str(self.device['idVendor']), pvid2str(self.device['idProduct']),
            self.desc,""]
    
    def info(self):
        super().info()
        self._console(self.device)
        self._console(self.configs)
        self._console(self.desc)

    def up(self, *args,**kwargs):
        bind_ip = "127.0.0.1"
        bind_port = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((bind_ip, bind_port))
        print(f"Connected to {bind_ip}:{bind_port}")
        # 发送数据
        data = json.dumps({
            'cmd':'add',
            'name':self.name
        })
        
        s.sendall(data.encode())
        data = s.recv(4086)
        resp = json.loads(data.decode())
        if not resp['ret']== "success":
            self._console(resp['ret'])
            self._console(resp['data'])
        data = json.dumps(self._toJson())
        s.sendall(data.encode())
        s.close()


    def getfunc(self, interface, func):
        iclass = str(interface['interfaceClass'])
        class_table = {
            '1':'audio',
            '3':'hid',
            '8':'storage',
            '9':'hub',
            '14':'video'
        }
        if iclass in class_table:
            iclass = class_table[iclass]
        if not iclass in func:
            func.append(iclass)

    def parse(self, *args, **kwargs):
        if self.desc:
            return
        confignum = len(self.configs)
        if confignum > 1:
            self.desc = self.desc+"|confignum:"+str(confignum)
        
        for config in self.configs:
            #print(config)
            asslen = len(config['interfaces'])
            if asslen > 1:
                self.desc = self.desc+"|interfaces_ass num:"+str(asslen)
            func = []
            for ass in config['interfaces']:
                for interface in ass:
                    self.getfunc(interface, func)
            self.desc = self.desc+"|has func:"+json.dumps(func)
        #self._console(self.desc)   
        self._update()

    def pcap(self):
        import subprocess
        cmd = self.parent.getcmd('pcap')+" |grep \":"+self.devnum+":\""

        process=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for line in iter(process.stdout.readline,b''):
            print(line)
        for line in iter(process.stdout.readline,b''):
            print(line)
