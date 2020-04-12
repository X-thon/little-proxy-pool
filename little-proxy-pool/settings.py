from os.path import dirname, abspath, join
from environs import Env

# 读取环境配置文件
env = Env()
env.read_env()


# definition of environments
DEV_MODE, TEST_MODE, PROD_MODE = 'dev', 'test', 'prod'
APP_ENV = env.str('APP_ENV', DEV_MODE).lower()
APP_DEBUG = env.bool('APP_DEBUG', True if APP_ENV == DEV_MODE else False) # 开发模式下打开调试模式
APP_DEV = IS_DEV = APP_ENV == DEV_MODE
APP_PROD = IS_PROD = APP_ENV == PROD_MODE
APP_TEST = IS_TEST = APP_ENV == TEST_MODE

# set rating; detect success score+1, else score-1; 
# lower than the min score, the proxy will be remove
MAX_SCORE = env.int('MAX_SCORE', 50)
MIN_SCORE = env.int('MIN_SCORE', 0)
INITIAL_SCORE = env.int('INITIAL_SCORE', 10)

# redis host
REDIS_HOST = env.str('REDIS_HOST', '127.0.0.1')
# redis port
REDIS_PORT = env.int('REDIS_PORT', 6379)
# redis password, if no password, set it to None
REDIS_PASSWORD = env.str('REDIS_PASSWORD', None)
# redis connection string, like redis://[password]@host:port or rediss://[password]@host:port
REDIS_CONNECTION_STRING = env.str('REDIS_CONNECTION_STRING', None)
# redis connected db
REDIS_DB = env.int('REDIS_DB', 1)
# redis hash table key name
REDIS_KEY = env.str('REDIS_KEY', 'proxies')

# detector settings 
VALID_STATUS_CODES = env.list('VALID_STATUS_CODES', [200]) # 包含正常的状态码
TEST_URL = env.str('TEST_URL', "http://icanhazip.com") # 如果针对爬取时，可以将检测网站换为目标网站
BATCH_TEST_SIZE = env.int('BATCH_TEST_SIZE', 100) # Number of agents per test

# getter settings
POOL_UPPER_THRESHOLD = env.int('POOL_UPPER_THRESHOLD', 300)

# scheduler settings
TESTER_CYCLE_INDEX = env.int('TESTER_CYCLE_INDEX', 60)
GETTER_CYCLE_INDEX = env.int('GETTER_CYCLE_INDEX', 60)
TESTER_ENABLED = env.bool('TESTER_ENABLED', True)
GETTER_ENABLED = env.bool('GETTER_ENABLED', True)
API_ENABLED = env.bool('API_ENABLED', True)

# definition of api
API_HOST = env.str('API_HOST', '0.0.0.0')
API_PORT = env.int('API_PORT', 5555)
API_THREADED = env.bool('API_THREADED', True)