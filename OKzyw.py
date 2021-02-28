import re
import random
import ffmpy3
from multiprocessing.pool import ThreadPool

import parsel
import requests

proxies = [
    'HTTP://113.194.28.41:9999',
    'HTTP://171.15.51.224:9999',
    'HTTP://125.73.220.18:49128',
    'HTTP://223.242.224.250:9999',
    'HTTP://118.113.247.155:9999',
    'HTTP://115.218.211.25:9000',
    'HTTP://125.108.121.29:9000'
]
proxy = {'HTTP': random.choice(proxies)}
headers = {
    'Host': 'www.jisudhw.com',
    'Origin': 'http://www.jisudhw.com',
    'Referer': 'http://www.jisudhw.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72'
}

path = 'C:/Users/FullMoon/Desktop/Spider/'

info_dict = {}
video = {}


def get_main(url, keyword):
    try:
        r = requests.post(url, proxies=proxy, params={'m': 'vod-search'}, headers=headers,
                          data={'wd': keyword, 'submit': 'search'})
        r.raise_for_status()
        r.encoding = 'utf-8'
        info_list = parsel.Selector(r.text).xpath('//li/span[@class="xing_vb4"]/a').extract()  # 搜索得到的信息
        for info in info_list:
            name = re.findall('<a href=".*?" target="_blank">(.*?)</a>', info)[0]  # 返回list
            url1 = re.findall('<a href="(.*?)" target="_blank">.*?</a>', info)[0]
            # http://www.jisudhw.com/?m=vod-detail-id-45104.html
            info_dict[name] = 'http://www.jisudhw.com' + url1
        if info_dict:  # 默认 () {} [] 相当于 False
            print(keyword + ' 的相关视频搜索成功！共 {} 条记录。'.format(len(info_dict)))
            print('\n++++++++++++++++++++++++++ 目录 ++++++++++++++++++++++++++')
            num = 1
            for info in info_dict.keys():
                if num % 2 == 0:
                    print('{}: '.format(num) + info + '\n', end='')
                else:
                    print('{}: '.format(num) + info + '  \t', end='')
                num += 1
        else:
            print('搜索记录为空，请检查搜索的关键字：' + keyword)
    except:
        print('POST 请求失败！')


def get_urls(url):
    try:
        r = requests.get(url, proxies=proxy, headers=headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        video_info = parsel.Selector(r.text).xpath('//div[@id="2"]/ul/li/text()').extract()
        # 第01集$http://youku.com-youku.com/20180122/OgFJZjkT/index.m3u8
        num=1
        for info in video_info:
            video[str(info).split('$')[0]] = str(info).split('$')[-1]
            num+=1
        print('{} 集的视频链接已准备完成！'.format(len(video)))
    except:
        print('GET 请求失败！')


def download(name):
    try:
        print(name)
        print(video[name])
        ffmpy3.FFmpeg(inputs={video[name]: None}, outputs={path+name+'.mp4':None}).run()
    except:
        print('视频下载失败！')


def user_ui(url):
    global keyword
    print('*******************************************************')
    print('<<<<<<<<<<<<<<<<<  欢迎使用***视频下载器  >>>>>>>>>>>>>>>>')
    # keyword = input('请输入视频名称：')
    keyword = '斗罗大陆'
    get_main(url, keyword)
    num = input('请输入记录前的序号进行选择：')
    # print(list(info_dict.keys())[int(num)-1])
    # 通过序号获取对应 key值：强转为list-->使用序号作下标， 强转为int-->input获取为String类型
    URL = info_dict[list(info_dict.keys())[int(num) - 1]]
    get_urls(URL)


if __name__ == '__main__':
    url = 'http://www.jisudhw.com/index.php?m=vod-search'
    user_ui(url)

# 开10个线程池
pool = ThreadPool(10)
results = pool.map(download, video.keys())
pool.close()
pool.join()
