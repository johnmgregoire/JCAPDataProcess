from xml.etree import ElementTree
import os, numpy, copy, time
from collections import OrderedDict as OD
p=r'K:\experiments\xrds\Lan\drop\35345_ZrV_550C_3h\data\Y-18-9_0_9.bsml'

#for node in tree.findall('.//TimePerStep'):
#    print node.tag, node.get('Value')





getxylist=lambda tree: [node.text.split(',')[:2] for node in tree.iter('Datum')]

def get_bmsl_dict(p):
    paramd={}
    
    with open(p, 'rt') as f:
        tree = ElementTree.parse(f)
    for node in tree.iter('TimePerStep'):
        #TODO: Dan fills in paramd with keywords from Lan
        paramd['TimePerStep']=node.attrib['Value']
    #TODO: generate YYYYMMDD.HHMMSS timestamp string
    timestamp=''
    try:
        xystr_list=getxylist(tree)
    except:
        return None
    return {'xystr_list':xystr_list, 'paramd':paramd, 'timestamp':timestamp}

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
            


def get_rcpdlist_xrdolfder(p):
    temptuplist=[(dirpath, fn) for dirpath, dirnames, filenames in os.walk(p) for fn in filenames if fn.endswith('.gfrm') or fn.endswith('.bsml')]
    g_tups=[(dp, fn) for dp, fn in temptuplist if fn.endswith('.gfrm')]
    b_tups=[(dp, fn) for dp, fn in temptuplist if fn.endswith('.bsml')]
    rcpdlist=[]
    rcpdind_pathstocopy=[]
    rcpind=-1#in case only gfrms
    for rcpind, (bfold, bfn) in enumerate(b_tups):
        rcpd={'files_technique__XRDS':{'bsml_files':[], 'gfrm_files':OD([]), 'TEMP_gfrm_xy':OD([])}}
        bname=bfn[:-5]#strip .bsml
        popinds=[count for count, (dp, fn) in enumerate(g_tups) if os.path.split(dp)[1]==bname and fn.startswith(bname)]
        if len(popinds)==0:
            print 'cannot find .gfrm files for %s in %s' %(bfn, bfold)
            raiseerror
        createtupfcn=lambda db_fn:tuple([eval(intstr.rstrip('.gfrm')) for intstr in db_fn[1].split('-')[-2:]]+list(db_fn))
        g__smpind_frameind_fold_fn=sorted([createtupfcn(g_tups.pop(i)) for i in popinds[::-1]])#sorted by sample ind then frame ind
        bsmld=get_bmsl_dict(os.path.join(bfold, bfn))
        rcpd['files_technique__XRDS']['bsml_files']=['%s: xrds_bruker_bsml_file;' %bfn]#only 1 of these per rcp
        rcpdind_pathstocopy+=[(rcpind, os.path.join(bfold, bfn))]
        for count, (xstr, ystr) in enumerate(bsmld['xystr_list']):
            xyarr=numpy.float64([eval(xstr), eval(ystr)])
            for smpind, frameind, gfold, gfn in g__smpind_frameind_fold_fn:#possibly not all gfrm got use but they were part of the bsml so they won't get treated as separate runs
                if smpind==count:
                    if gfn in rcpd['files_technique__XRDS']['gfrm_files'].keys():
                        print 'ERROR: mutliple gfrm found associated with the same bsml'
                        print bfold, bfn
                        print gfold, gfn
                        raiseerror
                    rcpd['files_technique__XRDS']['gfrm_files'][gfn]='xrds_bruker_gfrm_file;'
                    rcpd['files_technique__XRDS']['TEMP_gfrm_xy'][gfn]=xyarr
                    rcpdind_pathstocopy+=[(rcpind, os.path.join(gfold, gfn))]
        rcpd['name']=bsmld['timestamp']
        rcpd['parameters']=copy.deepcopy(bsmld['paramd'])
        rcpdlist+=[rcpd]

    for gfold, gfn in g_tups:
        rcpind+=1
        rcpd={'files_technique__XRDS':{'gfrm_files':OD([]), 'TEMP_gfrm_xy':OD([])}}
        timestampssecs=os.path.getmtime(os.path.join(gfold, gfn))
        ts=time.strftime('%Y%m%d.%H%M%S',time.gmtime(timestampssecs))
        while ts in [rcpdv['name'] for rcpdv in rcpdlist]:
            timestampssecs+=1
            ts=time.strftime('%Y%m%d.%H%M%S',time.gmtime(timestampssecs))
        
        xyarr=get_xy__solo_gfrm_fn(gfn)

        rcpd['name']=ts
        rcpd['files_technique__XRDS']['TEMP_gfrm_xy'][gfn]=xyarr
        rcpd['files_technique__XRDS']['gfrm_files'][gfn]='xrds_bruker_gfrm_file;'
        rcpdind_pathstocopy+=[(rcpind, os.path.join(gfold, gfn))]
        #TODO: add default parameters like Bruker name
        rcpdlist+=[rcpd]
    return rcpdind_pathstocopy, rcpdlist#the fns in rcpdlist


p=r'K:\experiments\xrds\Lan\drop\35345_ZrV_550C_3h'
rcpdind_pathstocopy, rcpdlist=get_rcpdlist_xrdolfder(p)
