import time
from PyQt5.QtWidgets import *
import os, os.path, shutil
import sys
import numpy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import operator
import pylab
from fcns_math import *
from fcns_io import *
from fcns_ui import *


def createontheflyrundict(expfiledict, expfolder, lastmodtime=0):
    d = expfiledict["run__1"]["files_technique__onthefly"]["all_files"]
    d_appended = {}
    fnl = os.listdir(expfolder)
    modtimes = [
        os.path.getmtime(os.path.join(expfolder, fn)) for fn in fnl
    ]  # expfolder not a .zip becuase on-the-fly
    modtime = max(modtimes)
    fnl2 = [fn for fn, mt in zip(fnl, modtimes) if mt > lastmodtime]
    for fn in fnl2:
        p = os.path.join(expfolder, fn)
        smp, attrd = smp_dict_generaltxt(
            p,
            delim="",
            returnsmp=True,
            addparams=False,
            lines=None,
            returnonlyattrdict=True,
        )
        if len(attrd) == 0:
            print "error reading ", fn
            if fn in d.keys():
                del d[
                    fn
                ]  # there was a previous versino of this file that has been overwritten
            continue
        d[fn] = copy.copy(attrd)
        d_appended[fn] = d[fn]
    return modtime, d_appended


def d_nestedkeys(d, keylist):
    return reduce(lambda dd, k: dd[k], keylist, d)


# plateid,code,sample,fom,xy,comp
def extractplotdinfo(
    fomd,
    pmkeys,
    fomname,
    expfiledict,
    fomdlist_index0,
    fomdlist_index1,
    calc_comps__starts_contains_tups=None,
):  # , ellabels=['a', 'b', 'c', 'd']):
    d = fomd
    returnlist = [fomdlist_index0, fomdlist_index1]
    returnlist += [d[k] for k in ["plate_id", "code", "sample_no", fomname]]
    if d["sample_no"] == 0:
        returnlist += [[numpy.nan] * 2, [numpy.nan] * 4]
    else:
        rund = expfiledict["run__%d" % d["runint"]]
        pmd = rund["platemapdlist"][rund["platemapsamples"].index(d["sample_no"])]
        returnlist += [[pmd[k] for k in ["x", "y"]]]
        if (
            calc_comps__starts_contains_tups is None
            or len(
                [
                    k
                    for startstr, contstr in calc_comps__starts_contains_tups
                    for k in d.keys()
                    if k.startswith(startstr) and contstr in k
                ]
            )
            == 0
        ):  # default platemap comps or no keys available for calc comp
            returnlist += [[pmd[k] for k in pmkeys]]
        else:  # at least 1 key available so use all available and fill zero otherwise. If multiple keys match criteria, use the first one found
            getmatchklist = lambda startstr, contstr: [
                k for k in d.keys() if k.startswith(startstr) and contstr in k
            ]
            matchkeys = [
                None
                if len(getmatchklist(startstr, contstr)) == 0
                else getmatchklist(startstr, contstr)[0]
                for startstr, contstr in calc_comps__starts_contains_tups
            ]
            returnlist += [[0.0 if k is None else d[k] for k in matchkeys]]
    return returnlist


