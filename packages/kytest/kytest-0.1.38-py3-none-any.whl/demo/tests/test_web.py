"""
@Author: kang.yang
@Date: 2023/11/16 17:50
"""
import kytest

from page.pub_page import PubPage


@kytest.story('登录模块')
class TestWebDemo(kytest.WebTC):
    def start(self):
        self.pp = PubPage(self.dr)

    @kytest.title("登录")
    def test_login(self):
        self.pp.login()
        self.assert_url()
        self.shot('首页', delay=3)

