## Little Proxy Pool 0.0.1

<p align="left">
	<img src='https://img.shields.io/badge/build-passing-brightgreen.svg' alt="Build Status"></a>
  <img src='https://img.shields.io/badge/python%20version-3.7.7-brightgreen.svg' alt="Build Status"></a>
  <img src='https://img.shields.io/badge/redis%20version-5.0.4-brightgreen.svg' alt="Build Status">
</p>

一个小型的IP代理池，提供简单的接口。

只是学习过程中的实践，参考崔庆才大大的项目实现的简单版本，会继续改进。



## Install

```
$ cd .../little-proxy-pool
$ pip install -r requirements.txt
```

还需要安装redis，如果是mac用户：

```
$ brew install redis
```



## Usage

> 默认配置项可以根据需要在`setting.py`文件中进行修改；


1. 打开redis服务：

```
$ redis-server
```

2. 运行代理服务：

```
$ python scheduler.py
```

3. 接口（默认监听地址：`0.0.0.0:5555`）：

```python
# 随机获取代理池中一个代理(返回数据是str类型)
response = requests.get(0.0.0.0:5555/random)
# 获取代理池总量
response = int(requests.get(0.0.0.0:5555/count))
```


