
from util import *
class Link(YModule):
    keys = {**{
        'link':None,
    },**YModuleItem.keys}
    def __init__(self):
        super().__init__()

    def _type(self):
        return Link

    def _listHead():
        return ['name', 'link']

    def _listItem(self):
        return [self.name, self.link]

    def _getkey(self, key):
        if key == 'link':
            return self[self.link]
        else:
            return super()._getkey(key)
