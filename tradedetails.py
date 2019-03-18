import datetime
from dateutil.parser import parse

from bs4 import BeautifulSoup
from lxml import etree

from restruct_taobao.login import Login


class TradeDetails(Login):
    now_time = datetime.datetime.now()
    tradedetails = {}

    def parse_html(self):
        # 点击已买到的宝贝
        self.driver.find_element_by_xpath('//*[@id="bought"]').click()
        trade_html = self.driver.page_source
        self.parse_trade(trade_html)

    def parse_trade(self, trade_html):
        """
        解析交易信息
        """
        html = etree.HTML(trade_html)

        # 找出每一页中的交易商品数量
        soup = BeautifulSoup(trade_html, 'lxml')
        class_attr = 'bought-table-mod__table___3u4gN bought-wrapper-mod__table___3xFFM'
        tables = soup.find_all("table", class_=class_attr)  # 所有交易的信息
        # length = len(tables)  # 长度为每一页的交易数量
        for table in tables:
            tradedetails = {}
            html = etree.HTML(str(table))
            trade_createtime = html.xpath('*//tbody[1]/tr/td[1]/label/span[2]/text()')[0]
            if self.judge_time(trade_createtime):
                tradedetails['trade_createtime'] = trade_createtime
                tradedetails['trade_id'] = html.xpath('*//tbody[1]/tr/td[1]/span/span[3]/text()')[0]
                tradedetails['seller_shopname'] = html.xpath('*//tbody[1]/tr/td[2]/span/a/text()')[0]
                actual_fee = html.xpath('*//tbody[2]/tr[1]/td[5]/div/div[1]/p/strong/span[2]/text()')[0]
                tradedetails['actual_fee'] = float(actual_fee) * 100
                tradedetails['trade_status'] = html.xpath('*//tbody[2]/tr[1]/td[6]/div/p/span/text()')[0]
                self.tradedetails[str(tables.index(table))] = tradedetails
            else:
                break

    def judge_time(self,trade_createtime):
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
