# import time
import os, os.path
import sys
import numpy, copy, itertools
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# import operator
import matplotlib

# from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# try:
#    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
# except ImportError:
#    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
# from matplotlib.figure import Figure
# import numpy.ma as ma
# import matplotlib.colors as colors
# import matplotlib.cm as cm
# import matplotlib.mlab as mlab
# import pylab
# import pickle
# from fcns_math import *
# from fcns_io import *
# from fcns_ui import *
PyCodePath = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
# matplotlib.rcParams['backend.qt4'] = 'PyQt5'
wd = os.getcwd()
sys.path.append(os.path.join(PyCodePath, "PythonCompositionPlots"))
# from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot
from quaternary_FOM_stackedtern2 import *
from quaternary_FOM_stackedtern5 import *
from quaternary_FOM_stackedtern20 import *
from quaternary_FOM_stackedtern30 import *
from quaternary_FOM_stackedtern9of100 import *
from quaternary_ternary_faces import *
from quaternary_faces_shells import *
from quaternary_folded_ternaries import *


class quatcompplotoptions:
    def __init__(
        self,
        plotw,
        combobox,
        plotw3d=None,
        ellabels=["A", "B", "C", "D"],
        plotwcbaxrect=None,
        include3doption=False,
    ):
        self.ellabels = ellabels
        self.plotw = plotw
        self.plotw3d = plotw3d
        self.plotwcbaxrect = plotwcbaxrect
        self.plottypeComboBox = combobox
        self.ternaryfaceoptions = [
            ("layers of\ntern. shells", ternaryfaces_shells),
            ("unfolded\ntern. slices", ternaryfaces_folded),
            ("only tern.\nfaces", ternaryfaces),
        ]
        self.ternaryface_uiinds = [1, 2, 3]
        self.stackedternoptions = [
            ("20% interv\nternaries", (make5ternaxes, scatter_5axes), 0.2),
            ("10% interv\nternaries", (make10ternaxes, scatter_10axes), 0.1),
            ("5% interv\nternaries", (make20ternaxes, scatter_20axes), 0.05),
            ("3.3% interv\nternaries", (make30ternaxes, scatter_30axes), 0.0333),
            ("9 plots at\n1% interv", (make9of100ternaxes, scatter_9of100axes), 0.01),
        ]
        self.stackedtern_uiinds = [4, 5, 6, 7, 8]
        if self.plotw3d or include3doption:
            self.quat3doptions = [
                ("3-D Quaternary", QuaternaryPlot),
            ]
            self.quat3d_uiinds = [9]
        else:
            self.quat3doptions = []
            self.quat3d_uiinds = []
        self.fillplotoptions()

    def fillplotoptions(self):
        self.plottypeComboBox.clear()
        self.plottypeComboBox.insertItem(0, "none")
        for count, tup in enumerate(self.ternaryfaceoptions):
            self.plottypeComboBox.insertItem(999, tup[0])
        for count, tup in enumerate(self.stackedternoptions):
            self.plottypeComboBox.insertItem(999, tup[0])
        for count, tup in enumerate(self.quat3doptions):
            self.plottypeComboBox.insertItem(999, tup[0])
        self.plottypeComboBox.setCurrentIndex(1)

    def loadplotdata(
        self,
        quatcomps,
        cols,
        nintervals=None,
        max_nintervals=30,
        comp1dindstocheck=[-1],
        negligible_comp_diff=0.005,
    ):
        self.cols = cols
        self.quatcomps = quatcomps
        if nintervals is None and len(self.quatcomps) > 0:
            #            pairwisediffs=(((quatcomps[1:]-quatcomps[:-1])**2).sum(axis=1))**.5/2.**.5
            #            mindiff=(pairwisediffs[pairwisediffs>0.005]).min()
            negligible_comp_diff2 = negligible_comp_diff ** 2
            mindiff = 999.0
            for elind in comp1dindstocheck:
                elconc = quatcomps[:, elind]
                elconcdiff = numpy.abs(elconc[1:] - elconc[:-1])
                elconcdiff = elconcdiff[elconcdiff > 0]
                if len(elconcdiff) == 0:  # all of them are equal
                    continue
                mindiff = min(mindiff, elconcdiff.min())
                mindiff2 = mindiff ** 2
                difflist = [
                    ((x0 - x1) ** 2) ** 0.5
                    for x0, x1 in itertools.combinations(elconc, 2)
                    if (x0 - x1) ** 2 > negligible_comp_diff2
                    and (x0 - x1) ** 2 < mindiff2
                ]
                if len(difflist) > 0:
                    mindiff = min(difflist)
            if (
                mindiff > 1.0
            ):  # actually menas 999 which means the mindiff was 0, all the checked comp axes were the same values within negligible_comp_diff
                self.nintervals = 5  # count this as the ~minumum number of intervals
            else:
                self.nintervals = int(min(max_nintervals, round(1.0 / mindiff)))
        else:
            self.nintervals = nintervals

    def plot(self, plotw=None, plotw3d=None, **kwargs):
        if plotw is None:
            plotw = self.plotw
        if plotw3d is None:
            plotw3d = self.plotw3d
        i = self.plottypeComboBox.currentIndex()
        if i == 0:
            return None
        if i in self.quat3d_uiinds:
            if plotw3d is None:
                plotw.redoaxes(
                    projection3d=True, cbaxkwargs=dict({}, axrect=self.plotwcbaxrect)
                )
                plotw3d = plotw
                self.cbax = plotw.cbax
            else:
                plotw3d.axes.cla()
            selclass = self.quat3doptions[self.quat3d_uiinds.index(i)][1]
            self.toComp = self.quat3dplot(plotw3d, selclass, **kwargs)
            return True
        plotw.fig.clf()
        if i in self.ternaryface_uiinds:
            selclass = self.ternaryfaceoptions[self.ternaryface_uiinds.index(i)][1]
            self.toComp = self.ternaryfaceplot(plotw, selclass, **kwargs)
        if i in self.stackedtern_uiinds:
            makefcn, scatterfcn = self.stackedternoptions[
                self.stackedtern_uiinds.index(i)
            ][1]
            delta = self.stackedternoptions[self.stackedtern_uiinds.index(i)][2]
            self.toComp = self.stackedternplot(
                plotw, makefcn, scatterfcn, delta, **kwargs
            )
        return False

    def quat3dplot(self, plotw3d, plotclass, **kwargs):
        if "s" in kwargs.keys() and not isinstance(kwargs["s"], int):
            kwargs["s"] = 18
        tf = plotclass(
            plotw3d.axes, ellabels=self.ellabels
        )  # , nintervals=self.nintervals)
        tf.label()
        tf.scatter(self.quatcomps, c=self.cols, **kwargs)
        return lambda x, y, ax: None

    def ternaryfaceplot(self, plotw, plotclass, **kwargs):
        if not self.plotwcbaxrect is None:
            plotw.axes = plotw.fig.add_axes((0, 0, self.plotwcbaxrect[0] - 0.01, 1))
            self.cbax = plotw.fig.add_axes(self.plotwcbaxrect)
        else:
            plotw.axes = plotw.fig.add_axes((0, 0, 1, 1))
        ax = plotw.axes
        tf = plotclass(ax, nintervals=self.nintervals, ellabels=self.ellabels)
        tf.label()
        tf.scatter(self.quatcomps, self.cols, **kwargs)
        return lambda x, y, ax: tf.toComp(x, y)

    def stackedternplot(
        self, plotw, makefcn, scatterfcn, delta, drawcolorbarhere=False, **kwargs
    ):
        if "s" in kwargs.keys() and not isinstance(kwargs["s"], int):
            kwargs["s"] = 18
        plotw.fig.clf()
        if self.plotwcbaxrect is None:
            self.cbax = None
            kwargs["cb"] = False
        elif drawcolorbarhere:
            self.cbax = None  # if drawing here cannot pass the cbax because scatterfcn doesn't return it
            kwargs["cb"] = True
            kwargs["cbrect"] = self.plotwcbaxrect
        else:  # going to draw colorbar externally so only make cbax here
            self.cbax = plotw.fig.add_axes(self.plotwcbaxrect)
            kwargs["cb"] = False  # do not make the colorbar in the scatterfcn
        self.axl, self.stpl = makefcn(fig=plotw.fig, ellabels=self.ellabels)
        scatterfcn(self.quatcomps, self.cols, self.stpl, edgecolor="none", **kwargs)

        def toComp(x, y, ax, delta=delta, axl=copy.copy(self.axl)):
            if not ax in axl:
                return None
            i = axl.index(ax)
            dclick = delta * i
            bclick = y * 2.0 / numpy.sqrt(3.0)
            aclick = 1.0 - x - bclick / 2.0
            cclick = 1.0 - aclick - bclick
            compclick = numpy.float64([aclick, bclick, cclick, dclick])
            compclick[:3] *= 1.0 - dclick
            if numpy.all((compclick >= 0.0) & (compclick <= 1.0)):
                return compclick
            else:
                return None

        return toComp


