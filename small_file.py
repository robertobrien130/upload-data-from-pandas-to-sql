import time
import pandas as pd
from sqlalchemy import create_engine
import psycopg2



#INPUT YOUR OWN CONNECTION STRING HERE
conn_string = 'postgres://user:password@host/database'

#Import .csv file
df = pd.read_csv('upload_test_data.csv')



#perform to_sql test and print result
db = create_engine(conn_string)
conn = db.connect()

start_time = time.time()
df.to_sql('to_sql_test', con=conn, if_exists='replace', index=False)
print("to_sql duration: {} seconds".format(time.time() - start_time))



#perform COPY test and print result
sql = '''
COPY copy_test
FROM 'PATH_TO_FILE.csv' --input full file path here. see line 46
DELIMITER ',' CSV;
'''

table_create_sql = '''
CREATE TABLE IF NOT EXISTS copy_test (id                bigint,
                                      quantity          int,
                                      cost              double precision,
                                      total_revenue     double precision)
'''

pg_conn = psycopg2.connect(conn_string)
cur = pg_conn.cursor()
cur.execute(table_create_sql)
cur.execute('TRUNCATE TABLE copy_test') #Truncate the table in case you've already run the script before

start_time = time.time()
df.to_csv('upload_test_data_from_copy.csv', index=False, header=False) #Name the .csv file reference in line 29 here
cur.execute(sql)
pg_conn.commit()
cur.close()
print("COPY duration: {} seconds".format(time.time() - start_time))



#close connection
conn.close()