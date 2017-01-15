__author__ = 'Jan Kempeneers'

import sys
from PyQt4 import QtGui

import pyqtgraph as pg

app = QtGui.QApplication(sys.argv)

#
data = [1, 4, 9, 16, 25]   # create new list
#
# print ("here")
# pg.plot(data)   # data can be a list of values or a numpy array
# pg.plot([1,2,3,4], [1,2,3,4], pen="g")
# print ("hello world!")

# import pyqtgraph
#
# pyqtgraph.examples.run()


# import sys
# from PyQt4 import QtGui
# import pyqtgraph as pg
# app = QtGui.QApplication(sys.argv)
pg.plot(x = [0, 1, 2, 3, 4], y = [0, 1, 4, 9, 16])
status = app.exec_()
sys.exit(status)
