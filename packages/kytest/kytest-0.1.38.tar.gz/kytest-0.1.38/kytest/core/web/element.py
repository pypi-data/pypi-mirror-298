"""
@Author: kang.yang
@Date: 2023/5/13 10:16
"""
from playwright.sync_api import expect

from .driver import Driver

from kytest.utils.log import logger


class RoleLocator:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.type = 'role'


class TextLocator:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.type = 'text'


class LabelLocator:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.type = 'label'


class PlaceholderLocator:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.type = 'placeholder'


class AltTextLocator:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.type = 'alt_text'


class TitleLocator:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.type = 'title'


class TestIdLocator:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.type = 'test_id'


class FrameLocator:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.type = 'frame'


class LocatorLocator:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.type = 'locator'


class FilterLocator:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.type = 'filter'


class NthLocator:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.type = 'nth'


class FirstLocator:

    def __init__(self):
        self.type = 'first'


class LastLocator:

    def __init__(self):
        self.type = 'last'


class Elem:
    """
    通过selenium定位的web元素
    """

    def __init__(self,
                 driver: Driver = None,
                 role=None,
                 name=None,
                 text=None,
                 label=None,
                 placeholder=None,
                 alt_text=None,
                 title=None,
                 test_id=None,
                 frame_loc=None,
                 locator=None,
                 exact=False
                 ):
        self._driver = driver
        self._kwargs = {}
        self.role = role
        if self.role:
            self._kwargs['role'] = role
        self.name = name
        if self.name:
            self._kwargs['name'] = name
        self.text = text
        if self.text:
            self._kwargs['text'] = text
        self.label = label
        if self.label:
            self._kwargs['label'] = label
        self.placeholder = placeholder
        if self.placeholder:
            self._kwargs['placeholder'] = placeholder
        self.alt_text = alt_text
        if self.alt_text:
            self._kwargs['alt_text'] = alt_text
        self.title = title
        if self.title:
            self._kwargs['title'] = title
        self.test_id = test_id
        if self.test_id:
            self._kwargs['test_id'] = test_id
        self.frame_loc = frame_loc
        if self.frame_loc:
            self._kwargs['frame_loc'] = frame_loc
        self.loc = locator
        if self.loc:
            self._kwargs['locator'] = locator
        self.exact = exact
        if self.exact:
            self._kwargs['exact'] = exact
        self.locators = []

        # self.get_first_locator()

    def __call__(self, *args, **kwargs):
        return self

    def __get__(self, instance, owner):
        """pm模式的关键"""
        if instance is None:
            return None
        self._driver = instance.driver
        return self

    def get_by_role(self, *args, **kwargs):
        self.locators.append(RoleLocator(*args, **kwargs))
        return self

    def get_by_text(self, *args, **kwargs):
        self.locators.append(TextLocator(*args, **kwargs))
        return self

    def get_by_label(self, *args, **kwargs):
        self.locators.append(LabelLocator(*args, **kwargs))
        return self

    def get_by_placeholder(self, *args, **kwargs):
        self.locators.append(PlaceholderLocator(*args, **kwargs))
        return self

    def get_by_alt_text(self, *args, **kwargs):
        self.locators.append(AltTextLocator(*args, **kwargs))
        return self

    def get_by_title(self, *args, **kwargs):
        self.locators.append(TitleLocator(*args, **kwargs))
        return self

    def get_by_test_id(self, *args, **kwargs):
        self.locators.append(TestIdLocator(*args, **kwargs))
        return self

    def frame_locator(self, *args, **kwargs):
        self.locators.append(FrameLocator(*args, **kwargs))
        return self

    def locator(self, *args, **kwargs):
        self.locators.append(LocatorLocator(*args, **kwargs))
        return self

    def filter(self, *args, **kwargs):
        self.locators.append(FilterLocator(*args, **kwargs))
        return self

    def nth(self, *args, **kwargs):
        self.locators.append(NthLocator(*args, **kwargs))
        return self

    @property
    def first(self):
        self.locators.append(FirstLocator())
        return self

    def last(self):
        self.locators.append(LastLocator())
        return self

    # 公共方法
    def get_first_locator(self):
        logger.info(f"查找第一个元素: {self._kwargs}")
        if self.role is not None:
            if self.name is not None:
                return self._driver.page.get_by_role(self.role, name=self.name)
            else:
                return self._driver.page.get_by_role(self.role)
        elif self.text is not None:
            if self.exact is True:
                return self._driver.page.get_by_text(self.text, exact=True)
            else:
                return self._driver.page.get_by_text(self.text)
        elif self.label is not None:
            return self._driver.page.get_by_label(self.label)
        elif self.placeholder is not None:
            return self._driver.page.get_by_placeholder(self.placeholder)
        elif self.alt_text is not None:
            return self._driver.page.get_by_alt_text(self.alt_text)
        elif self.title is not None:
            return self._driver.page.get_by_title(self.title)
        elif self.test_id is not None:
            return self._driver.page.get_by_test_id(self.test_id)
        elif self.frame_loc is not None:
            return self._driver.page.frame_locator(self.frame_loc)
        elif self.loc is not None:
            return self._driver.page.locator(self.loc)
        else:
            logger.info("第一个元素为空")
            return self._driver.page

    def find(self, timeout=10):
        """查找指定的一个元素"""
        logger.info(f"查找元素")
        element = self.get_first_locator()
        # 链式调用方法叠加
        logger.info(f"查找链式调用元素列表: {self.locators}")
        if self.locators:
            for loc_obj in self.locators:
                if loc_obj.type == "role":
                    element = element.get_by_role(*loc_obj.args, **loc_obj.kwargs)
                elif loc_obj.type == 'text':
                    element = element.get_by_text(*loc_obj.args, **loc_obj.kwargs)
                elif loc_obj.type == 'label':
                    element = element.get_by_label(*loc_obj.args, **loc_obj.kwargs)
                elif loc_obj.type == 'placeholder':
                    element = element.get_by_placeholder(*loc_obj.args, **loc_obj.kwargs)
                elif loc_obj.type == 'alt_text':
                    element = element.get_by_alt_text(*loc_obj.args, **loc_obj.kwargs)
                elif loc_obj.type == 'title':
                    element = element.get_by_title(*loc_obj.args, **loc_obj.kwargs)
                elif loc_obj.type == 'test_id':
                    element = element.get_by_test_id(*loc_obj.args, **loc_obj.kwargs)
                elif loc_obj.type == 'frame':
                    element = element.frame_locator(*loc_obj.args, **loc_obj.kwargs)
                elif loc_obj.type == 'locator':
                    element = element.locator(*loc_obj.args, **loc_obj.kwargs)
                elif loc_obj.type == 'filter':
                    element = element.filter(*loc_obj.args, **loc_obj.kwargs)
                elif loc_obj.type == 'nth':
                    element = element.nth(*loc_obj.args, **loc_obj.kwargs)
                elif loc_obj.type == 'first':
                    element = element.first
                elif loc_obj.type == 'last':
                    element = element.last

        try:
            element.wait_for(timeout=timeout * 1000)
            logger.info("查找成功")
            return element
        except:
            retry_count = 3
            for count in range(1, retry_count + 1):
                logger.info(f"第{count}次重试...")
                try:
                    element.wait_for(timeout=timeout * 1000)
                    logger.info("查找成功")
                    # if self._debug is True:
                    #     element.evaluate('(element) => element.style.border = "2px solid red"')
                    #     time.sleep(1)
                    #     self._driver.shot("查找成功")
                    return element
                except:
                    continue

            logger.info("查找失败")
            self._driver.shot("查找失败")
            raise Exception("查找失败")

    def exists(self, timeout=5):
        logger.info(f'判断元素是否存在')
        result = False
        try:
            self.find(timeout=timeout)
            result = True
        except:
            result = False
        finally:
            logger.info(result)
            return result

    def get_text(self):
        logger.info(f"获取文本属性")
        elem = self.find()
        text = elem.text_content()
        logger.info(text)
        return text

    def get_texts(self):
        logger.info(f"获取文本属性")
        elems = self.find().all()
        text_list = [elem.text_content() for elem in elems]
        logger.info(text_list)
        return text_list

    # 其他方法
    def scroll_into_view_if_needed(self, timeout=5):
        logger.info(f"滑动到可视区域")
        self.find(timeout=timeout).scroll_into_view_if_needed(timeout=timeout * 1000)
        logger.info("滑动完成")

    def click(self, timeout=5, position=None):
        logger.info(f"点击")
        self.find(timeout=timeout).click(timeout=timeout * 1000, position=position)
        logger.info("点击完成")

    def fill(self, text, timeout=5):
        logger.info(f"输入文本: {text}")
        self.find(timeout=timeout).fill(text, timeout=timeout * 1000)
        logger.info("输入完成")

    # def enter(self, timeout=5):
    #     logger.info("点击回车")
    #     self.find(timeout=timeout).press("Enter")
    #     logger.info("回车")

    def press(self, key, timeout=5):
        logger.info(f"点击按键: {key}")
        self.find(timeout=timeout).press(key)
        logger.info("点击完成")

    def check(self, timeout=5):
        logger.info("选择选项")
        self.find(timeout=timeout).check(timeout=timeout * 1000)
        logger.info("选择完成")

    def select_option(self, value: str, timeout=5):
        logger.info("下拉选择")
        self.find(timeout=timeout).select_option(value, timeout=timeout * 1000)
        logger.info("选择完成")

    def assert_visible(self, timeout=5):
        logger.info(f"断言可见")
        expect(self.find(timeout=timeout)).to_be_visible(timeout=timeout * 1000)

    def assert_hidden(self, timeout=5):
        logger.info(f"断言被隐藏")
        expect(self.find(timeout=timeout)).to_be_hidden(timeout=timeout * 1000)

    def assert_text_cont(self, text: str, timeout=5):
        logger.info(f"断言包含文本: {text}")
        expect(self.find(timeout=timeout)).to_contain_text(text, timeout=timeout * 1000)

    def assert_text_eq(self, text: str, timeout=5):
        logger.info(f"断言文本等于: {text}")
        expect(self.find(timeout=timeout)).to_have_text(text, timeout=timeout * 1000)


if __name__ == '__main__':
    pass
