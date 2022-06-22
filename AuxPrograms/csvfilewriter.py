import numpy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


def createcsvfilstr(
    fomdlist, fomkeys, intfomkeys=[], strfomkeys=[], fmt="%.5e"
):  # for each sample, if fom not available inserts NaN. Use to be datadlist with fomd as a key but now assume list of fomd
    smparr = [d["sample_no"] for d in fomdlist]
    fomarr_smps = numpy.array(
        [
            [(k in list(d.keys()) and (d[k],) or (numpy.nan,))[0] for k in fomkeys]
            for d in fomdlist
        ]
    )
    lines = [
        ",".join(
            ["%d" % smp]
            + ["%d" % d[nk] for nk in intfomkeys]
            + ["%s" % d[nk] for nk in strfomkeys]
            + [fmt % n for n in fomarr]
        )
        for smp, d, fomarr in zip(smparr, fomdlist, fomarr_smps)
    ]
    s = "\n".join(lines).replace("nan", "NaN").replace("inf", "NaN")
    s = "\n".join([",".join(["sample_no"] + intfomkeys + strfomkeys + fomkeys), s])
    return s


def createcsvfilstr_bare(
    fomdlist, fomkeys, intfomkeys=[], strfomkeys=[], fmt="%.5e", return_file_desc=False
):  # for each sample, if fom not available inserts NaN. Use to be datadlist with fomd as a key but now assume list of fomd
    if fomkeys is None:  # doesn't add Nan to missing foms like  createcsvfilstr does
        fomkeys = [
            k for k in list(fomdlist[0].keys()) if not (k in intfomkeys or k in strfomkeys)
        ]
    lines = [
        ",".join(
            ["%d" % d[nk] for nk in intfomkeys]
            + ["%s" % d[nk] for nk in strfomkeys]
            + [fmt % d[k] for k in fomkeys]
        )
        for d in fomdlist
    ]
    s = "\n".join(lines).replace("nan", "NaN").replace("inf", "NaN")
    s = "\n".join([",".join(intfomkeys + strfomkeys + fomkeys), s])
    if return_file_desc:
        file_desc = "csv_file;%s;1;%d" % (
            ",".join(intfomkeys + strfomkeys + fomkeys),
            len(lines),
        )
        return file_desc, s
    return s


class selectexportfom(QDialog):
    def __init__(
        self,
        parent,
        fomkeys,
        title="select FOMs to export. sample_no will be automatically included",
    ):
        super(selectexportfom, self).__init__(parent)
        self.setWindowTitle(title)
        self.parent = parent
        self.fomkeys = fomkeys
        vlayouts = []
        self.checkboxes = []
        for count, k in enumerate(fomkeys):
            if count % 10 == 0:
                vlayout = QVBoxLayout()
                vlayouts += [vlayout]
            cb = QCheckBox()
            cb.setText(k)
            if len(k) > 2 and not ("ample" in k or "x(mm)" in k or "y(mm)" in k):
                cb.setChecked(True)
            vlayout.addWidget(cb)
            self.checkboxes += [cb]
        mainlayout = QGridLayout()
        for count, l in enumerate(vlayouts):
            mainlayout.addLayout(l, 0, count)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        mainlayout.addWidget(self.buttonBox, min(10, len(self.checkboxes)), 0)
        self.buttonBox.accepted.connect(self.ExitRoutine)
        # QObject.connect(self.buttonBox,SIGNAL("rejected()"),self.ExitRoutineCancel)
        self.setLayout(mainlayout)
        # self.resize(300, 250)
        self.selectkeys = []

    def ExitRoutine(self):
        for cb, k in zip(self.checkboxes, self.fomkeys):
            if cb.isChecked():
                self.selectkeys += [k]
