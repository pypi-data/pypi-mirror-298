import logging
import os
import time
from abc import ABC, abstractmethod

def get_args(*args, **kwargs):
    if len(args) >= 1:
        list = args[0]

    if len(args) >= 2:
        a = args[1]
    else:
        a = tuple([None]*len(list))

    i = 0
    for key in list: 
        i = i+1
        if key in kwargs:
            if len(a) == i:
                b = a[0:i-1]+(kwargs[key],)
            else:
                b = a[0:i-1]+(kwargs[key],)+a[i:]
            a = b
    return a
        

class Yobj(ABC):
    @abstractmethod
    def summay(self):
        pass

class Ylog(ABC):
    def __init__(self):
        self.lvl = 2
        self.mod = "Unkown"
    
    def log(self, log, **kwargs):
        (module, r) = get_args(\
            ["module", "r"],\
            (self.mod, None),\
            **kwargs)
        logging.info('['+time.strftime("%Y-%m-%d")+']['+module+']'+log)
        pass

    def _error(self, log, **kwargs):
        if 'lvl' in kwargs:
            lvl = kwargs['lvl']
        else:
            lvl = self.lvl
        if lvl < 1:
            return
        self.log('[E]'+log, **kwargs)

    def _warn(self, log, **kwargs):
        if 'lvl' in kwargs:
            lvl = kwargs['lvl']
        else:
            lvl = self.lvl
        if lvl < 2:
            return 
        self.log('[W]'+log, **kwargs)

    def _info(self, log, **kwargs):
        if 'lvl' in kwargs:
            lvl = kwargs['lvl']
        else:
            lvl = self.lvl
        if lvl < 3:
            return
        self.log('[I]'+log, **kwargs)

    def _debug(self, log, **kwargs):
        if 'lvl' in kwargs:
            lvl = kwargs['lvl']
        else:
            lvl = self.lvl
        if lvl < 4:
            return
        self.log('[D]'+log, **kwargs)
    
    def _console(self, log):
        print(log)


logging.info("INIT tool.ycommon")


def mod_trace(msg):
    pass
    #print("[MODTRACE]:"+msg)

import re

def ignore(func):
    pass

def parse_args(func): 
    def wrapper(self, *args, **kwargs):
        for key,value in kwargs.items():
            if not isinstance(value, str):
                continue
            matches = re.findall(r"_\{[^\}]*\}", value)
            if matches == []:
                continue

            value = re.sub(r"_\{([^\}]*)\}", self._arg_replace, value)
            kwargs[key] = value
        return func(self, *args, **kwargs)  
    return wrapper  

def parse_str(self, str): 
    value = str
    matches = re.findall(r"_\{[^\}]*\}", value)
    if matches == []:
        pass
    else:
        value = re.sub(r"_\{([^\}]*)\}", self._arg_replace, value)
    return value



def revars(obj, dep = 3):
    if dep == 0:
        return "overdep"

    if isinstance(obj, (str, int)):
        return obj
    
    if isinstance(obj, list):
        ret = []
        for node in obj:
            nnode = revars(node,dep-1)
            ret.append(nnode)
        return ret

    if isinstance(obj, object):
        ret = {}
        vobj = vars(obj)
        for attr in vobj:
            value = vobj[attr]
            nvalue = revars(value, dep-1)
            ret[attr] = nvalue
        return ret

def list_overlap(list1, list2):
    return any(item in list2 for item in list1)


def pvid2str(num):  
    # 将数字转换为十六进制字符串（包含'0x'前缀）  
    hex_str = hex(num)[2:]  # 切片去掉'0x'前缀  
    # 使用格式化来确保结果是4位的，不足时前面补0  
    padded_hex_str = format(int(hex_str, 16), '04x')  
    return padded_hex_str  


def dictadd(dict1, dict2):  
    """  
    深度合并两个字典  
  
    参数:  
    dict1 (dict): 第一个字典  
    dict2 (dict): 第二个字典，其键值对将被合并到dict1中  
  
    返回:  
    dict: 合并后的字典  
    """  
    result = {}  
      
    # 遍历第一个字典  
    for key in dict1:  
        # 如果dict1的键在dict2中也存在，并且两者都是字典，则递归合并  
        if key in dict2 and isinstance(dict1[key], dict) and isinstance(dict2[key], dict):  
            result[key] = dictadd(dict1[key], dict2[key])  
        else:  
            # 否则，直接使用dict1的键值对  
            result[key] = dict1[key]  
              
    # 将dict2中独有的键值对添加到结果中  
    for key in dict2:  
        if key not in result:  
            result[key] = dict2[key]  
      
    return result  

def getPluginsPackageNames():
    from util.ysys import pyPath
    #遍历pyPath目录下记录所有名字是aprilcmd_开头的目录
    import os, sys
    PPNameList = []
    for root, dirs, files in os.walk(pyPath):
        for name in dirs:
            if name[:9] == 'aprilcmd_':
                #print(name)
                PPNameList.append(name[9:])
    return PPNameList

def getPluginsPackagePath(PPName):
    from util.ysys import pyPath
    path = os.path.join(pyPath, 'aprilcmd_'+PPName)
    if not os.path.exists(path):
        print('插件目录不存在')
        return None
    return path

def getPluginsPackageDataPath(PPName):
    PPPath = getPluginsPackagePath(PPName)
    PPDPath = PPPath + '/data'
    return PPDPath

def getPluginsPackageDataPaths():
    names = getPluginsPackageNames()
    print(names)
    paths = []
    for name in names:
        path = getPluginsPackageDataPath(name)
        paths.append(path)
    return paths