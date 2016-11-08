from xml.etree import ElementTree
import os, numpy, copy, time
from collections import OrderedDict as OD


def get_xy__solo_gfrm_fn(gfn):
    xyarr=numpy.ones(2, dtype='float64')*numpy.nan
    if gfn.count('pm')==2:
        xstr, ystr=gfn.split('pm')[1:3]
        xstr=xstr.lstrip('pmx').rstrip('_-')
        ystr=ystr.lstrip('pmy').rstrip('_.gfrm')
        try:
            xyarr=numpy.float64([eval(xstr), eval(ystr)])
        except:
            pass
    return xyarr



def xy_file_dict_into_rcpdlist(dp, fn, rcpdlist):
    with open(os.path.join(dp, fn), mode='r') as f:
        lines=f.readlines()
    gfn=lines[0].partition('.gfrm')[0].rpartition(' ')[2]+'.gfrm'
    fdlist=[fd for rcpd in rcpdlist for fd in rcpd['file_dlist'] if fd['fn']==gfn]
    if len(fdlist)==0:
        print 'cannot find .gfrm file for ', fn
        return True
    elif len(fdlist)==1:
        fd=fdlist[0]
    else:
        numcharsincommin=lambda p1, p2: numpy.array([c1==c2 for c1, c2 in zip(os.path.normpath(p1), os.path.normpath(p2))]).sum(dtype='int32')
        numchars, fd=sorted([(numcharsincommin(dp, fd['folderpath']), fd)] for fd in fdlist)[-1]#choose one with beginning path most similar
        print 'multiple gfrm matches for xy file %s  in folder %s with gfrm %s' %(fn, dp, gfn)
    an_name='Analysis__XRDS_Bruker_Integrate' if 'original' in dp else 'Analysis__XRDS_Bruker_Process'
    afd={'folderpath':dp, 'fn':fn, 'fn_gfrm':gfn, 'type':'misc_files', 'fval':'xrds_bruker_xy_csv_file;two_theta,intensity;1;%d;' %(len(lines)-1)}
    if not 'ana_files' in fd.keys():
        fd['ana_files']={}
    if not an_name in fd['ana_files'].keys():
        fd['ana_files'][an_name]=[]
    fd['ana_files'][an_name]+=[afd]
    return False
    


