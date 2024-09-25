from util import *

class Usbs(YModuleList):
    def __init__(self):
        super().__init__()
        pass

    def scan(self):
        pass

    def scan(self, *args, **kwargs):
        a_dp = False
        if 'a_dp' in kwargs:
            a_dp = kwargs['a_dp']

        import usb
        import usb.core
        busses = usb.busses()
        for bus in busses:
            arg = {}
            arg['busnum'] = str(bus.location)
            arg['name'] = 'bus'+str(bus.location)
            arg['type'] = 'Bus'
            item = self._new(**arg)
            if a_dp:
                item.scan()
                item.parse()
        Aset.write()     

    def up(self):
        for i in self.child:
            eval("self."+i+".up()")

    @ym_getItem
    def _getItem(self, *args, **kwargs):
        type = args[0]
        return eval(type+'()')

