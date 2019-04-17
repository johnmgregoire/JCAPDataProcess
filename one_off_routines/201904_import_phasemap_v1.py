import numpy, copy, operator
import time,pickle
if __name__ == "__main__":
    import os, sys
    #__file__=r'D:\Google Drive\Documents\PythonCode\JCAP\JCAPDataProcess\AnalysisFunctions\ecms.py'
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AnalysisFunctions'))
from fcns_math import *
from fcns_io import *
from fcns_ui import *
from csvfilewriter import createcsvfilstr, createcsvfilstr_bare
import zipfile


prevcsv=r'L:\processes\analysis\xrds\20181218.134602.copied-20181218221010726PST\ana__11_3928_3930_3932_3933.csv'
fileattrd={'keys':'sample_no,runint,plate_id,pmx,pmy,Intensity.max,Bi,Cu,V'.split(','),'num_header_lines':9}
d=readcsvdict(prevcsv, fileattrd, returnheaderdict=False, zipclass=None, includestrvals=False, delim=',')
d.keys()
anak='ana__1'
secondanak='ana__2'

instp=r'L:\processes\analysis\xrds\20190415.134602.run\ana__1_Bi-Cu-V_inst_Q512.udi'
soltnp=r'L:\processes\analysis\xrds\20190415.134602.run\ana__1_Bi-Cu-V_sol_Q512.txt'
modsoltnp=soltnp.replace(anak,secondanak)
anafolder=os.path.split(soltnp)[0]


with open(instp,mode='r') as f:
    lines=f.readlines()
smps=[int(s) for s in [l for l in lines if l.startswith('sample_no')][0].partition('=')[2].split(',')]
pids=[int(s) for s in [l for l in lines if l.startswith('plate_id')][0].partition('=')[2].split(',')]
Q=[float(s) for s in [l for l in lines if l.startswith('Q')][0].partition('=')[2].split(',')]
q0,q1=Q[0],Q[-1]
#error here means original csv doens't have all the samples - they can be removed but not added during external modification
inds=[np.where((d['sample_no']==smp) & (d['plate_id']==pid))[0][0] for smp,pid in zip(smps,pids)]

for k in d.keys():
    d[k]=d[k][inds]

N=len(inds)

with open(soltnp, mode='r') as f:
    soltnlines=f.readlines()
K=int([l.partition('=')[2] for l in soltnlines if l.startswith('K')][0])
C=np.zeros((N,K),dtype='float64')
S=np.zeros((N,K),dtype='float64')
Rsum=np.zeros((N,K),dtype='float64')
phase_names=['']*K
for l in soltnlines:
    if l.startswith('BName'):
        a,b,c=l.partition('=')
        smpind=int(a[5:])-1
        phase_names[smpind]=c.strip()
    elif l.startswith('C'):
        a,b,c=l.partition('=')
        smpind=int(a[1:])-1
        C[smpind,:]=np.array([float(s) for s in c.strip().split(',')])
    elif l.startswith('S'):
        a,b,c=l.partition('=')
        smpind=int(a[1:])-1
        S[smpind,:]=np.array([float(s) for s in c.strip().split(',')])
    elif l.startswith('R'):
        a,b,c=l.partition('=')
        aa,bb,cc=a[1:].partition('_')
        smpind=int(aa)-1
        phind=int(cc)-1
        Rsum[smpind,phind]=np.array([float(s) for s in c.strip().split(',')]).sum()
        if np.array([float(s) for s in c.strip().split(',')]).max()>1.0001:
            print 'error'
            break
S[C==0.]=0.

savekeys=['sample_no','plate_id','runint']
for phind in range(K):
    d['phase_weight.%d' %(phind+1)]=C[:,phind]
    d['shift_factor.%d' %(phind+1)]=S[:,phind]
    d['reconstructed_pattern_intensity.%d' %(phind+1)]=Rsum[:,phind]
    savekeys+=['phase_weight.%d' %(phind+1),'shift_factor.%d' %(phind+1),'reconstructed_pattern_intensity.%d' %(phind+1)]

dlist=[dict([(k,d[k][i]) for k in savekeys]) for i in range(N)]
           
filedesc,filestr=createcsvfilstr_bare(dlist,savekeys[3:],intfomkeys=savekeys[:3],strfomkeys=[],return_file_desc=True)
csvfn=anak+'__'+'-'.join(savekeys[3:6])+'.csv'
fom1path=os.path.join(anafolder, csvfn)
with open(fom1path,mode='w') as f:
    f.write(filestr)
print '%s: %s' %(csvfn,filedesc)

fn=anak+'__'+'phasenames.txt'
phasenamespath=os.path.join(anafolder, fn)
with open(phasenamespath,mode='w') as f:
    f.write('\n'.join(phase_names))
print '%s: %s' %(fn,'xrds_misc_file;')

phaseinfop=r'L:\processes\analysis\xrds\20190415.134602.run\ana__2_select_phases_info.csv'
ind__int_vs_std_by_cation=3
ind__select_icdd_id=1
int_vs_std_by_cation=readtxt_selectcolumns(phaseinfop, selcolinds=[ind__int_vs_std_by_cation], delim=',', num_header_lines=1, floatintstr=float, zipclass=None, lines=None)[0]
select_icdd_id=readtxt_selectcolumns(phaseinfop, selcolinds=[ind__select_icdd_id], delim=',', num_header_lines=1, floatintstr=str, zipclass=None, lines=None)[0]


icddzipp=r'L:\processes\analysis\xrds\20190415.134602.run\ana__1_20190304_BiCuVO_FTO_assembled_icdd.zip'
archive=zipfile.ZipFile(icddzipp, 'r')
fns=archive.namelist()

fn_selectphases=[[fn for fn in fns if os.path.split(fn)[1].startswith(s+'+') and 'icdd_vs_q' in fn and fn.endswith('.txt')][0] for s in select_icdd_id]
tot_int_selectphases=[]
for fn in fn_selectphases:
    with archive.open(fn, 'r') as f:
        lines=f.readlines()
    tot=0
    for l in lines[1:]:
        a,b,c=l.partition(' ')
        q=float(a)
        if q>q0 and q<q1:
            tot+=float(c)
    tot_int_selectphases+=[tot]

archive.close()
tot_int_per_phase_by_cation=(int_vs_std_by_cation*np.array(tot_int_selectphases))

modC=C*Rsum/tot_int_per_phase_by_cation[np.newaxis,:]
modC/=modC.sum(axis=1)[:,np.newaxis]


savekeys=['sample_no','plate_id','runint']
for phind in range(K):
    d['phase_concentration.%d' %(phind+1)]=modC[:,phind]
    savekeys+=['phase_concentration.%d' %(phind+1),'shift_factor.%d' %(phind+1)]

dlist=[dict([(k,d[k][i]) for k in savekeys]) for i in range(N)]
           
filedesc,filestr=createcsvfilstr_bare(dlist,savekeys[3:],intfomkeys=savekeys[:3],strfomkeys=[],return_file_desc=True)
csvfn=secondanak+'__'+'-'.join(savekeys[3:6])+'.csv'
fom2path=os.path.join(anafolder, csvfn)
with open(fom2path,mode='w') as f:
    f.write(filestr)
print '%s: %s' %(csvfn,filedesc)


for i,l in enumerate(soltnlines):
    if l.startswith('C'):
        a,b,c=l.partition('=')
        smpind=int(a[1:])-1
        soltnlines[i]=a+b+','.join(['%0.5f' %v for v in modC[smpind,:]])+'\n'
with open(modsoltnp,mode='w') as f:
    f.write(''.join(soltnlines))