import scrapy
import psycopg2
from ..items import CarsItem


class AutoSpider(scrapy.Spider):
    name = 'auto'
    allowed_domains = ['arabam.com']
    start_urls = ['https://www.arabam.com/ikinci-el/otomobil/']

    def start_requests(self):
        yield scrapy.Request('https://www.arabam.com/ikinci-el/otomobil/bmw', self.parse_page)
        yield scrapy.Request('https://www.arabam.com/ikinci-el/otomobil/honda', self.parse_page)
        yield scrapy.Request('https://www.arabam.com/ikinci-el/otomobil/citroen', self.parse_page)
        yield scrapy.Request('https://www.arabam.com/ikinci-el/otomobil/audi', self.parse_page)

    # def parse(self, response):
    #     hrefs = response.css(
    #         "ul.bg-white.category-facet-selection-wrapper > li > ul > li> a ::attr(href)").getall()
    #     for href in hrefs:
    #         url = response.urljoin(href)
    #         # print(url)
    #         yield scrapy.Request(url, self.parse_page)
        # NEXT PAGE
        # next_page = response.css("#pagingNext ::attr(href)")
        # if next_page:
        #     url = response.urljoin(next_page[0].extract())

        # yield scrapy.Request(url, self.parse_page)

    def parse_page(self, response):
        # # NEXT PAGE
        next_page = response.css("#pagingNext ::attr(href)")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse_page)

        models = response.css(
            "td.listing-modelname.pr > h3 > a::text").extract()
        years = response.css(
            "td:nth-child(4) > div > a::text").extract()
        kms = response.css(
            "td:nth-child(5) > div > a::text").extract()
        colors = response.css(
            "td:nth-child(6) > div > a::text").extract()
        prices = response.css(
            "td:nth-child(7) > div > span > a::text").extract()
        cities = response.css(
            "td:nth-child(9) > div > div.fade-out-content-wrapper > a > span:nth-child(1)::text").extract()

        for i in range(0, len(models)):
            # conn = psycopg2.connect("dbname=cars user=postgres password=root")
            # cur = conn.cursor()
            # command = """INSERT INTO autos (model, year, km, color, price, city, id) VALUES (%s, %s, %s, %s, %s, %s)"""
            # cur.execute(
            #     command, (models[i], years[i], kms[i], colors[i], prices[i], cities[i], id[i]))
            # cur.close()
            # conn.commit()
            # conn.close()

            item = CarsItem()
            item['model'] = models[i]
            item['year'] = years[i]
            item['km'] = kms[i].replace(".", "")
            item['color'] = colors[i]
            item['price'] = prices[i].replace(".", "")[:-3]
            item['city'] = cities[i]

            yield item

            # print(type(ids[i]), type(models[i]), type(years[i]), type(kms[i]),
            #       type(colors[i]), type(prices[i]), type(cities[i]))
