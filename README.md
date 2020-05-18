# 表情包检索系统

信息存储与检索课程 检索项目实验



## 2020-0517

### 上次工作总结

- 停用词表和w2v模型已经找到（李总说看起来效果挺好的，但还没有用）
- 切词效果大家觉得如何
- 万恶的CNN在李总呕心沥血配置tensorflow失败之后使用tourch配置成功，已经可以运行
- 数据库还没有确定，有点拿不准，群里有空了讨论一下吧
- flask框架基本搭好，数据库部分还没定下来



### 接下来的工作

首先说一下大家如果要在自己的电脑上运行项目的话需要做什么

建立虚拟环境（不用虚拟环境很容易导致包出错）

```bash
# 以下是命令行操作，命令为美元符$后面的语句
# 井号是注释，macOS同学一定要注意python2和python3的问题，一般来说所有pip都应该改成pip3

# 安装 virtualenv 库（虚拟环境），如果你没有安装过的话
$ pip install virtualenv

# 切换到我们的项目地址
$ cd xxxxxx/ISRproject

# 建立虚拟环境
$ virtualenv venv

# 激活虚拟环境 macOS
$ source venv/bin/activate
# 激活虚拟环境 windows
$ venv\Scripts\activate

# 激活成功后你的命令行会变成
(venv) $ xxxxx

# =============下面配环境

# 安装所有依赖库（有虚拟环境后macOS同学可以不用写pip3了）
(venv) $ pip install -r requirements.txt
# 这里花时间可能会很长，建议翻墙（pytorch模块不翻墙很可能装不上）

# 安装完之后就可以启动项目了（现在项目很不完整，没啥好看的，主要是给前端同学用来调试）
(venv) $ python app/app.py
# 命令行会输出类似下面的命令
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 311-217-084
# 浏览器输入 http://127.0.0.1:8080 就可以访问项目了
```

