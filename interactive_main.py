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
import math

from PyQt5 import QtWidgets
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene, QGraphicsPixmapItem

import interactive_interface
from interactive_ui import UiMainWindow
from interactive_ui_result import ResultUiDialog


class MyWindow(QtWidgets.QMainWindow):

    def __init__(self):
        self.image_path=""
        # self.result_check = ResultUiDialog()
        super(MyWindow, self).__init__()
        self.myCommand = " "
        self.ui = UiMainWindow()
        self.ui.setup_ui(self)

        self.ui.upload_photo_button.clicked.connect(self.open_image)
        self.ui.upload_video_button.clicked.connect(self.open_video)
        self.ui.start_search_button.clicked.connect(self.start_search)
        # self.ui.check_result_button.clicked.connect(self.check_result)

    # 开始 搜索/训练
    def start_search(self):
        image_path = self.image_path
        video_path = []
        for i in range(self.ui.video_table.rowCount()):
            if self.ui.video_table.item(i, 1):
                video_path.append(self.ui.video_table.item(i, 1).text())
        print(image_path, video_path)

    # def check_result(self):
        # self.result_check.show()

    # 选中图片
    def open_image(self):
        img_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "*.jpg;;*.png;;*.jpeg")
        self.image_path = img_name
        print(img_name)
        pix = QPixmap(img_name).scaled(math.floor(QPixmap(img_name).width()*self.ui.photo.width()/QPixmap(img_name).height()), self.ui.photo.height()-25)
        item = QGraphicsPixmapItem(pix)
        scene = QGraphicsScene()
        scene.addItem(item)
        self.ui.photo.setScene(scene)

    # 选中视频
    def open_video(self):
        video_name, _ = QFileDialog.getOpenFileName(self, "Open video File", "*.mp4")
        row_count = self.ui.video_table.rowCount()
        self.ui.video_table.insertRow(row_count)
        self.ui.video_table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(str(row_count)))
        self.ui.video_table.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(video_name)))
        delete_button = QtWidgets.QPushButton(self.ui.video_table)
        delete_button.setText("删除")
        # delete_button.clicked.connect(self.delete_video(row_count))
        delete_button.setStyleSheet(
            ''' text-align : center;
            background-color : LightCoral;
            height : 25px;
            font : 20px; '''
        )
        self.ui.video_table.setCellWidget(row_count, 2, delete_button)

    # 删除某一视频
    def delete_video(self, row_count):
        print("break")
        self.ui.video_table.removeRow(row_count)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = MyWindow()
    result_check = ResultUiDialog()
    application.ui.check_result_button.clicked.connect(result_check.show)
    application.show()
    sys.exit(app.exec())
