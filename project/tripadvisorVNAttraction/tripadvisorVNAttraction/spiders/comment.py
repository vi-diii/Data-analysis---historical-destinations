import scrapy
import re
import json
class MySpider(scrapy.Spider):
    name = 'AttractionReviews'
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
        if numpage : 
            numpage=int(numpage.replace(',',''))
            for i in self.parse_en(response) : yield i
            for i in range(1,round(numpage/10)+1):
                yield scrapy.Request(response.url.replace('-Reviews',f'-Reviews-or{i*10}'),self.parse_en)
        else :
            for i in self.parse_en(response) : yield i
    def parse_en(self, response):
        print(response.url)
        if response.xpath("//section[@id='REVIEWS']//div[@class='C' and @data-ft='true']//button[contains(@aria-label,'English')]").getall() :
            
            reviews= response.xpath("//section[@id='REVIEWS']//div[@class='C' and @data-ft='true']/div[@data-automation='reviewCard']").getall()
            reviews=[scrapy.Selector(text=i) for i in reviews]
            if reviews :
                names=[]
                links=[]
                for i in reviews:
                    try :
                        links.append(self.domain_en+i.xpath("//a[@target='_self']/@href").get())
                        names.append(i.xpath("//a[@target='_self']/text()").get())
                    except:
                        names.append(i.xpath("//span/text()").get())
                        links.append('')
                upvotes=[i.xpath("//div[@class='f']//span/span/text()").get() for i in reviews]

                describes=[i.xpath("//a[@target='_self']/../../div/div/span/text()").getall() for i in reviews]
                contributions=[i[-1].replace('contributions','') if len(i)>0 else 0 for i in describes]
                homeplaces=[i[-2] if len(i)>1 else '' for i in describes]

                rates=[]
                for i in reviews:
                    try :
                        rates.append(i.xpath("//svg/@aria-label").get().split(' ')[0])
                    except:
                        rates.append('3.0')
                
                titles=[i.xpath("//a[@target='_blank']/span/text()").get() for i in reviews]

                triptimes=[]
                tripwiths=[]
                contents=[]
                for i in reviews:
                    try :
                        tripinfos=i.xpath("//div[4]/text()").get().split('•')
                        triptimes.append(tripinfos[0] if len(tripinfos)>0 else '')
                        tripwiths.append(tripinfos[1] if len(tripinfos)>1 else '')
                        contents.append(' '.join(i.xpath("//div[5]/div[1]/div/span/text()").getall()).strip())
                    except:
                        triptimes.append('')
                        tripwiths.append('')
                        try:
                            contents.append(' '.join(i.xpath("//div[4]/div[1]/div/span/text()").getall()).strip())
                        except:
                            contents.append('')
                
                writtentimes=[i.xpath("//div[contains(text(),'not of Tripadvisor LLC')]/../div[1]/text()").get() for i in reviews]
                writtentimes=[i.split('Written ')[1] if (i) else '' for i in writtentimes]
                
                commentdict={
                    'weburl':[re.sub("Reviews\-or[0-9]{,}",'Reviews', response.url)]*len(names),
                    'name':names,
                    'link':links,
                    'upvote':upvotes,
                    'contributions':contributions,
                    'homeplace':homeplaces,
                    'rate':rates,
                    'title':titles,
                    'triptime':triptimes,
                    'tripwith':tripwiths,
                    'content':contents,
                    'writtentime':writtentimes,
                    'language':['en']*len(names),
                }
                commentdict=[dict(zip(commentdict,t)) for t in zip(*commentdict.values())]
                for i in commentdict : yield i
    def check_vi(self, response):
        numpage= response.xpath("//section[@id='REVIEWS']//div[@class='Ci']/text()[6]").get()
        if numpage : 
            numpage=int(numpage.replace(',',''))
            for i in self.parse_vi(response) : yield i
            for i in range(1,round(numpage/10)+1):
                yield scrapy.Request(response.url.replace('-Reviews',f'-Reviews-or{i*10}'),self.parse_vi)
        else :
            for i in self.parse_vi(response) : yield i
    def parse_vi(self, response):
        print(response.url)
        if response.xpath("//section[@id='REVIEWS']//div[@class='C' and @data-ft='true']//button[contains(@aria-label,'Tiếng Việt')]").getall() :
            reviews= response.xpath("//section[@id='REVIEWS']//div[@class='C' and @data-ft='true']/div[@data-automation='reviewCard']").getall()
            reviews=[scrapy.Selector(text=i) for i in reviews]

            if reviews :
                names=[]
                links=[]
                for i in reviews:
                    try :
                        links.append(self.domain_en+i.xpath("//a[@target='_self']/@href").get())
                        names.append(i.xpath("//a[@target='_self']/text()").get())
                    except:
                        names.append(i.xpath("//span/text()").get())
                        links.append('')
                upvotes=[i.xpath("//div[@class='f']//span/span/text()").get() for i in reviews]

                describes=[i.xpath("//a[@target='_self']/../../div/div/span/text()").getall() for i in reviews]
                contributions=[i[-1].replace('đóng góp','') if len(i)>0 else 0 for i in describes]
                homeplaces=[i[-2] if len(i)>1 else '' for i in describes]

                titles=[i.xpath("//a[@target='_blank']/span/text()").get() for i in reviews]

                rates=[]
                for i in reviews:
                    try :
                        rates.append(i.xpath("//svg/@aria-label").get().split(' ')[0])
                    except:
                        rates.append('3.0')
                
                titles=[i.xpath("//a[@target='_blank']/span/text()").get() for i in reviews]

                triptimes=[]
                tripwiths=[]
                contents=[]
                for i in reviews:
                    try :
                        tripinfos=i.xpath("//div[4]/text()").get().split('•')
                        triptimes.append(tripinfos[0] if len(tripinfos)>0 else '')
                        tripwiths.append(tripinfos[1] if len(tripinfos)>1 else '')
                        contents.append(' '.join(i.xpath("//div[5]/div[1]/div/span/text()").getall()).strip())
                    except:
                        triptimes.append('')
                        tripwiths.append('')
                        try:
                            contents.append(' '.join(i.xpath("//div[4]/div[1]/div/span/text()").getall()).strip())
                        except:
                            contents.append('')

                writtentimes=[i.xpath("//div[contains(text(),'không phải của Tripadvisor LLC')]/../div[1]/text()").get() for i in reviews]
                writtentimes=[i.split('Đã viết vào ')[1] if (i) else '' for i in writtentimes]
                
                commentdict={
                    'weburl':[re.sub("Reviews\-or[0-9]{,}",'Reviews', response.url).replace(self.domain_vi,self.domain_en)]*len(names),
                    'name':names,
                    'link':links,
                    'upvote':upvotes,
                    'contributions':contributions,
                    'homeplace':homeplaces,
                    'rate':rates,
                    'title':titles,
                    'triptime':triptimes,
                    'tripwith':tripwiths,
                    'content':contents,
                    'writtentime':writtentimes,
                    'language':['vi']*len(names),
                }
                commentdict=[dict(zip(commentdict,t)) for t in zip(*commentdict.values())]
                for i in commentdict : yield i
