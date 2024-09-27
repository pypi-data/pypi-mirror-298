from selenium.webdriver.remote.webdriver import WebDriver


class JavaScript:
    def __init__(self, driver: WebDriver = None):
        self._d = driver

    def __get__(self, instance, owner):
        if self._d is None:
            self._d = instance.web_driver
        return self

    def run_execute_script(self, script_code, *args):
        """
        运行JavaScript脚本
        :param script_code:
        :param args:
        :return:
        """
        return self._d.execute_script(script_code, *args)

    def open_new_tab(self, url=''):
        """
        打开一个新的tab页面
        :param url: 默认为空，如果url有值，则默认打开这个url
        :return:
        """
        _code = f'window.open({url})'
        self.run_execute_script(_code)

    def clear_input_control(self, ele):
        """
        js 清除输入框内容
        :return:
        """
        _code = "arguments[0].value = '';"
        self.run_execute_script(_code, ele)

    def goto_new_route(self, route):
        """
        切换到当前窗口到新路由上
        只针对同网站的不同路由进行切换
        :param route:
        :return:
        """
        _code = f"window.location.href='{route}'"
        self.run_execute_script(_code)

    @property
    def get_webdriver_arguments(self):
        """
        获取浏览器版本
        :return:
        """
        return self.run_execute_script("return window.navigator.webdriver")
