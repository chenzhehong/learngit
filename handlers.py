# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 12:04:44 2018

@author: chenzhehong
"""
import asyncio

from coroweb import get, post

from models import User, Blog, Comment, next_id

@get('/')
@asyncio.coroutine
def index(request):
    users = yield from User.findAll()
    return {
            '__template__': 'test.html',
            'users': users
        }