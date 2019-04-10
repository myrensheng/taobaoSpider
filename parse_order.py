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
    """
    解析href以buytertrade开头的订单详情内容
    :param page_source: 网页源码
    :return: 需要的字段信息（字典形式）
    """
    html = etree.HTML(page_source)
    order_detail = {}
    info_xpath_1 = '//*[@id="detail-panel"]/div/div[5]/div/div/div/div'  # 订单信息
    info_xpath_2 = '//*[@id="J_TabView"]/div/div/div'
    if html.xpath(info_xpath_1):
        try:
            trade_id_xpath = '/div[3]/div[1]/div[2]/span[1]/span[2]/span/text()'
            order_detail['trade_id'] = html.xpath(info_xpath_1 + trade_id_xpath)[0]
            deliver_name_phone = html.xpath(info_xpath_1 + '/div[1]/div[1]/dl[1]/dd/text()')[0]
            order_detail['deliver_name'] = deliver_name_phone.split('，')[0]
            order_detail['deliver_mobilephone'] = deliver_name_phone.split('，')[-1]
            trede_success_time_xpath = '/div[3]/div[1]/div[2]/span[5]/span[2]/span/text()'
            order_detail['trede_success_time'] = html.xpath(info_xpath_1 + trede_success_time_xpath)[0]
        except Exception as e:
            # print("info_xpath_1",e)
            pass
    # 可能出现需要的信息在不同位置的情况
    elif html.xpath(info_xpath_2):
        try:
            trade_id_xpath = '/table[1]/tbody[2]/tr[3]/td[1]/span[2]/text()'
            order_detail['trade_id'] = html.xpath(info_xpath_2+trade_id_xpath)[0]
            trede_success_time_xpath = '/table[1]/tbody[2]/tr[4]/td[1]/span[2]/text()'
            order_detail['trede_success_time'] = html.xpath(info_xpath_2 + trede_success_time_xpath)[0]
            deliver_name_phone = html.xpath(info_xpath_2+'/table[2]/tbody/tr[3]/td[2]/text()')[0]
            order_detail['deliver_name'] = deliver_name_phone.split(' ')[0].strip()
            order_detail['deliver_mobilephone'] = deliver_name_phone.split(' ')[1].strip()
        except Exception as e:
            # print("info_xpath_2",e)
            pass
    return order_detail


def parse_tradetmall(page_source):
    html = etree.HTML(page_source)
    order_detail = {'name': 'zs'}
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
