import re
import os
import time
import ffmpy3
import random
import parsel
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from multiprocessing.pool import ThreadPool

referer = 'https://www.pianku.tv'
header = {
    'referer': referer,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37'
}
proxies = ['HTTP://60.13.42.120:9999', 'HTTP://163.204.244.207:9999', 'HTTP://113.121.39.121:9999',
           'HTTP://125.117.134.99:9000', 'HTTP://123.169.114.81:9999', 'HTTP://58.253.159.230:9999',
           'HTTP://125.108.97.209:9000', 'HTTP://113.124.85.24:9999', 'HTTP://27.220.51.228:9000',
           'HTTP://113.124.84.205:9999', 'HTTP://110.243.31.147:9999']

path = './Spider/'
video = {}  # 保存搜索记录
download = {}  # 保存下载链接


def requests_url(url):  # 请求网址
    try:
        proxy = {'http': random.choice(proxies)}
        print(proxy)
        r = requests.get(url, proxies=proxy, headers=header)
        r.raise_for_status()
        r.encoding = 'UTF-8'
        return r
    except:
        print("*********请求失败！***********")


def split_info(videos_info):
    num = 1
    for video_info in videos_info:
        info = str(video_info).replace('<em>', '').replace('</em>', '')  # 去掉源码中红色字体的标注
        soup = BeautifulSoup(info, 'html.parser')
        info = soup.find_all('p')
        # 将通过关键字搜索到的视频名与对应链接保存下来 （对应链接为拼接后的完整链接，如：https://www.pianku.tv/tv/wNiNmMnRjZ.html）
        video[info[0].strong.a.string + info[0].span.string] = 'https://www.pianku.tv' + info[0].strong.a.attrs['href']
        name2_info = info[1].string  # 又名
        area_info = info[2].string  # 地区与类型
        actor_info = info[3].string  # 演员
        introduction = info[4].string  # 简介
        print('***********************************************************')
        print('{:0>2d}: '.format(num), end='')
        num += 1
        print('\t' + info[0].strong.a.string + info[0].span.string)  # 名称
        print('\t' + name2_info)
        print('\t' + area_info)
        print('\t' + actor_info)
        print('\t' + introduction)


def get_video(url):
    global referer
    referer = url
    # 根据重定向拼接真实的链接
    URL = 'https://www.pianku.tv/ajax/downurl/' + url.split('/')[-1].split('.')[0] + '_' + url.split('/')[3] + '/'
    # 请求视频链接
    response = requests_url(URL)
    soup = \
        BeautifulSoup(response.text, 'html.parser').find('ul', attrs={'class': "player ckp"}).find('li').a.attrs[
            'href']  # 找到每一集的链接
    URL1 = 'https://www.pianku.tv' + soup  # 重新拼接每一集主页链接
    response1 = requests_url(URL1).text
    soup1 = BeautifulSoup(response1, 'html.parser').find_all('script')[12]  # 获取script标签
    # 通过正则表达式找出所有下载链接
    p = re.compile(r"https://.*?/index.m3u8")
    information = p.findall(str(soup1))
    num = 1
    for info in information:
        download['第{}集'.format(num)] = str(info).replace('index.m3u8', '1000k/hls/index.m3u8')
        num += 1
    print('*********  已获取最新全部下载链接，共 {} 集。  *********'.format(len(download)))


def video_download(name):  # 通过ffmpy3下载
    try:
        if os.path.exists(path + NAME + '/'):
            pass
        else:
            os.makedirs(path + NAME + '/')
        ffmpy3.FFmpeg(inputs={download[name]: None}, outputs={path + NAME + '/' + name + '.mp4': None}).run()
        print('************' + name + '下载成功！' + '************')
    except:
        print('============' + name + '下载失败！' + '============')


def user_ui():
    global NAME, page_num
    print('***********************************************************')
    keyword = '传闻中'  # input('请输入搜索的视频关键字：')
    url = 'https://www.pianku.tv/s/go.php?q=' + quote(keyword, 'utf-8')  # 进行url加密
    URL = (url.split('go.php?q=')[0] + url.split('go.php?q=')[1]).replace('%', '_') + '.html'  # 根据网页，更改加密后的url
    html = requests_url(URL).text
    search_time = parsel.Selector(html).xpath('//div[@class="breadcrumbs"]/text()').extract()[0]  # 搜索时间以及数量
    videos_info = parsel.Selector(html).xpath('//dd').extract()  # 视频信息标签
    try:  # 若搜索结果小于10项，则无页码信息
        print(search_time, end='')
        page_num = parsel.Selector(html).xpath('//div[@class="pages"]/a/text()').extract()[-2]
        print('，共{}页。每页10项。'.format(page_num))
    except:
        print(end='\n')
    split_info(videos_info)  # 拆分显示视频信息
    choice = input('\n请输入序号选择：')
    NAME = list(video.keys())[int(choice) - 1]  # 通过下标确定进一步搜索的类容
    URL = video[NAME]
    get_video(URL)  # 获取下载链接
    # 选择从多少集开始下载
    download_num = int(input('请输入本次需要从第几集开始下载：'))
    for num in range(1, download_num):
        del download['第{}集'.format(num)]


user_ui()

time1 = time.time()
pool = ThreadPool(10)  # 开启线程池
results = pool.map(video_download, download.keys())
pool.close()
pool.join()
time2 = time.time()
print('*********耗时：{}*********'.format(time2 - time1))
