@post('/upload')
@asyncio.coroutine
def get_upload_file(request):
    data = yield from request.post()
    exfile = data['file']
    exfile_fd = exfile.file.read()
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), exfile.filename), 'wb') as f:
        f.write(exfile_fd)
    f.close()
    return web.Response(text='%s successfully stored' % exfile.filename)