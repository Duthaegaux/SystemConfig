import wmi
from check import *

pc = wmi.WMI()

def returnProcessor():
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
        return "Sorry, but something went wrong :(",\
               f"An error occured while attempting to returnProcessor"


def returnGraphics():
    try:
        graphics = []
        counter = 1
        for x in pc.Win32_VideoController():
            graphics.append(f"Graphics card {counter} --- {x.Caption}")
            graphics.append(f"    Video memory (Up to 4GB) --- {converted_ctypes(x.AdapterRAM, c_uint32=1)} GB")
            graphics.append(f"    Resolution --- {x.CurrentHorizontalResolution} x {x.CurrentVerticalResolution}")
            graphics.append(f"    Current refresh rate --- {x.CurrentRefreshRate} Hz")
            counter += 1
        return tuple(graphics)
    except:
        return "Sorry, but something went wrong :(",\
               f"An error occured while attempting to returnGraphics"


def returnRAM():
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
        return "Sorry, but something went wrong :(",\
               f"An error occured while attempting to returnRAM"


def returnStorage():
    try:
        storages = []
        for x in pc.Win32_LogicalDisk():
            storages.append(f"Disk {x.Caption}")
            storages.append(f"    File System --- {x.FileSystem}")
            storages.append(f"    Size --- {converted_ctypes(x.Size, c_uint64=1)} GB")
            storages.append(f"    Free Space --- {converted_ctypes(x.FreeSpace, c_uint64=1)} GB")
        return tuple(storages)
    except:
        return "Sorry, but something went wrong :(",\
               f"An error occured while attempting to returnStorage"


def createFile():
    with open("configuration.txt", "w") as f:
        for i in returnProcessor():
            f.write(i + "\n")
        for i in returnGraphics():
            f.write(i + "\n")
        for i in returnRAM():
            f.write(i + "\n")
        for i in returnStorage():
            f.write(i + "\n")


def showAll():
    for i in returnProcessor():
        print(i)
    for i in returnGraphics():
        print(i)
    for i in returnRAM():
        print(i)
    for i in returnStorage():
        print(i)


if __name__ == "__main__":
    showAll()
    createFile()
    wait_for_closing = input()
