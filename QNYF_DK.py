import base64
import datetime
import hashlib
import random
from urllib.parse import quote

import requests
import time


def msg(name):
    url = 'https://qmsg.zendee.cn/send/6c44a7d4e24fa396f199fd950e123e54?msg=' + quote(name)
    r = requests.get(url)
    print(r.json()['reason'])


def getAttrs():
    random_str = ['1tddiejat2w', 's9rv1kijwz9', '0cr1jr4xjde', 'a0k8xrv1wyw', 'ewmww899uf7', 'jtev75ngjwg']
    time_str = int(time.time())
    sign_str_o = random.choice(random_str).upper() + str(time_str) + 'Q9y1Vr5sbjGwR8gekNCzELhZioQb9UZw'
    sign_str = hashlib.md5(sign_str_o.encode(encoding="utf-8")).hexdigest().upper()
    return str(time_str), sign_str


def get_verCode(base64_str):
    img = base64.b64decode(base64_str)
    resp = requests.post('http://yzm.qxp.red', data=img)
    code = resp.json()['code']
    return code


# class DK():
#     code = ""
#
#     def __init__(self):
#         self.see1 = requests.session()
#         self.header = {
#             'pragma': 'no-cache',
#             'origin': 'https://wxyqfk.zhxy.net',
#             'referer': 'https://wxyqfk.zhxy.net/?yxdm=13668',
#             'sign': getAttrs()[1],
#             'timestamp': getAttrs()[0],
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.68'
#         }
#
#
#         r3 = self.see1.get('https://yqfkapi.zhxy.net/api/common/getverifycode', headers=self.header).json()
#         self.code = get_verCode(r3['data']['img'])
#         print(self.code)
#         self.json1 = {
#             'A1': "正常",
#             'A2': "全部正常",
#             'A3': "中国四川省乐山市成都理工大学工程技术学院",
#             'A4': "无",
#             'JWD': "29.56099,103.731063",
#             'UID': 1242551,
#             'UserType': 1,
#             'YXDM': "13668",
#             'ZZDKID': 0,
#             'code': self.code,
#             'key': "9bb6d8f25537454f97654f4d03561b58",
#             'version': "v1.2.9"
#         }
#
#     def DK_action(self):
#         r1 = self.see1.post('https://yqfkapi.zhxy.net/api/ClockIn/Save', headers=self.header, json=self.json1)
#         print(r1.json())


# DK().DK_action()

wd_list = []
num = 0


class tem():
    ZCTW = None
    ZCTJSJ = None
    ZWTW = None
    ZWTJSJ = None
    WSTW = None
    WSTJSJ = None
    tb_now = None
    flag = True

    def __init__(self, uid):
        self.header1 = {
            'origin': 'https://wxyqfk.zhxy.net',
            'referer': 'https://wxyqfk.zhxy.net/?yxdm=13668',
            'sign': getAttrs()[1],
            'timestamp': getAttrs()[0],
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.68'
        }
        self.UID = uid
        self.check()
        tem_list = ['36.{}'.format(i) for i in range(2, 9)]
        if self.ZCTW == None:
            self.ZCTJSJ = self.tb_now
            self.ZCTW = random.choice(tem_list)
        else:
            if self.ZWTW == None:
                self.ZWTJSJ = self.ZCTJSJ = self.tb_now
                self.ZWTW = random.choice(tem_list)
            else:
                if self.WSTW == None:
                    self.WSTJSJ = self.ZWTJSJ = self.ZCTJSJ = self.tb_now
                    self.WSTW = random.choice(tem_list)
                else:
                    print("已全部填写！")
                    self.flag = False

    def check(self):
        self.now = datetime.datetime.now()
        params = {
            # 'UID': 1242551,
            'UID': self.UID,
            'usertype': 1,
            'yxdm': '13668',
            'date': self.now.strftime("%Y-%m-%d")
        }
        r1 = requests.get('https://yqfkapi.zhxy.net/api/ClockIn/gettem', params=params, headers=self.header1)
        try:
            self.ID = r1.json()['data']['ID']
            self.ZCTW = r1.json()['data']['ZCTW']
            self.ZWTW = r1.json()['data']['ZWTW']
            self.WSTW = r1.json()['data']['WSTW']
            self.tb_now = self.now.strftime("%Y-%m-%d %H:%M:%S")
            print('已填报信息获取成功！')
            self.first_flag = False
        except:
            self.first_flag = True

    def tem_action(self):
        global temp
        if self.flag:
            if self.first_flag:
                self.json2 = {
                    # 'UID': 1242551,
                    'UID': self.UID,
                    'UType': 1,
                    'YXDM': "13668",

                    'ZCTJSJ': self.ZCTJSJ,
                    'ZCTW': self.ZCTW,
                }
            else:
                self.json2 = {
                    'ID': self.ID,
                    'SBRQ': self.now.strftime("%Y-%m-%d") + " 00:00:00",
                    # 'UID': 1242551,
                    'UID': self.UID,
                    'UType': 1,
                    'YXDM': "13668",

                    'ZCTJSJ': self.ZCTJSJ,
                    'ZCTW': self.ZCTW,

                    'ZWTJSJ': self.ZWTJSJ,
                    'ZWTW': self.ZWTW,

                    'WSTJSJ': self.WSTJSJ,
                    'WSTW': self.WSTW
                }

            # 体温填报
            print("填报")
            ses = requests.session()
            # r1 = ses.post('https://yqfkapi.zhxy.net/api/ClockIn/SaveTem', headers=self.header1, json=self.json2).json()
            # print("体温填写通知：\n每日体温已填报({})\n早晨：{}\n中午：{}\n晚上：{}".format(self.now.strftime("%Y-%m-%d"), r1['data']['ZCTW'], r1['data']['ZWTW'], r1['data']['WSTW']))
            #

            wd_list.append(
                self.UID + " 的体温已填报({})\n早晨：{}\n中午：{}\n晚上：{}\n----------------".format(self.now.strftime("%Y-%m-%d"),
                                                                                       self.ZCTW, self.ZWTW, self.WSTW))


person_list = ['1242551', '1242552']
for uid in person_list:
    tem(uid).tem_action()
    # time.sleep(random.random()*20)

item2 = "\n".join(wd_list)
print(item2)
