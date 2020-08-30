#!/usr/bin/env python

from bluepy.btle import UUID, Peripheral, DefaultDelegate
import struct
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from bluetooth_ui import Ui_bluetooth
from UDPBeep import udpbeep

class MyDelegate(DefaultDelegate):
    # Constructor (run once on startup)
    def __init__(self, params, temp_sig, wind_sig):
        DefaultDelegate.__init__(self)
        self.ble_device = params
        self.temp_sig = temp_sig
        self.wind_sig = wind_sig

    # func is called on notifications
    def handleNotification(self, cHandle, data):
        #print("Notification from Handle: 0x" + format(cHandle, '02X') + ", len: " + str(len(data)) + ", Value: " + str(data))
        data_list = list(data)
        data_str = []
        if len(data_list) == 19:
            for i in data_list:
                data_str.append(hex(i).replace("0x", ""))
            function = data_str[4]
            real_time_unit_text = data_str[14]
            value = str(float(data[5:11].decode("utf-8")))
            print(value)
            if function == "30": #temperature
                if value.find("L") == -1:
                    if real_time_unit_text=="30": #°C
                        self.temp_sig.emit(value, "°C")
                    elif real_time_unit_text=="31": #°F
                        self.temp_sig.emit(str(float(value)*1.8+32), "°F")
            elif function == "37": #wind
                if value.find("L") == -1:
                    if real_time_unit_text == "34": #m/s
                        self.wind_sig.emit(value, "m/s")
                    elif real_time_unit_text == "35": #km/h
                        self.wind_sig.emit(str(float(value)*3.6), "km/h")
                    elif real_time_unit_text == "36": #ft/min
                        self.wind_sig.emit(str(float(value)*196.85), "ft/min")
                    elif real_time_unit_text == "37": #knots
                        self.wind_sig.emit(str(float(value)*1.943), "knots")
                    elif real_time_unit_text == "38": #mph
                        self.wind_sig.emit(str(float(value)*2.237), "mph")



class ble_UT363 (QObject):
    CCCD = "00002902-0000-1000-8000-00805f9b34fb"
    UUID_HEART_RATE_MEASUREMENT = "00002a37-0000-1000-8000-00805f9b34fb"
    WX_SERVICE_UUID = "0000ff12-0000-1000-8000-00805f9b34fb"
    WX_CHAR_UUID = "0000FF01-0000-1000-8000-00805f9b34fb"
    WX_NOTIFICATION_UUID = "0000FF02-0000-1000-8000-00805f9b34fb"
    wind_sig = pyqtSignal(str, str)
    temp_sig = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.UT363 = None
        self.udp = udpbeep("192.168.1.251", 4445)
        print(self.udp)
        self.wind_sig.connect(self.send_udpwind)
        self.timerRx = QtCore.QTimer(self)
        self.timerRx.timeout.connect(self.writeRxCharacteristic)

    def disconnect(self):
        self.timerRx.stop()
        self.UT363.disconnect()
        self.UT363 = None

    def connect(self, address):
        self.UT363 = Peripheral(address)
        if self.UT363:
            self.UT363.setDelegate(MyDelegate(self.UT363, self.temp_sig, self.wind_sig))
            self.enableTxNotification()
            self.timerRx.start(800)

    def enableTxNotification(self):
        RxService = self.UT363.getServiceByUUID(self.WX_SERVICE_UUID)
        if RxService:
            TxChar = RxService.getCharacteristics(self.WX_NOTIFICATION_UUID)[0]
            if TxChar:
                TxChar.write(struct.pack('<B', True))

    def writeRxCharacteristic(self):
        RxService = self.UT363.getServiceByUUID(self.WX_SERVICE_UUID)
        if RxService:
            RxChar = RxService.getCharacteristics(self.WX_CHAR_UUID)[0]
            if RxChar:
                RxChar.write(struct.pack('<B', 0x5e))

    def send_udpwind(self, value, unit):
        msg = "wind -1 " + value + " " + unit
        #print(msg)
        self.udp.sendData(msg)

    def isconnected(self):
        return self.UT363 is not None

    def get_device_info(self):
        services = self.UT363.getServices()
        for service in services:
            print(service, "UUID : ", service.uuid)

        chList = self.UT363.getCharacteristics()
        print("Handle   UUID                                Properties")
        print("-------------------------------------------------------")
        for ch in chList:
            print("  0x" + format(ch.getHandle(), '02X') + "   " + str(ch.uuid) + " " + ch.propertiesToString())

        descriptors = self.UT363.getDescriptors(1, 0x00F)  # Bug if no limt is specified the function wil hang
        # (go in a endless loop and not return anything)
        print("UUID                                  Handle UUID by name")
        for descriptor in descriptors:
            print(" " + str(descriptor.uuid) + "  0x" + format(descriptor.handle, "02X") + "   " + str(descriptor))


class WindowsTest(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_bluetooth()
        self.ui.setupUi(self.MainWindow)
        self.ui.buttonConnect.clicked.connect(self.connect)
        self.ui.buttonDisconnect.clicked.connect(self.disconnect)
        self.ui.buttonQuit.clicked.connect(exit)
        self.ble = ble_UT363()
        self.ble.wind_sig.connect(self.display_wind)
        self.ble.temp_sig.connect(self.display_temp)
        self.display_temp(" -- ", " -- ")
        self.display_wind(" -- ", " -- ")
        self.MainWindow.show()

    def disconnect(self):
        self.ble.disconnect()
        self.display_temp(" -- ", " -- ")
        self.display_wind(" -- ", " -- ")

    def connect(self):
        if not self.ble.isconnected():
            self.ble.connect(self.ui.btaddress.text())
        return self.ble.isconnected()

    def display_temp(self, str_value, unit):
        self.ui.temp_value.setText(str_value)
        self.ui.temp_unit.setText(unit)

    def display_wind(self, str_value, unit):
        self.ui.wind_value.setText(str_value)
        self.ui.wind_unit.setText(unit)


if __name__ == '__main__':
    import sys
    import subprocess
    import shlex
    import getpass



    app = QtWidgets.QApplication(sys.argv)

    windows = WindowsTest()
    sys.exit(app.exec())

    #YOUR_DEVICE_ADDRESS = "50:33:8B:12:68:E5"

