import os

from tornado import gen
from tornado.httputil import url_concat
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from tornado import web

import psycopg2
import momoko


class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class TutorialHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        name = 2
        cursor = yield self.db.execute("SELECT pastedata from pste where id=%s;", (name,))
        print str(cursor.fetchone()[0])
        self.render("get.html")

    @gen.coroutine
    def post(self):
        body = str(self.get_body_argument('str'))
        # yield self.db.execute("INSERT INTO pste (pastedata) VALUES (%s);", (body,))
        cur = yield self.db.execute("SELECT id from pste where pastedata=%s", (body,))
        int = cur.fetchone()[0]
        wtf = 'http://localhost:8080/new/%s' % int
        print wtf
        self.redirect(wtf)
        # self.render("get.html")


class New(BaseHandler):

    @gen.coroutine
    def get(self, id):
        print 'Callin New'
        print id

        cur = yield self.db.execute("SELECT pastedata from pste where id=%s", (id,))
        print cur.fetchone()
        # self.redirect("post_data.html")
        self.render("get.html")

    @gen.coroutine
    def post(self, id):
        print 'Callin New'
        print id
        body = '1'
        cur = yield self.db.execute("SELECT pastedata from pste where id=%s", (body,))
        print cur.fetchone()
        # self.redirect("post_data.html")
        self.render("get.html")

settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "template"),
    )

if __name__ == '__main__':
    parse_command_line()
    application = web.Application([
        (r'/new/(.*)', New), (r'/', TutorialHandler,)
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
    http_server.listen(8080, 'localhost')
    ioloop.start()