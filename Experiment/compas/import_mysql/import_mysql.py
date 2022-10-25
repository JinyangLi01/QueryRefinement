import pandas as pd
import mysql.connector
import csv



data_file = r"../../../InputData/Compas/compas-scores.csv"

#
# data_file = r"compas-part.csv"


data = pd.read_csv(data_file, index_col=False)




cnx = mysql.connector.connect(
    user='root',
    password='ljy19980228',
    host='localhost',
    database='Proj2')

cursor = cnx.cursor()

# insert_statement = "INSERT INTO healthcare(id,smoker,county,num_children,race,income,age_group,complications,label) \
#                     VALUES (%d, %d, %s, %d, %s, %d, %s, %d, %d)"

insert_statement = "INSERT INTO compas \
                    VALUES (%s, %s, %s, %s, %s,   %s, %s, %s, %s, %s," \
                    + "   %s, %s, %s, %s, %s,   %s, %s, %s, %s, %s,   "\
                    + "   %s, %s, %s, %s, %s,   %s, %s, %s, %s, %s,   "\
                    + "   %s, %s, %s, %s, %s,   %s, %s, %s, %s, %s,   "\
                    + "%s, %s, %s, %s, %s,      %s, %s)"

for i,row in data.iterrows():
    # sql = "INSERT INTO employee.employee_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(insert_statement, tuple(row))
    # print("Record inserted")
    # the connection is not auto committed by default, so we must commit to save our changes



cnx.commit()
cursor.close()
cnx.close()
print("Done")



#
# drop table healthcare;
# -- id,smoker,county,num_children,race,income,age_group,complications,label
# CREATE TABLE healthcare (
# 	id int primary key,
#     smoker bool,
#     county VARCHAR(10),
#     `num-children` int,
#     race VARCHAR(10),
#     income int,
#     `age-group` VARCHAR(10),
#     complications int,
#     label bool
# );
#



