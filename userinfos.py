from bs4 import BeautifulSoup
from lxml import etree
from restruct_taobao.login import Login


class Userinfos(Login):
    """
    用户的基本信息，userinfos字典形式。
    nick：用户的淘宝昵称，email：绑定的邮箱，phone_number：绑定的手机号
    real_name：真实姓名，sex：性别，birth：生日
    """
    userinfos = {}

    def parse_html(self):
        # 进入账号设置
        self.driver.find_element_by_xpath('//*[@id="J_MtMainNav"]/li[2]').click()
        security_settings = self.driver.page_source
        self.parse_security_settings(security_settings)
        # 进入个人交易信息(Personal transaction information)
        self.driver.find_element_by_xpath('//*[@id="newAccountProfile"]').click()
        pti = self.driver.page_source
        self.parse_pti(pti)

    def parse_security_settings(self, page_source):
        """
        从安全信息中获取到 nick，email，phone_number
        """
        soup = BeautifulSoup(page_source, 'lxml')
        account_info = soup.find_all("span", class_="default")
        nick = account_info[0].string.strip() if account_info[0].string else "无"
        email = account_info[1].string.strip() if account_info[1].string.strip() else "无"
        phone_number = account_info[2].string.strip() if account_info[2].string.strip() else "无"
        self.userinfos["nick"] = nick
        self.userinfos["email"] = email
        self.userinfos["phone_number"] = phone_number

    def parse_pti(self, pti):
        """
        从个人交易信息中获取到 birth，sex
        """
        html = etree.HTML(pti)
        real_name = html.xpath('//*[@id="ah:addressForm"]/li[1]/strong/text()')[0]
        year_ = html.xpath('//*[@id="ah:addressForm"]/li[4]/input[1]/@value')[0]
        month_ = html.xpath('//*[@id="ah:addressForm"]/li[4]/input[2]/@value')[0]
        day_ = html.xpath('//*[@id="ah:addressForm"]/li[4]/input[3]/@value')[0]
        birth = year_ + "-" + month_ + "-" + day_
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
        self.userinfos["real_name"] = real_name
        self.userinfos["birth"] = birth


if __name__ == '__main__':
    user = Userinfos()
    print(user.userinfos)
