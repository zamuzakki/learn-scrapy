# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
from datetime import datetime

def remove_quotes(text):
    return text.strip(u'\u201c'u'\u201d')


def convert_date(text):
    return datetime.strptime(text,'%B %d, %Y')

def parse_location(text):
    return text[3:]

def parse_tags(list_tags):
    return ', '.join(list_tags)

class QuoteTutorialItem(Item):
    content = Field(
        input_processor = MapCompose(remove_quotes),
        output_processor = TakeFirst()
    )
    tags = Field()
    page = Field(output_processor = TakeFirst())

    author_name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    author_born_date = Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst()
    )
    author_born_location = Field(
        input_processor=MapCompose(parse_location),
        output_processor=TakeFirst()
    )
    author_description = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )