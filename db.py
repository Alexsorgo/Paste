import momoko


def con():
    db = momoko.Connection(
        dsn='dbname=paste user=sorgo password=123456'
            'host=localhost port=5432'
    )
    db.connect()
    cur = db.execute("INSERT INTO tbl_pst VALUES ('wtf');")
    print str(cur.fetchone()[0])
    print cur
    db.close()

con()
