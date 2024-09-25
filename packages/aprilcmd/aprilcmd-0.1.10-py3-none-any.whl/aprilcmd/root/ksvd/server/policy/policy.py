from tool import *

class Policys(YModuleList):
    def __init__(self):
        super().__init__()
        
    def scan(self):
        # 从ksvd_conf_path读取
        for root,dirs,files in os.walk(ksvd_conf_path):
            for afile in files:
                obj = re.match(r'settings\.([\da-f\-]*)$',afile);
                if obj:
                    id = obj.group(1)
                    item = self._getItem(id)
                    if item.name == None:
                        pass
                    Aset.add(self.path+'.'+item.name, id, sync=false, flush=false)
                else:
                    pass
        Aset.write()

    def summay(self):
        super().summay()
        super(YModule, self).summay()

    def info(self):
        self.summay()
        print("func:")
        print("scan to read info")
        print("getByName $name")
        print("getById $id")

    def dumpName(self):
        for id in self.policys:
            conf = self.policys[id].conf
            if 'UNIQB_SETTINGS_NAME' in conf.data:
                print(conf.data['UNIQB_SETTINGS_NAME'], "\t\t:", id)
            else:
                print("no name", "\t\t:", id)

    def getByName(self, name):
        for id in self.policys:
            policy = self.policys[id]
            if 'UNIQB_SETTINGS_NAME' in policy.conf.data:
                if policy.conf.data["UNIQB_SETTINGS_NAME"] == name:
                    policy.info()

    def getById(self, id):
        policy = self.policys[id]
        policy.info()
            
