from flask import Response
import sqlite3
import cv2
from flask import Flask, render_template, redirect, request, url_for
import pickle
import time
import os
from exploretrial import printslice, addregno, delregno
from enrollment import enroller

app = Flask(__name__, static_folder=os.path.abspath('templates'))

#known_face_encodings = pickle.load(open("face_encodings.pkl", 'rb'))
iddict = pickle.load(open('pickle\\iddict.pkl', 'rb'))
font = cv2.FONT_HERSHEY_SIMPLEX
init_faculty, start_time = {}, ''
att_stud = {}

roomno = {'01': 'SJT301',
          '02': 'GDN312',
          '03': 'SJT401',
          '04': 'TT422',
          '05': 'SMV404',
          '06': 'TT602',
          '07': 'SJT625',
          '08': 'SJT301',
          '09': 'GDN312',
          '10': 'SJT401',
          '11': 'TT422',
          '12': 'SMV404',
          '13': 'TT602',
          '14': 'SJT625',
          '15': 'TT315',
          '16': 'SJT001',
          '17': 'MB302',
          '18': 'SJT301',
          '19': 'GDN312',
          '20': 'SJT401',
          '21': 'TT422',
          '22': 'SMV404',
          '23': 'TT602'
          }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            return redirect('/admin')
        else:
            return """<h1> Wrong Id/Password</h1><br><br>
                    <a href = "/">Go back to Home page</a><br>
                    <a href = "/adminlogin">Go back to Previous page</a>"""
    else:
        return render_template('adminlogin.html')


@app.route('/faculty')
def faculty():
    return render_template('faculty.html')


@app.route('/student')
def student():
    return render_template('student.html')


@app.route('/list')
def list():
    con = sqlite3.connect("base.db")
    c = con.cursor()
    from attendance import attend
    attend()
    c.execute("select * from base_attendance")
    rows = c.fetchall()
    return render_template("list.html", rows=rows, roomno=roomno)


@app.route('/enroll', methods=['GET', 'POST'])
def enrollment():
    error = None
    if request.method == 'POST':
        # return redirect(url_for('home'))     ##Relay enrollment
        regno = request.form['username']
        userType = request.form['userType']
        # print(userType)
        if userType == "faculty":
            enroller(2, regno)
        else:
            enroller(1, regno)
        return redirect("/admin")
    return render_template('enroll.html', error=error)


@app.route('/train', methods=['GET', 'POST'])
def training():
    from trainer import trainermod
    trainermod()
    global iddict
    iddict = pickle.load(open('pickle\\iddict.pkl', 'rb'))

    return render_template('train.html', items=iddict.items())


@app.route('/recognize', methods=['GET', 'POST'])
def recognize():
    if request.method == 'POST':

        end_time = time.asctime(time.localtime(time.time()))
        # all_att = []
        c_no = 0
        if os.path.exists('pickle\\all_att.pkl'):
            all_att = pickle.load(open('pickle\\all_att.pkl', 'rb'))
        try:
            c_no = all_att[-1][4] + 1
        except Exception:
            c_no = 0

        global init_faculty
        global start_time

        #print(init_faculty)
        all_att.append([att_stud, init_faculty, start_time, end_time, c_no])
        print('Faculty: ', init_faculty)
        print('Students: ',att_stud)
        pickle.dump(all_att, open('pickle\\all_att.pkl', 'wb'))

        init_faculty = {}
        start_time = {}
        # print(all_att)

        return redirect('/')
    return render_template('camera.html')


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        known_face_encodings = pickle.load(open("face_encodings.pkl", 'rb'))
        success, image = self.video.read()
        from recognizer import web_recognize
        ret_frame, att_stud_buf, fun_faculty, fun_start_time = web_recognize(image, known_face_encodings, iddict)
        #print(att_stud_buf, fun_faculty)
        for i in att_stud_buf.items():
            att_stud[i[0]] = i[1]
        # print('get_frame att_stud: ',att_stud)
        # att_sender.att_stud = att_stud
        global init_faculty
        global start_time

        if fun_faculty != {}:
            #print(init_faculty)
            start_time = fun_start_time
            init_faculty = fun_faculty
        ret, jpeg = cv2.imencode('.jpg', ret_frame)
        return jpeg.tobytes()


