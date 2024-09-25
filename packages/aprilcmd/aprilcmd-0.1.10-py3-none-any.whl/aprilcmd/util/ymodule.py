
from util.ysys import *
from util.conf import *
from util.ycommon import *
from util.setting import *
import traceback

mod_trace(__file__)

try:
    from tabulate import tabulate
except:
    from third.tabulate import tabulate

class YTree(ABC):
    def __init__(self):
        self.name = None
        self.__april_child = {}
        self.parent = None

    def _getChildNames(self):
        names = []
        for name in self.__april_child:
            names.append(name)
        return names

    def _getpath(self):
        '''get mod's path for example root.pacakge.module'''
        if hasattr(self, 'parent') and self.parent:
            return self.parent._getpath()+'.'+self.name
        else:
            return self.name
        pass

    def _getroot(self):
        '''get mod's root always return root'''
        if self.parent:
            return self.parent._getroot()
        else:
            return self

    def _getkey(self, key):
        #print(str(self)+".__getkey:"+str(key))
        if key.isdecimal():
            key = "n"+key
        
        if key == 'root':
            return self._getroot()
        #item
        return getattr(self, key)
        

    def _reGetItem(self, keylist):
        if len(keylist) == 1:
            return self._getkey(keylist[0])

        obj = self._getkey(keylist[0])
        return obj._reGetItem(keylist[1:])

    def __getitem__(self, key):
        if key == '.':
            return self
        #str2list
        keylist = key.split('.')
        return self._reGetItem(keylist)
    
    def __getattr__(self, name):  
        #print(self._getpath()+"->y__getattr__:"+name)
        # 首先检查字典d中是否有该名称的键 
        #print("try get:"+name)
        if name == 'root':
            #print("try get root")
            return self._getroot()

        if name in self.__april_child:  
            return self.__april_child[name]  

        return None


    def __setitem__(self, key, value):
        if not type(key) == str:
            print(self.name+" set item error")
            return
        elif len(key) < 1:
            print(self.name+"set item error key:"+key+" key len 0")
            return
        elif key not in self.keys:
            print(self.name+"set item error key:"+key+"not in child")
            return
        setattr(self, key, value)

    def _addChild(self, child):
        self.__april_child[child.name]=child
        child.parent = self
        #print(str(self)+":"+self._getpath()+"->addChild:"+str(child)+" c.p:"+str(child.parent))

class LogC:
    log = Ylog() #defalut log

    def __init__(self):
        self.loglvl = 3

    def _error(self, log):
        self.log._error(log, lvl=self.loglvl, module=self.name)
    
    def _warn(self, log):
        self.log._warn(log,  lvl=self.loglvl, module=self.name)

    def _info(self, log):
        self.log._info(log,  lvl=self.loglvl, module=self.name)
    
    def _debug(self, log):
        self.log._debug(log,  lvl=self.loglvl, module=self.name)
        
class OutC:
    def _console(self, log):
        if self._getroot().out:
            self._getroot().out._console(log)

