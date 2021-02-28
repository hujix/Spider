import os
import random
import time
from tkinter.scrolledtext import ScrolledText
import parsel
import requests
import threading
import tkinter as tk
import tkinter.messagebox
from tkinter.filedialog import askdirectory, StringVar

from bs4 import BeautifulSoup

proxies = ['HTTP://59.62.26.158:9000', 'HTTP://125.108.88.166:9000', 'HTTP://117.87.177.231:9000',
           'HTTP://123.101.67.81:9999', 'HTTP://175.42.128.186:9999', 'HTTP://117.69.12.139:9999',
           'HTTP://171.13.136.129:9999', 'HTTP://123.163.121.46:9999', 'HTTP://171.15.67.8:9999',
           'HTTP://122.200.90.11:48634', 'HTTP://182.46.251.204:9999']

Cookie = requests.get("http://www.fabiaoqing.com", proxies={'HTTP': random.choice(proxies)}).headers['Set-Cookie']
headers = {
    'Connection': 'keep-alive',
    'Host': 'www.fabiaoqing.com',
    'Cookie': Cookie,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

window = tk.Tk()  # 创建窗口
window.title('表情包下载器  -------  Hu.Sir')
window.iconbitmap('./emoji.ico')  # 图标
window.resizable(0, 0)  # 防止用户调整尺寸

path = 'D:/表情包/'
path1 = StringVar()
path1.set(path)


def choice_path():
    global path
    path_ = askdirectory()
    path1.set(path_ + '/表情包/')
    path = e1.get()


menu_dict = {}


def request_url(url):
    try:
        proxy = {'HTTP': random.choice(proxies)}
        r = requests.get(url, proxies=proxy, headers=headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r
    except:
        tk.messagebox.showinfo(title='网页请求', message='请求失败！！！')

def center_window(window, w, h):
    # 获取屏幕 宽、高
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))

center_window(window, 580, 300)

l1 = tk.Label(window, text='********                     ********', width=43, height=2).grid(row=1, column=2)
l2 = tk.Label(window, text='********      欢迎使用表情包下载程序      ********', font=('华文行楷', 16), width=43).grid(row=2,column=2)
l3 = tk.Label(window, text='********                     ********', width=43, height=2).grid(row=3, column=2)
l4 = tk.Label(window, text='-------------------------------------', width=43, height=2).grid(row=4, column=2)


def check_download1(e1, PATH, window, text, flag):
    num = int(e1.get())
    # num：页数    PATH：下载地址     window：插入窗口     text：被插入的文本域
    th = threading.Thread(target=hot_download(num, PATH, window, text, flag))
    th.setDaemon(True)  # 守护线程
    th.start()

def check_download2(url, e1, window, text, flag):
    num = int(e1.get())
    # num：页数    PATH：下载地址     window：插入窗口     text：被插入的文本域
    th = threading.Thread(target=menu_search_download(url, num, window, text, flag))
    th.setDaemon(True)  # 守护线程
    th.start()


def choice_fun1():
    global text1
    flag = 1
    PATH = path + '热门表情/'
    if os.path.exists(PATH):
        pass
    else:
        os.makedirs(PATH)
    url1 = 'https://www.fabiaoqing.com/biaoqing'
    window2 = tk.Tk()  # 创建窗口
    center_window(window2, 450, 400)
    window2.resizable(0, 0)  # 防止用户调整尺寸
    window2.title('热门表情下载')
    window2.iconbitmap('./hot.ico')  # 图标
    page_num =parsel.Selector(request_url(url1).text).xpath('//div[@class="ui pagination menu"]/a/text()').extract()[-4].strip()
    tk.Label(window2, text="请输入下载页数：", font=('Arial', 10), width=20).grid()
    tk.Label(window2, text="(每页 45 张，共 " + page_num + " 页。)", font=('Arial', 8), width=30).grid()
    e1 = tk.Entry(window2, font=('Arial', 10), width=10)
    e1.grid()
    tk.Button(window2, text='确认', font=('Arial', 9), width=6, height=1,
              command=lambda: check_download1(e1, PATH, window2, text1, flag)).grid()
    tk.Label(window2, text=" ", width=8).grid()
    tk.Label(window2, text="下载情况：").grid()
    tk.Label(window2, text=" ", width=8).grid()
    text1 = ScrolledText(window2, font=('微软雅黑', 10), width=53, height=12, fg='blue')
    text1.grid()
    window2.mainloop()


