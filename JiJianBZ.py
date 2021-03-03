from hashlib import sha256

import requests
import time
from tqdm import tqdm

path = './spider/'


def get_access(timestamp) -> str:
    content_type = "application/json"
    location = "bz.zzzmh.cn"
    sign = "error"
    return sha256((content_type + location + sign + str(timestamp)).encode("utf-8")).hexdigest()


def download(images):
    for img in tqdm(images, desc="正在下载壁纸："):
        with open(path + str(img).split('/')[-1], 'wb')as fp:
            fp.write(requests.get(img, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}).content)


class JiJianBZ:
    api_url = 'https://api.zzzmh.cn/bz/getJson'

    def __init__(self):
        timestamp = int(time.time() * 1000)
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'access': get_access(timestamp),
            'content-length': '30',
            'content-type': 'application/json',
            'location': 'bz.zzzmh.cn',
            'origin': 'https://bz.zzzmh.cn',
            'referer': 'https://bz.zzzmh.cn/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sign': str(timestamp),
            'timestamp': "1614762200400",
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        self.data = {
            "target": "index",
            "pageNum": 1
        }

    def get_name(self):
        image_url = []  # 保存壁纸原图链接
        response = requests.post(self.api_url, headers=self.headers, json=self.data).json()
        pages = response['result']['pages']  # 总共页数：pageNum（待用）
        records = response['result']['records']
        for re in tqdm(iterable=records, desc="准备链接："):
            style = re['t']
            uri = re['i']
            if style == "j":
                url = 'https://w.wallhaven.cc/full/' + uri[:2] + '/wallhaven-' + uri + '.jpg'
                image_url.append(url)
            elif style == "p":
                url = 'https://w.wallhaven.cc/full/' + uri[:2] + '/wallhaven-' + uri + '.png'
                image_url.append(url)
        download(image_url)


JiJianBZ().get_name()