class YModule(Yobj,YTree, LogC, OutC):
    '''
    base Moduld
    '''
    keys = {
        'name':"it's a bug with no name",
        'hidden':False,
        'ver':1,
        'tags':[],
    }

    def __init__(self):
        Yobj.__init__(self)
        YTree.__init__(self)
        LogC.__init__(self)
        self._init = False

        self.funcs_info = {
            "summay":"",
            "f_info":"",
            "f_aset":"",
            "aset_export":"",
            "aset_import":""
        }

        self.root = None

    def _rmtag(self, key, **kwargs):
        print(self._getpath()+"->b-"+key+"-->"+str(self.tags))
        if key in self.tags:
            self.tags.remove(key)
        print(self._getpath()+"->a-"+key+"-->"+str(self.tags))

        if not 're' in kwargs:
            return
        self._initChildOnce()
        for name in self._getChildNames():
            self[name]._rmtag(key, **kwargs)

    def rmtag(self, key, **kwargs):
        self._rmtag(key, **kwargs)
        self.update('tree')

    def _addtag(self, key, **kwargs):
        print(self._getpath()+"->b-"+key+"-->"+str(self.tags))
        if key not in self.tags:
            self.tags.append(key)
        print(self._getpath()+"->a-"+key+"-->"+str(self.tags))

        if not 're' in kwargs:
            return
        self._initChildOnce()
        for name in self._getChildNames():
            self[name]._addtag(key, **kwargs)
        
    
    def addtag(self, key, **kwargs):
        self._addtag(key, **kwargs)
        self.update('tree')

       

    def __getattr__(self, key):
        #print("ymodle getattr:"+key)
        try:
            return object.__getattribute__(self, key)
        except:
            self._initChildOnce()
            return super().__getattr__(key)

    def __updateItem(self, key, value):
        try:
            self[key] = json.loads(value)
        except:
            self[key] = value

    def updateItem(self, *args, **kwargs):
        if len(args) > 2:
            self.__updateItem(args[0], args[1:])
        elif len(args) > 1:
            self.__updateItem(args[0], args[1])
        else:
            self.__updateItem(args[0], kwargs)
        self.update()

    def _arg_replace(self, match):
        return eval(match.group(1))

    def test(self, *arg, **kwargs):
        '''
        test func
            self.func *arg[1:] **kwargs
        '''
        func=self[arg[0]]
        print(func)
        print(func(*arg[1:], **kwargs))

    def _toJson(self, *arg, **kwargs):
        '''
        get a json from a module
        with out child and item, just self key
        '''
        arg = {}
        this = vars(self)
        for key in self.keys:
            if not key in this:
                continue

            keyval = this[key]
            if keyval == self.keys[key]: # defalut value
                continue

            arg[key] = keyval
        
        arg['type'] = type(self).__name__
        return arg
    
    def _fromJson(self, *arg, **kwargs):
        '''
        get a module from a json
        with out child and item, just self key
        '''
        for key in self.keys:
            if type(self.keys[key]) == dict or type(self.keys[key]) == list:
                self[key] = self.keys[key].copy()
            else:
                self[key] = self.keys[key]
        for key,value in kwargs.items():
            if key not in self.keys:
                self._warn(key + " not in keys of "+str(self.keys))
                continue
            self[key] = value
        

    def _update(self, *args, **kwargs):
        '''
        update module only with _local
        '''
        print(self._getpath()+" update-->"+str(self._toJson()))
        Aset.setMod(self._getpath(), **self._toJson(**kwargs))

        if not 'tree' in args:
            return
        self._initChildOnce()
        for i in self._getChildNames():
            if self[i]['_update']:
                self[i]._update(*args, **kwargs)
   
    def update(self, *args, **kwargs):
        self._update(*args, **kwargs)
        Aset.write()

    def _addChild(self, child):
        super()._addChild(child)
        child.parent = self
    
    def _research(self, *arg, **kwargs):
        fun = arg[0]
        narg = arg[1:]
        func = self[fun]
        if func:
            func(*narg, **kwargs)
            if 'sstop' in kwargs:
                return
        self._initChildOnce()
        for key in self._getChildNames():
            child = self[key]
            child._research(*arg, **kwargs)

    def _initChildOnce(self, *args, **kwargs):
        # only run once
        if self._init:
            return
        self._init = True
        self._initChild(*args, **kwargs)
    def _initChild(self, *args, **kwargs):
        ignore = []
        if 'ignore' in kwargs:
            ignore.append(kwargs['ignore'])
        
        _path = self._getpath()
        childs = Aset.getChild(_path)
    
        for key in childs:
            file = key
            if key in ignore:
                self._console("ignore "+key)
                continue
            mod=Aset.getMod(_path+"."+key)
            if not 'tags' in mod or not '_static' in mod['tags']:
                continue
            try:
                tmp = __import__(_path + '.'+file, fromlist=[file])
                # 没有manager的模块忽视
                if not hasattr(tmp,'manager'):
                    continue
                # 已经加载模块忽视
                if tmp.manager.name in self._getChildNames():
                    continue
                #self._addChild(tmp.manager)
                tmp.manager.createModule(self, *args, **kwargs)   
            except:
                tb = traceback.format_exc()
                self._warn("unexpect module "+_path +'.'+file+'\n'+tb)

    def _lvl(self, itemName):
        if re.match(r'\_\_.*',itemName):
            return 0
        elif re.match(r'\_.*',itemName):
            return 5
        else:
            return 9

    #@abstractmethod
    def summay(self, *args, **kwargs):
        self._initChildOnce()
        list = []
        for childname in self._getChildNames():
            child = self[childname]
            try:
                if hasattr(child, 'tags') and '_hidden' in child.tags:
                    continue
                list.append(childname)
            except:
                self._console(childname+" failed")
        self._console(list)
        
    
    def _next(self):
        self._initChildOnce()
        list = []
        for childname in self._getChildNames():
            child = self[childname]
            if hasattr(child,'tags') and '_hidden' in child.tags:
                continue

            if childname[0] == 'n' and childname[1:].isdecimal():
                childname = childname[1:]
            list.append(childname)
            if not hasattr(child, '_next'):
                continue
            if len(child._next()):
                list.append(childname+'.')
        return list
    
    def next(self):
        #list2str
        self._console(' '.join(self._next()))

    def _getFuncs(self):
        funcs = []
        for nodename in dir(self):
            node = self[nodename]
            if self._lvl(nodename) <= 5:
                continue
            if not callable(node):
                continue
            funcs.append(nodename)
        return funcs
				
        
    def info(self):
        self.summay()
        for nodename in dir(self):
            node = self[nodename]
            if self._lvl(nodename) <= 5:
                continue
            if not callable(node):
                continue
            if nodename in self.funcs_info:
                self._console(nodename+"    :"+self.funcs_info[nodename])
            else:
                self._console(nodename+"    : with nothing by author")
        pass
    
    def aset(self, *args, **kwargs):
        '''
        get module tree
        data from mem
        '''
        ret = self._aset_dp(*args, **kwargs)
        self._console(json.dumps(ret, indent = 2))

    def _ex_dp(self, *args, **kwargs):
        #print(self._getpath()+":=>_ex_dp:"+str(self.ex))
        # parse tag
        if 'tag' in kwargs:
            tag =  kwargs['tag']
        else:
            tag = None

        # get child
        aout = {}
        ain = args[0]
        for i in ain:
            if i == '_local':
                continue
            iout = self._ex_dp(ain[i], **kwargs)
            if idata:
                aout[i] = iout

        if not tag or not aout == {}:
            aout['_local'] = ain['_local']
            return True
        if 'tags' in ain['_local'] and tag in  ain['_local']['tags']:
            aout['_local'] = ain['_local']
            return True
        return False

    def _aset_dp(self, *args, **kwargs):
        self._initChildOnce()
        #print(self._getpath()+":=>_aset_dp:"+str(self._toJson()))
        ret = {}
        # parse tag
        if 'tag' in kwargs:
            tag =  kwargs['tag']
        else:
            tag = None

        #get child
        for name in self._getChildNames():
            c = self[name]._aset_dp(*args, **kwargs)
            if c:
                ret[name] = c
        #get ex
        if 'ex' in kwargs and self.ex:
            for i in self.ex:
                exdata = self._ex_dp(self.ex[i], tag=tag)
                if exdata:
                    ret[i] = exdata
        
        #get _local
        if not tag:
            ret['_local'] = self._toJson()
            return ret
        if self.tags and tag in self.tags:
            ret['_local'] = self._toJson()
            return ret
        elif not ret == {}:
            ret['_local'] = self._toJson()
            return ret
        else:
            return None

    def aset_export(self, *args, **kwargs):
        '''
        to export a module, data from mem
        args: path
        kwargs: path code
            path: the file path to import defalt is ./aset_tmp
            code: the file's code type if codeced defalt is None
            mod: 'set','adds' defalt is set
            tag: list or str .which tag need to export
        '''
        if len(args) >= 1:
            path = args[0]
        else:
            path = None

        (name, code, tag) = get_args(\
            ["name","code", "tag"],\
            (self.name, None, "*"),\
            **kwargs)
        
        
        #mod = Aset.getTree(self._getpath())
        print(self._getpath()+":=>aset_export:"+str(kwargs))
        mod = self._aset_dp(self, *args, **kwargs)
        if not mod:
            return
        tmp = JsonConfigFile(path, code=code)    
        tmp.data = mod
        tmp.write()
    
    def aset_import(self, *args, **kwargs):
        '''
        to import a module
        args: path
        kwargs: path code mod
            path: the file path to import defalt is ./aset_tmp
            code: the file's code type if codeced defalt is None
            mod: 'set','adds' defalt is set
        '''
        path = "./aset_tmp"
        if len(args) >= 1:
            path = args[0]

        (path, code, mod) = get_args(\
            ["path","code", "mod"],\
            (path, None, "set"),\
            **kwargs)

        tmp = JsonConfigFile(path, code=code)
        _mpath = self._getpath()
        tmp.read()
        self._console(self.name + " ?= " +tmp.data['_local']['name'])
        if (self.name == tmp.data['_local']['name']):
            path = _mpath
        else:
            path = _mpath+"."+tmp.data['_local']['name']

        self._console("add path:"+path)
        Aset.add(path, tmp.data, sync=True, flush=True)

    def _treeDp(self, indent):
        self._initChildOnce()
        line=indent+self.name
        self._console(line)
        indent = ' '*len(line)+'.'
        for name in self._getChildNames():
            try:
                self[name]._treeDp(indent)
            except:
                pass

    def tree(self):
        self._console('parent')
        self._treeDp("")        

