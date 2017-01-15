
import sys
# from PyQt4 import QtGui
from pyqtgraph.Qt import QtGui, QtCore

class FileSelector(QtGui.QFileDialog):
    #this class creates a dialog window to select files

    #constructor
    def __init__(self):
        super().__init__() #call super class constructor
        self.setWindowTitle("Select Files") #set window title

    @staticmethod
    def select():
        # dialog_app = QtGui.QApplication(sys.argv)
        return QtGui.QFileDialog.getOpenFileNames(caption='select files', directory='/home/jan/tmp')


    # def select(self):
    #     dialog_app = QtGui.QApplication(sys.argv)
    #     return QtGui.QFileDialog.getOpenFileNames(caption='select files', directory='/home/jan/tmp')

def main():
    dialog_app = QtGui.QApplication(sys.argv)
    return QtGui.QFileDialog.getOpenFileNames(caption='select files', directory='/home/jan/tmp')

if __name__ == '__main__':
    main()
