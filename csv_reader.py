import os
import csv
from urllib.parse import urlparse
import logging

def load_visited(filename, shorten_url=False):
    visited = set()
    printed = False
    count = 0
    if not os.path.exists(filename):
        logging.warning("No file found: " + filename)
        return visited
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not printed:
                print("First url: " + row['link'])
                printed = True
            path = row['link']
            if shorten_url:
                path = urlparse(path).path
            count += 1
            visited.add(path)
    print("Read {} visited urls, {} unique".format(count, len(visited)))
    return visited