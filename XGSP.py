import base64
import json
import os
import re

import requests

path = './'
rep = requests.get('https://ip.jiangxianli.com/api/proxy_ip')
proxy = {'HTTP': 'http://' + rep.json()['data']['ip'] + ':' + rep.json()['data']['port']}
print(proxy)


class XGSP:
    main_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.55'
    }

    video_headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'origin': 'https://www.ixigua.com',
        'referer': 'https://www.ixigua.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57'
    }

    def __init__(self, s_url):
        """
        CSDN ：高智商白痴
        CSDN个人主页：https://blog.csdn.net/qq_44700693
        :param s_url: 视频分享链接
        """
        self.url = s_url

    def XGSP_download(self):
        r = requests.get(self.url, proxies=proxy, headers=self.main_headers)
        r.encoding = 'utf-8'
        video_info = (re.findall('"packerData":{"video":(.*?)}}}},"', r.text)[0] + "}}}}").replace("undefined",
                                                                                                   '"undefined"')
        video_json = json.loads(video_info)
        video_name = video_json["title"].replace("|", "-").replace(" ", "")
        print("视频名：" + video_name)
        video_url = base64.b64decode(
            video_json['videoResource']['dash']['dynamic_video']['dynamic_video_list'][-1]['main_url']).decode("utf-8")
        print("视频链接：" + video_url)
        audio_url = base64.b64decode(
            video_json['videoResource']['dash']['dynamic_video']['dynamic_audio_list'][-1]['main_url']).decode("utf-8")
        print("音频链接：" + audio_url)
        with open(path + video_name + ".flv", "wb") as f:
            f.write(requests.get(video_url, proxies=proxy, headers=self.video_headers).content)
            print("视频文件下载完成...")
        with open(path + video_name + "-1.flv", "wb") as f:
            f.write(requests.get(audio_url, proxies=proxy, headers=self.video_headers).content)
        print("音视频均下载完成，即将开始拼接...")
        video_add_mp3("D:/Installed/ffmpeg-2020-09-30-essentials_build/bin/", path, path + video_name + ".flv",
                      path + video_name + "-1.flv")


def video_add_mp3(ffmpeg_path, save_path, file1_path, file2_path):
    """
    CSDN ：高智商白痴
    CSDN个人主页：https://blog.csdn.net/qq_44700693
    ffmpeg -i video.mp4 -i audio.m4a -c:v copy -c:a copy output.mp4
     视频添加音频
    :param ffmpeg_path: ffmpeg的安装 bin 路径
    :param save_path: 文件保存路径
    :param file1_path: 传入视频频文件的路径
    :param file2_path: 传入音频文件的路径
    :return:
    """
    mp4_name = file1_path.split('/')[-1].split('.')[0] + '-temp.mp4'
    mp3_name = file1_path.split('/')[-1].split('.')[0] + '-temp.mp3'
    outfile_name = file1_path.split('.')[0] + '.mp4'
    os.system(r'%sffmpeg -i %s %s' % (ffmpeg_path, file1_path, save_path + mp4_name))
    os.system(r'%sffmpeg -i %s %s' % (ffmpeg_path, file2_path, save_path + mp3_name))
    os.system(r'%sffmpeg -i %s -i %s -c:v copy -c:a copy %s' % (
        ffmpeg_path, save_path + mp4_name, save_path + mp3_name, outfile_name))
    os.remove(save_path + mp4_name)
    os.remove(save_path + mp3_name)
    os.remove(file1_path)
    os.remove(file2_path)


if __name__ == '__main__':
    s_url = input("请输入分享链接：")
    XGSP(s_url).XGSP_download()
