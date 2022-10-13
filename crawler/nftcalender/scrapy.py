# -*- coding: utf-8 -*-
#第二步，创建项目，执行一下命令

#scrapy startproject novel

#第三步，编写spider文件，文件存放位置novel/spiders/toscrape-xpath.py，内容如下


import scrapy


class ToScrapeSpiderXPath(scrapy.Spider):
    # 爬虫的名字
    name = 'novel'
    # 爬虫启始url
    start_urls = [
        'https://www.xbiquge6.com/0_638/1124120.html',
    ]

    def parse(self, response):
        # 定义存储的数据格式
        yield {
            'text': response.xpath('//div[@class="bookname"]/h1[1]/text()').extract_first(),
            'content': response.xpath('//div[@id="content"]/text()').extract(),
            # 'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
            # 'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
        }
        # 下一章的链接
        next_page_url = response.xpath('//div[@class="bottem1"]/a[3]/@href').extract_first()
        # 如果下一章的链接不等于首页 则爬取url内容  ps：最后一章的下一章链接为首页
        if next_page_url != 'https://www.xbiquge6.com/0_638/':
            yield scrapy.Request(response.urljoin(next_page_url))
