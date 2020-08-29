import time
from PyQt5.QtWidgets import *
import os, os.path
import sys
import numpy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import operator
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

try:
    from matplotlib.backends.backend_qt4agg import (
        NavigationToolbar2QTAgg as NavigationToolbar,
    )
except ImportError:
    from matplotlib.backends.backend_qt4agg import (
        NavigationToolbar2QT as NavigationToolbar,
    )
from matplotlib.figure import Figure
import numpy.ma as ma
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import pylab

PyCodePath = os.path.split(
    os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
)[0]

wd = os.getcwd()
sys.path.append(os.path.join(PyCodePath, "PythonCompositionPlots"))
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot
from quaternary_FOM_stackedtern2 import *
from quaternary_FOM_stackedtern20 import *
from quaternary_FOM_stackedtern30 import *
from quaternary_FOM_stackedtern9of100 import *
from quaternary_FOM_bintern import *
from quaternary_ternary_faces import ternaryfaces
from quaternary_binary_lines import binarylines

QuaternaryPlotInstance = QuaternaryPlot(None)
TernaryPlotInstance = TernaryPlot(None)


class ternaryfacesWidget(QDialog):
    def __init__(
        self,
        parent,
        comp,
        cols,
        cbaxrect=[0.88, 0.2, 0.04, 0.6],
        ellabels=["A", "B", "C", "D"],
        **kwargs
    ):
        super(ternaryfacesWidget, self).__init__(parent)
        mainlayout = QVBoxLayout()
        self.plotw = plotwidget(self, width=8, height=4)
        self.plotw.fig.clf()
        self.ax = self.plotw.fig.add_axes([0.05, 0.05, 0.78, 0.9])  # add_subplot(111)
        if not cbaxrect is None:
            self.cbax = self.plotw.fig.add_axes(cbaxrect)
        self.tf = ternaryfaces(self.ax, ellabels=ellabels, offset=0.04)
        self.tf.label(fontsize=16)
        mainlayout.addWidget(self.plotw)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        mainlayout.addWidget(self.buttonBox)
        self.setLayout(mainlayout)
        self.tf.scatter(comp, cols, s=20, edgecolors="none", **kwargs)


class binarylinesWidget(QDialog):
    def __init__(self, parent, comp, fom, ellabels=["A", "B", "C", "D"], **kwargs):
        super(binarylinesWidget, self).__init__(parent)
        mainlayout = QVBoxLayout()
        self.plotw = plotwidget(self, width=8, height=4)
        self.plotw.fig.clf()
        self.ax = self.plotw.fig.add_axes([0.3, 0.12, 0.6, 0.83])  # add_subplot(111)
        self.insetax = self.plotw.fig.add_axes([0, 0.7, 0.2, 0.3], projection="3d")
        self.bl = binarylines(self.ax, self.insetax, ellabels=ellabels, offset=0.04)
        mainlayout.addWidget(self.plotw)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        mainlayout.addWidget(self.buttonBox)
        self.setLayout(mainlayout)
        self.bl.plotbinaryfom(comp, fom, **kwargs)
        leg = self.ax.legend(loc=4, bbox_to_anchor=(-0.15, 0.0))
        leg.draggable()


class echem10axesWidget(QDialog):
    def __init__(self, parent=None, ellabels=["A", "B", "C", "D"]):
        super(echem10axesWidget, self).__init__(parent)
        mainlayout = QVBoxLayout()
        self.plotw = plotwidget(self)
        self.plotw.fig.clf()
        self.axl, self.stpl = make10ternaxes(fig=self.plotw.fig, ellabels=ellabels)
        mainlayout.addWidget(self.plotw)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        mainlayout.addWidget(self.buttonBox)
        self.setLayout(mainlayout)

    def plot(self, d, cb=True):
        if "fomlabel" in d.keys():
            cblabel = d["fomlabel"]
        else:
            cblabel = ""
        scatter_10axes(
            d["comps"],
            d["fom"],
            self.stpl,
            s=18,
            edgecolors="none",
            cb=cb,
            cblabel=cblabel,
            cmap=d["cmap"],
            norm=d["norm"],
        )


class echem20axesWidget(QDialog):
    def __init__(self, parent=None, ellabels=["A", "B", "C", "D"]):
        super(echem20axesWidget, self).__init__(parent)
        mainlayout = QVBoxLayout()
        self.plotw = plotwidget(self)
        self.plotw.fig.clf()
        self.axl, self.stpl = make20ternaxes(fig=self.plotw.fig, ellabels=ellabels)
        mainlayout.addWidget(self.plotw)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        mainlayout.addWidget(self.buttonBox)
        self.setLayout(mainlayout)

    def plot(self, d, cb=True):
        if "fomlabel" in d.keys():
            cblabel = d["fomlabel"]
        else:
            cblabel = ""
        scatter_20axes(
            d["comps"],
            d["fom"],
            self.stpl,
            s=18,
            edgecolors="none",
            cb=cb,
            cblabel=cblabel,
            cmap=d["cmap"],
            norm=d["norm"],
        )