def readandformat_anafomfiles(
    anafolder,
    anafiledict,
    l_fomdlist,
    l_fomnames,
    l_csvheaderdict,
    l_platemapkeys,
    treefcns,
    anazipclass=None,
    anakl=None,
    platemap4keys_default=["A", "B", "C", "D"],
):
    if anakl is None:
        anakl = sort_dict_keys_by_counter(anafiledict, keystartswith="ana__")
    for anak in anakl:
        foundafomfile = False
        anad = anafiledict[anak]
        anaint = int(anak.partition("ana__")[2])
        for anarunk, anarund in anad.iteritems():
            if not anarunk.startswith("files_"):
                continue
            for typek, typed in anarund.iteritems():
                for filek, filed in typed.iteritems():
                    if not (
                        "fom_file" in filed["file_type"] and filek.endswith(".csv")
                    ):  # TODO: is this the right way to selct what is read as foms?
                        continue
                    p = os.path.join(anafolder, filek)
                    fomd, csvheaderdict = readcsvdict(
                        p, filed, returnheaderdict=True, zipclass=anazipclass
                    )
                    if len(fomd) == 0:  # csv was only str values that were not read
                        continue
                    keys = (
                        fomd.keys()
                    )  # this is different from filed['keys'] if there are str vlaues in csv
                    fomdlist = [
                        dict([(k, fomd[k][count]) for k in keys] + [("anaint", anaint)])
                        for count in range(len(fomd[keys[0]]))
                    ]
                    l_fomdlist += [fomdlist]
                    l_fomnames += [keys + ["anaint"]]
                    csvheaderdict["anak"] = anak
                    l_csvheaderdict += [csvheaderdict]
                    if "platemap_comp4plot_keylist" in anad.keys():
                        pmkeys = anad["platemap_comp4plot_keylist"].split(",")
                    else:
                        pmkeys = platemap4keys_default
                    l_platemapkeys += [pmkeys]
                    treefcns.appendFom(keys, csvheaderdict, anak=anak, anad=anad)
                    foundafomfile = True
        if not foundafomfile:
            fomdlist = []
            foundsmps = []
            pid = anad["plate_ids"] if isinstance(anad["plate_ids"], int) else 0
            for anarunk, anarund in anad.iteritems():
                if not anarunk.startswith("files_run__"):
                    continue
                runint = eval(anarunk.partition("files_run__")[2])
                for typek, typed in anarund.iteritems():
                    newsmps = [
                        filed["sample_no"]
                        for filek, filed in typed.iteritems()
                        if "sample_no" in filed.keys()
                        and filed["sample_no"] > 0
                        and not filed["sample_no"] in foundsmps
                    ]
                    fomdlist += [
                        {
                            "sample_no": smp,
                            "anaint": anaint,
                            "runint": runint,
                            "plate_id": pid,
                        }
                        for smp in newsmps
                    ]
                    foundsmps += newsmps
            if len(fomdlist) > 0:
                keys = fomdlist[0].keys()
                l_fomdlist += [fomdlist]
                l_fomnames += [keys]
                csvheaderdict = {}
                csvheaderdict["anak"] = anak
                l_csvheaderdict += [csvheaderdict]
                if "platemap_comp4plot_keylist" in anad.keys():
                    pmkeys = anad["platemap_comp4plot_keylist"].split(",")
                else:
                    pmkeys = platemap4keys_default
                l_platemapkeys += [pmkeys]
                treefcns.appendFom(keys, csvheaderdict, anak=anak, anad=anad)


class legendformatwidget(QDialog):
    def __init__(self, parent=None, title=""):  # , arr=None):
        super(legendformatwidget, self).__init__(parent)
        self.parent = parent
        templab = QLabel()
        templab.setText("fom fmt")
        self.fomfmtLineEdit = QLineEdit()
        self.fomfmtLineEdit.setText("%.2e")
        templab2 = QLabel()
        templab2.setText("comp fmt")
        self.compfmtLineEdit = QLineEdit()
        self.compfmtLineEdit.setText("%d")
        templab3 = QLabel()
        templab3.setText(
            "legend contents, for example\n<sample>, <A><a><B><b><C><c><D><d>, <code>, <fom>, <x>, <y>"
        )
        self.legendLineEdit = QLineEdit()
        self.legendLineEdit.setText("<sample>")
        mainlayout = QGridLayout()
        mainlayout.addWidget(templab, 0, 0)
        mainlayout.addWidget(self.fomfmtLineEdit, 1, 0)
        mainlayout.addWidget(templab2, 0, 1)
        mainlayout.addWidget(self.compfmtLineEdit, 1, 1)
        mainlayout.addWidget(templab3, 2, 0, 1, 2)
        mainlayout.addWidget(self.legendLineEdit, 3, 0, 1, 2)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        mainlayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.buttonBox.accepted.connect(self.ExitRoutine)
        # QObject.connect(self.buttonBox,SIGNAL("rejected()"),self.ExitRoutineCancel)
        self.setLayout(mainlayout)
        self.resize(300, 250)
        self.selectinds = []

    def ExitRoutine(self):
        fomfmt = str(self.fomfmtLineEdit.text())
        compfmt = str(self.compfmtLineEdit.text())
        legendcmd = str(self.legendLineEdit.text())

        def genlegtext(
            sample,
            els,
            comp,
            code,
            fom,
            xy,
            fomfmt=fomfmt,
            compfmt=compfmt,
            legendcmd=legendcmd,
        ):
            legstr = legendcmd[:]
            for count, (n, ss, fmt) in enumerate(
                zip(
                    [fom, sample, code, xy[0], xy[1]],
                    ["<fom>", "<sample>", "<code>", "<x>", "<y>"],
                    [fomfmt, "%d", "%d", "%.2f", "%.2f"],
                )
            ):
                if n is None:
                    legstr = legstr.replace(ss, "")
                    continue
                s = fmt % n
                legstr = legstr.replace(ss, s)
            compusedandisnan = [
                numpy.isnan(c)
                for s, c in zip(["<a>", "<b>", "<c>", "<d>"], comp)
                if s in legstr
            ]
            if len(compusedandisnan) > 0 and not (
                True in compusedandisnan
            ):  # if list is empty then no compositions used in label so skip this. if there is a composition used in label then if e.g. the list is [True,False] skip because can't provide full compsotiion label but if [False,False] then proceed
                if "d" in compfmt:
                    compstr = [compfmt % int(round(c * 100.0)) for c in comp]
                else:
                    compstr = [compfmt % c for c in comp]
                for l, ssl in zip(
                    [els, compstr],
                    [["<A>", "<B>", "<C>", "<D>"], ["<a>", "<b>", "<c>", "<d>"]],
                ):
                    for s, ss in zip(l, ssl):
                        legstr = legstr.replace(ss, s)
            return legstr

        self.genlegfcn = genlegtext


