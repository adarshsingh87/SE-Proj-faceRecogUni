import sqlite3

conn = sqlite3.connect('base.db')
c = conn.cursor()


regno = input('Enter regno: ')
name = input('Enter name: ')
gender = input('Enter gender: ')
address = input('Enter address: ')
email = input('Enter email: ')
dept = input('Enter dept: ')
branch = input('Enter branch: ')

c.execute("INSERT into student_det VALUES(?, ?, ?, ?, ?, ?, ?, 1)", (regno, name, gender, address, email, dept, branch))

conn.commit()


