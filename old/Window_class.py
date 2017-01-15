import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from radio_button_widget_class import *

class TestWindow(QMainWindow):
    #this class creates a main window to test pyqt elements

    #constructor
    def __init__(self):
        super().__init__() #call super class constructor
        self.setWindowTitle("Test Window") #set window title

def main():
    test_program = QApplication(sys.argv) #create new application
    test_window = TestWindow() #create new instance of main window
    test_window.show() # make instance visible
    test_window.raise_() # raise instance to top of window stack
    test_program.exec_() # monitor application for events

if __name__ == '__main__':
    main()
