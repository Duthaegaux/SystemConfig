import ctypes


def convert(integer):
    """Converts integers from Bytes to GBytes"""
    if integer is not None and integer / 1073741824 > 3:
        return round(integer / 1073741824)
    elif integer is not None:
        return integer / 1073741824
    else:
        return "???"


def convert_ctypes(integer, c_uint32=None, c_uint64=None):
    """Converts c_uint32 or c_uint64 to integer"""
    if integer is not None:
        if integer is not int:
            integer = int(integer)
        if c_uint32 is None and c_uint64 is None:
            print("Err: 1 of required params unfilled")
        elif c_uint32 == 1 and c_uint64 is None:
            return ctypes.c_uint32(integer).value
        elif c_uint32 is None and c_uint64 == 1:
            return ctypes.c_uint64(integer).value
        else:
            print("Err: c_uint32 and c_uint64 can't be 1 together.")
    else:
        return "???"


def converted_ctypes(integer, c_uint32=None, c_uint64=None):
    """Converts c_uint32 or c_uint64 to integer and converts it to Gbytes"""
    if integer is not None:
        if integer is not int:
            integer = int(integer)
        if c_uint32 is None and c_uint64 is None:
            print("Err: 1 of required params unfilled")
        elif c_uint32 == 1 and c_uint64 is None:
            return convert(ctypes.c_uint32(integer).value)
        elif c_uint32 is None and c_uint64 == 1:
            return convert(ctypes.c_uint64(integer).value)
        else:
            print("Err: c_uint32 and c_uint64 can't be 1 together.")
    else:
        return "???"

