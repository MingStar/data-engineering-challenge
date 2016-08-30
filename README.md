# data engineering challenge
a python solution for a Data Engineering role

## To Run the Code

### Framework and Dependencies
* Python 3.x
* [Scrapy](http://scrapy.org/) for crawling
* [python-readability](https://github.com/buriy/python-readability) for producing HTML summary
* [PyMongo](https://api.mongodb.com/python/current/) for connecting to MongoDB
* [html2text](https://pypi.python.org/pypi/html2text) for changing HTML to text for full text search in Mongo
* [CherryPy](http://www.cherrypy.org/) for serving an API

### PIP Installation for Dependencies
```
pip3 install scrapy readability-lxml pymongo html2text cherrypy
```

### Steps to run:

1. crawling:
```
$ ./crawl.sh
```

2. Setup the mongo database

* refer to ```setup_mongo.commands.txt```


NB. for step 3 and 4, the environment variable ```
'ISENTIA_COMPOSE_MONGO_CONNECTION'``` needs to be defined as a MongoDB connection string.

3. cleanse and load data to compose


```
$ python3 cleanse_and_load.py <crawled_data.csv>
```

4. running the API
```
$ python3 api_server.py
```

### API parameters

* ```keywords```: a list of keywords to search from, syntax is the same as [the $search field in Mongo $text query](https://docs.mongodb.com/manual/reference/operator/query/text/#behavior).
* ```article_format```: can be ```html``` or ```text```, default to ```text```.
* ```limit```: the number of articles to return, should not be bigger than 100.


## Approach
* To use Scrapy to do some initial investigations to decide which sections and which attributes to crawl
* To investigate what to use cleanse the text (Readability was suggested)
* To investigate keyword search with stemming and casing (ElasticSearch could be an option)


## Design Decisions:
* Since Mongo 3 supports full text search with stemming and casing, the use of ElasticSearch was unnecessary.
* Only HTML and text summary (using Readability and html2text) was saved in the Mongo DB on compose.io
* The data processing was split into 2 separate steps:
    1. Crawl using Scrapy, save it into a CSV file
    2. Cleanse the data using Readability and html2text, and load it into Compose.io
* Even though Scrapy has a Mongo pipeline, this was not chosen, so that the raw HTML can be scraped and saved on disk
only.
* Decided to host the API on my existing DigitalOcean server, instead of Amazon EC2.

## Log
* 27/Aug crawled 2,335 articles from the Guardian from my DigitalOcean server.
* 30/Aug cleansed the text with Readability and load the cleansed text and other meta data into compose.io.
* 30/Aug Search API implemented and deployed.