import pickle
import sqlite3


def studinclass(regno):

    allstud = []
    conn = sqlite3.connect('base.db')
    c = conn.cursor()

    all_att = pickle.load(open('pickle\\all_att.pkl', 'rb'))

    c.execute("SELECT c_no FROM base_attendance WHERE fac_regno= '{}' ".format(regno))
    print('Select Class no.: ')

    for i in c.fetchall():
        print(i)

    chno = int(input())
    c.execute("SELECT st_regno FROM base_attendance WHERE c_no = {} " .format(chno))

    for i in c.fetchall():
        allstud.append(i)

    return [allstud, chno]


def addregno(regno):
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    
    print('Adding regno')
    [allstud, chno] = studinclass(regno)
    print(allstud)
    addreg = input('Enter regno to be added: ')
    c.execute("INSERT into base_attendance VALUES( ?, '', ?, ? )",(addreg, '', chno))

##    all_att = pickle.load(open('pickle\\all_att.pkl', 'rb'))
##
##    list
    conn.commit()
    

def delregno(regno):
    print('Deleting regno')

    print(studinclass(regno))
