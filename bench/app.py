#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
app.py
web server on tornado
"""
__author__ = 'Yoshiya Ito <myon53@gmail.com>'
__version__ = '0.0.1'
__date__ = '22 Sep 2015'

import asyncio
import random
from tornado import web, httpserver
from datetime import datetime
from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.gen import coroutine
from tornado.options import define, options
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import User, Base

define('port', default=8000, help='port number', type=int)


class SyncSQLAlchemy(web.RequestHandler):

    def get(self):
        user = self.query()
        print(user)

    def query(self):
        session = self.application.Session()
        number = random.randrange(10000)
        user = session.query(User).filter_by(id=number).first()
        return user;

class AsyncSQLAlchemy(web.RequestHandler):

    @coroutine
    def get(self):
        user = yield from self.query()
        print(user)

    @asyncio.coroutine
    def query(self):
        context = asyncio.get_event_loop()
        session = self.application.Session()
        number = random.randrange(10000)
        cursor = session.query(User).filter_by(id=number)
        user = yield from context.run_in_executor(None, cursor.first)
        return user;

class SyncBatchSQLAlchemy(web.RequestHandler):

    def get(self):
        self.batch()

    def batch(self):
        session = self.application.Session()
        users = []
        for i in range(0, 10000):
            user = User(id=str(i), name=str(i))
            users.append(user)
        session.add_all(users)
        session.commit()

class Application(web.Application):

    def __init__(self):
        settings = { 'autoreload': True }
        handlers = [
            ('/sync', SyncSQLAlchemy),
            ('/async', AsyncSQLAlchemy),
            ('/syncbatch', SyncBatchSQLAlchemy),
        ]
        url = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'\
            .format('mysql', 'mysql', '52.68.180.154', 3306, 'tutorial')
        engine = create_engine(url, pool_size=500)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.Session = Session
        super().__init__(handlers, **settings)

if __name__ == '__main__':
    AsyncIOMainLoop().install()
    options.parse_command_line()

    application = Application()

    server = httpserver.HTTPServer(application)
    server.listen(options.port)
    asyncio.get_event_loop().run_forever()
