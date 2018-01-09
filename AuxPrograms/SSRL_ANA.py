import os, numpy, time
import pandas as pd
import os, sys
projectroot = os.path.split(os.getcwd())[0]
sys.path.append(projectroot)
sys.path.append(os.path.join(projectroot, 'AuxPrograms'))
sys.path.append(os.path.join(projectroot, 'QtForms'))
sys.path.append(os.path.join(projectroot, 'AuxPrograms'))
sys.path.append(os.path.join(projectroot, 'OtherApps'))
sys.path.append(os.path.join(projectroot, 'BatchProcesses'))
sys.path.append(os.path.join(projectroot, 'AnalysisFunctions'))

# from fcns_math import *
from fcns_io import *
from fcns_ui import *

anapath=r'K:\users\helge.stein\20180108_CuPdZnAr_43557\processed'
exppath=r'K:\users\helge.stein\20180108_CuPdZnAr_43557\20170727.130926.done'

#this block loks at the exppath and contained files also this is where it looks up the timestamp etc.
rcpd={'file_dlist':[]}
rcpd['parameters']={}
an_name='Analysis__SSRL_batch_process'
multirun_ana_files={an_name:[]}

p_files=os.listdir(exppath)
shellfns=[fn for fn in p_files if not '.' in fn]
shellfn=shellfns[0]
with open(os.path.join(exppath, shellfn), mode='r') as f:
    lines=f.readlines()
for l in lines:
    if l.startswith('#D'):
        ts=time.strptime(l[2:].strip(), '%a %b %d %H:%M:%S %Y')
        rcpd['name']=time.strftime('%Y%m%d.%H%M%S',ts)
    if l.startswith('#S'):
        scmd=l.partition('  ')[2].strip()
        if len(scmd)>0:
            rcpd['parameters']['spec_command']=scmd

csvfns=[fn for fn in p_files if fn.endswith('.csv')]
if len(csvfns)==1:#should only be 1 file that is the summary of spec info
    fn=csvfns[0]
    #multirun_ana_files[an_name]+=[{'folderpath':p, 'fn':fn, 'type':'fom_files', 'fval':'csv_fom_file;'}]
    rcpd['file_dlist']+=[{'tech':'files_technique__SSRL', 'type':'csv_summary_files',  'fn':fn, 'fval':'ssrl_spec_csv_file;', 'folderpath':exppath}]

sysname=os.path.split(anapath)[1]
#h5path=os.path.join(os.path.join(p_processed, 'h5'), sysname+'.h5')

'''
h5f=h5py.File(h5path, mode='r')
g=h5f[h5f.attrs['default_group']]
gd=g['deposition']
q=g['xrd']['qcounts'].attrs['q']
npts=len(q)

if 'qcounts_subbcknd' in g['xrd'].keys():
    q_subbcknd=g['xrd']['qcounts_subbcknd'].attrs['q']
    npts_subbcknd=len(q_subbcknd)
else:
    q_subbcknd=None

if 'selectROI' in gd.keys():#make Analysis__SSRL_XRF_Comps ana block if possible but otherwise multirun_ana_files keeps its initialized value above
    gr=gd['selectROI']
    gs=g['spec']
    xrfcsvkeys=['sample_no,runint,plate_id']
    xrfcsvkeys+=['%s.%s' %(tup[1], tup[0]) for tup in sorted(gs.attrs.items())]
    roi_keys_to_copy=[tup[0] for tup in sorted(gs.attrs.items())]
    xrfcsvkeys+=['%s.AtFrac' %el for el in gd.attrs['elements']]
    xrfcsvfn=''.join([el for el in gd.attrs['elements']])+'.csv'
    an_name='Analysis__SSRL_XRF_Comps'
    headline=','.join(xrfcsvkeys)
'''

scan_csv = pd.read_csv(os.path.join(exppath,csvfns[0]),header=1)
xy_images=numpy.array(zip(scan_csv['   Plate X'], scan_csv['   Plate Y']))

imdir=os.path.join(exppath, 'images')
if os.path.isdir(imdir):
    imdir_files=os.listdir(imdir)
#        calibfns=sorted([fn for fn in imdir_files if fn.endswith('.calib')])
#        if len(calibfns)>0:#many but only need 1
#            fn=calibfns[0]
#            multirun_ana_files[an_name]+=[{'folderpath':imdir, 'fn':fn, 'type':'misc_files', 'fval':'ssrl_misc_file;'}]
    tif_fns=sorted([fn for fn in imdir_files if fn.endswith('.tif')])

    ana_files_generator=lambda fn: \
                {\
                 'Analysis__SSRL_Integrate':[{'fn':fn.replace('.tif', '_integrated.csv'),  'type':'pattern_files', 'fval':'ssrl_csv_pattern_file;q.nm,intensity.counts;1;%d;' %npts, 'h5arrind':count, 'h5dataset':'qcounts'}]\
                    }\
            if q_subbcknd is None else \
                {\
                 'Analysis__SSRL_Integrate':[{'fn':fn.replace('.tif', '_integrated.csv'),  'type':'pattern_files', 'fval':'ssrl_csv_pattern_file;q.nm,intensity.counts;1;%d;' %npts, 'h5arrind':count, 'h5dataset':'qcounts'}], \
                 'Analysis__SSRL_Process':[{'fn':fn.replace('.tif', '_processed.csv'),  'type':'pattern_files', 'fval':'ssrl_csv_pattern_file;q.nm_processed,intensity.counts_processed;1;%d;' %npts_subbcknd, 'h5arrind':count, 'h5dataset':'qcounts_subbcknd'}], \
                    }
    if len(tif_fns)==len(xy_images):

        rcpd['file_dlist']+=[{'xyarr':xyarr,'tech':'files_technique__SSRL', 'type':'image_files',  'fn':fn, 'fval':'ssrl_mar_tiff_file;', 'folderpath':imdir, \
             'ana_files':ana_files_generator(fn)\
             } for count, (fn, xyarr) in enumerate(zip(tif_fns, xy_images))]
#get Analysis__SSRL_Integrate params from g['xrd'].attrs.items()
pck2dfolder=os.path.join(anapath)
pck2dvalsfn='pck2d_chi_q_vals.pck'
pck2dvalsp=os.path.join(anapath, pck2dvalsfn)
if os.path.isdir(pck2dfolder) and os.path.isfile(pck2dvalsp):
    rcpd['file_dlist']+=[{'tech':'files_technique__SSRL', 'type':'pck2d_files',  'fn':pck2dvalsfn, 'fval':'ssrl_vals_pck_file;', 'folderpath':os.path.split(pck2dvalsp)[0]}]
    pck2d_fns=sorted([fn for fn in os.listdir(pck2dfolder) if fn.endswith('.npy')])#assuem this sorting gives the same ordering as the xys
    rcpd['file_dlist']+=[{'xyarr':xyarr,'tech':'files_technique__SSRL', 'type':'pck2d_files',  'fn':fn, 'fval':'ssrl_pck_file;', 'folderpath':pck2dfolder} for fn, xyarr in zip(pck2d_fns, xy_images)]
rcpdlist=[rcpd]

rcpfilestr = strrep_filedict(rcpd)