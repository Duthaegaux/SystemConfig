from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QVBoxLayout,QLabel
from PyQt6.QtCore import pyqtSignal
import sys
import os
import wmi
from check import *

pc = wmi.WMI()


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.w2, self.w3, self.w4, self.w5, self.w6 = None, None, None, None, None
        font = QtGui.QFont("Rubik", 11)
        resx = 0
        resy = 0

        self.setWindowTitle("SystemConfig")
        for i in pc.Win32_VideoController():
            resx = i.CurrentHorizontalResolution
            resy = i.CurrentVerticalResolution
        self.setGeometry((resx - 344) // 2, (resy - 190) // 2, 344, 190)
        self.setMinimumSize(344, 190)
        self.setMaximumSize(344, 190)
        self.setWindowIcon(QtGui.QIcon(resource_path("sysconf.ico")))

        self.ost = ClickedLabel(self)
        self.ost.setText("OS")
        self.ost.setFont(font)
        self.ost.move(50, 79)
        self.ost.clicked.connect(lambda: self.chk(0))

        self.os = ClickedLabel(self)
        self.os.setGeometry(30, 20, 64, 64)
        self.os.setPixmap(QtGui.QPixmap(resource_path("os.png")))
        self.os.clicked.connect(lambda: self.chk(0))

        self.cput = ClickedLabel(self)
        self.cput.setText("CPU(S)")
        self.cput.setFont(font)
        self.cput.move(147, 85)
        self.cput.adjustSize()
        self.cput.clicked.connect(lambda: self.chk(1))

        self.cpu = ClickedLabel(self)
        self.cpu.setGeometry(140, 20, 64, 64)
        self.cpu.setPixmap(QtGui.QPixmap(resource_path("cpu.png")))
        self.cpu.clicked.connect(lambda: self.chk(1))

        self.gput = ClickedLabel(self)
        self.gput.setText("GPU(S)")
        self.gput.setFont(font)
        self.gput.move(258, 85)
        self.gput.adjustSize()
        self.gput.clicked.connect(lambda: self.chk(2))

        self.gpu = ClickedLabel(self)
        self.gpu.setGeometry(250, 20, 64, 64)
        self.gpu.setPixmap(QtGui.QPixmap(resource_path("gpu.png")))
        self.gpu.clicked.connect(lambda: self.chk(2))

        self.ramt = ClickedLabel(self)
        self.ramt.setText("RAM")
        self.ramt.setFont(font)
        self.ramt.move(101, 164)
        self.ramt.adjustSize()
        self.ramt.clicked.connect(lambda: self.chk(3))

        self.ram = ClickedLabel(self)
        self.ram.setGeometry(85, 105, 64, 64)
        self.ram.setPixmap(QtGui.QPixmap(resource_path("ram.png")))
        self.ram.clicked.connect(lambda: self.chk(3))

        self.diskt = ClickedLabel(self)
        self.diskt.setText("Disk(S)")
        self.diskt.setFont(font)
        self.diskt.move(203, 164)
        self.diskt.adjustSize()
        self.diskt.clicked.connect(lambda: self.chk(4))

        self.disk = ClickedLabel(self)
        self.disk.setGeometry(195, 105, 64, 64)
        self.disk.setPixmap(QtGui.QPixmap(resource_path("disk.png")))
        self.disk.clicked.connect(lambda: self.chk(4))

    def returnOS(self):
        try:
            os = []
            for x in pc.Win32_OperatingSystem():
                os.append(f"OS --- {x.Caption}")
                os.append(f"    OS Architecture --- {x.OSArchitecture}")
                os.append(f"    Version --- {x.Version}")
                os.append(f"    System On Disk --- {x.SystemDrive}")
            return tuple(os)
        except:
            return "Sorry, but something went wrong :(", \
                   f"An error occured while attempting to returnOS"

    def returnProcessor(self):
        try:
            processors = []
            counter = 1
            for x in pc.Win32_Processor():
                processors.append(f"Processor {counter} --- {x.Name}")
                processors.append(f"    Socket --- {x.SocketDesignation}")
                processors.append(f"    Core(s) --- {x.NumberOfCores}")
                processors.append(f"    Thread(s) --- {x.NumberOfLogicalProcessors}")
                counter += 1
            return tuple(processors)
        except:
            return "Sorry, but something went wrong :(", \
                   f"An error occured while attempting to returnProcessor"

    def returnGraphics(self):
        try:
            graphics = []
            counter = 1
            for x in pc.Win32_VideoController():
                graphics.append(f"Graphics card {counter} --- {x.Caption}")
                graphics.append(f"    Video memory (Up to 4GB) --- {converted_ctypes(x.AdapterRAM, c_uint32=1)} GB")
                graphics.append(
                    f"    Resolution --- {x.CurrentHorizontalResolution} x {x.CurrentVerticalResolution}")
                graphics.append(f"    Current refresh rate --- {x.CurrentRefreshRate} Hz")
                counter += 1
            return tuple(graphics)
        except:
            return "Sorry, but something went wrong :(", \
                   f"An error occured while attempting to returnGraphics"

    def returnRAM(self):
        try:
            rams = []
            counter = 1
            for x in pc.Win32_PhysicalMemory():
                if x.Capacity is not None:
                    rams.append(f"RAM {counter} --- {x.Manufacturer} {x.PartNumber}")
                    rams.append(f"    Size --- {converted_ctypes(x.Capacity, c_uint64=1)} GB")
                    rams.append(f"    Clock Speed --- {x.ConfiguredClockSpeed} MHz")
                    rams.append(f"    Voltage --- {convert_ctypes(x.ConfiguredVoltage, c_uint32=1)} mV")
                    counter += 1
            return tuple(rams)
        except:
            return "Sorry, but something went wrong :(", \
                   f"An error occured while attempting to returnRAM"

    def returnStorage(self):
        try:
            storages = []
            for x in pc.Win32_LogicalDisk():
                storages.append(f"Disk {x.Caption}")
                storages.append(f"    File System --- {x.FileSystem}")
                storages.append(f"    Size --- {converted_ctypes(x.Size, c_uint64=1)} GB")
                storages.append(f"    Free Space --- {converted_ctypes(x.FreeSpace, c_uint64=1)} GB")
            return tuple(storages)
        except:
            return "Sorry, but something went wrong :(", \
                   f"An error occured while attempting to returnStorage"

    def createFile(self):
        with open("configuration.txt", "w", encoding="utf-8") as f:
            for i in self.returnOS():
                f.write(i + "\n")
            for i in self.returnProcessor():
                f.write(i + "\n")
            for i in self.returnGraphics():
                f.write(i + "\n")
            for i in self.returnRAM():
                f.write(i + "\n")
            for i in self.returnStorage():
                f.write(i + "\n")

    def showAll(self):
        for i in self.returnOS():
            print(i)
        for i in self.returnProcessor():
            print(i)
        for i in self.returnGraphics():
            print(i)
        for i in self.returnRAM():
            print(i)
        for i in self.returnStorage():
            print(i)

    def chk(self, part):
        if part == 0:
            if self.w2 is None:
                self.w2 = Osif()
                self.w2.show()
            else:
                self.w2.close()
                self.w2 = None
        elif part == 1:
            if self.w3 is None:
                self.w3 = Cpuif()
                self.w3.show()
            else:
                self.w3.close()
                self.w3 = None
        elif part == 2:
            if self.w4 is None:
                self.w4 = Gpuif()
                self.w4.show()
            else:
                self.w4.close()
                self.w4 = None
        elif part == 3:
            if self.w5 is None:
                self.w5 = Ramif()
                self.w5.show()
            else:
                self.w5.close()
                self.w5 = None
        elif part == 4:
            if self.w6 is None:
                self.w6 = Diskif()
                self.w6.show()
            else:
                self.w6.close()
                self.w6 = None


class ClickedLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.clicked.emit()


class Osif(QWidget):
    def __init__(self):
        super().__init__()

        resx1 = 0
        resy1 = 0

        for i in pc.Win32_VideoController():
            resx1 = i.CurrentHorizontalResolution
            resy1 = i.CurrentVerticalResolution

        self.setGeometry((resx1 - 344) // 2 - 344, (resy1 - 190) // 2 - 190, 344, 190)
        self.setMinimumSize(344, 190)
        self.setMaximumSize(344, 190)
        self.setWindowTitle("OS info")
        self.setWindowIcon(QtGui.QIcon(resource_path("os.png")))

        layout = QVBoxLayout()
        self.inf1 = QtWidgets.QPlainTextEdit()
        self.inf1.setReadOnly(True)
        self.inf1.setGeometry(0, 0, 344, 190)
        layout.addWidget(self.inf1)

        self.info()

        self.setLayout(layout)

    def info(self):
        try:
            for x in pc.Win32_OperatingSystem():
                self.inf1.appendPlainText(f"{x.Caption}")
                self.inf1.appendPlainText(f"    OS Architecture --- {x.OSArchitecture}")
                self.inf1.appendPlainText(f"    Version --- {x.Version}")
                self.inf1.appendPlainText(f"    System On Disk --- {x.SystemDrive}")
        except:
            self.inf1.appendPlainText("Sorry, but something went wrong :(")
            self.inf1.appendPlainText(f"An error occured while attempting to returnOS")


class Cpuif(QWidget):
    def __init__(self):
        super().__init__()

        resx2 = 0
        resy2 = 0

        for i in pc.Win32_VideoController():
            resx2 = i.CurrentHorizontalResolution
            resy2 = i.CurrentVerticalResolution

        self.setGeometry((resx2 - 344) // 2, (resy2 - 190) // 2 - 220, 344, 190)
        self.setMinimumSize(344, 190)
        self.setMaximumSize(344, 190)
        self.setWindowTitle("CPU info")
        self.setWindowIcon(QtGui.QIcon(resource_path("cpu.png")))

        layout = QVBoxLayout()
        self.inf2 = QtWidgets.QPlainTextEdit()
        self.inf2.setReadOnly(True)
        self.inf2.setGeometry(0, 0, 344, 190)
        layout.addWidget(self.inf2)

        self.info()

        self.setLayout(layout)

    def info(self):
        try:
            counter = 1
            for x in pc.Win32_Processor():
                self.inf2.appendPlainText(f"Processor {counter} --- {x.Name}")
                self.inf2.appendPlainText(f"    Socket --- {x.SocketDesignation}")
                self.inf2.appendPlainText(f"    Core(s) --- {x.NumberOfCores}")
                self.inf2.appendPlainText(f"    Thread(s) --- {x.NumberOfLogicalProcessors}")
                counter += 1
        except:
            self.inf2.appendPlainText("Sorry, but something went wrong :(")
            self.inf2.appendPlainText(f"An error occured while attempting to returnProcessor")


class Gpuif(QWidget):
    def __init__(self):
        super().__init__()

        resx3 = 0
        resy3 = 0

        for i in pc.Win32_VideoController():
            resx3 = i.CurrentHorizontalResolution
            resy3 = i.CurrentVerticalResolution

        self.setGeometry((resx3 - 344) // 2 + 344, (resy3 - 190) // 2 - 190, 344, 190)
        self.setMinimumSize(344, 190)
        self.setMaximumSize(344, 190)
        self.setWindowTitle("GPU info")
        self.setWindowIcon(QtGui.QIcon(resource_path("gpu.png")))

        layout = QVBoxLayout()
        self.inf3 = QtWidgets.QPlainTextEdit()
        self.inf3.setReadOnly(True)
        self.inf3.setGeometry(0, 0, 344, 190)
        layout.addWidget(self.inf3)

        self.info()

        self.setLayout(layout)

    def info(self):
        try:
            counter = 1
            for x in pc.Win32_VideoController():
                self.inf3.appendPlainText(f"Graphics card {counter} --- {x.Caption}")
                self.inf3.appendPlainText(f"    Video memory (Up to 4GB) --- {converted_ctypes(x.AdapterRAM, c_uint32=1)} GB")
                self.inf3.appendPlainText(f"    Resolution --- {x.CurrentHorizontalResolution} x {x.CurrentVerticalResolution}")
                self.inf3.appendPlainText(f"    Current refresh rate --- {x.CurrentRefreshRate} Hz")
                counter += 1
        except:
            self.inf3.appendPlainText("Sorry, but something went wrong :(")
            self.inf3.appendPlainText(f"An error occured while attempting to returnGraphics")


class Ramif(QWidget):
    def __init__(self):
        super().__init__()

        resx4 = 0
        resy4 = 0

        for i in pc.Win32_VideoController():
            resx4 = i.CurrentHorizontalResolution
            resy4 = i.CurrentVerticalResolution

        self.setGeometry((resx4 - 344) // 2 - 344, (resy4 - 190) // 2 + 30, 344, 190)
        self.setMinimumSize(344, 190)
        self.setMaximumSize(344, 190)
        self.setWindowTitle("RAM info")
        self.setWindowIcon(QtGui.QIcon(resource_path("ram.png")))

        layout = QVBoxLayout()
        self.inf4 = QtWidgets.QPlainTextEdit()
        self.inf4.setReadOnly(True)
        self.inf4.setGeometry(0, 0, 344, 190)
        layout.addWidget(self.inf4)

        self.info()

        self.setLayout(layout)

    def info(self):
        try:
            counter = 1
            for x in pc.Win32_PhysicalMemory():
                if x.Capacity is not None:
                    self.inf4.appendPlainText(f"RAM {counter} --- {x.Manufacturer} {x.PartNumber}")
                    self.inf4.appendPlainText(f"    Size --- {converted_ctypes(x.Capacity, c_uint64=1)} GB")
                    self.inf4.appendPlainText(f"    Clock Speed --- {x.ConfiguredClockSpeed} MHz")
                    self.inf4.appendPlainText(f"    Voltage --- {convert_ctypes(x.ConfiguredVoltage, c_uint32=1)} mV")
                    counter += 1
        except:
            self.inf4.appendPlainText("Sorry, but something went wrong :(")
            self.inf4.appendPlainText(f"An error occured while attempting to returnRAM")


class Diskif(QWidget):
    def __init__(self):
        super().__init__()

        resx5 = 0
        resy5 = 0

        for i in pc.Win32_VideoController():
            resx5 = i.CurrentHorizontalResolution
            resy5 = i.CurrentVerticalResolution

        self.setGeometry((resx5 - 344) // 2 + 344, (resy5 - 190) // 2 + 30, 344, 190)
        self.setMinimumSize(344, 190)
        self.setMaximumSize(344, 190)
        self.setWindowTitle("Disk info")
        self.setWindowIcon(QtGui.QIcon(resource_path("disk.png")))

        layout = QVBoxLayout()
        self.inf5 = QtWidgets.QPlainTextEdit()
        self.inf5.setReadOnly(True)
        self.inf5.setGeometry(0, 0, 344, 190)
        layout.addWidget(self.inf5)

        self.info()

        self.setLayout(layout)

    def info(self):
        try:
            for x in pc.Win32_LogicalDisk():
                self.inf5.appendPlainText(f"Disk {x.Caption}")
                self.inf5.appendPlainText(f"    File System --- {x.FileSystem}")
                self.inf5.appendPlainText(f"    Size --- {converted_ctypes(x.Size, c_uint64=1)} GB")
                self.inf5.appendPlainText(f"    Free Space --- {converted_ctypes(x.FreeSpace, c_uint64=1)} GB")
        except:
            self.inf5.appendPlainText("Sorry, but something went wrong :(")
            self.inf5.appendPlainText(f"An error occured while attempting to returnStorage")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    application()
