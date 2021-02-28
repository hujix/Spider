import os
import random
import requests
from tqdm import tqdm
from multiprocessing.pool import ThreadPool

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72'
}
proxies = ['HTTP://183.166.97.235:9999', 'HTTP://110.243.5.42:9999', 'HTTP://118.212.106.245:9999',
           'HTTP://124.93.201.59:42672', 'HTTP://113.194.31.36:9999', 'HTTP://36.248.133.247:9999',
           'HTTP://58.22.177.163:9999', 'HTTP://139.224.233.103:8118']

path = './Spider/'

if os.path.exists(path + "movie_name/"):
    pass
else:
    os.makedirs(path + "movie_name/")

failure_list = []  # 保存下载失败的片段


def download(num, flag=0):  # 下载所有的 ts文件
    url = 'https://********{:0>4d}.ts'.format(num)  # 当原 ts文件 路径的后缀依次递增时
    with open(path + "movie_name/" + str(url)[-7], 'wb') as f:  # str(url)[-7] 截取后面的4位数为片段名字，
        proxy = {'HTTP': random.choice(proxies)}
        try:
            r = requests.get(url, proxies=proxy, headers=header, timeout=4)
            r.raise_for_status()
            r.encoding = 'utf-8'
            print('正在下载第 {} 个片段。'.format(num))
            f.write(r.content)
            if flag == 1:  # 如果下载成功，则从失败列表中删除
                failure_list.remove(num)
        except:
            print('请求失败！')
            if num not in failure_list:  # 下载失败后就追加到列表中
                failure_list.append(num)


#
# 思路：下载所有的 ts文件（依次递增），遍历从小到大的 ts文件，以追加写打开目标文件，将遍历到的文件数据读出，然后写入目标文件。
#
# 改进：下载完成后删除当前 ts文件
def get_video():
    files = os.listdir(path + "movie_name/")  # 获取当前文件夹下的所有文件名，返回一个 list
    for file in tqdm(files, desc="正在转换视频格式："):
        if os.path.exists(path + "movie_name/" + file):
            with open(path + "movie_name/" + file, 'rb') as f1:  # 从小遍历 ts文件
                with open(path + "movie_name.mp4", 'ab') as f2:  # 打开下载的目标文件
                    f2.write(f1.read())
        else:
            print("失败")


#  改进：可以改为线程池检测
def check_ts():
    print("开始检查：")
    while failure_list:  # []、{}、() 为 False
        for num in failure_list:
            download(num, 1)
    print("ts 文件下载完成！")
    get_video()  # 当所有 ts文件 下载完成后


if __name__ == '__main__':
    # 开启线程池
    pool = ThreadPool(100)
    results = pool.map(download, range(0, MAX_Num))
    pool.close()
    pool.join()

check_ts()
