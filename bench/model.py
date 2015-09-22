#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
model.py
model on SQLAlchemy
"""
__author__ = 'Yoshiya Ito <myon53@gmail.com>'
__version__ = '0.0.1'
__date__ = '22 Sep 2015'

from sqlalchemy import Column, Boolean, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    id = Column(String(64), primary_key=True)
    name = Column(String(64))

    def __init__(self, id, name):
        self.id = id or str(uuid4())
        self.name = name or 'hoge'

    def __repr__(self):
        return 'id:{0}, name:{1}'.format(self.id, self.name)

