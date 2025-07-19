from .megaspin_spider import MegaspinSpider

class RubberSpiderMegaspin(MegaspinSpider):
    """
    Spider for scraping the blades from Megaspin.
    """
    name = 'rubber_megaspin'
    start_urls = ['https://www.megaspin.net/store/default.asp?cid=rubbers&type=All']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
