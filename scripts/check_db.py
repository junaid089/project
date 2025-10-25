import sqlite3

db='db.sqlite3'
try:
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'editor_%';")
    rows=cur.fetchall()
    print('found editor tables:', rows)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='editor_generatorjob';")
    exists = bool(cur.fetchone())
    print('editor_generatorjob exists?', exists)
    try:
        cur.execute("SELECT app, name FROM django_migrations WHERE app='editor';")
        print('applied editor migrations:', cur.fetchall())
    except Exception as e:
        print('could not read django_migrations:', e)
except Exception as e:
    print('error connecting to db:', e)
