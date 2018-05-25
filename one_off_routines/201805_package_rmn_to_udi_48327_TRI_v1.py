import numpy, copy, operator
from scipy import interpolate
from scipy.signal import savgol_filter
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    
from fcns_io import *
from fcns_math import myeval


pid='4832'

os.chdir(r'K:\users\hte\Raman\48327\averaged_20180522_square')
with open('46932_wafer_map-2_Copy_EM_avecirclespectra.txt', mode='r') as f:
    lines=f.readlines()

spectra_string=''.join([('\nI%d=' %(count+1))+','.join(l.strip().split(' ')[::-1]) for count, l in enumerate(lines)])

with open('46932_wafer_map-2_Copy_EM_averingspectra.txt', mode='r') as f:
    lines=f.readlines()

spectra_string_substrate=''.join([('\nI%d=' %(count+1))+','.join(l.strip().split(' ')[::-1]) for count, l in enumerate(lines)])

with open('46932_wafer_map-2_Copy_EM_wdata.txt', mode='r') as f:
    lines=f.readlines()
q_string='Q='+','.join([l.strip() for count, l in enumerate(lines)][::-1])

with open('46932_wafer_map-2_Copy_EM_sample_no.txt', mode='r') as f:
    lines=f.readlines()
smp_list=[int(myeval(l.strip())) for l in lines]
smp_string='sample_no='+','.join(['%d' %smp for count, smp in enumerate(smp_list)])



#os.chdir(r'K:\experiments\xrds\user\Lan\40374_alloyBVO_paul\20170710summaryfigs_lin')
#READ PLATEMAP
pmp=getplatemappath_plateid(pid)
pmdlist=readsingleplatemaptxt(pmp)
pmsmps=[d['sample_no'] for d in pmdlist]


els, tup_multielementink=getelements_plateidstr(pid, multielementink_concentrationinfo_bool=True, return_defaults_if_none=True)
cels_set_ordered, conc_el_chan=tup_multielementink[1]
calc_comps_multi_element_inks(pmdlist, cels_set_ordered, conc_el_chan)
pmsmps=[d['sample_no'] for d in pmdlist]
pmdlist_raman=[pmdlist[pmsmps.index(smp)] for smp in smp_list]

els_str=','.join(cels_set_ordered+['alloy'])

comp_str_list=[]
for el in cels_set_ordered:
    k=el+'.AtFrac'
    comp_str_list+=[el+'='+','.join(['%.4f' %d[k] for d in pmdlist_raman])]

comp_str='\n'.join(comp_str_list)

xy_str_list=[]
for k in ['x', 'y']:
    xy_str_list+=[k.upper()+'='+','.join(['%.4f' %d[k] for d in pmdlist_raman])]
xy_str='\n'.join(xy_str_list)


headlines=[\
'// Metadata', 
'M=%d' %len(cels_set_ordered), \
'Elements='+els_str, \
'Composition=%s' %('Bi,V,alloy'), \
'Deposition=X,Y', \
'N=%d' %len(smp_list), \
'', \
'// Deposition data', \
xy_str, \
smp_string, \
'plate_id='+','.join([pid]*len(smp_list)), \
'', \
'// Composition data', \
comp_str, \
'', \
'//Integrated counts data', \
q_string, \
]

s_smps='\n'.join(headlines+[spectra_string])
s_substrate='\n'.join(headlines+[spectra_string_substrate])

with open('20180522_TRI_48327_MnFeNiCuCoZn_sample_averaged.udi', mode='w') as f:
    f.write(s_smps)

with open('20180522_TRI_48327_MnFeNiCuCoZn_substrate_averaged.udi', mode='w') as f:
    f.write(s_substrate)

