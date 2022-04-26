from config import mysql

conn = mysql.connect()
curs = conn.cursor()

sql = "select id, contents from dummy limit 5"

curs.execute(sql)
result = curs.fetchall()
print(result)

conn.close()
