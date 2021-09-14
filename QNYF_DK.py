# -*- coding: utf8 -*-
import base64
import hashlib
import random
import string

import ddddocr
import requests
import time


def send_msg(m_msg):
    url = 'https://qmsg.zendee.cn/send/xxx?msg=' + str(m_msg)
    r = requests.post(url)
    print(r.json())


def get_attrs() -> tuple:
    time_str = int(time.time())
    random_str = ''.join(random.sample(string.ascii_letters + string.digits, 11)).upper()
    print(f"【随机字符串】：{random_str}")
    sign_str_o = random_str + str(time_str) + 'Q9y1Vr5sbjGwR8gekNCzELhZioQb9UZw'
    sign_str = hashlib.md5(sign_str_o.encode(encoding="utf-8")).hexdigest().upper()
    return str(time_str), sign_str, random_str


def get_verify_code(base64_str):
    ocr = ddddocr.DdddOcr()
    res = ocr.classification(base64.b64decode(base64_str))
    return res


def get_header():
    attrs = get_attrs()
    temp = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/json;charset=UTF-8',
        'authorization': 'Bearer undefined',
        'origin': 'https://wxyqfk.zhxy.net',
        'referer': 'https://wxyqfk.zhxy.net/',
        'noncestr': attrs[2],
        'sign': attrs[1],
        'timestamp': attrs[0],
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78'
    }
    print(f"【请求头】：{str(temp)}")
    return temp


def dk_action():
    session = requests.session()

    session.get("https://yqfkapi.zhxy.net/api/ClockIn/IsClockIn?uid=xxx&usertype=1&yxdm=xxx",
                headers=get_header())

    r3 = session.get('https://yqfkapi.zhxy.net/api/common/getverifycode', headers=get_header())
    print("【验证码】：" + str(r3.json()))
    code = get_verify_code(r3.json()['data']['img'])
    print('【识别出的验证码】：' + code)
    time.sleep(random.random() * 2)
    json1 = {
        'A1': "正常",
        'A2': "全部正常",
        'A3': "xxx",
        'A4': "无",
        'JWD': "0,0",
        'UID': 111111,
        'UserType': 1,
        'YXDM': "xxx",
        'ZZDKID': 0,
        'code': code,
        'key': r3.json()['data']['key'],
        'version': "v1.3.2"
    }
    print("【请求体】：" + str(json1))
    r1 = session.post('https://yqfkapi.zhxy.net/api/ClockIn/Save', headers=get_header(), json=json1)
    print("【打卡返回信息：】" + str(r1.json()))
    # send_msg(f"【打卡返回信息：】: {str(r1.json())}")


def main_handler(event, context):
    dk_action()


if __name__ == '__main__':
    main_handler('', '')

# DK().DK_action()
#
# wd_list = []
# num = 0
#
#
# class tem():
#     ZCTW = None
#     ZCTJSJ = None
#     ZWTW = None
#     ZWTJSJ = None
#     WSTW = None
#     WSTJSJ = None
#     tb_now = None
#     flag = True
#
#     def __init__(self, uid):
#         self.header1 = {
#             'origin': 'https://wxyqfk.zhxy.net',
#             'referer': 'https://wxyqfk.zhxy.net/',
#             'sign': getAttrs()[1],
#             'timestamp': getAttrs()[0],
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.68'
#         }
#         self.UID = uid
#         self.check()
#         tem_list = ['36.{}'.format(i) for i in range(2, 9)]
#         if self.ZCTW == None:
#             self.ZCTJSJ = self.tb_now
#             self.ZCTW = random.choice(tem_list)
#         else:
#             if self.ZWTW == None:
#                 self.ZWTJSJ = self.ZCTJSJ = self.tb_now
#                 self.ZWTW = random.choice(tem_list)
#             else:
#                 if self.WSTW == None:
#                     self.WSTJSJ = self.ZWTJSJ = self.ZCTJSJ = self.tb_now
#                     self.WSTW = random.choice(tem_list)
#                 else:
#                     print("已全部填写！")
#                     self.flag = False
#
#     def check(self):
#         self.now = datetime.datetime.now()
#         params = {
#             # 'UID': 1242551,
#             'UID': self.UID,
#             'usertype': 1,
#             'yxdm': '13668',
#             'date': self.now.strftime("%Y-%m-%d")
#         }
#         r1 = requests.get('https://yqfkapi.zhxy.net/api/ClockIn/gettem', params=params, headers=self.header1)
#         try:
#             self.ID = r1.json()['data']['ID']
#             self.ZCTW = r1.json()['data']['ZCTW']
#             self.ZWTW = r1.json()['data']['ZWTW']
#             self.WSTW = r1.json()['data']['WSTW']
#             self.tb_now = self.now.strftime("%Y-%m-%d %H:%M:%S")
#             print('已填报信息获取成功！')
#             self.first_flag = False
#         except:
#             self.first_flag = True
#
#     def tem_action(self):
#         global temp
#         if self.flag:
#             if self.first_flag:
#                 self.json2 = {
#                     # 'UID': 1242551,
#                     'UID': self.UID,
#                     'UType': 1,
#                     'YXDM': "13668",
#
#                     'ZCTJSJ': self.ZCTJSJ,
#                     'ZCTW': self.ZCTW,
#                 }
#             else:
#                 self.json2 = {
#                     'ID': self.ID,
#                     'SBRQ': self.now.strftime("%Y-%m-%d") + " 00:00:00",
#                     # 'UID': 1242551,
#                     'UID': self.UID,
#                     'UType': 1,
#                     'YXDM': "13668",
#
#                     'ZCTJSJ': self.ZCTJSJ,
#                     'ZCTW': self.ZCTW,
#
#                     'ZWTJSJ': self.ZWTJSJ,
#                     'ZWTW': self.ZWTW,
#
#                     'WSTJSJ': self.WSTJSJ,
#                     'WSTW': self.WSTW
#                 }
#
#             # 体温填报
#             print("填报")
#             ses = requests.session()
#             # r1 = ses.post('https://yqfkapi.zhxy.net/api/ClockIn/SaveTem', headers=self.header1, json=self.json2).json()
#             # print("体温填写通知：\n每日体温已填报({})\n早晨：{}\n中午：{}\n晚上：{}".format(self.now.strftime("%Y-%m-%d"), r1['data']['ZCTW'], r1['data']['ZWTW'], r1['data']['WSTW']))
#             #
#
#             wd_list.append(
#                 self.UID + " 的体温已填报({})\n早晨：{}\n中午：{}\n晚上：{}\n----------------".format(self.now.strftime("%Y-%m-%d"),
#                                                                                        self.ZCTW, self.ZWTW, self.WSTW))
#
#
# person_list = ['1242551', '1242552']
# for uid in person_list:
#     tem(uid).tem_action()
#     # time.sleep(random.random()*20)
#
# item2 = "\n".join(wd_list)
# print(item2)
