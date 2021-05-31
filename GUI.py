##import enrollment
##import trainer
##import recognizer
##import attendance
##import dbview
import sys
from PyQt5 import QtGui, QtCore, QtWidgets

def runenr(self):
    if __name__ == '__main__':
        import enrollment
##    self.getDets()
##    self.show()
##
##
##def getDets(self):
##    i, okPressed = QtWidgets.QInputDialog.getText(self, "Get Reg. No.", "Reg. No.:")
##
##    if okPressed:
##        print(i)



def runtrn():
    if __name__ == '__main__':
        import trainer


def runrec():
    if __name__ == '__main__':
        import recognizer

def runatt():
    if __name__ == '__main__':
        import attendance


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.resize(500, 330)
window.setWindowTitle('University Attendance')

enr = QtWidgets.QPushButton(window)
enr.setText('Enrollment')
enr.move(200, 0)
enr.clicked.connect(runenr)

trn = QtWidgets.QPushButton(window)
trn.setText('Trainer')
trn.move(200, 100)
trn.clicked.connect(runtrn)


rec = QtWidgets.QPushButton(window)

rec.setText('Recognizer')
rec.move(200, 200)
rec.clicked.connect(runrec)

att = QtWidgets.QPushButton(window)
att.setText('Attendance Update')
att.move(200, 300)
att.clicked.connect(runatt)

window.show()
sys.exit(app.exec_())
