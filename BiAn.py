import time
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import os

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36 Edg/81.0.416.58'
}

path = './spider/'
if os.path.exists(path):
    pass
else:
    os.mkdir(path)

menus_dict = {}  # 保存分类
image_lists = []  # 保存每张图片的页面链接
image_dict = {}  # 保存图片名字和下载链接


def get_info(url):  # 请求网页
    try:
        r = requests.get(url, headers=header)
        r.raise_for_status()
        r.encoding = 'gbk'
        return r
    except:
        print('请求失败！')


def image_menu(url):  # 获取分类及每个类型的网址存入 menus_dict
    soup = BeautifulSoup(get_info(url).text, 'html.parser')
    menu_lists = soup.find_all('a')[2:27]
    for i in menu_lists:
        menu_soup = BeautifulSoup(str(i), 'html.parser')
        menus_dict[menu_soup.a.string] = menu_soup.a.attrs['href']
    print('\n\n获取壁纸所有分类成功！')


def Type_image_urls(url, page_num):
    for num in range(1, int(page_num) + 1, 1):
        if num == 1:
            now_url = url
        else:
            now_url = url + '/index_{}.htm'.format(num)
        soup = BeautifulSoup(get_info(now_url).text, 'html.parser')
        image_info_list = soup.find_all('li')[5:]
        for image_info in image_info_list:
            image_list = BeautifulSoup(str(image_info), 'html.parser').a.attrs['href']
            if image_list == 'http://pic.netbian.com/':  # 过滤图片广告
                continue
            else:
                image_lists.append('http://www.netbian.com' + image_list)
    print(Type + ' 类型中的所有壁纸链接已加载完毕，\n即将开始准备图片下载链接：')


# <div class="pic"><p><a href="/desk/22607-***.htm" target="_blank"><img src="***.jpg" alt="***壁纸"
def get_image():
    for image_url in image_lists:
        soup = BeautifulSoup(get_info(image_url).text, 'html.parser')
        image_info = soup.find('p')
        image_dict[image_info.img.attrs['alt']] = image_info.img.attrs['src']
    print('图片下载链接已准备就绪，共有 {} 张照片。即将开始下载：'.format(len(image_dict.keys())))


def Download():
    #i = 1
    for image_url in image_dict:
    #for image_url in tqdm(image_dict, desc='正在下载：',ncols=50):  #改进为进度条显示
        if os.path.exists(path + Type):
            pass
        else:
            os.mkdir(path + Type)
        image = get_info(image_dict[image_url])
        # print(image_url+'\t'+image_dict[image_url])
        with open(path + Type + '/' + image_url + '.jpg', 'wb') as f:
            f.write(image.content)
            #print('正在保存 ' + Type + ' 壁纸中第 {} 张壁纸。'.format(i))
            #i += 1


def user_ui(url):
    global Type
    print('*************************************       欢迎使用 彼岸桌面 下载程序      **************************************')
    print(
        '-------------------------------------------      分        类      -------------------------------------------')
    for key in menus_dict:
        print(key + '\t', end='')
    Type = input('\n' + '请输入想要下载的壁纸类型: ')
    if Type == '4K壁纸':
        print('当前权限不足！无法对类型为 4K壁纸 的图片下载。')
    elif Type not in menus_dict:
        print('输入错误！正在退出。')
    else:
        page_num = input('请输入需下载的页数：')
        URl = url + menus_dict[Type]  # 具体的分类链接
        Type_image_urls(URl, page_num)


if __name__ == '__main__':
    url = 'http://www.netbian.com'
    # 获取分类链接
    time1 = time.time()
    image_menu(url)
    time2 = time.time()
    print('耗时：' + str(time2 - time1))

    user_ui(url)

    # 获取所有图片信息，包括名字和下载链接
    time3 = time.time()
    get_image()
    time4 = time.time()
    print('耗时：' + str(time4 - time3))

    # 下载
    time5 = time.time()
    Download()
    time6 = time.time()
    print('耗时：' + str(time6 - time5))
