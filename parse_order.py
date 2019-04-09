# 针对不同的订单解析出不同的字段
# 目前已知有5中不同的网页

# class ParseOrder():
#     def __init__(self,order_href):
#         self.page_source = order_href
#
#     def get_page_source(self):
#         pass
from lxml import etree


def parse_buytertrade(page_source):
    # print(page_source)
    html = etree.HTML(page_source)
    order_detail = {}
    trade_id_xpath = '//*[@id="detail-panel"]/div/div[5]/div/div/div/div/div[3]/div[1]/div[2]/span[1]/span[2]/span/text()'
    if html.xpath(trade_id_xpath):
        order_detail['trade_id'] = html.xpath(trade_id_xpath)[0]
    deliver_name_phone = html.xpath('//*[@id="detail-panel"]/div/div[5]/div/div/div/div/div[1]/div[1]/dl[1]/dd/text()')
    if deliver_name_phone:
        order_detail['deliver_name'] = deliver_name_phone[0].split('，')[0]
        order_detail['deliver_mobilephone'] = deliver_name_phone[0].split('，')[-1]
    trede_success_time = html.xpath('//*[@id="detail-panel"]/div/div[5]/div/div/div/div/div[3]/div[1]/div[2]/span[5]/span[2]/span/text()')
    if trede_success_time:
        order_detail['trede_success_time'] = [0]
    return order_detail


def parse_tradetmall(page_source):
    # print(page_source)
    html = etree.HTML(page_source)
    order_detail = {'name':'zs'}
    return order_detail
    pass


def parse_traintrip(page_source):
    html = etree.HTML(page_source)
    order_detail = {'name': 'zs'}
    return order_detail



def parse_tradearchive(page_source):
    html = etree.HTML(page_source)
    order_detail = {'name': 'zs'}
    return order_detail


def parse_dianying(page_source):
    html = etree.HTML(page_source)
    order_detail = {'name': 'zs'}
    return order_detail


