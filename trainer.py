from PIL import Image
import os
import cv2
import numpy as np
import pickle
import random


desig = []
trainingdata = []
recognizer = cv2.face.LBPHFaceRecognizer_create()
im_path = ['UserFaces\\student' , 'UserFaces\\faculty' , 'UserFaces\\admin']
im_path_all = []
for i in im_path:
    for j in os.listdir(i):
        im_path_all.append(i + '\\' + j)
def getImagesId(path):
    imagepaths_1 = []
    for path in im_path_all:
        if len(os.listdir(path))>0:
            imagepaths_1.append([os.path.join(path, imageid) for imageid in os.listdir(path)])

        
        imagepaths = []
        for sublist in imagepaths_1:
            for item in sublist:
                imagepaths.append(item)

##        faces = []
##        ids = []
        
        desig.append(path.split('\\')[1])
        for imagepath in imagepaths:
            faceimg = Image.open(imagepath).convert('L')
            npface = np.array(faceimg,'uint8')
            faceimgflip = cv2.flip(npface, 0)
            npfaceflip = np.array(faceimgflip, 'uint8')
            ID = os.path.split(imagepath)[0].split('\\')[2]
##            faces.append(npface)
##            faces.append(npfaceflip)
##            ids.append(ID)
##            ids.append(ID)
            trainingdata.append([npface, ID])
            trainingdata.append([npfaceflip, ID])
    
    return(trainingdata, desig)

trainingdata, desig = getImagesId(im_path)

random.shuffle(trainingdata)

faces = []
ids = []

for feature, label in trainingdata:
    faces.append(feature)
    ids.append(label)

iddict = {}
index = 0
train_ID = []
for i in im_path_all:
    comps = i.split('\\')
    iddict[comps[2]] = [index, comps[1]]
    index+=1
    #train_ID.append(ind)

#print(dict1)
#print(desig)
#print(len(list(set(ids))))
#iddict = pickle.load(open('pickle\\iddict.pkl','rb'))
#print(os.listdir('UserFaces\\student'))
##for id in ids:
##    if id not in iddict:
##        iddict[id]=[index, desig[index]]
##        index+=1
for id in ids:
    train_ID.append(iddict.get(id)[0])
    #print(iddict.get(id))

#print(train_ID, ids)
print(iddict)
pickle.dump(iddict,open('pickle\\iddict.pkl','wb'))

recognizer.train(faces, np.array(train_ID))
recognizer.save('training.yml')
cv2.destroyAllWindows()
