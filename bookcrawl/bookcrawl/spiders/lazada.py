# -*- coding: utf-8 -*-
import datetime
import scrapy
import socket
import urlparse
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.http import Request
from bookcrawl.items import BooksItem


class LazadaSpider(CrawlSpider):
    name = 'lazada'
    allowed_domains = ['lazada.vn']
    start_urls = [
            "http://www.lazada.vn/sach-tieng-viet-van-hoc/",
            "http://www.lazada.vn/tu-truyen-hoi-ky-sach-tieng-viet/",
            "http://www.lazada.vn/sach-kinh-te-tieng-viet/",
            "http://www.lazada.vn/sach-ton-giao-sach-tieng-viet/",
            "http://www.lazada.vn/nghe-thuat-am-thuc-sach-tieng-viet/",
            "http://www.lazada.vn/sach-lich-su-sach-tieng-viet/",
            "http://www.lazada.vn/sach-nghe-thuat-giai-tri/",
            "http://www.lazada.vn/sach-luat-phap-sach-tieng-viet/",
            "http://www.lazada.vn/sach-y-khoa-sach-tieng-viet/",
            "http://www.lazada.vn/sach-nghe-thuat-song-sach-tieng-viet/",
            "http://www.lazada.vn/sach-van-hoc-sach-tieng-anh/",
            "http://www.lazada.vn/sach-khoa-hoc-gia-tuong-sach-tieng-anh/",
            ]

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//*[@class="c-paging__next-link"]')),
        Rule(LinkExtractor(
            restrict_xpaths='//*[contains(@class, "product-card")]'),
            callback='parse_item'),
    )

    def parse_item(self, response):
        l = ItemLoader(item=BooksItem(), response=response)

        l.add_xpath('name', '//*[@id="prod_title"]/text()', MapCompose(unicode.strip, unicode.title))
        l.add_xpath('price', '//*[@id="special_price_box"]/text()')
        l.add_value('description',
                    re.sub('<[^<]+?>', '', l.get_xpath('//*[@class="product-description__block"]')[0]).strip())
        l.add_value('image_uri', l.get_xpath('//*[@itemprop="image"]/@content')[1])

        # Information fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()
