from util import *

import os
def getnode(map, path):
    if len(path) == 0:
        return map
        
    return getnode(map[path[0]],path[1:])

def Rpath(path):
    return './'+'/'.join(path)

def getfilefrommap(filemap, path):
    node = getnode(filemap, path)
    if node == {}:
        return [Rpath(path)]
    ret = []
    for i in node:
        newpath = []
        newpath.extend(path)
        newpath.append(i)
        ret.extend(getfilefrommap(filemap, newpath))
    return ret

class Package(YModule):
    def __init__(self):
        super().__init__()

    def summay(self):
        super().summay()
    

        
    def __pack(self, *args, **kwargs):
        filemap = {
            'code':{},
            'data':{}
        }
        desc = ' --exclude=data/priv/* --exclude=.git --exclude=*.pyc'
        (srcpath, dstpath, desc, filemap) = get_args(\
            ['srcpath', 'dstpath', 'desc', 'filemap'],\
            (aprilPath, aprilPath+'/tmp/ytool.tar', desc, filemap), **kwargs)

        filelist = getfilefrommap(filemap, [])
        self._console('pack filelist:'+str(filelist))
        
        cmd = 'cd '+ srcpath +';tar '+desc+ ' -cf '+dstpath+' '+' '.join(filelist)
        self._console(cmd)
        os.system(cmd)
        pass
    
    def _pack(self, *args, **kwargs):
        #arg lvl ex
        (lvl, ex) = get_args(\
            ['lvl','ex'],\
            (1,{}), **kwargs)
        
        if lvl == 1:
            filemap = {
                'code':{},
                'data':{}
            }
        if lvl == 2:
            filemap = {
                'code':{
                    'root':{
                        "host":{},'package':{},'tool':{},'__init__.py':{}
                    },
                    'shelltool':{},'third':{},'util':{},'install.sh':{},'ycmd.py':{}
                },
                'data':{},
                'tmp':{'.tmp':{}}
            }
        kwargs['filemap'] = {**filemap, **ex}
        self._console(kwargs)
        self.__pack(**kwargs)
        pass

    def __unpack(self, *args, **kwargs):

        (srcpath, dstpath) = get_args(\
            ['srcpath','dstpath'],\
            (aprilPath+'/tmp/ytool.tar', aprilPath), **kwargs)

        for key,value in kwargs.items():
            if key == 'srcpath':
                srcpath = value
            if key == 'dstpath':
                dstpath = value
            if key == 'desc':
                desc = value
        cmd = 'tar -xf ' + srcpath + ' -C '+ dstpath
        os.system('mkdir -p '+dstpath)
        self._console(cmd)
        os.system(cmd)

    def __clean(self):
        os.system('rm -rf '+ aprilPath +'/tmp/*')

    def __send(self, host):
        host.cmd("cd ~;/usr/bin/mkdir -p .ycmd")
        host.putFile(aprilPath + 'ytool.tar', "\~/.ycmd/ytool.tar")

    def __rinstall(self, *args, **kwargs):
        #kwargs lvl ex srcpath dstpath desc filemap from _pack
        #kwargs srcpath dstpath from __unpack
        #kwargs dir host
        #args
        host = args[0]
        (dir, host) = get_args(\
            ['dir','host'],\
            ('~',host), **kwargs)
        
        dstpath=aprilPath + '/tmp/.april'
        self._pack(**kwargs)
        self.__unpack(dstpath=dstpath)

        host.putFile(dstpath, dir)
        host.cmd("/bin/bash "+dir+"/.april/code/install.sh "+host.ip)

    def _rinstall(self, *arg, **kwargs):
        self.__rinstall(*arg, **kwargs)
        
    def __install(self):
        cmd="ln -sf "+codePath+"/ycmd.py ~/.local/bin/ycmd.py"
        print(cmd)
        os.system(cmd)
        cmd="ln -sf "+codePath+"/shelltool/yscps ~/.local/bin/yscps"
        print(cmd)
        os.system(cmd)
        cmd="ln -sf "+codePath+"/shelltool/yscpr ~/.local/bin/yscpr"
        print(cmd)
        os.system(cmd)
        cmd="ln -sf "+codePath+"/shelltool/ycmd ~/.local/bin/ycmd"
        print(cmd)
        os.system(cmd)

    def install(self):
        self.__install()

    def standard(self):
        for file in self.files:
            print ("standard file "+file)
            os.system("sed -i 's/\t/    /g' "+file)

    def pack(self, *args, **kwargs):
        if len(args) == 0:
            path = aprilPath+'/tmp/ytool.tar'
        else:
            path = args
        kwargs['dstpath'] = path
        self._pack(*args, **kwargs)

    def unpack(self, *args, **kwargs):
        if len(args) == 0:
            path = aprilPath+'/tmp/ytool.tar'
        else:
            path = args

        self.__unpack(path, **kwargs)
           
    def rinstall(self, *arg, **kwargs):

        if len(arg) < 1:
            print("rinstall: hostname")
            self._getroot().host.info()
            return
        
        host = arg[0]
        print("rinstall: "+host)

        try:
            # 远程安装
            dsthost = getattr(self._getroot().host.host, host)
            self.__rinstall(dsthost)
        except:
            print("rinstall faild")

    def rdown(self, arg):
        from root.host.host import host as RHost
        print("rdown: "+arg)
        dsthost = getattr(RHost, arg)
        dsthost.cmd('ycmd.py package pack')
        dsthost.getFile("\~/.ycmd/ytool.tar", os.environ['HOME']+"\~/.ycmd/ytool.tar")
        os.system('cd '+os.environ['HOME']+';tar -xvPf .ycmd/ytool.tar')

    def up(self, *args, **kwargs):
        center='center'
        if (len(args) >= 1):
            center=args[0]
        if self._getroot().host._base[center].up():
            return True
        self._console("up to center("+center+") failed")
        return False
    
    def down(self, *args, **kwargs):
        center='center'
        if (len(args) >= 1):
            center=args[0]
        if self._getroot().host._base[center].down():
            return True
        self._console("down from center("+center+") failed")
        return False


