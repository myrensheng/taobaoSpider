# taobaoSpider
获取淘宝用户的信息，主要内容包括：登录页面破解、个人中心的信息获取等。

主要配置环境在requirements.txt中

### 1、mitmproxy_.py

使用mitmproxy作为代理服务器，修改一些配置，使淘宝的服务器检测不到selenium。从而达到破解验证码的效果。在terminal中使用mitmweb -s mitmproxy_.py 命令启动文件。

### 2、userinfos.py





