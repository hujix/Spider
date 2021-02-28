#          短视频平台无水印下载
#    目前仅支持皮皮虾，皮皮搞笑，抖音，腾讯微视，开眼，快手，抖音火山版，最右，VUE
#            后续会增加平台
#
import os
import random
import re

import parsel
import requests
from tqdm import tqdm

url = 'https://ip.jiangxianli.com/api/proxy_ip'
r = requests.get(url)
proxy = {'HTTP': 'http://' + r.json()['data']['ip'] + ':' + r.json()['data']['port']}
print(proxy)

path = './Desktop/'


class PPX():  # 皮皮虾
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72 '
    }

    def __init__(self, url):
        self.url = url

    def ppx_download(self):
        video_num = str(requests.get(self.url, proxies=proxy, headers=self.headers).url).split('/')[-1].split('?')[0]
        URL = 'https://h5.pipix.com/bds/webapi/item/detail/?item_id=' + video_num + '&source=share'
        r = requests.get(URL, proxies=proxy, headers=self.headers)
        video_name = r.json()['data']['item']['content'].replace(' ', '')
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video_url = r.json()['data']['item']['origin_video_download']['url_list'][0]['url']
        video = requests.get(video_url, proxies=proxy).content
        with open(path + str(video_name) + '.mp4', 'wb') as f:
            f.write(video)
        print("【皮皮虾】: {}.mp4 无水印视频下载完成！".format(video_name))


class PpxNew:  # 皮皮虾
    api_url = 'https://i-lq.snssdk.com/bds/cell/cell_comment/'
    headers = {
        'Accept-Encoding': 'gzip',
        'passport-sdk-version': '30',
        'sdk-version': '2',
        'User-Agent': 'ttnet okhttp/3.10.0.2',
        'Host': 'i-lq.snssdk.com',
        'Connection': 'Keep-Alive'
    }

    def __init__(self, s_url):
        if '/item/' in s_url:
            self.cell_id = s_url.split('?')[0].split('/')[-1]
        elif '/s/' in s_url:
            self.rel_url = requests.get(s_url, headers={'user-agent': 'Mozilla/5.0'}).url
            self.cell_id = self.rel_url.split('?')[0].split('/')[-1]
        self.param = {
            'cell_id': self.cell_id,
            'aid': '1319',
            'app_name': 'super',
        }

    def parse_url(self):
        response = requests.get(self.api_url, headers=self.headers, params=self.param)
        video = response.json()['data']['cell_comments'][0]['comment_info']['item']['video']
        video_name = video['text']
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video_url = video['video_high']['url_list'][0]['url']
        with open(path + str(video_name) + ".mp4", 'wb')as fp:
            fp.write(requests.get(video_url).content)
        print("【皮皮虾】: {}.mp4 无水印视频下载完成！".format(video_name))


class PPGX():  # 皮皮搞笑
    def __init__(self, url):
        s_url = url
        self.headers = {
            'Host': 'share.ippzone.com',
            'Origin': 'http://share.ippzone.com',
            'Referer': s_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52'
        }
        self.JSON = {
            "pid": int(str(s_url).split('=')[-1]),
            "mid": int(str(s_url).split('&')[-2].split('=')[-1]),
            "type": "post"
        }

    def ppgx_download(self):
        URL = 'http://share.ippzone.com/ppapi/share/fetch_content'
        r = requests.post(URL, proxies=proxy, headers=self.headers, json=self.JSON)
        video_name = r.json()['data']['post']['content'].replace(' ', '')
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video_url = r.json()['data']['post']['videos'][str(r.json()['data']['post']['imgs'][0]['id'])]['url']
        video = requests.get(video_url, proxies=proxy).content
        with open(path + str(video_name) + '.mp4', 'wb') as f:
            f.write(video)
        print("【皮皮搞笑】: {}.mp4 无水印视频下载完成！".format(video_name))


