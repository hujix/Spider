import os
import time
import random
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import unquote

proxy = ['HTTP://125.108.84.103:9000', 'HTTP://118.126.107.41:8118', 'HTTP://113.194.23.84:9999',
         'HTTP://113.194.50.99:9999', 'HTTP://58.253.155.244:9999', 'HTTP://182.32.251.183:9999',
         'HTTP://120.83.104.120:9999', 'HTTP://113.121.67.66:9999', 'HTTP://114.239.172.17:9999',
         'HTTP://139.155.41.15:8118', 'HTTP://183.166.111.164:9999', 'HTTP://123.55.98.4:9999',
         'HTTP://123.169.166.127:9999', 'HTTP://110.243.26.86:9999', 'HTTP://118.212.107.10:9999',
         'HTTP://58.211.134.98:38480']

path = './Spider'
video_url = {}  # 搜索到的视频信息
episodes_url = {}  # 视频下载地址
episodes_urls = {}  # 分段视频链接
browser = webdriver.Chrome()


def search_get(keyword):
    try:
        input = browser.find_element_by_xpath('//*[@id="navbarSupportedContent"]/form/div/input')
        input.send_keys(keyword)
    except:
        print("搜索时出错！！！")
        exit()


vi_url = {}
def print_info(browser):
    try:
        all_info = browser.find_elements_by_xpath('//*[@id="search_list"]/ul/li')
        num = 0
        for info in all_info:
            num += 1
            vi_url[num] = info.find_element_by_class_name('stretched-link-').get_attribute('href')
            print('{}'.format(num), end='')
            print('\t' + info.text + '...')
            print("*" * 50 + '\n')
    except:
        print("获取搜索列表信息失败！！！")
        exit()


def video_urls(url):
    global rel_path
    try:
        browser.get(url)
        browser.implicitly_wait(5)
        time.sleep(3)
        video_info = browser.find_elements_by_xpath('//*[@id="plays_list"]/ul/li')
        name = browser.find_element_by_xpath('//*[@id="play"]/div[2]/div[2]/a/h5').text
        rel_path = path + '/' + str(name)
        if os.path.exists(rel_path):
            pass
        else:
            os.makedirs(rel_path)
        for info in video_info:
            video_url[info.text] = info.find_element_by_xpath('./a').get_attribute('href')
    except:
        print("获取视频链接出错！！！")
        exit()


def download_parsing():
    global route, piece, piecewise
    errow_url = list(video_url.keys())
    while errow_url:
        for name in errow_url:
            browser.get(video_url[name])
            browser.find_element_by_link_text(name).click()
            browser.implicitly_wait(5)
            time.sleep(4)
            try:
                piece = browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/span[1]').text
                piecewise = browser.find_elements_by_xpath('//span[@class="current_item_parts"]/button')
            except Exception as e:
                print("Error" + ': ' + str(type(e)) + str(e))
                print('该视频无分段！！！')
            try:
                if '请自行切换分段' not in piece:
                    route = browser.find_element_by_xpath('//*[@id="play"]/div[2]/div[1]/select/option').text
                    html = browser.execute_script("return document.documentElement.outerHTML")
                    URL = unquote(BeautifulSoup(html, 'html.parser').find('iframe').attrs['src'].split('=', 1)[-1])
                    if 'A' in route:
                        episodes_url[name] = URL.replace('&t=mp4', '')
                    else:
                        episodes_url[name] = URL
                else:
                    for pie in piecewise:  # 分段视频
                        try:
                            pie.click()
                        except Exception as e:
                            print(name + ": Error 001" + ': ' + str(type(e)) + str(e))
                        route = browser.find_element_by_xpath('//*[@id="play"]/div[2]/div[1]/select/option').text
                        html = browser.execute_script("return document.documentElement.outerHTML")
                        URL = unquote(BeautifulSoup(html, 'html.parser').find('iframe').attrs['src'].split('=', 1)[-1])
                        if 'A' in route:
                            episodes_urls.setdefault(name, []).append(URL.replace('&t=mp4', ''))
                        else:
                            episodes_urls.setdefault(name, []).append(URL)
                        time.sleep(1)
                errow_url.remove(name)
            except Exception as e:
                print("Error" + ': ' + str(type(e)) + str(e))
                print('获取{}的视频下载链接失败！！！'.format(name))


def video_download():
    global rel_path
    proxies = {'HTTP': random.choice(proxy)}
    if episodes_url:   # 下载没有分段的视频
        for name in tqdm(episodes_url, desc='正在下载: '):
            r = requests.get(episodes_url[name], proxies=proxies)
            with open(rel_path + '/' + name + '.mp4', 'wb') as f:
                f.write(r.content)
    if episodes_urls:  # 下载含有分段的视频
        for name in tqdm(episodes_urls, desc='正在下载: '):
            for epi_url in episodes_urls[name]:
                if os.path.exists(rel_path + '/' + name + '.mp4'):
                    r = requests.get(epi_url, proxies=proxies)
                    with open(rel_path + '/' + name + '1.mp4', 'wb') as f:
                        f.write(r.content)
                else:
                    r = requests.get(epi_url, proxies=proxies)
                    with open(rel_path + '/' + name + '.mp4', 'wb') as f:
                        f.write(r.content)


def user_ui():
    try:
        print('#' * 25 + "\tAGE动漫搜索下载\t" + '#' * 25)
        browser.get('http://agefans.org/')
        keyword = input('请输入搜索的关键字：')
        search_get(keyword + '\n')
        print_info(browser)
        choise = int(input('请输入序号选择：'))
        name = list(vi_url.keys())[choise - 1]
        video_urls(vi_url[name])
        download_parsing()
    except:
        print("未知错误！！！")
    finally:
        time.sleep(5)
        browser.close()

if __name__ == '__main__':
    user_ui()
    video_download()
