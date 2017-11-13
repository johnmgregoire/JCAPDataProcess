import os, numpy, time
import h5py
from fcns_ui import mygetdir
p=r'K:\experiments\xrds\user\SSRLFeb2015\2015Feb\24297_NbMnVO'
pp=r'K:\experiments\xrds\user\SSRLFeb2015\Processed\24297_NbMnVO'

p, p_processed=p, pp
def get_externalimportdatad_ssrl_batchresults(p, p_processed=None, askforprocessed=True, parent=None):#assume folder is for single .rcp
    if p_processed is None and askforprocessed:
        p_processed=str(mygetdir(parent=parent, xpath=p,markstr='Folder containing processed data, i.e. parent folder of "pck2d"' ))
        if p_processed is None or len(p_processed)==0:
            p_processed=None
    if p_processed is None:
        return {}

    rcpd={'file_dlist':[]}
    rcpd['parameters']={}
    an_name='Analysis__SSRL_batch_process'
    multirun_ana_files={an_name:[]}

    p_files=os.listdir(p)
    shellfns=[fn for fn in p_files if not '.' in fn]
    shellfn=shellfns[0]
    with open(os.path.join(p, shellfn), mode='r') as f:
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
        rcpd['file_dlist']+=[{'tech':'files_technique__SSRL', 'type':'csv_summary_files',  'fn':fn, 'fval':'ssrl_spec_csv_file;', 'folderpath':p}]

    sysname=os.path.split(p_processed)[1]
    h5path=os.path.join(os.path.join(p_processed, 'h5'), sysname+'.h5')
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
        multirun_ana_files[an_name]=[{'type':'fom_files', 'fn':xrfcsvfn, 'fval':'csv_fom_file;%s;1;%d' %(headline, len(gr['compositions'])), 'roi_keys_to_copy':roi_keys_to_copy, 'headline':headline}]


    xy_images=numpy.array(zip(gd['pmp_x'][:], gd['pmp_y'][:]))

    imdir=os.path.join(p, 'images')
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
    pck2dfolder=os.path.join(p_processed, 'pck2d')
    pck2dvalsfn='pck2d_chi_q_vals.pck'
    pck2dvalsp=os.path.join(os.path.split(p_processed)[0], pck2dvalsfn)
    if os.path.isdir(pck2dfolder) and os.path.isfile(pck2dvalsp):
        rcpd['file_dlist']+=[{'tech':'files_technique__SSRL', 'type':'pck2d_files',  'fn':pck2dvalsfn, 'fval':'ssrl_vals_pck_file;', 'folderpath':os.path.split(pck2dvalsp)[0]}]
        pck2d_fns=sorted([fn for fn in os.listdir(pck2dfolder) if fn.endswith('_chiq.pck')])#assuem this sorting gives the same ordering as the xys
        rcpd['file_dlist']+=[{'xyarr':xyarr,'tech':'files_technique__SSRL', 'type':'pck2d_files',  'fn':fn, 'fval':'ssrl_pck_file;', 'folderpath':pck2dfolder} for fn, xyarr in zip(pck2d_fns, xy_images)]
    rcpdlist=[rcpd]
    #h5f.close()#keep it open so don't need h5py in ExternalDataImportApp
    return {'rcpdlist':rcpdlist, 'multirun_ana_files':multirun_ana_files, 'h5f':h5f}#the fns in rcpdlist
#xyfiledlist xy files are not in rcpdind_fold_fn__tocopy. they get copied to ana folder instead but only if rcpdlist is >=0 and the rcpind gets put into the exp



#maindatad=get_externalimportdatad_ssrl_batchresults(p, p_processed=pp)

#p=r'K:\experiments\xrds\Lan\drop\35345_ZrV_550C_3h'
#h5f,maindatad=get_rcpdlist_xrdolfder(p)
#p=r'K:\experiments\xrds\user\Lan\MaterialsProject-2\Vanadates\35345_ZrV_550C_3h'