def choice_type(ra1):
    num = ra1.get()
    print(num)
    # name = list(menu_dict.keys())[num - 1]
    # page_num = parsel.Selector(request_url(menu_dict[name]).text).xpath(
    #     '//div[@class="ui pagination menu"]/a/text()').extract()[-2].strip()
    # num = int(input('请输入下载页数：（每页 10 套，共 {} 页。）'.format(page_num)))
    # menu_search_download(menu_dict[name], num)

def choice_fun2():
    url = 'https://www.fabiaoqing.com/bqb/lists'
    info_list = parsel.Selector(request_url(url).text).xpath(
        '//div[@class="ui secondary pointing blue menu"]/a').extract()
    for info in info_list:
        soup = BeautifulSoup(info, 'html.parser')
        # https://www.fabiaoqing.com/bqb/lists/type/hot.html
        menu_dict[soup.string.strip()] = 'https://www.fabiaoqing.com' + soup.a.attrs['href']
    window3 = tk.Tk()  # 创建窗口
    window3.title('分类菜单')
    window3.iconbitmap('C:/Users/Hu.Sir/Documents/PycharmProjects/MyDemo/资源/class.ico')  # 图标
    center_window(window3, 500, 600)
    window3.resizable(0, 0)  # 防止用户调整尺寸
    ra1 = tk.IntVar()
    row = 5
    column = 1
    if menu_dict:
        tk.Label(window3, text='菜单加载完成！').grid(row=1, column=2)
        tk.Label(window3, text='\n***************  目  录  *****************').grid(row=2, column=2)
        value = 1
        for menu in menu_dict.keys():
            if column % 3 == 0:
                tk.Radiobutton(window3, text=menu + '\t', variable=ra1, value=value).grid(row=row, column=column)
                row += 1
                column = 1
            else:
                tk.Radiobutton(window3, text=menu + '\t', variable=ra1, value=value).grid(row=row, column=column)
                column += 1
            value += 1
        tk.Label(window3, text=" ", font=('Arial', 10)).grid()
        tk.Button(window3, text='确定', font=('Arial', 10), width=6, height=1, command=lambda: choice_type(ra1)).grid(
            column=2)
    else:
        tk.messagebox.showinfo(title='菜单加载', message='菜单加载失败！')
    ra1.set(1)
    window3.mainloop()

def choice_fun30():
    window4 = tk.Tk()  # 创建窗口
    window4.title('搜索下载')
    window4.iconbitmap('./search.ico')  # 图标
    center_window(window4, 580, 500)
    # window4.resizable(0, 0)  # 防止用户调整尺寸
    tk.Label(window4, text="请输入需要下载的关键字：", font=('Arial', 10), width=20).grid(row=1, column=1)
    e2 = tk.Entry(window4, font=('Arial', 10), width=20)
    e2.grid(row=2, column=1)
    ra2 = tk.IntVar()
    tk.Radiobutton(window4, text="表情包", variable=ra2, value=1).grid(row=3, column=1)
    tk.Button(window4, text='开始', font=('Arial', 10), width=6, height=1,
              command=lambda: choice_fun31(ra2, e2, window4)).grid(row=4, column=2)
    tk.Radiobutton(window4, text="表情套图", variable=ra2, value=2).grid(row=5, column=1)
    ra2.set(1)

