from tool import *

class Nodes(YModule):
    def __init__(self):
        self.nodes = []
        self.getNodes()   
        pass

    def getNodes(self):
        with open("/etc/hosts", "r") as fo:
            logging.info("open success")
            for line in fo.readlines():
                obj = re.match(r'(.*)\ node(.*)', line)
                if (obj):
                    ip = obj.group(1)
                    id = obj.group(2)
                    logging.info("node "+id+" "+ip)
                    inode = {}
                    inode['id'] = "node"+id
                    inode['ip'] = ip
                    self.nodes.append(inode)
        pass

    def dispatch(self):
        self.clusterfile("~/april")
        pass

    def clusterfile(self, file):
        for node in self.nodes:
            os.system("scp -r "+file+" "+node['id']+":~/")
        pass

    def clustercmd(self, cmd):
        for node in self.nodes:
            os.system("ssh "+node['id']+" "+cmd)
        pass

    def fun(self, name):
        if name == "all":
            self.clusterfile("/home/ygh/")
    
    def debug(self):
        os.system("mkdir -p /home/ygh")
        import root.host as RHost
        srv = RHost.host.hostByName['MYWORK']
        srv.ssh.getFile("~/code/crazyboy/shtool/hook/","/home/ygh/")
        pass

    def summay(self):
        table = []
        table.append(['id', 'ip'])
        i = 1
        for node in self.nodes:
            item = []
            item.append(i)
            item.append(node)
            table.append(item)
            i = i + 1
        
        print(tabulate(table, headers='firstrow', tablefmt='orgtbl'))
        print("dispatch")
        print("clusterfile + file")
        print("clustercmd + cmd")
        print("debug")

