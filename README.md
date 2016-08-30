# data engineering challenge
a python solution for a Data Engineering role

## Framework and Dependencies
* Python 3.x
* [Scrapy](http://scrapy.org/) for crawling
* [python-readability](https://github.com/buriy/python-readability) for producing HTML summary
* [PyMongo](https://api.mongodb.com/python/current/) for connecting to MongoDB
* [html2text](https://pypi.python.org/pypi/html2text) for changing HTML to text for full text search in Mongo
* [CherryPy](http://www.cherrypy.org/) for serving an API

### PIP Installation
```
pip3 install scrapy readability-lxml pymongo html2text cherrypy
```

## Approach
* To use Scrapy to do some initial investigations to decide which sections and which attributes to crawl
* To investigate what to use cleanse the text (Readability was suggested)
* To investigate keyword search with stemming and casing, ElasticSearch is known to support those features.


### Design Decisions:
* Since Mongo 3 supports full text search with stemming and casing, the use of ElasticSearch was unnecessary.
* Only HTML and text summary (using Readability and html2text) was saved in the Mongo DB on compose.io
* The processing is split into 3 steps:
    1. Crawl using Scrapy, save it into CSV
    1. Cleanse the data using Readability, and load it into Compose.io
    1. Python API is put on top of Compose
* Even though Scrapy has a Mongo pipeline, this was not chosen the raw HTML can be scraped and saved on disk.
* Decided to host the API on my existing DigitalOcean server, instead of Amazon EC2.

### Log
* 27/Aug crawled 2,335 articles from the Guardian from my DigitalOcean server
* 30/Aug cleansed the text with Readability and load the cleansed text and other meta data into compose.io
*