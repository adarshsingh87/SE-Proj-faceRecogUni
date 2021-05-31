import cv2
import time
import face_recognition
import pickle
import numpy as np

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


def web_recognize(img, known_face_encodings, iddict):
    global face_encodings
    global face_locations
    global face_names
    global process_this_frame
    known_face_names = list(iddict.keys())
    # print(iddict)
    start_time = time.asctime(time.localtime(time.time()))
    # cap = cv2.VideoCapture(0)
    att_stud = {}
    init_faculty = {}

    # while True:

    # _, img = frame.read()
    # grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
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
            #print(best_match_index)
            #print(known_face_names)
            #print(known_face_names)
            #print(best_match_index)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), pred_id in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        if pred_id in known_face_names:
            pred_desig = iddict[pred_id][1]
            pred_regno = pred_id

            # Draw a box around the face
            colour_desig = tuple([255 if pred_desig == 'student' else 0, 255 if pred_desig == 'faculty' else 0, 0])

            cv2.rectangle(img, (left, top), (right, bottom), colour_desig, 2)

            # Draw a label with a name below the face
            cv2.rectangle(img, (left, bottom - 35), (right, bottom), colour_desig, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, pred_id, (left + 6, bottom - 6), font, 1.0, (0, 0, 255), 1)

            #print(pred_regno, pred_desig)

            if pred_regno not in att_stud and pred_desig == 'student':
                att_stud[pred_regno] = [pred_desig, time.asctime(time.localtime(time.time()))]
                ##########print(pred_regno)

            if pred_regno not in init_faculty and pred_desig == 'faculty':
                init_faculty[pred_regno] = [pred_desig, time.asctime(time.localtime(time.time()))]
            #########print(pred_regno)

    return img, att_stud, init_faculty, start_time
