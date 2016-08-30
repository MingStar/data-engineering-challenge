# data-engineering-challenge
a coding solution for Data Engineering roles


## Approach
* Use Scrapy to do first initial investigations, decide which attributes to pull
    * article text
    * author
    * headline
    * url
    * etc..
* Use Readability to cleanse the text
* Use ElasticSearch to do the searching (with Stemming)

## Framework and Dependencies
* Python 3.x
* [Scrapy](http://scrapy.org/)
* [python-readability](https://github.com/buriy/python-readability)
* [PyMongo](https://api.mongodb.com/python/current/)

## Installation
```
pip3 install scrapy readability-lxml pymongo
```

### Design Decisions:
* The processing is split into 3 steps:
    1. Crawl using Scrapy, save it into CSV
    1. Cleanse the data using Readability, and load it into Compose.io
    1. ElasticSearch API is put on top of Compose


### Log
* 27/Aug crawled 2,700 articles from the Guardian from my DigitalOcean server
* 30/Aug cleansed the text with Readability and load the cleansed text and other meta data into compose.io
*