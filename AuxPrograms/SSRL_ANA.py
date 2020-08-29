import os, numpy, time
import pandas as pd
import os, sys

projectroot = os.path.split(os.getcwd())[0]
sys.path.append(projectroot)
sys.path.append(os.path.join(projectroot, "AuxPrograms"))
sys.path.append(os.path.join(projectroot, "QtForms"))
sys.path.append(os.path.join(projectroot, "AuxPrograms"))
sys.path.append(os.path.join(projectroot, "OtherApps"))
sys.path.append(os.path.join(projectroot, "BatchProcesses"))
sys.path.append(os.path.join(projectroot, "AnalysisFunctions"))
# from fcns_math import *
from fcns_io import *
from fcns_ui import *

anapath = r"K:\users\helge.stein\20180108_CuPdZnAr_43557\processed"
exppath = r"K:\users\helge.stein\20180108_CuPdZnAr_43557\20170727.130926.done"
# create the proper ana numbers
runcount = 0
runk = "ana__%d" % (runcount + 1)
expdict = {}
expdict[runk] = {}
exprund = expdict[runk]
an_name = "Analysis__SSRL_batch_process"
multirun_ana_files = {an_name: []}
p_files = os.listdir(exppath)
shellfns = [fn for fn in p_files if not "." in fn]
shellfn = shellfns[0]
with open(os.path.join(exppath, shellfn), mode="r") as f:
    lines = f.readlines()
for l in lines:
    if l.startswith("#D"):
        ts = time.strptime(l[2:].strip(), "%a %b %d %H:%M:%S %Y")
        expdict["experiment_name"] = time.strftime("%Y%m%d.%H%M%S", ts)
    if l.startswith("#S"):
        scmd = l.partition("  ")[2].strip()
        if len(scmd) > 0:
            expdict["spec_command"] = scmd
csvfns = [fn for fn in p_files if fn.endswith(".csv")]
# h5path=os.path.join(os.path.join(p_processed, 'h5'), sysname+'.h5')
scan_csv = pd.read_csv(os.path.join(exppath, csvfns[0]), header=1)
xy_images = numpy.array(zip(scan_csv["   Plate X"], scan_csv["   Plate Y"]))
intens = numpy.array(scan_csv["       i0"])
imdir_files = os.listdir(exppath)
# integration block ---------------------------------------------------------------------------------
tk = "files_run__%d" % (runcount + 1)
int_fns = sorted([fn for fn in imdir_files if fn.endswith("ed.csv")])
rcpdict = {}
exprund[tk] = {}
rcpdict[tk] = {}
exprund[tk]["plate_ids"] = shellfn[0:4]
exprund[tk]["technique"] = "ssrl"
exprund[tk]["name"] = "Analysis__SSRL_Integrate"
exprund[tk]["ssrl_csv_pattern_file"] = {}
rcpdict[tk]["ssrl_csv_pattern_file"] = {}
itegrd = (rcpdict[tk]["ssrl_csv_pattern_file"], exprund[tk]["ssrl_csv_pattern_file"])
# fixme!!!
sample_nos = [i + 1 for i in range(len(int_fns))]
rows = sum(1 for line in open(os.path.join(anapath, int_fns[0])))
add_integr_file = lambda fn, sample_no: [
    d.update(
        {
            fn: filed_createflatfiledesc(
                {
                    "file_type": "ssrl_csv_pattern_file",
                    "sample_no": sample_no,
                    "num_header_lines": 1,
                    "num_data_rows": rows - 1,
                    "keys": ["q.nm,intensity.counts"],
                }
            )
        }
    )
    for d in itegrd
]
for fni, sample_no in zip(int_fns, sample_nos):
    add_integr_file(fni, sample_no)
# increase the run number ----------------
runcount += 1
runk = "ana__%d" % (runcount + 1)
expdict[runk] = {}
exprund = expdict[runk]
# processing block ---------------------------------------------------------------------------------
tk = "files_run__%d" % (runcount + 1)
tif_fns = sorted([fn for fn in imdir_files if fn.endswith(".npy")])
exprund[tk] = {}
rcpdict[tk] = {}
exprund[tk]["plate_ids"] = shellfn[0:4]
exprund[tk]["technique"] = "ssrl"
exprund[tk]["name"] = "Analysis__SSRL_Qchi"
exprund[tk]["ssrl_qchi_npy_file"] = {}
rcpdict[tk]["ssrl_qchi_npy_file"] = {}
procd = (rcpdict[tk]["ssrl_qchi_npy_file"], exprund[tk]["ssrl_qchi_npy_file"])
add_proc_file = lambda fn, sample_no: [
    d.update(
        {
            fn: filed_createflatfiledesc(
                {"file_type": "ssrl_qchi_npy_file", "sample_no": sample_no}
            )
        }
    )
    for d in procd
]
for fnp, sample_no in zip(tif_fns, sample_nos):
    add_proc_file(fnp, sample_no)
# add this to file?
pck2dvalsfn = "pck2d_chi_q_vals.pck"
pck2dvalsp = os.path.join(anapath, pck2dvalsfn)
access = "hte"
expdict["run_ids"] = "letest"
expdict["plate_ids"] = shellfn[0:4]
expdict["ana_version"] = 4
expdict["created_by"] = "ssrl"
expdict[
    "description"
] = "Analysis__SSRL_Qchi,Analysis__SSRL_Integrate on plate_id {}".format(
    expdict["plate_ids"]
)
expdict["analysis_type"] = "ssrl"
expdict["access"] = access
expdict["experiment_path"] = os.path.join(
    os.path.split(anapath)[1], expdict["experiment_name"]
)
calibfn = sorted([fn for fn in imdir_files if fn.endswith(".calib")])
expdict["calibfn"] = calibfn[0]
print strrep_filedict(expdict)
