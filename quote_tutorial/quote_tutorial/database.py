from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Sequence, ForeignKey, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from decouple import config


class Database():
    engine = create_engine(config("DB_ENGINE"))

    def __init__(self):
        self.connection = self.engine.connect()
        self.base = declarative_base()
        self.base.metadata.bind = self.engine
        self.Session = sessionmaker(bind=self.engine)
        # self.cursor = self.connection.cur

    def create_all(self):
        # self.drop_all()
        self.base.metadata.create_all()
        # print('create all table')

    def drop_all(self):
        self.base.metadata.drop_all()
        # print('drop all table')

    def check_table_exist(self,table_name):
        if self.engine.has_table(table_name):
            return True

    def fetch_by_query(self, query):
        fetch_query = self.connection.execute(f"SELECT * FROM {query}")

        for data in fetch_query.fetchall():
            print(data)

db = Database()
Base = db.base

class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, Sequence("author_id_seq"), primary_key=True, nullable=False)
    name = Column(String, nullable=True)
    born_date = Column(Date, nullable=True)
    born_location = Column(String, nullable=True)
    description = Column(Text)
    quotes = relationship("Quote", back_populates="author")

    def __repr__(self):
        return f'<Author> {self.id} - {self.name}'

class Quote(Base):
    __tablename__ = "quote"
    id = Column(Integer, Sequence("quote_id_seq"), primary_key=True, nullable=False)
    content = Column(String, nullable=True)
    author_id = Column(ForeignKey("author.id", ondelete="CASCADE"), nullable=False)
    tags = Column(String, nullable=True)
    page = Column(Integer, nullable=True)
    author = relationship("Author", back_populates="quotes")

    def __repr__(self):
        return f'<Quote> {self.id} - {self.author.name}'