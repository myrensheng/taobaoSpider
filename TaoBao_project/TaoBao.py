import pymongo
import random
import time
from datetime import datetime

from bs4 import BeautifulSoup
from dateutil.parser import parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from restruct_taobao.parse_order import *

LOGIN_URL = "https://login.taobao.com/"
# CHROME_DRIVER = ""
MONGODB_USER = ""
MONGODB_PASSWORD = ""
MONGODB_IP = ""
MONGODB_PORT = ""
MONGODB_CONN = "mongodb://"+MONGODB_USER+":"+MONGODB_PASSWORD+"@"+MONGODB_IP+":"+MONGODB_PORT+"/"


class User:
    """
    交易信息的详情页获取待完善...
    """
    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.userinfos = {}
        self.deliveraddress = {}
        self.tradedetails = {}
        self.order_href = {}
        self.order_detail = {}
        self.user_all_info = {}
        self.now_time = datetime.now()
        # self.driver = self.chrome_driver_browser()
        self.driver = self.chrome_driver_no_browser()
        self.rest = random.randint(2, 5)
        self.login()

    @staticmethod
    def chrome_driver_no_browser():
        """
        使用无界面的浏览器
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--proxy-server=http://127.0.0.1:9000')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        return driver

    @staticmethod
    def chrome_driver_browser():
        """
        使用有界面的浏览器
        """
        chrome_options = Options()
        chrome_options.add_argument('--proxy-server=http://127.0.0.1:9000')
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def login(self):
        """
        登录用户的淘宝账号
        """
        self.driver.get(LOGIN_URL)  # 进入淘宝登录界面
        # 点击账号密码登录
        print("使用账号密码登录...")
        self.driver.find_element_by_xpath('//*[@id="J_QRCodeLogin"]/div[5]/a[1]').click()
        time.sleep(self.rest)
        # 输入账号
        print("输入账号中...")
        self.driver.find_element_by_xpath('//*[@id="TPL_username_1"]').send_keys(self.account)
        time.sleep(self.rest)
        # 输入密码
        print("输入密码中...")
        self.driver.find_element_by_xpath('//*[@id="TPL_password_1"]').send_keys(self.password)
        time.sleep(self.rest)
        # 点击登录
        self.driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').click()
        time.sleep(self.rest)
        print("登录中...")
        # 点击登陆后可能会出现再次输入密码的情况
        try:
            # 输入密码
            print("再次输入密码...")
            self.driver.find_element_by_xpath('//*[@id="TPL_password_1"]').send_keys(self.password)
            time.sleep(self.rest)
            # 点击登录
            print("登录中...")
            self.driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').click()
        except Exception as e:
            # print(e)
            pass
        finally:
            time.sleep(self.rest)
            try:
                self.start_spider()
                self.driver.quit()
            except Exception as e:
                print(e)
                print("账号或密码错误！")
                self.driver.quit()

    def start_spider(self):
        print("登录成功...")
        print("正在获取用户基本信息")
        self.user_info()
        time.sleep(0.5)
        print("正在获取收货地址")
        self.deliver_address()
        time.sleep(0.5)
        print("正在获取交易信息")
        self.trade_details()
        time.sleep(0.5)
        print("正在整理信息...")
        self.all_info()
        print("数据保存到mongodb中...")
        self.save_mongodb()

    # 用户的基本信息
    def user_info(self):
        # 进入账号设置
        self.driver.find_element_by_xpath('//*[@id="J_MtMainNav"]/li[2]').click()
        security_settings = self.driver.page_source
        self.parse_security_settings(security_settings)
        # 进入个人交易信息(Personal transaction information)
        self.driver.find_element_by_xpath('//*[@id="newAccountProfile"]').click()
        pti = self.driver.page_source
        self.parse_pti(pti)
        # 支付宝绑定页面
        self.driver.find_element_by_xpath('//*[@id="newAccountManagement"]').click()
        alipay = self.driver.page_source
        self.parse_alipay(alipay)

    def parse_security_settings(self, page_source):
        """
        从安全信息中获取到 nick，email，phone_number，authentication，
        login_password，pwd_protect，phone_bind
        """
        soup = BeautifulSoup(page_source, 'lxml')
        account_info = soup.find_all("span", class_="default")
        self.userinfos["nick"] = account_info[0].string.strip() if account_info[0].string else "无"
        self.userinfos["email"] = account_info[1].string.strip() if account_info[1].string.strip() else "无"
        phone_number = account_info[2].string.strip() if account_info[2].string.strip() else "无"
        self.userinfos["phone_number"] = phone_number
        html = etree.HTML(page_source)
        # 安全等级
        security_level = html.xpath('//*[@id="main-content"]/dl/dd[2]/div/div/div[1]/span/text()')[0]
        self.userinfos['security_level'] = security_level
        # 身份认证,登录密码,密保问题,绑定手机
        infos = ["authentication", "login_password", "pwd_protect", "phone_bind"]
        settings = ["已完成", "已设置", "已设置", "已绑定"]
        for i in range(1, 5):
            xpath_str = '//*[@id="main-content"]/dl/dd[3]/ul/li[{}]/div[1]/span/text()'.format(i)
            self.userinfos[infos[i - 1]] = 'true' if html.xpath(xpath_str)[0] == settings[i - 1] else 'false'

    def parse_pti(self, pti):
        """
        从个人交易信息中获取到 birth，sex
        """
        html = etree.HTML(pti)
        self.userinfos["real_name"] = html.xpath('//*[@id="ah:addressForm"]/li[1]/strong/text()')[0]
        year_ = html.xpath('//*[@id="ah:addressForm"]/li[4]/input[1]/@value')[0]
        month_ = html.xpath('//*[@id="ah:addressForm"]/li[4]/input[2]/@value')[0]
        day_ = html.xpath('//*[@id="ah:addressForm"]/li[4]/input[3]/@value')[0]
        birth = year_ + "-" + month_ + "-" + day_
        self.userinfos["birth"] = birth
        # 性别字段的获取
        select_list = ['//*[@id="ah:addressForm"]/li[3]/span[{}]/input/@checked'.format(i) for i in range(2, 5)]
        sex_ = ["1", "2", "0"]  # 1-男，2-女，0-保密
        for s in select_list:
            try:
                checked = html.xpath(s)[0]
                if checked == '':
                    sex = sex_[select_list.index(s)]
                    self.userinfos['sex'] = sex
                    break
            except IndexError:
                pass
                continue

    def parse_alipay(self, alipay):
        """
         从支付宝中获取到绑定的支付宝账号
        """
        html = etree.HTML(alipay)
        alipay_xpath = '//*[@id="main-content"]/div/div[2]/div/div[2]/h3/span/text()'
        self.userinfos['alipay_account'] = html.xpath(alipay_xpath)[0]

    # 用户的收货地址
    def deliver_address(self):
        # 点击进入安全设置
        self.driver.find_element_by_xpath('//*[@id="J_MtMainNav"]/li[2]').click()
        # 点击进入收货地址界面
        self.driver.find_element_by_id("newDeliverAddress").click()
        deliver_address_html = self.driver.page_source
        self.parse_deliver_address(deliver_address_html)

    def parse_deliver_address(self, html):
        """
        解析用户的收货地址
        """
        soup = BeautifulSoup(html, "lxml")
        tbody = soup.find("tbody", attrs={"class": "next-table-body"})
        rows = tbody.find_all("tr", attrs={"role": "row"})  # 每一行的数据
        for row in rows:
            one_address = {}
            html = etree.HTML(str(row))
            address_ = html.xpath("*//tr[1]/td[2]/div/span/text()")[0]
            address_list = address_.split(" ")
            one_address["province"] = address_list[0].split("省")[0]
            one_address["city"] = address_list[1].split("市")[0]
            one_address["address"] = address_list[2]
            # 判断是否是默认地址
            default = html.xpath("*//tr[1]/td[7]/div/div/span/text()")[0]
            if default == "默认地址":
                default = "true"
            else:
                default = "false"
            one_address["default"] = default
            one_address["name"] = html.xpath("*//tr[1]/td[1]/div/text()")[0]
            one_address["full_address"] = html.xpath("*//tr[1]/td[3]/div/text()")[0]
            one_address["zip_code"] = html.xpath("*//tr[1]/td[4]/div/text()")[0]
            one_address["phone_no"] = html.xpath("*//tr[1]/td[5]/div/span/text()")[0]
            self.deliveraddress[str(rows.index(row) + 1)] = one_address

    # 用户的交易信息
    def trade_details(self):
        # 点击到达首页
        self.driver.find_element_by_xpath('//*[@id="J_MtMainNav"]/li[1]').click()
        # 点击已买到的宝贝
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath('//*[@id="bought"]').click()
        shop_num = 0
        trade_html = self.driver.page_source
        # 获取交易信息
        result = self.parse_trade(trade_html, shop_num)
        if not result:  # 第一页数据获取完成，继续点击下一页
            while True:
                time.sleep(self.rest)
                shop_num += 15
                try:
                    # 如果点击到最后一页，交易信息仍在6个月内，会报错
                    self.driver.implicitly_wait(10)
                    next_btn_xpath = '//*[@id="tp-bought-root"]/div[3]/div[2]/div/button[2]'
                    next_btn = self.driver.find_element_by_xpath(next_btn_xpath)
                    self.driver.execute_script("arguments[0].scrollIntoView()", next_btn)
                    next_btn.click()
                    time.sleep(self.rest)
                    self.driver.implicitly_wait(10)
                    trade_html = self.driver.page_source
                    result = self.parse_trade(trade_html, shop_num)
                except Exception as e:
                    print("翻页循环获取交易信息", e)
                    break
                if result:  # 解析结果为false跳出循环
                    break
        # 获取订单详情页的数据
        # self.parse_order_detail()

    def parse_trade(self, trade_html, shop_num):
        """
        解析交易信息
        :param trade_html 网页源码；
        :param shop_num 自定义的商品编号。
        :return True表示获取已完成，结束下一页点击操作；False表示获取未完成，继续点击下一页
        """
        # 找出每一页中的交易商品数量
        soup = BeautifulSoup(trade_html, 'lxml')
        class_attr = 'bought-table-mod__table___3u4gN bought-wrapper-mod__table___3xFFM'
        tables = soup.find_all("table", class_=class_attr)  # 所有交易的信息
        for table in tables:
            tradedetails = {}
            html = etree.HTML(str(table))
            trade_createtime = html.xpath('*//tbody[1]/tr/td[1]/label/span[2]/text()')[0]
            if self.judge_time(trade_createtime):
                tradedetails['trade_createtime'] = trade_createtime
                tradedetails['trade_id'] = html.xpath('*//tbody[1]/tr/td[1]/span/span[3]/text()')[0]
                tradedetails['seller_shopname'] = html.xpath('*//tbody[1]/tr/td[2]/span/a/text()')[0]
                item_url = html.xpath('*//tbody[1]/tr/td[2]/span/a/@href')[0]
                tradedetails['item_url'] = item_url
                tradedetails['item_id'] = item_url.split('=')[-1]
                tradedetails['item_pic'] = html.xpath('*//tbody[2]/tr/td[1]/div/div[1]/a/img/@src')[0]
                item_name_xpath = '*//tbody[2]/tr[1]/td[1]/div/div[2]/p[1]/a[1]/span[2]/text()'
                tradedetails['item_name'] = html.xpath(item_name_xpath)[0]
                actual_fee = html.xpath('*//tbody[2]/tr[1]/td[5]/div/div[1]/p/strong/span[2]/text()')[0]
                actual_fee = round(float(actual_fee) * 100, 1)  # 交易金额按照“分”计算
                try:
                    # 商品未打折价格，有就获取，没有就按照原价
                    origin = html.xpath('*//tbody[2]/tr[1]/td[2]/div/p[1]/del/span[2]/text()')[0]
                    origin = round(float(origin) * 100, 1)  # 交易金额按照“分”计算
                    tradedetails['original'] = origin
                except IndexError:
                    tradedetails['original'] = actual_fee
                tradedetails['actual_fee'] = actual_fee
                tradedetails['quantity'] = html.xpath('*//tbody[2]/tr/td[3]/div/p/text()')[0]
                trade_status_dict = {'等待买家付款': 'WAIT_BUYER_PAY',
                                     '等待卖家发货': 'WAIT_SELLER_SEND_GOODS',
                                     '卖家部分发货': 'SELLER_CONSIGNED_PART',
                                     '等待买家确认收货': 'WAIT_BUYER_CONFIRM_GOODS',
                                     '交易成功': 'TRADE_FINISHED',
                                     '充值成功': 'TRADE_FINISHED',
                                     '交易关闭': 'TRADE_CLOSED',
                                     '交易被淘宝关闭': 'TRADE_CLOSE_BY_TAOBAO',
                                     '没有创建外部交易（支付宝交易）': 'TRADE_NO_CREATE_PAY',
                                     '外卡支付付款确认中': 'PAY_PENDING',
                                     }
                trade_text = html.xpath('*//tbody[2]/tr[1]/td[6]/div/p/span/text()')[0]
                tradedetails['trade_text'] = trade_text
                tradedetails['trade_status'] = trade_status_dict.get(trade_text, "ERROR")
                self.tradedetails[str(shop_num + tables.index(table))] = tradedetails
                order_url = "https:" + html.xpath('//*[@id="viewDetail"]/@href')[0]
                self.order_href[str(shop_num + tables.index(table))] = order_url
            else:
                # 表示交易时间已超过6个月，任务已完成。
                return True
        return False

    def judge_time(self, trade_createtime):
        """
        判断交易是否是在6个月内发生的
        :param trade_createtime: 交易时间
        :return: 是-True，否-False
        """
        days = (self.now_time - parse(trade_createtime)).days
        if days <= 180:
            return True
        else:
            return False

    def parse_order_detail(self):
        """
        解析订单详情页面
        """
        # 根据得到的href，判断需要使用哪个函数解析页面
        parse_method = {
            '//buyertrade': parse_buytertrade,
            '//trade': parse_tradetmall,
            '//train': parse_traintrip,
            '//tradearchive': parse_tradearchive,
            '//diannying': parse_dianying,
        }
        # 循环遍历order_href字典，解析到对应的字段
        for k, v in self.order_href.items():
            start_with = v.split(':')[-1].split('.')[0]
            fun = parse_method.get(start_with, False)
            if fun:  # 有可能没有对应的解析函数
                self.driver.get(v)
                time.sleep(self.rest)
                self.driver.implicitly_wait(10)
                page_source = self.driver.page_source

                # ----------------------------------------------
                result = fun(page_source)
                print(v)
                print(k, result)
                # 将得到的字段更新到tradedetails中
                self.tradedetails[k].update(result)
                # ----------------------------------------------
                # 将解析到的字段放到order_detail中
                # self.order_detail[k] = fun(page_source)
                # print(v)
                # print(k, self.order_detail)
            else:
                print("没有对应解析的函数", start_with)

    def all_info(self):
        """
        将所有信息合并
        """
        self.user_all_info['userinfos'] = self.userinfos
        self.user_all_info['deliveraddress'] = self.deliveraddress
        self.user_all_info['tradedetails'] = self.tradedetails

    def save_mongodb(self):
        client = pymongo.MongoClient(MONGODB_CONN)
        collection = client.TaoBao.users
        result = collection.insert_one(self.user_all_info)
        print(result.inserted_id)


if __name__ == '__main__':
    user_account = ''
    user_password = ''
    user = User(user_account, user_password)
    print(user.user_all_info)
