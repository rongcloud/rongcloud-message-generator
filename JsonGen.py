#coding=utf-8
import os,json
from BaseGen import BaseGen
import Util
class JsonGen(BaseGen):
    
    def gen(self):
        map = self._convertToDic()
        outPath = os.path.join(self.msgObj.outputPath,self.msgObj.msgName+".json")
        self._writeJson(map,outPath)

        print(outPath)
        print("\n\n")

    def _writeJson(self,map,output):
        with open(output,"w+") as f:
            json.dump(map,f,indent=2)

    def _convertToDic(self):
        map = {}
        map[Util.Message.MsgName] = self.msgObj.msgName
        map[Util.Message.ObjName] = self.msgObj.objName
        map[Util.Message.PersistentFlag] = self.msgObj.persistentFlag
        map[Util.Message.Package] = self.msgObj.package
        map[Util.Message.Param] = self.msgObj.param
        return map