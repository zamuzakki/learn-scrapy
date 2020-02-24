import scrapy
from scrapy.http import FormRequest, Request
from scrapy.loader import ItemLoader
from ..items import QuoteTutorialItem

class QuoteSpider(scrapy.Spider):
    name = 'quotes'

    start_urls = [
        'http://quotes.toscrape.com/login'
    ]
    # start_urls = 'http://quotes.toscrape.com/'

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        token = response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'username': 'age.zakki@gmail.com',
            'password': 'helloworld'
        }, callback=self.parse_items)

    def parse_items(self, response):
        quotes = response.css('div.quote')

        next_page = response.css('li.next a')

        for quote in quotes:
            self.logger.info('get quote')
            loader = ItemLoader(QuoteTutorialItem(), selector=quote)
            # tags = quote.css('.tag::text').extract()

            try:
                page = response.request.url.split('/')[4]
                page = response.request.url.split('/')[4] if response.request.url.split('/')[4].isdigit() else 1
            except Exception as e:
                page = 1

            loader.add_css('content', '.text::text')
            loader.add_css('tags', '.tag::text')
            loader.add_value('page', page)

            quote_item = loader.load_item()

            author_url = quote.css('.author + a::attr(href)').get()
            self.logger.info('get author page url')
            print(f"{quote_item}")
            yield response.follow(author_url, self.parse_author, meta={'quote_item':quote_item}, dont_filter=True)


        for next in next_page:
            yield response.follow(next, self.parse_items)

    def parse_author(self, response):
        quote_item = response.meta['quote_item']
        loader = ItemLoader(item=quote_item, response=response)

        loader.add_css('author_name', '.author-title::text')
        loader.add_css('author_born_date', '.author-born-date::text')
        loader.add_css('author_born_location', '.author-born-location::text')
        loader.add_css('author_description', '.author-description::text')

        yield loader.load_item()