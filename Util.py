#coding=utf-8

import os

class Message:
    MsgName = "msgName"
    ObjName = "objName"
    PersistentFlag = "persistentFlag"
    Param = "param"
    Package = "package"
    Output = "output"

class Param:
    Bool = "bool"
    Int = "int"
    String = "string"
    Double = "double"
    Map = "map" # Map 对应 java map ，OC NSDictionary
    List = "list" # List 对应 java list，OC NSArray

class Persistent:
    # 在本地不存储，不计入未读数
    IsNone = 0 
    # 在本地只存储，但不计入未读数
    IsPersisted = 1
    # 在本地进行存储并计入未读数
    IsCounted = 3
    # 在本地不存储，不计入未读数，并且如果对方不在线，服务器会直接丢弃该消息，对方如果之后再上线也不会再收到此消息。
    # 一般用于发送输入状态之类的消息，该类型消息的messageUId为nil。
    IsStatus = 16

def checkValidMsgObj(msgObj):
    if not msgObj.msgName:
        print("msgName 不存在 ，程序终止 ")
        exit()

    if not msgObj.objName:
        print("objName 不存在 ，程序终止")
        exit()

    if len(msgObj.objName) > 16:
        print("objName 长度不能超过 16 个字符")
        exit()
    
    if msgObj.objName.upper().startswith("RC:"):
        print("( objName :" + msgObj.objName +" )唯一标识 objName 不能以 RC: 开头，程序终止")
        exit()

    if not (msgObj.persistentFlag == Persistent.IsNone or msgObj.persistentFlag == Persistent.IsPersisted or msgObj.persistentFlag == Persistent.IsCounted or msgObj.persistentFlag == Persistent.IsStatus):
        print("( persistentFlag :" + str(msgObj.persistentFlag) +" ) 非法的持久化标识 persistentFlag ，程序终止")
        exit()
    
    if not msgObj.package:
        print("package 不存在 ，程序终止")
        exit()
    
    for key in msgObj.param:
        paramType = msgObj.param[key]
        if not isValidParamType(paramType):
            print("param 参数类型出错 ( " + key + " : " + paramType +" )，请参考 Util.py 的 class Param")
            exit()

def checkValidJsonDict(jsonDict):
    if not Message.MsgName in jsonDict:
        _exitByJson(Message.MsgName)
    if not Message.ObjName in jsonDict:
        _exitByJson(Message.ObjName)
    if not Message.PersistentFlag in jsonDict:
        _exitByJson(Message.PersistentFlag)
    if not Message.Package in jsonDict:
        _exitByJson(Message.Package)
    if not Message.Param in jsonDict:
        _exitByJson(Message.Param)

def _exitByJson(key):
    print("json 模板不存在关键字 " + key + " ，程序终止")
    exit()

def isValidParamType(type):
    if type == Param.Bool or type == Param.Int or type == Param.Double or type == Param.String or type == Param.Map or type == Param.List:
        return True
    return False

def getOutputPath():
    pwd = os.getcwd()
    outputPath = os.path.join(pwd,Message.Output)
    _createOutputPath(outputPath)
    return outputPath


def _createOutputPath(outputPath):
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)