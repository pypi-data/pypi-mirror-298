from util import *

class Item(YModule):
    def __init__(self):
        super().__init__()

    def getModule(self, **kwargs):
        import items

        if 'include' in kwargs:
            include = kwargs['include'].split('.')
        else:
            include = None
        if 'exclude' in kwargs:
            exclude = kwargs['exclude'].split('.')
        else:
            exclude = None

        mlist = []
        for moduleName in items.M_module:
            module = items.M_module[moduleName]
            if not include or list_overlap(include, module.M_tags):
                if not exclude or not list_overlap(exclude , module.M_tags):
                    mlist.append(module)
        
        dst = []
        for module in mlist:
            if 'dst' in kwargs:
                if kwargs['dst'] == 'path':
                    dst.append(module.M_path)

        if 'split' in kwargs:
            print(kwargs['split'].join(dst))
        else:
            print(dst)
