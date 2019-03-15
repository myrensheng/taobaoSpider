import random
import time

from restruct_taobao import ACCOUNT,PASSWORD

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


LOGIN_URL = "https://login.taobao.com/"


class Login(object):
    
    def __init__(self):
        self.driver = self.ChromeDriverBrowser()
        self.rest = random.randint(2, 5)
        self.login()

    def ChromeDriverNOBrowser(self):
        """
        使用无界面的浏览器
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        return driver

    def ChromeDriverBrowser(self):
        """
        使用有界面的浏览器
        """
        driver = webdriver.Chrome()
        return driver

    def login(self):
        """
        登录用户的淘宝账号
        """
        self.driver.get(LOGIN_URL)  # 进入淘宝登录界面
        # 点击账号密码登录
        self.driver.find_element_by_xpath('//*[@id="J_QRCodeLogin"]/div[5]/a[1]').click()
        time.sleep(self.rest)
        # 输入账号
        self.driver.find_element_by_xpath('//*[@id="TPL_username_1"]').send_keys(ACCOUNT)
        time.sleep(self.rest)
        # 输入密码
        self.driver.find_element_by_xpath('//*[@id="TPL_password_1"]').send_keys(PASSWORD)
        time.sleep(self.rest)
        # 点击登录
        self.driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').click()
        time.sleep(self.rest)
        # 点击登陆后可能会出现再次输入密码的情况
        try:
            # 输入密码
            self.driver.find_element_by_xpath('//*[@id="TPL_password_1"]').send_keys(PASSWORD)
            time.sleep(self.rest)
            # 点击登录
            self.driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').click()
        except Exception as e:
            pass
        finally:
            time.sleep(self.rest)
            try:
                self.parse_html()
            except Exception:
                print("账号或密码错误！")
                self.driver.quit()

    def parse_html(self):
        pass
