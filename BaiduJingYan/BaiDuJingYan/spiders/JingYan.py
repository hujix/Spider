import json
import logging

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from BaiDuJingYan.items import JingYanItem
from BaiDuJingYan.redis_conn import redis_check_exist


class JingYanSpider(scrapy.Spider):
    name = 'JingYan'
    allowed_domains = ['jingyan.baidu.com']
    logger = logging.getLogger("Scrapy")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open("./keyword.json", "r", encoding="UTF-8") as fp:
            self.keyword_list = list(json.loads(fp.read()))

    # start_urls = ['https://jingyan.baidu.com/search?word=xpath&lm=0&pn=0']

    def start_requests(self):
        for keyword in self.keyword_list:
            self.logger.info("切换关键词：" + keyword)
            self.keyword_list.remove(keyword)
            with open("./keyword.json", "w", encoding="UTF-8") as fp:
                fp.write(json.dumps(self.keyword_list, ensure_ascii=False))
            yield Request(url=f"https://jingyan.baidu.com/search?word={keyword}&lm=0&pn=0", dont_filter=True)

    def parse(self, response: HtmlResponse, **kwargs):
        current_href_list = response.selector.xpath("//div[@id='search-list']/dl/dt/a/@href").extract()
        for current_href in current_href_list:
            page_name = current_href.split("/")[-1].replace(".html", "")
            if redis_check_exist(page_name):
                continue
            yield Request(url=response.urljoin(current_href), callback=self.parse_detail)

        page_url_list = response.selector.xpath(
            '//div[@class="bottom-pager"]//a[not(contains(@class,"pg-btn-direction"))]/@href').extract()
        for page_url in page_url_list:
            yield Request(url=response.urljoin(page_url))

    @classmethod
    def parse_detail(cls, response: HtmlResponse, **kwargs):
        if "抱歉，没有找到" in str(response.text):
            return None
        jingyan_item = JingYanItem()
        jingyan_item["url"] = response.url
        jingyan_item["title"] = response.selector.xpath('//span[@class="title-text"]/text()').extract_first()
        if jingyan_item["title"] == "" or jingyan_item["title"] is None or len(jingyan_item["title"]) == 0:
            return Request(url=response.url)
        jingyan_item["html"] = response.selector.xpath('//span[@class="exp-content-outer"]').extract_first()
        return jingyan_item
