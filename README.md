# taobaoSpider
获取淘宝用户的信息，主要内容包括：登录页面破解、个人中心的信息获取等。

主要配置环境在requirements.txt中

### 1、mitmproxy_.py

使用mitmproxy作为代理服务器，修改一些配置，使淘宝的服务器检测不到selenium。从而达到破解验证码的效果。在terminal中使用mitmweb -s mitmproxy_.py 命令启动文件。

### 2、login.py

**功能**：破解淘宝登录界面，输入账号和密码即可登录。

**难点**：有的时候输入账号和密码后，可能还在登录界面还需要在输入一次密码。使用try except finally解决。

parse_html 解析网页的源码，主要是在子类中实现该功能。

### 3、userinfos.py

**功能**：获取用户的基本信息。

| userinfos中的keys |      解释      | 示例 |
| :---------------: | :------------: | :--: |
|       nick        | 用户的淘宝昵称 |      |
|       email       |   绑定的邮箱   |      |
|   phone_number    |  绑定的手机号  |      |
|     real_name     |    真实姓名    |      |
|        sex        |      性别      |      |
|       birth       |    出生日期    |      |

**难点**：用户的性别比较难判断。需要判断性别中的check属性是否存在。使用xpath选择属性。判断规则为：if checked = “”

### 4、deliverAddress.py

功能：获取用户的收货地址。

用户的地址可能有多个。deliverAddress={"0":{},"1":{},...}，deliveraddress的values是一个字典。

| 字典中的keys |    解释    | 示例 |
| :----------: | :--------: | :--: |
|   default    | 是否是默认 |      |
|     name     |    姓名    |      |
|   province   |    省份    |      |
|     city     |    城市    |      |
|   address    |    地区    |      |
| full_address |  详细地址  |      |
|   zip_code   |    邮编    |      |
|   phone_no   |    电话    |      |

**难点**：

1、地址的切分

2、是否是默认地址的判断

### 5、tradedetail.py

**功能**：获取用户最近6个月的交易信息

tradedetails = {"0":{},"1":{},,,}，tradedetails中的每一个value也是一个字典。

|   字典中的keys   |     解释     | 示例 |
| :--------------: | :----------: | :--: |
| trade_createtime |   交易时间   |      |
|     trade_id     |   订单编号   |      |
| seller_shopname  |   商家名称   |      |
|     quantity     |   商品数量   |      |
|   trade_status   |   交易状态   |      |
|     item_url     |   商品地址   |      |
|     item_id      |    商品id    |      |
|     item_pic     | 商品图片地址 |      |
|    item_name     |   商品名称   |      |
|     original     |   商品原价   |      |
|    actual_fee    |   实际价格   |      |
|    trade_text    | 交易中文状态 |      |

**难点**：

1、点击下一页的按钮，直接获取会报错，not clicked...  。需要使用下面代码实现点击下一页。

```python
nextBtn = self.driver.find_element_by_xpath('//*[@id="tp-bought-root"]/div[3]/div[2]/div/button[2]')
self.driver.execute_script("arguments[0].scrollIntoView()",nextBtn)
nextBtn.click()
```

2、隐形等待时间和自定义休息时间加上，不然可能会出现重复获取的情况。

3、时间的判断使用dateutil.parser工具。

4、点击到订单详情页面后，获取详细的交易信息。？？？尚未解决。