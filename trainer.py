from PIL import Image
import os
import cv2
import numpy as np
import pickle
import face_recognition


def trainermod():
#recognizer = cv2.face.LBPHFaceRecognizer_create()
    im_path = ['UserFaces\\student', 'UserFaces\\faculty']
    im_path_all = []
    for i in im_path:
        for j in os.listdir(i):
            im_path_all.append(i + '\\' + j)


    def getImagesId():
        desig = []
        trainingdata = []



        for path in im_path_all:

            imagepaths_1 = []
            if len(os.listdir(path)) > 0:
                imagepaths_1.append([os.path.join(path, imageid) for imageid in os.listdir(path)])

            imagepaths = []
            for sublist in imagepaths_1:
                for item in sublist:
                    if item not in imagepaths:
                        imagepaths.append(item)


            #print('111',imagepaths)
            desig.append(path.split('\\')[1])

            for imagepath in imagepaths:
                faceimg = Image.open(imagepath)
                npface = np.array(faceimg, 'uint8')
                # faceimgflip = cv2.flip(npface, 0)
                # npfaceflip = np.array(faceimgflip, 'uint8')

                ID = os.path.split(imagepath)[0].split('\\')[2]
                #print(ID, imagepath)
                trainingdata.append([npface, ID])
                # trainingdata.append([npfaceflip, ID])

        return trainingdata, desig


    trainingdata, desig = getImagesId()

    #random.shuffle(trainingdata)

    faces = []
    ids = []

    for feature, label in trainingdata:
        faces.append(feature)
        ids.append(label)

    iddict = {}
    index = 0
    for i in im_path_all:
        comps = i.split('\\')
        iddict[comps[2]] = [index, comps[1]]
        index += 1


    pickle.dump(iddict, open('pickle\\iddict.pkl', 'wb'))
    face_encodings = []

    for i in faces:
        encoding = face_recognition.face_encodings(i)[0]
        face_encodings.append(encoding)

    print('Number of people:', len(face_encodings))
    print(iddict)
    pickle.dump(face_encodings, open("face_encodings.pkl", 'wb'))
    #recognizer.train(faces, np.array(train_ID))
    #recognizer.save('training.yml')
    cv2.destroyAllWindows()
