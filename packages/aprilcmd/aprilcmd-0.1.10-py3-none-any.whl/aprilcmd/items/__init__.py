import os,sys

thisfile=os.path.abspath(__file__)
thisdir=os.path.dirname(thisfile)
sys.path.insert(0,thisdir)

classes = {}
M_module = {}

def list_overlap(list1, list2):
    #return any(item in list2 for item in list1)
    return bool(set(list1) & set(list2))

def getClass(name, tags = []):
    c = classes[name]
    if not hasattr(c,'C_tags') or list_overlap(c.C_tags, tags):
        return c
    return None

for file in os.listdir(thisdir):
    if file == "__init__.py" or file == "__pycache__":
        continue

    '''
        exec("from "+file+" import *")
    '''
    if not os.path.exists(thisdir+'/'+file+'/__init__.py'):
        continue

    import importlib
    import inspect
    try:
        module = importlib.import_module(file)
        classes.update(module.M_classes)
        M_module[file] = module

    except:
        import traceback
        import logging
        tb = traceback.format_exc()
        logging.info("unexpect item "+file+'\n'+tb)

sys.path.remove(thisdir)
