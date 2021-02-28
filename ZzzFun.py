import os
import re
import parsel
import requests
from tqdm import tqdm

path = './'

rep = requests.get('https://ip.jiangxianli.com/api/proxy_ip')
proxy = {'HTTP': 'http://' + rep.json()['data']['ip'] + ':' + rep.json()['data']['port']}
print(proxy)


class Download:
    urls = []
    m3u8_headers = {
        'Host': 'service-agbhuggw-1259251677.gz.apigw.tencentcs.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69',
        'Accept': '*/*',
        'Origin': 'null',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }

    def __init__(self, name, m3u8_url, download_path):
        """
        :param name: 视频名
        :param m3u8_url: 视频的 m3u8文件 地址
        :param path: 下载地址
        """
        self.video_name = name
        self.path = download_path
        self.f_url = m3u8_url
        with open(self.path + '/{}.m3u8'.format(self.video_name), 'wb')as f:
            f.write(requests.get(m3u8_url, proxies=proxy, headers=self.m3u8_headers).content)

    def get_ts_urls(self):
        with open(self.path + '/{}.m3u8'.format(self.video_name), "r") as file:
            lines = file.readlines()
            for line in lines:
                if 'pgc-image' in line:
                    self.urls.append(line.replace('\n', ''))

    def start_download(self):
        self.get_ts_urls()
        for url in tqdm(self.urls, desc="正在下载 {} ".format(self.video_name)):
            video_headers = {
                'Host': re.findall("https://(.*?)/obj/", str(url))[0],
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69',
                'Accept': '*/*',
                'Origin': 'http://www.zzzfun.com',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
            }
            response = requests.get('https://ip.jiangxianli.com/api/proxy_ip')
            proxy = {'HTTP': 'http://' + rep.json()['data']['ip'] + ':' + response.json()['data']['port']}
            movie = requests.get(url, proxies=proxy, headers=video_headers)
            with open(self.path + '/{}.flv'.format(self.video_name), 'ab')as f:
                f.write(movie.content)
        os.remove(self.path + '/{}.m3u8'.format(self.video_name))


def user_ui(videos_url):
    """
    :param videos_url: 视频的详情页链接
    :return:
    """
    main_headers = {
        'Host': 'www.zzzfun.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': videos_url,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }
    r = requests.get(videos_url, proxies=proxy, headers=main_headers)
    video_name = re.findall("<title>(.*?)详情介绍-.*?</title>", r.text)[0].replace(" ", '')
    video_nums = len(parsel.Selector(r.text).xpath('//div[@class="episode-wrap"]/ul[1]/li'))
    video_id = videos_url.split("-")[-1].split('.')[0]
    video_urls = ['http://www.zzzfun.com/static/danmu/bed-bofang.php?{}/{:0>2d}.m3u8'.format(video_id, num) for num in
                  range(1, video_nums + 1)]
    rel_path = path + video_name
    if os.path.exists(rel_path):
        pass
    else:
        os.makedirs(rel_path)
    for url in video_urls:
        r = requests.get(url, proxies=proxy, headers=main_headers)
        m3u8_url = re.findall("video.src = '(.*?)';", r.text)[0]
        name = "第" + url.split('/')[-1].split('.')[0] + "话"
        Download(name, m3u8_url, rel_path).start_download()


if __name__ == '__main__':
    print("""CSDN ：高智商白痴\nCSDN个人主页：https://blog.csdn.net/qq_44700693""")
    videos_url = input("请输入视频的详情页链接: ")
    user_ui(videos_url)

# http://www.zzzfun.com/vod-detail-id-1916.html
# http://www.zzzfun.com/vod-detail-id-1929.html
# http://www.zzzfun.com/vod-detail-id-1913.html