def choice_fun31(ra2, e2, window4):
    global keyword
    flag = 0
    choice = ra2.get()
    keyword = e2.get()
    if choice == 1:
        PATH = path + keyword + '/'
        if os.path.exists(PATH):
            pass
        else:
            os.makedirs(PATH)
        # https://www.fabiaoqing.com/search/search/keyword/%E5%B0%8F%E9%BB%84%E9%B8%AD/type/bq.html
        url2 = 'https://www.fabiaoqing.com/search/search/keyword/' + keyword + '/type/bq.html'
        page_num = \
            parsel.Selector(request_url(url2).text).xpath('//div[@class="ui pagination menu"]/a/text()').extract()[
                -2].strip()
        tk.Label(window4, text="请输入下载页数：", font=('Arial', 10), width=20).grid(column=2)
        tk.Label(window4, text="(每页 45 张，共 " + page_num + " 页。)", font=('Arial', 8), width=30).grid(column=2)
        e1 = tk.Entry(window4, font=('Arial', 10), width=10)
        e1.grid(column=2)
        tk.Button(window4, text='确认', font=('Arial', 9), width=6, height=1,
                  command=lambda: check_download1(e1, PATH, window4, text2, flag)).grid(column=2)
        tk.Label(window4, text=" ", width=8).grid()
        tk.Label(window4, text="下载情况：").grid()
        tk.Label(window4, text=" ", width=8).grid()
        text2 = ScrolledText(window4, font=('微软雅黑', 10), width=53, height=12, fg='blue')
        text2.grid()
    elif choice == 2:
        url3 = 'https://www.fabiaoqing.com/search/search/keyword/' + keyword + '/type/bqb.html'
        page_num = parsel.Selector(request_url(url3).text).xpath('//div[@class="ui pagination menu"]/a/text()') \
            .extract()[-2].strip()
        tk.Label(window4, text=" ", width=8).grid()
        tk.Label(window4, text="请输入下载页数：", font=('Arial', 10), width=20).grid()
        tk.Label(window4, text="(每页 8 套，共 " + page_num + " 页。)", font=('Arial', 8), width=30).grid()
        e1 = tk.Entry(window4, font=('Arial', 10), width=10)
        e1.grid()
        tk.Button(window4, text='确认', font=('Arial', 9), width=6, height=1,
                  command=lambda: check_download2(url3, e1, text3, window4, 0)).grid()
        tk.Label(window4, text=" ", width=8).grid()
        tk.Label(window4, text="下载情况：").grid()
        tk.Label(window4, text=" ", width=8).grid()
        text3 = ScrolledText(window4, font=('微软雅黑', 10), width=53, height=12, fg='blue')
        text3.grid()


def hot_download(num, path, window, text, flag):  # 直接下载热门和搜索
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
        for image_url in image_urls:
            # https://www.fabiaoqing.com/biaoqing/detail/id/650361.html
            URL1 = 'https://www.fabiaoqing.com' + image_url
            html = request_url(URL1).text
            name = parsel.Selector(html).xpath('//div[@class="swiper-slide swiper-slide-active"]/img/@title').extract()[
                0]
            NAME = str(name).replace('/', '').replace('\\', '').replace(':', '').replace('：', '').replace('"', '') \
                .replace('*', '').replace('?', '').replace('？', '').replace('|', '').replace('<', '').replace('>', '')
            image = parsel.Selector(html).xpath('//div[@class="swiper-slide swiper-slide-active"]/img/@src').extract()[
                0]
            proxy = {'HTTP': random.choice(proxies)}
            info = requests.get(image, proxies=proxy)
            time.sleep(random.random())
            with open(path + NAME + '.' + str(image).split('.')[-1], 'wb') as f:
                f.write(info.content)
            text.insert('end', '正在下载：' + NAME[:20] + '.' + str(image).split('.')[-1] + '\n')
            window.update()
            text.see(tk.END)
    text.insert(tk.END, '\n*********下载完成！********\n')
    window.update()