class DY():  # 抖音
    headers = {  # 模拟手机端
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/84.0.4147.105'
    }

    def __init__(self, s_url):
        self.s_url = str(s_url).replace('\n', '')
        self.url = re.findall('(https?://[^\s]+)', s_url)[0]  # 正则提取字符串中的链接

    def dy_download(self):
        rel_url = str(requests.get(self.url, proxies=proxy, headers=self.headers).url)
        if 'video' == rel_url.split('/')[4]:
            URL = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + rel_url.split('/')[5] + '&dytk='
            r = requests.get(URL, proxies=proxy, headers=self.headers)
            video_url = r.json()['item_list'][0]['video']['play_addr']['url_list'][0].replace('/playwm/', '/play/')
            video_name = r.json()['item_list'][0]['share_info']['share_title'].split('#')[0].split('@')[0].replace(' ',
                                                                                                                   '')
            if video_name == '':
                video_name = int(random.random() * 2 * 1000)
            if len(str(video_name)) > 20:
                video_name = video_name[:20]
            video = requests.get(video_url, proxies=proxy, headers=self.headers).content
            with open(path + str(video_name) + '.mp4', 'wb') as f:
                f.write(video)
            if 'www.iesdouyin.com' in self.s_url:
                print("【抖音短视频】: {}.mp4 无水印视频下载完成！".format(video_name))
            if 'v.douyin.com' in self.s_url:
                print("【抖音短视频/抖音极速版】: {}.mp4 无水印视频下载完成！".format(video_name))
        if 'user' == rel_url.split('/')[4]:
            URL = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=' + rel_url.split('=')[1].split('&')[0]
            print("douyin")


class TXWS():  # 腾讯微视
    headers = {  # 模拟手机端
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/84.0.4147.105'
    }

    def __init__(self, s_url):
        self.url = re.findall('(https?://[^\s]+)', s_url)[0]  # 正则提取字符串中的链接
        self.data = {
            'datalvl': "all",
            'feedid': str(self.url).split('/')[5],
            'recommendtype': '0',
            '_weishi_mapExt': '{}'
        }

    def txws_download(self):  # 参数 t 为随机数
        url = 'https://h5.weishi.qq.com/webapp/json/weishi/WSH5GetPlayPage?t={}&g_tk='.format(random.random())
        r = requests.post(url, proxies=proxy, headers=self.headers, data=self.data)
        video_name = r.json()['data']['feeds'][0]['feed_desc'].replace(' ', '')
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video_url = r.json()['data']['feeds'][0]['video_url']
        video = requests.get(video_url, proxies=proxy, headers=self.headers).content
        with open(path + str(video_name) + '.mp4', 'wb') as f:
            f.write(video)
        print("【腾讯微视】: {}.mp4 无水印视频下载完成！".format(video_name))


class KY_Eyepetizer():  # 开眼
    def __init__(self, url):
        self.vid = str(url).split('=')[1].split('&')[0]
        self.headers = {
            'origin': 'https://www.eyepetizer.net',
            'referer': url,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58'
        }

    def ky_download(self):
        url = 'https://baobab.kaiyanapp.com/api/v1/video/{}?f=web'.format(self.vid)
        r = requests.get(url, proxies=proxy, headers=self.headers)
        video_name = r.json()['title'].replace(' ', '')
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video_url = r.json()['playUrl']
        video = requests.get(video_url, proxies=proxy, headers=self.headers).content
        with open(path + str(video_name) + '.mp4', 'wb') as f:
            f.write(video)
        print("【开眼 Eyepetizer】: {}.mp4 无水印视频下载完成！".format(video_name))


