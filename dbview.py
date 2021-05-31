
import sqlite3

conn = sqlite3.connect('base.db')
c = conn.cursor()

c.execute("SELECT * from base_attendance")
for i in c.fetchall():
    print(i)

##c.execute("delete from base_attendance")
##
##conn.commit()

    
##c.execute("SELECT * from student_det")
##for i in c.fetchall():
##    print(i)
##    
##c.execute("SELECT * from faculty_det")
##for i in c.fetchall():
##    print(i)
##    
##c.execute("SELECT * from admin_det")
##for i in c.fetchall():
##    print(i)
