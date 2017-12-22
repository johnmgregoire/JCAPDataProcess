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

xrdsnames=r'xrds/20171221.174144.run,xrds/20171221.164203.run,xrds/20171221.163932.run,xrds/20171221.163722.run'.split(',')

pl=[]
for fn in xrdsnames:
    pl+=[buildanapath(fn)]
append_udi_to_ana(l_anapath=pl, l_anak_comps=['ana__6']*len(pl), l_anak_patterns=['ana__5']*len(pl), pattern_key='pattern_files', compkeys='AtFrac', q_key='q.nm_resampled',intensity_key='intensity.counts_resampled', union_el_list=True)

