import json
import os
import requests
from tqdm import tqdm

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.122 Safari/537.36 Edg/81.0.416.64 '
}

if os.path.exists('./spider'):
    pass
else:
    os.mkdir('./spider')

photo_lists = []


def get_info(url):  # 请求网页（包含判断是否请求成功）
    try:
        r = requests.get(url, headers=header)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r
    except:
        print('请求失败！')


def now_get():
    TYPE = input('请输入你准备在堆糖搜索并下载的关键字：')
    for page_num in range(0, 200, 24):
        URL = 'https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}'.format(TYPE, page_num)
        photo_info = json.loads(get_info(URL).text)
        for info in photo_info['data']['object_list']:
            photo_lists.append(info['photo']['path'])
    print('图片下载链接准备完成。')


def download():
    for num in tqdm(photo_lists, desc='正在下载：'):
        r = get_info(num)
        name = str(num).split('/')[-1]
        with open('./spider/' + name, 'wb') as f:
            f.write(r.content)


if __name__ == '__main__':
    now_get()
    download()
