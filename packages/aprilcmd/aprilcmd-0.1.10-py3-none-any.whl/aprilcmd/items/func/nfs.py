import sys

from util import *
sys.path.append(getDir(__file__))
from base import *
sys.path.pop()


class Nfs(Function):
    def __init__(self):
        super().__init__()
        self.keys.extend(['dir'])
        self.name = "Nfs"

    def input(self):
        print("input dir")
        self.dir = input()

    def mount(self):
        pass

