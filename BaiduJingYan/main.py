import json
import logging
import math
import os.path

from scrapy import cmdline

logger = logging.getLogger("Scrapy")

file_path = "./seeds.json"
with open(file_path, "r", encoding="UTF-8") as fp:
    seed_source_list = list(json.loads(fp.read()))


def start_spider():
    spider_id = 4
    size = math.ceil(len(seed_source_list) / 5)
    seed_list = seed_source_list[spider_id * size:min(len(seed_source_list), (spider_id + 1) * size)]
    if not os.path.exists("./keyword.json"):
        with open("./keyword.json", "w", encoding="UTF-8") as f:
            f.write(json.dumps(seed_list, ensure_ascii=False))
    cmdline.execute("scrapy crawl JingYan".split())


if __name__ == '__main__':
    start_spider()
