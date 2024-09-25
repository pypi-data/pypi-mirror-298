import os
import sys

#命令所在目录作为工具目录
ycmdfile=os.path.abspath(__file__)
ycmddir=os.path.dirname(ycmdfile)
sys.path.append(ycmddir)

# 检查配置
import util.setting

#解析参数
def getArgs():
    args = []
    kwargs = {}
    for arg in sys.argv:
        if '=' not in arg:
            args.append(arg)
            continue
        key = arg[:arg.index('=')] # 提取等号前的部分作为key
        value = arg[arg.index('=')+1:] # 提取等号后的部分作为value
        try:
            value = int(value) # 根据需要进行类型转换
        except ValueError:
            pass
        
        kwargs[key] = value # 添加到kwargs字典中

    if 'dict' in kwargs:
        dict =  eval(kwargs['dict'])
        del kwargs['dict']
        kwargs = {**kwargs,**dict}

    return (args, kwargs)

#加载root
from root import *
def main():
    (args, kwargs) = getArgs()

    root = Root()
    root._initChildOnce(*args, **kwargs)

    obj = root
    fun = "summay"


    #提取obj和fun
    args = args[1:]
    n = len(args)

    if n > 0:
        obj = root[args[0]]
        args = args[1:]
 
    if n > 1:
        fun = args[0]
        args = args[1:]


    # 执行命令
    #print(str(obj)+fun)
    func = obj[fun]
    func(*args, **kwargs)

pythondir=os.path.dirname(ycmddir)

def scan(dir, file_len):
    #先判断目录下有没有__init__.py文件
    if os.path.exists(os.path.join(dir,"__init__.py")):
        #打印下当前目录，退出
        print("目录"+dir+"下有__init__.py")
        #判断当前文件相对于pythondir下的aprilcmd_xxx的目录，并在pythondir下aprilcmd目录下对应的相对位置创建一个链接
        rel_dir = dir[len(pythondir)+1+file_len:]
        print(rel_dir)
        link_path = os.path.join(pythondir,"aprilcmd",rel_dir)
        if os.path.exists(link_path):
            print("already path"+link_path)
            return
        os.symlink(dir,link_path)
        print("创建了"+link_path)
        #把link_path记录到配置文件中
        with open(ycmddir+"/aprilcmd_config.json","a") as f:
            f.write(link_path+"\n")
            return

        print("error path"+link_path)
        return
    
    #遍历目录下的所有文件，加载到root中
    for file in os.listdir(dir):
        #如果是个目录，则递归调用scan函数
        if os.path.isdir(os.path.join(dir,file)):
            scan(os.path.join(dir,file), file_len)
        #如果是个py文件，#判断当前文件相对于pythondir下的aprilcmd_xxx的目录，并在pythondir下aprilcmd目录下对应的相对位置创建一个链接
        if file[-3:] == ".py":
            rel_file = os.path.join(dir,file)[len(pythondir)+1+file_len:]
            #创建链接文件
            link_path = os.path.join(pythondir,"aprilcmd",rel_file)
            if os.path.exists(link_path):
                print("already path"+link_path)
                continue
            os.symlink(file,link_path)
            print("加载"+rel_file)
            #把文件记录到配置文件中
            with open(ycmddir+"/aprilcmd_config.json","a") as f:
                f.write(link_path+"\n")
    return


def load():
    print("load")
    #遍历pythondir
    for file in os.listdir(pythondir):
        #如果文件名是aprilcmd_开头的，并且是目录，则递归调用scan函数
        if file[:9] == "aprilcmd_" and os.path.isdir(os.path.join(pythondir,file)):
            file_len = len(file)+1
            scan(os.path.join(pythondir,file), file_len)
    

def unload():
    print("unload")
    #打开配置文件
    with open(ycmddir+"/aprilcmd_config.json","r") as f:
        lines = f.readlines()
    for line in lines:
        link_path = os.path.join(pythondir,line[:-1])
        if os.path.exists(link_path):
            print("删除"+link_path)
            os.remove(link_path)
    #清空配置文件
    with open(ycmddir+"/aprilcmd_config.json","w") as f:
        pass
