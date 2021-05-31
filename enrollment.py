import cv2
import face_recognition
import numpy as np
import pickle
import os
import shutil

def enroller(category, id):
    #category = int(input('Enter 1 for student, 2 for faculty : '))
    category_path = {1: 'student', 2: 'faculty'}
    #id = input('Enter registration number: ')
    if not os.path.exists('UserFaces\\' + str(category_path[category]) + '\\' + str(id)):
        os.mkdir('UserFaces\\' + str(category_path[category]) + '\\' + str(id))
    else:
        shutil.rmtree('UserFaces\\' + str(category_path[category]) + '\\' + str(id))
        os.mkdir('UserFaces\\' + str(category_path[category]) + '\\' + str(id))

    # url='http://192.168.43.59:8080/video'
    # cap = cv2.VideoCapture(url)

    cap = cv2.VideoCapture(0)
    # face_cascade = cv2.CascadeClassifier('HCTrainingImages\\haarcascade_frontalface_default.xml')
    # eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    facenum = 0

    while True:

        _, img = cap.read()
        k = cv2.waitKey(30) & 0xFF
        if k == ord('q'):
            cv2.imwrite('UserFaces\\' + str(category_path[category]) + '\\' + str(id) + '\\' + str(facenum) + '.jpg',
                        img)
            break
        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        #img = cv2.resize(img, (640, 480))
        #grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #faces = face_cascade.detectMultiScale(grey, 1.3, 5)

        # for (x, y, w, h) in faces:
        #     roi_grey = grey[y:y + h, x:x + w]
        #     facenum += 1
        #     cv2.imwrite('UserFaces\\' + str(category_path[category]) + '\\' + str(id) + '\\' + str(facenum) + '.jpg',
        #                 roi_grey)
        #     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        ##        roi_color = img[y:y+h, x:x+w]
        ##        eyes = eye_cascade.detectMultiScale(roi_grey)
        ##        for (ex, ey, ew, eh) in eyes:
        ##            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)
        face_locations = face_recognition.face_locations(rgb_small_frame, model='cnn')

        for (top, right, bottom, left) in face_locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # Draw a box around the face
            colour_desig = tuple([255 if category == 'student' else 0, 255 if category == 'faculty' else 0, 0])

            cv2.rectangle(img, (left, top), (right, bottom), colour_desig, 2)

            # Draw a label with a name below the face
            cv2.rectangle(img, (left, bottom - 35), (right, bottom), colour_desig, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, id, (left + 6, bottom - 6), font, 1.0, (0, 0, 255), 1)

        cv2.imshow('Press q to take image', img)


    cap.release()
    cv2.destroyAllWindows()
