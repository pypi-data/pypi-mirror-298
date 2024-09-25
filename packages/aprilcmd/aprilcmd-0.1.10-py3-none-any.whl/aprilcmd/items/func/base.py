
from util import *
class Function(YModuleItem):
    def _type(self):
        return Function

    def _listHead():
        return ['name', 'desc']

    def _listItem(self):
        return [self.name, ""]

    def input(self):
        pass


from abc import ABC, abstractmethod  
  
class FileTransfer(ABC):  
    @abstractmethod  
    def putFile(self, file_path, target_location):  
        """  
        纯虚函数，用于上传文件。  
        子类必须实现这个方法。  
          
        :param file_path: 本地文件路径  
        :param target_location: 目标位置（可能是一个URL、路径或其他标识符）  
        """  
        pass  
  
    @abstractmethod  
    def getFile(self, source_location, local_path):  
        """  
        纯虚函数，用于下载文件。  
        子类必须实现这个方法。  
          
        :param source_location: 源位置（可能是一个URL、路径或其他标识符）  
        :param local_path: 本地存储路径  
        """  
        pass  
  
    def canRead(self):  
        """  
        具体方法，用于判断是否可以读取文件。  
        默认实现返回True，但子类可以覆盖以提供更具体的实现。  
        """  
        return True  
  
    def canWrite(self):  
        """  
        具体方法，用于判断是否可以写入文件。  
        默认实现返回True，但子类可以覆盖以提供更具体的实现。  
        """  
        return True  

class Auth(ABC):
    def encode(self, up):
        return up
    def decode(self, dup):
        return dup
    def getAuth(self, n=0):
        if len(self.auths) <= n:
            return (None, None)
        dup = self.auths[n]
        if not dup:
            return (None, None)
        up = self.decode(dup)
        hl=int(up[0])
        ul=int(up[1:hl+1])
        return(up[hl+1:hl+ul+1], up[hl+ul+1:])

    
    def setAuth(self, *args, **kwargs):
        """
        """
        if len(args) >= 1:
            auths = args[0]
        print("setAuth:"+str(auths))
        for auth in auths:
            ul=len(auth['username'])
            hl=len(str(ul))
            up=str(hl)+str(ul)+auth['username']+auth['password']
            dup=self.encode(up)
            if not dup in self.auths:
                self.auths.append(dup)

'''
class TAuth(Auth):
    def __init__(self):
        self.auths=[]

tAuth = TAuth()
tauths = [
    {
        'username':"hahaha",
        'password':"hahahapass"
    },
    {
        'username':"hahahahahahahahahahahahahahaha",
        'password':"hahahapass"
    }
]
tAuth.setAuth(tauths)
(u,p) = tAuth.getAuth()
print(u)
print(p)
(u,p) = tAuth.getAuth(1)
print(u)
print(p)
'''