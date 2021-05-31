def attend():
    import pickle
    import sqlite3

    all_att = pickle.load(open('pickle\\all_att.pkl', 'rb'))

    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    distatt = pickle.load(open('pickle\\distatt.pkl', 'rb'))
    # print(distatt)
    # distatt = []

    print("UPDATE ATTENDANCE")
    print('Registration No.\tDesignation\t\t\tIn-Time\t\t\t\tClass No.\n', '_' * 130)

    ########### FACULTY #####################################
    for att in list(all_att):
        print(att)
        try:
            if list(att[1].values()) != []:
                if [list(att[1])[0], att[4]] not in distatt:
                    distatt.append([list(att[1])[0], att[4]])
                    print(list(att[1])[0], '\t\tfaculty\t\t\t', list(att[1].values())[0][1], '\t\t', att[4])
                    c.execute("INSERT into base_attendance VALUES( '', ?, ?, ? )",
                              (list(att[1])[0], list(att[1].values())[0][1], att[4]))

            ############## STUDENT ##################################
            for i in att[0].items():
                if i[1][0] == 'student':
                    regno = i[0]
                    desig = i[1][0]
                    intime = i[1][1]
                    if [regno, att[4]] not in distatt:
                        distatt.append([regno, att[4]])
                        print(regno, '\t\t', desig, '\t\t', intime, '\t\t', att[4])
                        c.execute("INSERT into base_attendance VALUES( ?, '', ?, ? )", (regno, intime, att[4]))
        except:
            print('Error in :', att)

    pickle.dump(distatt, open('pickle\\distatt.pkl', 'wb'))
    # print(distatt)
    conn.commit()
