import sqlite3
import exploretrial

def checking():
    conn = sqlite3.connect('base.db')
    c = conn.cursor()

    c.execute("SELECT st1_regno FROM base_attendance")

    l = []
    for i in c.fetchall():
            l.append(list(i)[0])

    return l
