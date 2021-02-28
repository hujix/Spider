import os
import time
import parsel
import random
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import unquote

referer = 'http://agefans.org/'
header = {
    'Cookie': '自行填写Cookies',
    'Host': 'agefans.org',
    'Referer': referer,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
}
proxy = ['HTTP://113.195.225.104:9999', 'HTTP://110.243.6.125:9999', 'HTTP://58.215.201.98:56566',
         'HTTP://115.221.245.165:9999', 'HTTP://110.243.15.112:9999', 'HTTP://115.221.242.162:9999',
         'HTTP://218.59.193.14:38640', 'HTTP://120.198.76.45:41443', 'HTTP://113.128.9.88:9999',
         'HTTP://110.243.31.141:9999', 'HTTP://125.108.84.103:9000', 'HTTP://120.83.101.89:9999',
         'HTTP://113.194.135.166:9999', 'HTTP://118.126.107.41:8118']

path = './Spider'
video_url = {}  # 搜索到的视频信息
episodes_url = {}  # 视频下载地址
episodes_urls = {}  #分段视频链接


# rsp = requests.get('https://ip.jiangxianli.com/api/proxy_ip').json()
# protocol = rsp['data']['protocol']
# IP = rsp['data']['ip'] + ':' + rsp['data']['port']
# proxies = {protocol: protocol + '://' + IP}
# print(proxies)


def request(url):
    proxies = {'HTTP': random.choice(proxy)}
    try:
        r = requests.get(url, headers=header,proxies=proxies)
        r.raise_for_status()
        r.encoding = 'utf-8'
        time.sleep(2)
        return r
    except Exception as e:
        print('request(url) : Error :' + str(type(e)) + ' : ' + str(e))


def print_info(url):  # 输出搜索到的视频信息
    html = request(url).text
    search_info = parsel.Selector(html).xpath('//*[@id="search_list"]/ul//div[@class="card-body p-2"]').extract()
    Serial = 0
    for info in search_info:
        Serial += 1
        soup = BeautifulSoup(info, 'html.parser')
        video_url[soup.a.h5.string] = 'http://agefans.org' + soup.a.attrs['href']
        print("{:0>2d}:\t《 ".format(Serial) + soup.a.h5.string + ' 》')
        for div in soup.find_all('div', {'class': ''}):
            print('\t' + div.span.string + div.span.next_sibling.next_sibling.string)
        num = 0
        for li in soup.find_all('li'):
            num += 1
            if num % 2 != 0:
                print('\t' + li.span.string + li.span.next_sibling.next_sibling.string, end='')
            else:
                print('\t' + li.span.string + li.span.next_sibling.next_sibling.string)
        intro = soup.find('div', {'class': 'ellipsis_summary catalog_summary small'})
        try:
            print('\t' + intro.span.string + intro.span.next_sibling.next_sibling.string.replace('\n', '') + '...')
        except:
            content = str(intro.span.next_sibling.next_sibling).replace('\n', '').replace('<span>', '').replace(
                '<br/>', '').replace('</span>', '').replace('&lt;', '') + '...'
            print('\t' + intro.span.string + content)
        print('\n' + '=' * 30 + '\n')


def get_relurl(name):
    global referer, rel_path
    rel_path = path + '/' + name
    if os.path.exists(rel_path):
        pass
    else:
        os.makedirs(rel_path)
    referer = video_url[name]
    html = request(video_url[name]).text
    time.sleep(random.random())
    all_li = parsel.Selector(html).xpath('//div[@id="plays_list"]/ul/li').extract()
    for info in tqdm(all_li, desc='正在获取视频链接：'):
        li = BeautifulSoup(info, 'html.parser')
        url = 'http://agefans.org/myapp/_get_ep_plays?{}&anime_id={}'.format(li.a.attrs['href'].split('_', 1)[-1].replace('_', '='), video_url[name].split('/')[-1])
        referer = video_url[name] + li.a.attrs['href']
        ID=request(url).json()['result'][0]['id']
        try:
            new_url = 'http://agefans.org/myapp/_get_e_i?url={}&quote=1'.format(ID)
            episodes_url[li.a.string.replace(' ', '')] = unquote(request(new_url).json()['result'])
        except:
            try:
                new_url = 'http://agefans.org/myapp/_get_mp4s?id={}'.format(ID)
                url_lists = request(new_url).json()
                if url_lists:
                    episodes_urls[li.a.string.replace(' ', '')] = url_lists
                else:
                    new_url = 'http://agefans.org/myapp/_get_raw?id={}'.format(ID)
                    episodes_urls.setdefault(li.a.string.replace(' ', ''), []).append(request(new_url).text)
            except Exception as e:
                print(type(e), e)


def video_download():
    global rel_path
    proxies = {'HTTP': random.choice(proxy)}
    if episodes_url:
        for name in tqdm(episodes_url, desc='正在下载: '):
            r = requests.get(episodes_url[name], proxies=proxies)
            with open(rel_path + '/' + name + '.mp4', 'wb') as f:
                f.write(r.content)
    else:
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
    print('#' * 25 + '\tAGE动漫离线助手\t' + '#' * 25)
    keyword = input('请输入搜索关键字：')
    url = 'http://agefans.org/search?q=' + keyword
    print_info(url)
    choice = int(input('请输入序号选择：'))
    name = list(video_url.keys())[choice - 1]
    start = time.time()
    get_relurl(name)
    video_download()
    end = time.time()
    print("下载完成！共耗时：{}".format(end - start))


if __name__ == '__main__':
    user_ui()
