import os

import requests
from tqdm import tqdm


class Download:
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
        with open(self.path + '/{}.m3u8'.format(self.video_name), 'wb') as f:
            f.write(requests.get(m3u8_url, headers={'user-agent': 'Chrome/84.0.4147.135'}).content)

    def get_ts_urls(self):
        with open(self.path + '/{}.m3u8'.format(self.video_name), "r") as file:
            lines = file.readlines()
            for line in lines:
                if '.ts' in line:
                    self.urls.append(self.f_url + line.replace('\n', ''))

    def start_download(self):
        self.get_ts_urls()
        for url in tqdm(self.urls, desc="正在下载 {} ".format(self.video_name)):
            movie = requests.get(url, headers={'user-agent': 'Chrome/84.0.4147.135'})
            with open(self.path + '/{}.flv'.format(self.video_name), 'ab') as f:
                f.write(movie.content)
        os.remove(self.path + '/{}.m3u8'.format(self.video_name))
