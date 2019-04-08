import datetime
import time

from dateutil.parser import parse

from bs4 import BeautifulSoup
from lxml import etree

from restruct_taobao.login import Login


class TradeDetails(Login):
    now_time = datetime.datetime.now()
    tradedetails = {}

    def parse_html(self):
        # 点击已买到的宝贝
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath('//*[@id="bought"]').click()
        shop_num = 0
        trade_html = self.driver.page_source
        result = self.parse_trade(trade_html, shop_num)
        if not result:  # 第一页数据获取完成，继续点击下一页
            while True:
                time.sleep(self.rest)
                shop_num += 15
                try:
                    # 如果点击到最后一页，交易信息仍在6个月内，会报错
                    self.driver.implicitly_wait(10)
                    nextBtn_xpath = '//*[@id="tp-bought-root"]/div[3]/div[2]/div/button[2]'
                    nextBtn = self.driver.find_element_by_xpath(nextBtn_xpath)
                    self.driver.execute_script("arguments[0].scrollIntoView()", nextBtn)
                    nextBtn.click()
                    time.sleep(self.rest)
                    self.driver.implicitly_wait(10)
                    trade_html = self.driver.page_source
                    result = self.parse_trade(trade_html, shop_num)
                except Exception as e:
                    break
                if result:  # 解析结果为false跳出循环
                    break

    def parse_trade(self, trade_html, shop_num):
        """
        解析交易信息
        :param trade_html网页源码；shop_num 自定义的商品编号。
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
                tradedetails['item_name'] = html.xpath('*//tbody[2]/tr[1]/td[1]/div/div[2]/p[1]/a[1]/span[2]/text()')[0]
                actual_fee = html.xpath('*//tbody[2]/tr[1]/td[5]/div/div[1]/p/strong/span[2]/text()')[0]
                actual_fee = round(float(actual_fee) * 100, 1)  # 交易金额按照“分”计算
                try:
                    origin = html.xpath('*//tbody[2]/tr[1]/td[2]/div/p[1]/del/span[2]/text()')[0]
                    origin = round(float(origin) * 100, 1)  # 交易金额按照“分”计算
                    tradedetails['original'] = origin
                except Exception as e:
                    tradedetails['original'] = actual_fee
                tradedetails['actual_fee'] = actual_fee
                tradedetails['quantity'] = html.xpath('*//tbody[2]/tr/td[3]/div/p/text()')[0]
                tradedetails['trade_status'] = html.xpath('*//tbody[2]/tr[1]/td[6]/div/p/span/text()')[0]
                self.tradedetails[str(shop_num + tables.index(table))] = tradedetails
                # 点击进入订单详情页面
                # self.driver.find_element_by_xpath('//*[@id="viewDetail"]/@href').click()
                # 解析订单详情页面的信息

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


if __name__ == '__main__':
    trade = TradeDetails()
    print(trade.tradedetails)
