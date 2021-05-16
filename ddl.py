import sqlite3

conn = sqlite3.connect('base.db')
c = conn.cursor()

c.execute(""" CREATE table base_attendance(
                st_regno text,
                fac_regno text,
                intime text,
                c_no int,
                foreign key(st_regno) references student_det(st_regno),
                foreign key(fac_regno) references faculty_det(fac_regno)
                ) """)

c.execute(""" CREATE table student_det(
                st_regno text primary key,
                name text,
                gender character(1),
                address text,
                email text,
                dept text,
                branch text,
                power int
                ) """)

c.execute(""" CREATE table faculty_det(
                fac_regno text primary key,
                name text,
                gender character(1),
                address text,
                email text,
                dept text,
                power int
                ) """)

c.execute(""" CREATE table admin_det(
                ad_regno text primary key,
                name text,
                gender character(1),
                address text,
                email text
                power int
                ) """)
conn.commit()
conn.close()
