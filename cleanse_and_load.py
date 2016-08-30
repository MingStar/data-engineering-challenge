import sys
import datetime
import csv
csv.field_size_limit(sys.maxsize)

import readability
import html2text

h2t = html2text.HTML2Text()
h2t.ignore_images = True
h2t.ignore_links = True

def cleanse(raw_text):
    doc = readability.Document(raw_text)
    return doc.summary(html_partial=True)

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

def transform_record(row):
    row['html_summary'] = cleanse(row['html_raw'])
    row['text_summary'] = h2t.handle(row['html_summary'])
    row['published_time'] = transform_time(row['published_time'])
    row['keywords'] = row['keywords'].split(',')

def load_all(filename, db):
    with open(filename) as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            transform_record(row)
            load(row, ['link', 'section', 'headline',
                       'author', 'keywords', 'published_time',
                       'html_summary', 'text_summary'], db)
            count += 1
            if count % 100 == 0:
                print("{} records loaded".format(count))
        print("Done! {} records loaded in total".format(count))

if __name__ == '__main__':
    import mongo_utils
    db = mongo_utils.get_db()
    load_all(sys.argv[1], db)