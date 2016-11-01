from xml.etree import ElementTree
import os, numpy, copy, time
from collections import OrderedDict as OD
p=r'K:\users\hte\ProjectSummaries\Oxynitrides\La-Ta-O-N\15635\xrd\postacid\20160715\data\postacid.bsml'

#for node in tree.findall('.//TimePerStep'):
#    print node.tag, node.get('Value')


# tuple list for parsing bsml 2 cases:
#     1. xpath to taget tag is unique, 3-tuple (keyname, xpath_to_target_tag, target_attrib)
#     2. xpath to target tag is not unique, 6-tuple (keyname, xpath_to_parent_tag, match_parent_attrib, match_parent_value, target_tag, target_attrib)
#         2b. if target tag is empty string, parent node contains the desired attribute
bstuplist= [\
    ('machine_name', './/SerializedObject/Identifier', "IdentificationType", 'MeasurementLogic', '', ['MachineName']), \
    ('sample_id', './/SampleInfo/SampleId', ['Value']), \
    ('user', './/XmlFieldConnections/FieldRestrictionConnection', 'FieldName', 'User', './/Data', ['Value']), \
    ('comment', './/XmlFieldConnections/FieldRestrictionConnection', 'FieldName', 'Comment', './/Data', ['Value']), \
    ('exp_method', './/SerializedObject/BaseMethods/Method', ['AppType']), \
    ('xray_tube_type', './/MountedTube/Generator/Matcher', ['BeringObjectName']), \
    ('xray_tube_voltage', './/MountedTube/Generator/Voltage', ['Value', 'Unit']), \
    ('xray_tube_current', './/MountedTube/Generator/Current', ['Value', 'Unit']), \
    ('xray_tube_material', './/MountedTube/Generator/TubeMaterial', ['Value', 'Unit']), \
    ('slit_condition', './/MountedComponent/MountedOptic', ['VisibleName']), \
    ('collimator', './/BeamPathContainerAbc/BankPositions/BankPosition', 'BankPosition', '4', './/MountedComponent', ['VisibleName']), \
    ('detector_type', './/BeamPathContainerAbc/BankPositions/BankPosition', 'BankPosition', '0', './/MountedComponent', ['VisibleName']), \
    ('theta', './/DataEntityContainer/Data', 'VisibleName', 'Theta', './/Position', ['Value', 'Unit']), \
    ('2theta', './/DataEntityContainer/Data', 'VisibleName', 'Two Theta', './/Position', ['Value', 'Unit']), \
    ('psi', './/DataEntityContainer/Data', 'VisibleName', 'Psi', './/Position', ['Value', 'Unit']), \
    ('phi', './/DataEntityContainer/Data', 'VisibleName', 'Phi', './/Position', ['Value', 'Unit']), \
    ('beam_translation', './/DataEntityContainer/Data', 'VisibleName', 'Beam Transl.', './/Position', ['Value', 'Unit']), \
    ('beam_translation', './/DataEntityContainer/Data', 'VisibleName', 'Beam Transl.', './/Position', ['Value', 'Unit']), \
    ('track_distance', './/DataEntityContainer/Data', 'VisibleName', 'TrackDistance', './/Position', ['Value', 'Unit']), \
    ('motor_z', './/DataEntityContainer/Data', 'VisibleName', 'Z', './/Position', ['Value', 'Unit']), \
    ('scan_type', './/LogicData/DataEntityContainer', '{http://www.w3.org/2001/XMLSchema-instance}type', 'ScanSetup', '', ['VisibleName']), \
    ('integration_time', './/DataEntityContainer/TimePerStep', ['Value', 'Unit']), \
    ('frames_per_sample', './/DataEntityContainer/MeasurementPoints', ['Value', 'Unit']), \
    ('detector_serial', './/Detectors/DetectorList/DetectorData/SerialNumber', ['Value']), \
    ('detector_image_size_x', './/Detectors/DetectorList/DetectorData/ImageSizeX', ['Value', 'Unit']), \
    ('detector_image_size_y', './/Detectors/DetectorList/DetectorData/ImageSizeX', ['Value', 'Unit']), \
    ('face_to_detection_layer', './/Detectors/DetectorList/DetectorData/FaceToDetectionLayer', ['Value', 'Unit']), \
    ('header_name', './/Detectors/DetectorList/DetectorData/HeaderName', ['Value']) \
    ]

