# -*- coding: utf-8 -*-
import os
from compiler.ast import obj

from tornado import gen
from tornado.httputil import url_concat
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from tornado import web

import momoko


def read_unicode(wtf, charset='utf-8'):
    if isinstance(wtf, basestring):
        if not isinstance(wtf, unicode):
            wtf = unicode(obj, charset)
    return wtf


class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class TutorialHandler(BaseHandler):


    @gen.coroutine
    def get(self):
        self.render("get.html")

    @gen.coroutine
    def post(self):
        body = read_unicode(self.get_body_argument('str'))
        print body
        # body = str(self.get_body_argument('str')).encode(encoding='utf-8')
        yield self.db.execute("INSERT INTO pste (pastedata) VALUES (%s);", (body,))
        cur = yield self.db.execute("SELECT id from pste where pastedata=%s", (body,))
        int = cur.fetchone()[0]
        wtf = 'http://192.168.1.116:8080/post/%s' % int
        print wtf
        self.redirect(wtf)
        # self.render("get.html")


class New(BaseHandler):

    @gen.coroutine
    def get(self, id):
        print id
        cur = yield self.db.execute("SELECT pastedata from pste where id=%s", (id,))
        self.render("post_data.html", storm=str(cur.fetchone()[0]), same=id)

    @gen.coroutine
    def post(self, id):
        if self.get_body_argument('edit') == 'edit':
            cur = yield self.db.execute("SELECT pastedata from pste where id=%s", (id,))
            self.render("edit_data.html", storm=str(cur.fetchone()[0]), same=id)
        elif self.get_body_argument('edit') == 'save':
            body = read_unicode(self.get_body_argument('str'))
            yield self.db.execute("Update pste set pastedata =%s where id=%s", (body, id,))
            cur = yield self.db.execute("SELECT pastedata from pste where id=%s", (id,))
            self.render("post_data.html", storm=str(cur.fetchone()[0]), same=id)

settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "template"),
    )

if __name__ == '__main__':
    parse_command_line()
    application = web.Application([
        (r'/post/(.*)', New), (r'/', TutorialHandler,)
    ], debug=True, **settings)

    ioloop = IOLoop.instance()


    application.db = momoko.Pool(
        dsn='dbname=paste user=sorgo password=123456 host=localhost port=5432',
        size=1,
        ioloop=ioloop,
    )

    # this is a one way to run ioloop in sync
    future = application.db.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    future.result()  # raises exception on connection error

    http_server = HTTPServer(application)
    http_server.listen(8080, '192.168.1.116')
    ioloop.start()