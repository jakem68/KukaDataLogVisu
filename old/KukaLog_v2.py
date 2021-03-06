"""
Demonstrates some customized mouse interaction by drawing a crosshair that follows
the mouse.


"""
import random
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

#generate layout
app = QtGui.QApplication([])
win = pg.GraphicsWindow()
win.setWindowTitle('pyqtgraph example: crosshair')
label = pg.LabelItem(justify='right')
win.addItem(label)
p1 = win.addPlot(row=1, col=0)
p2 = win.addPlot(row=2, col=0)

region = pg.LinearRegionItem()
region.setZValue(10)
# Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
# item when doing auto-range calculations.
p2.addItem(region, ignoreBounds=True)

#pg.dbg()
p1.setAutoVisible(y=True)

def pencolor():
    r = random.random() * 255
    g = random.random() * 255
    b = random.random() * 255
    pencolor = (r, g, b)
    return pencolor


#create numpy arrays
#make the numbers large to show that the xrange shows data from 10000 to all the way 0
pen = ['', 'r', 'g', 'b', 'y']
start = 10000
datalist = []
j = 1

for i in range(1,4):
    print("num index = %d" %(i))
    data = start + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
    datalist.append(data)
    start += 2500
    if j > 4:
        j = 1
    myPen = pen[j]
    # myPen = pencolor()
    p1.plot(datalist[i-1], pen=myPen)
    j += 1
    p2.plot(datalist[i-1], pen=myPen)
data1 = datalist[0]
data2 = datalist[1]

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

#cross hair
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
p1.addItem(vLine, ignoreBounds=True)
p1.addItem(hLine, ignoreBounds=True)


vb = p1.vb

def mouseMoved(evt):
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    if p1.sceneBoundingRect().contains(pos):
        mouse_point = vb.mapSceneToView(pos)
        index = int(mouse_point.x())
        if index > 0 and index < len(data1):
            nr_plots = len(datalist)

            # sT_param = "<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>,   <span style='color: blue'>y3=%0.1f</span>" % (mouse_point.x(), datalist[0][index], datalist[1][index], datalist[2][index])

            stparam1 = "\"<span style='font-size: 12pt'>x=%v"
            stparam2 = " % (mouse_point.x()"

            color = ['', 'red', 'green', 'blue', 'yellow']

            j = 1
            for i in range(nr_plots):

                if j > 4:
                    j = 1
                myColor = color[j]

                stparam1 += ",   <span style='color: " + myColor + "'>y" + str(i+1) + "=%v</span>"
                stparam2 += ", datalist[" + str(i) + "][index]"
                j += 1
            stparam1 += "\""
            stparam2 += ")"
            stparam = stparam1 + stparam2
            print(stparam)
            print(nr_plots)

            print(datalist[0][index])
            # input("press enter to continue...")

print("{}. {} appears {} times.".format(i, key, wordBank[key]))



            label.setText("<span style='font-size: 12pt'>x=%v,   <span style='color: red'>y1=%v</span>,   <span style='color: green'>y2=%v</span>,   <span style='color: blue'>y3=%v</span>" % (mouse_point.x(), datalist[0][index], datalist[1][index], datalist[2][index]))

            # label.setText(stparam)



            # label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mouse_point.x(), data1[index], data2[index]))
        vLine.setPos(mouse_point.x())
        hLine.setPos(mouse_point.y())


proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
#p1.scene().sigMouseMoved.connect(mouseMoved)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