# special tuple list for theta/2theta setup values, needs 3 calls to .iterfind
thetatuplist= [\
    ('Start', ['Value', 'Unit']), \
    ('Increment', ['Value', 'Unit']), \
    ('End', ['Value', 'Unit']), \
    ]

getxylist=lambda tree: [node.text.split(',')[:2] for node in tree.iter('Datum')]
fmtbrukertimestamp=lambda s:s.partition('.')[0].replace('-','').replace(':','').replace('T','.')
def get_bmsl_dict(p):
    paramd={}

    with open(p, 'rt') as f:
        tree = ElementTree.parse(f)
    for tup in bstuplist:
        if len(tup)==3: # xpath to node is unique
            keyname, tpath, tattr = tup
            for node in tree.iterfind(tpath):
                paramd[keyname]=node.attrib[tattr[0]] if len(tattr)==1 else ' '.join([node.attrib[attr] for attr in tattr]).encode('utf-8').replace('\xb5','u').replace('\xb0','deg').replace('\xc2','')
        else: # xpath is not unique, find the correct node by matching parent attributes
            keyname, ppath, pattr, pval, tpath, tattr = tup
            for pnode in tree.iterfind(ppath):
                if pnode.attrib[pattr]==pval:
                    if tpath=='': # match part of multi-attribute node
                        paramd[keyname]=pnode.attrib[tattr[0]] if len(tattr)==1 else ' '.join([pnode.attrib[attr] for attr in tattr]).encode('utf-8').replace('\xb5','u').replace('\xb0','deg').replace('\xc2','')
                    else: # match parent attribute then iterate on children to find tag & value
                        for node in pnode.iterfind(tpath):
                            paramd[keyname]=node.attrib[tattr[0]] if len(tattr)==1 else ' '.join([node.attrib[attr] for attr in tattr]).encode('utf-8').replace('\xb5','u').replace('\xb0','deg').replace('\xc2','')

    # spectial matching for theta/2theta setup. there's got to be a better way of crawling through these nodes
    for gpnode in tree.iterfind('.//ScanAxisList/ScanAxis'):
        if gpnode.attrib['VisibleName'] in ['2Theta', 'Theta']:
            for tup in thetatuplist:
                for pnode in gpnode.iterfind('.//ScanParameterAbc'):
                    if pnode.attrib['VisibleName']==tup[0]:
                        for node in pnode.iterfind('.//Value'):
                            paramd['_'.join([gpnode.attrib['VisibleName'], tup[0]]).lower()]=' '.join([node.attrib[attr] for attr in tup[1]]).encode('utf-8').replace('\xb5','u').replace('\xb0','deg').replace('\xc2','')

    #TODO: generate YYYYMMDD.HHMMSS timestamp string
    timestr=[node for node in tree.iter('TimeStampSaved')][0].text
    timestamp=fmtbrukertimestamp(timestr)
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



def init_xy_file_dict(dp, fn, rcpdind_fold_fn__tocopy=[]):
    with open(os.path.join(dp, fn), mode='r') as f:
        s=f.read(100)
    gfn=s.partition('.gfrm')[0].rpartition(' ')[2]+'.gfrm'
    tuplist=[tup for tup in rcpdind_fold_fn__tocopy if tup[2]==gfn]
    if len(tuplist)==0:
        rcpind=-1
        gfold=''
    elif len(tuplist)==1:
        rcpind, gfold, gfn=tuplist[0]
    else:
        numcharsincommin=lambda p1, p2: numpy.array([c1==c2 for c1, c2 in zip(os.path.normpath(p1), os.path.normpath(p2))]).sum(dtype='int32')
        numchars, (rcpind, gfold, gfn)=sorted([(numcharsincommin, tup)] for tup in tuplist)[-1]#choose one with beginning path most similar
        print 'multiple gfrm matches for xy file %s  in folder %s with gfrm %s' %(fn, dp, gfn)
    nm='Analysis__XRDS_Bruker_Integrate' if 'original' in gfold else 'Analysis__XRDS_Bruker_Processed'
    return {'folderpath':dp, 'fn':fn, 'fn_gfrm':gfn, 'rcpind':rcpind, 'analysis_name':nm}

