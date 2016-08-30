import os
import pymongo
import ssl

def get_db():
    client = pymongo.MongoClient(os.environ['ISENTIA_COMPOSE_MONGO_CONNECTION'],
                         ssl_cert_reqs=ssl.CERT_NONE)
    print("Database connected")
    return client.isentia

def get_collection():
    return get_db().news_articles