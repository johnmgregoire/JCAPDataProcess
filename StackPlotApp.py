import itertools, time
from PyQt5.QtWidgets import *
import os, os.path
import sys
import numpy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import operator
import matplotlib

projectpath = os.path.split(os.path.abspath(__file__))[0]
sys.path.append(os.path.join(projectpath, "QtForms"))
sys.path.append(os.path.join(projectpath, "AuxPrograms"))
sys.path.append(os.path.join(projectpath, "OtherApps"))
import matplotlib.colors as colors
import matplotlib.cm as cm
import pylab
from fcns_math import *
from fcns_io import *
from fcns_ui import *

print time.ctime()
from VisualizeAuxFcns import *
from StackPlotForm import Ui_StackPlotDialog
from SaveImagesApp import *
from LoadCSVApp import loadcsvDialog


from OpenFromInfoApp import openfrominfoDialog
from StackPlotClasses import StackClasses

GUIMODE = True


class stackplotDialog(QDialog, Ui_StackPlotDialog):
    def __init__(self, parent=None, title="", folderpath=None, GUIMODE=GUIMODE):
        super(stackplotDialog, self).__init__(parent)
        self.setupUi(self)
        self.GUIMODE = GUIMODE
        self.parent = parent
        # self.SelectTreeView.setModel(CheckableDirModel(self))
        self.AnaExpFomTreeWidgetFcns = treeclass_anaexpfom(
            self.AnaExpFomTreeWidget, None
        )
        button_fcn = [
            (self.AnaPushButton, self.importana),
            (self.OpenInfoPushButton, self.importfrominfo),
            (self.UpdateFiltersPushButton, self.filterandplotstackdata),
            (self.UpdatePlotPushButton, self.plot),
            (self.customxystylePushButton, self.getxystyle_user),
            (self.SaveFigsPushButton, self.savefigs),
            (self.LoadCsvPushButton, self.loadcsv),
            (self.ClearPushButton, self.clearall),
            (self.RaiseErrorPushButton, self.raiseerror),
            (self.EditParamsPushButton, self.editparams),
        ]
        # (self.UndoExpPushButton, self.undoexpfile), \
        for button, fcn in button_fcn:
            button.pressed.connect(fcn)
        self.SelectTreeWidget.clear()
        self.SelectTreeFileFilterTopLevelItem = None
        # QObject.connect(self.AnaExpFomTreeWidget, SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.processclick_selecttreeitem)
        self.xplotchoiceComboBox.activated["QString"].connect(self.fillxsearchstr)
        for count, c in enumerate(StackClasses):
            self.StackClassComboBox.insertItem(count, c.stackplot_name)
        self.plotwsetup()
        self.clearall()

    def raiseerror(self):
        raiseerror

    def clearall(self):
        self.l_fomdlist = []
        self.l_fomnames = []
        self.l_csvheaderdict = []
        self.repr_anaint_plots = 1
        self.anafiledict = {}
        self.expfiledict = {}
        self.expzipclass = None
        self.anazipclass = None
        self.getactiveclass()
        self.expfolder = ""
        self.clearfomplotd()
        self.clearvisuals()

    def clearfomplotd(self):
        self.fomplotd = dict({}, fomdlist_index0=[], fomdlist_index1=[])
        self.stackplotd = None

    def fillxsearchstr(self):
        if not self.stackplotd is None:  # dont' overwrite if stak plot already defined
            return
        cb = self.xplotchoiceComboBox
        self.StackXKeySearchLineEdit.setText(str(cb.currentText()))

    def editparams(self):
        if self.stackplotclass is None or len(self.stackplotclass.params) == 0:
            return
        keys_paramsd = [
            k for k, v in self.analysisclass.params.iteritems() if isinstance(v, dict)
        ]
        if len(keys_paramsd) == 0:
            self.editparams_paramsd(self.stackplotclass.params)
            return
        else:
            keys_paramsd = ["<non-nested params>"] + keys_paramsd
        i = userselectcaller(
            self, options=keys_paramsd, title="Select type of parameter to edit"
        )
        if i == 0:
            self.editparams_paramsd(self.stackplotclass.params)
        else:
            self.editparams_paramsd(self.stackplotclass.params[keys_paramsd[i]])

    def editparams_paramsd(self, paramsd):
        inputs = [
            (k, type(v), (isinstance(v, str) and (v,) or (str(v),))[0])
            for k, v in paramsd.iteritems()
            if not isinstance(v, dict)
        ]
        if len(inputs) == 0:
            return
        ans, changedbool = userinputcaller(
            self,
            inputs=inputs,
            title="Enter Calculation Parameters",
            returnchangedbool=True,
        )
        somethingchanged = False
        for (k, tp, v), newv, chb in zip(inputs, ans, changedbool):
            if chb:
                paramsd[k] = newv
                somethingchanged = True
        if (
            somethingchanged
        ):  # soem analysis classes have different files applicable depending on user-enter parameters so update here but don't bother deleting if numfiles goes to 0
            self.processeditedparams()

    def processeditedparams(self):
        self.stackplotclass.processnewparams(StackPlotDialogclass=self)
        self.getactiveclass()

    def getactiveclass(self):
        ind = int(self.StackClassComboBox.currentIndex())
        self.stackplotclass = StackClasses[ind]

    def importfrominfo(self):
        idialog = openfrominfoDialog(self, runtype="", exp=True, ana=True, run=False)
        idialog.exec_()
        if idialog.selecttype == "ana":
            self.importana(p=idialog.selectpath)
        if idialog.selecttype == "exp":
            self.importexp(experiment_path=idialog.selectpath)

    def importana(
        self,
        p=None,
        anafiledict=None,
        anafolder=None,
        anazipclass=None,
        ellabelsforquatplots="ask",
    ):  # if running batch set ellabelsforquatplots to something else
        if anafiledict is None or anafolder is None:
            if p is None:
                p = selectexpanafile(
                    self, exp=False, markstr="Select .ana/.pck to import, or .zip file"
                )
            if len(p) == 0:
                return
            self.anafiledict, anazipclass = readana(
                p, stringvalues=False, erroruifcn=None, returnzipclass=True
            )
            if len(self.anafiledict) == 0:
                idialog = messageDialog(
                    self, "Aborting import of ana - Failed to read \n%s" % p
                )
                idialog.exec_()
                return
            if p.endswith(".ana") or p.endswith(".pck"):
                self.anafolder = os.path.split(p)[0]
            else:
                self.anafolder = p
            if self.anazipclass:
                self.anazipclass.close()
            self.anazipclass = anazipclass
        else:
            self.anafiledict = anafiledict
            self.anafolder = anafolder
            if self.anazipclass:
                self.anazipclass.close()
            self.anazipclass = anazipclass  # when run from CalcFOMApp the .ana can't be in a .zip so make this the default anazipclass=None
        self.clearvisuals()
        self.importexp(
            experiment_path=self.anafiledict["experiment_path"], fromana=True
        )
        self.l_fomdlist = []
        self.l_fomnames = []
        self.l_csvheaderdict = []
        templ_platemap4keys = []
        readandformat_anafomfiles(
            self.anafolder,
            self.anafiledict,
            self.l_fomdlist,
            self.l_fomnames,
            self.l_csvheaderdict,
            templ_platemap4keys,
            self.AnaExpFomTreeWidgetFcns,
            anazipclass=self.anazipclass,
            anakl=self.sorted_ana_exp_keys(),
        )
        self.expanafilenameLineEdit.setText(os.path.normpath(self.anafolder))
        self.setupfilterchoices()
        self.fillxyoptions(clear=True)

    def importexp(
        self, experiment_path=None, fromana=False, ellabelsforquatplots="ask"
    ):  # experiment_path here is the folder, not the file. thsi fcn geretaes expapth, which is the file, but it could be the file too
        if experiment_path is None:
            exppath = selectexpanafile(
                self, exp=True, markstr="Select .exp/.pck EXP file, or .zip file"
            )
            if exppath is None or len(exppath) == 0:
                return
        else:
            if experiment_path.endswith(".exp") or experiment_path.endswith(".pck"):
                exppath = experiment_path
            else:
                exppath = buildexppath(experiment_path)
        expfiledict, expzipclass = readexpasdict(
            exppath, includerawdata=False, erroruifcn=None, returnzipclass=True
        )
        if expfiledict is None:
            print "Problem opening EXP"
            return
        #        self.clearexp()
        self.exppath = exppath
        self.expfolder = os.path.split(exppath)[0]
        self.expfiledict = expfiledict
        if self.expzipclass:
            self.expzipclass.close()
        self.expzipclass = expzipclass
        self.AnaExpFomTreeWidgetFcns.initfilltree(self.expfiledict, self.anafiledict)
        self.clearfomplotd()

    def sorted_ana_exp_keys(self, ana=True):
        if ana:
            anarun = "ana__"
            anaexpfiled = self.anafiledict
        else:
            anarun = "run__"
            anaexpfiled = self.expfiledict
        sorttups = sorted(
            [
                (int(k[len(anarun) :]), k)
                for k in anaexpfiled.keys()
                if k.startswith(anarun)
            ]
        )
        return map(operator.itemgetter(1), sorttups)

    def fillxyoptions(self, clear=False):  # TODO
        cbl = [
            self.xplotchoiceComboBox,
            self.yplotchoiceComboBox,
            self.rightyplotchoiceComboBox,
        ]
        fomopts = set([n for fomnames in self.l_fomnames for n in fomnames])
        for cbcount, cb in enumerate(cbl):
            if clear:
                cb.clear()
                cb.insertItem(0, "None")
            for count, s in enumerate(fomopts):
                cb.insertItem(count + 1, s)
                if cbcount == 0 and "norm_dist" in s:
                    cb.setCurrentIndex(count + 1)

    def setupfilterchoices(self):
        self.SelectTreeWidget.clear()
        for count, fomdlist in enumerate(self.l_fomdlist):
            if len(fomdlist) == 0 or not "anaint" in fomdlist[0].keys():
                continue
            mainitem = QTreeWidgetItem(
                ["%d:ana__%d" % (count, fomdlist[0]["anaint"])], 0
            )
            self.SelectTreeWidget.addTopLevelItem(mainitem)
            for k in fomdlist[0].keys():
                item = QTreeWidgetItem([k], 0)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(0, Qt.Unchecked)
                mainitem.addChild(item)
            mainitem.setExpanded(True)

    def loadcsv(self):
        # TODO
        newrunk = self.gethighestrunk(
            getnextone=True
        )  # create a new run, maybe wouldn't need to if somethign already loaded but usually thsi will be used to load only .csv so need to create a run for toehr mechanics to work
        pmpath = str(self.platemapfilenameLineEdit.text()).split(",")[
            -1
        ]  # last used platemap or empty if non loaded
        idialog = loadcsvDialog(
            self,
            ellabels=self.ellabels,
            platemappath=pmpath,
            csvstartpath=self.expfolder,
            runk=newrunk,
        )
        if idialog.error:
            return
        if not idialog.exec_():
            return
        if idialog.error:
            return
        self.ellabels = idialog.ellabels
        if not "exp_version" in self.expfiledict.keys():
            self.expfiledict["exp_version"] = 0
        self.expfiledict[newrunk] = copy.deepcopy(idialog.rund)
        s = str(self.platemapfilenameLineEdit.text())
        ps = str(idialog.platemapLineEdit.text())
        if not ps in s:
            self.platemapfilenameLineEdit.setText(",".join([s, ps]).strip(","))
        fomnames = copy.copy(idialog.fomnames)
        self.expfiledict[newrunk]["run_path"] = idialog.csvpath
        self.expfiledict[newrunk]["run_use"] = "usercsv"
        self.expfiledict[newrunk]["files_technique__usercsv"] = {}
        self.expfiledict[newrunk]["files_technique__usercsv"][
            "csv_files"
        ] = copy.deepcopy(idialog.runfilesdict)
        self.l_fomdlist += [
            copy.deepcopy(idialog.fomdlist)
        ]  # on-the-fly analysis gets appended to the list of dictionaries, but since opening ana cleans these lists, the l_ structures will start with ana csvs.
        self.l_fomnames += [copy.copy(idialog.fomnames)]
        # TODO
        if self.ellabels == [
            "A",
            "B",
            "C",
            "D",
        ]:  # If default ellabels give option for user to enter new ones. otherwise assume thigns already loaded and use existing ellabels
            self.fillcomppermutations()
        else:
            self.remap_platemaplabels()
        if newrunk == "run__1":
            self.AnaExpFomTreeWidgetFcns.initfilltree(
                self.expfiledict, self.anafiledict
            )  # might erase things that already exist
        self.updatefomdlist_plateruncode()  # inds=[-1])
        self.AnaExpFomTreeWidgetFcns.appendFom(
            self.l_fomnames[-1], self.l_csvheaderdict[-1], uncheckprevious=True
        )
        self.setupfilterchoices()
        self.updatefomplotchoices()
        self.fillxyoptions()  # clear=True

    def filterandplotstackdata(self, plotbool=True):
        self.clearfomplotd()
        l_usefombool = self.AnaExpFomTreeWidgetFcns.getusefombools()
        for k in ["fomdlist_index0", "fomdlist_index1"]:
            self.fomplotd[k] = []
        for fomdlist_index0, (usebool, fomdlist, fomnames) in enumerate(
            zip(l_usefombool, self.l_fomdlist, self.l_fomnames)
        ):
            # not plotting foms like in vis so just keep track of the ana in play for xyy in extractxy_fomnames. so filter duplicate fom names using checkboxes in AnaExpFomTreeWidgetFcns
            if not usebool:
                continue
            self.fomplotd["fomdlist_index0"] += [fomdlist_index0] * len(fomdlist)
            self.fomplotd["fomdlist_index1"] += range(len(fomdlist))
        for k in ["fomdlist_index0", "fomdlist_index1"]:
            self.fomplotd[k] = numpy.array(self.fomplotd[k])
        # stack plot foms chosen from checked boxes in a single ana
        xkeysearchstr = str(self.StackXKeySearchLineEdit.text()).strip()
        l_ind = None
        for l_count in range(int(self.SelectTreeWidget.topLevelItemCount())):
            mainitem = self.SelectTreeWidget.topLevelItem(l_count)
            checkedkeys = [
                str(mainitem.child(i).text(0)).strip()
                for i in range(mainitem.childCount())
                if bool(mainitem.child(i).checkState(0))
            ]
            if len(checkedkeys) > 0:  # find first ana that has checks and use that
                xkeyl = [k for k in self.l_fomnames[l_count] if xkeysearchstr in k]
                if len(xkeyl) == 0:
                    continue
                elif len(xkeyl) > 1:
                    print "WARNING: more than 1 stack x key match search"
                xkey = xkeyl[0]
                l_ind = l_count
                break
        if l_ind is None:
            return
        fomdlist = self.l_fomdlist[l_ind]
        arr2d = numpy.array([[d[k] for d in fomdlist] for k in [xkey] + checkedkeys])
        inds = numpy.where(numpy.logical_not(numpy.isnan(arr2d.prod(axis=1))))[0]
        if len(inds) == 0:
            return
        arr2d = arr2d[inds]
        sortinds = numpy.argsort(arr2d[0])
        self.stackplotd = {}
        self.stackplotd["xkey"] = xkey
        self.stackplotd["xarr"] = arr2d[0][sortinds]
        checkedarr2d = arr2d[1:, sortinds]
        checkedarr2d /= checkedarr2d.sum(axis=0)[numpy.newaxis, :]
        avexindex = (
            numpy.arange(checkedarr2d.shape[1])[numpy.newaxis, :] * checkedarr2d
        ).sum(axis=1)
        checksortinds = numpy.argsort(avexindex)
        self.stackplotd["stackarr_keysbyxpts"] = checkedarr2d[checksortinds]
        self.stackplotd["stackkeys"] = [checkedkeys[i] for i in checksortinds]
        self.repr_anaint_plots = fomdlist[0]["anaint"]
        if plotbool:
            self.stackplot()

    def stackplot(self):
        self.plotw_xy.axes.cla()
        self.plotw_xy.twaxes.cla()
        colsstrs = str(self.StackColorsTextEdit.toPlainText()).split("\n")
        cols = [
            [myeval(s.strip()) for s in ls.split(",")]
            for ls in colsstrs
            if ls.count(",") == 2
        ]
        if len(cols) == 0:
            if self.GUIMODE:
                idialog = messageDialog(self, "Failed to Read colors")
                idialog.exec_()
            return
        cols = cols[: len(self.stackplotd["stackarr_keysbyxpts"])]
        if len(cols) != len(self.stackplotd["stackarr_keysbyxpts"]):
            cols = cols * (len(self.stackplotd["stackarr_keysbyxpts"]) // len(cols) + 1)
            cols = cols[: len(self.stackplotd["stackarr_keysbyxpts"])]
        self.stackcolors = cols
        self.getactiveclass()
        ax = self.plotw_xy.stackaxes
        legax = self.plotw_xy.legendaxes
        for l, col in zip(self.stackplotd["stackkeys"], cols):
            legax.plot(
                [], [], marker="s", ls="None", c=col, markersize=8, alpha=1.0, label=l
            )
        # legax.legend(loc=2, bbox_to_anchor=(1.1, .55), numpoints=1, markerscale=2, frameon=False, prop={'size':12})
        legax.legend(
            loc=2, numpoints=1, markerscale=2, frameon=False, prop={"size": 12}
        )
        self.stackplotclass.stackplot(ax, self)
        ax.set_yticks([])
        ax.margins(0, 0)
        ax.set_zorder(1)
        self.plotw_xy.fig.canvas.draw()
        # self.plotw_legends.fig.canvas.draw()

    def extractxy_fomnames(self, arrkeys):
        # get the fomdlist that have the requested fomname and make sure it is represented in the fomplotd,  which is post-filters
        # if plotting fom1 vs fom2 they both need to be in the same fomd, i.e. this routine will not try to pair them up by plate,sample or other means
        fominds_xyy = [
            [
                i0
                for i0, fomnames in enumerate(self.l_fomnames)
                if k in fomnames and i0 in self.fomplotd["fomdlist_index0"]
            ]
            for k in arrkeys
        ]
        if (
            len(fominds_xyy[0]) + len(fominds_xyy[1]) + len(fominds_xyy[2]) == 0
        ):  # if none of x,y,yl in fomnames quit but otherwise only use x,y,yl that are in fomnames
            return None
        x_inds_fom = []
        plotdata = [[[], []], [[], []]]
        selectpointdata = [[[], []], [[], []]]
        for count, (k, i0list) in enumerate(zip(arrkeys, fominds_xyy)):
            inds_fom = [
                [(i0, i1), self.l_fomdlist[i0][i1][k]]
                for i0 in i0list
                for i1 in self.fomplotd["fomdlist_index1"][
                    self.fomplotd["fomdlist_index0"] == i0
                ]
            ]
            if len(inds_fom) == 0:
                continue
            if count == 0:
                x_inds_fom = inds_fom
            else:
                if arrkeys[0] == "None":  # for x use indexes
                    ytemp = map(operator.itemgetter(1), inds_fom)
                    ytemp = numpy.array(ytemp)
                    ytemp = ytemp[numpy.logical_not(numpy.isnan(ytemp))]
                    xtemp = numpy.arange(len(ytemp))
                    plotdata[count - 1] = [xtemp, ytemp]
                    if not self.selectind is None:
                        i0, i1 = (
                            self.fomplotd["fomdlist_index0"][self.selectind],
                            self.fomplotd["fomdlist_index1"][self.selectind],
                        )
                        if (i0, i1) in map(operator.itemgetter(0), inds_fom):
                            i = map(operator.itemgetter(0), inds_fom).index((i0, i1))
                            selectpointdata[count - 1] = [[i], [inds_fom[i][1]]]
                else:
                    # pair up fom data points between x and y
                    indsset = sorted(
                        list(
                            set(map(operator.itemgetter(0), inds_fom)).intersection(
                                map(operator.itemgetter(0), x_inds_fom)
                            )
                        )
                    )
                    if len(indsset) == 0:
                        continue
                    if not self.selectind is None:
                        i0, i1 = (
                            self.fomplotd["fomdlist_index0"][self.selectind],
                            self.fomplotd["fomdlist_index1"][self.selectind],
                        )
                        if (i0, i1) in indsset:
                            selectpointdata[count - 1] = [
                                [self.l_fomdlist[i0][i1][arrkeys[0]]],
                                [self.l_fomdlist[i0][i1][k]],
                            ]  # signle data point corresponding to select sample
                    xtemp = numpy.array(
                        [fom for inds, fom in x_inds_fom if inds in indsset]
                    )
                    ytemp = numpy.array(
                        [fom for inds, fom in inds_fom if inds in indsset]
                    )
                    notnaninds = numpy.where(
                        numpy.logical_not(numpy.isnan(xtemp))
                        & numpy.logical_not(numpy.isnan(ytemp))
                    )[0]
                    xtemp = xtemp[notnaninds]
                    sortinds = numpy.argsort(xtemp)
                    xtemp = xtemp[sortinds]
                    ytemp = ytemp[notnaninds][sortinds]
                    plotdata[count - 1] = [xtemp, ytemp]
        return plotdata, selectpointdata

    def extractxydata(self, arrkeys):
        # plottign from single file so x is required to be in there and then if either of the y are in, filter by nan and sort. No label for legend because not necessarily a sample_no, i.e. could be a fom file selected
        if len(self.l_fomnames) > 0:
            tempplotdatatup = self.extractxy_fomnames(arrkeys)
            if not tempplotdatatup is None:
                return tempplotdatatup[0]
        else:
            return None

    def plot(
        self,
    ):  # filed to plot from a  single file and must have key 'path' in addition to standard filed
        cbl = [
            self.xplotchoiceComboBox,
            self.yplotchoiceComboBox,
            self.rightyplotchoiceComboBox,
        ]
        arrkeys = [str(cb.currentText()) for cb in cbl]
        if arrkeys == (["None"] * 3):
            return
        tempplotdatatup = self.extractxydata(arrkeys)
        if tempplotdatatup is None:
            return
        self.plotdata = tempplotdatatup
        if not self.overlayselectCheckBox.isChecked():
            self.plotw_xy.axes.cla()
            self.plotw_xy.twaxes.cla()
        if self.overlayselectCheckBox.isChecked():
            self.xyplotcolorrotation = self.xyplotcolorrotation[1:] + [
                self.xyplotcolorrotation[0]
            ]
            self.xyplotstyled["c"] = self.xyplotcolorrotation[0]
        else:
            self.xyplotcolorrotation = ["b", "k", "m", "y", "c", "r", "g"]
            self.xyplotstyled["c"] = "b"
        somethingplotted = False
        legax = self.plotw_xy.legendaxes
        for count, (ax, (xarr, yarr), xl, yl) in enumerate(
            zip(
                [self.plotw_xy.axes, self.plotw_xy.twaxes],
                self.plotdata,
                [arrkeys[0], arrkeys[0]],
                [arrkeys[1], arrkeys[2]],
            )
        ):
            if len(xarr) == 0:
                continue
            somethingplotted = True
            if count == 0:
                styled = dict(
                    [
                        (k, v)
                        for k, v in self.xyplotstyled.iteritems()
                        if not "sel" in k and not "right_" in k and v != ""
                    ]
                )
            else:
                styled = dict(
                    [
                        (k.partition("right_")[2], v)
                        for k, v in self.xyplotstyled.iteritems()
                        if "right_" in k and v != ""
                    ]
                )
            ax.plot(xarr, yarr, **styled)
            ax.set_xlabel(xl)
            ax.set_ylabel(yl)
            legax.plot([], [], label=yl, **styled)
        legax.legend(loc=3, frameon=False, prop={"size": 12})
        # leg=self.plotw_xy.axes.legend(loc=0)
        # leg.draggable()
        autotickformat(self.plotw_xy.axes, x=1, y=1)
        autotickformat(self.plotw_xy.twaxes, x=0, y=1)
        self.plotw_xy.axes.patch.set_alpha(0)
        self.plotw_xy.axes.set_zorder(3)
        self.plotw_xy.twaxes.patch.set_alpha(0)
        self.plotw_xy.twaxes.set_zorder(3)
        self.plotw_xy.fig.canvas.draw()

    def clearvisuals(self):
        self.expanafilenameLineEdit.setText("")
        self.plotw_xy.axes.cla()
        self.plotw_xy.twaxes.cla()
        self.plotw_xy.fig.canvas.draw()

    def plotwsetup(self):
        self.xyplotstyled = dict(
            {},
            marker="o",
            ms=5,
            c="b",
            ls="-",
            lw=0.7,
            right_marker="None",
            right_ms=3,
            right_ls=":",
            right_lw=0.7,
            select_ms=6,
            select_c="r",
            right_c="g",
        )
        self.xyplotcolorrotation = ["b", "k", "m", "y", "c", "r", "g"]
        self.selectind = None
        self.plotw_xy = plotwidget(self)
        self.plotw_xy.fig.set_facecolor("w")
        self.plotw_xy.stackaxes = self.plotw_xy.axes.twinx()
        self.plotw_xy.twaxes = self.plotw_xy.axes.twinx()
        for b, w in [
            (self.textBrowser_xy, self.plotw_xy),
        ]:
            w.setGeometry(b.geometry())
            b.hide()
        self.plotw_xy.fig.subplots_adjust(left=0.15, bottom=0.12, right=0.65, top=0.92)
        self.plotw_xy.legendaxes = self.plotw_xy.fig.add_axes([0.8, 0, 0.2, 1])
        self.plotw_xy.legendaxes.set_xticks([])
        self.plotw_xy.legendaxes.set_yticks([])

    def getxystyle_user(self):
        inputs = [
            (k, type(v), str(v))
            for k, v in self.xyplotstyled.iteritems()
            if not (k.startswith("right_") or k.startswith("select_"))
        ]
        inputs += [
            (k, type(v), str(v))
            for k, v in self.xyplotstyled.iteritems()
            if k.startswith("select_")
        ]
        inputs += [
            (k, type(v), str(v))
            for k, v in self.xyplotstyled.iteritems()
            if k.startswith("right_")
        ]
        ans = userinputcaller(
            self, inputs=inputs, title="Enter x-y plot parameters", cancelallowed=True
        )
        if ans is None:
            return
        self.xyplotstyled = dict([(tup[0], v) for tup, v in zip(inputs, ans)])

    def savefigs(self, filenamesearchlist=None, justreturndialog=False, prependstr=""):
        cbl = [
            self.xplotchoiceComboBox,
            self.yplotchoiceComboBox,
            self.rightyplotchoiceComboBox,
        ]
        x_y_righty = [
            str(cb.currentText()) for cb in cbl if str(cb.currentText()) != "None"
        ]
        xyplotw = self.plotw_xy
        idialog = saveimagesDialog(
            self,
            self.anafolder,
            self.fomplotd["fomname"],
            plateid_dict_list=[],
            code_dict_list=[],
            histplow=None,
            xyplotw=xyplotw,
            x_y_righty=x_y_righty,
            repr_anaint_plots=self.repr_anaint_plots,
            selectsamplebrowser=None,
            filenamesearchlist=filenamesearchlist,
        )
        idialog.prependfilenameLineEdit.setText(prependstr)
        if justreturndialog:
            return idialog
        else:
            idialog.exec_()
            if idialog.newanapath:
                self.importana(p=idialog.newanapath)


if __name__ == "__main__":

    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):
            super(MainMenu, self).__init__(None)
            self.stackui = stackplotDialog(
                self, title="Visualize Stack Plots from ANA data", **kwargs
            )
            #            p=r'\\htejcap.caltech.edu\share\home\processes\analysis\temp\20150909.230012.done\20150909.230012.ana'
            #            self.stackui.importana(p=p)
            #            self.stackui.plotfom()
            if execute:
                self.stackui.exec_()

    mainapp = QApplication(sys.argv)
    form = MainMenu(None)
    form.show()
    form.setFocus()
    mainapp.exec_()
