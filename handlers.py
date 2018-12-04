# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 12:04:44 2018

@author: chenzhehong
"""
import asyncio, time, re, hashlib, json, logging

from coroweb import get, post
from config import configs
from aiohttp import web
from apis import APIValueError, APIResourceNotFoundError, APIError, APIPermissionError, Page

from models import User, Blog, Comment, next_id

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError('Only admin can create a new blog.')

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError:
        pass
    if p < 1:
        p = 1
    return p

def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), \
                filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)

def user2cookie(user, max_age):
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

@asyncio.coroutine
def cookie2user(cookie_str):
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L)!=3:
            return None
        uid, expires, sha1 = L
        user = yield from User.find(uid)
        if user is None:
            return None
        if int(expires) < time.time():
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1!=hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None
    
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

@get('/blog/{id}')
def get_blog(*, id):
    blog = yield from Blog.find(id)
    comments = yield from Comment.findAll(where='blog_id=?', args=[id], orderBy='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
    blog.html_content = text2html(blog.content)
    return {
            '__template__': 'blog.html',
            'blog': blog,
            'comments': comments
        }

@get('/register')
def register():
    return {
            '__template__': 'register.html'
        }
    
@get('/signin')
def signin():
    return {
            '__template__': 'signin.html'
        }
    
@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r

@get('/manage/blogs')
def manage_blogs(*, page='1'):
    return {
            '__template__': 'manage_blogs.html',
            'page_index': get_page_index(page)
        }

@get('/manage/blogs/create')
def manage_create_blog():
    return {
            '__template__': 'manage_blog_edit.html',
            'id': '',
            'action': '/api/blogs'
        }
    
@get('/api/users')
def api_get_users():
    users = yield from User.findAll(orderBy='created_at desc')
    for u in users:
        u.passwd = '******'
    return dict(users=users)

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

@post('/api/users')
def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not email.strip() or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not passwd.strip() or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    users = yield from User.findAll(where='email=?', args=[email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, email=email, name=name, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), \
                image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    logging.info('user info: %s' % (user.name))
    yield from user.save()
    r = web.Response()
    r.content_type = 'application/json;charset=utf-8'
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@get('/api/blogs')
def api_blogs(*, page='1'):
    page_index = get_page_index(page)
    num = yield from Blog.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, blogs=())
    blogs = yield from Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)

@post('/api/authenticate')
def authenticate(*, email, passwd):
    if not email or not email.strip() or not _RE_EMAIL.match(email):
        raise APIValueError('email', 'Invalid email.')
    if not passwd or not passwd.strip() or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd', 'Invalid password.')
    users = yield from User.findAll(where='email=?', args=[email])
    if len(users)==0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd!=sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')
    r = web.Response()
    r.content_type = 'application/json;charset=utf-8'
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@get('/api/blogs/{id}')
def api_get_blog(*, id):
    blog = yield from Blog.find(id)
    return blog

@post('/api/blogs')
def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, 
                name=name.strip(), summary=summary.strip(), content=content.strip())
    yield from blog.save()
    return blog