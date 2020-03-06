import numpy, copy, operator
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AnalysisFunctions'))

from fcns_io import *
from fcns_ui import *



def merge_interp_xrfs_single_plate_id(calcui, ananame=None, pidstr=None, fom_keys='ALL', l_anak_to_merge=['ana__1'],xrfs_ana_int='highest containing search string', atfrac_search_string='AtFrac', interpmerge=True, save_extension='.run'):
    if not ananame is None:#send None if already importana in calcui so extra import -> copy avoided
        anapath=buildanapath(ananame)
        calcui.importana(p=anapath)
    if pidstr is None:
        pidstr=calcui.anadict['plate_ids']
    if ',' in pidstr:
        print 'aborting xrfs merge, only written for single plate_id and in this ana includes :', pidstr
        return None
    infod=importinfo(pidstr)
    #for ank in sort_dict_keys_by_counter(infod['analyses'], keystartswith='analyses__'):#use
    analysesd=infod['analyses']
    xrfstups=sorted([(time.strptime(v['created_at'].rpartition(' ')[0],'%Y-%m-%d %H:%M:%S'), v) for k, v in analysesd.iteritems() if v['type']=='xrfs'])
    if len(xrfstups)==0:
        print 'aborting xrfs merge, xrfs data for ', pidstr
        return None
    relapth_xrfsana=xrfstups[-1][1]['path']#latest created_at analyses__ dict

    calcui.importauxexpana(relapth_xrfsana, exp=False)
    xrfs_anad=calcui.aux_ana_dlist[0]

    if not isinstance(xrfs_ana_int, int):
        anakeys=sort_dict_keys_by_counter(xrfs_anad)
        for anak in anakeys[::-1]:
            if not ('files_multi_run' in xrfs_anad[anak].keys() and 'fom_files' in xrfs_anad[anak]['files_multi_run'].keys()):
                continue
            for fn, filed in xrfs_anad[anak]['files_multi_run']['fom_files'].iteritems():
                numcompfoms=len([True for k in filed['keys'] if atfrac_search_string in k])
                if numcompfoms>1:
                    xrfs_ana_int=int(anak[5:])
                    print 'using xrfs ', anak
                    break
    if not isinstance(xrfs_ana_int, int):
        print 'aborting xrfs merge, no ana__ found containing more than 1 fom with ', atfrac_search_string
        return None

    anakeys0=sort_dict_keys_by_counter(calcui.anadict)
    for anak_to_merge in l_anak_to_merge:
        for i in range(1, int(calcui.FOMProcessNamesComboBox.count())):
            if (str(calcui.FOMProcessNamesComboBox.itemText(i)).partition('(')[0])=='Analysis__FOM_Interp_Merge_Ana' if interpmerge else 'Analysis__FOM_Merge_Ana':
                calcui.FOMProcessNamesComboBox.setCurrentIndex(i)
                calcui.getactiveanalysisclass()
                calcui.processeditedparams()
                break
        c=calcui.analysisclass

        c.params['select_aux_keys']=atfrac_search_string
        c.params['select_aux_ints']=`xrfs_ana_int`
        c.params['select_fom_keys']=fom_keys

        if interpmerge:
            c.params['interp_is_comp']=1
        else:
            print 'aborting xrfs merge, asked for direct merge but not supported yet'
            return None

        c.params['select_ana']=anak_to_merge
        c.processnewparams(calcFOMDialogclass=calcui, recalc_filedlist=True)
        calcui.analyzedata()
    anakeys1=sort_dict_keys_by_counter(calcui.anadict)
    if len(anakeys1)<(len(l_anak_to_merge)+len(anakeys0)):
        if len(anakeys1)==len(anakeys0):
            print 'aborting xrfs merge, merge failed within analysis function'
            return None
        else:
            print 'continuing with xrfs merge but not all requested ana__ were succesfully merged'

    if not save_extension is None:
        newanasavefolder=calcui.saveana(dontclearyet=False, anatype=calcui.anadict['analysis_type'], rundone=save_extension)
        newanapath=buildanapath(newanasavefolder)
        return newanapath