另外，CNN的模型比较大，不放git了，[在这个链接](https://lanzous.com/icpnpsd)下载后解压，把`net_best.pth`放入`app/main/retrieval/models/`这个文件夹。



#### 前端同学

前端同学需要开始使用jinja模板进行开发，强烈建议前端同学使用pycharm，他有对jinja模板的支持（自动补全），sublime text等我不确定有没有。

- jinja金笑缘已经改了一部分，有空的时候金笑缘直接电话跟前端同学沟通一下大概的使用方式。

- 接口格式如下：==你们觉得还需要加一些内容吗（比如情境什么的）==

  ```python
  success=1 # 1成功 0后端发生错误
  query_mode=2 # 1表示用户发起的是文本检索，2表示图片检索
  query_info='query/query.jpg' # 文本检索为检索式，图片检索为检索图片后台保存的路径(均在static文件夹下)
  length=2 # 检索结果数量
  data=[
    {
      'name': '0001.jpg',
      'src_path': 'static/bqbSource/0001.jpg',
      'score': 78.8,
      'description': 'it is a description',
      'role': ['熊猫头', '黄脸'],
      'emotion': ['开心', '愤怒'],
      'style': ['沙雕', '睿智'],
      'topic': ['怼人']
    },
    {
      'name': '0002.jpg',
      'src_path': 'static/bqbSource/0002.jpg',
      'score': 71.2,
      'description': 'it is a description',
      'role': ['熊猫头', '黄脸'],
      'emotion': ['开心', '愤怒'],
      'style': ['沙雕', '睿智'],
      'topic': ['怼人']
    },
  ]
  ```

- 前端需要完善的功能

  - 分页
  - 选择器
  - 图片上传
  - 图片上传完成后也要在页面展示
  - 尺寸的适配
  - 更多的展开

#### 后端

==先讨论下数据库的结构吧。==

具体要做的就是

- 切词
- 同义词、停用词控制（已经有词表了）
- 近义词控制（word2vector）
- 倒排档的制作（真的用tfidf吗）

------

## 2020-0508 分工

#### 董：找停用词表，找word2vector模型

停用词表不详细说了，说一下word2vector：

- 说明：word2vector类似一个由许多词组成的二维矩阵，涵盖了每个词之间的相关性，实际结构不一定是矩阵。它用来进行近义控制。

- 目标：
  - 输入一个词，输出和这个词相关性大于某个值（比如0.8，这个系数需要可调节）的所有词的列表。
  - 大概调试一下，看看上面所说的阈值取值多少的情况下输出结果数量比较合适。
- 参考：[一个别人做好的w2v模型](https://www.jianshu.com/p/ae5b45e96dbf)，详情请咨询李总

#### 陈：切词

- 说明：给图片描述做切词，用jieba。
- 目标
  - 暂时不用导到数据库因为数据库结构还没有，先输出成txt或者csv看看切词的效果
  - 需要具备**自定义词典的功能**（就是我们可以输入自己定义的词典，让jieba可以认识“蕉绿”这种词），初步只需要具备词典功能，不需要有明确的词典，词典之后一起讨论。
- 参考：[jieba的一个实例](https://blog.csdn.net/liukuan73/article/details/80462922)
- 扩展：目标1做出结果先在群里讨论一下，如果需要则针对一些特例进一步纠正（比如问号、感叹号，调研一下jieba自定义词典的功能）

#### 李：CNN和数据库

- 目标
  - 图片匹配图片的CNN算法，确定好模型，做到可以用一张图片去获取图库中最相似的图片
  - 数据库的构建尽量实时在群里汇报/讨论

#### 金：flask基本框架

- 目标
  - flask服务器的基本调用
  - 给前端写好调用的程序和接口数据，方便前端调试
  - 建好数据库后进行数据库统一查询接口的编写，方便调用



分工的原则：尽量确保每个模块独立，任务量如果分工不妥当，随时调整。

------



# 主要工作分类

- 前端编写（2个人？）
- 后端编写（2个人？）
- 框架管理（前后端接口、数据库、测试）（1个人？）
- 算法和功能（1个人？）

使用python3 flask架构，可以算是MVC吧



# 项目结构（大概）

```
ISRproject/  <-- 根目录
|
+- conf/                 <-- 配置文件（比如数据库参数啥的）
|
+- dist/                 <-- 打包目录（部署的时候的事情）
|
+- www/                  <-- Web目录，存放.py文件
|  |
|  +- static/            <-- 存放静态文件（比如4000张表情包）
|  |
|  +- templates/         <-- 存放前端模板文件
```



# 前端编写

大约需要2人左右。总共两个页面，一个是检索入口页面，一个是结果展示页面。所谓的前端和UI还是不一样的，更多的工作其实还是写js来实现交互功能。

- 页面具体功能见线框图

#### 使用的技术

- `html/css/javascript`（JS部分可能需要使用jQuery等库，这个由前端同学来决定就行，独立的。）
- `python3 flask web架构中的 jinja2 模板` （html模板，供后端渲染数据）

#### 可能需要学习的知识

- `python jinja2 `的原理（本质上就是html，加上`控制结构 {% %}`，`变量取值 {{ }}`，`注释 {# #}`这几个用来更方便渲染、有助于前后端分离的功能性语句）

  - [这个教程](https://www.cnblogs.com/dachenzi/p/8242713.html)比较简洁

  - 最好还是全面了解一下[python的flask使用jinja模板的具体原理](https://www.liaoxuefeng.com/wiki/1016959663602400/1017806952856928)

#### 接口

主要需要跟后端交互的数据有

- 发给后端：检索式
- 发给后端：图片（可以用base64来传图片）

- 每个（检索到的）表情包的全套信息，以及相关系数的信息（用来排序）

用flask的话，前端模板的测试还是要用python来进行的，具体见上面的教程，核心的渲染就是这么一个flask的函数：

```python
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/query', methods=['POST']) # 这里是设置路由，意思就是说如果浏览器要访问/query这个网页，我就执行下面这个query函数
def query():
  query_str = request.form['query'] # 前端页面发送post请求时会带有一些参数
  query_mode = request.form['queryMode']
  return render_template('result.html', message='success', imageData=getResult(query)) # return就是请求返回的返回
```

##### 接口数据格式（暂定）

form['query'] `是前端的请求参数中的检索式，前端请求结构大概这样（用json表示）：

```json
{
    "queryMode":"",
    "query":"",
    "picContent":""
}
```

模板的返回数据用json来表示应该是这样

```json
{
    "message":"seccess",
    "imageData":[
        {
            "picId":"",
            "picName":"",
            "picType":"",
            "picRole":[

            ],
            "picStyle":[

            ],
            "picDescription":"",
            "rankValue":10
        }
    ]
}
```



# 后端编写（还不太完善）

大约需要2个人实现后端算法

后端太复杂了，flask我也还不熟悉，怎么架构还没确定，先把需要实现的功能梳理一下吧，领锅的人可以先独立地函数，前提是“后端1”要尽快完成

#### 后端0 编写web框架

可以让管理框架的人做一下，需要系统学一下flask



#### 后端1 和数据库交互（ORM框架）

- 用`sqlalchemy`来实现数据库关系和python类的映射关系，产生通用的数据库的接口，供所有后端使用



#### 后端2 切词

- 使用jieba等工具对检索式和图片实现切词功能
- 对切词结果进行评价，效果不好还需要手工修改



#### 后端3 标引

- 切词：同“后端2”
- 使用tf-idf处理切词结果



#### 后端4 词表

- 使用word2vec建立相关词表
- 扩充现有的词表



#### 后端5 处理检索式

- 去停用词
- 切词（见“后端2”）



#### 后端6 倒排档

- 建立倒排档
- 根据检索式去匹配倒排档



#### 后端7 以图搜图

这个部分比较独立，暂时不展开了，使用CNN，也要建数据表



#### 后端8 图文结合

算法还未确定



# 框架管理

### 前后端接口、测试

- 考虑接口规范
- 编写测试样例（上面的接口写的还很粗糙）
- 整理代码结构

### 数据库管理

- 考虑为倒排档、建表



# 算法和功能

主要是要考虑图文结合的问题
