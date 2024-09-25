

import sys
import os.path

from util import *
sys.path.append(getDir(__file__))
from host import *
sys.path.pop()

def tag_match(a, b):
    ret = []
    for i in a:
        if i in b:
            ret.append(i)
    return ret

class HostList(YModuleItem, YModuleList):
    def __init__(self):
        super().__init__()
        self.type = "HostList"

    def _getipa(self, ipa):
        childname = self.name
        if not ipa:
            ipa = []
        if childname[0] == 'n' and childname[1:].isdecimal():
            ipa = [childname[1:]] + ipa
            return self.parent._getipa(ipa)
        else:
            return ipa

    def _getips(self):
        dest = ["0","0","0","0"]
        ipa = self._getipa(None)
        mask = len(ipa)*8
        ipa.extend(dest[len(ipa):4])
        ips = '.'.join(ipa)
        return ips+"/"+str(mask)

    def gettip(self,ipa = ["10","0","0","1"]):
        thisipa = self._getipa(None)
        if not thisipa == ipa[0:len(thisipa)]:
            print("error gettip diff :"+str(thisipa)+" vs "+str(ipa[0:len(thisipa)]))
        return ipa[len(thisipa):4]


    def summay(self):
        super().summay()

    def _new(self, *args, **kwargs):
        newType = self._getType(*args, **kwargs)
        if newType not in ['Host', 'HostList']:
            print("type e")
            return super()._new(*args, **kwargs)
        if 'name' not in kwargs:
            print("no name e")
            return super()._new(*args, **kwargs)
        name = kwargs['name']
        obj = re.match(r'[\.\d]',name)
        if not obj:
            print("no obj")
            return super()._new(*args, **kwargs)
        ipa = name.split('.')
        if len(ipa) == 1:
            kwargs['name'] = 'n'+ipa[0]
            return super()._new(*args, **kwargs)

        print(ipa)
        print(ipa[0:len(ipa)-1])
        print(ipa[len(ipa)-1])
        item = self

        for n in ipa[0:len(ipa) - 1]:
            t = item['n'+n]
            if not t:
                t = item._new('HostList', name='n'+n) 
            item = t
            print(item)
        kwargs['name'] = 'n'+ipa[len(ipa)-1]
        item._new(newType, **kwargs)

    def str():
        return "Host"

    def _type(self):
        return Host

    def _listHead():
        return ['name', 'type', 'types', 'ip', 'id']

    def _listItem(self):
        ip = self._getips()
        return [self.name, "list", "", ip, ""]

    def input(self):
        print("input name:")
        self.name = input()
        pass

    def scan(self):
        pass

    def rrun(self, *args, **kwargs):
        (aif, cmd) = get_args(\
            ['aif', 'cmd'],\
            (None, None), **kwargs)
        
        if 'aif' in kwargs:
            del kwargs['aif']
        if 'cmd' in kwargs:
            del kwargs['cmd']

        for host in self.items:
            if aif and not eval(aif):
                continue
            func = host[cmd]
            func(*args, **kwargs)
    
    def tags(self, *args, **kwargs):
        tags = args

        mlist = []
        for host in self.items:
            if not host.desc or not host.desc['types']:
                continue
            m = tag_match(tags, host.desc['types'])
            if len(m) > 0:
                mlist.append(host)

        self.printTable(mlist)

    @ym_getItem
    def _getItem(self, *args, **kwargs):
        type = args[0]
        return eval(type+'()')


def setclasses(classes):
    classes['HostList'] = HostList