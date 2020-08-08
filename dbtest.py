import sqlite3
dbname = 'grass.db'

conn=sqlite3.connect(dbname)
c = conn.cursor()

# # executeメソッドでSQL文を実行する
# create_table = 'create table grass (username verchar,filename verchar)'
# c.execute(create_table)

# SQL文に値をセットする場合は，Pythonのformatメソッドなどは使わずに，
# セットしたい場所に?を記述し，executeメソッドの第2引数に?に当てはめる値をタプルで渡す．
sql = 'insert into grass (username, filename) values (?,?)'
namelist = (1, "uma")
c.execute(sql, namelist)

conn.commit()

select_sql = 'select * from grass where username='
username = ('"laminne#8098"')
select_sql = select_sql + username
c.execute(select_sql)
result=c.fetchone()

conn.close()

print(result)