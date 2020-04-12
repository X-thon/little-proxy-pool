from db import RedisClient
from crawler import Crawler

POOL_UPPER_THRESHOLD = 300

class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD: 
            print("代理池已满，获取器暂停获取代理")
            return True
        else:
            print("代理池未满，获取器继续获取代理")
            return False
    
    def run(self):
        """
        获取器主函数
        """
        print('获取器开始执行')
        if not self.is_over_threshold():
            # __CrawlFunc__ 是通过元类添加的属性，包含所有爬虫函数的函数名
            # __CrawlFuncCount__ 记录爬虫函数个数
            for callback_label in range(self.crawler.__CrawlFuncCount__): 
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)

