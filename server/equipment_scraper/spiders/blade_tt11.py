from .tt11_spider import TT11Spider

class BladeSpiderTT11(TT11Spider):
    """
    Spider for scraping the blades from Tabletennis11.
    """
    name = 'blade_tt11'
    start_urls = ['https://www.tabletennis11.com/other_eng/blades']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
