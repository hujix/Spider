import os
import time
import parsel
import random
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

proxies = ['HTTP://182.32.246.171:9999', 'HTTP://163.204.241.13:9999', 'HTTP://171.35.169.194:9999',
           'HTTP://110.243.16.2:9999', 'HTTP://125.108.90.202:9000', 'HTTP://94.191.40.157:8118',
           'HTTP://125.108.85.2:9000', 'HTTP://123.169.164.30:9999', 'HTTP://113.121.39.100:9999',
           'HTTP://110.243.8.116:9999', 'HTTP://125.73.220.18:49128', 'HTTP://223.242.224.250:9999',
           'HTTP://1.197.203.238:9999', 'HTTP://49.85.211.213:8118', 'HTTP://110.243.27.11:9999',
           'HTTP://117.90.137.180:9000', 'HTTP://121.232.194.166:9000']
proxy = {'HTTP': random.choice(proxies)}
print(proxy)

headers = {
    'Connection': 'keep-alive',
    'Host': 'www.fabiaoqing.com',
    'Cookie': 'PHPSESSID=1c0pgtniprjr7uk00d8evsm2pv',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72 '
}

path = 'C:/Users/FullMoon/Desktop/Spider/'
if os.path.exists(path):
    pass
else:
    os.mkdir(path)

menu_dict = {}


