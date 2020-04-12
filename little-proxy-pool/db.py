import redis
from random import choice
from settings import MAX_SCORE, MIN_SCORE, INITIAL_SCORE, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB, REDIS_KEY



# 配置redis客户端操作类
class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        :param db: Redis数据库
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=db)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy: score}) # 随redis版本变化，zadd接口也变化，如果要向下兼容需要增加版本判断字段

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE) # 将min, max参数都传入MAX_SOCRE取最高分数代理
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE) # 按照分值从小到大的顺序获取，参数2，3指定了一个范围
            if len(result):
                return choice(result)
            else:
                pass
                #raise PoolEmptyError # 代理池为空，抛出错误

    def decrease(self, proxy):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy) # 返回proxy对应的分数
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, -1, proxy) # 接口改变，为 proxy 加上 -1
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy) # 从有序集合里移除一个或者多个成员

    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):
        """
        获取池中代理数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY) # 返回有序集合包含的成员数量

    def all(self):
        """
        获取全部代理，从小到大排列
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
