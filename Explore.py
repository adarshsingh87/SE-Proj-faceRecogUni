import pickle
import cv2
import exploretrial

all_att = pickle.load(open('pickle\\all_att.pkl', 'rb'))

def unlock(authregno):

    cap = cv2.VideoCapture(0)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('training.yml')
    face_cascade = cv2.CascadeClassifier('HCTrainingImages\\haarcascade_frontalface_default.xml')
    font = cv2.FONT_HERSHEY_SIMPLEX

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
                    if pred_regno == authregno:
                        return True
        
        cv2.imshow('img', img)
        k = cv2.waitKey(30) &0xFF
        if k==27:
            break

    cap.release()
    cv2.destroyAllWindows()


def faculty_explore(regno):
    print("Faculty Exploring")
    all_att = pickle.load(open('pickle\\all_att.pkl', 'rb'))

    mot = int(input('0 to view attendance, 1 to add regno, 2 to delete regno'))

    if mot == 0:
        [allstud, chno] = exploretrial.studinclass(regno)
        print(allstud)
    elif mot == 1:
        exploretrial.addregno(regno)
    elif mot == 2:
        exploretrial.delregno(regno)


def stud_explore(regno):
    print("student Exploring")


def admin_explore(regno):
    print("admin Exploring")


iddict = pickle.load(open('pickle\\iddict.pkl','rb'))
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
        if iddict[choice][1] == 'admin':
            admin_explore(choice)
            









