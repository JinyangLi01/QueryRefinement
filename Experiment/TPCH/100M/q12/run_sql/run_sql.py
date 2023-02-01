import pymysql
import json
from decimal import Decimal
import pandas as pd

# Your connection code here...

host_args = {
    "host": "localhost",
    "user": "root",
    "password": "ljy19980228",
    'db': 'tpch100M'
}

sql_connection = pymysql.connect(**host_args)


cursor = sql_connection.cursor()



sql_filename = '../tpch100M-q12.sql'
sql_file = open(sql_filename, 'r')
sql_file_read = sql_file.read()
sql_file.close()

cursor.execute(sql_file_read)
column_names = [i[0] for i in cursor.description]
fetch_result = cursor.fetchall()
df = pd.DataFrame(fetch_result, columns=column_names)

print(df.to_string())
df.to_csv("answer_sql12.csv", sep='|', index=False)

sql_connection.commit()



