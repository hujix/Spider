import re

import execjs
import requests


class BaiDuTranslate:
    def __init__(self):
        self.base_url = "https://fanyi.baidu.com/"
        self.translate_url = "https://fanyi.baidu.com/v2transapi?from=en&to=zh"
        self.session = requests.session()
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                      "application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "dnt": "1",
            "Host": "fanyi.baidu.com",
            "Pragma": "no-cache",
            "Referer": "https://fanyi.baidu.com/",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
            "Sec-Fetch-Site": "cross-site",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.30 "
        }

    def _get_sign_and_token(self) -> tuple:
        self.session.get(self.base_url, headers=self.headers)
        response = self.session.get(self.base_url, headers=self.headers)
        gtk = re.findall(";window.gtk = '(.*)';", response.text)[0]
        token = re.findall("token: '(.*)',", response.text)[0]
        return gtk, token

    def translate(self, word: str):
        gtk, token = self._get_sign_and_token()
        with open("./baidu.js", 'r', encoding="utf-8") as fp:
            sign = execjs.compile(fp.read()).call("e", word, gtk)
        data = {
            "from": "en",
            "to": "zh",
            "query": word,
            "transtype": "translang",
            "simple_means_flag": "3",
            "sign": sign,
            "token": token,
            "domain": "common"
        }
        response = self.session.post(self.translate_url, headers=self.headers, data=data)
        print(response.text)


if __name__ == '__main__':
    BaiDuTranslate().translate("she")