def get_externalimportdatad_ssrl_batchresults(p, p_processed=None, askforprocessed=True):#assume folder is for single .rcp
    if p_processed is None and askforprocessed:
        p_processed=str(mygetdir(parent=None, xpath=p,markstr='Folder containing processed data, e.g. pck2d' ))
        if p_processed is None or len(p_processed)==0:
            p_processed=None
    
    rcpd={'file_dlist':[]}
    an_name='Analysis__SSRL_batch_process'
    multirun_ana_files={an_name:[]}
    
    p_files=os.listdir(p)
    csvfns=[fn for fn in p_files if fn.endswith('.csv')]
    if len(csvfns)==1:#should only be 1 file that is the summary of spec info
        fn=csvfns[0]
        multirun_ana_files[an_name]+=[{'folderpath':p, 'fn':fn, 'type':'fom_files', 'fval':'csv_fom_file;'}]
        rcpd['file_dlist']+=[{'tech':'files_technique__SSRL', 'type':'csv_summary_files',  'fn':fn, 'fval':'ssrl_spec_csv_file;', 'folderpath':p}]
        
    imdir=os.path.join(p, 'images')
    if os.path.isdir(imdir):
        imdir_files=os.listdir(p)
        calibfns=sorted([fn for fn in imdir_files if fn.endswith('.calib')])
        if len(calibfns)>0:#many but only need 1
            fn=calibfns[0]
            multirun_ana_files[an_name]+=[{'folderpath':imdir, 'fn':fn, 'type':'misc_files', 'fval':'ssrl_misc_file;'}]
        tif_fns=[fn for fn in imdir_files if fn.endswith('.tif')]
        how to get xyarr?
        rcpd['file_dlist']+=[{'xyarr':xyarr,'tech':'files_technique__SSRL', 'type':'xrd_image_files',  'fn':fn, 'fval':'ssrl_mar_tiff_file;', 'folderpath':imdir} for fn in tif_fns]
    
    if not p_processed is None:
        
    temptuplist=[(dirpath, fn) for dirpath, dirnames, filenames in os.walk(p) for fn in filenames if fn.endswith('.gfrm') or fn.endswith('.bsml') or fn.endswith('.xy') or fn.endswith('.eva') or fn.endswith('.txt')]
    g_tups=[(dp, fn) for dp, fn in temptuplist if fn.endswith('.gfrm')]
    b_tups=[(dp, fn) for dp, fn in temptuplist if fn.endswith('.bsml')]
    e_tups=[(dp, fn) for dp, fn in temptuplist if fn.endswith('.xy')]
    m_tups=[(dp, fn) for dp, fn in temptuplist if fn.endswith('.eva')]
    t_tups=[(dp, fn) for dp, fn in temptuplist if fn.endswith('.txt')]
    rcpdlist=[]
    #rcpdind_fold_fn__tocopy=[]
    rcpind=-1#in case only gfrms
    for rcpind, (bfold, bfn) in enumerate(b_tups):
        rcpd={'file_dlist':[]}
        bname=bfn[:-5]#strip .bsml
        popinds=[count for count, (dp, fn) in enumerate(g_tups) if os.path.split(dp)[1]==bname and fn.startswith(bname)]
        if len(popinds)==0:
            print 'cannot find .gfrm files for %s in %s' %(bfn, bfold)
            raiseerror
        createtupfcn=lambda db_fn:tuple([eval(intstr.rstrip('.gfrm')) for intstr in db_fn[1].split('-')[-2:]]+list(db_fn))
        g__smpind_frameind_fold_fn=sorted([createtupfcn(g_tups.pop(i)) for i in popinds[::-1]])#sorted by sample ind then frame ind
        bsmld=get_bmsl_dict(os.path.join(bfold, bfn))
        rcpd['file_dlist']+=[{'tech':'files_technique__XRDS', 'type':'bsml_files',  'fn':bfn, 'fval':'xrds_bruker_bsml_file;', 'folderpath':bfold}]

        for count, (xstr, ystr) in enumerate(bsmld['xystr_list']):
            xyarr=numpy.float64([eval(xstr), eval(ystr)])
            for smpind, frameind, gfold, gfn in g__smpind_frameind_fold_fn:#possibly not all gfrm got use but they were part of the bsml so they won't get treated as separate runs
                if smpind==count:
                    if gfn in [tempd['fn'] for tempd in rcpd['file_dlist']]:
                    #if gfn in rcpd['files_technique__XRDS']['gfrm_files'].keys():
                        print 'ERROR: mutliple gfrm found associated with the same bsml'
                        print bfold, bfn
                        print gfold, gfn
                        raiseerror
                    rcpd['file_dlist']+=[{'tech':'files_technique__XRDS', 'type':'gfrm_files',  'fn':gfn, 'fval':'xrds_bruker_gfrm_file;', 'xyarr':xyarr, 'folderpath':gfold}]

        rcpd['name']=bsmld['timestamp']
        rcpd['parameters']=copy.deepcopy(bsmld['paramd'])
        rcpdlist+=[rcpd]

    for gfold, gfn in g_tups:
        rcpind+=1
        rcpd={'file_dlist':[]}
        timestampssecs=os.path.getmtime(os.path.join(gfold, gfn))
        ts=time.strftime('%Y%m%d.%H%M%S',time.gmtime(timestampssecs))
        while ts in [rcpdv['name'] for rcpdv in rcpdlist]:
            timestampssecs+=1
            ts=time.strftime('%Y%m%d.%H%M%S',time.gmtime(timestampssecs))

        xyarr=get_xy__solo_gfrm_fn(gfn)

        rcpd['name']=ts

        rcpd['file_dlist']+=[{'tech':'files_technique__XRDS', 'type':'gfrm_files',  'fn':gfn, 'fval':'xrds_bruker_gfrm_file;', 'xyarr':xyarr, 'folderpath':gfold}]
        rcpd['parameters']={}#other default paremetrs could be added here but at least need dictionary defined so plate_id can be added 

        rcpdlist+=[rcpd]
    for dp, fn in e_tups:
        find_gfrm_error_bool=xy_file_dict_into_rcpdlist(dp, fn, rcpdlist)
    multirun_ana_files={}
    multirun_ana_files['Analysis__Bruker_Eva']=[{'folderpath':dp, 'fn':fn, 'type':'misc_files', 'fval':'xrds_bruker_eva_file;'} for dp, fn in m_tups]
    multirun_ana_files['Analysis__User_Notes']=[{'folderpath':dp, 'fn':fn, 'type':'misc_files', 'fval':'xrds_user_txt_file;'} for dp, fn in t_tups]
    return {'rcpdlist':rcpdlist, 'multirun_ana_files':multirun_ana_files}#the fns in rcpdlist
    #xyfiledlist xy files are not in rcpdind_fold_fn__tocopy. they get copied to ana folder instead but only if rcpdlist is >=0 and the rcpind gets put into the exp


#p=r'K:\experiments\xrds\Lan\drop\35345_ZrV_550C_3h'
#maindatad=get_rcpdlist_xrdolfder(p)
#p=r'K:\experiments\xrds\user\Lan\MaterialsProject-2\Vanadates\35345_ZrV_550C_3h'
