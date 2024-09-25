from util import *

class Qemu(YModule):
    def __init__(self):
        self.web = None
        try:
            self.web = RWeb.web.webByName['jenkins_30']
        except:
            print("web not found")
            self.disable()
        pass

    def __down(self):
        self.web.getPageByStr("/view/Qemu-Spice%E5%A4%9A%E5%B9%B3%E5%8F%B0%E7%BC%96%E8%AF%91/job/qemu_kvm_ksvd_build_inner/1121/artifact/*zip*/archive.zip")

    def down(self, arg):
        self.__down()
        os.system("mv archive.zip "+arg)

    def summay(self):
        if not self.is_enable:
            print("not enable")
            return

        print("===func===")
        print("down")
