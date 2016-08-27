#!/bin/sh

PYTHONPATH=. scrapy runspider crawl.py \
-t csv \
-o data/theguardian.com.csv \
-s USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36" \
-s DOWNLOAD_DELAY=15
