# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interactive_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UiMainWindow(object):
    def setupUi(self, UiMainWindow):
        UiMainWindow.setObjectName("UiMainWindow")
        UiMainWindow.resize(400, 300)

        self.retranslateUi(UiMainWindow)
        QtCore.QMetaObject.connectSlotsByName(UiMainWindow)

    def retranslateUi(self, UiMainWindow):
        _translate = QtCore.QCoreApplication.translate
        UiMainWindow.setWindowTitle(_translate("UiMainWindow", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UiMainWindow = QtWidgets.QWidget()
    ui = Ui_UiMainWindow()
    ui.setupUi(UiMainWindow)
    UiMainWindow.show()
    sys.exit(app.exec_())
