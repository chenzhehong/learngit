# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 12:04:44 2018

@author: chenzhehong
"""
import asyncio, time

from coroweb import get, post

from models import User, Blog, Comment, next_id

@get('/')
@asyncio.coroutine
def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time()-7200)
    ]
    return {
            '__template__': 'blogs.html',
            'blogs': blogs
        }