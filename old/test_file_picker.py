#!/usr/bin/env python
#
# [SNIPPET_NAME: File Picker]
# [SNIPPET_CATEGORIES: PyQt4]
# [SNIPPET_DESCRIPTION: An example file picker]
# [SNIPPET_AUTHOR: Darren Worrall <dw@darrenworrall.co.uk>]
# [SNIPPET_LICENSE: GPL]
# [SNIPPET_DOCS: http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qfiledialog.html]

# example test_file_picker.py.py

import sys
from PyQt4 import QtGui, QtCore

class FilePicker(QtGui.QWidget):
    """
    An example file picker application
    """

    def __init__(self):
        # create GUI
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('File picker')
        # Set the window dimensions
        self.resize(300,75)

        # vertical layout for widgets
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)

        # Create a label which displays the path to our chosen file
        self.lbl = QtGui.QLabel('No file selected')
        self.vbox.addWidget(self.lbl)

        # Create a push button labelled 'choose' and add it to our layout
        btn = QtGui.QPushButton('Choose file', self)
        self.vbox.addWidget(btn)

        # Connect the clicked signal to the get_fname handler
        self.connect(btn, QtCore.SIGNAL('clicked()'), self.select_files)

    def select_files(self):
        """
        Handler called when 'choose file' is clicked
        """
        # When you call getOpenFileName, a file picker dialog is created
        # and if the user selects a file, it's path is returned, and if not
        # (ie, the user cancels the operation) None is returned
        fn_list = QtGui.QFileDialog.getOpenFileNames(self, 'Select files')
        return fn_list
        # if len(fn_list)>0:
            # for fn_index in range(len(fn_list)):
            #     self.lbl.setText(fn_list[fn_index])
            #     sleep(1)
        # else:
        #     self.lbl.setText('No file selected')
def main():
    app = QtGui.QApplication(sys.argv)
    gui = FilePicker()
    gui.show()
    app.exec_()

# If the program is run directly or passed as an argument to the python
# interpreter then create a test_file_picker.py instance and show it
if __name__ == "__main__":
    main()
