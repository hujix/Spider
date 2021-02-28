import os
import random
import requests

proxies = ['HTTP://117.95.201.66:9999', 'HTTP://183.166.103.169:9999', 'HTTP://58.211.134.98:38480',
           'HTTP://171.35.162.210:9999', 'HTTP://110.243.5.139:9999', 'HTTP://122.4.49.163:9999',
           'HTTP://125.73.220.18:49128', 'HTTP://223.242.224.250:9999', 'HTTP://123.163.96.2:9999',
           'HTTP://183.166.70.82:9999', 'HTTP://49.85.211.213:8118', 'HTTP://117.69.150.141:9999']
proxy = {'HTTP': random.choice(proxies)}
headers = {

    'referer': 'https://haokan.baidu.com/tab/vlog',
    'cookie': '自行填写Cookies',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72'
}
params = {
    'tab': 'vlog',
    'act': 'pcFeed',
    'pd': 'pc',
    'num': '20',
    'shuaxin_id': '1589079762940'
}

path = './Spider/'
if os.path.exists(path):
    pass
else:
    os.mkdir(path)


def requests_url(url):
    try:
        r = requests.get(url, proxies=proxy, params=params, headers=headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r
    except:
        print('请求失败！')


def get_download():
    url = 'https://haokan.baidu.com/videoui/api/videorec?'
    Response = requests_url(url).json()
    videos = Response['data']['response']['videos']
    for video in videos:
        response = requests_url(video['play_url'])
        with open(path + video['title'] + '.mp4', 'wb') as f:
            f.write(response.content)
            print('正在下载 ' + video['title'])


get_download()
