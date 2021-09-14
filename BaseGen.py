#coding=utf-8

import time

class BaseGen:

    def __init__(self,msgObj):
        self.msgObj = msgObj
        self.copyright = self._Copyright()

    #子类复写该方法，生成代码
    def gen(self):
        pass

    #子类复写该方法，进行参数类型转换
    def convertParamType(self):
        pass

    #生成 copyright
    def _Copyright(self):
        copyright = "/**\n";
        copyright += " * Copyright RongCloud.\n"
        copyright += " * Created by RongCloud on " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ".\n"
        copyright += " * Author Qi.\n"
        copyright += " */\n"
        return copyright