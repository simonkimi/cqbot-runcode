# 运行基于酷Q和glot.io的运行代码机器人

## 活跃编程群气氛用

### 部署
修改config文件的 bot_host和bot_port为机器人cqhttp的地址
```
bot_host = "127.0.0.1"
bot_port = "8080"
group_id = []  # 要在什么群发消息
```

在群内发送信息
```
运行代码 [语言]
内容
```

例如
```
运行代码 python
for i in range(10):
    print("Hello World")
```
