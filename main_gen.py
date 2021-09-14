#coding=utf-8

from MsgObj import MsgObj;
import Util

def main():
    # 1.构造 MsgObj 对象
    obj = MsgObj("CustomMessage","app:cusMsg")
    # 2.设置消息持久化标识
    obj.setPersistentFlag(Util.Persistent.IsCounted)
    # 3.设置消息所在包名 安卓专用
    obj.setPackage("cn.rongcloud.im.im.message")
    # 4.设置参数列表
    obj.addParamBool("isVip")
    obj.addParamString("name")
    obj.addParamString("uid")
    obj.addParamInt("age")
    obj.addParamDouble("price")
    obj.addParamMap("dataMap")
    obj.addParamList("dataList")

    # 5.打印消息内容
    obj.showDetail()

    # 6.生成消息
    obj.genMsg()
    pass
    

if __name__ == '__main__':
    main()
    