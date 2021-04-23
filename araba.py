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
            model=li.css("td:nth-child(2) h3 a ::text").get()
            
            yil=li.css("td:nth-child(4) div a ::text").get()
           
            kilometre=li.css("td:nth-child(5) div a ::text").get()
            
            renk=li.css("td:nth-child(6) div a ::text").get()
            
            fiyat=li.css("td:nth-child(7) div span a ::text").get()
            
            il=li.css("td:nth-child(9) div div:nth-child(1) a span:nth-child(1) ::text").get()
                
            print(model,yil,kilometre,renk,fiyat,il)

