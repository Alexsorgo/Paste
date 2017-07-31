# -*- coding: utf-8 -*-
import base64, gzip
import hashlib
from StringIO import StringIO


def enc(data):
    data_decoded = base64.b64decode(unicode(data).translate(dict(zip(map(ord, u'-_'), u'+/'))))
    sio = StringIO(data_decoded)
    gzf = gzip.GzipFile(fileobj=sio)
    guff = gzf.read()
    try:
        return guff.decode('windows-1251')
    except:
        return guff


def decd(data):

    zip_text_file = StringIO()
    zipper = gzip.GzipFile(mode='wb', fileobj=zip_text_file)
    zipper.write(data.encode('windows-1251'))
    zipper.close()
    enc_text = base64.b64encode(zip_text_file.getvalue())
    return enc_text


# dt = 'ðæö'
#
# wa = "".join(["%02x" % ord(c) for c in dt])
#
# inc = hashlib.md5(dt.encode('utf-16le'))
# print inc.hexdigest()
# print "".join(["%02x" % ord(c) for c in '512'])
# 'bdbc2a01e84432496e23200289716ef8'

# m = hashlib.md5()
# m.update('ðæö')
# m.update("ðæö.encode('utf-16le')")
# print m.hexdigest()
