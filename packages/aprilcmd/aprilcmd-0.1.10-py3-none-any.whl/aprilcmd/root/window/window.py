from tool import *
from util import *
import sys
mod_trace(__file__)
#from root.host.items import *
from PyQt5.QtWidgets import *
def on_item_clicked(item, column):

    # 获取绑定的自定义对象
    (obj,this) = item.data(0,1)

    this.combo_box.clear()
    this.combo_box.addItems(obj._getFuncs())    

def on_button_click(this):

    this._console('Button clicked')
    this._console('Button clicked')
    (obj, this) = this.qtree.currentItem().data(0,1)
    func = this.combo_box.currentText()
    arg = this.line_edit.text()

    this._console(func)
    this._console(arg)
    cmd = "obj."+func+"("+arg+")"
    this._console(cmd)
    eval(cmd)

class Window(YModule):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.qtree = QTreeWidget()
        self.qout = QTextBrowser()
        self.combo_box = QComboBox()
        self.line_edit = QLineEdit()
        self.button = QPushButton()
        self.button.clicked.connect(lambda: on_button_click(self))

    def _console(self, log):

        if isinstance(log, list):
            dlog = json.dumps(log)
        elif isinstance(log, dict):
            dlog = json.dumps(log)
        else:
            dlog = log

        self.qout.append(dlog)
    
    @ym_getItem
    def _getItem(self, *args, **kwargs):
        type = args[0]
        return eval(type+'()')
        
    def summay(self):
        self._getroot().out = self
        self.window.setWindowTitle("april window")
        self.addroot()

        # 连接itemClicked信号到自定义槽函数
        self.qtree.itemClicked.connect(on_item_clicked)
        self.qtree.setFixedWidth(200)
        mlayout = QHBoxLayout()
        mlayout.addWidget(self.qtree)
        rlayout = QVBoxLayout()
        mlayout.addLayout(rlayout)
        self.combo_box.setFixedWidth(800)
        rlayout.addWidget(self.combo_box)
        rlayout.addWidget(self.line_edit)
        rlayout.addWidget(self.button)
        rlayout.addWidget(self.qout)
        self.window.setLayout(mlayout)
        self.window.show()
        self.app.exec()
    
    def addnode(self, parent, childobj):
			  # 添加节点
        childnode = QTreeWidgetItem(parent)
        childnode.setData(0,1, (childobj, self))
        childnode.setText(0, childobj.name)

        for i in childobj.child:
            name = i
            obj = eval('childobj.'+name)
            self.addnode(childnode, obj)

    def addroot(self):
        # 添加根节点
        # 创建QTreeWidget
        self.qtree.setColumnCount(1)  # 设置列数为1
        self.addnode(self.qtree, self._getroot())


    
    
        
