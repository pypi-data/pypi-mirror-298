# std.
import ctypes
import json
import sys
import os

# qa.
from qanalytics.Struct import *
from qanalytics.Enum import *

def SetValue(Dict, Keys, Value):
    if(len(Keys) == 1):
        Dict[Keys[0]] = Value
    else:
        if(Keys[0] not in Dict):
            Dict[Keys[0]] = dict()
        SetValue(Dict[Keys[0]], Keys[1:], Value)

def GetValue(Dict, Keys):
    if(len(Keys) == 1):
        return Dict[Keys[0]]
    else:
        return GetValue(Dict[Keys[0]], Keys[1:])

def Request(pPath, pArgs, pLogger):

    # load library.
    LibraryExt = '' 
    if sys.platform == 'linux' or sys.platform == 'linux2':
        LibraryExt = 'so'
    elif sys.platform == 'darwin':
        LibraryExt = 'dylib'
    elif sys.platform == 'win32':
        LibraryExt = 'dll'
    LibraryPath = os.path.dirname(__file__) + '\\bin\\qAPI.' + LibraryExt
    if not os.path.isfile(LibraryPath):
        raise Exception("dll not found: " + LibraryPath)
    Library = ctypes.CDLL(LibraryPath)

    # set function prototype.
    Function = getattr(Library, "Request")
    Function.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    Function.restype = ctypes.c_bool

    # prepare path.
    PathPtr = pPath.encode('utf-8')

    # prepare request.
    RequestDict = {}
    RequestDict['Logger'] = pLogger.serialize()
    for ArgNames, ArgStruct in pArgs:
        SetValue(RequestDict, ArgNames, ArgStruct.serialize())
    RequestStr = json.dumps(RequestDict)
    RequestPtr = ctypes.c_char_p(RequestStr.encode())

    # prepare response.
    ResponseSize = 8 * len(RequestStr) * sys.getsizeof(ctypes.c_char_p)
    ResponsePtr = ctypes.create_string_buffer(ResponseSize)

    # execute request.
    # print(RequestStr)
    Success = Function(PathPtr, RequestPtr, ResponsePtr)

    # set results.
    if ResponsePtr != None:
        ResponseStr = ResponsePtr.value.decode('utf-8')
        if ResponseStr != '':
            try:
                ResponseDict = json.loads(ResponseStr)
                pLogger.deserialize(ResponseDict['Logger'])
                if Success:
                    for ArgNames, ArgStruct in pArgs:
                        ArgStruct.deserialize(GetValue(ResponseDict, ArgNames))
                    return True
                else:
                    return False
            except json.decoder.JSONDecodeError:
                raise Exception(pPath + ': Cannot decode JSON response')
        else:
            raise Exception(pPath + ': Cannot read response')
    else:
        raise Exception(pPath + ': Cannot read response')