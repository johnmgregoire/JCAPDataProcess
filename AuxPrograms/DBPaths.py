import os

projectpath=os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
print os.path.join(projectpath,'LocalDBPaths.py')
if os.path.isfile(os.path.join(projectpath,'LocalDBPaths.py')):
    from sys import path as syspath
    syspath.append(projectpath)
    from LocalDBPaths import *
    print 'paths loaded from LocalDBPaths'
else:

    PLATEFOLDERS=[r'\\htejcap.caltech.edu\share\data\hte_jcap_app_proto\plate', r'J:\hte_jcap_app_proto\plate']

    RUNFOLDERS=[r'\\htejcap.caltech.edu\share\data\hte_jcap_app_proto\run', r'J:\hte_jcap_app_proto\run', ]

    EXPFOLDERS_J=[r'\\htejcap.caltech.edu\share\data\hte_jcap_app_proto\experiment', r'J:\hte_jcap_app_proto\experiment', ]

    EXPFOLDERS_K=[r'\\htejcap.caltech.edu\share\home\processes\experiment', r'K:\processes\experiment', ]

    ANAFOLDERS_J=[r'\\htejcap.caltech.edu\share\data\hte_jcap_app_proto\analysis', r'J:\hte_jcap_app_proto\analysis']

    ANAFOLDERS_K=[r'\\htejcap.caltech.edu\share\home\processes\analysis', r'K:\processes\analysis', r'\\hte-nasv-02.htejcap.caltech.edu\home\processes\analysis', ]

    FOMPROCESSFOLDERS=[r'\\htejcap.caltech.edu\share\home\users\hte\platemaps\FilterSmoothMaps', r'K:\users\hte\platemaps\FilterSmoothMaps', ]

    PLATEMAPFOLDERS=[r'\\htejcap.caltech.edu\share\data\hte_jcap_app_proto\map', r'J:\hte_jcap_app_proto\map', \
                           r'\\htejcap.caltech.edu\share\home\users\hte\platemaps', r'ERT',r'K:\users\hte\platemaps']

    EXPERIMENT_DROP_FOLDERS=[r'\\htejcap.caltech.edu\share\home\experiments', r'K:\experiments']

    XRFSPROCESSFOLDERS=[r'\\htejcap.caltech.edu\share\home\experiments\xrfs\calibration_libraries', r'K:\experiments\xrfs\calibration_libraries', ]



    for l in [PLATEFOLDERS, RUNFOLDERS, EXPFOLDERS_J, EXPFOLDERS_K, ANAFOLDERS_J, ANAFOLDERS_K, FOMPROCESSFOLDERS]:
        for i in range(len(l))[::-1]:
            if not os.path.isdir(l[i]):
                l.pop(i)
        if len(l)==0:
            print 'WARNING: some DBPaths have no remaining options'


