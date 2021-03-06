import scrapy

import js2xml


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://spidyquotes.herokuapp.com/js"]
    download_delay = 1.5

    def parse(self, response):
        script = response.xpath(
            '//script[contains(., "var data =")]/text()'
        ).extract_first()
        sel = scrapy.Selector(_root=js2xml.parse(script))
        for quote in sel.xpath('//var[@name="data"]/array/object'):
            yield {
                "texto": quote.xpath(
                    'string(./property[@name="text"])'
                ).extract_first(),
                "autor": quote.xpath(
                    'string(./property[@name="author"]//property[@name="name"])'
                ).extract_first(),
                "tags": quote.xpath(
                    './property[@name="tags"]//string/text()'
                ).extract(),
            }

        link_next = response.css('li.next a::attr("href")').extract_first()
        if link_next:
            yield scrapy.Request(response.urljoin(link_next))
