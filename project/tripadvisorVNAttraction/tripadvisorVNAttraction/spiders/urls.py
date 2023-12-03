import scrapy
class MySpider(scrapy.Spider):
    name = 'VNAttraction'
    #custom_settings = { 'CONCURRENT_REQUESTS': '1' }
    def start_requests(self):
        for page in range (round(11544/30)+1):
            yield scrapy.Request(f'https://www.tripadvisor.com/Attractions-g293921-Activities-oa{page*30}-Vietnam.html',self.parse)
        #yield scrapy.Request(f'https://www.tripadvisor.com/Attractions-g293921-Activities-oa{60}-Vietnam.html',self.parse)
    def parse(self, response):
        attraction_url= response.xpath("//section//a/@href").getall()
        attraction_url=[i for i in attraction_url if 'Attraction_Review' in i and '#REVIEWS' not in i]
        attraction_url = dict.fromkeys(attraction_url).keys()
        rank=response.xpath("//section//a//span[@name='title']//span/text()").getall()
        rank= [int(i[:-1]) for i in rank]
        name= response.xpath("//section//a//span[@name='title']/div/text()[2]").getall()
        url_rank={'rank':rank,'name':name,'attraction_url':attraction_url}
        url_rank=[dict(zip(url_rank,t)) for t in zip(*url_rank.values())]
        for i in url_rank : yield i

