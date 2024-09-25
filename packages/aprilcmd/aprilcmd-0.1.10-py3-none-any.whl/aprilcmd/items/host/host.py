#codeing = utf-8
from util import *

import sys
import os.path

class Host(YModuleItem, YModuleList):
    keys = {**{
        'desc':[],
        'ip':"127.0.0.1"
    },**YModuleItem.keys}

    def _fromJson(self,*args, **kwargs):
        super()._fromJson(*args, **kwargs)
        if self.desc == {}:
            self.desc = []
    
    def __init__(self):
        super().__init__()

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
        #if hasattr(self,"ip"):
        #    return self.ip
        ipa = self._getipa(None)
        ips = '.'.join(ipa)
        return ips

    def str():
        return "Host"
        
    def _type(self):
        return Host

    def _listHead():
        return ['name', 'type', 'types', 'ip', 'desc']

    def _getTypes(self):
        types = []
        for type in self._getChildNames():
            types.append(type)
        return types

    def _listItem(self):
        self._initChildOnce()
        types = []
        for itype in self._getChildNames():
            c = self[itype]
            types.append(itype)
            if c.getdesc and c.getdesc() not in self.desc:
                self.desc.append(c.getdesc())
                
        if hasattr(self,'ip'):
            ip = self.ip
        else:
            ip = self._getips()
        table = [self.name, type(self).__name__, str(types), ip, str(self.desc)]
        return table

    def input(self):
        print("input name:")
        self.name = input()
        print("input username")
        self.username = input()
        print("input password")
        self.password = input()


    def scan(self):
        pass
    
    def addDesc(self, *args, **kwargs):
        for i in kwargs:
            if i not in self.desc:
                self.desc[i] = []
            lt = type(self.desc[i])
            rt = type(kwargs[i])
            if lt == list:
                if rt == list:
                    self.desc[i].extend(kwargs[i])
                else:
                    self.desc[i].append(kwargs[i])
            else:
                self.desc[i] = kwargs[i]

        self._update()

    def summay(self):
        table = []
        table.append(Host._listHead())
        table.append(self._listItem())

        print(tabulate(table, headers='firstrow', tablefmt='orgtbl'))

        super().summay()

    def rinstall(self, arg='help'):
        # 清空功能配置
        #self._getroot().package.module.f_clean()
        try:
            # 远程安装
            self._getroot().package._rinstall(self, lvl=2)
        except:
            self._console("rinstall faild")
            traceback.print_exc()

        # 恢复配置
        #self._getroot().package.module.check()


def setclasses(classes):
    classes['Host'] = Host