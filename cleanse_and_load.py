import sys
import csv
import ssl
csv.field_size_limit(sys.maxsize)

import datetime
from readability import Document
from pymongo import MongoClient

def cleanse(raw_text):
    doc = Document(raw_text)
    return doc.summary()

def transform_time(str):
    if str == '':
        return ''
    return datetime.datetime.strptime(str, '%Y-%m-%dT%H:%M:%S.000Z')

def load(article, keys, db):
    # if db.news_articles.find({link: article['link']}).limit(1).size() > 0:
    #     return False
    db.news_articles.insert_one({
        k:article[k] for k in keys
    })

def load_all(filename, db):
    with open(filename) as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            row['summary'] = cleanse(row['html_raw'])
            row['published_time'] = transform_time(row['published_time'])
            row['keywords'] = row['keywords'].split(',')
            load(row, ['link', 'section', 'headline',
                       'author', 'keywords', 'published_time',
                       'summary'], db)
            count += 1
            if count % 100 == 0:
                print("{} records loaded".format(count))
        print("Done! {} records loaded in total".format(count))

if __name__ == '__main__':
    import os
    client = MongoClient(os.environ['ISENTIA_COMPOSE_MONGO_CONNECTION'], ssl_cert_reqs=ssl.CERT_NONE)
    db = client.isentia
    print("Database connected")
    load_all(sys.argv[1], db)