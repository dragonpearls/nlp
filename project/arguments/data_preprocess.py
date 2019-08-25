from sqlalchemy import create_engine
from sqlalchemy import orm
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

import sqlalchemy
import sqlite3

import numpy as np
import pandas as pd
import json
from pathlib import Path
import os
import re

import pyltp
from pyltp import SentenceSplitter
from pyltp import Segmentor  
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser

import gensim
from gensim.models import Word2Vec

# data db server info
db_url = {
    'database': 'stu_db',
    'drivername': 'mysql+mysqldb',
    'username': 'root',
    'password': 'AI@2019@ai',
    'host': 'rm-8vbwj6507z6465505ro.mysql.zhangbei.rds.aliyuncs.com',
    'query': {'charset': 'utf8'},
}

# get data by ROM
def User_get_db(url=db_url):
    url = URL(**db_url)
    engine = create_engine(url, echo=True, encoding='utf8')

    Base = declarative_base()
    class News(Base):
        __tablename__ = 'news_chinese'
        
        id = Column(Integer, primary_key=True)
        author = Column(String)
        source = Column(String)    
        content = Column(String)    
        feature = Column(String)   
        title = Column(String)        
        url = Column(String)     
        
        def __repr__(self):
            return "<news_chinese(id='%s', author='%s', title='%s')>" % (self.id, self.author, self.title)

    Session = sessionmaker(bind=engine)
    session = Session()
    news_all = session.query(News).all()
    session.close()   
    return news_all

# get data by pandas query
def pd_query_db(url=db_url):
    url = URL(**db_url)
    engine = create_engine(url, echo=True, encoding='utf8')
    query = 'select * from news_chinese'
    df = pd.read_sql_query(query, engine)
    df.to_csv('news_chinese.csv')
    return df


# clear common useless chars from web
def clear_web_chars(ss, chars=r'\\n|&nbsp|\xa0|\\xa0|\u3000|\\u3000|\\u0020|\u0020'):
    if isinstance(ss, str):
        return re.sub(chars, '', ss) 
    else:
        return ss

# pre-process data
def pre_process(df):
    news_nona = df.dropna()
    news_sorted = news_nona.assign(f = news_nona['content'].str.len()).sort_values('f', ascending = True).drop('f', axis = 1)
    news_big_content = news_sorted[news_sorted['content'].str.len()>=100]
    news_final = news_big_content.applymap(clear_web_chars)
    return news_final

if __name__ == "__main__":
    pass