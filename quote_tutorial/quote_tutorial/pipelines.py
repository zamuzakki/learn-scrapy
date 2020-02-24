# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .database import db, Author, Quote

class QuoteTutorialPipeline(object):
    def __init__(self):
        self.db = db
        self.session = db.Session()
        db.drop_all()
        db.create_all()

    def get_or_create(self, model, **kwargs):
        print(f"GET OR CREATE > Author: {kwargs['name']}")

        session = self.session
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            instance = model(**kwargs)
            self.session.add(instance)
            self.session.commit()
            return instance, True

    def save_item(self, item):
        print(f"Save Item Awal > Page: {item['page']}, Author: {item['author_name']}, {item['content']}")
        kwargs = {
            'name': item['author_name'],
            'born_date': item['author_born_date'],
            'born_location': item['author_born_location'],
            'description': item['author_description']
        }
        author, created = self.get_or_create(Author, **kwargs)
        print(author, created)

        print(item.keys())
        if 'tags' in item.keys():
            quote = Quote(content=item['content'], tags=', '.join(item['tags']), page=item['page'], author=author)
        else:
            quote = Quote(content=item['content'], tags='', page=item['page'], author=author)
        print(f"Save Item Akhir > Page: {item['page']}, Author: {item['author_name']}, {item['content']}")
        self.session.add(quote)
        self.session.commit()
        return quote

    def process_item(self, item, spider):
        self.save_item(item)
        return item
