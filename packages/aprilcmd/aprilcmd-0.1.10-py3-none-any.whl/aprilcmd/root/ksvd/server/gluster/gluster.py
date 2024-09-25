from tool import *
from util import *

class Gluster(YModule):
    def __init__(self):
        self.volumes = {}
        self.ByName = {}

        try:
            (status, output) = commands.getstatusoutput('gluster volume info');
            volumeList = output.split("\n \n")
            #print volumeList
            for volumeText in volumeList:
            #	print "getconf:", volumeText
                volume = gfs_volume.GfsVolume()
                volume.gettext(volumeText)
                self.volumes[volume.id] = volume
                self.ByName[volume.name] = volume
        except:
            print("no gfs")


    def summay(self):
        print("gluster:")
        for id in self.volumes:
            print(id)
            self.volumes[id].summay()


