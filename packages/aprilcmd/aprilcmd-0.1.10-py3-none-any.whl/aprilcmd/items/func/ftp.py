import sys
import ftplib
import time

from util import *
sys.path.append(getDir(__file__))
from base import *
sys.path.pop()

def is_dir(ftp, path):  
    try:
        ftp.cwd(path)  # 尝试进入目录  
    except Exception as e:
        return False
    return True

def get_time(ftp, file):
    try:
        mod_time = ftp.sendcmd('MDTM '+file)[4:]
        mod_time = time.strptime(mod_time,'%Y%m%d%H%M%S')
        mod_time = time.mktime(mod_time)
        return mod_time
    except Exception as e:
        return 0


class Ftp(Function, FileTransfer, Auth):
    C_hconf = {
        '21':{
            'ftp':{
                'ftp':{
                    'hdict':['ftp','tmp']
                }
            }
        }
    }
    keys = {**{
        "auths":[],
        "dir":'/'
    },**Function.keys}

    def __init__(self):
        super().__init__()
        self.name = "ftp"
        self.time_e = 36000
        self.time_diff = 0
        self.ftp = None

    def _login(self, **kwargs):
        (user, passwd, adir, w) = get_args(\
            ['user', 'passwd', 'dir', 'w'],\
            (None, None, self.dir, False), **kwargs)
        if user:
            try:
                self.ftp = ftplib.FTP()
                self.ftp.close()
                self.ftp.encoding = 'utf-8'
                self.ftp.connect(self.parent._getips())
                self.ftp.login(user=user, passwd=passwd)
                return True
            except:
                self.ftp.quit()
                return False
        
        n=0
        (user, passwd) = self.getAuth(n)
        while user:
            try:
                print(str(n)+":try login with "+user)
                self.ftp = ftplib.FTP()
                self.ftp.close()
                self.ftp.encoding = 'utf-8'
                self.ftp.connect(self.parent._getips())
                self.ftp.login(user=user, passwd=passwd)
                if w:
                    try:
                        from io import BytesIO 
                        bio = BytesIO(b'Hello, FTP!') 
                        self.ftp.storbinary('STOR '+adir+'/test_'+user+'.txt', bio)  
                    except Exception as e:
                        raise e
                return True
            except Exception as e:
                print("log failed")
                traceback.print_exc()
                self.ftp.quit()
                print(e)
                n=n+1
                (user, passwd) = self.getAuth(n)
                continue
                
        
        try:
            print("try login with anonymous")
            self.ftp = ftplib.FTP()
            self.ftp.close()
            self.ftp.encoding = 'utf-8'
            self.ftp.connect(self.parent._getips())
            self.ftp.login(user='anonymous', passwd='anonymous@')
            if w:
                self.ftp.storbinary('STOR '+adir+'/test_'+user+'.txt', b'Hello, FTP!') 
            return True
        except:
            print("log failed")
            self.ftp.quit()
            return False
        
        
    def _diffTime(self, srv, cli):
        (srv, cli, op) = get_args(\
            ["srv","cli","op"],\
            **kwargs)
        srv_time = get_time(self.ftp, srv)
        cli_time = os.path.getmtime(cli)
        diff_time = srv_time - cli_time -self.time_diff
        print(diff_time)
        if (diff_time > 0 and diff_time > self.time_e):
            return diff_time
        if (diff_time < 0 and diff_time < -self.time_e):
            return diff_time
        else:
            return 0

    def _putFile(self, **kwargs):
        (srv, cli, func_difftime) = get_args(\
            ["srv","cli","func_difftime"],\
            **kwargs)
        
        diff_time = 0

        if func_difftime:
            diff_time = func_difftime(srv=srv, cli=cli, op='put')

        if get_time(self.ftp, srv) !=0 and ( diff_time >= 0):
            self._info(srv + "srv is new pass it, time:"+str(diff_time))
            return
 
        self._console("put file "+cli+ " => "+ srv + " diff time:"+str(diff_time))

        bufsize = 1024
        file_handle = open(cli, "rb")
        self.ftp.storbinary('STOR '+srv, file_handle, bufsize)
        file_handle.close()
    
    def _putDir(self, **kwargs):
        (srv, cli, func_difftime) = get_args(\
            ["srv","cli", "func_difftime"],\
            **kwargs)

        # 如果cli目录不存在，创造目录
        try:
            self.ftp.cwd(os.path.dirname(srv))
            self.ftp.mkd(os.path.basename(srv))
        except Exception as e:
            self._debug("create dir failed:"+srv)


        for _file in os.listdir(cli):  
            if os.path.isdir(cli+'/'+_file):  
                self._putDir(srv=srv+'/'+_file, cli=cli+'/'+_file, func_difftime=func_difftime)
            else:
                self._putFile(srv=srv+'/'+_file, cli=cli+'/'+_file, func_difftime=func_difftime)


    def putFile(self, **kwargs):
        if not self._login(**kwargs, w=True):
            return False
        if 'dir' in kwargs:
            self.dir = kwargs['dir']
        (srv, cli) = get_args(\
            ["srv","cli"],\
            ("april", "april"),\
            **kwargs)

        if os.path.isdir(cli):
            self._putDir(srv=self.dir+'/'+srv, cli=cli, func_difftime=self._ignoreTime)
        else:
            self._putFile(srv=self.dir+'/'+srv, cli=cli, func_difftime=self._ignoreTime)
        return True

    def _getFile(self, **kwargs):
        (srv, cli, func_difftime) = get_args(\
            ["srv","cli","func_difftime"],\
            **kwargs)

        print(srv)
        print(cli)
        print(func_difftime)
        diff_time = 0
        if func_difftime:
            diff_time = func_difftime(srv=srv, cli=cli, op='get')

        if os.path.exists(cli) and (diff_time <= 0):
            self._info("cli is new pass it diff_time:"+str(diff_time)+" func:"+str(func_difftime))
            return
            

        self._console("get file "+cli+ " <="+ srv + " diff time:"+str(diff_time))
        
        bufsize = 1024
        file_handle = open(cli, "wb")

        self.ftp.retrbinary('RETR '+srv, file_handle.write, bufsize)
        file_handle.close()

    def _getDir(self, **kwargs):

        (srv, cli, func_difftime) = get_args(\
            ["srv","cli","func_difftime"],\
            **kwargs)

        self._debug("get dir "+srv+
            " <="+ cli)

        # 如果cli目录不存在，创造目录
        if os.path.exists(cli):
            self._debug("dir "+cli+" exists")
            pass
        else:
            self._debug("try create dir "+cli)
            os.mkdir(cli)

        self.ftp.cwd(srv)

        for file in self.ftp.nlst():  
            if file == '.' or file == '..':  
                continue  # Skip the '.' and '..' directories  
            self._debug("test file:"+file)
            if is_dir(self.ftp, srv+'/'+file):  # Check if it's a directory  
                self._getDir(srv=srv+'/'+file, cli=cli+'/'+file, func_difftime=func_difftime)  # If it's a directory, recursively traverse it 
            else:
                self._getFile(srv=srv+'/'+file, cli=cli+'/'+file, func_difftime=func_difftime)

    @parse_args
    def getFile(self, **kwargs):
        if not self._login(**kwargs):
            return False

        (srv, cli) = get_args(\
            ["srv","cli"],\
            ("april", "april"),\
            **kwargs)

        if is_dir(self.ftp, srv):
            self._getDir(srv=self.dir+'/'+srv, cli=cli, func_difftime=self._ignoreTime)
        else:
            print(self._ignoreTime)
            self._getFile(srv=self.dir+'/'+srv, cli=cli, func_difftime=self._ignoreTime)
        
        self.ftp.quit()
        return True
    
    def _diffPrintCli(self, file):
        self._console("_diffPrintCli ==> "+file)

    def _diffPrintSrv(self, file):
        self._console("_diffPrintSrv <== "+file)

    def _diffDelCli(self, file):
        self._console("f_delete file:"+file)
        if os.path.isdir(file):
            import shutil
            shutil.rmtree(file)
        else:
            os.remove(file)

    def _diffDelSrv(self, file):
        self._console("f_delete file:"+file)
        if is_dir(self.ftp, file):
            self.ftp.rmd(file)
        else:
            self.ftp.delete(file)
    
    def _ignoreTime(self, *args, **kwargs):
        (srv, cli, op) = get_args(\
            ["srv","cli","op"],\
            **kwargs)
        if op == 'get':
            return 1
        if op == 'put':
            return -1
        return 0

    def _diff(self, local_dir, ftp_dir, **kwargs):
        (dc,ds,func_difftime) = get_args(\
            ["dc","ds","time"],\
            (self._diffPrintCli,self._diffPrintSrv,self._ignoreTime),\
            **kwargs)

        if not os.path.isdir(local_dir):
            time_diff = func_difftime(ftp_dir, local_dir)
            if (time_diff < 0):
                dc(local_dir)
            if (time_diff > 0):
                ds(ftp_dir)
            return
        
        self.ftp.cwd(ftp_dir)
        ftp_file = []
        local_file = []
        for _file in self.ftp.nlst():
            ftp_file.append(_file)
        
        for _file in os.listdir(local_dir):  
            local_file.append(_file)
        
        for _file in ftp_file:
            if _file in local_file:
                self._diff(local_dir+'/'+_file, ftp_dir+'/'+_file, ds=ds,dc=dc)
                local_file.remove(_file)
            else:
                ds(ftp_dir+'/'+_file)

        for _file in local_file:
            dc(local_dir+'/'+_file)


    @parse_args
    def diff(self, *args, **kwargs):
        self._login(**kwargs)

        (srv, cli) = get_args(\
            ["srv","cli"],\
            (self.dir, "/var/ftp"),\
            **kwargs)

        if not is_dir(self.ftp, srv):
            self._console("srv:"+srv+" is not dir")
            return
        
        if not os.path.isdir(cli):
            self._console("cli:"+cli+" is not dir")
            return
        
        self._diff(cli, srv)
    
    @parse_args  
    def fupdate(self, *args, **kwargs):
        self._login(**kwargs)

        (srv, cli, base) = get_args(\
            ["srv","cli","base"],\
            ("/ygh/", "/var/ftp",""),\
            **kwargs)
    
        if (base == ""):
            self.putFile(*args, srv=srv,cli=cli)
            self.getFile(*args, srv=srv,cli=cli)
        
        if (base == "cli"):
            self._diff(cli, srv, ds=self._diffDelSrv)
            self.putFile(*args, srv=srv,cli=cli)
        
        if (base == "srv"):
            self._diff(cli, srv, dc=self._diffDelCli)
            self.getFile(*args, srv=srv,cli=cli)


class Center(Function):
    def __init__(self):
        super().__init__()
        self.name = "center"

    def up(self):
        for funName in self.parent._getChildNames():
            fun = self.parent[funName]
            if fun.canWrite():
                print("try send by:"+funName)
                self._getroot().package.pack()
                if fun.putFile(srv="ytool.tar",cli=aprilPath+"/tmp/ytool.tar"):
                    return True
        return False
    
    def down(self):
        for funName in self.parent._getChildNames():
            fun = self.parent[funName]
            if fun.canRead():
                print("try get by:"+funName)
                if fun.getFile(srv="ytool.tar",cli=aprilPath+"/tmp/ytool.tar"):
                    self._getroot().package.unpack()
                    return True
        return False
    
