# Python Web Scraping Midterm Project

This project is for collecting, processing, and analyzing data scraped from a publicly available website using Python and BeautifulSoup4. 

## Features

- HTTP request handling with error management and rate limiting
- BeautifulSoup4 parsing with multiple selectors
- Object-oriented data modeling
- Data storage in CSV and JSON
- Basic data analysis and transformation

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Project Structure

```
scraper/
  collector.py
  parser.py

models/
  data_models.py

utils/
  file_handler.py
  analyzer.py

data/
  (scraped data files)

main.py
requirements.txt
README.md
```

## Notes

- Follows ethical scraping guidelines and respects robots.txt
- Extendable as a continuous project for future development