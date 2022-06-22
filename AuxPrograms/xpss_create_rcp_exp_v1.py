import string, copy

# import time
import os, os.path  # , shutil
import sys
import numpy

# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
import operator
import numpy as np

projectpath = os.path.split(os.path.abspath(__file__))[0]
sys.path.append(os.path.join(projectpath, "AuxPrograms"))
from fcns_math import *
from fcns_io import *
from fcns_ui import *


class setup_rcp_and_exp_xpss:
    def __init__(
        self,
        import_path,
        rcpext=".done",
        expext=".done",
        overwrite_runs=False,
        plate_idstr=None,
        access="hte",
        pmidstr=None,
        sample_no_from_position_index=lambda i: (1 + i),
        testmode=False,
    ):
        """
        the xpss data should be saved so that once import_path is given, this class knows what to do to copy and name all rcp and exp files
        rcpext and expext should be set to .run for testing and then in standard operation can make them .done
        overwrite_runs can be set to True to help with debugging but safer to keep as False in case there is a mistkae, really overwrite of a .done run is not allowed but this is not checked
        plate_idstr should be auto read but passing the string here overrides that
        access for the data is set here and can be public,hte,tri,muri
        pmidstr will be auto read from the .info file but if for some reason the platempa used for xps is different this value can be overridden, which is dangerous but the sample_no generated for the .rcp/.exp must correspond to the pmidstr
        sample_no_from_position_index should either be aq list of all the sample_no in the order they were measured, or a lambda function like the default value above when the sample_no were measured in order
        """
        self.access = access
        self.pmidstr = pmidstr
        self.import_path = import_path
        self.sample_no_from_position_index = sample_no_from_position_index
        self.plate_idstr = plate_idstr
        self.parse_spec_files()
        self.datatype = "xpss"
        self.rcpext = rcpext
        self.expext = expext
        iserror = self.setup_folders(overwrite_runs)
        if iserror:
            return
        self.setup_file_dicts()
        self.add_all_files()
        self.save_rcp_exp(testmode)

    def setup_folders(self, overwrite_runs=True):
        if self.pmidstr is None:
            ans = getplatemappath_plateid(
                self.plate_idstr,
                erroruifcn=None,
                infokey="screening_map_id:",
                return_pmidstr=True,
            )
            if ans is None:
                print("aborting because failed retrieval of platemap id for plate :", self.plate_idstr)
                return True
            self.pmidstr = ans[1]
        dropfolder = getdropfolder_exptype(self.datatype)
        if dropfolder is None:
            # messageDialog(None, 'Aborting SAVE because cannot find drop folder').exec_()
            print("Aborting SAVE because cannot find drop folder")
            return True
        if not os.path.isdir(dropfolder):
            os.mkdir(dropfolder)
        ellist = getelements_plateidstr(self.plate_idstr)
        rcplab = "".join(ellist)
        self.rcpmainfoldname = "_".join(
            [timestampname()[:8], rcplab, get_serial_plate_id(self.plate_idstr)]
        )
        rcpmainfolder = os.path.join(dropfolder, self.rcpmainfoldname)
        if not os.path.isdir(rcpmainfolder):
            os.mkdir(rcpmainfolder)
        self.runfolderpath = os.path.join(
            rcpmainfolder, self.data_acquisition_timestamp + self.rcpext
        )
        if os.path.isdir(self.runfolderpath):
            if overwrite_runs:
                shutil.rmtree(self.runfolderpath)
            else:
                # messageDialog(None, 'Aborting SAVE because %s folder exists' %rcpmainfolder).exec_()
                print("Aborting SAVE because %s folder exists" % rcpmainfolder)
                return True
        os.mkdir(self.runfolderpath)
        return False

    def parse_spec_files(self):
        # using self.import_path
        # TODO: Helge put parsing code here and define plate_idstr and technique_names. Ideally plate_id is somehow read from the folder or a file (user types it in when data collected instead of now)
        if (
            self.plate_idstr is None
        ):  # ideally plate_id is read from the filename or spec file because it was entered by user when starting data acquisition, but if it was passed in the class init then ignore
            self.plate_idstr = "4082"
        self.technique_names = ["XPSSNAPSHOT-Mn2p", "XPSSNAPSHOT-Fe2p"]
        self.data_acquisition_timestamp = "20170101.010101"  # if you read timestamp from the xps image file using time module, which produces a tuple, then convert it to this format using time.strftime('%Y%m%d.%H%M%S',tuple)
        self.run_params_dict = (
            {}
        )  # flat dictionary where the values can be numeric or strings where illegal characters will be removed. The parameters are probably from the spec file since these params apply to all data being imported
        self.run_params_dict[
            "technique_names"
        ] = (
            self.technique_names
        )  # if there are parameters like starting binding energy that shoudl be saved for each technique, make the dict value a list of the param values assumed to be in the same order as technique_names

    def setup_file_dicts(self):
        self.expdict = {}
        self.expdict["experiment_type"] = self.datatype
        self.expdict["exp_version"] = "3"
        self.expdict["description"] = "%s run on plate_id %s with %s" % (
            self.datatype,
            self.plate_idstr,
            ",".join(self.technique_names),
        )
        self.expdict["created_by"] = self.datatype
        self.expdict["access"] = self.access
        runcount = 0
        runk = "run__%d" % (runcount + 1)
        self.expdict[runk] = {}
        exprund = self.expdict[runk]
        self.rcpdict = {}
        rcpdict = self.rcpdict
        rcpdict["experiment_type"] = self.datatype
        rcpdict[
            "technique_name"
        ] = (
            self.datatype
        )  # don't pay attention to this "technique_name" it is an artifact of previous data and does not have the same meaning as e.g. XPSSURVEY
        rcpdict["rcp_version"] = "2"
        self.add_run_attr = lambda k, v: [d.update({k: v}) for d in [exprund, rcpdict]]
        self.add_run_attr("screening_map_id", self.pmidstr)
        self.add_run_attr("run_use", "data")
        self.add_run_attr("plate_id", self.plate_idstr)
        self.add_run_attr("name", self.data_acquisition_timestamp)
        compname = "HTE-XPSS-01"
        self.add_run_attr("computer_name", compname)
        exprund["run_path"] = r"/%s/%s/%s/%s" % (
            self.datatype,
            compname.lower(),
            self.rcpmainfoldname,
            rcpdict["name"] + self.rcpext,
        )
        exprund["rcp_file"] = rcpdict["name"] + ".rcp"
        rcpdict["parameters"] = {}
        exprund["parameters"] = {}
        self.add_run_param = lambda k, v: [
            d.update({k: v}) for d in [exprund["parameters"], rcpdict["parameters"]]
        ]
        self.add_run_param("plate_id", self.plate_idstr)
        for k, v in self.run_params_dict.items():
            v = (
                strrep_generic_file_dict_value(v).strip("[").rstrip("]")
            )  # make lists comma delimited but without the brackets
            self.add_run_param(k, v)
        techdlist = []
        for count, tech in enumerate(["XPSS"] + self.technique_names):
            tk = "files_technique__%s" % tech
            exprund[tk] = {}
            rcpdict[tk] = {}
            if count == 0:
                exprund[tk]["kratos_files"] = {}
                rcpdict[tk]["kratos_files"] = {}
                xpsstechd = (rcpdict[tk]["kratos_files"], exprund[tk]["kratos_files"])
            else:
                exprund[tk]["pattern_files"] = {}
                rcpdict[tk]["pattern_files"] = {}
                techdlist += [
                    (rcpdict[tk]["pattern_files"], exprund[tk]["pattern_files"])
                ]
        self.add_kratos_file = lambda fn: [
            d.update({fn: filed_createflatfiledesc({"file_type": "xpss_kratos_file"})})
            for d in xpsstechd
        ]
        # self.add_meta_file=lambda fn:[d.update({fn:filed_createflatfiledesc({'file_type':'xpss_kratos_file'})}) for d in xpsstechd]
        self.pattern_file_keys = ["BE(eV)", "Intensity"]
        self.add_pattern_file = lambda tech, fn, nrows, sample_no: [
            d.update(
                {
                    fn: filed_createflatfiledesc(
                        {
                            "file_type": "xpss_spectrum_csv",
                            "keys": self.pattern_file_keys,
                            "num_header_lines": 1,
                            "num_data_rows": nrows,
                            "sample_no": sample_no,
                        }
                    )
                }
            )
            for d in techdlist[self.technique_names.index(tech)]
        ]

    def save_rcp_exp(self, testmode):
        rcpfilestr = strrep_filedict(self.rcpdict)
        p = os.path.join(self.runfolderpath, self.rcpdict["name"] + ".rcp")
        if testmode:
            print("THIS IS THE RCP FILE THAT WOULD BE SAVED:")
            print(rcpfilestr)
            return
        with open(p, mode="w") as f:
            f.write(rcpfilestr)
        print("rcp file saved to ", p)
        saveexpfiledict, dsavep = saveexp_txt_dat(
            self.expdict,
            saverawdat=False,
            experiment_type=self.datatype,
            rundone=self.expext,
            file_attr_and_existence_check=False,
        )
        print("exp file saved to ", dsavep)

    def add_all_files(self):
        self.import_path  # this path should be all that's necessary to
        position_index_of_file_index = lambda fi: fi // len(self.technique_names)
        sample_no_of_file_index = (
            lambda fi: self.sample_no_from_position_index[
                position_index_of_file_index[position_index_of_file_index(fi)]
            ]
            if isinstance(self.sample_no_from_position_index, list)
            else self.sample_no_from_position_index(position_index_of_file_index(fi))
        )
        """
        TODO
        for each file that kratos produces copy the file to self.runfolderpath and run this to add it to the rcp
        self.add_kratos_file(fn)
        for each pattern file,  sample_no_of_file_index() should work for determining the sample_no as a function of the file index, or "ID" in your existing meta.csv file
        add as the first line of the .csv ','.join(self.pattern_file_keys)
        then for adding the file to the rcp and exp call this function where the arguments are the string technique name you generated in spec parsing, the filename you generate here,  the number of data rows there are in the file (data points),  and the sample_no
        self.add_pattern_file(tech, fn, nrows, sample_no)
        you save the files into self.runfolderpath as you call this function
        I'm not sure we need the meta .csv. are we ever going to do something with those x,y,z positions. Since the startE is the same for every sample these should be added to self.run_params_dict (see above note)
        below is dummy code to demo how this works
            """
        kratosfn = "testfilefromkratos.dat"
        fns = ["file%d.csv" % i for i in range(6)]
        self.add_kratos_file(kratosfn)
        for fileindex, fn in enumerate(fns):
            sample_no = sample_no_of_file_index(fileindex)
            tech = self.technique_names[fileindex % len(self.technique_names)]
            self.add_pattern_file(tech, fn, 77, sample_no)


xpsimportclass = setup_rcp_and_exp_xpss(
    "",
    rcpext=".run",
    expext=".run",
    overwrite_runs=True,
    plate_idstr=None,
    access="tri",
    pmidstr=None,
    sample_no_from_position_index=lambda i: (1 + i),
    testmode=True,
)
