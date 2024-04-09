import mysql.connector
connection = mysql.connector.connect(user = 'root', database='lesson_3', password = 'R05esbe11@')
#cursor is table
cursor = connection.cursor()
testQuery = ("SELECT * FROM bank_accounts")
cursor.execute(testQuery)#sort all things in cursor

#goes through table
for item in cursor:
    print(item)

addData = ("INSERT INTO bank_accounts(PIN, balance) VALUES(2222, 2)")

cursor.execute(addData)
connection.commit()

for item in cursor:
    print(item)

cursor.close()
connection.close()


'''
INSERT INTO tablename VALUES(values)

SELECT * FROM tablename WHERE ...

TRUNCATE TABLE

cursor.fetchall()
cursor.execute()
cursor.commit()
'''
