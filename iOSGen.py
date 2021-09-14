#coding=utf-8

import os
from BaseGen import BaseGen
import Util

class iOSGen(BaseGen):

    def gen(self):
        print("> 生成 ios 自定义消息\n")
        self._genHeader()
        self._genM()
        pass

    def convertParamType(self,type):
        if type == Util.Param.Bool:
            return "BOOL";
        elif type == Util.Param.Int:
            return "int";
        elif type == Util.Param.Double:
            return "double";
        elif type == Util.Param.String:
            return "NSString *"
        elif type == Util.Param.Map:
            return "NSDictionary *"
        elif type == Util.Param.List:
            return "NSArray *"
        str = "convertParamType " + "unknown ParamType " + type
        print(str)
        return str


    def _genHeader(self):
        print("生成 .h 文件")
        # print(self.msgName)
        # print(self.copyright)

        str = self.copyright;
        str += "\n" + "#import <RongIMLibCore/RongIMLibCore.h>" + "\n\n"

        str += "@interface "+ self.msgObj.msgName + " : RCMessageContent" + "\n\n"

        for key in self.msgObj.param:
            paramType = self.msgObj.param[key];
            str += "@property (nonatomic, " + self._convertParamAssignType(paramType) + ") " + self.convertParamType(paramType) + " " + key + ";" + "\n\n"
            
        str += "@end" + "\n"
        # print(str)

        outputPath = os.path.join(self.msgObj.outputPath,self.msgObj.msgName + ".h")
        with open(outputPath,"w+") as f:
            f.write(str)
        
        print("%s\n" % outputPath)

    def _genM(self):
        print("生成 .m 文件")
        str = self.copyright;
        str += "#import \"" + self.msgObj.msgName + ".h\"" + "\n\n"
        str += "@implementation " + self.msgObj.msgName + "\n";
        str += self._genPersistentFlagMethod()
        str += self._genEncodeMethod()
        str += self._genDecodeMethod()
        str += self._genObjNameMethod()
        str += self._genSearchWordMethod()
        str += self._genConversationDigestMethod()
        str += "@end\n"

        # print(str)

        outputPath = os.path.join(self.msgObj.outputPath,self.msgObj.msgName + ".m")
        with open(outputPath,"w+") as f:
            f.write(str)
        
        print("%s\n\n" % outputPath)

    def _genPersistentFlagMethod(self):
        str = "+ (RCMessagePersistent)persistentFlag {" + "\n"
        str += "    return " + self._convertPersistentFlag() + ";" + "\n"
        str += "}" + "\n"
        return str;

    def _genEncodeMethod(self):
        str = ""
        str += "- (NSData *)encode {" + "\n"
        str += "    NSMutableDictionary *dataDict = [NSMutableDictionary dictionary];" + "\n"
        
        for key in self.msgObj.param:
            paramType = self.msgObj.param[key]
            str += self.__encodeParam(key,paramType);

        str += self.__encodeExtra()
        str += self.__encodeSenderUserInfo()
        str += self.__encodeMentionedInfo()

        str += "    NSData *data = [NSJSONSerialization dataWithJSONObject:dataDict options:kNilOptions error:nil];" + "\n"
        str += "    return data;" + "\n"
        str += "}" + "\n\n"

        return str

    def _genDecodeMethod(self):
        str = "- (void)decodeWithData:(NSData *)data {" + "\n"

        str += "    if (!data) {" + "\n"
        str += "         return;" + "\n"
        str += "    }" + "\n"

        str += "    NSDictionary *dic = [NSJSONSerialization JSONObjectWithData:data options:kNilOptions error:nil];" + "\n"
        str += "    if (dic) {" + "\n"

        for key in self.msgObj.param:
            paramType = self.msgObj.param[key]
            str += self.__decodeParam(key,paramType)

        str += self.__decodeExtra()
        str += self.__decodeSenderUserInfo()
        str += self.__decodeMentionedInfo()

        str += "    }" + "\n"


        str += "}" + "\n\n"
        # print(self.param)
        return str

    
    def _genObjNameMethod(self):
        str = "+ (NSString *)getObjectName {" + "\n"
        str += "    return @\""+ self.msgObj.objName + "\";" + "\n"
        str += "}" + "\n\n"
        return str

    def _genSearchWordMethod(self):
        str = "- (NSArray<NSString *> *)getSearchableWords {" + "\n"
        str += "    //todo : 该方法返回用于消息搜索" + "\n"
        str += "    return nil;" + "\n"
        str += "}" + "\n\n"
        return str;

    def _genConversationDigestMethod(self):
        str = "- (NSString *)conversationDigest {" + "\n"
        str += "    //todo : 该方法返回内容展示在会话列表" + "\n"
        str += "    return nil;" + "\n"
        str += "}" + "\n\n"
        return str

    def __encodeParam(self,key,value):
        # print("encode key:%s     value:%s" % (key,value))
        str = ""
        if value == Util.Param.Bool or value == Util.Param.Int or value == Util.Param.Double:
            str = "    [dataDict setObject:@(self." + key+ ") forKey:@\"" + key + "\"];" + "\n"
        elif value == Util.Param.String:
            str = "    if(!self." + key +") {" + "\n"
            str += "        self." + key + " = @\"\";" + "\n"
            str += "    }" + "\n"
            str += "    [dataDict setObject:self." + key + " forKey:@\"" + key +"\"];"  + "\n"
        elif value == Util.Param.Map or value == Util.Param.List:
            str = "    if (self." + key+ ") {" + "\n"
            str += "        [dataDict setObject:self." + key + " forKey:@\"" + key +"\"];" + "\n"
            str += "    }" + "\n"
        else:
            print("__encodeParam unknown encode " + key +" " + value)
        return str
    
    def __encodeExtra(self):
        str = "    if (self.extra) {" + "\n"
        str += "        [dataDict setObject:self.extra forKey:@\"extra\"];" + "\n"
        str += "    }" + "\n"
        return str
    
    def __encodeSenderUserInfo(self):
        str = "    if (self.senderUserInfo) {" + "\n"
        str += "        [dataDict setObject:[self encodeUserInfo:self.senderUserInfo] forKey:@\"user\"];" + "\n"
        str += "    }" + "\n"
        return str

    def __encodeMentionedInfo(self):
        str = "    if (self.mentionedInfo) {" + "\n"
        str += "        [dataDict setObject:[self encodeMentionedInfo:self.mentionedInfo] forKey:@\"mentionedInfo\"];" + "\n"
        str += "    }" + "\n"
        return str

    def __decodeParam(self,key,value):
        # print("decode key:%s     value:%s" % (key,value))
        str = ""
        if value == Util.Param.Bool:
            str += "        self." + key + " = [[dic objectForKey:@\"" + key + "\"] boolValue];" + "\n"
            pass
        elif value == Util.Param.Int:
            str += "        self." + key + " = [[dic objectForKey:@\"" + key + "\"] intValue];" + "\n"
        elif value == Util.Param.Double:
            str += "        self." + key + " = [[dic objectForKey:@\"" + key + "\"] doubleValue];" + "\n"
        elif value == Util.Param.String or value == Util.Param.Map or value == Util.Param.List:
            str += "        self." + key + " = [dic objectForKey:@\"" + key + "\"];" + "\n"
        else:
            str += "__decodeParam unknown decode " + key +" " + value
            print(str)
        return str
    
    def __decodeExtra(self):
        return "        self.extra = [dic objectForKey:@\"extra\"];" + "\n"
    
    def __decodeSenderUserInfo(self):
        str = "        NSDictionary *userinfoDic = [dic objectForKey:@\"user\"];" + "\n"
        str += "        [self decodeUserInfo:userinfoDic];" + "\n"
        return str

    def __decodeMentionedInfo(self):
        str = "        NSDictionary *mentionedInfoDic = [dic objectForKey:@\"mentionedInfo\"];" + "\n"
        str += "        [self decodeMentionedInfo:mentionedInfoDic];" + "\n"
        return str

    def _convertPersistentFlag(self):
        flag = self.msgObj.persistentFlag
        if flag == Util.Persistent.IsNone:
            return "MessagePersistent_NONE"
        elif flag == Util.Persistent.IsPersisted:
            return "MessagePersistent_ISPERSISTED"
        elif flag == Util.Persistent.IsCounted:
            return "MessagePersistent_ISCOUNTED"
        elif flag == Util.Persistent.IsStatus:
            return "MessagePersistent_STATUS"
        else :
            return "unknown PersistentFlag"

    def _convertParamAssignType(self,type):
        if type == Util.Param.Bool:
            return "assign";
        elif type == Util.Param.Int:
            return "assign";
        elif type == Util.Param.Double:
            return "assign";
        elif type == Util.Param.String:
            return "copy"
        elif type == Util.Param.Map or type == Util.Param.List:
            return "strong"
        str = "_convertParamAssignType unknow " + type;
        print(str)
        return str;
