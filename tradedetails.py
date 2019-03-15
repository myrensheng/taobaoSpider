from restruct_taobao.login import Login


class TradeDetails(Login):
    tradedetails = {}

    def parse_html(self):
        # 点击已买到的宝贝
        self.driver.find_element_by_xpath('//*[@id="bought"]').click()
        trade_html = self.driver.page_source
        self.parse_trade(trade_html)
        pass

    def parse_trade(self,trade_html):
        print(trade_html)
        pass


if __name__ == '__main__':
    trade = TradeDetails()