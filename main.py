#coding=utf-8

import os,json
import Util

from MsgObj import MsgObj

def main():
    template_path = os.path.join(os.getcwd(),"MessageTemplate.json")
    if not os.path.exists(template_path):
        print("自定义消息模板 MessageTemplate.json 不存在")
        exit(1)
    
    load_dict = {}
    with open(template_path,"r") as f:
        load_dict = json.load(f)
    
    Util.checkValidJsonDict(load_dict)

    format_dict = json.dumps(load_dict,indent=2)
    print("加载的 json 模板为：")
    print(format_dict)
    msgName = load_dict[Util.Message.MsgName]
    objName = load_dict[Util.Message.ObjName]
    persistentFlag = load_dict[Util.Message.PersistentFlag]
    package = load_dict[Util.Message.Package]
    param = load_dict[Util.Message.Param]
    msgObj = MsgObj(msgName,objName)
    msgObj.setPersistentFlag(persistentFlag)
    msgObj.setPackage(package)
    msgObj.param = param
    msgObj.showDetail()
    msgObj.genMsg()
    

if __name__ == '__main__':
    main()
    