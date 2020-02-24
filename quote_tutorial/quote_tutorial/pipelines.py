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
        # db.drop_all()
        db.create_all()

    def get_or_create(self, model, session=None, defaults=None, **kwargs):
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
        kwargs = {'name': item['author']}
        author, created = self.get_or_create(Author,**kwargs)

        quote = Quote(title=item['title'], tags=', '.join(item['tags']), page=item['page'], author=author)
        self.session.add(quote)
        self.session.commit()
        return quote

    def process_item(self, item, spider):
        self.save_item(item)
        return item
