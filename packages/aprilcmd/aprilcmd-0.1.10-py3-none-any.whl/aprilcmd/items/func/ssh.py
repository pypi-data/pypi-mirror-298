import sys

from util import *
sys.path.append(getDir(__file__))
from base import *
sys.path.pop()

class Ssh(Function,FileTransfer):
    C_hconf = {
        '22':{
            'ssh':{
                'ssh':{
                    'hdict':['base6']
                }
            }
        }
    }
    keys = {**{
        "auths":[]
    },**Function.keys}

    def __init__(self):
        super().__init__()
        self.name = "ssh"
        
    def getIUP(self):
        return self.parent.ip + " " +self.auths[0]['username'] + " " + self.auths[0]['password']

    def ssh(self):
        import subprocess
        subprocess.run(['gnome-terminal', '--', 'sshpass', '-p', self.auths[0]['password'], 'ssh', '-o', 'StrictHostKeyChecking=no', self.auths[0]['username']+'@'+self.parent.ip])

    def cmd(self, cmdstr):
        cmd = "ycmd "+self.getIUP()+" '"+cmdstr+"'"
        logging.info(self.parent.name+"==>"+cmd)
        os.system(cmd)

    def debugsrv(self, user, debugfiledir):
        self.cmd("mkdir -p /home/"+user+"debug")
        self.putFile(debugfiledir, "/home/"+user)

    def updatetool(self, user, debugfiledir):
        self.getFile("/home/"+user+"/start.sh", debugfiledir+"/start.sh")
        self.getFile("/home/"+user+"/hook.sh", debugfiledir+"/hook.sh")

    def putFile(self, src, dst=""):
        cmd = "yscps "+self.getIUP()+" \""+src+"\" \""+dst+"\" "
        self._console("putFile "+cmd)
        os.system(cmd)

    def getFile(self, src, dst=""):
        cmd = "yscpr "+self.getIUP()+" \""+src+"\" \""+dst+"\" "
        self._console("getFile "+cmd)
        os.system(cmd)
