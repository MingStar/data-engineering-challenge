# data-engineering-challenge
a coding solution for Data Engineering roles


## Framework and Dependencies
* Python 3.x
* [Scrapy](http://scrapy.org/) for crawling
* [python-readability](https://github.com/buriy/python-readability) for producing HTML summary
* [PyMongo](https://api.mongodb.com/python/current/) for connecting to MongoDB
* [html2text](https://pypi.python.org/pypi/html2text) for changing HTML to text for full text search in Mongo

### PIP Installation
```
pip3 install scrapy readability-lxml pymongo
```

## Approach
* Use Scrapy to do initial investigations on the home page, decide which attributes to pull
    * article text
    * author
    * headline
    * url
    * etc..
* Use Readability to cleanse the text


### Design Decisions:
* The processing is split into 3 steps:
    1. Crawl using Scrapy, save it into CSV
    1. Cleanse the data using Readability, and load it into Compose.io
    1. Python API is put on top of Compose
* Even though Scrapy has a Mongo pipeline, this was not chosen so that we could save the raw HTML on local machine
instead of on Compose

### Log
* 27/Aug crawled 2,700 articles from the Guardian from my DigitalOcean server
* 30/Aug cleansed the text with Readability and load the cleansed text and other meta data into compose.io
*