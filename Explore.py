import pickle
import cv2
import face_recognition
import numpy as np

import exploretrial

all_att = pickle.load(open('pickle\\all_att.pkl', 'rb'))
iddict = pickle.load(open('pickle\\iddict.pkl', 'rb'))


def unlock(authregno, known_face_encodings):
    cap = cv2.VideoCapture(0)
    known_face_names = list(iddict.keys())

    while True:

        _, img = cap.read()
        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame, model='cnn')
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            # print(known_face_names)
            # print(best_match_index)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                if name == authregno:
                    return True

        cv2.imshow('Unlocking...', img)
        k = cv2.waitKey(30) & 0xFF


    cap.release()
    cv2.destroyAllWindows()


def faculty_explore(regno):
    print("Faculty Exploring")
    # all_att = pickle.load(open('pickle\\all_att.pkl', 'rb'))

    mot = int(input('0 to view attendance, 1 to add regno, 2 to delete regno'))

    if mot == 0:
        [allstud, chno] = exploretrial.studinclass(regno)
        print(allstud)
        return allstud
    elif mot == 1:
        exploretrial.addregno(regno)
    elif mot == 2:
        exploretrial.delregno(regno)


def stud_explore(regno):
    print("student Exploring")
    return exploretrial.studcno(regno)


def initial():
    choice = input("Enter Registration No.: ")

    if choice not in iddict:
        print('Registration number not present')
    else:
        allowed = unlock(choice)
        if allowed == True:
            print("Unlocked")

            if iddict[choice][1] == 'student':
                stud_explore(choice)
            if iddict[choice][1] == 'faculty':
                faculty_explore(choice)
