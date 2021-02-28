import random

import requests

path = "./Desktop/"


class PpxNew:
    api_url = 'https://i-lq.snssdk.com/bds/cell/cell_comment/'
    headers = {
        'Accept-Encoding': 'gzip',
        'passport-sdk-version': '30',
        'sdk-version': '2',
        'User-Agent': 'ttnet okhttp/3.10.0.2',
        'Host': 'i-lq.snssdk.com',
        'Connection': 'Keep-Alive'
    }

    def __init__(self, s_url):
        if '/item/' in s_url:
            self.cell_id = s_url.split('?')[0].split('/')[-1]
        elif '/s/' in s_url:
            self.rel_url = requests.get(s_url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}).url
            self.cell_id = self.rel_url.split('?')[0].split('/')[-1]
        self.param = {
            'cell_id': self.cell_id,
            'aid': '1319',
            'app_name': 'super',
        }

    def parse_url(self):
        response = requests.get(self.api_url, headers=self.headers, params=self.param)
        video = response.json()['data']['cell_comments'][0]['comment_info']['item']['video']
        video_name = video['text']
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video_url = video['video_high']['url_list'][0]['url']
        with open(path + str(video_name) + ".mp4", 'wb')as fp:
            fp.write(requests.get(video_url).content)
        print("【皮皮虾】: {}.mp4 无水印视频下载完成！".format(video_name))


if __name__ == '__main__':
    s_url = 'https://h5.pipix.com/s/eJXwbxC/'
    PpxNew(s_url).parse_url()
