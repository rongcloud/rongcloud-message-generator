#coding=utf-8
# 自定义消息的描述类

import json

import Util

from iOSGen import iOSGen
from AndroidGen import AndroidGen
from JsonGen import JsonGen

class MsgObj:

    param = {}

    outputPath = Util.getOutputPath()
    pass

    def __init__(self,msgName,objName):
        self.msgName = msgName
        self.objName = objName
        print("\n"+"输出路径为:")
        print(self.outputPath)
    
    def addParamBool(self,name):
        self.param[name] = Util.Param.Bool;

    def addParamInt(self,name):
        self.param[name] = Util.Param.Int;

    def addParamString(self,name):
        self.param[name] = Util.Param.String;
    
    def addParamDouble(self,name):
        self.param[name] = Util.Param.Double;
    
    def addParamMap(self,name):
        self.param[name] = Util.Param.Map

    def addParamList(self,name):
        self.param[name] = Util.Param.List

    def setPersistentFlag(self,flag):
        self.persistentFlag = flag;
    
    def setPackage(self,package):
        self.package = package
    
    def genMsg(self):
        Util.checkValidMsgObj(self)
        self._genJson()
        self._genMsg()

    
    def showDetail(self):
        print("\n\n详细数据:")
        print("msgName:\t %s" % self.msgName)
        print("objName:\t %s" % self.objName)
        print("persistentFlag:\t %s" % self.persistentFlag)
        print("package:\t %s" % self.package)
        print("params:")
        print(json.dumps(self.param,indent=2))
        print("\n\n")
    
    def _genMsg(self):
        print("开始生成自定义消息\n")
        ios = iOSGen(self)
        ios.gen()
        android = AndroidGen(self)
        android.gen()

    def _genJson(self):
        print("> 生成自定义消息 json 模板文件")

        jsonGen = JsonGen(self)
        jsonGen.gen()