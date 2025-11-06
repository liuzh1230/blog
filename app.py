from dotenv import load_dotenv
load_dotenv()

import os
print("FLASK_APP:", os.getenv("FLASK_APP"))
print("FLASK_ENV:", os.getenv("FLASK_ENV"))


from flask import Flask   #这个类表示一个Flask程序
app=Flask(__name__)   #实例化这个类，得到程序实例app
                      #传入的第一个参数是模块或包的名称，这里应该使用特殊变量__name__
                      #python会根据所处的模块赋予该变量相应的值，这里这个值为app

#建立处理请求的函数并定义对应的URL规则
@app.route('/hi')   #app.route()装饰器把根地址/和index()函数绑定起来，当用户访问这个地址时就会触发这个函数
                  #函数返回值将作为响应的主体，一般为呈现在浏览器窗口的HTML界面
#route()装饰器的第一个参数是URL规则，必须以/开始
#这里的URL是相对URL，即不包含域名
@app.route("/hello") #为一个函数绑定多个URL
def say_hello():
    return '<hl>Hello Flask!</hl>'

#动态URL
#在URL中添加变量
@app.route('/greet/<name>')   #类似/greet/foo的请求都会触发这个函数
@app.route('/greet/',defaults={'name':'Programmer'}) 
#defaults:接收一个字典，存储URL变量和默认值的映射
#给变量指定默认值，当输入时未包含变量，则name=Programmer，以避免报错
def greet(name):
    return '<h1>Hello, %s!</h1>' % name  #%s 是 Python 的字符串格式化占位符，意思是“把后面的变量按字符串插入到这里”。


#Flask内置了一个CLI系统，让我们可以在终端中进行启动/停止 Flask 应用等一系列操作
#其中，flask run用于启动内置的服务开发器
#可以使用flask --help 查看所有可用命令
#flask run运行的开发服务器默认监听http://127.0.0.1:5000/地址
#实际上，http://127.0.0.1即localhost，是指向本地机的IP地址，一般用来测试
#flask默认使用5000端口


