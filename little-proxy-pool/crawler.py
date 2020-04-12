# 代理获取模块

from utils import get_page
from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        """实现一个元类，将所有以 crawl 开头的方法定义成了一个属性，
        动态地获取到所有以 crawl 开头的方法列表。

        :param type: type类，为了调用type.__new__方法创建并返回类对象
        :type type: type
        :param name: 要创建的类名
        :type name: str
        :param bases: 继承的父类名
        :type bases: tuple
        :param attrs: 包含属性的字典（名称和值）
        :type attrs: dict
        """
        count = 0
        attrs['__CrawlFunc__'] = []
        for key, _ in attrs.items():
            if 'crawl_' in key:  # 将名称中含有 crawl_ 的方法添加到字典中
                attrs['__CrawlFunc__'].append(key)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    """爬虫类，用以获取代理

    :param object: 继承object类
    :type object: 
    :param metaclass: 定义元类，动态地为此类添加了一个'__CrawlFunc__'属性, defaults to ProxyMetaclass
    :type metaclass: type, optional
    """

    def get_proxies(self, callback):
        """调用爬虫类中所有的爬虫方法(对应爬取不同代理网站), 获取代理

        :param callback: 爬虫函数名
        :type callback: function
        :return: 代理列表
        :rtype: list
        """
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        """抓取代理66网站的代理

        :param page_count: 要抓取的页码, defaults to 4
        :type page_count: int
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count+1)]
        for url in urls:
            print('Crawling', url)
            # 考虑到有请求失败的原因，所以没有直接用 doc = pq(url=url) 的方式获取、构造html
            html = get_page(url)
            if html:
                doc = pq(html)
                # gt(0) 表示选择序号在0之后的符合的tr标签; 与jQuery的一个接口同名
                trs = doc('.containerbox table tr:gt(0)').items()  # CSS选择器的语法
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    # 如果需要获取地区、代理类型等数据后续可以自行添加
                    yield ":".join([ip, port])

    def crawl_7yip(self, page_count=4):
        """抓取齐云代理的免费代理

        :param page_count: 页码, defaults to 4
        :type page_count: int
        """
        start_url = 'https://www.7yip.cn/free/?action=china&page={}'
        urls = [start_url.format(page) for page in range(1, page_count+1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    respond_speed = float(
                        tr.find('td:nth-child(6)').text().replace('秒', ""))
                    if respond_speed >= 10:  # 去除响应速度太慢的链接
                        continue
                    yield ":".join([ip, port])

    def crawl_ihuan(self):
        """
        获取小幻代理，由于小幻代理的页码采用了(我不知道的)编码，
        此处使用硬编码，不支持修改抓取页数
        """
        start_url = 'https://ip.ihuan.me/address/5Lit5Zu9.html?page={}'
        page_code = ['b97827cc', '4ce63706', '5crfe930', 'f3k1d581']
        urls = [start_url.format(page) for page in page_code]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    respond_speed = float(
                        tr.find('td:nth-child(8)').text().replace('秒', ""))
                    if respond_speed >= 10 or ip == "" or port == "":
                        continue
                    yield ":".join([ip, port])

    def crawl_ihuan_api(self, count=100):
        """通过小幻代理的api，批量提取代理

        :param count: 提取的数量, defaults to 100
        :type count: int
        """
        from selenium import webdriver
        from selenium.webdriver.support.ui import Select  # 用于下拉框
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        prefs = {
            'profile.default_content_settings': {
                'profile.default_content_setting_values': {
                    'images': 2,  # 不加载图片
                    # 'javascript': 2,  # 不加载JS
                    # "User-Agent": ua,  # 更换UA
                }}}
        chrome_options.add_experimental_option("prefs",prefs)
        
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get("https://ip.ihuan.me/ti.html")
        # 以下是表单项
        num = driver.find_element_by_name("num")  # 通过xpath定位居然出错了...
        # port = driver.find_element_by_name("port")  # 端口
        # kill_port = driver.find_element_by_name("kill_port")  # 排除端口
        # address = driver.find_element_by_name("address")
        # anonymity = driver.find_element_by_name("anonymity")  # 指定匿名程度
        proxy_type = Select(driver.find_element_by_name("type"))  # 指定代理类型
        # post = Select(driver.find_element_by_name("post"))  # 指定代理模式
        sort_type = Select(driver.find_element_by_name("sort"))  # 指定排序方式
        submit = driver.find_element_by_id("sub")

        # 对表单进行操作
        num.clear()
        num.send_keys(str(count))
        proxy_type.select_by_index(1)
        sort_type.select_by_index(1)
        submit.click()  # 点击后打开新窗口

        windows = driver.window_handles
        driver.switch_to_window(windows[-1])  # 切换至新窗口
        content = driver.find_elements_by_class_name("panel-body")[0].text
        content = content.split("\n")
        driver.quit() # 关闭驱动
        for proxy in content:
            yield proxy


# if __name__ == "__main__":
#     clawer = Crawler()
#     clawer.crawl_ihuan()
