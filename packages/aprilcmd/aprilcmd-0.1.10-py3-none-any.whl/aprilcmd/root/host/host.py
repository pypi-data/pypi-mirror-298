from util import *
mod_trace(__file__)


class Hosts(YModuleListWithConf):
    def __init__(self):
        super().__init__('host.config')

'''
    @ym_getItem
    def _getItem(self, *args, **kwargs):
        type = args[0]
        return eval(type+'()')

'''
        
    
    
        