import json
import os
import random
import re
from urllib.parse import quote

import parsel
import requests

ip_url = 'https://ip.jiangxianli.com/api/proxy_ip'
r = requests.get(ip_url)
proxy = {'HTTP': 'http://' + r.json()['data']['ip'] + ':' + r.json()['data']['port']}
print(proxy)
path = './Java/'


class BiLiBiLi_phone():
    def __init__(self, s_url):
        self.url = s_url
        self.headers = {
            'origin': 'https://m.bilibili.com',
            'referer': self.url,
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)'
        }

    def bili_Download(self):
        r = requests.get(self.url, proxies=proxy, headers=self.headers)
        video_name = re.findall(',"title":"(.*?)","pubdate":', r.text)[0]
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video_url = re.findall(',"url":"(.*?)","backup_url"', r.text)[0].encode('utf-8').decode('unicode_escape')
        r = requests.get(video_url, proxies=proxy, headers=self.headers)
        with open(path + video_name + '.mp4', 'wb')as f:
            f.write(r.content)
        print("【BiLiBiLi】: {} 下载完成！".format(video_name))


class BiLiBiLi_api():
    def __init__(self, s_url):
        self.url = s_url.split('?')[0]
        self.header1 = {
            'Host': 'www.shipinyu.com',
            'Origin': 'http://www.shipinyu.com',
            'Referer': quote('http://www.shipinyu.com/video?url={}&page=video&submit=视频下载'.format(self.url)),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63'
        }
        self.data = {
            'url': self.url,
            'format': 'flv',
            'from': 'parse',
            'retry': '1'
        }
        self.header2 = {
            'origin': 'https://www.bilibili.com/',
            'referer': self.url,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63'
        }

    def BL_api_Download(self):
        r = requests.post('http://www.shipinyu.com/parse', proxies=proxy, data=self.data, headers=self.header1)
        video_name = re.findall('data-clipboard-text="(.*?)"', r.json()['msg'])[0]
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video_url = re.findall('href="(.*?)"', r.json()['msg'])[0].replace('amp;', '')
        r1 = requests.get(video_url, proxies=proxy, headers=self.header2)
        with open(path + video_name + '.flv', 'wb')as f:
            f.write(r1.content)
        print("【BiLiBiLi】: {} 下载完成！".format(video_name))


class BiLiBiLi():
    def __init__(self, s_url, name_num=0, flag=False):
        self.url = s_url
        self.name_num = name_num
        self.flag = flag
        self.header = {
            'Range': 'bytes=0-',
            'referer': self.url,
            'origin': 'https://www.bilibili.com/',
            # 'cookie':'填写自己的B站大会员cookie',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63'
        }

    def BL_download(self):
        global v_name, rel_path, video_name
        html = requests.get(self.url, proxies=proxy, headers=self.header).text
        json_data = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
        video_name = re.findall(',"title":"(.*?)","', html)[0].replace('（', '(').replace('）', ')').replace(' ', '_')
        if self.flag:
            video_temp_name = re.findall('","part":"(.*?)","', html)[int(self.name_num) - 1].replace(' ', '_')
            rel_path = path + video_name + '/'
            v_name = video_temp_name
            if os.path.exists(rel_path):
                pass
            else:
                os.mkdir(rel_path)
        else:
            rel_path = path
            v_name = video_name
        video = json.loads(json_data)['data']['dash']['video'][0]['baseUrl']
        self.download(video, rel_path + v_name + '.m4s')
        print("【BiLiBiLi】: {} 视频下载完成！".format(v_name))
        audio = json.loads(json_data)['data']['dash']['audio'][0]['baseUrl']
        self.download(audio, rel_path + v_name + '-1.m4s')
        print("【BiLiBiLi】: {} 音频下载完成！".format(v_name))

    def download(self, url, rel_path):
        r = requests.get(url, headers=self.header)
        with open(rel_path, 'wb')as f:
            f.write(r.content)


def user_ui():
    print('*' * 10 + '\t BiLiBiLi视频下载\t' + '*' * 10)
    print('*' * 5 + "\t\tAuthor:  高智商白痴\t\t" + '*' * 5)
    choice1 = int(input("1、单个视频下载  2、多个视频下载  \n选择下载类型："))
    share_url = input('请输入链接: ')
    choice2 = int(input("1、模拟手机端下载  2、调用接口下载  3、直接下载\n选择下载方式："))
    if choice1 == 1:
        if choice2 == 1:
            BiLiBiLi_phone(share_url).bili_Download()
        if choice2 == 2:
            BiLiBiLi_api(share_url).BL_api_Download()
        if choice2 == 3:
            BiLiBiLi(share_url).BL_download()
    if choice1 == 2:
        v_url = share_url.split('?')[0]
        v_num = parsel.Selector(
            requests.get(share_url, proxies=proxy,
                         headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}).text).xpath(
            '//span[@class="cur-page"]/text()').extract()[0].split('/')[-1]
        video_list = ['{}?p={}'.format(v_url, i) for i in range(1, int(v_num) + 1)]
        if choice2 == 1:
            for url in video_list:
                BiLiBiLi_phone(url).bili_Download()
        if choice2 == 2:
            for url in video_list:
                BiLiBiLi_api(url).BL_api_Download()
        if choice2 == 3:
            for url in video_list:
                num = int(url.split('=')[-1])
                BiLiBiLi(url, num, True).BL_download()


if __name__ == '__main__':
    user_ui()

# https://api.vc.bilibili.com/link_draw/v1/doc/doc_list?uid=6823116&page_num=0&page_size=500&biz=all
# https://space.bilibili.com/6823116/album
