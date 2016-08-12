import os

PLATEFOLDERS=[r'\\htejcap.caltech.edu\share\data\hte_jcap_app_proto\plate', r'J:\hte_jcap_app_proto\plate', \
                       r'\\htejcap.caltech.edu\share\home\users\hte\platemaps', r'ERT',r'K:\users\hte\platemaps', ]
#                       r'/cifs/10.231.101.11/data/hte_jcap_app_proto/plate', r'/cifs/10.231.101.12/home/users/hte/platemaps']

RUNFOLDERS=[r'\\htejcap.caltech.edu\share\data\hte_jcap_app_proto\run', r'J:\hte_jcap_app_proto\run', ]
#						r'/cifs/10.231.101.11/data/hte_jcap_app_proto/run']

EXPFOLDERS_J=[r'\\htejcap.caltech.edu\share\data\hte_jcap_app_proto\experiment', r'J:\hte_jcap_app_proto\experiment', ]
#						r'/cifs/10.231.101.11/data/hte_jcap_app_proto/experiment']

EXPFOLDERS_K=[r'\\htejcap.caltech.edu\share\home\processes\experiment', r'K:\processes\experiment', ]
#						r'/cifs/10.231.101.12/home/processes/experiment']

ANAFOLDERS_J=[r'\\htejcap.caltech.edu\share\data\hte_jcap_app_proto\analysis', r'J:\hte_jcap_app_proto\analysis']
#, r'\\hte-nasv-01.htejcap.caltech.edu\data\hte_jcap_app_proto\analysis', \
#						r'/cifs/10.231.101.11/data/hte_jcap_app_proto/analysis']

ANAFOLDERS_K=[r'\\htejcap.caltech.edu\share\home\processes\analysis', r'K:\processes\analysis', r'\\hte-nasv-02.htejcap.caltech.edu\home\processes\analysis', ]
#						r'/cifs/10.231.101.12/home/processes/analysis']

FOMPROCESSFOLDERS=[r'\\htejcap.caltech.edu\share\home\users\hte\platemaps\FilterSmoothMaps', r'K:\users\hte\platemaps\FilterSmoothMaps', ]
#						r'/cifs/10.231.101.12/home/users/hte/platemaps/FilterSmoothMaps']

PLATEMAPBACKUP=[r'\\htejcap.caltech.edu\share\data\hte_jcap_app_proto\map', ]
#r'/cifs/10.231.101.11/data/hte_jcap_app_proto/map']


XRFSPROCESSFOLDERS=[r'\\htejcap.caltech.edu\share\home\experiments\xrfs\calibration_libraries', r'K:\experiments\xrfs\calibration_libraries', ]



for l in [PLATEFOLDERS, RUNFOLDERS, EXPFOLDERS_J, EXPFOLDERS_K, ANAFOLDERS_J, ANAFOLDERS_K, FOMPROCESSFOLDERS]:
    for i in range(len(l))[::-1]:
        if not os.path.isdir(l[i]):
            l.pop(i)
    if len(l)==0:
        print 'WARNING: some DBPaths have no remaining options'

#import os
#[os.path.isdir(p) for p in ANAFOLDERS_K]
