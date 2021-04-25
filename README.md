# Class4-Webscraping-Week14

### 1-Auto isminde Scrapy spider olusturulmalidir.

### 2-"https://www.arabam.com/ikinci-el/otomobil" adresinden BMW,Citroen,Honda araclarinin 
	Model
	Yil
	kilometre 
	renk
	fiyat
	il
bilgileri cekilmelidir,
### 3-Cekilen bilgiler bir database'e kaydedilmelidir.
### 4-Databasedeki araclar yil,sehir,modele gore aranilip siralanabilmelidir
İlk ekranda, verilerin tamami goruntulenmeli ve yillara gore siralanmalidir(Kucukten buyuge).
Diger aramalarda Fiyata gore siralanmalidir.

![alt text](https://github.com/pycoders-nl/Class4-Webscraping-Week14/blob/main/1.jpg)
![alt text](https://github.com/pycoders-nl/Class4-Webscraping-Week14/blob/main/2.jpg)
![alt text](https://github.com/pycoders-nl/Class4-Webscraping-Week14/blob/main/3.jpg)

### Arabam.com_Scrapy_Project
In this project, a dashboard was created using the data obtained from arabam.com. The project consists of 3 parts.

The dataset has been scraped from the arabam.com. (Scrapy)
The cleaned dataset has been uploaded to the database. (PostgreSQL)
The data extracted from the database has been visualized with an interactive dashboard. (Dash, Psycopg2, HTML)
