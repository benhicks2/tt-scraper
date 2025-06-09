import scrapy

from ttequipment.items import EquipmentItem

class TT11Spider(scrapy.Spider):
    allowed_domains = ['www.tabletennis11.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_count = 1

    async def start(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse, cookies={'currency': 'USD'})

    def parse(self, response):
        for equipment_item in response.css('div.item-wrapper'):
            item = EquipmentItem()
            item['url'] = equipment_item.css('.product-name > a::attr(href)').get()
            item['name'] = equipment_item.css('.product-name > a::text').get().strip()
            item['price'] = equipment_item.css('.price::text').get().strip()
            yield item

        next_page_button = response.css('li > a.next::attr(href)').get()
        if next_page_button:
            # The next page exists, so we want to manually increment the page count
            self.page_count += 1
            # Quit out if we have already scraped 10 pages
            if self.page_count > 10:
                return
            next_page = f'{self.start_urls[0]}?p={self.page_count}'
            yield scrapy.Request(url=next_page, callback=self.parse, cookies={'currency': 'USD'})
