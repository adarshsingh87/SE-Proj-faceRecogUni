import cv2
import numpy as np
import pickle
import os

category = int(input('Enter 1 for student, 2 for faculty, 3 for admin: '))
category_path = {1:'student' , 2:'faculty' , 3:'admin'}
id = input('Enter register number: ')
os.mkdir('UserFaces\\' + str(category_path[category]) +'\\' + str(id))
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('HCTrainingImages\\haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

facenum = 0

while True:

    _, img = cap.read()
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grey, 1.3, 5)

    for (x,y,w,h) in faces:
        roi_grey = grey[y:y+h, x:x+w]
        facenum += 1
        cv2.imwrite('UserFaces\\' + str(category_path[category]) +'\\' + str(id) + '\\' + str(facenum) + '.jpg', roi_grey)
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
##        roi_color = img[y:y+h, x:x+w]
##        eyes = eye_cascade.detectMultiScale(roi_grey)
##        for (ex, ey, ew, eh) in eyes:
##            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)

    cv2.imshow('img', img)
    if facenum == 100:
        break
    k = cv2.waitKey(30) &0xFF
    if k==27:
           break


cap.release()
cv2.destroyAllWindows()

    

    
