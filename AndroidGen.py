#coding=utf-8

from BaseGen import BaseGen
import Util
import os

class AndroidGen(BaseGen):
 
    def gen(self):
        print("> 生成 android 自定义消息\n")
        self._genJava()
        pass

    def convertParamType(self,type):
        if type == Util.Param.Bool:
            return "boolean"
        elif type == Util.Param.Int:
            return "int";
        elif type == Util.Param.Double:
            return "double";
        elif type == Util.Param.String:
            return "String"
        elif type == Util.Param.Map:
            return "Map"
        elif type == Util.Param.List:
            return "List"
        else :
            str = "convertParamType " + "unknown ParamType " + type
            print(str)
            return str

    def _genJava(self):
        str = self._genPackage()
        str += self._genImport()
        str += self.copyright
        str += self._genMessageTag()
        str += "public class " + self.msgObj.msgName + " extends MessageContent {" + "\n"
        str += self._genParamList()
        str += self._getConstructionMethod();
        str += self._genEncodeMethod()
        str += self._getConstructionDecodeMethod()
        str += self._genWriteToParcelMethod()
        str += self._getConstructionParcelMethod()
        str += self._genDescribeContentsMethod()
        str += self._genCreatorMethod()
        str += self._genGetSearchableWord()
        str += self._genGetterSetter()
        str += "}\n"
        
        # print("java 内容")
        # print(str)
        outputPath = os.path.join(self.msgObj.outputPath,self.msgObj.msgName + ".java")
        with open(outputPath,"w+") as f:
            f.write(str)
        
        print("%s\n" % outputPath)

    def _genPackage(self):
        if not self.msgObj.package:
            print("[Warnning] 没有设置安卓包名")
        return "package " + self.msgObj.package + ";\n\n"

    
    def _genImport(self):
        str = "import android.os.Parcel;" + "\n"
        str += "import android.text.TextUtils;" + "\n\n"

        str += "import org.json.JSONArray;" + "\n"
        str += "import org.json.JSONException;" + "\n"
        str += "import org.json.JSONObject;" + "\n\n"

        str += "import java.io.UnsupportedEncodingException;" + "\n"
        str += "import java.util.ArrayList;" + "\n"
        str += "import java.util.HashMap;" + "\n"
        str += "import java.util.Iterator;" + "\n"
        str += "import java.util.List;" + "\n"
        str += "import java.util.Map;" + "\n\n"

        str += "import io.rong.common.ParcelUtils;" + "\n"
        str += "import io.rong.common.RLog;" + "\n"
        str += "import io.rong.imlib.MessageTag;" + "\n"
        str += "import io.rong.imlib.model.MentionedInfo;" + "\n"
        str += "import io.rong.imlib.model.MessageContent;" + "\n"
        str += "import io.rong.imlib.model.UserInfo;" + "\n"
        str += "\n"
        return str

    def _genMessageTag(self):
        return "@MessageTag(value = \"" + self.msgObj.objName + "\", flag = " + self._convertPersistentFlag() + ")" + "\n"

    def _genParamList(self):
        str = "    private final static String TAG = \"" + self.msgObj.msgName + "\";" + "\n\n"

        for key in self.msgObj.param:
            paramType = self.msgObj.param[key];
            str += "    private " + self.convertParamType(paramType) + " " + key + ";" + "\n"
        
        str += "\n"
        return str
    
    def _getConstructionMethod(self):
        return "    public " + self.msgObj.msgName + "(){ }" + "\n\n"

    def _genEncodeMethod(self):
        str = "    @Override" + "\n"
        str += "    public byte[] encode() {" + "\n"

        str += "        JSONObject jsonObj = new JSONObject();" + "\n"
        str += "        try {" + "\n"

        for key in self.msgObj.param:
            paramType = self.msgObj.param[key]
            str += self.__encodeParam(key,paramType);

        str += self.__genEncodeExtra()
        str += self.__genEncodeUserInfo()
        str += self.__genEncodeMentionInfo()

        str += "        } catch (JSONException e) {" + "\n"
        str += "            RLog.e(TAG, \"JSONException \" + e.getMessage());" + "\n"
        str += "        }" + "\n\n"

        str += "        try {" + "\n"
        str += "            return jsonObj.toString().getBytes(\"UTF-8\");" + "\n"
        str += "        } catch (UnsupportedEncodingException e) {" + "\n"
        str += "            RLog.e(TAG, \"UnsupportedEncodingException \", e);" + "\n"
        str += "        }" + "\n"
        
        str += "        return null;" + "\n"

        str += "    }" + "\n"
        return str + "\n\n"

    def _getConstructionDecodeMethod(self):
        str = "    public "+ self.msgObj.msgName + "(byte[] data) {"+ "\n"

        str += "        if (data == null) {" + "\n"
        str += "            RLog.e(TAG, \" " + self.msgObj.msgName + " data is null \");"+ "\n"
        str += "            return;" + "\n"
        str += "        }" + "\n\n"

        str += "        String jsonStr = null;" + "\n"
        str += "        try {" + "\n"
        str += "            jsonStr = new String(data, \"UTF-8\");" + "\n"
        str += "        } catch (UnsupportedEncodingException e) {" + "\n"
        str += "            RLog.e(TAG, \"UnsupportedEncodingException \", e);" + "\n"
        str += "        }"  + "\n\n"

        str += "        if (jsonStr == null) {" + "\n"
        str += "            RLog.e(TAG, \"jsonStr is null \");" + "\n"
        str += "            return;" + "\n"
        str += "        }"  + "\n"

        str += "        try {" + "\n"
        str += "            JSONObject jsonObj = new JSONObject(jsonStr);" + "\n"
        
        for key in self.msgObj.param:
            paramType = self.msgObj.param[key]
            str += self.__decodeParam(key,paramType)

        str += self.__decodeExtra()
        str += self.__decodeUserInfo()
        str += self.__decodeMentionedInfo()
        str += "        } catch (JSONException e) {" + "\n"
        str += "            RLog.e(TAG, \"JSONException \" + e.getMessage());" + "\n"
        str += "        }"  + "\n"

        str += "    }" + "\n"
        return str + "\n\n"

    def _genWriteToParcelMethod(self):
        str = "    @Override" + "\n"
        str += "    public void writeToParcel(Parcel dest, int flags) {" + "\n"

        for key in self.msgObj.param:
            paramType = self.msgObj.param[key]
            if paramType == Util.Param.Bool:
                # ParcelUtils 无法写入 bool，所以 bool 转 int
                str += "        ParcelUtils.writeToParcel(dest, " + key + " ? 1 : 0);" + "\n"
            else:
                str += "        ParcelUtils.writeToParcel(dest, " + key + ");" + "\n"

        str += "        ParcelUtils.writeToParcel(dest, getExtra());" + "\n"
        str += "        ParcelUtils.writeToParcel(dest, getUserInfo());" + "\n"
        str += "        ParcelUtils.writeToParcel(dest, getMentionedInfo());" + "\n"

        str +=  "    }" + "\n"
        return str + "\n\n"

    def _getConstructionParcelMethod(self):
        key = self.msgObj.msgName
        str = "    public " + key + "(Parcel in) {" + "\n"
        
        for key in self.msgObj.param:
            paramType = self.msgObj.param[key]
            if paramType == Util.Param.List:
                str += "        " + key + " = ParcelUtils." + self.__getParcelReadKey(paramType) + "(in , Object.class);"  + "\n"
            elif paramType == Util.Param.Bool:
                # ParcelUtils 无法读取 bool，所以 int 转 bool
                str += "        " + key + " = ParcelUtils." + self.__getParcelReadKey(paramType) + "(in) == 1;"  + "\n"
            else:
                str += "        " + key + " = ParcelUtils." + self.__getParcelReadKey(paramType) + "(in);"  + "\n"
        
        str += "        setExtra(ParcelUtils.readFromParcel(in));" + "\n"
        str += "        setUserInfo(ParcelUtils.readFromParcel(in, UserInfo.class));" + "\n"
        str += "        setMentionedInfo(ParcelUtils.readFromParcel(in, MentionedInfo.class));" + "\n"
        str +=  "    }" + "\n"
        return str + "\n\n"
    
    def _genDescribeContentsMethod(self):
        str = "    @Override" + "\n"
        str += "    public int describeContents() {" + "\n"
        str += "        return 0;" + "\n"
        str += "    }" + "\n"
        return str + "\n"

    def _genCreatorMethod(self):
        key = self.msgObj.msgName
        str = "    public static final Creator<" + key + "> CREATOR = new Creator<" + key + ">() {" + "\n"
        str += "        @Override" + "\n"
        str += "        public " + key + " createFromParcel(Parcel source) {" + "\n"
        str += "            return new " + key + "(source);" + "\n"
        str += "        }" + "\n\n"
        str += "        @Override" + "\n"
        str += "        public " + key + "[] newArray(int size) {" + "\n"
        str += "            return new " + key + "[size];" + "\n"
        str += "        }" + "\n"
        str += "    };" + "\n"
        return str + "\n\n"
    
    def _genGetSearchableWord(self):
        str = "    @Override" + "\n"
        str += "    public List<String> getSearchableWord() {" + "\n"
        str += "        //todo : 该方法返回用于消息搜索" + "\n"
        str += "        return null;" + "\n"
        str += "    }" + "\n"
        return str + "\n\n"
    
    def _genGetterSetter(self):
        str = ""
        for key in self.msgObj.param:
            paramType = self.msgObj.param[key]
            str += self.__genGetter(key,paramType)
            str += self.__genSetter(key,paramType)

        return str + "\n"

    def _convertPersistentFlag(self):
        flag = self.msgObj.persistentFlag
        if flag == Util.Persistent.IsNone:
            return "MessageTag.NONE"
        elif flag == Util.Persistent.IsPersisted:
            return "MessageTag.ISPERSISTED"
        elif flag == Util.Persistent.IsCounted:
            return "MessageTag.ISCOUNTED"
        elif flag == Util.Persistent.IsStatus:
            return "MessageTag.STATUS"
        else :
            return "unknown PersistentFlag"
    
    def __encodeParam(self,key,value):
        # print("encode key:%s     value:%s" % (key,value))
        str = ""
        if value == Util.Param.Bool or value == Util.Param.Int or value == Util.Param.Double:
            str = "            jsonObj.put(\"" + key +"\", " + key + ");" + "\n"
        elif value == Util.Param.String:
            str += "            if (!TextUtils.isEmpty(" + key + ")) {" + "\n"
            str += "                jsonObj.put(\"" + key +"\", " + key + ");" + "\n"
            str += "            }" + "\n"
        elif value == Util.Param.Map:
            str += "            if (" + key + " != null) {" + "\n"
            str += "                jsonObj.put(\"" + key + "\", new JSONObject(" + key + "));" + "\n"
            str += "            }" + "\n"
        elif value == Util.Param.List:
            str += "            if (" + key + " != null) {" + "\n"
            str += "                jsonObj.put(\"" + key +"\", JSONObject.wrap(" + key +"));" + "\n"
            str += "            }" + "\n"
        else:
            str += "__encodeParam unknown encode " + key +" " + value
            print(str)
        return str
    
    def __genEncodeExtra(self):
        str = "            if (!TextUtils.isEmpty(getExtra())) {" + "\n"
        str += "                jsonObj.put(\"extra\", getExtra());" + "\n"
        str += "            }" + "\n"
        return str
    
    def __genEncodeUserInfo(self):
        str = "            if (getJSONUserInfo() != null) {" + "\n"
        str += "                jsonObj.putOpt(\"user\", getJSONUserInfo());" + "\n"
        str += "            }" + "\n"
        return str
    
    def __genEncodeMentionInfo(self):
        str = "            if (getJsonMentionInfo() != null) {" + "\n"
        str += "                jsonObj.putOpt(\"mentionedInfo\", getJsonMentionInfo());" + "\n"
        str += "            }" + "\n"
        return str
    
    def __decodeParam(self,key,value):
        # print("decode key:%s     value:%s" % (key,value))
        str = ""
        if self.__isBaseParamType(value):
            objGetKey = self.___decodeParamJsonObjKey(value)
            str += "            if (jsonObj.has(\"" + key + "\")) {" + "\n"
            str += "                " + key + " = " + "jsonObj." + objGetKey + "(\"" + key + "\");" + "\n"
            str += "            }" + "\n"
        elif value == Util.Param.Map:
            str += self.___decodeParamMap(key)
        elif value == Util.Param.List:
            str += self.___decodeParamList(key)
        else :
            str += "            __decodeParam invalid type :" + value + "\n"
        return str
    
    def __decodeExtra(self):
        objGetKey = self.___decodeParamJsonObjKey(Util.Param.String)
        key = "extra"
        str = ""
        str += "            if (jsonObj.has(\"" + key + "\")) {" + "\n"
        str += "                setExtra(jsonObj." + objGetKey + "(\"" + key + "\"));" + "\n"
        str += "            }" + "\n"
        return str

    def __decodeUserInfo(self):
        objGetKey = self.___decodeParamJsonObjKey(Util.Param.Map)
        key = "user"
        str = ""
        str += "            if (jsonObj.has(\"" + key + "\")) {" + "\n"
        str += "                setUserInfo(parseJsonToUserInfo(jsonObj." + objGetKey + "(\"" + key + "\")));" + "\n"
        str += "            }" + "\n"
        return str

    def __decodeMentionedInfo(self):
        objGetKey = self.___decodeParamJsonObjKey(Util.Param.Map)
        key = "mentionedInfo"
        str = ""
        str += "            if (jsonObj.has(\"" + key + "\")) {" + "\n"
        str += "                setMentionedInfo(parseJsonToMentionInfo(jsonObj." + objGetKey + "(\"" + key + "\")));" + "\n"
        str += "            }" + "\n"
        return str
    
    def ___decodeParamJsonObjKey(self,value):
        if value == Util.Param.Bool:
            return "getBoolean"
        elif value == Util.Param.Int:
            return "getInt"
        elif value == Util.Param.Double:
            return "getDouble"
        elif value == Util.Param.String:
            return "optString"
        elif value == Util.Param.Map or value == Util.Param.List:
            return "getJSONObject"
        else :
            return "unknown decodeParamJsonObjKey"
    
    def __isBaseParamType(self,value):
        if value == Util.Param.Bool or value == Util.Param.Int or value == Util.Param.Double or value == Util.Param.String:
            return True
        return False
    
    def ___decodeParamMap(self,key):
        str = ""
        str += "            if (jsonObj.has(\"" + key+"\")) {" + "\n"
        str += "                " + key + " = new HashMap<>();" + "\n"
        str += "                JSONObject mapObject = jsonObj.getJSONObject(\""+key+"\");" + "\n"
        str += "                Iterator<String> keys = mapObject.keys();" + "\n"
        str += "                while (keys.hasNext()) {" + "\n"
        str += "                    String key = keys.next();" + "\n"
        str += "                    Object obj = mapObject.get(key);" + "\n"
        str += "                    if (obj instanceof String) {" + "\n"
        str += "                        " + key + ".put(key, (String)obj);" + "\n"
        str += "                    }else if(obj instanceof Integer) {" + "\n"
        str += "                        Integer value = (Integer)obj;" + "\n"
        str += "                        " + key + ".put(key,value.intValue());" + "\n"
        str += "                    }else if(obj instanceof Double) {" + "\n"
        str += "                        Double value = (Double)obj;" + "\n"
        str += "                        " + key + ".put(key,value.doubleValue());" + "\n"
        str += "                    }else if(obj instanceof  Boolean){" + "\n"
        str += "                        Boolean value = (Boolean)obj;" + "\n"
        str += "                        " + key + ".put(key,value.booleanValue());" + "\n"
        str += "                    }else {" + "\n"
        str += "                        RLog.w(TAG,\"无法识别 map 内的类型，被强转为 String: key = \" + key);" + "\n"
        str += "                        " + key + ".put(key, (String)obj);" + "\n"
        str += "                    }" + "\n"
        str += "                }" + "\n"
        str += "            }" + "\n"
        return str
    
    def ___decodeParamList(self,key):
        str = ""
        str += "            if (jsonObj.has(\"" + key+"\")) {" + "\n"
        str += "                " + key + " = new ArrayList<>();" + "\n"
        str += "                JSONArray listArray = jsonObj.getJSONArray(\"" + key + "\");" + "\n"
        str += "                for (int i = 0; i < listArray.length(); i++) {" + "\n"
        str += "                    Object obj = listArray.get(i);" + "\n"
        str += "                    if (obj instanceof String) {" + "\n"
        str += "                        " + key + ".add((String) obj);" + "\n"
        str += "                    }else if(obj instanceof Integer) {" + "\n"
        str += "                        Integer value = (Integer)obj;" + "\n"
        str += "                        " + key + ".add(value.intValue());" + "\n"
        str += "                    }else if(obj instanceof Double) {" + "\n"
        str += "                        Double value = (Double)obj;" + "\n"
        str += "                        " + key + ".add(value.doubleValue());" + "\n"
        str += "                    }else if(obj instanceof  Boolean) {" + "\n"
        str += "                        Boolean value = (Boolean) obj;" + "\n"
        str += "                        " + key + ".add(value.booleanValue());" + "\n"
        str += "                    }else {" + "\n"
        str += "                        RLog.w(TAG,\"无法识别 list 内的类型，被强转为 String: index = \" + i);" + "\n"
        str += "                        " + key + ".add((String)obj);" + "\n"
        str += "                    }" + "\n"
        str += "                }" + "\n"
        str += "            }" + "\n"
        return str
    
    def __getParcelReadKey(self,value):
        if value == Util.Param.Bool:
            return "readIntFromParcel"
        elif value == Util.Param.Int:
            return "readIntFromParcel"
        elif value == Util.Param.Double:
            return "readDoubleFromParcel"
        elif value == Util.Param.String:
            return "readFromParcel"
        elif value == Util.Param.Map:
            return "readMapFromParcel"
        elif value == Util.Param.List:
            return "readListFromParcel"
        else :
            return "unknown __getParcelReadKey"
    
    def __genGetter(self,key,value):
        str = ""
        str += "    public " + self.convertParamType(value) + " get" + self.___upperFirstLetter(key) + "() {" + "\n"
        str += "        return " + key + ";" + "\n"
        str += "    }" + "\n"
        return str + "\n"

    def __genSetter(self,key,value):
        str = ""
        str += "    public void set" + self.___upperFirstLetter(key) + "(" + self.convertParamType(value) + " " + key + ") {" + "\n"
        str += "        this." + key + " = " + key + ";" + "\n"
        str += "    }" + "\n"
        return str + "\n"

    def ___upperFirstLetter(self,key):
        return "".join(key[:1].upper()+key[1:])