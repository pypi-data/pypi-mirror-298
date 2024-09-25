#codeing = utf-8
import json
import re
import os
from util.ycommon import *

class File:
    def __init__(self, path): 
        self.path = path

    def read(self):
        pass

    def write(self):
        pass

    def tryCreate(self):
        pass

class Config(Yobj):
    def parse(self, data):
        pass

    def __init__(self, data = None):
        self.data = {}
        if (data):
            self.parse(data)

    #add del set get
    def __add(self, path, data):
        pass

    def __del(self, path):
        pass

    def __set(self, path, data):
        pass

    def __get(self, path):
        pass

    def summay(self):
        print("conf path:", self.path)

class KylinConfigFile(Config, File):
    def __init__(self, path):
        Config.__init__(self) 
        File.__init__(self, path)

    def read(self):
        logging.debug("trace KylinConfig read")
        with open(self.path, "r") as fo:
            for line in fo.readlines():
                obj = re.match(r'(.*)=(.*)', line)
                if (obj):
                    self.data[obj.group(1)] = obj.group(2).strip('"')
    def info(self):
        self.toTable()
        for k in self.data:
            print(k+":"+self.data[k])
    
    def get(self, path):
        if path in self.data:
            return self.data[path]
        else:
            return "NONAME"
    
    def toTable(self, keys = []):
        table = []
        table.append(["key", "val"])
        if len(keys) == 0:
            for k in self.data:
                line = [k, self.data[k]]
                table.append(line)
            return table
        else:
            for k in self.data:
                if k in keys:
                    line = [k, self.data[k]]
                    table.append(line)
            return table

class DirConfig(Config):
    def __init__(self, path, lvl = 4):
        self.path = path
        self.lvl = lvl

    def _getpath(self, paths):
        return paths.split('.')
    def add(self, path, data):
        pass
    def delete(self, path, data):
        pass
    def set(self, path, data):
        pass
    def get(self, path, data):
        pass

class JsonConfig(Config):
    def __getRec(self, path, now):
        if len(path) == 0:
            return now

        if type(now) != dict and type(now) != list:
            return None 

        idx = path[0]
        obj = re.match(r'\[(\d)\]', idx) 
        if obj:
            idx = int(obj.group(1))
        elif idx in now:
            pass
        else:
            return None

        return self.__getRec(path[1:], now[idx])

    def __get(self, path):
        if path == "":
            pathlist = []
        else:
            pathlist = path.split('.')
        return self.__getRec(pathlist, self.data)


    def __setValue(self, data):
        logging.debug("[__setValue] "+json.dumps(data))
        if data == "ydict":
            return {}
        if data == "ylist":
            return []
        else:
            return data

    def __setRecList(self, idx, path, now, data):
        if len(path) == 0:
            if len(now) == idx:
                now.append({})
            now[idx] = self.__setValue(data)
            return

        if type(now) != list:
            #not list
            logging.debug("not list")
            return

        if len(now) <= idx:
            #len not enough
            logging.debug("len short")
            return 

        self.__setRec(path, now[idx], data)
        return

    def __setRecDict(self, idx, path, now, data):
        if len(path) == 0:
            now[idx] = self.__setValue(data)
            return

        if type(now) != dict:
            #not dict
            logging.debug("not dict")
            return

        if idx not in now:
            #no this key
            logging.debug("no key")
            return 


        self.__setRec(path, now[idx], data)
        return

    def __setRec(self, path, now, data):
        if len(path) == 0:
            raise Networkerror("Invalid argment")

        idx = path[0]
        obj = re.match(r'\[(\d)\]', idx) 
        if obj:
            idx = int(obj.group(1))
            self.__setRecList(idx, path[1:], now, data)
        else:
            self.__setRecDict(idx, path[1:], now, data)

        return

    def __set(self, path, data):
        if path == "":
            pathlist = []
            self.data = self.__setValue(data)
            return
        else:
            pathlist = path.split('.')
            self.__setRec(pathlist, self.data, data)
            return

    def __add(self, path, data):
        now = self.__get(path)
        print("add __get "+path+" :"+str(now)+ " =>"+str(data))
        if not now:
            self.__set(path, data)
        elif type(now) == dict:
            now.update(data)
            self.__set(path, now)
        else:
            logging.warn("add "+path+" exist data:"+str(now))

    def __delete(self, path):
        logging.debug("__delete "+path)
        if path == "":
            logging.warn("__delete unexpect arg \"\"")
            return
        else:
            pathlist = path.split('.')
        
        last = len(pathlist)
        dpath = pathlist[0:last-1]
        dst = pathlist[last-1]
        now = self.__getRec(dpath, self.data)
        if now == None:
            return        
        del now[dst]
        now = self.__get(path)

    # 命令
    def add(self, *args, **kwargs):
        """
        add data to conf
            {"a":1, "b":2 } add {"b":3, "c":4} = {"a":1, "b":3, "c":4}
        args: path, data
        kwargs: path, data
            path: for example host.net.10.10.10.1.ftp
            data: a dict(json)
        """
        path=args[0]
        data=args[1]
        self.__add(path, data);

    def delete(self, *args, **kwargs):
        path=args[0]
        self.__delete(path)
        pass

    def set(self, *args, **kwargs):
        path=args[0]
        data=args[1]
        self.__set(path, data)
        logging.debug("after set :"+json.dumps(self.data))

    def get(self, *args, **kwargs):
        """
        get data in conf
        args: path
        kwargs: path
            path: for example host.net.10.10.10.1.ftp
        ret:data
            data: a data maybe dict, list, number, str...
        """
        path = args[0]
        return self.__get(path)

    def summay(self):
        super().summay()
        
    def info(self):
        self.summay()
        for k in self.data:
            if type(k) == str:
                print(k, self.data[k])
            else:
                print(k)
        print("KylinConfig===func===")
        print("function add del set get")

