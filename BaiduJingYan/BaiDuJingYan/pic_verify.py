import time

import ddddocr
import requests
from fake_useragent import UserAgent
from scrapy import Selector

headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "jingyan.baidu.com",
    "Origin": "https://jingyan.baidu.com",
    "Pragma": "no-cache",
    "Referer": "https://jingyan.baidu.com/verify.html",
    "User-Agent": str(UserAgent().random),
    "X-Requested-With": "XMLHttpRequest"
}

session = requests.session()


def get_code_img() -> str:
    verify_response = session.get("https://jingyan.baidu.com/verify.html", headers=headers, timeout=15)
    selector = Selector(text=verify_response.text)
    img_code_url = selector.xpath("//img[@id='code-img-e']/@src").extract_first()
    code_response = session.get(f"https://jingyan.baidu.com{img_code_url}", headers=headers, timeout=15)
    ocr = ddddocr.DdddOcr()
    code = ocr.classification(code_response.content)
    print("异常验证:", code, f"https://jingyan.baidu.com{img_code_url}")
    return code.strip()


def verify():
    while True:
        code = get_code_img()
        if len(code) == 5:
            json = {"method": "vertify", "vcode": code}
            ver = session.post("https://jingyan.baidu.com/submit/antispam", headers=headers, data=json, timeout=15)
            print("验证结果：", ver.json())
            if ver.json()["errno"] == 0:
                break
        time.sleep(30)


if __name__ == '__main__':
    verify()
