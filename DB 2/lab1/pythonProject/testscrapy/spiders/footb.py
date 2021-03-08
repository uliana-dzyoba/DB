import scrapy


class FootbSpider(scrapy.Spider):
    name = 'footb'
    allowed_domains = ['football.ua']
    start_urls = ['https://football.ua/']
    visited_urls = []

    COUNT_MAX = 20
    count = 0

    def parse(self, response):
        if response.url not in self.visited_urls:
            self.visited_urls.append(response.url)
        item = {
            'url': response.url,
            'text': response.xpath('//body//text()[normalize-space() and not(ancestor::script)]').extract(),
            'image': response.xpath('//img/@src').extract()
        }
        self.count = self.count + 1
        yield item

        if self.count<self.COUNT_MAX:
            print("count")
            print(self.count)
            links = response.xpath('//a[contains(@href, "://football.ua/")]/@href').extract()
            next_page = next((page for page in links if page not in self.visited_urls), None)
            print(next_page)
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