class treeclass_anaexpfom:
    def __init__(self, tree, summarybrowser):
        self.treeWidget = tree
        self.summarybrowser = summarybrowser

    def initfilltree(self, expfiledict, anafiledict):
        self.treeWidget.clear()
        self.expwidgetItem = QTreeWidgetItem(["exp"], 0)
        self.set_allfilekeys = set([])
        self.filltree(
            expfiledict,
            self.expwidgetItem,
            startkey="exp_version",
            laststartswith="run__",
            expparent=True,
        )
        self.expwidgetItem.setExpanded(False)
        self.anawidgetItem = QTreeWidgetItem(["ana"], 0)
        if len(anafiledict) > 0:
            self.filltree(anafiledict, self.anawidgetItem)
            self.anawidgetItem.setExpanded(False)
        self.fomwidgetItem = QTreeWidgetItem(["fom"], 0)
        self.treeWidget.addTopLevelItem(self.expwidgetItem)
        self.treeWidget.addTopLevelItem(self.anawidgetItem)
        self.treeWidget.addTopLevelItem(self.fomwidgetItem)

    def appendexpfiles(self, d_appended):
        self.nestedfill(d_appended, self.expfileitem_forappend, prependstr="*")
        self.set_allfilekeys = self.set_allfilekeys.union(
            set(
                [
                    fk
                    for filed in d_appended.itervalues()
                    for fk in (filed["keys"] if "keys" in filed.keys() else [])
                ]
            )
        )

    def getusefombools(self):
        mainitem = self.fomwidgetItem
        l_usefombool = [
            bool(mainitem.child(i).checkState(0)) for i in range(mainitem.childCount())
        ]
        return l_usefombool

    def uncheckfoms(self):
        n = self.fomwidgetItem.childCount()
        for count in range(n):
            item = self.fomwidgetItem.child(count)
            item.setCheckState(0, Qt.Unchecked)

    def appendFom(
        self, fomnames, csvheaderdict, uncheckprevious=False, anak=None, anad=None
    ):
        i = self.fomwidgetItem.childCount()
        if uncheckprevious:
            self.uncheckfoms()
        fomlabel = "CSV%d" % (i + 1)
        mainitem = QTreeWidgetItem([fomlabel], 0)
        mainitem.setFlags(mainitem.flags() | Qt.ItemIsUserCheckable)
        mainitem.setCheckState(0, Qt.Checked)
        item = QTreeWidgetItem([",".join(fomnames)], 0)
        mainitem.addChild(item)
        item = QTreeWidgetItem(["csvheader"], 0)
        self.nestedfill(csvheaderdict, item, laststartswith="plot")
        mainitem.addChild(item)
        if not anak is None:
            item = QTreeWidgetItem([anak], 0)
            if not anad is None:
                self.nestedfill(
                    dict(
                        [(k, v) for k, v in anad.iteritems() if not isinstance(v, dict)]
                    ),
                    item,
                    laststartswith="xx",
                )
            mainitem.addChild(item)
        self.fomwidgetItem.addChild(mainitem)
        if not self.summarybrowser is None:
            summlines = [
                str(self.summarybrowser.toPlainText())
            ]  # adds lines onto self.SummaryTextBrowser (where self is visdataDialog) and since analysis can be done on the fly fom csvs must come last in the summary browser
            summlines += [
                "%s: %s; %s"
                % (fomlabel, anak if (not anak is None) else "", ",".join(fomnames))
            ]
            self.summarybrowser.setText("\n".join(summlines))

    def filltree(
        self,
        d,
        toplevelitem,
        startkey="ana_version",
        laststartswith="ana__",
        expparent=False,
    ):
        self.treeWidget.clear()
        # assume startkey is not for dict and laststatswith is dict
        mainitem = QTreeWidgetItem([": ".join([startkey, str(d[startkey])])], 0)
        toplevelitem.addChild(mainitem)
        for k in sorted(
            [k for k, v in d.iteritems() if k != startkey and not isinstance(v, dict)]
        ):
            mainitem = QTreeWidgetItem([": ".join([k, str(d[k])])], 0)
            toplevelitem.addChild(mainitem)
        for k in sorted(
            [
                k
                for k, v in d.iteritems()
                if not k.startswith(laststartswith) and isinstance(v, dict)
            ]
        ):
            mainitem = QTreeWidgetItem([k + ":"], 0)
            self.nestedfill(d[k], mainitem, expparent=expparent)
            toplevelitem.addChild(mainitem)
            mainitem.setExpanded(False)
        anakl = sort_dict_keys_by_counter(d, keystartswith=laststartswith)
        for k in anakl:
            mainitem = QTreeWidgetItem([k + ":"], 0)
            self.nestedfill(d[k], mainitem, expparent=expparent)
            toplevelitem.addChild(mainitem)
            mainitem.setExpanded(False)

    def nestedfill(
        self,
        d,
        parentitem,
        laststartswith="files_",
        prependstr="",
        skipkeys=["platemapdlist", "platemapsamples"],
        expparent=False,
    ):
        nondictkeys = sorted(
            [
                k
                for k, v in d.iteritems()
                if not isinstance(v, dict) and not k in skipkeys
            ]
        )
        for k in nondictkeys:
            item = QTreeWidgetItem([": ".join([prependstr + k, str(d[k])])], 0)
            parentitem.addChild(item)
        dictkeys1 = sorted(
            [
                k
                for k, v in d.iteritems()
                if not k.startswith(laststartswith)
                and isinstance(v, dict)
                and not k in skipkeys
            ]
        )
        for k in dictkeys1:
            item = QTreeWidgetItem([prependstr + k + ":"], 0)
            if k.endswith(
                "_files"
            ):  # find the last _files where filename keys are being added and if this is in .exp make this the place where filenames are appened. the intention is that for on-the-fly this will be the only run__ in exp
                self.set_allfilekeys = self.set_allfilekeys.union(
                    set(
                        [
                            fk
                            for filed in d[k].itervalues()
                            for fk in (filed["keys"] if "keys" in filed.keys() else [])
                        ]
                    )
                )
                # prepend this * to fielnames so they can be clicked and plotted. this inlcudes fom_files
                self.nestedfill(d[k], item, prependstr="*", expparent=expparent)
                #                while not parentitem.parent() is None:
                #                    parentitem=parentitem.parent()
                #                print parentitem==self.expwidgetItem, str(parentitem.text(0)), str(self.expwidgetItemtext(0))
                #                if parentitem==self.expwidgetItem:
                if expparent:
                    self.expfileitem_forappend = item
            else:
                self.nestedfill(d[k], item, expparent=expparent)
            parentitem.addChild(item)
        dictkeys2 = sorted(
            [k for k in d.keys() if k.startswith(laststartswith) and not k in skipkeys]
        )
        for k in dictkeys2:
            item = QTreeWidgetItem([prependstr + k + ":"], 0)
            self.nestedfill(d[k], item, expparent=expparent)
            parentitem.addChild(item)

    ###everything below here is copied and not necessarily needed in theis class def
    def createtxt(self, indent="    "):
        self.indent = indent
        return "\n".join(
            [
                self.createtxt_item(self.treeWidget.topLevelItem(count))
                for count in range(int(self.treeWidget.topLevelItemCount()))
            ]
        )

    def createtxt_item(self, item, indentlevel=0):
        str(item.text(0))
        itemstr = self.indent * indentlevel + str(item.text(0)).strip()
        if item.childCount() == 0:
            return itemstr
        childstr = "\n".join(
            [
                self.createtxt_item(item.child(i), indentlevel=indentlevel + 1)
                for i in range(item.childCount())
            ]
        )
        return "\n".join([itemstr, childstr])

    def partitionlineitem(self, item):
        s = str(item.text(0)).strip()
        a, b, c = s.partition(":")
        return (a.strip(), c.strip())

    def createdict(self):
        return dict(
            [
                self.createdict_item(self.treeWidget.topLevelItem(count))
                for count in range(int(self.treeWidget.topLevelItemCount()))
            ]
        )

    def createdict_item(self, item):
        tup = self.partitionlineitem(item)
        if item.childCount() == 0:
            return tup
        d = dict(
            [self.createdict_item(item.child(i)) for i in range(item.childCount())]
        )
        return (tup[0], d)
