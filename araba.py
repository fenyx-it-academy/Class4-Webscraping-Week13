import scrapy
import psycopg2
from pymongo import MongoClient
import pandas.io.sql as sqlio

class ArabaSpider(scrapy.Spider):
    name ='araba'
    #allowed_domains = ['araba.com']
    start_urls = ['https://www.arabam.com/ikinci-el/otomobil/honda?page=1']


    def parse(self, response):

        hrefs=response.css("div.pr10.fade-out-content-wrapper a ::attr(href)").extract()
        print ("-----------------------------------------------------")
        for href in hrefs:
             url=response.urljoin(href)
             #print (url)
             yield scrapy.Request(url, callback=self.parse_page)

        next_page= response.xpath('//*[@id="pagingNext"]/@href')
        if next_page:
            url=response.urljoin(next_page[0].extract())
            yield scrapy.Request(url,self.parse)


    def parse_page(self, response):

        marka =response.xpath('//*[@id="js-hook-for-observer-detail"]/div[2]/ul/li[3]/span[2]/text()').get()
        model=response.xpath('//*[@id="js-hook-for-observer-detail"]/div[2]/ul/li[5]/span[2]/text()').get()
        fiyat = response.xpath('//*[@id="js-hook-for-observer-detail"]/div[2]/div[1]/div/span/text()').get().split('.')[0]+"000"
        km = response.xpath('//*[@id="js-hook-for-observer-detail"]/div[2]/ul/li[11]/span[2]/text()').get().split(".")[0]+"000"
        il = response.xpath('//*[@id="js-hook-for-observer-detail"]/div[2]/p/text()').get().split(" /")[0]

        yield {"Marka":marka,
                "Model":model,
                "Fiyat":fiyat,
                "Km":km,
                "il":il}

        conn = psycopg2.connect("dbname=class4 user=postgres password=Denizli20")
        cur = conn.cursor()
        cur.execute("INSERT INTO Araba ( Marka, Model, Fiyat, Km,  il) VALUES(%s, %s, %s, %s, %s)", (marka, model, fiyat, km, il))
        cur.close()
        conn.commit()
        conn.close()

        # cluster = MongoClient("mongodb+srv://Mahir:Denizli20@cluster0.pnlce.mongodb.net/test2?retryWrites=true&w=majority")
        # db = cluster["Mahir"]
        # collection = db["test2"]
        # post = {"marka": marka, "model": model, "fiyat": fiyat, "km":km, "il":il}
        # collection.insert_one(post)


