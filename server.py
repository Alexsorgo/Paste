# -*- coding: utf-8 -*-
import codecs
import hashlib
import os
from compiler.ast import obj

import sys

import cx_Oracle as cx_Oracle
import requests
from lxml import etree
from lxml.etree import XMLSyntaxError
from requests.exceptions import ProxyError
from requests.packages import urllib3

from hash import decd, enc

from tornado import gen
from tornado.escape import url_unescape, url_escape
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
        # print self.request
        self.render("get.html")

    @gen.coroutine
    def post(self):
        body = read_unicode(self.get_body_argument('str'))
        if self.get_body_argument('btn') == 'decd':
            try:
                wtf = enc(body)
                self.render("decode_data.html", storm=wtf)
            except (UnicodeEncodeError, TypeError, IOError):
                wtf = 'You must be set invalid data.\n Try again.'
                self.render("error.html", storm=wtf)
        elif self.get_body_argument('btn') == 'enc':
            wtf = decd(body)
            self.render("post_data.html", storm=wtf)
        elif self.get_body_argument('btn') == 'edit':
            try:
                wtf = read_unicode(self.get_body_argument('str'))
                f = open('/Users/admin/PycharmProjects/hash/country_data.xml', 'wb')
                f.write(wtf)
                f.close()
                x = etree.parse("/Users/admin/PycharmProjects/hash/country_data.xml")
                wtf = '<?xml version="1.0" encoding="windows-1251"?>' + etree.tostring(x, pretty_print=True)
                self.render("decode_data.html", storm=wtf)
            except (XMLSyntaxError, UnicodeEncodeError):
                wtf = 'Data wasnt XML.\n Please set XML and try again.'
                self.render("error.html", storm=wtf)


class New(BaseHandler):

    @gen.coroutine
    def get(self):
        self.render("/Users/admin/PycharmProjects/hash/bootstrap/css/bootstrap.min.css")

    @gen.coroutine
    def post(self):
        body = read_unicode(self.get_body_argument('str'))
        wtf = decd(body)
        self.render("post_data.html", storm=wtf)


class Paste(BaseHandler):

    @gen.coroutine
    def get(self):
        self.render("get_paste.html")

    @gen.coroutine
    def post(self):
        body = read_unicode(self.get_body_argument('str'))
        user = self.request.remote_ip
        # body = str(self.get_body_argument('str')).encode(encoding='utf-8')
        yield self.db.execute("INSERT INTO pste (pastedata, ip) VALUES (%s, %s);", (body,user,))
        cur = yield self.db.execute("SELECT id from pste where pastedata=%s", (body,))
        int = cur.fetchall()[-1][0]
        wtf = 'http://192.168.1.116:8080/post/%s' % int
        self.redirect(wtf)
        # self.render("get.html")


class Edit(BaseHandler):

    @gen.coroutine
    def get(self, id):
        user = self.request.remote_ip
        cur = yield self.db.execute("SELECT pastedata, ip from pste where id=%s", (id,))
        if cur.fetchone()[1] == user:
            cur = yield self.db.execute("SELECT pastedata, ip from pste where id=%s", (id,))
            self.render("post_paste.html", storm=str(cur.fetchone()[0]), same=id)
        else:
            cur = yield self.db.execute("SELECT pastedata, ip from pste where id=%s", (id,))
            self.render("post_notedit.html", storm=str(cur.fetchone()[0]), same=id)

    @gen.coroutine
    def post(self, id):
        if self.get_body_argument('edit') == 'edit':
            cur = yield self.db.execute("SELECT pastedata, ip from pste where id=%s", (id,))
            self.render("edit_paste.html", storm=str(cur.fetchone()[0]), same=id)
        elif self.get_body_argument('edit') == 'save':
            body = read_unicode(self.get_body_argument('str'))
            yield self.db.execute("Update pste set pastedata =%s where id=%s", (body, id,))
            cur = yield self.db.execute("SELECT pastedata from pste where id=%s", (id,))
            self.render("post_paste.html", storm=str(cur.fetchone()[0]), same=id)


