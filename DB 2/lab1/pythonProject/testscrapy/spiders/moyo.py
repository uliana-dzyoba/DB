import scrapy


class MoyoSpider(scrapy.Spider):
    name = 'moyo'
    allowed_domains = ['moyo.ua']
    start_urls = ['https://www.moyo.ua/ua/telecommunication/smart/apple/']

    def parse(self, response):
        for item in response.xpath("(//div[@class='product-tile_inner'])[position()<=20]"):
            yield {
                'price': item.xpath(".//div[@class='product-tile_price-current']//span[@class='product-tile_price-value']/text()").extract_first(),
                'description': item.xpath("normalize-space(.//a[@class='gtm-link-product']/text())").extract_first(),
                'image': item.xpath(".//img[contains(@class, 'first-image')]/@src").extract_first()
            }
