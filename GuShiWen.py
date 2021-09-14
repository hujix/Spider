import ddddocr
import requests
from lxml import etree


class GuShiWen:
    def __init__(self):
        self.see = requests.session()
        self.url = "https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx"
        self.login_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-type': 'application/x-www-form-urlencoded',
            'cache-control': 'no-cache',
            'cookie': 'login=flase; Hm_lvt_9007fab6814e892d3020a64454da5a55=1629255250; ASP.NET_SessionId=jg1tgojygoaxadaslwpo3kq3;',
            'origin': 'https://so.gushiwen.cn',
            'referer': 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73'
        }

        self.code_header = {
            'accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie': 'Hm_lvt_9007fab6814e892d3020a64454da5a55=1629255250; ASP.NET_SessionId=jg1tgojygoaxadaslwpo3kq3; login=flase;',
            'referer': 'https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73'
        }

    def get_verify_code(self):
        code_url = "https://so.gushiwen.cn/RandCode.ashx"
        res = self.see.get(code_url, headers=self.code_header)
        ocr = ddddocr.DdddOcr()
        code = ocr.classification(res.content)
        return code

    def get_request_data(self) -> dict:
        response = self.see.get(self.url, headers=self.login_headers)
        view_state = etree.HTML(response.text).xpath('//input[@id="__VIEWSTATE"]/@value')[0]
        view_state_generator = etree.HTML(response.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value')[0]
        return {
            '__VIEWSTATE': view_state,
            '__VIEWSTATEGENERATOR': view_state_generator,
            'from': 'http://so.gushiwen.cn/user/collect.aspx',
            'email': 'aaa@9em.org',
            'pwd': '123456789',
            'code': self.get_verify_code(),
            'denglu': '登录'
        }

    def to_login(self):
        response = self.see.post(self.url, headers=self.login_headers, data=self.get_request_data())
        print(response.text)


if __name__ == '__main__':
    GuShiWen().to_login()