# class plotwidget(FigureCanvas):
#    def __init__(self, parent, width=12, height=6, dpi=72, projection3d=False):
#
#        #plotdata can be 2d array for image plot or list of 2 1d arrays for x-y plot or 2d array for image plot or list of lists of 2 1D arrays
#
#        self.fig=Figure(figsize=(width, height), dpi=dpi)
#        if projection3d:
#            self.axes=self.fig.add_subplot(111, navigate=True, projection='3d')
#        else:
#            self.axes=self.fig.add_subplot(111, navigate=True)
#            self.mpl_connect('button_press_event', self.myclick)
#
#        self.axes.hold(True)
#        FigureCanvas.__init__(self, self.fig)
#        self.setParent(parent)
#        #self.parent=parent
#        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
#        FigureCanvas.updateGeometry(self)
#        #NavigationToolbar(self, parent)
#        self.toolbar=NavigationToolbar(self, self)
#
#
#        self.clicklist=[]
#
#    def myclick(self, event):
#        if not (event.xdata is None or event.ydata is None):
#            arrayxy=[event.xdata, event.ydata]
#            print 'clicked on image: array indeces ', arrayxy, ' using button', event.button
#            self.clicklist+=[arrayxy]
#            self.emit(SIGNAL("genericclickonplot"), [event.xdata, event.ydata, event.button])
#
