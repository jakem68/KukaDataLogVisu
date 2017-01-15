"""
Built from pygtgraph demonstration code
Demonstrates some customized mouse interaction by drawing a crosshair that follows
the mouse.

"""
import random
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

class Graphwindow(QtGui.QMainWindow):

    data_list = []
    nr_plots = int
    x_axis = []
    cl_titles_checked = []


    def __init__(self):
        QtGui.QMainWindow.__init__(self) #call super class constructor

        self.pgwin = pg.GraphicsWindow()
        self.setCentralWidget(self.pgwin)
        self.label = pg.LabelItem(justify='right')
        self.pgwin.addItem(self.label)
        # self.p1 = self.pgwin.addPlot(title=self.graph_title(), row=1, col=0)
        self.p1 = self.pgwin.addPlot(row=1, col=0)
        self.p2 = self.pgwin.addPlot(row=2, col=0)
        self.p1.addLegend(size=None, offset=(0,00))
        self.region = pg.LinearRegionItem()
        self.region.setZValue(10)
        # Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
        # item when doing auto-range calculations.
        self.p2.addItem(self.region, ignoreBounds=True)

        self.p1.setAutoVisible(y=True)

        self.region.sigRegionChanged.connect(self.update)
        self.p1.sigRangeChanged.connect(self.updateRegion)
        self.region.setRegion(self.region_init())

        # cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.p1.addItem(self.vLine, ignoreBounds=True)
        self.p1.addItem(self.hLine, ignoreBounds=True)

        self.vb = self.p1.vb

        self.proxy = pg.SignalProxy(self.p1.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        self.plot_data()

    def graph_title (self):
        # y1 = file 1 cartforcex
        graph_title = "<span style='font-size: 12pt'>x=milliseconds"
        color = ['red', 'green', 'blue', 'yellow']
        j = 0
        for i in range(Graphwindow.nr_plots):
            if j > 3:
                j = 0
            my_color = color[j]
            graph_title += ",   <span style='color: {}'>y{}=file{}, column </span>".format(my_color, i+1, i+1)
            j += 1
        return graph_title

    def region_init(self):
        max_x = max(self.x_axis)
        min_x = min(self.x_axis)
        span = max_x - min_x
        r_begin = (span*0.1)+min_x
        r_end = (span*0.3)+min_x
        return [r_begin, r_end]

    def pencolor(self):
        r = random.random() * 255
        g = random.random() * 255
        b = random.random() * 255
        self.pencol = (r, g, b)
        return self.pencol

    def plot_data(self):
        pen = ['r', 'g', 'b', 'y']
        color_counter = 0
        for i in range (len(Graphwindow.data_list)):
            for j in range (len(Graphwindow.data_list[i])):
                if color_counter > 3:
                    color_counter = 0
                my_pen = pen[color_counter]
                color_counter += 1
                # my_pen = self.pencolor()
                if self.data_list[i][j]:
                    self.y_axis = self.data_list[i][j]
                # print(self.x_axis)
                # print(type(self.x_axis[1]))
                # print(self.y_axis)
                # print(type(self.y_axis[1]))

                #build legend text
                    self.my_pl = " = file {}: {}". format(i+1, Graphwindow.cl_titles_checked[i][j])

                    self.p1.plot(self.x_axis, self.y_axis, pen=my_pen, name=self.my_pl)
                    self.p2.plot(self.x_axis, self.y_axis, pen=my_pen)#, fillLevel=-0.3, brush=(191, 63, 191,50))
        self.p2.setLabel('bottom', "X Axis", units='milliseconds')

    def update(self):
        self.region.setZValue(10)
        minX, maxX = self.region.getRegion()
        self.p1.setXRange(minX, maxX, padding=0)

    def updateRegion(self, window, viewRange):
            rgn = viewRange[0]
            self.region.setRegion(rgn)

    def mouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.p1.sceneBoundingRect().contains(pos):
            mouse_point = self.vb.mapSceneToView(pos)
            index = int(mouse_point.x())
            max_x = max(self.x_axis)
            min_x = min(self.x_axis)
            span = max_x - min_x
            new_index = int(index/span*len(self.data_list[0][0]))

            if index > 0 and index < max_x:
                stparam = "<span style='font-size: 12pt'>x={:10.2f}".format(mouse_point.x())
                color = ['red', 'green', 'blue', 'yellow']
                color_counter = 0
                for i in range(len(Graphwindow.data_list)):
                    for j in range (len(Graphwindow.data_list[i])):
                        if color_counter > 3:
                            color_counter = 0
                        my_color = color[color_counter]


                        stparam += ",   <span style='color: {}'>y{}={:10.2f}</span>".format(my_color, i + 1, self.data_list[i][j][new_index])

                        color_counter += 1
                self.label.setText(stparam)
            self.vLine.setPos(mouse_point.x())
            self.hLine.setPos(mouse_point.y())

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