class md(BaseHandler):

    @gen.coroutine
    def get(self):
        self.render('coloms.html', enc='Set your password to hash it', decd='5fa285e1bebe0a6623e33afc04a1fbd5')

    @gen.coroutine
    def post(self):
        if self.get_body_argument('btn') == 'decd':
            unhash = self.get_body_arguments('str1')
            hash = self.get_body_arguments('str2')[0]

            f = open("/Users/admin/Desktop/Work/rockyou.txt", "r")
            text = f.read()
            f.close()
            for i in text.split('\n'):
                print i
                try:
                    u = i.decode('utf-8')
                    inc = hashlib.md5(u.encode('utf-16LE'))
                except UnicodeDecodeError:
                    pass
                if inc.hexdigest() == hash:
                    self.render("coloms.html", enc=i, decd=hash)
                    break
                else:
                    pass

        elif self.get_body_argument('btn') == 'enc':
            unhash = self.get_body_arguments('str1')[0]
            print unhash
            f = open("/Users/admin/Desktop/Work/rockyou.txt", "a")
            f.write(unhash.encode('utf-8'))
            f.close()

            wa = "".join(["/x%02x" % ord(c) for c in unhash])
            md5 = hashlib.md5()
            md5.update(unhash.encode('utf-16LE'))

            self.render("coloms.html", enc=unhash, decd=md5.hexdigest())


class send(BaseHandler):

    @gen.coroutine
    def get(self):
        self.render('coloms.html', enc='Set your password to hash it', decd='5fa285e1bebe0a6623e33afc04a1fbd5', server='https://192.168.7.9:8943/WMService')

    @gen.coroutine
    def post(self):
            data = self.get_body_arguments('str1')[0]
            dt = decd(data)
            body = """<?xml version="1.0"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"><SOAP-ENV:Body SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><NS1:callService xmlns:NS1="http://ift.webservices.ifobs.cs.com/"><sWebServiceXML xsi:type="xsd:string">%s</sWebServiceXML></NS1:callService></SOAP-ENV:Body></SOAP-ENV:Envelope>""" % dt
            url = "https://192.168.7.9:15143/WMService/services/WMService"
            headers = {'content-type': 'text/xml;charset=utf-8', 'User-Agent': 'ksoap2-android/2.6.0+',
                       'Accept-Encoding': 'gzip', 'Connection': 'close'}
            urllib3.disable_warnings()
            try:
                response = requests.post(url, data=body, headers=headers, verify=False)
                tex = response.text
            except ProxyError:
                tex = 'Please tell me to turn on VPN'
            self.render("coloms.html", enc=data, decd=tex, server=self.get_body_arguments('server')[0])


class sql(BaseHandler):
    user = "IFOBS"
    password="ifobs"
    # dsn="(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=kerberos)(PORT=1521)))(CONNECT_DATA=(SERVER=DEDICATED)(SID=dev)))"
    dsn = "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=10.247.5.121)(PORT=1521)))(CONNECT_DATA=(SERVER=DEDICATED)(SID=IFOBSTEST)))"

    @gen.coroutine
    def get(self):
        print '1'
        self.render('coloms2.html', sql='Set your SQL here', table='Pease set table name')

    @gen.coroutine
    def post(self):
        print self.get_body_arguments('server')
        data = self.get_body_arguments('str')[0]
        table = self.get_body_arguments('str1')[0]
        print data
        conn = cx_Oracle.connect(user=sql.user, password=sql.password, dsn=sql.dsn)
        cursor = conn.cursor()
        cur = cursor.execute(data)
        tex = cur.fetchall()
        print tex
        cur2 = cursor.execute("SELECT column_name FROM USER_TAB_COLUMNS WHERE table_name = :tbl ORDER by column_id", tbl=table)
        tex2 = cur2.fetchall()
        print tex2
        self.render("sql.html", resp=tex, sql=data, header=tex2, table=table, server=self.get_body_arguments('server')[0])



settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
    )

if __name__ == '__main__':
    parse_command_line()
    application = web.Application([
        (r'/bootstrap/css/bootstrap.min.css', New), (r'/', TutorialHandler,), (r'/post/(.*)', Edit), (r'/paste', Paste,), (r'/postman', send), (r'/sql', sql)
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