
import sqlite3
import checkstud


def studcno(regno):
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    
    c.execute("SELECT c_no FROM base_attendance WHERE st1_regno = '{}'".format(regno))
    #print(regno,"was present for the classes: ")
    return printslice(c.fetchall())
    
    
def studinclass(regno, chno):
    allstud = []
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    
    c.execute("SELECT c_no FROM base_attendance WHERE fac1_regno= '{}' ".format(regno))
    #print('Select Class no.: ')

    p = printslice(c.fetchall())

    #chno = int(input())
    c.execute("SELECT st1_regno FROM base_attendance WHERE c_no = {} " .format(chno))

    for i in c.fetchall():
        allstud.append(i)

    return [allstud, chno], p


def addregno(fac_regno, stud_regno, c_no):
    conn = sqlite3.connect('base.db')
    c = conn.cursor()

    [allstud, chno], p = studinclass(fac_regno, c_no)
    print('Students currently in class: ', allstud)
    #addreg = input('Enter regno to be added: ')

    addreg = stud_regno
    if addreg in checkstud.checking():
        if addreg not in [i[0] for i in allstud]:
            print(addreg, allstud)
            print('Adding regno in addregno')
            c.execute("INSERT into base_attendance VALUES( ?, ?, ?, ? )",(addreg, fac_regno, '', chno))
    else:
        print("Registration number not present")
    conn.commit()


def delregno(fac_regno,stud_regno, c_no):
    conn = sqlite3.connect('base.db')
    c = conn.cursor()

    [allstud, chno], p = studinclass(fac_regno, c_no)
    print('Students before deleting: ',allstud)
    #delreg = input('Enter regno to be deleted: ')
    delreg = stud_regno
    if delreg in checkstud.checking():
        print('Deleting regno')
        c.execute("DELETE from base_attendance WHERE st1_regno = ? AND c_no = ? ", (delreg, chno))
    else:
        print("Registration number not present")

    conn.commit()


def printslice(pr):
    p = []
    for i in pr:
        #print(list(i)[0])
        p.append(list(i)[0])
    return p
