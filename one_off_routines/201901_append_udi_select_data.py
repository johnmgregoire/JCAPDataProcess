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

#newanasavefolder=r'L:\processes\analysis\xrds\20190113.192701.run'
newanasavefolder=r'L:\processes\analysis\ssrl\20190207.010101.run'
newanapath=buildanapath(newanasavefolder)

q_key='q.nm'

intensity_key='intensity.counts'
#append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=['ana__7'], l_anak_patterns=['ana__2'], pattern_key='pattern_files', compkeys='AtFrac', q_key=q_key,intensity_key=intensity_key, pattern_fn_search_str='1st_frame')
#append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=['ana__7'], l_anak_patterns=['ana__2'], pattern_key='pattern_files', compkeys='AtFrac', q_key=q_key,intensity_key=intensity_key, pattern_fn_search_str='2nd_frame')

#append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=['ana__6'], l_anak_patterns=['ana__2'], pattern_key='pattern_files', compkeys='AtFrac', q_key=q_key,intensity_key=intensity_key, pattern_fn_search_str='1st_frame')
append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=['ana__5'], l_anak_patterns=['ana__1'], pattern_key='pattern_files', compkeys='AtFrac', q_key=q_key,intensity_key=intensity_key, pattern_fn_search_str='integrated', xykeys_compcsv=('mX', 'mY'))

