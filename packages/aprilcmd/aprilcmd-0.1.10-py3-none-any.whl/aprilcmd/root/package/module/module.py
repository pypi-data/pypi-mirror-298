from util import *

class Module(YModule):
    def __init__(self):
        super().__init__()

    def clean(self):
        from util import Aset
        Aset.clean()
        Aset.write()

    def check(self):
        from root import manager
        from util import Aset
        self._info("checking...")
        Aset.read()
        manager.doCheck()
        Aset.write()
    
    def list(self):
        from util import Aset
        self._console(json.dumps(Aset.data,indent = 2))

    def getModule(self, **kwargs):
        from root import manager
        mlist=manager.getModule(**kwargs)

        if 'split' in kwargs:
            print(kwargs['split'].join(mlist))
        else:
            print(mlist)
