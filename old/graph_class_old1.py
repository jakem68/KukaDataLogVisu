"""
Demonstrates some customized mouse interaction by drawing a crosshair that follows
the mouse.


"""
import sys
import random
import numpy as np
import pyqtgraph
from pyqtgraph.Qt import QtGui, QtCore

class Graphwindow(QtGui.QDialog):

    #constructor
    def __init__(self):
        # super().__init__() #call super class constructor
        self._pg = pyqtgraph
        self._win = self._pg.GraphicsWindow()
        self._win.setWindowTitle("Graph Window") #set window title
        self._label = self._pg.LabelItem(justify='right')
        self._win.addItem(self._label)
        self._p1 = self._win.addPlot(row=1, col=0)
        self._p2 = self._win.addPlot(row=2, col=0)
        self.data_list = []

        self.region = self._pg.LinearRegionItem()
        self.region.setZValue(10)
        # Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
        # item when doing auto-range calculations.
        self._p2.addItem(self.region, ignoreBounds=True)

        # pg.dbg()
        self._p1.setAutoVisible(y=True)

    def update(self):
        self.region.setZValue(10)
        minX, maxX = self.region.getRegion()
        self._p1.setXRange(minX, maxX, padding=0)

    self.region.sigRegionChanged.connect(update)



    def updateRegion(self, window, viewRange):
        rgn = viewRange[0]
        self.region.setRegion(rgn)

    self._p1.sigRangeChanged.connect(updateRegion)

    self.region.setRegion([1000, 2000])

    # cross hair
    self.vLine = self._pg.InfiniteLine(angle=90, movable=False)
    self.hLine = self._pg.InfiniteLine(angle=0, movable=False)
    self._p1.addItem(self.vLine, ignoreBounds=True)
    self._p1.addItem(self.hLine, ignoreBounds=True)

    self.vb = self._p1.vb

    def mouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self._p1.sceneBoundingRect().contains(pos):
            mouse_point = self.vb.mapSceneToView(pos)
            index = int(mouse_point.x())
            if index > 0 and index < len(self.data_list[0]):
                nr_plots = len(self.data_list)
                stparam = "<span style='font-size: 12pt'>x={:10.2f}".format(mouse_point.x())
                color = ['', 'red', 'green', 'blue', 'yellow']
                j = 1
                for i in range(nr_plots):
                    if j > 4:
                        j = 1
                    my_color = color[j]
                    stparam += ",   <span style='color: {}'>y{}={:10.2f}</span>".format(my_color, i + 1, self.data_list[i][index])
                    j += 1
                self._label.setText(stparam)
            self.vLine.setPos(mouse_point.x())
            self.hLine.setPos(mouse_point.y())


    self.proxy = self._pg.SignalProxy(self._p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
    # p1.scene().sigMouseMoved.connect(mouseMoved)

    def plot_data(self):
        pen = ['r', 'g', 'b', 'y']
        j = 0
        for i in range (len(self.data_list)):
            if j > 3:
                j = 0
            myPen = pen[j]
            j += 1
            # myPen = pencolor()
            self._p1.plot(self.data_list[i], pen=myPen)
            self._p2.plot(self.data_list[i], pen=myPen)#, fillLevel=-0.3, brush=(191, 63, 191,50))

        # create_data()
        # plot_data()

# data1 = datalist[0]
# data2 = datalist[1]

def pencolor():
    r = random.random() * 255
    g = random.random() * 255
    b = random.random() * 255
    pencolor = (r, g, b)
    return pencolor

# datalist = []
# def create_data():
#     start = 10000
#     for i in range(4):
#         # print("num index = {}".format(i))
#         data = start + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
#         datalist.append(data)
#         start += 2500
#     print(len(datalist))




## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
