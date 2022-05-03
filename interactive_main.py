"""
交互界面主函数
主要包括主窗口类MyWindow。
该模块中，设计ui部分都在interactive_ui.ui和interactive_ui.py中实现，其余部分（信号与槽等）在interactive_interface.py中实现。
设计ui方法：
1、配置可视化ui设计工具
    pycharm配置pyqt5-tools开发环境的方法步骤https://www.jb51.net/article/156026.htm
    关于安装Pyqt5-tools后找不到designer.exe的解决方法https://blog.csdn.net/wujiabao123/article/details/118271573
2、使用QtDesigner打开interactive_ui.ui进行编辑
3、保存interactive_ui.ui并将其转换成interactive_ui.py。注：Qt转换的python文件格式不够规范，后续考虑统一进行调整
"""
from PyQt5 import QtWidgets
import sys
import interactive_interface
from interactive_ui import Ui_UiMainWindow


class MyWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_UiMainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()
    sys.exit(app.exec())
