import os
import requests
import random
from multiprocessing.pool import ThreadPool
from tqdm import tqdm

header = {
    'origin': 'https://www.pianku.tv',
    'referer': 'https://www.pianku.tv/py/lJWMpVmYqRWb_1.html?158064',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72'
}
proxies = ['HTTP://183.166.97.235:9999', 'HTTP://110.243.5.42:9999', 'HTTP://118.212.106.245:9999',
           'HTTP://222.93.72.121:8118', 'HTTP://106.46.108.163:9999', 'HTTP://121.233.206.212:9999',
           'HTTP://1.198.110.147:9999', 'HTTP://118.112.194.29:9999', 'HTTP://113.194.31.143:9999',
           'HTTP://117.131.235.198:8060', 'HTTP://123.169.115.78:9999', 'HTTP://118.212.106.253:9999',
           'HTTP://175.42.128.207:9999', 'HTTP://36.248.132.41:9999', 'HTTP://118.212.104.216:9999',
           'HTTP://163.204.244.70:9999', 'HTTP://182.148.206.23:9999', 'HTTP://123.169.167.215:9999',
           'HTTP://175.42.129.249:9999', 'HTTP://59.62.24.8:9000', 'HTTP://123.52.96.68:9999',
           'HTTP://163.204.241.119:9999', 'HTTP://110.249.176.26:8060', 'HTTP://1.193.244.253:9999',
           'HTTP://110.243.11.83:9999', 'HTTP://175.42.123.144:9999', 'HTTP://211.147.226.4:8118',
           'HTTP://115.218.6.108:9000', 'HTTP://163.204.244.136:9999', 'HTTP://120.234.138.100:53779',
           'HTTP://111.230.209.207:9999', 'HTTP://182.92.113.148:8118', 'HTTP://112.87.69.135:9999',
           'HTTP://175.43.84.159:9999', 'HTTP://175.43.179.11:9999', 'HTTP://59.62.24.183:9000',
           'HTTP://183.147.25.77:9000', 'HTTP://163.204.243.151:9999', 'HTTP://219.159.38.207:56210',
           'HTTP://124.93.201.59:42672', 'HTTP://113.194.31.36:9999', 'HTTP://36.248.133.247:9999',
           'HTTP://58.22.177.163:9999', 'HTTP://139.224.233.103:8118']

path = 'C:/Users/Hu.Sir/Desktop/Spider/'

if os.path.exists(path + "天气之子/"):
    pass
else:
    os.makedirs(path + "天气之子/")

failure_list = []  # 保存下载失败的片段


def download(num, flag=0):
    # https://youku.cdn7-okzy.com/20200508/19312_c9d456ff/1000k/hls/d3276cb1804001613.ts
    url = 'https://youku.cdn7-okzy.com/20200508/19312_c9d456ff/1000k/hls/d3276cb180400{:0>4d}.ts'.format(num)
    with open(path + "天气之子/" + str(url).split('/')[-1][-7:], 'wb') as f:
        proxy = {'HTTP': random.choice(proxies)}
        #print(proxy)
        try:
            r = requests.get(url, proxies=proxy, headers=header, timeout=4)
            r.raise_for_status()
            r.encoding = 'utf-8'
            print('正在下载第 {} 个片段。'.format(num))
            f.write(r.content)
            if flag == 1:
                failure_list.remove(num)
        except:
            print('请求失败！')
            if num not in failure_list:
                failure_list.append(num)


def get_video():
    files = os.listdir(path + "天气之子/")
    for file in tqdm(files, desc="正在转换视频格式："):
        if os.path.exists(path + "天气之子/" + file):
            with open(path + "天气之子/" + file, 'rb') as f1:
                with open(path + "天气之子.mp4", 'ab') as f2:
                    f2.write(f1.read())
        else:
            print("失败")


def check_ts():
    print("开始检查：")
    while failure_list:
        for num in failure_list:
            download(num, 1)
    print("ts 文件下载完成！")
    get_video()


if __name__ == '__main__':
    # 开启线程池
    pool = ThreadPool(100)
    results = pool.map(download, range(1, 1613 + 1))
    pool.close()
    pool.join()

check_ts()
