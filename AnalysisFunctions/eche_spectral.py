import numpy, copy, sys, os

if __name__ == "__main__":
    sys.path.append(os.path.split(os.getcwd())[0])
sys.path.append(
    os.path.join(
        os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], "AuxPrograms"
    )
)
array_folder = os.path.join(
    os.path.split(os.path.split(os.path.realpath(__file__))[0])[0],
    "static_analysis_arrays",
)
from fcns_math import *
from fcns_io import *
from csvfilewriter import createcsvfilstr
from Analysis_Master import *

# import matplotlib.pyplot as plt
# this take a filedlist based on required keys in raw data and then finds samples where a required prior analysis was completed and encodes the path to the intermediate data in anadict
def ECHEPHOTO_checkcompletedanalysis_files_by_sample(
    filedlist,
    expfiledict,
    anadict,
    requiredanalysis="Analysis__Iphoto",
    tech=None,
    gui_mode_bool=False,
):
    anak_ftklist = [
        (anak, [ftk for ftk in anav.keys() if "files_run__" in ftk])
        for anak, anav in anadict.iteritems()
        if anak.startswith("ana__")
        and anav["name"] == requiredanalysis
        and True in ["files_run__" in ftk for ftk in anav.keys()]
    ]
    if len(tech) > 0:
        # if tech=None then don't filter by technique. otherwise only require first 2 characters to be the same so CA1 can be combined with CA4 but not CV4
        anak_ftklist = [
            (anak, ftkl)
            for anak, ftkl in anak_ftklist
            if tech is None or anadict[anak]["technique"][:2] == tech[:2]
        ]
    if len(anak_ftklist) == 0:
        return []
    # goes through all inter_files in all analyses and matches run and sample_no . This could include multiple analysis on different runs but if anlaysis done multiple times with different parameters, all of them will be included
    ## sample_no is matched so this implies that the plate_id is match
    # this used to use [anak, ftk, typek, fnk] but anadict is not available in perform() so use filename because it is the same .ana so should be in same folder
    # if smaple number matched in inter_files then presumably the sample_no is in the fom_files so capture fom_files infor for each interfnk dict
    genfomdlist = lambda anad: [
        dict(
            {},
            fn=fnk,
            num_header_lines=int(tagandkeys.split(";")[2]),
            keys=tagandkeys.split(";")[1].split(","),
        )
        for fnk, tagandkeys in anad["files_multi_run"]["fom_files"].iteritems()
    ]
    interfnks_filedlist = [
        [
            dict(
                {},
                anakeys=[anak, ftk, typek, fnk],
                anak=anak,
                fn=fnk,
                runk=ftk[6:],
                sample_no=filed["sample_no"],
                nkeys=len(tagandkeys.split(";")[1].split(",")),
                num_header_lines=int(tagandkeys.split(";")[2]),
                keys=tagandkeys.split(";")[1].split(","),
                fom_files_dlist=genfomdlist(anadict[anak]),
            )
            for anak, ftkl in anak_ftklist
            for ftk in ftkl
            for typek in ["inter_files"]
            for fnk, tagandkeys in anadict[anak][ftk][typek].iteritems()
            if int(tagandkeys.split(";")[4].strip()) == filed["sample_no"]
        ]
        for filed in filedlist
    ]
    if not True in [len(dlist) > 0 for dlist in interfnks_filedlist]:
        return []
    for dlist in interfnks_filedlist:
        for d in dlist:
            echemparamsk = "echem_params__" + anadict[d["anak"]]["technique"]
            runk = d["runk"]
            if (
                "user_run_foms" in expfiledict[runk].keys()
                and "user_fom_led_wavelength"
                in expfiledict[runk]["user_run_foms"].keys()
            ):  # user can override wavelength but presently no other params taken from here
                d["illumination_wavelength"] = float(
                    expfiledict[runk]["user_run_foms"]["user_fom_led_wavelength"]
                )
            elif (
                (
                    not False
                    in [
                        k in expfiledict[runk]["parameters"].keys()
                        for k in [
                            "illumination_wavelength",
                            "toggle_value_illumination",
                            echemparamsk,
                        ]
                    ]
                )
                and "toggle_value"
                in expfiledict[runk]["parameters"][echemparamsk].keys()
            ):
                togvallist = expfiledict[runk]["parameters"][
                    "toggle_value_illumination"
                ]
                if isinstance(togvallist, str) and "," in togvallist:
                    togvals = [s.strip() for s in togvallist.strip().split(",")]
                    tv = expfiledict[runk]["parameters"][echemparamsk]["toggle_value"]
                    tv = tv.strip() if isinstance(tv, str) else ("%d" % tv)
                    toglistind = togvals.index(tv)
                    d["toglistind"] = toglistind
                    for k, v in expfiledict[runk]["parameters"].iteritems():
                        if not (k.startswith("illumination_") and "," in v):
                            continue
                        d[k] = attemptnumericconversion_tryintfloat(
                            v.split(",")[toglistind].strip()
                        )
                else:
                    for k, v in expfiledict[runk]["parameters"].iteritems():
                        if not k.startswith("illumination_") and isinstance(
                            v, (int, float)
                        ):
                            continue
                        d[k] = v
    interfnks_filedlist = [
        [d for d in dlist if "illumination_wavelength" in d.keys()]
        for dlist in interfnks_filedlist
    ]
    # the key ana__inter_filedlist gives the above list of inter_files from the right type of ana__ with matched run and sample
    filedlist2 = [
        dict(filed, ana__inter_filedlist=interfiledlist)
        for filed, interfiledlist in zip(filedlist, interfnks_filedlist)
        if len(interfiledlist) > 0
    ]
    return filedlist2  # inside of each filed are key lists ana__inter_filed and ana__inter_rawlen_filed that provide the path through anadict to get to the fn that mathces the fn in filed


