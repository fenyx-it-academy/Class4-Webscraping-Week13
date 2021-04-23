from typing import Counter
import scrapy
from pymongo import MongoClient

connect=MongoClient('mongodb+srv://emrah:2520@cluster0.f2kvo.mongodb.net/week13?retryWrites=true&w=majority')
db=connect['week13']
collection=db['autos']


class arabamSpider(scrapy.Spider):
    name = "autos"
    


    start_urls = [
        'https://www.arabam.com/ikinci-el/otomobil/bmw?page=1'
    ]

    def parse(self, response):   
        
        price=[] 
        qalite=[]
        auto_model=response.css("td.listing-modelname.pr ::text").extract() 
        info=response.css("td.listing-text.pl8.pr8.tac.pr div.fade-out-content-wrapper  ::text").extract() #other information
        
        while len(info)>0:
            qalite.append(info[0:5])
            del info[0:5]                                                                                              
                
        for i in response.css("div.fade-out-content-wrapper span ::text").getall():
            if i.isalnum() is False:
                price.append(i)
        
        for i in qalite:
            mongodb={"marka":auto_model[0],"price":price[0],"model":i[0],"km":i[1],"color":i[2],"place":i[3:5]}
            collection.insert_one(mongodb)                   #insertt mongo db
            del auto_model[0]
            del price[0]
            del info[0:5]           
     
        next_page= f'https://www.arabam.com/ikinci-el/otomobil/bmw?page=2' 
        
        if next_page is not None:
            
            for i in range(10):                
                next_page= f'https://www.arabam.com/ikinci-el/otomobil/bmw?page={i}'    
                yield scrapy.Request(url = next_page,callback = self.parse)  
                
                       
                 
        elif next_page is not None: 
         
           for i in range(10):            
                next_page= f'https://www.arabam.com/ikinci-el/otomobil/honda?page={i}'
                yield scrapy.Request(url = next_page,callback = self.parse)
                
                
               
        if next_page is not None: 
       
           for i in range(10):            
                next_page= f'https://www.arabam.com/ikinci-el/otomobil/citroen?page={i}'
                yield scrapy.Request(url = next_page,callback = self.parse)
                
  
            
            
        
        
        
        

               
                   
        
    
