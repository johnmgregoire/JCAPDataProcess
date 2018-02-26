import numpy, copy, operator
from scipy import interpolate
from scipy.signal import savgol_filter
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    
from fcns_io import *
from fcns_math import myeval

pids='3933,3930,3932,3928'.split(',')
folds=r'K:\users\hte\Raman\39338\20180221analysis_averaged,K:\users\hte\Raman\39305\20180221analysis_averaged,K:\users\hte\Raman\39327\20180220analysis_averaged,K:\users\hte\Raman\39282\20180221analysis_averaged'.split(',')


p=r'K:\users\hte\CompSustNet\2017_BiCuV\3928\ana__8_3928_3930_3932_3933_BckGrnd_Rank2.txt'
pnew=r'K:\users\hte\CompSustNet\2017_BiCuV\3928\201802Raman_3928_3930_3932_3933.udi'

with open(p, mode='r') as f:
    lines=f.readlines()

for l in lines:
    if l.startswith('plate_id='):
        break

pidlist=l.partition('plate_id=')[2].strip().split(',')

for l in lines:
    if l.startswith('sample_no='):
        break
        
smplist=l.partition('sample_no=')[2].strip().split(',')

pid_smp_tups=[tup for tup in zip(pidlist, smplist)]

new_lines=[]
for l in lines:
    if l.startswith('pattern_fn'):
        continue
    if l.startswith('Q='):
        break
    new_lines+=[l]
evalraman=lambda s:[float(v.strip()) for v in s.split(' ')][::-1]
evalraman_q=lambda lines:[float(l.strip()) for l in lines][::-1]
backtostring=lambda vals:','.join(['%.5e' %v for v in vals])+'\n'
spectra_line_tups=[]
for pid, fold in zip(pids, folds):
    fns=os.listdir(fold)
    psmp, pspec, pwave=[[os.path.join(fold, fn) for fn in fns if fn.endswith(s) and not '_circle' in fn][0] for s in ['sample_no.txt', 'avecirclespectra.txt', '_wdata.txt']]
    
    with open(psmp, mode='r') as f:
        lines=f.readlines()
    smp_this_plate=[`int(myeval(l.strip()))` for l in lines]
    print [(pid, smp) for smp in smp_this_plate if not (pid, smp) in pid_smp_tups]
    inds_old_new=[(pid_smp_tups.index((pid, smp)), count) for count, smp in enumerate(smp_this_plate) if (pid, smp) in pid_smp_tups]
    
    with open(pspec, mode='r') as f:
        lines=f.readlines()
    #print '***',''.join(lines[:10])
    
    spectra_line_tups+=[(i_old, ('I%d=' %(i_old+1))+backtostring(evalraman(lines[i_new]))) for i_old, i_new in inds_old_new]
    print '^^^',[(i_new, lines[i_new]) for i_old, i_new in inds_old_new if i_old==0]
    with open(pwave, mode='r') as f:
        lines=f.readlines()
    q_string='Q='+backtostring(evalraman_q(lines))#assume this is the same every time

new_lines+=[q_string]

print 'LENGTH CHECK:',  len(pidlist), len(spectra_line_tups)
new_lines+=[s for i, s in sorted(spectra_line_tups)]

print 'NOT FOUND:'
print '\n'.join(['%s,%s'%tup for count, tup in enumerate(pid_smp_tups) if not count in [i for i, s in sorted(spectra_line_tups)]])
print '\n'.join([`count` for count, tup in enumerate(pid_smp_tups) if not count in [i for i, s in sorted(spectra_line_tups)]])
print set([pidlist[i] for i, s in sorted(spectra_line_tups) ])

newfilestr=''.join(new_lines)
with open(pnew, mode='w') as f:
    f.write(newfilestr)


