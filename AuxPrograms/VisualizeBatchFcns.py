# import time
# import shutil
import os, os.path

# import sys
# import numpy
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# import operator
# import pylab
from fcns_math import *
from fcns_io import *
from fcns_ui import *


def batch_plotuvisrefs_R(self):
    return batch_plotuvisrefs(self, tech="R_UVVIS")


def batch_plotuvisrefs(self, tech="T_UVVIS"):
    if choosexyykeys(self, ["Wavelength (nm)", "Signal_0"]):
        return True
    self.overlayselectCheckBox.setChecked(False)
    self.customlegendfcn = lambda sample, els, comp, code, fom: ""
    self.xyplotstyled = dict({}, marker=".", ms=0, c="b", ls="-", lw=0.5)
    runkl = [
        runk
        for runk in self.sorted_ana_exp_keys(ana=False)
        if "run_use" in self.expfiledict[runk].keys()
        and self.expfiledict[runk]["run_use"] == "ref_light"
    ]
    for runk in runkl:
        filetupl = [
            tup
            for td in [
                techd
                for techk, techd in self.expfiledict[runk].iteritems()
                if tech in techk
            ]
            for tup in td["spectrum_files"].items()
        ]
        for fn, filed in filetupl:
            ans = buildrunpath_selectfile(
                fn,
                self.expfolder,
                runp=self.expfiledict[runk]["run_path"],
                expzipclass=self.expzipclass,
                returnzipclass=True,
            )
            if ans is None:
                continue
            p, zipclass = ans
            filed = copy.copy(filed)
            filed["path"] = p
            filed["zipclass"] = zipclass
            self.plotxy(filed=filed)
            self.overlayselectCheckBox.setChecked(True)
    self.xyplotstyled = dict({}, marker=".", ms=0, c="b", ls=":", lw=0.5)
    runkl = [
        runk
        for runk in self.sorted_ana_exp_keys(ana=False)
        if "run_use" in self.expfiledict[runk].keys()
        and self.expfiledict[runk]["run_use"] == "ref_dark"
    ]
    for runk in runkl:
        filetupl = [
            tup
            for td in [
                techd
                for techk, techd in self.expfiledict[runk].iteritems()
                if tech in techk
            ]
            for tup in td["spectrum_files"].items()
        ]
        for fn, filed in filetupl:
            ans = buildrunpath_selectfile(
                fn,
                self.expfolder,
                runp=self.expfiledict[runk]["run_path"],
                expzipclass=self.expzipclass,
                returnzipclass=True,
            )
            if ans is None:
                continue
            p, zipclass = ans
            filed = copy.copy(filed)
            filed["path"] = p
            filed["zipclass"] = zipclass
            self.plotxy(filed=filed)
    self.overlayselectCheckBox.setChecked(True)
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
    return False


def batch_ramanavesetup(self):
    if choosexyykeys(self, ["wavenumbers", "spectrum_ave"]):
        return True
    self.createfilenamefilter(filterstr="ave")
    self.filterandplotfomdata()
    self.addallsamples()


def choosexyykeys(self, xyykeys):
    cbl = [
        self.xplotchoiceComboBox,
        self.yplotchoiceComboBox,
        self.rightyplotchoiceComboBox,
    ]
    for cb, k in zip(cbl, xyykeys):
        arrkeys = [str(cb.itemText(i)) for i in range(int(cb.count()))]
        if not k in arrkeys:
            return True
        cb.setCurrentIndex(arrkeys.index(k))
    return False


BatchFcnList = [batch_plotuvisrefs, batch_plotuvisrefs_R, batch_ramanavesetup]
BatchDescList = [
    "Plot T ref_dark and ref_light",
    "Plot R ref_dark and ref_light",
    "Setup for Raman ave plotting",
]
