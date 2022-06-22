import numpy, copy, operator

if __name__ == "__main__":
    import os, sys

    sys.path.append(os.path.split(os.getcwd())[0])
from fcns_math import *
from fcns_io import *
from csvfilewriter import createcsvfilstr
from DBPaths import *

infop = r"D:\data\201512uvispcktoana\pcktoana.csv"
l_expname, l_ananame, l_resultsfolder = readtxt_selectcolumns(
    infop,
    selcolinds=[1, 2, 3],
    delim=",",
    num_header_lines=1,
    floatintstr=str,
    zipclass=0,
)
istart, istop = 70, 85  # 0, 999
l_expname = l_expname[istart:istop]
l_ananame = l_ananame[istart:istop]
l_resultsfolder = l_resultsfolder[istart:istop]
#        self.RunTypeLineEdit.setText('ref_dark')
#        self.FileStartLineEdit.setText('0_-1_')
#        self.editexp_addmeasurement()
#
#        self.RunTypeLineEdit.setText('ref_light')
#        self.FileStartLineEdit.setText('0_1_')
#        self.editexp_addmeasurement()
#
genexpfilep = lambda expnam: os.path.join(
    os.path.join(r"K:\processes\experiment\uvis\todo", expname + ".todo"),
    expname + ".exp",
)
# genanafolderp=lambda ananame: os.path.join(r'K:\processes\analysis\uvis',ananame+'.todo')
genexpsavefolderp = lambda expname: os.path.join(
    r"D:\data\201512uvispcktoana\uvis\exp", expname + ".done"
)
genexpfolderforanafile = lambda expname: (r"/uvis/" + expname + ".done").replace(
    chr(92), chr(47)
)
genanafolderp = lambda ananame: os.path.join(
    r"D:\data\201512uvispcktoana\uvis\ana", ananame + ".done"
)
genresfolderp = lambda resultsfolder: os.path.join(
    r"K:\experiments\uvis\drop", resultsfolder
)
for expname, ananame, resultsfolder in zip(
    l_expname, l_ananame, l_resultsfolder
):  # [-1:]
    print(expname)
    expfilep = genexpfilep(expname)
    expsavefolderp = genexpsavefolderp(expname)
    expfolderp = os.path.split(expfilep)[0]
    anafolderp = genanafolderp(ananame)
    resfolderp = genresfolderp(resultsfolder)
    #    if not expname=='20140312.123904':
    #        continue
    #    expfilep=r'K:\processes\experiment\temp\manualchangesmplines.temp\20140312.123904.exp'
    try:
        resfns = [fn[:-4] for fn in os.listdir(resfolderp) if fn.endswith(".pck")]
        anabool = True
    except:
        resfns = []
        anabool = False
    if 0:  # just print params from 1st file
        if len(resfns) == 0:
            continue
        with open(os.path.join(resfolderp, resfns[0] + ".pck"), mode="r") as f:
            rd = pickle.load(f)
        print("\t".join(
            [
                rd["function_parameters"]["darkcode"],
                rd["function_parameters"]["refcode"],
                resultsfolder,
            ]
        ))
        # continue
    if anabool:
        anad = {}
        anad["ana_version"] = "3"
        anad["experiment_name"] = expname
        anad["experiment_path"] = genexpfolderforanafile(expname)
        anad["name"] = ananame
        anad["ana__1"] = {}
        d = anad["ana__1"]
        anak = "ana__1"
        initanaparams = True
        expfiled = readexpasdict(expfilep, createfiledicts=False)
        runkl = sorted([k for k in list(expfiled.keys()) if k.startswith("run__")])
        garb, garb, maxrunint = runkl[-1].partition("__")
        maxruncount = eval(maxrunint)
    else:
        initanaparams = False
    fomdlist = []
    qfomdlist = []
    # expfiled['recipe']['refcode']
    zipclass = 0
    while len(runkl) > 0:
        runk = runkl.pop(0)
        rund = expfiled[runk]
        runp_fullpath = tryprependpath(RUNFOLDERS, rund["run_path"])
        if zipclass:
            zipclass.close()
        zipclass = gen_zipclass(runp_fullpath)
        # import other data in parent folder
        if 1:  #
            zipsinexp = [
                os.path.split(v["run_path"])[1]
                for k, v in list(expfiled.items())
                if k.startswith("run__")
            ]
            runparentfolder = os.path.split(runp_fullpath)[0]
            for zipfn in os.listdir(runparentfolder):
                if zipfn in zipsinexp:
                    continue
                zipp = os.path.join(runparentfolder, zipfn)
                compareprependpath(RUNFOLDERS, zipp)
                Nname = zipfn[:15]
                Nrcp = zipfn[:15] + ".rcp"
                Nzipclass = gen_zipclass(zipp)
                if Nzipclass.fn_in_archive(Nrcp):
                    Nlines = Nzipclass.readlines(Nrcp)
                    maxruncount += 1
                    Nrunk = "run__%d" % (maxruncount)
                    runkl += [Nrunk]
                    expfiled[Nrunk] = {}
                    expfiled[Nrunk]["name"] = Nname
                    expfiled[Nrunk]["rcp_file"] = Nrcp
                    expfiled[Nrunk]["run_path"] = compareprependpath(RUNFOLDERS, zipp)
                    expfiled[Nrunk]["run_use"] = "data"
                    expfiled[Nrunk]["parameters"] = {}
                    Npard = expfiled[Nrunk]["parameters"]
                    l = Nlines.pop(0)
                    while not l.startswith("files"):
                        if not "version" in l:
                            l = l.strip()
                            k, garb, v = l.partition(": ")
                            Npard[k] = v
                        l = Nlines.pop(0)
                    filetechk = l.partition(":")[0].strip()
                    l = Nlines.pop(0)  #'spectrumfiles
                    expfiled[Nrunk][filetechk] = {}
                    expfiled[Nrunk][filetechk]["spectrum_files"] = {}
                    Nfilesd = expfiled[Nrunk][filetechk]["spectrum_files"]
                    for l in Nlines:
                        l = l.strip()
                        k, garb, v = l.partition(": ")
                        if len(k) == 0:
                            continue
                        Nfilesd[k] = v
        for techcount, tk in enumerate(["DR_UVVIS", "T_UVVIS", "R_UVVIS"]):
            techk = "files_technique__%s" % tk
            if techk in list(rund.keys()) and "spectrum_files" in rund[techk]:
                typed = rund[techk]["spectrum_files"]
                # import R data into .exp
                if 1 and techcount == 1:  # T_UVVIS
                    Rrunp_fullpath = runp_fullpath.replace("T-UVVIS", "R-UVVIS")
                    if os.path.isfile(Rrunp_fullpath):
                        Rzipclass = gen_zipclass(Rrunp_fullpath)
                        if Rzipclass.fn_in_archive(rund["rcp_file"]):
                            Rlines = Rzipclass.readlines(rund["rcp_file"])
                            maxruncount += 1
                            Rrunk = "run__%d" % (maxruncount)
                            runkl += [Rrunk]
                            expfiled[Rrunk] = {}
                            expfiled[Rrunk]["name"] = rund["name"]
                            expfiled[Rrunk]["rcp_file"] = rund["rcp_file"]
                            expfiled[Rrunk]["run_path"] = rund["run_path"].replace(
                                "T-UVVIS", "R-UVVIS"
                            )
                            expfiled[Rrunk]["run_use"] = "data"
                            expfiled[Rrunk]["parameters"] = {}
                            Rpard = expfiled[Rrunk]["parameters"]
                            l = Rlines.pop(0)
                            while not l.startswith("files"):
                                if not "version" in l:
                                    l = l.strip()
                                    k, garb, v = l.partition(": ")
                                    Rpard[k] = v
                                l = Rlines.pop(0)
                            l = Rlines.pop(0)  #'spectrumfiles
                            expfiled[Rrunk]["files_technique__R_UVVIS"] = {}
                            expfiled[Rrunk]["files_technique__R_UVVIS"][
                                "spectrum_files"
                            ] = {}
                            Rfilesd = expfiled[Rrunk]["files_technique__R_UVVIS"][
                                "spectrum_files"
                            ]
                            for l in Rlines:
                                l = l.strip()
                                k, garb, v = l.partition(": ")
                                if len(k) == 0:
                                    continue
                                Rfilesd[k] = v
                for smpfn, filedstr in list(typed.items()):
                    if not zipclass.fn_in_archive(smpfn):
                        del typed[smpfn]  # fn was in rcp but does not exist
                        continue
                    #######fix exp file line
                    try:
                        if (
                            filedstr.count(";") < 3
                        ):  # needs addition of headlines and numpts and remove sample_no 0
                            if filedstr.endswith(";0"):
                                a, garb, garb = filedstr.rpartition(";")
                                samplestrwithcolon = ""
                                samplestr = ""
                            elif filedstr.count(";") == 1:  # no sample_no
                                a = filedstr
                                stemp = getsamplenum_fn(smpfn)
                                if stemp == 0:
                                    samplestrwithcolon = ""
                                    samplestr = ""
                                else:
                                    samplestr = "%d" % stemp
                                    samplestrwithcolon = ";" + samplestr
                            else:
                                a, garb, b = filedstr.rpartition(";")
                                samplestrwithcolon = ";" + b
                                samplestr = b
                            smpstr = zipclass.readlines(smpfn)[0].strip()
                            garb, garb, nrawpts, nheads = smpstr.split("\t")
                            nheads = "%d" % (eval(nheads) + 2)
                            typed[smpfn] = "%s;%s;%s%s" % (
                                a,
                                nheads,
                                nrawpts,
                                samplestrwithcolon,
                            )
                            nrawpts = eval(nrawpts)
                    except:
                        print("error, skipping ", smpfn)
                        del typed[smpfn]  # fn was in rcp but does not exist
                        continue
                    ####if T or DR process the file for ana and initial parameters including the search strs fopr dark and light ref
                    if (techcount < 2) and (smpfn[:-4] in resfns):
                        resfn = resfns.pop(resfns.index(smpfn[:-4])) + ".pck"
                        try:
                            with open(os.path.join(resfolderp, resfn), mode="r") as f:
                                rd = pickle.load(f)
                        except:
                            print("skipped pck file ", os.path.join(resfolderp, resfn))
                            continue
                        qualityfomkcheck = (
                            lambda fomk: "rescaled" in fomk or "2ndderiv" in fomk
                        )
                        fomd = dict(
                            [
                                (
                                    fomk.replace("maxabsorp", "max_abs").replace(
                                        "-", "_"
                                    ),
                                    fomv,
                                )
                                for fomk, fomv in rd["fom"].items()
                                if not qualityfomkcheck(fomk)
                            ]
                        )
                        qfomd = dict(
                            [
                                (fomk.replace("-", "_"), fomv)
                                for fomk, fomv in rd["fom"].items()
                                if qualityfomkcheck(fomk)
                            ]
                        )
                        plateid = rd["measurement_info"]["Plate ID"]
                        if initanaparams:
                            rund["run_use"] = "data"
                            initanaparams = False
                            d["analysis_fcn_version"] = rd["version"]
                            d["description"] = "%s on %s; plate_id %s" % (
                                ",".join(sorted(fomd.keys())),
                                tk,
                                plateid,
                            )
                            d["name"] = "Analysis__BG_Legacy"
                            d["parameters"] = {}
                            pd = d["parameters"]
                            for k, v in list(rd["function_parameters"].items()):
                                pd[k] = repr( v)
                            refdarkstr = "0_%s_" % (
                                rd["function_parameters"]["darkcode"]
                            )
                            reflightstr = "0_%s_" % (
                                rd["function_parameters"]["refcode"]
                            )
                            plotparams = dict({}, plot__1={})
                            plotparams["plot__1"]["x_axis"] = "t(s)"
                            plotparams["plot__1"]["series__1"] = (
                                "abs"
                                if "abs" in list(rd["intermediate_arrays"].keys())
                                else "Signal_0"
                            )
                            csvheaderdict = dict(
                                {}, csv_version="1", plot_parameters={}
                            )
                            csvheaderdict["plot_parameters"]["plot__1"] = dict(
                                {},
                                fom_name="DA_bgcode_repr"
                                if "DA_bgcode_repr" in list(fomd.keys())
                                else (
                                    "DA_bg_0"
                                    if "DA_bg_0" in list(fomd.keys())
                                    else list(fomd.keys())[0]
                                ),
                                colormap="jet_r",
                                colormap_over_color="(0.,0.,0.)",
                                colormap_under_color="(0.5,0.,0.)",
                            )
                        # write inter files and append to fomd
                        if 1 and len(fomd) > 0:  # saveinter files
                            if not os.path.isdir(anafolderp):
                                os.mkdir(anafolderp)
                            if samplestr:
                                fomdlist += [
                                    dict(
                                        fomd,
                                        sample_no=int(samplestr),
                                        plate_id=int(plateid),
                                        runint=int(runk.partition("run__")[2]),
                                    )
                                ]
                                if len(qfomd) > 0:
                                    qfomdlist += [
                                        dict(
                                            qfomd,
                                            sample_no=int(samplestr),
                                            plate_id=int(plateid),
                                            runint=int(runk.partition("run__")[2]),
                                        )
                                    ]  # , run=runk
                            # write inter data if foms reagrdless of vald sample_no
                            for count, (fk, fdesc, fext) in enumerate(
                                [
                                    (
                                        "inter_rawlen_files",
                                        "uvis_inter_rawlen_file",
                                        "rawlen",
                                    ),
                                    (
                                        "inter_files",
                                        "uvis_inter_interlen_file",
                                        "interlen",
                                    ),
                                ]
                            ):
                                if count == 0:
                                    interd = dict(
                                        [
                                            (k, v)
                                            for k, v in rd[
                                                "intermediate_arrays"
                                            ].items()
                                            if isinstance(v, numpy.ndarray)
                                            and len(v) == nrawpts
                                        ]
                                    )
                                else:
                                    if (
                                        not "rawselectinds"
                                        in list(rd["intermediate_arrays"].keys())
                                    ):
                                        continue
                                    ninterpts = len(
                                        rd["intermediate_arrays"]["rawselectinds"]
                                    )
                                    interd = dict(
                                        [
                                            (k, v)
                                            for k, v in rd[
                                                "intermediate_arrays"
                                            ].items()
                                            if isinstance(v, numpy.ndarray)
                                            and len(v) == ninterpts
                                        ]
                                    )
                                if len(interd) > 0:
                                    fn = "%s__%s_%s.txt" % (
                                        anak,
                                        os.path.splitext(smpfn)[0],
                                        fext,
                                    )
                                    p = os.path.join(anafolderp, fn)
                                    kl = saveinterdata(p, interd, savetxt=True)
                                    if not ("files_" + runk) in list(d.keys()):
                                        d["files_" + runk] = {}
                                        anarund = d["files_" + runk]
                                    if not fk in list(anarund.keys()):
                                        anarund[fk] = {}
                                    kl = saveinterdata(p, interd, savetxt=True)
                                    anarund[fk][fn] = "%s;%s;%d;%d%s" % (
                                        fdesc,
                                        ",".join(kl),
                                        1,
                                        len(interd[kl[0]]),
                                        samplestrwithcolon,
                                    )
                ###copy smp files to reference blocks in the .exp if ana params have been initialized. just loop through them again after ana has been completed for this technique
                if anabool and initanaparams:
                    print(expname, " initparams not executed")
                    # raiseanerror
                    continue
                if (
                    not anabool
                ):  # use the refcode and darkcode from the pck if possible but if not use these as default
                    try:
                        refdarkstr = "0_%d_" % (expfiled["recipe"]["darkcode"])
                        reflightstr = "0_%d_" % (expfiled["recipe"]["refcode"])
                    except:
                        refdarkstr = "THERE IS NO CODE TO SEARCH FOR"
                        reflightstr = "THERE IS NO CODE TO SEARCH FOR"
                for refstr, runuse in [
                    (refdarkstr, "ref_dark"),
                    (reflightstr, "ref_light"),
                ]:
                    refrunk = ""
                    for smpfn, filedstr in list(typed.items()):
                        if smpfn.startswith(refstr):
                            if not refrunk:
                                maxruncount += 1
                                refrunk = "run__%d" % (maxruncount)
                                expfiled[refrunk] = {}
                                for k, v in rund.items():
                                    if k.startswith("files"):
                                        continue
                                    expfiled[refrunk][k] = v
                                expfiled[refrunk]["run_use"] = runuse
                                expfiled[refrunk][techk] = {}
                                expfiled[refrunk][techk]["spectrum_files"] = {}
                            expfiled[refrunk][techk]["spectrum_files"][smpfn] = typed[
                                smpfn
                            ]
                # break#this break stays here so that only 1 of ['DR_UVVIS', 'T_UVVIS', 'R_UVVIS'] is acted upon
        if 0:  # stop after 1 run
            break
    usevals = [v["run_use"] for k, v in list(expfiled.items()) if k.startswith("run__")]
    if not "ref_dark" in usevals:
        print(expname, "is missing ref_dark")
    if not "ref_light" in usevals:
        print(expname, "is missing ref_light")
    if 1:  # save exp
        expfilestr = strrep_filedict(expfiled)
        if not os.path.isdir(expsavefolderp):
            os.mkdir(expsavefolderp)
        if 1:
            try:
                saverawdat_expfiledict(expfiled, expsavefolderp)
            except:
                print("raw data nto saveable for ", expsavefolderp)
        with open(os.path.join(expsavefolderp, expname + ".exp"), mode="w") as f:
            f.write(expfilestr)
    if 1 and anabool and len(fomdlist) > 0:  # saveana
        if not os.path.isdir(anafolderp):
            os.mkdir(anafolderp)
        if not initanaparams:
            d["plot_parameters"] = plotparams
        for count, (dlist, fk, fdesc) in enumerate(
            [
                (fomdlist, "fom_files", "csv_fom_file"),
                (qfomdlist, "misc_files", "csv_fom_file"),
            ]
        ):
            if len(dlist) == 0:
                continue
            fomnames = list(
                set([k for fd in dlist for k in list(fd.keys())]).difference(
                    set(["sample_no", "runint", "plate_id"])
                )
            )
            csvfilstr = createcsvfilstr(
                dlist, fomnames, intfomkeys=["runint", "plate_id"]
            )  # , strfomkeys=strkeys+strkeys_fomdlist)#, fn=fnf)
            allfomnames = ["sample_no", "runint", "plate_id"] + fomnames
            if count == 0:
                fn = "%s__%s.csv" % (anak, "-".join(fomnames[:3]))
            else:
                fn = "%s__%s.csv" % (anak, "qualityfoms")
            p = os.path.join(anafolderp, fn)
            totnumheadlines = writecsv_smpfomd(p, csvfilstr, headerdict=csvheaderdict)
            if not "files_multi_run" in list(d.keys()):
                d["files_multi_run"] = {}
                anamultirund = d["files_multi_run"]
            if not fk in list(anamultirund.keys()):
                anamultirund[fk] = {}
            anamultirund[fk][fn] = "%s;%s;%d;%d" % (
                fdesc,
                ",".join(allfomnames),
                totnumheadlines,
                len(fomdlist),
            )
        if 1:  # copy misc files
            miscfns = [
                fn
                for fn in os.listdir(resfolderp)
                if fn.endswith(".png")
                or (fn.endswith(".pck") and not fn[0].isdigit())
                or fn.endswith(".txt")
            ]
            if len(miscfns) > 0:
                anamultirund["misc_files"] = {}
                for fn in miscfns:
                    shutil.copy(
                        os.path.join(resfolderp, fn), os.path.join(anafolderp, fn)
                    )
                    anamultirund["misc_files"][fn] = "uvis_legacy_misc_file;"
        anafilestr = strrep_filedict(anad)
        # write fom files
        with open(os.path.join(anafolderp, ananame + ".ana"), mode="w") as f:
            f.write(anafilestr)
    if 0:  # stop after 1 exp/ana
        break
