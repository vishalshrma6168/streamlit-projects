# create database

"""
import pymysql
mydb= pymysql.connect(
  host="localhost",
  user="root",
  password="hp22d6168",
  
)
cousor=mydb.cursor()
cousor.execute("create database db4")
mydb.commit()
cousor.close()
mydb.close()
print("database is created successfuly")

"""

# create table
"""
import pymysql
mydb= pymysql.connect(
  host="localhost",
  user="root",
  password="hp22d6168",
  database="db4"
  
)
cousor=mydb.cursor()
cousor.execute("create table student (name varchar(255),rollno int(10),age int(10))")
mydb.commit()
cousor.close()
mydb.close()
print(" create table successfuly")

"""

# insert values

"""


import pymysql
mydb=pymysql.connect(
  host="localhost",
  user="root",
  password="hp22d6168",
  database="db4",
)

c=mydb.cursor()
a="insert into student (name,rollno,age) values(%s,%s,%s)"
b=("anku",1,10)
c.execute(a,b)
mydb.commit()
c.close()
mydb.close()
print("values are added")
"""

# read data

"""
import pymysql
mydb=pymysql.connect(
  host="localhost",
  user="root",
  password="hp22d6168",
  database="db4",
)
c=mydb.cursor()
a="select * from  student"
c.execute(a)
result=c.fetchall()

for row in result:
  print(row)

mydb.commit()
c.close()
mydb.close()
print("read the values")

"""

# update data
"""

import pymysql
mydb=pymysql.connect(
  host="localhost",
  user="root",
  password="hp22d6168",
  database="db4",
)
c=mydb.cursor()
a="update student set rollno=40 where age=10"
c.execute(a)


mydb.commit()
c.close()
mydb.close()
print("update the values")

"""


# delete values

import pymysql
mydb=pymysql.connect(
  host="localhost",
  user="root",
  password="hp22d6168",
  database="db4",
)
c=mydb.cursor()
a="delete from student where age=10"
c.execute(a)


mydb.commit()
c.close()
mydb.close()
print("delete the values")