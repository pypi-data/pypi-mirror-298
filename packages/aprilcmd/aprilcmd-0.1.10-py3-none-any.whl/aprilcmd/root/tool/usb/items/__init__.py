import os,sys

thisfile=os.path.abspath(__file__)
thisdir=os.path.dirname(thisfile)

sys.path.append(thisdir)
for file in os.listdir(thisdir):
    if file == "__init__.py" or file == "__pycache__":
        continue
    if file.endswith(".py"):
        file = file[:-3]
        exec("from "+file+" import *")
sys.path.pop()


