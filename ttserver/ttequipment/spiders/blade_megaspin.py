from .megaspin_spider import MegaspinSpider

class BladeSpiderMegaspin(MegaspinSpider):
    name = 'blade_megaspin'
    start_urls = ['https://www.megaspin.net/store/default.asp?cid=blades&type=All']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
