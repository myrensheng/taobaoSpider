from bs4 import BeautifulSoup
from lxml import etree
from restruct_taobao.login import Login


class Userinfos(Login):
    """
    用户的基本信息
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
        infos = ["authentication","login_password","pwd_protect","phone_bind"]
        settings = ["已完成","已设置","已设置","已绑定"]
        for i in range(1,5):
            xpath_str = '//*[@id="main-content"]/dl/dd[3]/ul/li[{}]/div[1]/span/text()'.format(i)
            self.userinfos[infos[i-1]] = 'true' if html.xpath(xpath_str)[0] == settings[i-1] else 'false'

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
        html = etree.HTML(alipay)
        self.userinfos['alipay'] = html.xpath('//*[@id="main-content"]/div/div[2]/div/div[2]/h3/span/text()')[0]
        pass


if __name__ == '__main__':
    user = Userinfos()
    print(user.userinfos)
