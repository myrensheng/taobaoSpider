from bs4 import BeautifulSoup
from lxml import etree

from restruct_taobao.login import Login


class DeliverAddress(Login):
    """
    用户的收货地址
    default：是否是默认地址，name：姓名，province：省份city：城市
    address：地区，full_address：纤细地址，zip_code：邮编，phone_no：电话
    """
    deliveraddress = {}

    def parse_html(self):
        # 点击进入安全设置
        self.driver.find_element_by_xpath('//*[@id="J_MtMainNav"]/li[2]').click()
        # 点击进入收货地址界面
        self.driver.find_element_by_id("newDeliverAddress").click()
        deliver_address = self.driver.page_source
        self.parse_deliver_address(deliver_address)

    def parse_deliver_address(self, deliver_address):
        """
        解析用户的收货地址
        """
        soup = BeautifulSoup(deliver_address, "lxml")
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
            self.deliveraddress["da" + str(rows.index(row) + 1)] = one_address


if __name__ == '__main__':
    dd = DeliverAddress()
    print(dd.deliveraddress)