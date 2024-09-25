from tool import *
mod_trace("Test")
class Test(YModule):
    def __init__(self):

        super().__init__()
        pass

    def summay(self):
        print("up path");


    def test(self, a, b, c):
        webbrowser.open_new("http://192.168.120.30:8080/view/KSVD%E6%9C%8D%E5%8A%A1%E7%AB%AF%E5%B7%A5%E7%A8%8B%E5%8D%95%E7%8B%AC%E7%BC%96%E8%AF%91/job/uniqb_back_module/")
        print(self, a, b, c);
    
    def freadf(self, *args, **kwargs):
        file=args[0]
        with open(file) as fo:
            print("open file success")
            for line in fo.readlines():
                obj = re.match(r'.*myfio\ ([a-z]*)\ ([\da-z]*)\ ([\d]*).*', line)
                if obj:
                    print(obj.group(1)+" "+obj.group(2)+" "+obj.group(3))
                obj = re.match(r'.*bw=([^,]*),.*',line)
                if obj:
                    print("bw:"+obj.group(1))
                obj = re.match(r'.*IOPS=([\d]*).*',line)
                if obj:
                    print("IOPS:"+obj.group(1),end=' ')
                

    @parse_args
    def test1(self, **kwargs):
        print(type(self))
        this = dir(self)
        print(this)
        print(type(self))
        print(self.name)
        print(type(self.name))
        print(type(self.test1))

    @parse_args
    def test2(self, **kwargs):
        import pyautogui

        # 获取屏幕的宽高
        screen_width, screen_height = pyautogui.size()

        # 设置程序窗口大小和位置
        program_width = int(screen_width * 0.8)
        program_height = int(screen_height * 0.8)
        pyautogui.moveTo(0, 0)
        pyautogui.dragTo(program_width, program_height, duration=1)

        # 创建虚拟屏幕以外的区域
        virtual_screen_x = program_width
        virtual_screen_y = 0
        virtual_screen_width = screen_width - program_width
        virtual_screen_height = screen_height
        pyautogui.moveTo(virtual_screen_x, virtual_screen_y)
        pyautogui.dragTo(screen_width, virtual_screen_height, duration=1)

