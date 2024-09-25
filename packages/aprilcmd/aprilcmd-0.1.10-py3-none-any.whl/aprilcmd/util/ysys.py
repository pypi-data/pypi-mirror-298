import os
import logging
import tempfile

def getDir(f):
    path = os.path.abspath(f)
    dir = os.path.dirname(path)
    return dir
    
__ysys_path=os.path.abspath(__file__)
__util_path=os.path.dirname(__ysys_path)
codePath=os.path.dirname(__util_path)
aprilPath=os.path.dirname(codePath)
pyPath=os.path.dirname(codePath)
dataPath=codePath+'/data/'
# 获取系统的临时目录
tmpPath=tempfile.gettempdir()

#logging.basicConfig(level=logging.INFO, filename=tmpPath + "/april.log")
logging.basicConfig(level=logging.DEBUG, filename=tmpPath + "/april.log")


logging.info("start==========================================================")
logging.info("aprilPath: "+aprilPath)
logging.info("pyPath: "+pyPath)
logging.info("dataPath: "+dataPath)
logging.info("tmpPath: "+tmpPath)
logging.info("codePath: "+codePath)
logging.info("INIT tool.sys")



