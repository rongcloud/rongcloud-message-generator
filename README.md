# 融云自定义消息生成器

该脚本支持一键生成`消息 json 模板`，`iOS 自定义消息`和` Android 自定义消息`

请确保在 `python3` 环境下执行脚本，所有输出物在 `output` 目录

**该脚本不支持自定义媒体消息**

> 支持数据类型列表

仅支持如下类型

类型|iOS|Android|类型
:--|:--|:--|:--
bool|BOOL|boolean|基本类型
int|int|int|基本类型
double|double|double|基本类型
string|NSString|String|基本类型
map|NSDictionary|Map|复杂类型
list|NSArray|List|复杂类型

**注：map，list 等复杂数据类型内部仅支持 bool，int，double，string 等四种基本数据类型，业务所需的复杂的数据类型(如商品对象)请自行转换成基本类型的 map**

说明：`该项目只会对 map list 进行根节点数据解析`，但 map 和 list 根据实际业务可能是多层嵌套的，则需要开发者自行进行多层嵌套的解析

> 名词解释

名词|含义
:--|:--
msgName|自定义消息的名字
objName|自定义消息的唯一标识，禁止使用 `RC:` 作为开头，不能超过 16 个字符
persistentFlag|自定义消息的持久化标识，参见下面的含义
package|包名，安卓专用
param|自定义消息的参数列表

`说明1：`json 模板名，iOS 文件名类名，Android 文件名类型和 msgName 完全一致

`说明2：`persistentFlag 取值与其具体含义

值|含义|建议
:--|:--|:--
0|在本地不存储，不计入未读数|可以用作信令消息，用作业务通知
1|在本地只存储，但不计入未读数|
3|在本地进行存储并计入未读数|此类型消息最为常见，如文本，图片，视频等常见消息
16|在本地不存储，不计入未读数，并且如果对方不在线，服务器会直接丢弃该消息，对方如果之后再上线也不会再收到此消息。|一般用于发送输入状态之类的消息，该类型消息的messageUId为nil。

如果 persistentFlag 值设置错误，将无法正确执行脚本

`说明 3：`参数类型设置说明

详见上面的 支持数据类型列表

## 1. 使用 json 模板生成

终端执行命令

```
$ python3 main.py
```

`main.py` 会读取内置的 json 模板文件 `MessageTemplate.json`

按需修改 MessageTemplate.json ，`务必确保模板文件的 json 是合法 json`

消息 json 模板示例如下

```
{
  "msgName": "CustomMessage",
  "objName": "app:cusMsg",
  "persistentFlag": 3,
  "package": "cn.rongcloud.im.im.message",
  "param": {
    "name": "string",
    "uid": "string",
    "isVip" : "bool",
    "age": "int",
    "price": "double",
    "dataMap": "map",
    "dataList": "list"
  }
}
```

## 2. 使用 python 生成

终端执行命令

```
$ python3 main_gen.py
```

按需在 `main_gen.py` 中修改代码

main_gen.py 的代码示例如下

```python
    # 1.构造 MsgObj 对象
    # 参数 1 ：自定义消息名称
    # 参数 2 ：自定义消息标识
    obj = MsgObj("CustomMessage","app:cusMsg")

    # 2.设置消息持久化标识
    obj.setPersistentFlag(Util.Persistent.IsNone)

    # 3.设置消息所在包名 安卓专用
    obj.setPackage("com.test.message")

    # 4.设置参数列表
    # 增加 String 类型参数
    obj.addParamString("name")
    obj.addParamString("uid")
    # 增加 bool 类型参数
    obj.addParamBool("isVip")
    # 增加 int 类型参数
    obj.addParamInt("age")
    # 增加 double 类型参数
    obj.addParamDouble("price")
    # 增加 map 类型参数
    obj.addParamMap("dataMap")
    # 增加 list 类型参数
    obj.addParamList("dataList")

    # 5.打印消息内容
    obj.showDetail()

    # 6.生成消息
    obj.genMsg()
```

## 3.自定义消息的使用

1.将生成的自定义消息代码分别放入 iOS/Android 项目，把`自定义消息注册给 iOS/Android SDK`，这样 SDK 才能正常识别自定义消息

2.如果消息需要在聊天页面展示，开发者需要编写自定义消息的 UI，并将`自定义消息和 UI 进行绑定`

详细请参考[融云官方文档](https://docs.rongcloud.cn)