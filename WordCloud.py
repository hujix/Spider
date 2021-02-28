#
#  疫情词云
#

import json
import numpy as np
import PIL
import requests
import wordcloud
import matplotlib.pyplot as plt

data = {}

TEXT = requests.get("https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5").text
Data = TEXT.replace('\\', '').replace('"data":"{"l', '"data":{"l').replace(':true}}]}]}]}"}', ':true}}]}]}]}}')
relData = json.loads(Data)
for ch1 in relData['data']['areaTree'][0]['children']:
    for ch2 in ch1['children']:
        Name = ch2['name']
        Num = ch2['total']['confirm']
        data[Name]=Num

# wcloud=wordcloud.WordCloud(background_color='white',width=1800,height=900,font_path='‪C:/Windows/Fonts/STXINGKA.TTF')
# wcloud.generate_from_frequencies(frequencies=data)
#
# plt.figure(dpi=1200)
# plt.imshow(wcloud,interpolation='bilinear')
# plt.axis('off')
# plt.show()

mask1=np.array(PIL.Image.open('D:/view.jpg'))

wcloud=wordcloud.WordCloud(background_color='white',mask=mask1,font_path='‪C:/Windows/Fonts/STXINGKA.TTF')
wcloud.generate_from_frequencies(frequencies=data)

plt.figure(dpi=1000)
plt.imshow(wcloud,interpolation='bilinear')
plt.axis('off')
plt.show()

#
# 流行词词云
#

# import PIL
# import time
# import numpy
# import tqdm
# import random
# import parsel
# import requests
# import wordcloud
# import matplotlib.pyplot as plt
# from urllib.parse import quote
# 
# header = {
#     'Host': 'jikipedia.com',
#     'Connection': 'keep-alive',
#     'Origin': 'https://jikipedia.com',
#     'Referer': 'https://jikipedia.com/',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
#     'Cookie': '自行填写Cookies'
# }
# proxy = ['HTTP://106.42.216.132:9999', 'HTTP://115.221.242.206:9999', 'HTTP://163.204.245.77:9999',
#          'HTTP://114.224.223.164:9999', 'HTTP://125.108.78.245:9000', 'HTTP://120.83.98.217:9999',
#          'HTTP://112.84.98.40:9999', 'HTTP://122.4.42.59:9999']
# 
# data = {}
# num1 = 10

# def request(num2, url):
#     try:
#         proxies = {'http': random.choice(proxy)}
#         r = requests.get(url=url, headers=header, proxies=proxies)
#         r.raise_for_status()
#         r.encoding = 'utf-8'
#         return r
#     except:
#         warning(num2, 0)
# 
# 
# def fun(num2, url):
#     likes = []
#     try:
#         time.sleep(3)
#         html = request(num2, url).text
#         words = parsel.Selector(html).xpath('//a[@class="card-content"]//strong/text()').extract()
#         like_html = parsel.Selector(html).xpath('//div[@class="like button hoverable"]').extract()
#         for li in like_html:
#             like = parsel.Selector(li).xpath('//div/text()').extract()[-1]
#             if like != ' ':
#                 likes.append(like)
#             else:
#                 likes.append(0)
#         for num in range(20):
#             data[words[num]] = int(likes[num])
#     except:
#         warning(num2, 0)
# 
# 
# def draw():
#     mask1 = numpy.array(PIL.Image.open('./123.jpg'))
#     wcloud = wordcloud.WordCloud(background_color='white', mask=mask1, font_path='‪C:/Windows/Fonts/STXINGKA.TTF')
#     wcloud.generate_from_frequencies(frequencies=data)
# 
#     plt.figure(dpi=1200)
#     plt.imshow(wcloud, interpolation='bilinear')
#     plt.axis('off')
#     plt.show()
# 
# 
# def warning(num1, flag=1):  # 0  失败    1  成功
#     par = {"num": str(num1)}
#     if flag == 1:
#         temp = '成功事件码'
#     else:
#         temp = '失败事件码'
#     Parameters = {
#         'secretKey': 'key',
#         'appCode': '应用码',
#         'templateCode': temp,
#         'params': quote(str(par))
#     }
#     URL = 'https://api.wangfengta.com/api/alarm'
#     r = requests.get(URL, params=Parameters)
#     print(r.text)
# 
# 
# if __name__ == '__main__':
#     url = 'https://jikipedia.com/'
#     for num in tqdm.tqdm(range(num1),desc="正在统计："):
#         fun(num, url)
#     warning(num1)
#     draw()