class Analysis__SpectralPhoto(Analysis_Master_inter):
    def __init__(self):
        self.analysis_fcn_version = "3"
        self.dfltparams = dict(
            [
                ("photo_analysis_ana_fcn", "Analysis__Iphoto"),
                ("optical_power_mw", "illumination_intensity"),
                ("spectral_integral_fom_file", "am15g"),
                ("spectral_integral_fom_keys", "irrad.mW_cm2_nm,flux.mA_cm2_nm"),
                ("spectral_integral_below_above_vals", "const,0."),
            ]
        )
        self.params = copy.copy(self.dfltparams)
        self.analysis_name = "Analysis__SpectralPhoto"
        # assume intermediate and raw data available
        self.requiredkeys = [
            "t(s)"
        ]  # , 't(s)_dark', 'Ewe(V)_dark', 'I(A)_dark', 't(s)_ill', 'Ewe(V)_ill', 'I(A)_ill', 'IllumBool']#these intermediate keys are not tested for explicitly, ontly through the custom getapplicablefilenames below
        self.optionalkeys = []
        self.requiredparams = [
            "illumination_wavelength",
            "toggle_value_illumination",
            "echem_params__",
        ]
        # Voc is almost always extrapolated, Vmicro will require i_photo_base parameter from previous analysis of Iphotomin_in_range
        self.fomnames = ["num_wavelengths"]
        # self.fomnames=['E.eV_illum', 'wl.nm_illum']
        self.plotparams = dict({}, plot__1={})
        self.plotparams["plot__1"]["x_axis"] = "t(s)"
        self.plotparams["plot__1"]["series__1"] = "I(A)"
        self.csvheaderdict = dict({}, csv_version="1", plot_parameters={})
        self.csvheaderdict["plot_parameters"]["plot__1"] = dict(
            {},
            fom_name="num_wavelengths",
            colormap="jet",
            colormap_over_color="(0.5,0.,0.)",
            colormap_under_color="(0.,0.,0.)",
        )

    # this is the default fcn but with requiredkeys changed to relfect user-entered illum key
    # def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
    #     self.requiredkeys[-1]=self.params['illum_key']
    #     self.num_files_considered, self.filedlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys)
    #     self.description='%s on %s' %(','.join(self.fomnames), techk)
    #     return self.filedlist
    def getgeneraltype(self):  # make this fucntion so it is inhereted
        return "analysis_of_ana"

    def getapplicablefilenames(
        self,
        expfiledict,
        usek,
        techk,
        typek,
        runklist=None,
        anadict=None,
        calcFOMDialogclass=None,
    ):
        self.num_files_considered, self.filedlist = stdgetapplicablefilenames(
            expfiledict,
            usek,
            techk,
            typek,
            runklist=runklist,
            requiredkeys=self.requiredkeys,
            requiredparams=self.requiredparams,
        )
        # this is the only place that require dprevious analysis is specified. It is assumed that if this analysis complete and files are present, we know that certain keys exist without explicitely testing for them
        self.filedlist = ECHEPHOTO_checkcompletedanalysis_files_by_sample(
            self.filedlist,
            expfiledict,
            anadict,
            requiredanalysis=self.params["photo_analysis_ana_fcn"],
            tech=techk,
            gui_mode_bool=self.gui_mode_bool,
        )
        self.description = "%s on %s" % (",".join(self.fomnames), techk)
        return self.filedlist

    def perform(
        self,
        destfolder,
        expdatfolder=None,
        writeinterdat=True,
        anak="",
        zipclass=None,
        anauserfomd={},
        expfiledict=None,
    ):
        if destfolder is None:
            return
        self.initfiledicts(runfilekeys=[])
        self.multirunfiledict["sample_vector_files"] = {}
        mwparam = self.params["optical_power_mw"].strip()
        if len(mwparam) == 0:
            genmw = None
        elif "," in self.params["optical_power_mw"]:
            mwvals = [float(s) for s in mwparam.split(",")]
            genmw = (
                lambda d: mwvals[d["toglistind"]]
                if "toglistind" in d.keys()
                else numpy.nan
            )
        elif isinstance(attemptnumericconversion_tryintfloat(mwparam), (float, int)):
            genmw = lambda d: float(attemptnumericconversion_tryintfloat(mwparam))
        else:  # key from interd oarams
            genmw = lambda d: d[mwparam] if mwparam in d.keys() else numpy.nan
        spectrum_path = None
        if (
            self.params["spectral_integral_fom_file"] != "None"
        ):  # this is list of file startswith and then keys so if no comma then skip, ie. "None" as a value will skip this calculation
            integral_wlkey = "wl.nm"
            l = self.params["spectral_integral_fom_keys"].split(",")
            spectrum_integral_keys = [v.strip() for v in l]
            file_start_str = self.params["spectral_integral_fom_file"]
            for fn in os.listdir(array_folder):
                if fn.startswith(file_start_str) and fn.endswith(".csv"):
                    p = os.path.join(array_folder, fn)
                    specd_headerdict = {"num_header_lines": 1}
                    specd = readcsvdict(p, specd_headerdict)
                    if not (
                        False
                        in [
                            k in specd.keys()
                            for k in [integral_wlkey] + spectrum_integral_keys
                        ]
                    ):
                        spectrum_path = p
                        inds = numpy.argsort(specd[integral_wlkey])
                        for k, v in specd.items():
                            specd[k] = v[inds]
                        limfcns = []
                        for count, limvalstr in enumerate(
                            self.params["spectral_integral_below_above_vals"].split(",")
                        ):
                            limvalstr = attemptnumericconversion_tryintfloat(limvalstr)
                            if isinstance(limvalstr, str):
                                if limvalstr != "const":
                                    print "unknown limit parameter"
                                    raiseerror
                                limfcns += [lambda l: l[0 if count == 0 else -1]]
                            else:
                                limfcns += [lambda l: float(limvalstr)]
                        break
        self.fomdlist = []
        for filed in self.filedlist:
            if numpy.isnan(filed["sample_no"]):
                if self.debugmode:
                    raiseTEMP
                continue
            photofomd_wl = {}
            interdlist = filed["ana__inter_filedlist"]
            fomkeyset = set([])
            for interd in interdlist:
                wl = interd["illumination_wavelength"]
                wlk = int(wl)
                photofomd_wl[
                    wlk
                ] = (
                    {}
                )  # if ana__ data for multiple waqvelengths overwrite will happen here
                photofomd = photofomd_wl[wlk]
                for fomfiled in interd["fom_files_dlist"]:
                    fomd = readcsvdict(
                        os.path.join(destfolder, fomfiled["fn"]),
                        fomfiled,
                        returnheaderdict=False,
                        zipclass=None,
                        includestrvals=False,
                    )
                    if not filed["sample_no"] in list(fomd["sample_no"]):
                        continue
                    fomind = list(fomd["sample_no"]).index(
                        filed["sample_no"]
                    )  # assumption that sample_no is in the fom csv fiel is from the fiel matching above that finds sample_no from the inter_files within this ana__
                    photofomd.update(
                        [(k, v[fomind]) for k, v in fomd.iteritems() if "photo" in k]
                    )
                fomkeyset = fomkeyset.union(photofomd.keys())  # only the photokeys
                if not genmw is None:
                    photofomd["P.mW_illum"] = genmw(interd)
                photofomd["WL.nm_illum"] = wl
                photofomd["E.eV_illum"] = 1239.8 / wl
                photofomd["runint"] = int(interd["runk"].partition("run__")[2])
                photofomd["anaint"] = int(interd["anak"].partition("ana__")[2])
                photofomd["sample_no"] = filed[
                    "sample_no"
                ]  # sample_no is needed for csv but does not count as a
            for wlk, photofomd in photofomd_wl.iteritems():
                # fill in any missing foms for each wavelength
                for k in list(fomkeyset.difference(set(photofomd.keys()))):
                    photofomd[k] = numpy.nan
                # eqe calcualtion if possible
                if "I.A_photo" in photofomd.keys() and "P.mW_illum" in photofomd.keys():
                    iph = photofomd["I.A_photo"]
                    wl = photofomd["WL.nm_illum"]
                    pmw = photofomd["P.mW_illum"]
                    photofomd["EQE"] = (
                        1.2398e6 * iph / (wl * pmw)
                    )  # the constant is hc/e in units of mW nm / A
            floatkeys = (
                ["E.eV_illum", "WL.nm_illum"]
                + ([k for k in ["P.mW_illum", "EQE"] if k in photofomd.keys()])
                + list(fomkeyset)
            )
            intkeys = ["runint", "anaint"]
            num_wavelengths = len(photofomd_wl.keys())
            sortedwls = sorted(photofomd_wl.keys())
            wl_dlist = [
                photofomd_wl[k] for k in sortedwls[::-1]
            ]  # inverse sorting for the spectralfoms files
            fn = "%s__%s-%d.csv" % (
                anak,
                "spectralfoms",
                filed["sample_no"],
            )  # name file by foms but onyl inlcude the 1st 3 to avoid long names
            csvfilstr = createcsvfilstr(
                wl_dlist, floatkeys, intfomkeys=intkeys
            )  # , fn=fnf)
            allnames = (
                ["sample_no"] + intkeys + floatkeys
            )  # this is the order in createcsvfilstr
            p = os.path.join(destfolder, fn)
            totnumheadlines = writecsv_smpfomd(p, csvfilstr, headerdict={})
            self.multirunfiledict["sample_vector_files"][fn] = "%s;%s;%d;%d;%d" % (
                "csv_sample_file",
                ",".join(allnames),
                totnumheadlines,
                len(wl_dlist),
                filed["sample_no"],
            )
            integral_fom_tups = []
            if not spectrum_path is None:
                x = numpy.float64([photofomd_wl[k]["WL.nm_illum"] for k in sortedwls])
                y = numpy.float64([photofomd_wl[k]["EQE"] for k in sortedwls])
                x = x[numpy.logical_not(numpy.isnan(y))]
                y = y[numpy.logical_not(numpy.isnan(y))]
                for k in spectrum_integral_keys:
                    if len(y) == 0:
                        integral_fom = numpy.nan
                    else:
                        integral_fom = integrate_spectrum_with_piecewise_weights(
                            specd[integral_wlkey],
                            specd[k],
                            x,
                            y,
                            below_val=limfcns[0](y),
                            above_val=limfcns[1](y),
                        )
                    k2 = "SpectralInt." + k
                    integral_fom_tups += [(k2, integral_fom)]
            # now update the official fomdlist which has only the number of wavelength  points
            self.fomdlist += [
                dict(
                    [(self.fomnames[0], num_wavelengths)] + integral_fom_tups,
                    sample_no=filed["sample_no"],
                    plate_id=filed["plate_id"],
                    run=filed["run"],
                    runint=int(filed["run"].partition("run__")[2]),
                )
            ]
        if not spectrum_path is None:
            self.fomnames += [k for k, v in integral_fom_tups]
            specfn = os.path.split(spectrum_path)[1]
            newfn = "%s__%s" % (anak, specfn)
            destp = os.path.join(destfolder, newfn)
            shutil.copy(spectrum_path, destp)
            self.multirunfiledict["misc_files"] = {}
            self.multirunfiledict["misc_files"][newfn] = "%s;%s;%d;%d" % (
                "csv_misc_file",
                ",".join(specd_headerdict["keys"]),
                specd_headerdict["num_header_lines"],
                specd_headerdict["num_data_rows"],
            )
        self.writefom(destfolder, anak, anauserfomd=anauserfomd)


# c=Analysis__Pphotomax()
# c.debugmode=True
##p_exp='/home/dan/htehome/processes/experiment/temp/20150904.112552.done/20150904.112552.exp'
##p_ana='/home/dan/htehome/processes/analysis/temp/20150904.113437.done/20150904.113437.ana'
# p_exp='//htejcap.caltech.edu/share/home/processes/experiment/temp/20150904.112552.done/20150904.112552.exp'
# p_ana='//htejcap.caltech.edu/share/home/processes/analysis/temp/20150904.113437.done/20150904.113437.ana'
# expd=readexpasdict(p_exp)
# usek='data'
# techk='CV3'
# typek='pstat_files'
# anadict=readana(p_ana, stringvalues=True, erroruifcn=None)
# filenames=c.getapplicablefilenames(expd, usek, techk, typek, runklist=['run__1', 'run__2'], anadict=anadict)
# c.perform(os.path.split(p_ana)[0], expdatfolder=os.path.split(p_exp)[0], writeinterdat=False, anak='ana__2')
# print 'THESE FOM FILES WRITTEN'
# for k, v in c.multirunfiledict.items():
#    print k, v
# print 'THESE FOMs CALCULATED'
# print c.fomdlist
