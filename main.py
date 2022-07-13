import wmi
import ctypes

pc = wmi.WMI()
counter = 0

for x in pc.Win32_Processor():
    print(f"Processor --- {x.Name}",
          f"    Socket --- {x.SocketDesignation}",
          f"    Core(s) --- {x.NumberOfCores}",
          f"    Thread(s) --- {x.NumberOfLogicalProcessors}", "", sep="\n")
for x in pc.Win32_VideoController():
    print(f"Graphics card --- {x.Caption}",
          f"    Video memory (Up to 4GB) --- {round(ctypes.c_uint32(int(x.AdapterRAM)).value / 1073741824)} GB",
          f"    Resolution --- {x.CurrentHorizontalResolution} x {x.CurrentVerticalResolution}",
          f"    Current refresh rate --- {x.CurrentRefreshRate} Hz", "", sep="\n")
for x in pc.Win32_PhysicalMemory():
    if x.Capacity and x.ConfiguredVoltage is not None:
        counter += 1
        print(f"RAM {counter} --- {x.Manufacturer} {x.PartNumber}",
              f"    Size --- {round(ctypes.c_uint64(int(x.Capacity)).value / 1073741824)} GB",
              f"    Clock Speed --- {x.ConfiguredClockSpeed} MHz",
              f"    Voltage --- {ctypes.c_uint32(x.ConfiguredVoltage).value / 1000} V", sep="\n")
    elif x.Capacity is not None:
        counter += 1
        print(f"RAM {counter} --- {x.Manufacturer} {x.PartNumber}",
              f"    Size --- {round(ctypes.c_uint64(int(x.Capacity)).value / 1073741824)} GB",
              f"    Clock Speed --- {x.ConfiguredClockSpeed} MHz", sep="\n")
print()
for x in pc.Win32_LogicalDisk():
    print(f"Disk {x.Caption}",
          f"    File System --- {x.FileSystem}",
          f"    Size --- {round(int(x.Size) / 1073741824)} GB",
          f"    Free Space --- {round(int(x.FreeSpace) / 1073741824)} GB", sep="\n")
wait_for_closing = input()