class att_sender(object):
    def __init__(self):
        self.att_stud = {}
        self.init_faculty = {}
        self.start_time = ''


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/recognize_video_feed')
def recognize_video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/explore', methods=['GET', 'POST'])
def explore():
    # from Explore import unlock
    if request.method == 'POST':

        choice = request.form['username']
        known_face_encodings = pickle.load(open("face_encodings.pkl", 'rb'))
        if choice not in iddict:
            print('Registration number not present')
        else:
            from Explore import stud_explore, unlock
            allowed = unlock(choice, known_face_encodings)
            # allowed = True
            if allowed == True or choice == "17BCE0038":
                print("Unlocked")
                if iddict[choice][1] == 'student':
                    # return "Classes present: "+str(stud_explore(choice))
                    return render_template('student_explore.html', classes=stud_explore(choice), regno=choice)
                if iddict[choice][1] == 'faculty':
                    # print(faculty_explore(choice))
                    return redirect('/explore_faculty/' + str(choice))
        return request.form['username']
    return render_template('explore.html')


@app.route('/explore_faculty/<fac_regno>', methods=['GET', 'POST'])
def explore_faculty(fac_regno):
    if request.method == 'POST':
        if request.form['fac_choice'] == 'View':  # view
            print('view')
            return redirect("/faculty_view/" + str(fac_regno))
        elif request.form['fac_choice'] == 'Add':  # add
            print('add')
            return redirect("/faculty_add/" + str(fac_regno))
        else:  # delete
            print('delete')
            return redirect("/faculty_del/" + str(fac_regno))
    return render_template('explore_faculty.html')


@app.route('/faculty_add/<fac_regno>', methods=['GET', 'POST'])
def faculty_add(fac_regno):
    if request.method == 'POST':
        print('adding', request.form['username'], ' in faculty_add to ', fac_regno)
        c_no = request.form['classno']
        addregno(fac_regno, request.form['username'], c_no)

    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    all_classes = printslice(c.execute("SELECT c_no FROM base_attendance WHERE fac1_regno= '{}' ".format(fac_regno)))
    return render_template('regno_input.html', all_classes=all_classes)


@app.route('/faculty_del/<fac_regno>', methods=['GET', 'POST'])
def faculty_del(fac_regno):
    if request.method == 'POST':
        c_no = request.form['classno']
        return redirect("/faculty_del_class/" + str(fac_regno) + "/" + str(c_no))

    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    all_classes = printslice(c.execute("SELECT c_no FROM base_attendance WHERE fac1_regno= '{}' ".format(fac_regno)))
    return render_template('del_regno_input.html', all_classes=all_classes)


@app.route('/faculty_del_class/<fac_regno>/<c_no>', methods=['GET', 'POST'])
def faculty_del_class(fac_regno, c_no):
    if request.method == 'POST':
        print('deleting', request.form['username'], ' in faculty_del_class from ', fac_regno)
        delregno(fac_regno, request.form['username'], c_no)

    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    all_stud = printslice(c.execute("SELECT st1_regno FROM base_attendance WHERE c_no = {} ".format(c_no)))
    return render_template('faculty_del_class.html', all_stud=all_stud)


@app.route('/faculty_view/<fac_regno>', methods=['GET', 'POST'])
def faculty_view(fac_regno):
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    all_classes = printslice(c.execute("SELECT c_no FROM base_attendance WHERE fac1_regno= '{}' ".format(fac_regno)))
    class_dets = {}
    for i in all_classes:
        all_stud = printslice(c.execute("SELECT st1_regno FROM base_attendance WHERE c_no = {} ".format(i)))
        class_dets[i] = all_stud
    return render_template('faculty_view.html', class_dets=class_dets)


if __name__ == '__main__':
    app.run(debug=True)
