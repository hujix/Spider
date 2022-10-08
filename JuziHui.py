import json

import requests
import parsel
from tqdm import tqdm

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "www.juzih.com",
    "Pragma": "no-cache",
    "Referer": "http://www.juzih.com/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50"
}


class JuZiHui:
    def __init__(self):
        self.url = "http://www.juzih.com/"
        self.target_dict = {}

    def _get_header_menu(self) -> dict:
        response = requests.get(self.url, headers=headers)
        response.encoding = "gb2312"
        menu_list = parsel.Selector(response.text).xpath(
            '//div[@class="header-menu"]//div[@class="nav"]/li[not(@class!="sep")]/a').extract()
        menu_dict = {}
        for menu in menu_list:
            temp = parsel.Selector(menu)
            path = temp.xpath("//@href").extract_first()
            if path == "/":
                continue
            menu_dict[f"http://www.juzih.com{path}"] = temp.xpath("//text()").extract_first()
        return menu_dict

    @classmethod
    def _get_sub_menu(cls, header_url) -> dict:
        response = requests.get(header_url, headers=headers)
        response.encoding = "gb2312"
        sub_title_list = parsel.Selector(response.text).xpath("//div[@class='childs']/a").extract()
        sub_menu_dict = {}
        for sub_title in sub_title_list:
            temp = parsel.Selector(sub_title)
            path = temp.xpath("//@href").extract_first()
            sub_menu_dict[f"http://www.juzih.com{path}"] = temp.xpath("//text()").extract_first()
        return sub_menu_dict

    @classmethod
    def _get_sentence(cls, sub_url) -> dict:
        response = requests.get(sub_url, headers=headers)
        response.encoding = "gb2312"
        sentence_list = parsel.Selector(response.text).xpath("//ul[@class='alist']/li//a").extract()
        sentence_url_dict = {}
        for sentence in sentence_list:
            temp = parsel.Selector(sentence)
            sentence_url_dict[f'http://www.juzih.com{temp.xpath("//@href").extract_first()}'] = \
                temp.xpath("//text()").extract_first()
        return sentence_url_dict

    @classmethod
    def _get_sentence_list(cls, sentence_url) -> list:
        response = requests.get(sentence_url, headers=headers)
        response.encoding = "gb2312"
        return parsel.Selector(response.text).xpath("//div[@class='content']/p/text()").extract()

    def run(self):
        target_dict = {}
        for key, value in tqdm(self._get_header_menu().items(), desc="大标题进度："):
            sub_dict = {}
            for sub_key, sub_value in tqdm(self._get_sub_menu(key).items(), desc="小标题进度："):
                sentence_dict = {}
                for sentence_key, sentence_value in self._get_sentence(sub_key).items():
                    sentence_dict[sentence_value] = self._get_sentence_list(sentence_key)
                sub_dict[sub_value] = sentence_dict
            target_dict[value] = sub_dict
        with open("jzh-target.json", "w", encoding="UTF-8") as fp:
            fp.write(json.dumps(target_dict, ensure_ascii=False))


if __name__ == '__main__':
    JuZiHui().run()
