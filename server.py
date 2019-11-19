# -*- coding: utf-8 -*-
import os
import bert

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from tornado import web

from ipcheck import get_lan_ip


class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class Send(BaseHandler):

    @gen.coroutine
    def get(self):
        self.render('coloms.html', enc='Set your password to hash it', decd='5fa285e1bebe0a6623e33afc04a1fbd5', server='https://192.168.7.9:8943/WMService')

    @gen.coroutine
    def post(self):
            data = self.get_body_arguments('str1')[0]
            body = list(data.replace(',\r\n  ', ', ').split(', '))
            dec = []
            for i in body:
                dec.append(int(i, 0))
            wtf = bert.decode(bytes(dec))
            self.render("coloms.html", enc=data, decd=wtf)


settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "template"),
    )

if __name__ == '__main__':
    parse_command_line()
    application = web.Application([
        (r'/', Send,),
    ], debug=True, **settings)

    http_server = HTTPServer(application)
    ip = get_lan_ip()
    http_server.listen(8081, ip)
    print('server started on ' + str(ip))
    IOLoop.current().start()
