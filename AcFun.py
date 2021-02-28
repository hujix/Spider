import os
import re
import json
import requests
from tqdm import tqdm

path = 'C:/Users/Jackson-art/Desktop/'

rep = requests.get('https://ip.jiangxianli.com/api/proxy_ip', verify=False)
proxy = {'HTTP': 'http://' + rep.json()['data']['ip'] + ':' + rep.json()['data']['port']}
print(proxy)
headers = {
    'referer': 'https://www.acfun.cn/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83'
}

flag = True
qua = 0


class m3u8_url():
    def __init__(self, f_url, name=""):
        """
        :param f_url: 当前视频的链接
        :param name:  番剧名，默认为空
        """
        self.url = f_url
        self.name = name

    def get_m3u8(self):
        global flag, qua, rel_path
        html = requests.get(self.url, proxies=proxy, headers=headers).text
        first_json = json.loads(re.findall('window.pageInfo = window.*? = (.*?)};', html)[0] + '}', strict=False)
        if self.name == '':
            name = first_json['title'].strip().replace("|", '')
            rel_path = path
        else:
            name = self.name
            rel_path = path + first_json['bangumiTitle'].strip()
            if os.path.exists(rel_path):
                pass
            else:
                os.makedirs(rel_path)
        video_info = json.loads(first_json['currentVideoInfo']['ksPlayJson'], strict=False)['adaptationSet'][0][
            'representation']
        Label = {}
        num = 0
        for quality in video_info:  # 清晰度
            num += 1
            Label[num] = quality['qualityLabel']
        if flag:
            print(Label)
            choice = int(input("请选择清晰度: "))
            flag = False
            qua = choice
            Download(name + '[{}]'.format(Label[choice]), video_info[choice - 1]['url'], rel_path).start_download()
        else:
            Download(name + '[{}]'.format(Label[qua]), video_info[qua - 1]['url'], rel_path).start_download()


class Pan_drama():
    def __init__(self, f_url):
        """
        :param f_url: 视频主页的链接
        """
        self.aa = len(str(f_url).split('/')[-1])
        if self.aa == 7:
            self.url = f_url
        elif self.aa > 7:
            self.url = str(f_url).split('_')[0]

    def get_info(self):
        video_info = {}
        html = requests.get(self.url, proxies=proxy, headers=headers).text
        all_item = json.loads(re.findall('window.bangumiList = (.*?);', html)[0])['items']
        for item in tqdm(all_item, desc="正在准备番剧"):
            video_info[item['episodeName'] + '-' + item['title']] = self.url + '_36188_' + str(item['itemId'])
        for name in video_info.keys():
            m3u8_url(video_info[name], name).get_m3u8()


class Download():
    urls = []

    def __init__(self, name, m3u8_url, path):
        """
        :param name: 视频名
        :param m3u8_url: 视频的 m3u8文件 地址
        :param path: 下载地址
        """
        self.video_name = name
        self.path = path
        self.f_url = str(m3u8_url).split('hls/')[0] + 'hls/'
        with open(self.path + '/{}.m3u8'.format(self.video_name), 'wb')as f:
            f.write(requests.get(m3u8_url, proxies=proxy, headers={'user-agent': 'Chrome/84.0.4147.135'}).content)

    def get_ts_urls(self):
        with open(self.path + '/{}.m3u8'.format(self.video_name), "r") as file:
            lines = file.readlines()
            for line in lines:
                if '.ts' in line:
                    self.urls.append(self.f_url + line.replace('\n', ''))

    def start_download(self):
        self.get_ts_urls()
        for url in tqdm(self.urls, desc="正在下载 {} ".format(self.video_name)):
            rep = requests.get('https://ip.jiangxianli.com/api/proxy_ip')
            proxy = {'HTTP': 'http://' + rep.json()['data']['ip'] + ':' + rep.json()['data']['port']}
            movie = requests.get(url, proxies=proxy, headers={'user-agent': 'Chrome/84.0.4147.135'})
            with open(self.path + '/{}.flv'.format(self.video_name), 'ab')as f:
                f.write(movie.content)
        os.remove(self.path + '/{}.m3u8'.format(self.video_name))


url1 = input("输入地址: ")
if url1.split('/')[3] == 'v':
    m3u8_url(url1).get_m3u8()
elif url1.split('/')[3] == 'bangumi':
    Pan_drama(url1).get_info()
