import cv2
import numpy as np
import pickle
import time
import os

face_cascade = cv2.CascadeClassifier('HCTrainingImages\\haarcascade_frontalface_default.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('training.yml')
iddict = pickle.load(open('pickle\\iddict.pkl','rb'))
font = cv2.FONT_HERSHEY_SIMPLEX

print(iddict)
start_time = time.asctime(time.localtime(time.time()))
cap = cv2.VideoCapture(0)
att_stud = {}
init_faculty = {}

while True:

    _, img = cap.read()
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grey, 1.3, 5)

    for (x,y,w,h) in faces:
        roi_grey = grey[y:y+h, x:x+w]
        pred_id, config = recognizer.predict(roi_grey)
       
        for regno,[id,desig] in iddict.items():
            if id == pred_id:
                pred_regno = regno
                pred_desig = desig

        colour_desig = tuple([255 if pred_desig == 'student' else 0, 255 if pred_desig == 'faculty' else 0,255 if pred_desig == 'admin' else 0])
        cv2.putText(img, str(pred_regno), (x,y), font , 1, colour_desig, 2)
        cv2.putText(img, str(pred_desig), (x,y+h), font , 1, colour_desig, 2)
        #cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        cv2.circle(img, (int(x+w/2),int(y+h/2)), int(h/2), colour_desig, 2)

        if pred_regno not in att_stud and pred_desig == 'student':
            att_stud[pred_regno] = [pred_desig, time.asctime(time.localtime(time.time()))]
            print(pred_regno)

        if pred_regno not in init_faculty and pred_desig == 'faculty':
            init_faculty[pred_regno] = [pred_desig, time.asctime(time.localtime(time.time()))]
            print(pred_regno)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) &0xFF
    if k==27:
        break

cap.release()
cv2.destroyAllWindows()
end_time = time.asctime(time.localtime(time.time()))

all_att = []
c_no = 0
if os.path.exists('pickle\\all_att.pkl'):
    all_att = pickle.load(open('pickle\\all_att.pkl', 'rb'))
try:    
    c_no = all_att[-1][4] + 1
except Exception:
    c_no = 0        
all_att.append([att_stud, init_faculty, start_time, end_time, c_no])
pickle.dump(all_att,open('pickle\\all_att.pkl','wb'))