def menu_search_download(url, num, text, window, flag):  # 菜单方式下载，搜索方式下载
    global photos_url
    for page in range(1, num + 1):
        # https://www.fabiaoqing.com/bqb/lists/type/doutu/page/2.html
        URL = str(url).split('.html')[0] + '/page/{}.html'.format(page)  # 每一个类型翻页
        proxy = {'HTTP': random.choice(proxies)}
        response = requests.get(URL, proxies=proxy)
        time.sleep(random.random())
        if flag == 1:
            photos_url = parsel.Selector(response.text).xpath('//div[@class="right floated left aligned twelve wide column"]/a/@href').extract()  # 菜单套图链接
        elif flag == 0:
            photos_url = parsel.Selector(response.text).xpath('//div[@class="ui segment imghover"]/a/@href').extract()  # 搜索套图链接
        for photo_url in photos_url:
            # https://www.fabiaoqing.com/bqb/detail/id/9825.html
            URL1 = 'https://www.fabiaoqing.com' + photo_url  # 拼接成完整的套图链接 print(URL1)
            response1 = requests.get(URL1, proxies=proxy)
            time.sleep(random.random())
            image_urls = parsel.Selector(response1.text).xpath('//div[@class="swiper-slide swiper-slide-active bqpp"]/a/@href').extract()  # 拿到每个图的链接
            image_name = parsel.Selector(response1.text).xpath('//div[@class="ui segment imghover"]/h1/text()').extract()[0]  # 套图名称
            for image_url in image_urls:
                # https://www.fabiaoqing.com/biaoqing/detail/id/149344.html
                URL2 = 'https://www.fabiaoqing.com' + image_url
                response2 = requests.get(URL2, proxies=proxy)
                time.sleep(random.random())
                images_info = parsel.Selector(response2.text).xpath('//div[@class="swiper-slide swiper-slide-active"]/img').extract()  # 每张图片的信息list
                for image_info in images_info:
                    soup = BeautifulSoup(image_info, 'html.parser')
                    name1 = str(soup.img.attrs['title'])
                    image = requests.get(soup.img.attrs['src'], proxies=proxy)
                    NAME = name1.split('-')[0].strip().replace('/', '').replace('\\', '').replace(':', '') .replace('：', '').replace('"', '').replace('*', '').replace('?', '').replace('？', '').replace('|', '').replace('<', '').replace('>', '')
                    PATH = path + image_name + '/'
                    if os.path.exists(PATH):
                        pass
                    else:
                        os.makedirs(PATH)
                    with open(PATH + NAME + '.' + str(soup.img.attrs['src']).split('.')[-1], 'wb') as f:
                        f.write(image.content)
                    text.insert('end', '正在下载：' + NAME[:20] + '.' + str(soup.img.attrs['src']).split('.')[-1] + '\n')
                    window.update()
                    text.see(tk.END)
                text.insert(tk.END, '\n*********下载完成！********\n')
                window.update()


def fun_choice(ra):
    choice = ra.get()
    if choice == 1:
        choice_fun1()
    elif choice == 2:
        choice_fun2()
    elif choice == 3:
        choice_fun30()


ra = tk.IntVar()
tk.Label(window, text="下载位置：", font=('Arial', 10), width=8).grid(row=5, column=1)
e1 = tk.Entry(window, textvariable=path1, font=('Arial', 10), width=30)
e1.grid(row=5, column=2)
tk.Button(window, text='选择', font=('Arial', 10), width=6, height=1, command=lambda: choice_path()).grid(row=5, column=3)
tk.Label(window, text=" ", width=8).grid(row=6, column=1)
tk.Radiobutton(window, text="热门表情", font=('Arial', 10), variable=ra, value=1).grid(row=7, column=1)
tk.Radiobutton(window, text="获取菜单", font=('Arial', 10), variable=ra, value=2).grid(row=8, column=1)
tk.Radiobutton(window, text="搜索下载", font=('Arial', 10), variable=ra, value=3).grid(row=9, column=1)
tk.Button(window, text='开始', font=('Arial', 10), width=6, height=1, command=lambda: fun_choice(ra)).grid(row=8,
                                                                                                         column=2)

ra.set(2)

window.mainloop()