class echem30axesWidget(QDialog):
    def __init__(self, parent=None, ellabels=["A", "B", "C", "D"]):
        super(echem30axesWidget, self).__init__(parent)
        mainlayout = QVBoxLayout()
        self.plotw = plotwidget(self)
        self.plotw.fig.clf()
        self.axl, self.stpl = make30ternaxes(fig=self.plotw.fig, ellabels=ellabels)
        mainlayout.addWidget(self.plotw)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        mainlayout.addWidget(self.buttonBox)
        self.setLayout(mainlayout)

    def plot(self, d, cb=True):
        if "fomlabel" in d.keys():
            cblabel = d["fomlabel"]
        else:
            cblabel = ""
        scatter_30axes(
            d["comps"],
            d["fom"],
            self.stpl,
            s=18,
            edgecolors="none",
            cb=cb,
            cblabel=cblabel,
            cmap=d["cmap"],
            norm=d["norm"],
        )


class echem100axesWidget(QDialog):
    def __init__(self, parent=None, ellabels=["A", "B", "C", "D"]):
        super(echem100axesWidget, self).__init__(parent)
        mainlayout = QVBoxLayout()
        self.plotw = plotwidget(self)
        self.plotw.fig.clf()
        self.axl, self.stpl = make9of100ternaxes(fig=self.plotw.fig, ellabels=ellabels)
        mainlayout.addWidget(self.plotw)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        mainlayout.addWidget(self.buttonBox)
        self.setLayout(mainlayout)

    def plot(self, d, cb=True):
        if "fomlabel" in d.keys():
            cblabel = d["fomlabel"]
        else:
            cblabel = ""
        scatter_9of100axes(
            d["comps"],
            d["fom"],
            self.stpl,
            s=20,
            edgecolors="none",
            cb=cb,
            cblabel=cblabel,
            cmap=d["cmap"],
            norm=d["norm"],
        )


class echem4axesWidget(QDialog):
    def __init__(self, parent=None, ellabels=["A", "B", "C", "D"]):
        super(echem4axesWidget, self).__init__(parent)
        mainlayout = QVBoxLayout()
        self.plotw = plotwidget(self)
        self.plotw.fig.clf()
        self.axl, self.stpl = make4ternaxes(fig=self.plotw.fig, ellabels=ellabels)
        mainlayout.addWidget(self.plotw)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        mainlayout.addWidget(self.buttonBox)
        self.setLayout(mainlayout)

    def plot(self, d, cb=True):
        if "fomlabel" in d.keys():
            cblabel = d["fomlabel"]
        else:
            cblabel = ""
        scatter_4axes(
            d["comps"],
            d["fom"],
            self.stpl,
            edgecolors="none",
            cb=cb,
            cblabel=cblabel,
            cmap=d["cmap"],
            norm=d["norm"],
        )


class echembinWidget(QDialog):
    def __init__(self, parent=None, ellabels=["A", "B", "C", "D"]):
        super(echembinWidget, self).__init__(parent)
        mainlayout = QVBoxLayout()
        self.plotw = plotwidget(self)
        self.plotw.fig.clf()
        self.axbin, self.axbininset = plotbinarylines_axandinset(
            fig=self.plotw.fig, ellabels=ellabels
        )
        mainlayout.addWidget(self.plotw)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        mainlayout.addWidget(self.buttonBox)
        self.setLayout(mainlayout)

    def plot(self, d, cb=True, ellabels=["A", "B", "C", "D"]):
        if "fomlabel" in d.keys():
            cblabel = d["fomlabel"]
        else:
            cblabel = ""
        plotbinarylines_quat(
            self.axbin,
            d["comps"],
            d["fom"],
            markersize=10,
            ellabels=d["ellabels"],
            linewidth=2,
        )
        self.axbin.set_xlabel("binary composition", fontsize=16)
        self.axbin.set_ylabel(cblabel, fontsize=16)


class plotwidget(FigureCanvas):
    genericclickonplot = pyqtSignal()

    def __init__(self, parent, width=12, height=6, dpi=72, projection3d=False):
        # plotdata can be 2d array for image plot or list of 2 1d arrays for x-y plot or 2d array for image plot or list of lists of 2 1D arrays
        self.projection3d = projection3d
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        if projection3d:
            self.axes = self.fig.add_subplot(111, navigate=True, projection="3d")
        else:
            self.axes = self.fig.add_subplot(111, navigate=True)
        self.axes.hold(True)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        # self.parent=parent
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # NavigationToolbar(self, parent)
        NavigationToolbar(self, self)
        self.mpl_connect("button_press_event", self.myclick)
        self.clicklist = []
        self.cbax = None

    def redoaxes(self, projection3d=False, onlyifprojectionchanges=True, cbaxkwargs={}):
        if onlyifprojectionchanges and (projection3d == self.projection3d):
            return
        self.fig.clf()
        if projection3d:
            self.axes = self.fig.add_subplot(111, navigate=True, projection="3d")
            self.axes.set_axis_off()
        else:
            self.axes = self.fig.add_subplot(111, navigate=True)
        if not self.cbax is None or len(cbaxkwargs) > 0:
            self.createcbax(**cbaxkwargs)
        self.axes.hold(True)

    def createcbax(self, axrect=[0.88, 0.1, 0.04, 0.8], left=0, rshift=0.01):
        self.fig.subplots_adjust(left=left, right=axrect[0] - rshift)
        self.cbax = self.fig.add_axes(axrect)

    def myclick(self, event):
        if not (event.xdata is None or event.ydata is None):
            arrayxy = [event.xdata, event.ydata]
            print "clicked on image: array indeces ", arrayxy, " using button", event.button
            self.clicklist += [arrayxy]
            self.genericclickonplot.emit(
                [event.xdata, event.ydata, event.button, event.inaxes]
            )
