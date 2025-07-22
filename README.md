# tt-scraper

## Getting Started
### Folder structure
```
├── client - CLI tool to communicate with the server.
├── server - Flask REST API server.
│   ├── equipment_scraper - Scrapy project to scrape the websites.
│   │   └── spiders - Scrapy spiders, one for each page.
│   └── routes - API endpoints.
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
    - Python should be 3.12 or newer.
- MongoDB is installed and started, and contains the following:
    - A database called `ttequipment_db`. This default can be changed in the `config.ini` file.
    - 2 collections: `rubbers` and `blades`.

### Flask server
```
pip install -r requirements.txt
flask --app main.py
```

### Command line interface
```
python ttclient.py <command> <options>
```
Run the following for more detailed information on using the CLI.
```
python ttclient.py -h
```
The file `clientconfig.ini` can be modified to change any default settings.

### Scraper
The Flask server provides an endpoint to run the scraper, and can be issued with an `update` command. To run scrapy manually, run:
```
scrapy crawl <spider name>
```
Where spider name is one of the following:
- `rubber_tt11`
- `rubber_megaspin`
- `blade_tt11`
- `blade_megaspin`

This will populate the corresponding collection (rubbers or blades) with the data, or update the existing values.

### Testing
TODO

## Disclaimer
Use at your own risk, creator is not responsible for any misuse of this tool.
