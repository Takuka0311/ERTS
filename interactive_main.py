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
import json
import sys

from data_main import DataMain
from interactive_ui import UiMainWindow
from interactive_ui_result import ResultUiDialog

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QDialog, QMessageBox
from PIL import Image

import cgitb

cgitb.enable(format='text')


class MyWindow(QtWidgets.QMainWindow):

    def __init__(self):
        self.image_path = ""
        self.video_path = []
        self.model_id = 0
        self.result_path = ""
        self.result_check_button = ResultDialog()

        super(MyWindow, self).__init__()
        self.myCommand = " "
        self.ui = UiMainWindow()
        self.ui.setup_ui(self)

        self.init()

        self.ui.upload_photo_button.clicked.connect(self.open_image)
        self.ui.upload_video_button.clicked.connect(self.open_video)
        self.ui.start_search_button.clicked.connect(self.start_search)
        self.ui.check_result_button.clicked.connect(self.check_result)
        self.ui.comboBox.activated.connect(self.change_model)

    # 初始化
    def init(self):
        # 初始化界面
        self.ui.search_progress_label.setText(QtCore.QCoreApplication.translate("ui_main_window", "等待检索"))
        self.ui.progressBar.setProperty("value", 0)
        self.ui.check_result_button.setEnabled(False)

        # 初始化模型
        obj = json.load(open('model.json'))
        model_num = obj["num"]
        model_arr = obj["array"]
        print("model num:", model_num, "model list:", model_arr)

        if model_num != 0:
            self.model_id = model_arr[0]["id"]
        for i in range(model_num):
            item = model_arr[i]
            self.ui.accuracy_table.setItem(i, 0, QtWidgets.QTableWidgetItem(item["id"]))
            self.ui.accuracy_table.setItem(i, 1, QtWidgets.QTableWidgetItem(item["acc"]))
            self.ui.accuracy_table.setItem(i, 2, QtWidgets.QTableWidgetItem(item["note"]))
            self.ui.comboBox.addItem("模型" + item["id"])

    # 开始 搜索/训练
    def start_search(self):
        # 准备识别
        image_path = self.image_path
        video_path = self.video_path
        model_id = self.model_id
        if image_path == "":
            QMessageBox.information(self, "提示", "请选择要识别的目标图片", QMessageBox.Yes)
            return
        if not video_path :
            QMessageBox.information(self, "提示", "请添加至少一个视频", QMessageBox.Yes)
            return

        # 开始识别
        self.ui.search_progress_label.setText(QtCore.QCoreApplication.translate("ui_main_window", "检索中..."))
        print("search start!\nimage path:", image_path, "\nvideo_path:", video_path, "\nmodel_id:", model_id)
        data_class = DataMain()
        data_class.video_path = ["./test/食堂_20220515085959.mp4"]
        data_class.output_path = "./test/"
        data_class.execute()
        self.result_path = "./test/食堂1"

        # 识别完成
        QMessageBox.information(self, "提示", "识别完成！", QMessageBox.Yes)
        self.ui.search_progress_label.setText(QtCore.QCoreApplication.translate("ui_main_window", "检索完成"))
        self.ui.progressBar.setProperty("value", 100)
        self.ui.check_result_button.setEnabled(True)

    # 打开结果界面
    def check_result(self):
        self.result_check_button.set_path(self.result_path)
        self.result_check_button.exec()

    # 修改模型
    def change_model(self):
        combobox_id = self.ui.comboBox.currentText()
        self.model_id = int(combobox_id[2:])

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

    def set_path(self, result_path):
        image_list = os.listdir(result_path)
        image_list.sort(key=lambda x: int(x.split('.')[0]))

        for count in range(0, len(image_list)):
            im_name = image_list[count]
            im_path = os.path.join(result_path, im_name)

            row_count = self.ui.result_table.rowCount()
            self.ui.result_table.insertRow(row_count)
            self.ui.result_table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(str(row_count)))
            self.ui.result_table.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(im_name.split('.')[0])))
            self.ui.result_table.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(result_path.split('/')[-1])))
            check_button = QtWidgets.QPushButton("查看")
            check_button.setStyleSheet(
                ''' text-align : center;
                background-color : rgb(181, 251, 232);
                height : 30px;
                font : 20px; '''
            )
            check_button.clicked.connect(lambda: self.check_image(im_path))
            self.ui.result_table.setCellWidget(row_count, 3, check_button)

    @staticmethod
    def check_image(im_path):
        image = Image.open(im_path)
        image.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()
    sys.exit(app.exec())
