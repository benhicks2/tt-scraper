import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from equipment_scraper.spiders.blade_megaspin import BladeSpiderMegaspin
from equipment_scraper.spiders.rubber_megaspin import RubberSpiderMegaspin
from equipment_scraper.spiders.blade_tt11 import BladeSpiderTT11
from equipment_scraper.spiders.rubber_tt11 import RubberSpiderTT11

def run_spider():
    """
    Run the spider based on the command line argument, which should be the equipment type.
    """
    if len(sys.argv) != 2:
        print("Usage: python run_spider.py <equipment_type>")
        return 1
    equipment_type = sys.argv[1]

    process = CrawlerProcess(get_project_settings())
    if equipment_type == 'blade':
        process.crawl(BladeSpiderMegaspin)
        process.crawl(BladeSpiderTT11)
    elif equipment_type == 'rubber':
        process.crawl(RubberSpiderMegaspin)
        process.crawl(RubberSpiderTT11)
    else:
        print(f"Unknown equipment type: {equipment_type}")
        return 1
    process.start()
