"""
主函数
"""

from PyQt5 import QtWidgets
from interactive_main import MyWindow
import sys
from QSSLoader import QSSLoader

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = MyWindow()

    style_file = 'style.qss'
    style_sheet = QSSLoader.read_qss_file(style_file)
    application.setStyleSheet(style_sheet)

    application.show()
    sys.exit(app.exec())

