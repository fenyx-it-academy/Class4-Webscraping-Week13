import scrapy
import sys
import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import dash_html_components as html
import dash_bootstrap_components as dbc
import psycopg2
import pandas.io.sql as sqlio

# Connection parameters, yours will be different
param_dic = {
    "host"      : "localhost",
    "database"  : "Arabalar",
    "user"      : "postgres",
    "password"  : "pg05330477"
}

def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1) 
    print("Connection successful")
    return conn


class ArabaSpider(scrapy.Spider):
    name = 'araba'
    allowed_domains = ['arabam.com']
    start_urls = ['https://www.arabam.com/ikinci-el/otomobil']

    def parse(self, response):
        self.connection = connect(param_dic)
        cursor = self.connection.cursor()
        cursor.execute("DELETE from cars")
        self.connection.commit()
        cursor.close() 
        models = []
        models.append(response.xpath('//*[@id="js-hook-for-listen-scroll-cta"]/div[1]/ul[2]/li/ul/li[6]/a/@href').extract())
        models.append(response.xpath('//*[@id="js-hook-for-listen-scroll-cta"]/div[1]/ul[2]/li/ul/li[11]/a/@href').extract())
        models.append(response.xpath('//*[@id="js-hook-for-listen-scroll-cta"]/div[1]/ul[2]/li/ul/li[21]/a/@href').extract())

        for model in models:
            for urls in model:
                url=response.urljoin(urls)
                yield scrapy.Request(url, callback=self.sorgu)
    




    def sorgu(self,response):
        liste=response.css('tbody tr')
    
        for li in liste:
            #model  //*[@id="listing17354547"]/td[2]/h3/a
            model=li.css("td:nth-child(2) h3 a ::text").get()
            #yil //*[@id="listing17354547"]/td[4]/div/a
            yil=li.css("td:nth-child(4) div a ::text").get()
            #kilometre //*[@id="listing17354547"]/td[5]/div/a
            kilometre=li.css("td:nth-child(5) div a ::text").get()
            #renk //*[@id="listing17354547"]/td[6]/div/a
            renk=li.css("td:nth-child(6) div a ::text").get()
            #fiyat //*[@id="listing17354547"]/td[7]/div/span/a
            fiyat=li.css("td:nth-child(7) div span a ::text").get()
            #il //*[@id="listing17354547"]/td[9]/div/div[1]/a/span[1]
            il=li.css("td:nth-child(9) div div:nth-child(1) a span:nth-child(1) ::text").get()
             
            self.save_to_db(model,yil,kilometre,renk,fiyat,il)
            
            next_page=response.xpath('//*[@id="pagingNext"]/@href')
            # print(next_page)

            if next_page:
                print("-----------------")
                # print(response.url)

                url=response.urljoin(next_page.get())
                # print(url)
                print("--------------")
                yield scrapy.Request(url, callback=self.sorgu)


    def save_to_db(self, model, yil, kilometre, renk, fiyat, il):
        if model != None:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO cars ( model, yil, kilometre, renk, fiyat, il) VALUES(%s, %s, %s, %s, %s, %s)", ( model, yil, kilometre, renk, fiyat, il))
            self.connection.commit()
            cursor.close()  

