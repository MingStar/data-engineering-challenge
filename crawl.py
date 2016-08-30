import scrapy
import threading
from visited_link_reader import load_visited

PROJECT_NAME = 'theguardian.com'

SETTINGS = {
    'USER_AGENT': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    'DOWNLOAD_DELAY': 15,
    'FEED_EXPORT_FIELDS': ['link', 'section', 'headline', 'author', 'keywords', 'published_time', 'text_raw', 'html_raw']
}

VISITED_LOCK = threading.Lock()
visited = load_visited('data/{}.csv'.format(PROJECT_NAME), shorten_url=False)


class GuardianSpider(scrapy.Spider):
    name = PROJECT_NAME
    start_urls = ['https://www.theguardian.com/au']
    custom_settings = SETTINGS

    def parse(self, response):
        for href in response.css('.global-navigation__section a::attr(href)').extract():
            full_url = response.urljoin(href)
            yield scrapy.Request(full_url, callback=self.parse_section_page)

    def parse_section_page(self, response):
        global VISITED_LOCK, visited
        for href in response.css('.fc-item__content a::attr(href)').extract():
            with VISITED_LOCK:
                if href in visited:
                    print("!!! {} is already visited! skipped. visited: {}".format(href, len(visited)))
                    continue
                else:
                    visited.add(href)
            full_url = response.urljoin(href)
            yield scrapy.Request(full_url, callback=self.parse_article_page)

    def parse_article_page(self, response):
        text = response.css('.content__article-body').extract_first()
        if not text:
            text = response.css('.content__main').extract_first()
        headline = response.css('.content__headline::text').extract_first()
        if headline:
            headline = headline.strip()
        else:
            headline = response.xpath('//title/text()').extract_first()
        yield {
            'link': response.url,
            'section': response.xpath('//meta[@property="article:section"]/@content').extract_first(),
            'headline': headline,
            'author': response.xpath('//meta[@name="author"]/@content').extract(),
            'keywords': response.xpath('//meta[@name="keywords"]/@content').extract_first(),
            'published_time': response.xpath('//meta[@property="article:published_time"]/@content').extract_first(),
            'text_raw': text,
            'html_raw': response.body
            # response.css('.content__article-body p::text, .content__article-body a::text').extract()
        }
