import os,sys

thisfile=os.path.abspath(__file__)
thisdir=os.path.dirname(thisfile)
sys.path.append(thisdir)

M_classes = {}
M_tags = ['_base']
M_path = "./items/func"

for file in os.listdir(thisdir):
    if file == "__init__.py" or file == "__pycache__":
        continue
    
    if file.endswith(".py"):
        file = file[:-3]
    else:
        continue


    '''
        exec("from "+file+" import *")
    '''
    import importlib
    import inspect
    try:
        module = importlib.import_module(file)
        
        # 假设你想从每个模块中导入所有类
        # 使用inspect模块来检查模块中的所有成员，并找出类
        for name, obj in inspect.getmembers(module):
            # 检查是否为类（假设我们忽略内置的和新式类）
            if inspect.isclass(obj) and obj.__module__ == module.__name__:
                # 如果找到类，则将其添加到数组中
                M_classes[name] = obj
    except:
        import traceback
        import logging
        tb = traceback.format_exc()
        logging.info("unexpect item "+file+'\n'+tb)

sys.path.pop()
