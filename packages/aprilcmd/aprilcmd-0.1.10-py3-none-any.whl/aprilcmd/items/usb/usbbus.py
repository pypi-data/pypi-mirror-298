from util import *

class UsbList(YModuleItem, YModuleList):
    @ym_getItem
    def _getItem(self, *args, **kwargs):
        type = args[0]
        return eval(type+'()')

    def str():
        return "Usb"

    def _type(self):
        return Usb

    def _listHead():
        return ["name","vid","pid","desc","note"]
    
    def _listItem(self):
        return [self.name, 0,0,"alist",""]

class Bus(UsbList):
    keys = {
        **UsbList.keys,
        **{
            'busnum':None
        }
    }
    def __init__(self):
        super().__init__()

    def getcmd(self, cmd):
        if cmd == "pcap":
            return "cat /sys/kernel/debug/usb/usbmon/"+self.busnum+"u"
        elif cmd == "plugin":
            ret = "cat /sys/kernel/debug/usb/usbmon/"+self.busnum+"u"
            for usb in self.items:
                ret = ret+' |grep -v ":'+usb.devnum+':"'
            return ret

    def parse(self):
        for i in self.child:
            eval("self."+i+".parse()")
    
    def up(self):
        for i in self.child:
            eval("self."+i+".up()")

    def pcap(self, arg = 'pcap'):
        import subprocess
        fo = open(tmpPath+'/tmp.pcap', "w+")
        cmd = self.getcmd(arg)
        if fo:
            fo.write(cmd)
        print(cmd)
        process=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            if fo:
                fo.write(line.decode('utf-8'))
                fo.flush()
            print("%s"%line.decode('utf-8').rstrip(), flush = True)
        if fo:
            fo.close()
        print("end")

    def scan(self):
        import usb
        import usb.core
        busses = usb.busses()
        for bus in busses:
            if str(bus.location) == self.busnum:
                break

        for dev in bus.devices:
            arg = {}
            print(dev)
            arg['name'] = 'u'+pvid2str(dev.idVendor)+pvid2str(dev.idProduct)
            arg['type'] = 'Usb'
            arg['configs'] = []
            adev = vars(dev)
            for config in adev['configurations']:
                arg['configs'].append(revars(config,8))
            del adev['configurations']
            del adev['dev']
            arg['device'] = adev
                
            item = self._new(**arg)

        Aset.write()     
        pass
    
    @ym_getItem
    def _getItem(self, *args, **kwargs):
        type = args[0]
        return eval(type+'()')

