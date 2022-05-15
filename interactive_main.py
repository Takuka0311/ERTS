"""
交互界面主函数
主要包括主窗口类MyWindow。
该模块中，设计ui部分都在interactive_ui.ui和interactive_ui.py中实现，其余部分（信号与槽等）在interactive_interface.py中实现。
设计ui方法：
1、配置可视化ui设计工具
    pycharm配置pyqt5-tools开发环境的方法步骤https://www.jb51.net/article/156026.htm
2、使用QtDesigner打开interactive_ui.ui进行编辑
3、保存interactive_ui.ui并将其转换成interactive_ui.py。注：Qt转换的python文件格式不够规范，后续考虑统一进行调整
"""
import os

from PyQt5 import QtWidgets
import sys

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QDialog, QMessageBox

from data_main import DataMain
from interactive_ui import UiMainWindow
from interactive_ui_result import ResultUiDialog

from PIL import Image

import cgitb
cgitb.enable(format='text')


class MyWindow(QtWidgets.QMainWindow):

    def __init__(self):
        self.image_path = ""
        self.video_path = []
        self.model_id = 0
        self.result_check_button = ResultDialog()

        super(MyWindow, self).__init__()
        self.myCommand = " "
        self.ui = UiMainWindow()
        self.ui.setup_ui(self)

        self.ui.upload_photo_button.clicked.connect(self.open_image)
        self.ui.upload_video_button.clicked.connect(self.open_video)
        self.ui.start_search_button.clicked.connect(self.start_search)
        self.ui.check_result_button.clicked.connect(self.check_result)

    # 开始 搜索/训练
    def start_search(self):
        image_path = self.image_path
        video_path = self.video_path
        model_id = self.model_id
        print(image_path, video_path, model_id)

        data_class = DataMain()
        data_class.image_set_path(image_path)
        data_class.video_path = video_path
        data_class.output_path = "C:/Vscode/"

    # 打开结果界面
    def check_result(self):
        self.result_check_button.exec()

    # 选中图片
    def open_image(self):
        img_name, img_type = QFileDialog.getOpenFileName(self, "Open Image File", "", "*.jpg;;*.png;;*.jpeg;;*.tiff")
        if img_name != "":
            # 生成预览图
            img = Image.open(img_name)
            img = img.resize((self.ui.photo.width() - 5, self.ui.photo.height() - 5), Image.ANTIALIAS)
            img.save("Preview.png", 'png')
            # 设置预览图
            pix = QPixmap.fromImage(QImage("Preview.png"))
            item = QGraphicsPixmapItem(pix)
            scene = QGraphicsScene()
            scene.addItem(item)
            self.ui.photo.setScene(scene)
            self.image_path = img_name
            # 善后
            print("load success", img_name)
            os.remove("Preview.png")

    # 选中视频
    def open_video(self):
        video_name, _ = QFileDialog.getOpenFileName(self, "Open video File", "*.mp4")
        for i in range(self.ui.video_table.rowCount()):
            if self.ui.video_table.item(i, 0):
                if video_name == self.ui.video_table.item(i, 0).text():
                    QMessageBox.information(self, "提示", "请不要重复导入视频", QMessageBox.Yes)
                    return

        if video_name != "":
            self.video_path.append(video_name)
            row_count = self.ui.video_table.rowCount()
            self.ui.video_table.insertRow(row_count)
            self.ui.video_table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(str(video_name)))
            delete_button = QtWidgets.QPushButton(self.ui.video_table)
            delete_button.setText("删除")
            delete_button.clicked.connect(lambda: self.delete_video(video_name))
            delete_button.setStyleSheet(
                ''' text-align : center;
                background-color : LightCoral;
                height : 25px;
                font : 20px; '''
            )
            self.ui.video_table.setCellWidget(row_count, 1, delete_button)

    # 删除某一视频
    def delete_video(self, video_name):
        for i in range(self.ui.video_table.rowCount()):
            if self.ui.video_table.item(i, 0):
                if video_name == self.ui.video_table.item(i, 0).text():
                    self.ui.video_table.removeRow(i)
                    self.video_path.remove(video_name)
                    break


class ResultDialog(QDialog):
    def __init__(self):
        super(ResultDialog, self).__init__()
        self.ui = ResultUiDialog()
        self.ui.setup_ui(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()
    sys.exit(app.exec())
