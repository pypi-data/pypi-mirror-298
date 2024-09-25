from util import *

class RootManager(YManager):
    def __init__(self):
        super().__init__()
        self.name = 'root'
        self.out = self.log

    def _getFilePath(self, **kwargs):
        if hasattr(self, 'parent') and self.parent:
            return self.parent._getFilePath(**kwargs)+"/"+self.name
        else:
            if 'local' in kwargs and kwargs['local']:
                return "./aprilcmd/"
            return os.path.dirname(__file__)

class Root(YModule):
    def __init__(self):
        super().__init__()
        self.name = "root"
        self.root = self
        self.out = self.log
        self.manager = manager

   
    def _initChild(self, *args, **kwargs):
        mod = Aset.getMod(self._getpath())
        if mod:
            self._fromJson(**mod)
        # 加载初始模块
        try:
            #import root.debug as debug
            #manager._addChild(debug.manager)
            manager.debug.createModule(self)
            #import root.file as file
            manager.file.createModule(self)
        except:
            pass
        #import root.package as package
        #manager._addChild(package.manager)
        manager.package.createModule(self)

        #import root.package.module as module
        #manager.package._addChild(module.manager)
        manager.package.module.createModule(self.package)
        super()._initChild(*args, **kwargs)

    def init(self, *args, **kwargs):
        self._initChildOnce()
        for key in self._getChildNames():
            print(key)
            child = self[key]
            child._research('init', *args, **kwargs, sstop=True)
        self._update()

    def fini(self, *args, **kwargs):
        self._initChildOnce()
        for key in self._getChildNames():
            print(key)
            child = self[key]
            child._research('fini', *args, **kwargs, sstop=True)
    
    def items(self):
        import items 
        tags = []
        if hasattr(self, 'tags'):
            tags = self.tags
        for name in items.classes:
            print(name+":"+str(items.getClass(name, tags)))

manager = RootManager()
manager._initChild()





