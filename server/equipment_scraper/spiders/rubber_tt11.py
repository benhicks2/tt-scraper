from .tt11_spider import TT11Spider

class RubberSpiderTT11(TT11Spider):
    """
    Spider for scraping the rubbers from Tabletennis11.
    """
    name = 'rubber_tt11'
    start_urls = ['https://www.tabletennis11.com/other_eng/rubbers']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
