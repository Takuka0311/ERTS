# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interactive_ui_result.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject


class ResultUiDialog(QObject):

    def __init__(self):
        super().__init__()
        self.result_table = None

    def setup_ui(self, result_ui_dialog):
        result_ui_dialog.setObjectName("result_ui_dialog")
        result_ui_dialog.resize(1100, 700)
        result_ui_dialog.setStyleSheet("background-color: #EBE5FF;")
        # result_ui_dialog.setStyleSheet("qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FBB8FF, stop:1 #A2E7FF);")
        self.result_table = QtWidgets.QTableWidget(result_ui_dialog)
        self.result_table.setGeometry(QtCore.QRect(70, 30, 950, 600))
        self.result_table.setObjectName("result_table")
        self.result_table.setStyleSheet("background-color: white; font: 19px;")
        self.result_table.setColumnCount(4)
        self.result_table.setRowCount(0)
        self.result_table.setHorizontalHeaderLabels(["序号", "时间", "地点", "查看视频"])
        self.result_table.horizontalHeader().setStyleSheet("background-color: white;")
        self.result_table.setColumnWidth(0, 70)
        self.result_table.setColumnWidth(1, 240)
        self.result_table.setColumnWidth(2, 490)
        self.result_table.setColumnWidth(3, 120)
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.result_table.setItem(0, 0, QtWidgets.QTableWidgetItem("1"))
        self.result_table.setItem(0, 1, QtWidgets.QTableWidgetItem("2022-05-04 16:04:00"))
        self.result_table.setItem(0, 2, QtWidgets.QTableWidgetItem("黄渡理工技术学校"))
        check_button = QtWidgets.QPushButton("查看")
        check_button.setStyleSheet(
            ''' text-align : center;
            background-color : rgb(181, 251, 232);
            height : 30px;
            font : 20px; '''
        )
        self.result_table.setCellWidget(0, 3, check_button)

        self.retranslate_ui(result_ui_dialog)
        QtCore.QMetaObject.connectSlotsByName(result_ui_dialog)

    def retranslate_ui(self, result_ui_dialog):
        _translate = QtCore.QCoreApplication.translate
        result_ui_dialog.setWindowTitle(_translate("result_ui_dialog", "检索结果"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    result_ui_dialog = QtWidgets.QDialog()
    ui = ResultUiDialog()
    ui.setup_ui(result_ui_dialog)
    result_ui_dialog.show()
    sys.exit(app.exec_())
