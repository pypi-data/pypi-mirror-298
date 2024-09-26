import typing

from uiautomator2 import UiObject
from uiautomator2.xpath import XPathSelector

from kytest.utils.log import logger
from kytest.core.adr.driver import Driver


class Elem(object):
    """
    安卓元素定义
    """

    def __init__(self,
                 driver: Driver = None,
                 rid: str = None,
                 class_: str = None,
                 text: str = None,
                 xpath: str = None,
                 index: int = None,
                 watch: list = None):
        """

        @param driver: 安卓驱动
        @param rid: resourceId定位
        @param class_: className定位
        @param text: 文本定位
        @param xpath: xpath定位
        @param index: 识别到多个元素时，根据index获取其中一个
        @param watch: 需要处理的异常弹窗定位方式列表
        """
        self._kwargs = {}
        if rid is not None:
            self._kwargs["resourceId"] = rid
        if class_ is not None:
            self._kwargs["className"] = class_
        if text is not None:
            self._kwargs["text"] = text
        if xpath:
            self._kwargs["xpath"] = xpath
        if index is not None:
            self._kwargs["instance"] = index

        self._driver = driver
        self._xpath = xpath
        self._watch = watch

    def __get__(self, instance, owner):
        """po模式中element初始化不需要带driver的关键"""
        if instance is None:
            return None

        self._driver = instance.driver
        return self

    # 公共方法
    def watch_handler(self):
        """
        异常弹窗处理
        @return:
        """
        logger.info("开始弹窗检测")
        ctx = self._driver.d.watch_context()
        for loc in self._watch:
            ctx.when(loc).click()
        ctx.wait_stable()
        ctx.close()
        logger.info("检测结束")

    def find(self, timeout=5, n=3):
        """
        增加截图的方法
        @param timeout: 每次查找时间
        @param n：失败后重试的次数
        @return:
        """

        _element = self._driver.d.xpath(self._xpath) if \
            self._xpath is not None else self._driver.d(**self._kwargs)

        retry_count = n
        if _element.wait(timeout=timeout):
            logger.info(f"查找成功")
            return _element
        else:
            if retry_count > 0:
                for count in range(1, retry_count + 1):
                    logger.info(f"第{count}次重试...")
                    if self._watch:
                        self.watch_handler()
                    if _element.wait(timeout=timeout):
                        logger.info(f"查找成功")
                        return _element

            logger.info("查找失败")
            self._driver.shot("查找失败")
            raise Exception(f"控件: {self._kwargs}, 查找失败")

    # 属性获取
    def get_text(self):
        logger.info(f"获取文本属性")
        _elem = self.find(timeout=3)
        if isinstance(_elem, XPathSelector):
            elems = _elem.all()
        else:
            elems = list(_elem)
        text = []
        for elem in elems:
            text.append(elem.get_text())

        if len(text) == 1:
            text = text[0]
        return text

    def exists(self, timeout=5):
        logger.info(f"检查控件是否存在")
        result = False
        try:
            _element = self.find(timeout=timeout, n=0)
            result = True
        except:
            result = False
        finally:
            return result

    def count(self, timeout=5):
        return self.find(timeout=timeout).count

    def info(self, timeout=5):
        return self.find(timeout=timeout).info

    def center(self, timeout=5, *args, **kwargs):
        return self.find(timeout=timeout).center(*args, **kwargs)

    @staticmethod
    def _adapt_center(e: typing.Union[UiObject, XPathSelector],
                      offset=(0.5, 0.5)):
        """
        修正控件中心坐标
        """
        if isinstance(e, UiObject):
            return e.center(offset=offset)
        else:
            return e.offset(offset[0], offset[1])

    # 操作
    def click(self, timeout=5):
        logger.info(f"点击 {self._kwargs}")
        element = self.find(timeout=timeout)
        x, y = self._adapt_center(element)
        self._driver.util.click(x, y)
        logger.info("点击完成")

    def long_click(self, timeout=5):
        logger.info(f"长按 {self._kwargs}")
        element = self.find(timeout=timeout)
        x, y = self._adapt_center(element)
        self._driver.long_click(x, y)
        logger.info("点击完成")

    def input(self, text, timeout=5, pwd_check=False):
        logger.info(f"输入文本: {text}")
        self.click(timeout=timeout)
        if pwd_check is True:
            self._driver.d(focused=True).set_text(text)
        else:
            self._driver.util.input(text)
        logger.info("输入完成")

    def clear_text(self, timeout=5, *args, **kwargs):
        logger.info("清空输入框")
        self.find(timeout=timeout).clear_text(*args, **kwargs)

    def screenshot(self, file_path, timeout=5):
        logger.info("截图定位元素")
        self.find(timeout=timeout).screenshot().save(file_path)

    def drag_to(self, timeout=5, *args, **kwargs):
        logger.info("拖动")
        self.find(timeout=timeout).drag_to(*args, **kwargs)


if __name__ == '__main__':
    pass