def get_rcpdlist_xrdolfder(p):
    temptuplist=[(dirpath, fn) for dirpath, dirnames, filenames in os.walk(p) for fn in filenames if fn.endswith('.gfrm') or fn.endswith('.bsml') or fn.endswith('.xy')]
    g_tups=[(dp, fn) for dp, fn in temptuplist if fn.endswith('.gfrm')]
    b_tups=[(dp, fn) for dp, fn in temptuplist if fn.endswith('.bsml')]
    e_tups=[(dp, fn) for dp, fn in temptuplist if fn.endswith('.xy')]
    rcpdlist=[]
    rcpdind_fold_fn__tocopy=[]
    rcpind=-1#in case only gfrms
    for rcpind, (bfold, bfn) in enumerate(b_tups):
        rcpd={'file_dlist':[]}
        #{'files_technique__XRDS':{'bsml_files':[], 'gfrm_files':OD([]), 'TEMP_xy':OD([])}}
        bname=bfn[:-5]#strip .bsml
        popinds=[count for count, (dp, fn) in enumerate(g_tups) if os.path.split(dp)[1]==bname and fn.startswith(bname)]
        if len(popinds)==0:
            print 'cannot find .gfrm files for %s in %s' %(bfn, bfold)
            raiseerror
        createtupfcn=lambda db_fn:tuple([eval(intstr.rstrip('.gfrm')) for intstr in db_fn[1].split('-')[-2:]]+list(db_fn))
        g__smpind_frameind_fold_fn=sorted([createtupfcn(g_tups.pop(i)) for i in popinds[::-1]])#sorted by sample ind then frame ind
        bsmld=get_bmsl_dict(os.path.join(bfold, bfn))
        rcpd['file_dlist']+=[{'tech':'files_technique__XRDS', 'type':'bsml_files',  'fn':bfn, 'fval':'xrds_bruker_bsml_file;'}]
        #rcpd['files_technique__XRDS']['bsml_files']=['%s: xrds_bruker_bsml_file;' %bfn]#only 1 of these per rcp
        rcpdind_fold_fn__tocopy+=[(rcpind, bfold, bfn)]
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
                    rcpd['file_dlist']+=[{'tech':'files_technique__XRDS', 'type':'gfrm_files',  'fn':gfn, 'fval':'xrds_bruker_gfrm_file;', 'xyarr':xyarr}]
                    rcpdind_fold_fn__tocopy+=[(rcpind, gfold, gfn)]
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

        rcpd['file_dlist']+=[{'tech':'files_technique__XRDS', 'type':'gfrm_files',  'fn':gfn, 'fval':'xrds_bruker_gfrm_file;', 'xyarr':xyarr}]
        
        rcpdind_fold_fn__tocopy+=[(rcpind, gfold, gfn)]
        #TODO: add default parameters like Bruker name
        rcpdlist+=[rcpd]

    xyfiledlist=[init_xy_file_dict(dp, fn, rcpdind_fold_fn__tocopy=rcpdind_fold_fn__tocopy) for dp, fn in e_tups]
    return {'rcpdind_fold_fn__tocopy':rcpdind_fold_fn__tocopy, 'rcpdlist':rcpdlist, 'auxfiledlist':xyfiledlist}#the fns in rcpdlist
    #xyfiledlist xy files are not in rcpdind_fold_fn__tocopy. they get copied to ana folder instead but only if rcpdlist is >=0 and the rcpind gets put into the exp


p=r'K:\experiments\xrds\Lan\drop\35345_ZrV_550C_3h'
#maindatad=get_rcpdlist_xrdolfder(p)
#p=r'K:\experiments\xrds\Lan\MaterialsProject-2\Vanadates\35345_ZrV_550C_3h'