class KS():  # 快手
    def __init__(self, s_url):
        self.s_url = s_url.replace('\n', '')
        self.url = re.findall('(https?://[^\s]+)', s_url)[0]  # 正则提取字符串中的链接
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/84.0.4147.105'
        }
        self.video_list = []
        self.rel_url = requests.get(self.url, proxies=proxy, headers=self.headers)  # 真实网址

    def ks_download(self):
        if 'user' != self.rel_url.url.split('/')[4]:
            self.ks_download_video()
        if 'user' == self.rel_url.url.split('/')[4]:
            self.ks_download_user()

    def ks_download_video(self):
        video_name = re.findall('name":"(.*?)"', self.rel_url.text)[0].replace(' ', '')
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video_url = re.findall('srcNoMark":"(.*?)"', self.rel_url.text)[0]
        video = requests.get(video_url, proxies=proxy, headers=self.headers).content
        with open(path + str(video_name) + '.mp4', 'wb') as f:
            f.write(video)
        if '【快手App】' in self.s_url:
            print("【快手】: {}.mp4 无水印视频下载完成！".format(video_name))
        elif '【快手极速版App】' in self.s_url:
            print("【快手极速版】: {}.mp4 无水印视频下载完成！".format(video_name))

    def ks_download_user(self):
        global user_name
        headers = {
            'Cookie': 'clientid=3; did=web_01d486186dce6601f3bc0ad63fe32e44; client_key=65890b29; didv=1597214426040; sid=17a010ca66bb1506257015b7',
            'Origin': 'https://c.kuaishou.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/84.0.4147.125'
        }
        rel_url = requests.get(self.url, proxies=proxy, headers=headers)  # 真实网址
        user_name = re.findall('<div class="name">(.*?)</div>', rel_url.text)[-1]
        if os.path.exists(path + user_name + '/'):
            pass
        else:
            os.makedirs(path + user_name + '/')
        videos = re.findall('<a href="(.*?)" role="ev" data-lazy=', rel_url.text)
        for video1 in videos:
            self.video_list.append('https://c.kuaishou.com' + video1)
        pcursor = ''
        url = 'https://c.kuaishou.com/rest/kd/feed/profile'
        flag = 1
        while flag:
            data = {"eid": str(rel_url.url).split('/')[-1].split('?')[0], "count": 18, "pcursor": pcursor}
            r = requests.post(url, proxies=proxy, headers=headers, json=data)
            for video2 in tqdm(r.json()['feeds'], desc='正在准备视频链接: '):
                photoId = video2['share_info'].split('=')[-1]
                temp_last = '?' + self.video_list[0].split('?')[-1]
                self.video_list.append('https://c.kuaishou.com/fw/photo/' + photoId + temp_last)
            pcursor = r.json()['pcursor']
            if r.json()['pcursor'] == "no_more":
                flag = 0
        print('用户 {} 共 {} 个视频！'.format(user_name, len(self.video_list)))
        for video_url in self.video_list:
            html = requests.get(video_url, headers={
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X)'})  # 真实网址
            print(html.text)
            video_name = int(random.random() * 2 * 1000)
            video_url = re.findall('srcNoMark":"(.*?)"', html.text)[0]
            video = requests.get(video_url, proxies=proxy, headers=headers).content
            with open(path + user_name + '/' + str(video_name) + '.mp4', 'wb') as f:
                f.write(video)
                print("【快手】: {}.mp4 无水印视频下载完成！".format(video_name))


class DY_HSB():
    headers = {  # 模拟手机
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/84.0.4147.105'
    }

    def __init__(self, s_url):
        self.s_url = s_url
        self.url = re.findall('(https?://[^\s]+)', s_url)[0]  # 正则提取字符串中的链接

    def dyhsb_download(self):
        rel_url = str(requests.get(self.url, proxies=proxy, headers=self.headers).url)
        if 'item' == rel_url.split('/')[4]:  # 单个视频
            video_name = int(random.random() * 2 * 1000)
            video_url = 'https://api.huoshan.com/hotsoon/item/video/_source/?item_id=' + \
                        rel_url.split('=')[1].split('&')[0]
            video = requests.get(video_url, proxies=proxy, headers=self.headers).content
            with open(path + str(video_name) + '.mp4', 'wb') as f:
                f.write(video)
            if '【抖音火山版】' in self.s_url:
                print("【抖音火山版】: {}.mp4 无水印视频下载完成！".format(video_name))
            elif '【火山极速版】' in self.s_url:
                print("【火山极速版】: {}.mp4 无水印视频下载完成！".format(video_name))
        if 'user' == rel_url.split('/')[4]:  # 用户视频
            ##########
            # 缺陷：最多支持下载 45 个该用户视频。
            ##########
            to_user_id = rel_url.split('=')[1].split('&')[0]
            info_json = requests.get('https://share.huoshan.com/api/user/info?encrypted_id={}'.format(to_user_id))
            item_count = info_json.json()['data']['item_count']
            user_name = info_json.json()['data']['nickname']
            if os.path.exists(path + user_name + '/'):
                pass
            else:
                os.makedirs(path + user_name + '/')
            videos_url = 'https://share.huoshan.com/api/user/video?encrypted_id={}&count={}'.format(to_user_id,
                                                                                                    item_count)
            video_info = requests.get(videos_url, proxies=proxy, headers=self.headers).json()['data']
            for info in tqdm(video_info, desc='正在下载用户 {} 的视频:'.format(user_name)):
                video_name = int(random.random() * 2 * 1000)
                video_url = 'https://api.huoshan.com/hotsoon/item/video/_source/?item_id=' + info['item_id']
                video = requests.get(video_url, proxies=proxy, headers=self.headers).content
                with open(path + user_name + '/' + str(video_name) + '.mp4', 'wb') as f:
                    f.write(video)
            if '【抖音火山版】' in self.s_url:
                print("【抖音火山版】: 用户 {} 的无水印视频下载完成！".format(user_name))
            elif '【火山极速版】' in self.s_url:
                print("【火山极速版】: 用户 {} 的无水印视频下载完成！".format(user_name))


class ZY():  # 最右
    headers = {  # 模拟成手机
        'Host': 'share.izuiyou.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/84.0.4147.105'
    }

    def __init__(self, s_url):
        self.url = re.findall('(https?://[^\s]+)', s_url)[0]  # 正则提取字符串中的链接

    def zy_download(self):
        global video_url
        url_flag = str(self.url).split('/')[3]
        if 'hybrid' == url_flag:
            html = requests.get(self.url, proxies=proxy, headers=self.headers).text
            flag = re.findall('"imgs":\[{"id":(.*?),"h":', html)[0]
            video_name = re.findall('{"id":.*?,"share":.*?,"content":"(.*?)","title":"', html)[0].replace(' ', '')
            if video_name == '':
                video_name = int(random.random() * 2 * 1000)
            if len(str(video_name)) > 20:
                video_name = video_name[:20]
            video_url = re.findall(',"thumb":' + flag + ',"playcnt":.*?"url":"(.*?)","prior', html)[0] \
                .replace('u002F', '').replace('\\', '/')
            video = requests.get(video_url, proxies=proxy).content
            with open(path + str(video_name) + '.mp4', 'wb') as f:
                f.write(video)
            print("【最右】: {}.mp4 无水印视频下载完成！".format(video_name))
        if 'topic' == url_flag:
            ###########
            #  缺陷：话题区最多下载 10  个视频
            ###########
            JSON = {
                'app': "zuiyou",
                'd': str(self.url).split('=')[2].split('&')[0],
                'm': str(self.url).split('=')[1].split('&')[0],
                'tid': int(str(self.url).split('/')[4].split('?')[0]),
                'ua': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/84.0.4147.125"
            }
            URL = 'https://share.izuiyou.com/api/topic/details'
            r = requests.post(URL, json=JSON, proxies=proxy, headers=self.headers)
            video_info = r.json()['data']['list']
            type_name = r.json()['data']['topic']['topic'].replace(' ', '')
            if os.path.exists(path + type_name + '/'):
                pass
            else:
                os.makedirs(path + type_name + '/')
            for video_info in tqdm(video_info, desc='正在下载类型 【{}】 的视频: '.format(type_name)):
                video_name = video_info['content'].replace(' ', '')
                if video_name == '':
                    video_name = int(random.random() * 2 * 1000)
                if len(str(video_name)) > 20:
                    video_name = video_name[:20]
                flag = video_info['imgs'][0]['id']
                try:
                    video_url = video_info['videos'][str(flag)]['url']
                    video = requests.get(video_url, proxies=proxy).content
                    with open(path + type_name + '/' + str(video_name) + '.mp4', 'wb') as f:
                        f.write(video)
                except:
                    pass
                try:
                    video_info1 = video_info['god_reviews'][0]['videos']
                    for a in tqdm(range(len(video_info1)), desc="正在下载该视频下的评论视频:"):
                        flag1 = video_info['god_reviews'][0]['imgs'][a]['id']
                        video_url1 = video_info['god_reviews'][0]['videos'][str(flag1)]['url']
                        video_name = int(random.random() * 2 * 1000)
                        video = requests.get(video_url1, proxies=proxy).content
                        with open(path + type_name + '/' + str(video_name) + '.mp4', 'wb') as f:
                            f.write(video)
                except:
                    pass
            print("【最右】: 类型 【{}】 无水印视频下载完成！".format(type_name))


class VUE():  # VUEvlog
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59'
    }

    def __init__(self, url):
        self.url = url

    def vue_download(self):
        rel = requests.get(self.url, proxies=proxy, headers=self.headers)
        if str(rel.url).split('/')[4] == 'post':  # 单个视频
            video_name = parsel.Selector(rel.text).xpath('//div[@class="videoTitle"]/text()').extract()[0].replace(' ',
                                                                                                                   '')
            if video_name == '':
                video_name = int(random.random() * 2 * 1000)
            if len(str(video_name)) > 20:
                video_name = video_name[:20]
            video_url = parsel.Selector(rel.text).xpath('//div[@class="videoContainer"]/video/@src').extract()[0]
            video = requests.get(video_url, proxies=proxy).content
            with open(path + str(video_name) + '.mp4', 'wb') as f:
                f.write(video)
            print("【VUE】: {}.mp4 视频下载完成！".format(video_name))
        if str(rel.url).split('/')[4] == 'topics':  # 主题视频
            all_li = parsel.Selector(rel.text).xpath('//div[@class="info-layout"]').extract()
            topics_name = re.findall('><span>(.*?)</span><', rel.text)[0].replace(' ', '')
            for li_info in tqdm(all_li, desc="正在下载类型为 {} 的视频:".format(topics_name)):
                video_name = re.findall('="post-title-text">(.*?)</span></div', li_info)[0].replace(' ', '').replace(
                    ':', '')
                if video_name == '':
                    video_name = int(random.random() * 2 * 1000)
                if len(str(video_name)) > 20:
                    video_name = video_name[:20]
                video_url = re.findall('src="(.*?)"', li_info)[1].replace(' ', '')
                if os.path.exists(path + topics_name + '/'):
                    pass
                else:
                    os.makedirs(path + topics_name + '/')
                video = requests.get(video_url, proxies=proxy).content
                with open(path + topics_name + '/' + str(video_name) + '.mp4', 'wb') as f:
                    f.write(video)
            print("【VUE】: 类型 【{}】 无水印视频下载完成！".format(topics_name))


