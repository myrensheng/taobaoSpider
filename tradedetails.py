from lxml import etree

from restruct_taobao.login import Login


class TradeDetails(Login):
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
        select_list = ['//*[@id="tp-bought-root"]/div[{}]/div/table'.format(i) for i in range(4, 19)]
        for select in select_list:
            tradedetails = {}
            tradedetails['trade_createtime'] = html.xpath(select + '/tbody[1]/tr/td[1]/label/span[2]/text()')[0]
            tradedetails['trade_id'] = html.xpath(select + '/tbody[1]/tr/td[1]/span/span[3]/text()')[0]
            tradedetails['seller_shopname'] = html.xpath(select + '/tbody[1]/tr/td[2]/span/a/text()')[0]
            actual_fee = html.xpath(select + '/tbody[2]/tr[1]/td[5]/div/div[1]/p/strong/span[2]/text()')[0]
            tradedetails['actual_fee'] = float(actual_fee) * 100
            tradedetails['trade_status'] = html.xpath(select + '/tbody[2]/tr[1]/td[6]/div/p/span/text()')[0]
            self.tradedetails[str(select_list.index(select))] = tradedetails


if __name__ == '__main__':
    trade = TradeDetails()
    print(trade.tradedetails)