class YManager(YTree, LogC, OutC):
    tags = ['_static']
    def __init__(self):
        YTree.__init__(self)
        LogC.__init__(self)
        self.log = Ylog()
        self.log.mod = "YManager"

    def ignore_test(self, *arg, **kwargs):
        '''
        test func
            self.func *arg[1:] **kwargs
        '''
        func=self[arg[0]]
        print(func)
        print(func(*arg[1:], **kwargs))

    def _getFilePath(self, **kwargs):
        if hasattr(self, 'parent') and self.parent:
            return self.parent._getFilePath(**kwargs)+"/"+self.name
        else:
            if 'local' in kwargs and kwargs['local']:
                return "./aprilcmd"
            return os.path.dirname(__file__)

    def isHidden(self):
        #默认 不隐藏
        return False

    def createModule(self, p, *args, **kwargs):
        self.check()
        path = self._getpath() +'.'+self.name
        tmp = __import__(path, fromlist=[self.type])
        if not hasattr(tmp, self.type):
            self._warn(str(tmp)+"has no type:"+self.type+ " attr")
            return

        module = eval('tmp.'+self.type+'()')
        arg = {}
        arg['name'] = self.name
        arg['tags'] = ['_static']
        if self.isHidden():
            arg['tags'].append('_hidden')

        module._fromJson(**arg)
        p._addChild(module)

    def isEnable(self):
        if Aset.get(self.path) == None:
            return False
        else:
            return True
    
    #@abstractmethod
    def check(self):
        return True

    def getModule(self, **kwargs):
        modules = []
        self.getModuleRe(modules, **kwargs)
        return modules

    def getModuleRe(self, modules, **kwargs):
        #print("try getModuleRe:"+self._getpath())
        if 'include' not in kwargs or kwargs['include'] in self.tags:
            if 'exclude' not in kwargs or kwargs['exclude'] not in self.tags:
                modules.append(self._getFilePath(local=True))

        for name in self._getChildNames():
            self[name].getModuleRe(modules, **kwargs)

    def doCheck(self):
        self._info("======doCheck==============")
        if self.check():
            mod = Aset.getMod(self._getpath())
            if not mod:
                Aset.addMod(self._getpath(), self.name, **{'tags':self.tags})
            
            names = self._getChildNames()
           
            for name in names:
                self[name].doCheck()
        else:
            Aset.delMod(self._getpath())

    def _initChild(self, *args, **kwargs):
        '''
        init the module tree
        '''
        self._debug("======_initChild============") 
        if self._getFilePath() == "":
            self._info("module "+self.name+" modulePath = NULL")
            return

        for file in os.listdir(self._getFilePath()):
            try:
                if not os.path.isdir(self._getFilePath()+'/'+file):
                    continue
                tmp = __import__(self._getpath() + '.'+file, fromlist=['manager'])
                if hasattr(tmp,'manager'):
                    self._addChild(tmp.manager)
                    tmp.manager._initChild(*args, **kwargs)
            except:
                self._info("module "+file+" not found")
                tb = traceback.format_exc()
                self._warn("unexpect module "+file+'\n'+tb)
                
        
        

