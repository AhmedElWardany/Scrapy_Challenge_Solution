import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from ..property import Property


class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(url=start_url,
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(url=area_url,
                          callback=self.parse_area_pages)

    def parse_area_pages(self, response):
        # Write your code here and remove `pass` in the following line

        items = Property()

        title = response.css("h4 a::text").extract()
        price = response.xpath("//div[contains(@class, 'bottom-ic')]/h5/text()").extract()
        url = response.css("h4 a").xpath("@href").extract()
        for i in range(len(url)):
            url[i] = "https://londonrelocation.com"+ url[i]
            price[i] = price[i].replace("£", "")
            title[i] = title[i].replace("\n", "")
            if "pw" in price[i]:
                price[i] = price[i].split("pw")[0]
                price[i] = int(price[i]) * 4
            else:
                price[i] = price[i].split("pcm")[0]
                price[i] = int(price[i])
            items['title'] = title[i]
            items['price'] = price[i]
            items['url'] = url[i]

            yield items

        # an example for adding a property to the json list:
        # property = ItemLoader(item=Property())
        # property.add_value('title', '2 bedroom flat for rental')
        # property.add_value('price', '1680') # 420 per week
        # property.add_value('url', 'https://londonrelocation.com/properties-to-rent/properties/property-london/534465-2-bed-frognal-hampstead-nw3/')
        # return property.load_item()