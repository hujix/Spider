import json

import requests
import parsel
from tqdm import tqdm

word_list = []


class QuWord:
    def __init__(self):
        self.base_url = "https://www.quword.com/ciku/id_0_0_0_0_{}.html"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                      "application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.quword.com',
            'Pragma': "no-cache",
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.30 "
        }

    def start(self):
        for page in tqdm(range(0, 2236 + 1), desc="正在下载"):
            response = requests.get(self.base_url.format(page), headers=self.headers)
            captions = parsel.Selector(response.text).xpath('//div[@class="row"]/div//div[@class="caption"]').extract()
            for caption in captions:
                selector = parsel.Selector(caption)
                word = selector.xpath("//h3/a/text()").extract_first()
                translate = str(selector.xpath("//p/text()").extract_first()).strip()
                temp = {
                    "word": word,
                    "tran": translate
                }
                word_list.append(temp)
        with open("./words.json", 'w', encoding="utf-8") as fp:
            fp.write(json.dumps(word_list, ensure_ascii=False))
        print(len(word_list))


if __name__ == '__main__':
    QuWord().start()
