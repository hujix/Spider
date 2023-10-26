# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# import jsonlines
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from BaiDuJingYan.redis_conn import redis_save_cache


class BaidujingyanPipeline:
    def __init__(self):
        self.item_list = []

    def process_item(self, item, spider):
        # self.item_list.append(item)
        # if len(self.item_list) >= 10:
        #     print(f"----------------------------保存{len(self.item_list)}-----------------------------")
        #     with jsonlines.open("./data.jsonl", "a") as fp:
        #         for temp in self.item_list:
        #             fp.write(temp)
        #             fp.write("\n")
        #     self.item_list.clear()
        page_id = item["url"].split("/")[-1].replace(".html", "")
        redis_save_cache(page_id, json.dumps(dict(item), ensure_ascii=False))
        return item
