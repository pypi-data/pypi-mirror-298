import kytest

from page.adr_page import AdrPage


@kytest.story('测试demo')
class TestAdrDemo(kytest.AdrTC):
    def start(self):
        self.dp = AdrPage(self.dr)

    @kytest.title('进入设置页')
    def test_go_setting(self):
        self.start_app()
        if self.dp.adBtn.exists():
            self.dp.adBtn.click()
        self.dp.myTab.click()
        self.dp.setBtn.click()
        self.shot("设置页", delay=3)
        self.stop_app()




