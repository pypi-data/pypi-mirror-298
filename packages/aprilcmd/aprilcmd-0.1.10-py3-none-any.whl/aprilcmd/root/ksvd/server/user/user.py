from util import *
from tool import ksvd

class User(YModuleList):
    def __init__(self):
        super().__init__()
        pass
    
    def __scan(self, path):
        logging.info("scan users from "+path+" ...")
        path += "/ksvd-orgs/org-0/users/0local/"
        for dir in os.listdir(path):
            logging.info("scan add user:"+dir)
            Aset.addMod(self.path+"."+dir, dir, path+"/"+dir)
        Aset.write()
        
    def scan(self, path = None):
        if path == None:
            self.__scan("/home/kylin-ksvd/")
            return
        else:
            self.__scan(path)
            return

    def summay(self):
        super().summay()
        super(YModule, self).summay()
        print("function scan")
    
    def info(self):
        print("func:")
        print("scan ")
        pass
