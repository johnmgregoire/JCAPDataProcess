import os

projectpath = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
print os.path.join(projectpath, "LocalDBPaths.py")
if os.path.isfile(os.path.join(projectpath, "LocalDBPaths.py")):
    from sys import path as syspath

    syspath.append(projectpath)
    from LocalDBPaths import *

    print "paths loaded from LocalDBPaths"
else:
    PLATEFOLDERS = [
        r"\\htejcap.caltech.edu\share\data\hte_jcap_app_proto\plate",
        r"J:\hte_jcap_app_proto\plate",
    ]
    RUNFOLDERS = [
        r"\\htejcap.caltech.edu\share\data\hte_jcap_app_proto\run",
        r"J:\hte_jcap_app_proto\run",
    ]
    EXPFOLDERS_J = [
        r"\\htejcap.caltech.edu\share\data\hte_jcap_app_proto\experiment",
        r"J:\hte_jcap_app_proto\experiment",
    ]
    EXPFOLDERS_L = [
        r"\\htejcap.caltech.edu\share\proc\processes\experiment",
        r"L:\processes\experiment",
    ]
    ANAFOLDERS_J = [
        r"\\htejcap.caltech.edu\share\data\hte_jcap_app_proto\analysis",
        r"J:\hte_jcap_app_proto\analysis",
    ]
    ANAFOLDERS_L = [
        r"\\htejcap.caltech.edu\share\proc\processes\analysis",
        r"L:\processes\analysis",
    ]
    FOMPROCESSFOLDERS = [
        r"\\htejcap.caltech.edu\share\home\users\hte\platemaps\FilterSmoothMaps",
        r"K:\users\hte\platemaps\FilterSmoothMaps",
    ]
    PLATEMAPFOLDERS = [
        r"\\htejcap.caltech.edu\share\data\hte_jcap_app_proto\map",
        r"J:\hte_jcap_app_proto\map",
        r"\\htejcap.caltech.edu\share\home\users\hte\platemaps",
        r"ERT",
        r"K:\users\hte\platemaps",
    ]
    EXPERIMENT_DROP_FOLDERS = [
        r"\\htejcap.caltech.edu\share\home\experiments",
        r"K:\experiments",
    ]
    XRFSPROCESSFOLDERS = [
        r"\\htejcap.caltech.edu\share\home\experiments\xrfs\user\calibration_libraries",
        r"K:\experiments\xrfs\user\calibration_libraries",
    ]
    ECMSPROCESSFOLDERS = [
        r"\\htejcap.caltech.edu\share\home\experiments\anec\SIMULATION_LIBRARIES",
        r"K:\experiments\anec\SIMULATION_LIBRARIES",
    ]
    for l in [
        PLATEFOLDERS,
        RUNFOLDERS,
        EXPFOLDERS_J,
        EXPFOLDERS_L,
        ANAFOLDERS_J,
        ANAFOLDERS_L,
        FOMPROCESSFOLDERS,
    ]:
        for i in range(len(l))[::-1]:
            if not os.path.isdir(l[i]):
                l.pop(i)
        if len(l) == 0:
            print "WARNING: some DBPaths have no remaining options"
