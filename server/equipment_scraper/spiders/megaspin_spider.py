import scrapy

from equipment_scraper.items import EquipmentItem

class MegaspinSpider(scrapy.Spider):
    """
    Spider for scraping equipment data from Megaspin. Can handle any equipment type.
    """
    allowed_domains = ['www.megaspin.net']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_count = 1

    def parse(self, response):
        for equipment_item in response.css('.product-list > .product-card'):
            item = EquipmentItem()
            item['url'] = "https://" + self.allowed_domains[0] + equipment_item.css('.product-name > a::attr(href)').get()
            item['name'] = equipment_item.css('.product-name > a::text').get().strip()
            item['price'] = (equipment_item.css('.product-price > .main_price_usd::text').get().strip() +
                             equipment_item.css('.product-price > .main_price_usd_cents::text').get().strip())
            yield item
