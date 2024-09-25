from util import *

class UsbManger(YManager):
    def __init__(self):
        super().__init__()
        self.name = "usb"
        self.type = "Usbs"
        pass
        
    def check(self):     
        try:
            import usb
            import usb.core
        except:
            self._console("usb checking ...false")
            self._console("need libusb run pip install pyusb")
            return False

        self._info("usb checking ...true")
        return True

manager = UsbManger()

