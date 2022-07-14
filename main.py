import wmi
from check import *

pc = wmi.WMI()


def showProcessor():
    try:
        for x in pc.Win32_Processor():
            print(f"Processor --- {x.Name}",
                  f"    Socket --- {x.SocketDesignation}",
                  f"    Core(s) --- {x.NumberOfCores}",
                  f"    Thread(s) --- {x.NumberOfLogicalProcessors}", sep="\n")
    except:
        print("Sorry, but something went wrong :(",
              f"An error occured while attempting to showProcessor", sep="\n")


def showGraphics():
    try:
        for x in pc.Win32_VideoController():
            print(f"Graphics card --- {x.Caption}",
                  f"    Video memory (Up to 4GB) --- {converted_ctypes(x.AdapterRAM, c_uint32=1)} GB",
                  f"    Resolution --- {x.CurrentHorizontalResolution} x {x.CurrentVerticalResolution}",
                  f"    Current refresh rate --- {x.CurrentRefreshRate} Hz", sep="\n")
    except:
        print("Sorry, but something went wrong :(",
              f"An error occured while attempting to showGraphics", sep="\n")


def showRAM():
    try:
        counter = 0
        for x in pc.Win32_PhysicalMemory():
            if x.Capacity is not None:
                counter += 1
                print(f"RAM {counter} --- {x.Manufacturer} {x.PartNumber}",
                      f"    Size --- {converted_ctypes(x.Capacity, c_uint64=1)} GB",
                      f"    Clock Speed --- {x.ConfiguredClockSpeed} MHz",
                      f"    Voltage --- {convert_ctypes(x.ConfiguredVoltage, c_uint32=1)} mV", sep="\n")
    except:
        print("Sorry, but something went wrong :(",
              f"An error occured while attempting to showRAM", sep="\n")


def showStorage():
    try:
        for x in pc.Win32_LogicalDisk():
            print(f"Disk {x.Caption}",
                  f"    File System --- {x.FileSystem}",
                  f"    Size --- {converted_ctypes(x.Size, c_uint64=1)} GB",
                  f"    Free Space --- {converted_ctypes(x.FreeSpace, c_uint64=1)} GB", sep="\n")
    except:
        print("Sorry, but something went wrong :(",
              f"An error occured while attempting to showStorage", sep="\n")


def showAll():
    showProcessor()
    showGraphics()
    showRAM()
    showStorage()


if __name__ == "__main__":
    showAll()
    wait_for_closing = input()