import base64

class JsonConfigFile(JsonConfig, File):
    def __init__(self, path, **kwargs):
        if 'code' in kwargs:
            self.code = kwargs['code']
        else:
            self.code = 'b64'
        JsonConfig.__init__(self)
        File.__init__(self, path)

    def encode(self, data):
        if (self.code == 'b64'):
            return base64.b64encode(data.encode("utf-8"))
        else:
            return data.encode("utf-8")
    
    def decode(self, data):
        if (self.code == 'b64'):
            return base64.b64decode(data).decode('utf-8')
        else:
            return data

    def read(self):
        logging.debug("trace JsonConfig read "+self.path)
        if os.path.isfile(self.path):
            logging.debug("open success")
            with open(self.path, "r") as fo:
                if fo:
                    context = fo.read()
                    data = self.decode(context)
                    self.data = json.loads(data)
                    fo.close()
        else:
            logging.error(self.path+" is not a file")
            self.data = {} 
        
    def write(self):
        logging.info("JsonConfig write "+self.path)
        print("JsonConfig write "+self.path)
        with open(self.path, "wb+") as fo:
            if fo:
                data = json.dumps(self.data, indent=2)
                context = self.encode(data)
                fo.write(context)
                fo.close()

    def add(self, *args, **kwargs):
        """
        add data to conf
            {"a":1, "b":2 } add {"b":3, "c":4} = {"a":1, "b":3, "c":4}
        args: path, data
        kwargs: path, data, flush, sync
            path: for example host.net.10.10.10.1.ftp
            data: a dict(json)
            flush: true or false to write to disk
            sync: true or false to update before add
        """
        if 'sync' in kwargs and kwargs['sync']:
            self.read()
        super().add(*args, **kwargs)
        if 'flush' in kwargs and kwargs['flush']:
            self.write()

    def delete(self, *args, **kwargs):
        """
        delete data in conf
        args: path
        kwargs: path, flush, sync
            path: for example host.net.10.10.10.1.ftp
            flush: true or false to write to disk
            sync: true or false to update before add
        """
        print("delete"+args[0])
        if 'sync' in kwargs and kwargs['sync']:
            self.read()
        super().delete(*args, **kwargs)
        if 'flush' in kwargs and kwargs['flush']:
            self.write()

    def set(self, *args, **kwargs):
        """
        set data to conf
            {"a":1, "b":2 } set {"b":3, "c":4} = {"b":3, "c":4}
        args: path, data
        kwargs: path, data, flush, sync
            path: for example host.net.10.10.10.1.ftp
            data: a dict(json)
            flush: true or false to write to disk
            sync: true or false to update before add
        """
        if 'sync' in kwargs and kwargs['sync']:
            self.read()
        super().set(*args, **kwargs)
        if 'flush' in kwargs and kwargs['flush']:
            self.write()
    
    def get(self, *args, **kwargs):
        """
        get data in conf
        args: path
        kwargs: path, sync
            path: for example host.net.10.10.10.1.ftp
            sync: true or false to update before add
        ret:data
            data: a data maybe dict, list, number, str...
        """
        if 'sync' in kwargs and kwargs['sync']:
            self.read()
        return super().get(*args, **kwargs)
        


logging.info("INIT tool.conf")

class Dict(Config, File):
    def __init__(self, path):
        self.path = path
        self.keys = []
    
    def read(self):
        if not os.path.isfile(self.path):
            return None
        fo = open(self.path, "r")
        if not fo:
            return None
        import base64
        context = fo.read()
        print("context:"+context)
        data = base64.b64decode(context)
        self.keys = data.decode("utf-8").split('\n')
    


