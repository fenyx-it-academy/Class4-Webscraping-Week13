import scrapy



class AutoSpider(scrapy.Spider):
    name = 'Auto'
    # allowed_domains = ['arabam.com']
    start_urls = ["https://www.arabam.com/ikinci-el/otomobil"]

    def parse(self, response):
        # extract() metodu ise bize bir liste return eder. get()/getall() ilk buldugu sonucu/hepsini return eder.        

        BMW = response.xpath('//*[@id="js-hook-for-listen-scroll-cta"]/div[1]/ul[2]/li/ul/li[6]/a/@href').get() # BMW
        CITROEN = response.xpath('//*[@id="js-hook-for-listen-scroll-cta"]/div[1]/ul[2]/li/ul/li[11]/a/@href').get()  # citroen
        HONDA = response.xpath('//*[@id="js-hook-for-listen-scroll-cta"]/div[1]/ul[2]/li/ul/li[21]/a/@href').get() # honda

        for href in [BMW,CITROEN,HONDA]:               
            url = response.urljoin(href)                                
            yield scrapy.Request(url, callback=self.parse_page)            

    def parse_page(self,response):          
        liste = response.css('tbody tr')             
        for i in liste:            # .css('td a ::text').getall()
            model=i.css("td:nth-child(2) h3 a ::text").get()  
            if model==None:
                model='undefined'                        
            year=i.css("td:nth-child(4) div a ::text").get() 
            if year==None:
                year=2050
            else:
                year=int(year)
            km=i.css("td:nth-child(5) div a ::text").get()  

            if km:
                km=km.split('.')
                km=''.join(km)
                km=int(km)     
            else:
                km=1000000   
            color=i.css("td:nth-child(6) div a ::text").get()   
            if color==None: 
                color=''          
            price=i.css("td:nth-child(7) div span a ::text").get() 
            if price==None:
                price=1000000
            else:
                price=price.split('.')
                price=''.join(price)
                price=price.split('TL')
                price=''.join(price)
                price=int(price)           

            city=i.css("td:nth-child(9) div div:nth-child(1) a span:nth-child(1) ::text").get()  
            if city==None: 
                city='undefined'                      
            yield {"model":model,"year":year,"km":km,"color":color,"price":price,"city":city}   

        # next butonu xpath i
        next_page = response.xpath("//*[@id='pagingNext']/@href")    

        # eger next sayfasi var ise bu bloga girer. yoksa girmez.      
        if next_page:                                                              
            url = response.urljoin(next_page.get())           
            yield scrapy.Request(url, callback=self.parse_page)
        