class KKSP():
    def __init__(self, s_url):
        self.moviesId = str(s_url).split('=')[-1]
        self.headers = {
            'Host': 'svideo-api.kankan.com',
            'Origin': 'https://micro.kankan.com',
            'Referer': s_url,
            'terminal': 'H5',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44',
            'userid': '-1'
        }

    def kksp_download(self):
        global video_url, video_name
        url = 'https://svideo-api.kankan.com/microvision/getSetListByMoviesId?moviesId=' + self.moviesId
        r = requests.get(url, proxies=proxy, headers=self.headers)
        video_infos = r.json()['data']['moviesSetList']
        name = r.json()['data']['moviesName']
        if os.path.exists(path + name):
            pass
        else:
            os.makedirs(path + name)
        video_num = 0
        for video_info in tqdm(video_infos, desc="正在下载 {}: ".format(name)):
            video_num += 1
            video_name = '第{}集 '.format(video_num) + video_info['des']
            if video_name == '':
                video_name = int(random.random() * 2 * 1000)
            if len(str(video_name)) > 20:
                video_name = video_name[:20]
            video_url = video_info['moviesSetScreenList'][0]['vodurl']
            video = requests.get(video_url, proxies=proxy).content
            with open(path + name + '/' + str(video_name) + '.mp4', 'wb') as f:
                f.write(video)
        print("【看看视频】: {}.mp4 视频下载完成！".format(name))