def request_url(url):
    try:
        r = requests.get(url, proxies=proxy, headers=headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r
    except:
        print('请求失败！')


def menu_info(url):
    info_list = parsel.Selector(request_url(url).text).xpath(
        '//div[@class="ui secondary pointing blue menu"]/a').extract()
    for info in info_list:
        soup = BeautifulSoup(info, 'html.parser')
        # https://www.fabiaoqing.com/bqb/lists/type/hot.html
        menu_dict[soup.string.strip()] = 'https://www.fabiaoqing.com' + soup.a.attrs['href']
    if menu_dict:
        print('菜单加载完成！')
        print('\n***************  目  录  *****************')
        num = 1
        for menu in menu_dict:
            if num % 3 == 0:
                print('{}: '.format(num) + menu + '\n', end='')
            else:
                print('{}: '.format(num) + menu + '  \t', end='')
            num += 1
    else:
        print('菜单加载出错！')


def hot_download(num, path, flag=1):  # 直接下载热门和搜索
    global URL, image_urls
    for page in range(1, num + 1):
        if flag == 1:  # 热门下载
            # https://www.fabiaoqing.com/biaoqing/lists/page/1.html
            URL = 'https://www.fabiaoqing.com/biaoqing/lists/page/' + '{}.html'.format(page)
            image_urls = parsel.Selector(request_url(URL).text).xpath('//div[@class="tagbqppdiv"]/a/@href').extract()
        elif flag == 0:  # 搜索下载
            # https://fabiaoqing.com/search/search/keyword/%E5%B0%8F%E9%BB%84%E9%B8%AD/type/bq/page/1.html
            URL = 'https://fabiaoqing.com/search/search/keyword/' + keyword + '/type/bq/page/{}.html'.format(page)
            image_urls = parsel.Selector(request_url(URL).text).xpath(
                '//div[@class="searchbqppdiv tagbqppdiv"]/a/@href').extract()
        for image_url in tqdm(image_urls, desc='正在下载第 {} 页的表情图：'.format(page)):
            # https://www.fabiaoqing.com/biaoqing/detail/id/650361.html
            URL1 = 'https://www.fabiaoqing.com' + image_url
            image = parsel.Selector(request_url(URL1).text).xpath(
                '//div[@class="swiper-slide swiper-slide-active"]/img/@src').extract()[0]
            info = requests.get(image, proxies=proxy)
            time.sleep(random.random())
            with open(path + '/' + str(image).split('/')[-1], 'wb') as f:
                f.write(info.content)


def menu_search_download(url, num, flag=1):  # 菜单方式下载，搜索方式下载
    global photos_url
    for page in tqdm(range(1, num + 1), desc='正在下载：'):
        # https://www.fabiaoqing.com/bqb/lists/type/doutu/page/2.html
        URL = str(url).split('.html')[0] + '/page/{}.html'.format(page)  # 每一个类型翻页
        response = requests.get(URL, proxies=proxy)
        time.sleep(random.random())
        if flag == 1:
            photos_url = parsel.Selector(response.text).xpath(
                '//div[@class="right floated left aligned twelve wide column"]/a/@href').extract()  # 菜单套图链接
        elif flag == 0:
            photos_url = parsel.Selector(response.text).xpath(
                '//div[@class="ui segment imghover"]/a/@href').extract()  # 搜索套图链接
        for photo_url in photos_url:
            # https://www.fabiaoqing.com/bqb/detail/id/9825.html
            URL1 = 'https://www.fabiaoqing.com' + photo_url  # 拼接成完整的套图链接 print(URL1)
            response1 = requests.get(URL1, proxies=proxy)
            time.sleep(random.random())
            image_urls = parsel.Selector(response1.text).xpath(
                '//div[@class="swiper-slide swiper-slide-active bqpp"]/a/@href').extract()  # 拿到每个图的链接
            image_name = \
                parsel.Selector(response1.text).xpath('//div[@class="ui segment imghover"]/h1/text()').extract()[
                    0]  # 套图名称
            for image_url in image_urls:
                num1 = 1
                # https://www.fabiaoqing.com/biaoqing/detail/id/149344.html
                URL2 = 'https://www.fabiaoqing.com' + image_url
                response2 = requests.get(URL2, proxies=proxy)
                time.sleep(random.random())
                images_info = parsel.Selector(response2.text).xpath(
                    '//div[@class="swiper-slide swiper-slide-active"]/img').extract()  # 每张图片的信息list
                for image_info in images_info:
                    soup = BeautifulSoup(image_info, 'html.parser')
                    name1 = str(soup.img.attrs['title'])
                    image = requests.get(soup.img.attrs['src'], proxies=proxy)
                    if os.path.exists(path + image_name + '/'):
                        pass
                    else:
                        os.mkdir(path + image_name + '/')
                    with open(path + image_name + '/' + name1.split('-')[0].strip().replace('?', '').replace('/',
                                                                                                             '') + '.' +
                              str(soup.img.attrs['src']).split('.')[-1], 'wb') as f:
                        f.write(image.content)


def user_ui(url):
    print('*****************************************')
    print('<<<<<<<<  感谢使用***表情包下载程序  >>>>>>>>')
    print('*****************************************')
    print('\n1.热门表情        2.获取菜单       3.搜索下载')
    choice = int(input('请输入序号选择想要下载的方式：'))
    if choice != 1 and choice != 2 and choice != 3:
        print('输入有误！')
    elif choice == 1:
        url1 = 'https://www.fabiaoqing.com/biaoqing'
        page_num = parsel.Selector(request_url(url1).text).xpath(
            '//div[@class="ui pagination menu"]/a/text()').extract()[-4].strip()
        num = int(input('请输入下载页数：（每页 45 张，共 {} 页。）'.format(page_num)))
        PATH = path + '热门表情'
        if os.path.exists(PATH):
            pass
        else:
            os.mkdir(PATH)
        hot_download(num, PATH)
    elif choice == 2:
        menu_info(url)
        type = int(input('\n请输入序号选择需要下载的类型：'))
        name = list(menu_dict.keys())[type - 1]
        page_num = parsel.Selector(request_url(menu_dict[name]).text).xpath(
            '//div[@class="ui pagination menu"]/a/text()').extract()[-2].strip()
        num = int(input('请输入下载页数：（每页 10 套，共 {} 页。）'.format(page_num)))
        menu_search_download(menu_dict[name], num)
    elif choice == 3:
        global keyword
        keyword = input('请输入需要下载的关键字：')
        print('    1.仅图片        2.表情包')
        choice2 = int(input('请输入序号选择想要下载的方式：'))
        if choice2 != 1 and choice2 != 2:
            print('输入有误！')
        elif choice2 == 1:
            # https://www.fabiaoqing.com/search/search/keyword/%E5%B0%8F%E9%BB%84%E9%B8%AD/type/bq.html
            url2 = 'https://www.fabiaoqing.com/search/search/keyword/' + keyword + '/type/bq.html'
            page_num = parsel.Selector(request_url(url2).text).xpath(
                '//div[@class="ui pagination menu"]/a/text()').extract()[-2].strip()
            num = int(input('请输入下载页数：（每页 45 张，共 {} 页。）'.format(page_num)))
            PATH = path + keyword
            if os.path.exists(PATH):
                pass
            else:
                os.mkdir(PATH)
            hot_download(num, PATH, 0)
        elif choice2 == 2:
            url3 = 'https://www.fabiaoqing.com/search/search/keyword/' + keyword + '/type/bqb.html'
            page_num = parsel.Selector(request_url(url3).text).xpath(
                '//div[@class="ui pagination menu"]/a/text()').extract()[-2].strip()
            num = int(input('请输入下载页数：（每页 8 套，共 {} 页。）'.format(page_num)))
            menu_search_download(url3, num, 0)


if __name__ == '__main__':
    url = 'https://www.fabiaoqing.com/bqb/lists'
    user_ui(url)
