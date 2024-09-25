from util.conf import *
from util.ysys import *

class Setting(JsonConfigFile):
    def __init__(self):
        JsonConfigFile.__init__(self, tmpPath+"/setting.json")
        self.read()
        pass

    def clean(self):
        self.data = {}

    def setMod(self, *args, **kwargs):
        path = args[0]
        self.set(path+"._local",kwargs,sync=False, flush=False)

    def getTree(self, path):
        thisset = self.get(path)
        '''
        for i in thisset:
            if i == "_local":
                continue
            dest = []
            for j in thisset[i]:
                if j == "_local":
                    continue
                dest.append(j)
            for j in dest:
                del thisset[i][j]
        '''
        return thisset
    def addMod(self, *args, **kwargs):
        """
        add a mod to setting
        args: path, name
        kwargs: data
        """
        path = args[0]
        name = args[1]

        kwargs.update({"name":name})
        self.add(path, {
            "_local":kwargs
        }, sync=False, flush=False)


    def _tag(self, set, tags):
        return set


    def getMod(self, path, **kwargs):
        """
        get a mod from setting
        args: path
        kwargs: mod tag
            mod: local: just self conf
            tag:
        """

        thisset = self.get(path)
        if not thisset:
            return None
        ##change
        if '_items' in thisset:
            for i in thisset['_items']:
                thisset[i] = thisset['_items'][i]
            del thisset['_items']
            self.set(path, thisset,sync=False, flush=False)
        ## 
        if 'all' in kwargs and kwargs['all'] == True:
            return thisset
        return thisset['_local']

    def getChild(self, path, **kwargs):
        thisset = self.get(path)
        if not thisset:
            return []
        childs = []
        for i in thisset:
            if i == '_local':
                continue
            childs.append(i)
        return childs
    def delMod(self, path):
        try:
            self.delete(path, sync=False, flush=False)
        except:
            pass
    
    def write(self):
        super().write()

Aset = Setting()
logging.info("INIT setting")