#   ItemModule
#   作为字节点出现，类型统一，名字不同
#
class YModuleItem(YModule):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def _type(self, arg):
        pass

    @abstractmethod
    def _listHead():
        pass
    
    @abstractmethod
    def _listItem(self):
        pass
    
    def input(self, *args, **kwargs):
        pass

    def _fromJson(self,*arg,**kwargs):
        if (kwargs != {}):
            super()._fromJson(*arg, **kwargs)
        else:
            self.input()

    def _resetGetPath(self):
        self.f_tree()
        self._console("please input dstpath")
        dst = input()
        if dst == "":
            return '.'

        dstLen = len(dst)
        dstEnd = dst[dstLen -1]
        if dstEnd == '.':
            obj = self[dst[0:dstLen-1]]
            if obj:
                return dst + obj._resetGetPath()
            else:
                self._console("error path")
                return self._resetGetPath()
        else:
            obj = self[dst]
            if obj:
                return dst
            else:
                self._console("error path")
                return self._resetGetPath()

    def rename(self, *args):
        old = self.name
        self.name = args[0]
        self.parent._new(**self._toJson(a_dp=True))
        self.parent._delete(old)
        Aset.write()
        pass

    def resetItem(self, *args):
        if (len(args) > 0):
            dstpath = args[0]
        else:
            dstpath = self.parent._resetGetPath()
        if not dstpath:
            self._console("stop resetItem")
            return
        
        self.parent[dstpath]._new(**self._toJson(a_dp=True))
        self.parent._delete(self.name)
        Aset.write()
    
    def copyItem(self, *args):
        if (len(args) > 0):
            dstpath = args[0]
        else:
            dstpath = self.parent._resetGetPath()
        
        if not dstpath:
            self._console("stop resetItem")
            return
        
        self.name = self.name+'_bak'
        self.parent[dstpath]._new(**self._toJson(a_dp=True))
        Aset.write()

