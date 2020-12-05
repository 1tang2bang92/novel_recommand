import pymysql
# dbconfig.py
connect = pymysql.connect(${{secrets.DB_USER}}, charset='utf8')

#커서 생성
cur = connect .cursor()

# sql문 실행
sql = "select * from testTable"
cur.execute(sql)


# DB결과를 모두 가져올 때 사용
rows = cur.fetchall()

# 한번에 다 출력
print(rows)

# 원하는 행만 출력
print(rows[0])

# for문으로 출력
for row in rows:
    print(row)

# 연결 해제
connect .close()