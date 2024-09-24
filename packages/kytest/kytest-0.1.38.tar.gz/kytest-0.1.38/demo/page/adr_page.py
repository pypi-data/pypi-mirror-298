"""
@Author: kang.yang
@Date: 2024/9/14 09:44
"""
from kytest import Page, AdrElem


class AdrPage(Page):
    adBtn = \
        AdrElem(rid='com.qizhidao.clientapp:id/bottom_btn')
    myTab = \
        AdrElem(xpath='//android.widget.FrameLayout[4]')
    spaceTab = \
        AdrElem(text='科创空间')
    setBtn = \
        AdrElem(rid='com.qizhidao.clientapp:id/me_top_bar_setting_iv')
    title = \
        AdrElem(rid='com.qizhidao.clientapp:id/tv_actionbar_title')
    agreeText = \
        AdrElem(rid='com.qizhidao.clientapp:id/agreement_tv_2')
    moreService = \
        AdrElem(xpath='//*[@resource-id="com.qizhidao.clientapp:id/layout_top_content"]'
                      '/android.view.ViewGroup[3]/android.view.View[10]')
