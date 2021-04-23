import scrapy


class ArabaSpider(scrapy.Spider):
    name = 'araba'
    allowed_domains = ['arabam.com/ikinci-el/otomobil/bmw']
    start_urls = ['https://www.arabam.com/ikinci-el/otomobil/bmw']

    def parse(self, response):
        hrefbmw = response.css("h3.crop-after a ::attr(href)").extract()
        
        for href in hrefbmw:
            url = response.urljoin(href)
            print("--------------------------------------------------------------------------")
            print(url)
            yield scrapy.Request(url, callback=self.parse_page)

            next_page = response.css("#pagingNext ::attr(href)").extract()
            print(next_page)

            if next_page:
                url = response.urljoin(next_page[0])
                yield scrapy.Request(url)

    def parse_page(self, response):
        model = response.xpath("/html[1]/body[1]/div[2]/div[6]/div[3]/div[1]/div[1]/p[1]").get()
        print("######################################################################################")
        print(model)

