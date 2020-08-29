# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 13:59:45 2016
@author: sksuram
"""
import os, sys, numpy as np, matplotlib.pyplot as plt, sys

sys.path.append(r"E:\GitHub\JCAPDataProcess\AuxPrograms")
from fcns_io import *
from DBPaths import *

sys.path.append(r"E:\GitHub\JCAPDataProcess\AnalysisFunctions")
sys.path.append(r"E:\python-codes\CALTECH\datahandling")
from Analysis_Master import *
from datamanipulation import *

xyfolder = r"K:\experiments\xrds\Lan\Oxynitride\30801_TaLaON_postRTP\pmpy24p3_line\integration\bkg_subtraction"
plateidstr = xyfolder.split(os.sep)[-4].split("_")[0][0:-1]
Normalize = 0.0
write_udi = 1
CompType = "random"  # options are 'random','calibrated','raw'
replace_xynan = False
replace_Int_lessthanzeros_val = 1e-05
replace_Int_lessthanzeros = True
add_fn_str = "_normalized" if Normalize else ""
udifl = os.path.join(xyfolder, r"udifl" + add_fn_str + ".txt")
fn = lambda x: os.path.join(xyfolder, x)
xyd = {}
wl_CuKa = 1.5406 * 0.1
replace_X_nan = 50.0
replace_Y_nan = 47.23
xyfiles = filter(
    lambda x: os.path.splitext(x)[-1] == ".xy", map(fn, os.listdir(xyfolder))
)
specinds = []
xarr = []
yarr = []
for xyind, xyfile in enumerate(xyfiles):
    bxyf = os.path.basename(xyfile).split(".xy")[0]
    xyfileinfo, xyd[xyind] = text2dict(
        xyfile,
        header_row=1,
        delimiter=" ",
        skip_footer=0,
        obscolnum=None,
        headerfromdata=False,
        header=["twoth", "Inte"],
    )
    xarr += [float(bxyf.split("pmpx")[-1].split("_")[0])]
    yarr += [float(bxyf.split("pmpy")[-1].split("_")[0])]
    if "specind" in bxyf:
        specinds += [int(bxyf.split("specind")[-1].split("_")[0])]
    else:
        specinds += [int(xyind)]
xarr = np.array(xarr)
yarr = np.array(yarr)
naninds_xarr = list(np.where(np.isnan(xarr))[0])
naninds_yarr = list(np.where(np.isnan(yarr))[0])
if replace_xynan:
    xarr[naninds_xarr] = replace_X_nan
    yarr[naninds_yarr] = replace_Y_nan
elif len(naninds_xarr) > 0 or len(naninds_yarr) > 0:
    raise ValueError("Nans exist for positions, no replacement values are provided")
infofiled = importinfo(plateidstr)
udi_dict = {}
udi_dict["ellabels"] = [
    x for x in getelements_plateidstr(plateidstr) if x not in ["", "O", "Ar", "N"]
]  # ,print_id=2 removed on 20161019 because no longer valid
udi_dict["X"] = xarr
udi_dict["Y"] = yarr
udi_dict["specind"] = specinds
udi_dict["sample_no"] = []
udi_dict["plate_id"] = [int(plateidstr)]
udi_dict["mX"] = np.ones(np.shape(udi_dict["X"])) * np.nan
udi_dict["mY"] = np.ones(np.shape(udi_dict["Y"])) * np.nan
getplatemappath_plateid(plateidstr)
pmap_path = getplatemappath_plateid(plateidstr)
pmpdl = readsingleplatemaptxt(pmap_path)
pmpx, pmpy, smplist = [
    [iter_d[fom] for iter_d in pmpdl] for fom in ["x", "y", "sample_no"]
]
udi_dict["sample_no"] = [
    smplist[
        np.argmin(
            (np.array(pmpx) - udi_dict["X"][row]) ** 2
            + (np.array(pmpy) - udi_dict["Y"][row]) ** 2
        )
    ]
    for row in xrange(np.shape(udi_dict["X"])[0])
]
intsn_twoth_range = np.arange(
    np.max([x["twoth"][0] for x in xyd.values()]),
    np.min([x["twoth"][-1] for x in xyd.values()]),
    0.005,
)
# intsn_twoth_range=np.arange(60.,np.min([x['twoth'][-1] for x in xyd.values()]),0.005)
for key in xyd.keys():
    xyd[key]["interp_Inte"] = np.interp(
        intsn_twoth_range, xyd[key]["twoth"], xyd[key]["Inte"]
    )
Qarr = (4 * np.pi * np.sin(np.radians(intsn_twoth_range / 2.0))) / (wl_CuKa)
Iarr = np.zeros([len(xyd.keys()), len(intsn_twoth_range)])
for idx, key in enumerate(sorted(xyd.keys())):
    Iarr[idx, :] = xyd[key]["interp_Inte"]
    if replace_Int_lessthanzeros:
        Iarr[idx, np.where(Iarr[idx, :] < 0)[0]] = replace_Int_lessthanzeros_val
if Normalize:
    for idx in xrange(np.shape(Iarr)[0]):
        Iarr[idx, :] = Iarr[idx, :] / np.max(Iarr[idx, :])
udi_dict["Iarr"] = Iarr
udi_dict["Q"] = Qarr
udi_dict["Normalize"] = False
if CompType == "random":
    udi_dict["CompType"] = CompType
    num_samples = len(xarr)
    comps = np.r_[[np.random.random(num_samples) for x in udi_dict["ellabels"]]].T
    sums = np.sum(comps, axis=1)
    udi_dict["comps"] = comps / np.tile(sums, (np.shape(comps)[1], 1)).T
if write_udi:
    writeudifile(udifl, udi_dict)
