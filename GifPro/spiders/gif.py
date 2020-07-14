# -*- coding: utf-8 -*-
import scrapy

from GifPro.items import GifproItem


class GifSpider(scrapy.Spider):
    name = 'gif'
    allowed_domains = ['www.doutula.com']
    start_urls = ['http://www.doutula.com/']

    def parse(self, response):
        nums = response.xpath('//ul[@class="pagination"]/li[last()-1]').extract_first()
        if nums:
            for i in range(4, 655):
                url = "https://www.doutula.com/article/list/?page={}".format(i)
                yield scrapy.Request(
                    url=url,
                    dont_filter=True,
                    callback=self.gifparse
                )
        else:
            print("页面出错,爬取停止")


    def gifparse(self, response):
        a_list = response.xpath('//div[@class="col-sm-9 center-wrap"]/a')
        for a in a_list:
            url_detail = a.xpath('./@href').extract_first()
            title_detail = a.xpath('./div[@class="random_title"]/text()').extract_first()
            yield scrapy.Request(
                url=url_detail,
                meta={'title_detail': title_detail},
                callback=self.detail_parse
            )

    def detail_parse(self, response):
        item = GifproItem()
        title = response.meta['title_detail']
        tag = ""
        tag_list = []
        if "pic-footer" in response.text:
            try:
                pic_tips = response.xpath('//div[@class="pic-tips"]/a')
            except Exception as e:
                tag_list = []
            else:
                for tips in pic_tips:
                    tip = tips.xpath('./text()').extract_first()
                    tip_list = tip.split()
                    tag_list.extend(tip_list)
        print('tag_list', tag_list)
        if len(tag_list) > 1:
            tag = "、".join(tag_list)
        elif len(tag_list) == 1:
            tag = tag_list[0]
        else:
            tag = ''
        pics = response.xpath('//div[@class="artile_des"]//a/img/@src').extract()
        print(pics)
        print("---"*50)

        item['title'] = title
        item['tag'] = tag
        item['pics'] = pics

        yield item


