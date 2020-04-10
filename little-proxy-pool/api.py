from db import RedisClient
from flask import Flask, g
from settings import API_HOST, API_PORT, API_THREADED

__all__ = ['app']
app = Flask(__name__)

def get_conn():
    """将应用连接到数据库
    
    :return: 返回redis连接
    :rtype: RedisClient
    """    
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():
    return "<h1>This is a little Proxy Pool System</h1>"

@app.route('/random')
def get_a_random_proxy():
    """
    获取随机可用代理
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random()

@app.route('/count')
def get_count():
    """
    获取代理池总量
    :return: 代理池总量
    """
    conn = get_conn()
    return str(conn.count())

if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)