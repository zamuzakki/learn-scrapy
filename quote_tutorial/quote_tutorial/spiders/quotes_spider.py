import scrapy
from scrapy.http import FormRequest
from ..items import QuoteTutorialItem

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/login'
    ]
    # start_urls = 'http://quotes.toscrape.com/'

    def parse(self, response):
        token = response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(response,formdata={
            'csrf_token': token,
            'username': 'age.zakki@gmail.com',
            'password': 'helloworld'
        }, callback=self.scrape_items)

    def scrape_items(self, response):
        items = QuoteTutorialItem()
        quotes = response.css('div.quote')

        next_page = response.css('li.next a')

        for quote in quotes:
            title = quote.css('span.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tags = quote.css('a.tag::text').extract()
            page = response.request.url[-2:-1] if response.request.url[-2:-1].isdigit() else 1

            items['title'] = title[1:-1]
            items['author'] = author
            items['tags'] = tags
            items['page'] = page

            yield items

        for next in next_page:
            yield response.follow(next, self.scrape_items)