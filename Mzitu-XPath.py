import os
import time
from random import random
import requests
import parsel
from tqdm import tqdm

ref_url = 'https://www.mzitu.com'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ',
    'referer': ref_url
}
path = './Spider/'
if os.path.exists(path):
    pass
else:
    os.mkdir(path)

def requests_url(url):
    try:
        r = requests.get(url, headers=header)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r
    except:
        print('链接请求失败！')

def get_info(url):
    global ref_url
    page = []
    main_urls = parsel.Selector(requests_url(url).text).xpath('//li/span/a/@href').extract()  # 获取套图链接
    for main_url in main_urls:
        ref_url = main_url
        file_name = parsel.Selector(requests_url(main_url).text).xpath('//h2/text()').extract()  # 套图名称
        page_num = parsel.Selector(requests_url(main_url).text).xpath('//a/span/text()')[-2].extract()  # 获取页码
        for i in range(1, int(page_num) + 1):
            page.append(i)
        for i in tqdm(page, desc='正在下载：{}'.format(file_name[0])):
            URL = main_url + '/' + str(i)
            image_url = parsel.Selector(requests_url(URL).text).xpath('//p/a/img/@src').extract()
            download(file_name,image_url)
            time.sleep(random())

def download(file_name, image_url):
    if os.path.exists(path + file_name[0]):
        pass
    else:
        os.mkdir(path + file_name[0])
    image = requests_url(image_url[0])
    with open(path + file_name[0] + '/' + image_url[0].split('/')[-1], 'wb') as f:
        f.write(image.content)

if __name__ == '__main__':
    url = 'https://www.mzitu.com/'
    get_info(url)
