import scrapy
import re
import json
class MySpider(scrapy.Spider):
    name = 'countcmts'
    domain_en='https://www.tripadvisor.com'
    domain_vi='https://www.tripadvisor.com.vn'
    url='/Attraction_Review-g293924-d25191362-Reviews-K_Hair_Studio-Hanoi.html'
    #custom_settings = { 'ROBOTSTXT_OBEY': False }
    def start_requests(self):
        with open('./dataset/urls.json') as f:
            url=json.load(f)
        for i in url :
            yield scrapy.Request(f'{self.domain_en}{i["attraction_url"]}',self.check_en)
            yield scrapy.Request(f'{self.domain_vi}{i["attraction_url"]}',self.check_vi)
    def check_en(self, response):
        numpage= response.xpath("//section[@id='REVIEWS']//div[@class='Ci']/text()[6]").get()
        if response.xpath("//section[@id='REVIEWS']//div[@class='C' and @data-ft='true']//button[contains(@aria-label,'English')]").getall() :
            if numpage : 
                numpage=int(numpage.replace(',',''))
                yield {'numpage':numpage}
            else :
                yield {'numpage':5}
    def check_vi(self, response):
        numpage= response.xpath("//section[@id='REVIEWS']//div[@class='Ci']/text()[6]").get()
        if response.xpath("//section[@id='REVIEWS']//div[@class='C' and @data-ft='true']//button[contains(@aria-label,'Tiếng Việt')]").getall() :
            if numpage : 
                numpage=int(numpage.replace(',',''))
                yield {'numpage':numpage}
            else :
                yield {'numpage':5}
    