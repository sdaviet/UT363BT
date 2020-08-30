# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bluetooth.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_bluetooth(object):
    def setupUi(self, bluetooth):
        bluetooth.setObjectName("bluetooth")
        bluetooth.resize(336, 129)
        self.centralwidget = QtWidgets.QWidget(bluetooth)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.wind_unit = QtWidgets.QLabel(self.centralwidget)
        self.wind_unit.setObjectName("wind_unit")
        self.gridLayout_2.addWidget(self.wind_unit, 0, 3, 1, 1)
        self.temp_unit = QtWidgets.QLabel(self.centralwidget)
        self.temp_unit.setObjectName("temp_unit")
        self.gridLayout_2.addWidget(self.temp_unit, 1, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)
        self.temp_value = QtWidgets.QLabel(self.centralwidget)
        self.temp_value.setObjectName("temp_value")
        self.gridLayout_2.addWidget(self.temp_value, 1, 2, 1, 1)
        self.wind_value = QtWidgets.QLabel(self.centralwidget)
        self.wind_value.setObjectName("wind_value")
        self.gridLayout_2.addWidget(self.wind_value, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 4, 1, 1, 1)
        self.buttonDisconnect = QtWidgets.QPushButton(self.centralwidget)
        self.buttonDisconnect.setObjectName("buttonDisconnect")
        self.gridLayout_2.addWidget(self.buttonDisconnect, 2, 3, 1, 1)
        self.buttonConnect = QtWidgets.QPushButton(self.centralwidget)
        self.buttonConnect.setObjectName("buttonConnect")
        self.gridLayout_2.addWidget(self.buttonConnect, 2, 2, 1, 1)
        self.btaddress = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btaddress.sizePolicy().hasHeightForWidth())
        self.btaddress.setSizePolicy(sizePolicy)
        self.btaddress.setObjectName("btaddress")
        self.gridLayout_2.addWidget(self.btaddress, 2, 1, 1, 1)
        self.buttonQuit = QtWidgets.QPushButton(self.centralwidget)
        self.buttonQuit.setObjectName("buttonQuit")
        self.gridLayout_2.addWidget(self.buttonQuit, 3, 1, 1, 3)
        bluetooth.setCentralWidget(self.centralwidget)

        self.retranslateUi(bluetooth)
        QtCore.QMetaObject.connectSlotsByName(bluetooth)

    def retranslateUi(self, bluetooth):
        _translate = QtCore.QCoreApplication.translate
        bluetooth.setWindowTitle(_translate("bluetooth", "UT363 BT"))
        self.wind_unit.setText(_translate("bluetooth", "TextLabel"))
        self.temp_unit.setText(_translate("bluetooth", "TextLabel"))
        self.label_5.setText(_translate("bluetooth", "Temp."))
        self.label_2.setText(_translate("bluetooth", "Wind Speed"))
        self.temp_value.setText(_translate("bluetooth", "TextLabel"))
        self.wind_value.setText(_translate("bluetooth", "TextLabel"))
        self.buttonDisconnect.setText(_translate("bluetooth", "Disconnect"))
        self.buttonConnect.setText(_translate("bluetooth", "Connect"))
        self.btaddress.setText(_translate("bluetooth", "50:33:8B:12:68:E5"))
        self.buttonQuit.setText(_translate("bluetooth", "Quit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    bluetooth = QtWidgets.QMainWindow()
    ui = Ui_bluetooth()
    ui.setupUi(bluetooth)
    bluetooth.show()
    sys.exit(app.exec_())