"""
Demonstrates some customized mouse interaction by drawing a crosshair that follows
the mouse.


"""
import sys
import random
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

class Graphwindow(QtGui.QMainWindow):

    global datalist

    datalist = []

    global pgwin
    # generate layout
    pgwin = pg.GraphicsWindow()
    pgwin.setCentralWidget(pgwin)
    global label
    label = pg.LabelItem(justify='right')
    pgwin.addItem(label)
    global p1
    global p2
    p1 = pgwin.addPlot(row=1, col=0)
    p2 = pgwin.addPlot(row=2, col=0)

    global region
    region = pg.LinearRegionItem()
    region.setZValue(10)
    # Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
    # item when doing auto-range calculations.
    p2.addItem(region, ignoreBounds=True)

    # pg.dbg()
    p1.setAutoVisible(y=True)

def plot_data(self):
    pen = ['r', 'g', 'b', 'y']
    j = 0
    for i in range (len(datalist)):
        if j > 3:
            j = 0
        myPen = pen[j]
        j += 1
        # myPen = pencolor()
        p1.plot(datalist[i], pen=myPen)
        p2.plot(datalist[i], pen=myPen)#, fillLevel=-0.3, brush=(191, 63, 191,50))

plot_data()

    # data1 = datalist[0]
    # data2 = datalist[1]


def update():
    region.setZValue(10)
    minX, maxX = region.getRegion()
    p1.setXRange(minX, maxX, padding=0)

region.sigRegionChanged.connect(update)


def updateRegion(window, viewRange):
    rgn = viewRange[0]
    region.setRegion(rgn)


p1.sigRangeChanged.connect(updateRegion)

region.setRegion([1000, 2000])

# cross hair
global vLine
global hLine
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
p1.addItem(vLine, ignoreBounds=True)
p1.addItem(hLine, ignoreBounds=True)
global vb
vb = p1.vb


def mouseMoved(evt):
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    if p1.sceneBoundingRect().contains(pos):
        mouse_point = vb.mapSceneToView(pos)
        index = int(mouse_point.x())
        if index > 0 and index < len(datalist[0]):
            nr_plots = len(datalist)
            stparam = "<span style='font-size: 12pt'>x={:10.2f}".format(mouse_point.x())
            color = ['', 'red', 'green', 'blue', 'yellow']
            j = 1
            for i in range(nr_plots):
                if j > 4:
                    j = 1
                my_color = color[j]
                stparam += ",   <span style='color: {}'>y{}={:10.2f}</span>".format(my_color, i + 1, datalist[i][index])
                j += 1
            label.setText(stparam)
        vLine.setPos(mouse_point.x())
        hLine.setPos(mouse_point.y())

proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
# p1.scene().sigMouseMoved.connect(mouseMoved)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
