import requests


def get_page(url):
    """访问url，返回html内容
    
    :param url: 目标网址
    :type url: str
    """    
    try:
        rep = requests.get(url)
    except Exception as e:
        raise e
    return rep.text