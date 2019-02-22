import numpy, copy, operator
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AnalysisFunctions'))
#import matplotlib.pyplot as plt
from fcns_io import *
from fcns_ui import *
from CalcFOMApp import calcfomDialog
from Analysis_Master import Analysis_Master_nointer
from create_udi_standalone import append_udi_to_ana, append_resampled_merged_patterns_to_ana, smoothfcn
analysismasterclass=Analysis_Master_nointer()

newanasavefolder=r'L:\processes\analysis\xrds\20181218.134602.run'

auxpaths=[buildanapath(p) for p in r'/xrds/20171221.164203,/xrds/20171221.163932,/xrds/20171221.163722'.split(',')]

newanapath=buildanapath(newanasavefolder)

q_key='q.nm'

intensity_key='intensity.counts'
append_udi_to_ana(l_anapath=[newanapath]+auxpaths, l_anak_comps=['ana__6']*4, l_anak_patterns=['ana__2']*4, pattern_key='pattern_files', compkeys='AtFrac', q_key=q_key,intensity_key=intensity_key, pattern_fn_search_str='1st_frame', union_el_list=True)
append_udi_to_ana(l_anapath=[newanapath]+auxpaths, l_anak_comps=['ana__6']*4, l_anak_patterns=['ana__2']*4, pattern_key='pattern_files', compkeys='AtFrac', q_key=q_key,intensity_key=intensity_key, pattern_fn_search_str='2nd_frame', union_el_list=True)


