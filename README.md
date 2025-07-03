# tt-scraper

## Getting Started
### File structure
```
├── client
│   └── ttclient.py
├── requirements.txt
└── server
    ├── equipment_scraper
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   ├── settings.py
    │   └── spiders
    │       ├── blade_megaspin.py
    │       ├── blade_tt11.py
    │       ├── megaspin_spider.py
    │       ├── rubber_megaspin.py
    │       ├── rubber_tt11.py
    │       └── tt11_spider.py
    ├── main.py
    ├── scrapy.cfg
    └── start.sh
```
### Folder information
| Folder            | Description                                                          |
| ----------------- | -------------------------------------------------------------------- |
| client            | Contains the CLI that communicates with the REST API.                |
| server            | The REST API and scraper, built using Flask.                         |
| equipment_scraper | The scraper to scrape table tennis websites. Must be run manually.   |
| spiders           | The spiders that enable the websites to be scraped.                  |

## Using the Tool
### Prerequisites
- Scrapy, Python, and pip are installed.
- MongoDB is installed and started, and contains the following:
    - A database called `ttequipment_db`.
    - 2 collections: `rubbers` and `blades`.

### Scraper
```
scrapy crawl <spider name>
```
Where spider name is one of the following:
- rubber_tt11
- rubber_megaspin
- blade_tt11
- blade_megaspin
This will populate the corresponding collection (rubbers or blades) with the data, or update the existing values.

### Flask server
```
pip install -r requirements.txt
flask --app main.py
```
The `pip` command is only required if those packages have not already been installed.

### Command line interface
```
python ttclient.py <command> <options>
```
Run the following for more detailed information on using the CLI.
```
python ttclient.py -h
```

## Disclaimer
Use at your own risk, creator is not responsible for any misuse of this tool.
