import numpy, copy, operator
from scipy import interpolate
from scipy.signal import savgol_filter
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    
from fcns_io import *
from fcns_math import myeval


pid='4067'

os.chdir(r'K:\users\hte\Raman\40677\Averaged_spectra')
with open('test-new_montage-3_avecirclespectra_v2__all.txt', mode='r') as f:
    lines=f.readlines()

spectra_string=''.join([('I%d=' %(count+1))+l.replace(' ', ',') for count, l in enumerate(lines)])

with open('test-new_montage-3_averingspectra_v2__all.txt', mode='r') as f:
    lines=f.readlines()

spectra_string_substrate=''.join([('I%d=' %(count+1))+l.replace(' ', ',') for count, l in enumerate(lines)])

with open('test-new_montage-3_wdata_all.txt', mode='r') as f:
    lines=f.readlines()
q_string='Q='+','.join([l.strip() for count, l in enumerate(lines)])

with open('test-new_montage-3_sample_no_all.txt', mode='r') as f:
    lines=f.readlines()
smp_list=[int(myeval(l.strip())) for l in lines]
smp_string='sample_no='+','.join(['%d' %smp for count, smp in enumerate(smp_list)])



#os.chdir(r'K:\experiments\xrds\user\Lan\40374_alloyBVO_paul\20170710summaryfigs_lin')
#READ PLATEMAP
pmp=getplatemappath_plateid(pid)
pmdlist=readsingleplatemaptxt(pmp)
pmsmps=[d['sample_no'] for d in pmdlist]


els, tup_multielementink=getelements_plateidstr(pid, multielementink_concentrationinfo_bool=True)
cels_set_ordered, conc_el_chan=tup_multielementink[1]
calc_comps_multi_element_inks(pmdlist, cels_set_ordered, conc_el_chan)
pmsmps=[d['sample_no'] for d in pmdlist]
pmdlist_raman=[pmdlist[pmsmps.index(smp)] for smp in smp_list]

els_str=','.join(cels_set_ordered+['alloy'])

comp_str_list=[]
for el in cels_set_ordered:
    k=el+'.AtFrac'
    comp_str_list+=[el+'='+','.join(['%.4f' %d[k] for d in pmdlist_raman])]
comp_str_list+=['alloy='+','.join(['%.4f' %(1.-d['V.AtFrac']-d['Bi.AtFrac']) for d in pmdlist_raman])]
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

with open('test-new_montage-3_avecirclespectra_v2__all.udi', mode='w') as f:
    f.write(s_smps)

with open('test-new_montage-3_averingspectra_v2__all.udi', mode='w') as f:
    f.write(s_substrate)

