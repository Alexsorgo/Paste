import momoko


def con():
    db = momoko.Connection(
        dsn='dbname=prod user=sorgo password=123456'
            'host=localhost port=5432'
    )
    db.connect()
    cur = db.execute("select * from tbl_pst;")
    print str(cur.fetchone()[0])
    print cur
    db.close()

con()
