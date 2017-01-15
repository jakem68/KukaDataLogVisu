from PyQt4 import QtGui

app = QtGui.QApplication([])

w = QtGui.QMainWindow()
menu = QtGui.QMenu("menu", w)
ag = QtGui.QActionGroup(w, exclusive=True)

a = ag.addAction(QtGui.QAction('50%', w, checkable=True))
menu.addAction(a)

a = ag.addAction(QtGui.QAction('100%', w, checkable=True))
menu.addAction(a)

a = ag.addAction(QtGui.QAction('200%', w, checkable=True))
menu.addAction(a)

a = ag.addAction(QtGui.QAction('300%', w, checkable=True))
menu.addAction(a)

a = ag.addAction(QtGui.QAction('400%', w, checkable=True))
menu.addAction(a)

w.menuBar().addMenu(menu)
w.show()
app.exec_()