def ym_getItem(func): 
    def wrapper(self, *args, **kwargs):
        if len(args) >= 1:
            type = args[0] 
        elif kwargs != {}:
            type = kwargs['type']
        else:
            type = input()
        ret = func(self, type, args[1:], **kwargs)
        return ret
    return wrapper
#   ModuleList
#
class YModuleList(YModule):
    def __init__(self):
        super().__init__()
        self.items = []

    def _printTable(self, *args, **kwargs):
        items = args[0]
        table = {}
        for item in items:
            try:
                itype = item._type()
            except:
                continue
            if itype in table:
                table[itype].append(item)
            else:
                table[itype] = []
                table[itype].append(item)

        for itype in table:
            pt = []
            pt.append(itype._listHead())
            for item in table[itype]:
                if item.hidden:
                    continue
                try:
                    pt.append(item._listItem())
                except:
                    self._error("Error item not support:"+item.name)
            self._console(tabulate(pt, headers='firstrow', tablefmt='orgtbl'))
        return 

    def summay(self, *args, **kwargs):
        super().summay()
        items = []
        for item in self._getChildNames():
            if hasattr(self[item], 'tags') and '_static' in self[item].tags:
                continue
            items.append(self[item])

        if len(items) == 0:
            self._console("no data")
            return

        self._printTable(items)

    def _initChild(self, *args, **kwargs):
        _path = self._getpath()
        super()._initChild(*args, **kwargs)
        keys = Aset.getChild(_path)
        #print("init"+str(self)+" "+_path+" p:"+str(self.parent))
        for key in keys:
            arg = Aset.getMod(self._getpath()+'.'+key)
            if 'tags' in arg and '_static' in arg['tags']:
                continue
            try:
                item = self._InitItem(**arg) 
            except:
                if not self.ex:
                    self.ex = {}
                self.ex[key] = Aset.getMod(self._getpath()+'.'+key, all=True)
                self._info(self._getpath()+" init child "+key+" failed")
                tb = traceback.format_exc()
                self._warn(tb)


    def _getType(self, *args, **kwargs):
        if 'type' in kwargs:
            return kwargs['type']
        else:
            return args[0]

    def _InitItem(self, *args, **kwargs):
        import items
        newtype = self._getType(*args, **kwargs)
        if 'type' in kwargs:
            del kwargs['type']
        #print(str(args)+" ==> type:"+newtype)
        item = items.getClass(newtype)()
        item._fromJson(**kwargs)
        self._addChild(item)
        return item

    def _delItem(self, path):
        Aset.delMod(path)
    
    def _resetItem(self, *args, **kwargs):
        pass    

    def _new(self, *args, **kwargs):
        try:
            item = self._InitItem(*args, **kwargs)
            Aset.addMod(item._getpath(), item.name, **item._toJson())
            if hasattr(item,'C_depend'):
                print("depend:"+item.C_depend)
                self._InitItem(item.C_depend)
            return item
        except:
            tb = traceback.format_exc()
            self._warn("_new error\n"+tb)
            return None

    def new(self, *arg, **kwargs):
        print(self._getpath()+" new "+str(arg))
        item = self._new(*arg, **kwargs)
        Aset.write()
        return item
    
    def clean(self):
        self._initChildOnce()
        for item in self._getChildNames():
            print(item)
            if hasattr(self[item],'tags') and '_static' in self[item].tags:
                continue
            print("Delete mod:"+item)
            Aset.delMod(self[item]._getpath())
        Aset.write()
    
    def _delete(self, dst):
        Aset.delMod(self._getpath()+"."+dst)

    def delete(self, dst):
        self._delete(dst)
        Aset.write()
    
    def _getfile(self, key, **kwargs):
        paths = [dataPath]
        if 'path' in kwargs and kwargs['path'] != None:
            paths = kwargs['path']
        
        files = []
        for path in paths:
            if not os.path.exists(path+"/"+key):
                if 'create' in kwargs and kwargs['create'] == True:
                    os.makedirs(path+"/"+key)
                continue
            if not os.path.exists(path+"/"+key+'/'+self._getpath()):
                if 'create' in kwargs and kwargs['create'] == True:
                    files.append(path+"/"+key+'/'+self._getpath())
                continue
            files.append(path+'/'+key+'/'+self._getpath())
        return files
        
    def _loadDir(self, *args, **kwargs):
        keys = args[0]
        for key in keys:
            paths = self._getfile(key, **kwargs)
            for path in paths:
                print("loaddir:"+path)
                if os.path.exists(path):
                    self.aset_import(path)

                
    
    def _toDir(self, *args, **kwargs):
        keys = args[0]
        for key in keys:
            path = self._getfile(key, **kwargs)
            print("exprot:"+path+":"+key)
            self.aset_export(path,tag=key,ex=1)

            

    def init(self, *args, **kwargs):
        list = getPluginsPackageDataPaths()
        list.append(dataPath)
        keys = ['_base','priv']
        keys.extend(args)
        print("init plugin:"+str(list))
        print("init keys:"+str(keys))
        self._loadDir(keys, path=list)
    
    def fini(self, *args, **kwargs):
        keys = ['_base','priv']
        keys.extend(args)
        self._toDir(keys)

class YModuleListWithConf(YModuleList):
    def __init__(self, arg):
        super().__init__()
        self.configPath = '/data/tmp/'+arg


    @abstractmethod
    def scan(self, arg = None):
        pass

    def scan(self, arg = None):
        # 从另一个配置文件中copy
        from tool import aprilPath
        conf = JsonConfigFile(aprilPath + self.configPath)
        conf.read()
        self.scan_data(conf.data)
        Aset.write()

    def upload(self):
        self._console("conf upload => "+self.configPath)
        mod = Aset.getMod(self._getpath())
        if mod == None:
            return
        from tool import aprilPath
        conf = JsonConfigFile(aprilPath + self.configPath)
        conf.read()

        for task in mod['_items']:
            conf.add(task, mod['_items'][task])

        conf.write()

    def bset(self):
        conf = JsonConfigFile(aprilPath + self.configPath)
        conf.read()
        self._console(json.dumps(conf.data, indent=2))
    
    
