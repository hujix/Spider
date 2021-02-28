import os
import time
from random import random
import requests
from bs4 import BeautifulSoup

path = './spider'
if os.path.exists(path):
    pass
else:
    os.mkdir(path)
url = 'https://www.mzitu.com'
main_url = []
name_dict = {}
main_num = 0

ref_url='https://www.mzitu.com'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.53',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'Referer': ref_url
    }


def get_main_url(url):  # 获取每个主页的24个图片链接
    res = requests.get(url,headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')
    Temp_list = soup.find_all('li')[8:]
    for lab_list in Temp_list:
        div = BeautifulSoup(str(lab_list), 'html.parser')
        main_url.append(div.a.attrs['href'])  # 每个主页中图片详情列表链接
        name_dict[div.a.attrs['href']] = div.img.attrs['alt']
    print("获取当前页面所有链接成功！")


# <div class="main-image">  图片标签
# <div class="pagenavi">    页码标签
def get_image():
    global main_num,ref_url
    for now_url in main_url:
        main_num+=1
        ref_url=now_url
        if os.path.exists(path + '/' + name_dict[now_url]):
            pass
        else:
            os.mkdir(path + '/' + name_dict[now_url])
        response = requests.get(now_url, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_nums = soup.find('div', attrs={'class': "pagenavi"})
        page_num = BeautifulSoup(str(page_nums), 'html.parser').find_all('span')[-2].string
        for i in range(1, int(page_num) + 1):
            now_new_url = now_url + '/' + '{}'.format(i)
            new_response = requests.get(now_new_url, headers=header)
            Temp = BeautifulSoup(new_response.text, 'html.parser')
            image_url = Temp.find('div', attrs={'class': "main-image"}).img.attrs['src']
            image = requests.get(image_url,headers=header)
            name = str(image_url).split('/', 5)[-1]
            with open(path + '/' + name_dict[now_url] + '/' + name, 'wb') as f:
                f.write(image.content)
                print('正在爬取第'+str(main_num)+'个图库的第'+str(i)+'张图片,本页共'+page_num+'张照片。')
                time.sleep(random())


if __name__ == '__main__':
    start_time = time.time()
    get_main_url(url)
    get_image()
    end_time = time.time()
    print('耗时：' + str(end_time - start_time))