def user_ui():
    print('*' * 10 + '\t 短视频平台无水印聚合下载\t' + '*' * 10)
    print('*' * 5 + "\t\t\tAuthor:  Hu.Sir\t\t\t" + '*' * 5)
    print('*' * 5 + '  (直接粘贴复制内容，程序会自动提取链接)  ' + '*' * 5)
    share_url = input('请输入分享链接: ')
    if 'h5.pipix.com' in share_url:  # 皮皮虾
        PpxNew(share_url).parse_url()
    if 'ippzone.com' in share_url:  # 皮皮搞笑
        PPGX(share_url).ppgx_download()
    if 'www.iesdouyin.com' in share_url or 'v.douyin.com' in share_url:  # 抖音  /  抖音极速版
        DY(share_url).dy_download()
    if 'share.huoshan.com' in share_url:  # 抖音火山版  /  火山极速版
        DY_HSB(share_url).dyhsb_download()
    if 'h5.weishi.qq.com' in share_url:  # 腾讯微视
        TXWS(share_url).txws_download()
    if 'www.eyepetizer.net' in share_url:  # 开眼视频
        KY_Eyepetizer(share_url).ky_download()
    if 'v.kuaishou.com' in share_url or 'v.kuaishouapp.com' in share_url:  # 快手  /  快手极速版
        KS(share_url).ks_download()
    if 'share.izuiyou.com' in share_url:  # 最右
        ZY(share_url).zy_download()
    if 'v.vuevideo.net' in share_url:  # VUEvlog
        VUE(share_url).vue_download()
    if 'micro.kankan.com' in share_url:  # 看看视频
        KKSP(share_url).kksp_download()


if __name__ == '__main__':
    user_ui()
