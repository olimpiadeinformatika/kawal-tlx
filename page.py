from sqlitedict import SqliteDict

with SqliteDict('./db.sqlite', autocommit=True) as d:
    print(d['page'])
