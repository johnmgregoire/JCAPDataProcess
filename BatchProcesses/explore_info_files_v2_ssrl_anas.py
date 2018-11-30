import sys, os
############
projectroot=os.path.split(os.getcwd())[0]
sys.path.append(projectroot)
sys.path.append(os.path.join(projectroot,'QtForms'))
sys.path.append(os.path.join(projectroot,'AuxPrograms'))
sys.path.append(os.path.join(projectroot,'OtherApps'))
import operator, pickle
from fcns_io import *
#fix error of too many open files
#import win32file
#if win32file._getmaxstdio()<1000:
#    win32file._setmaxstdio(2048)

#from get_raw_data_from_exp import get_file_dicts_containing_data


platefolder=tryprependpath(PLATEFOLDERS, '')

def add_entry_for_each_analysis(d, pidstr, anatype='image'):
    infop=os.path.join(os.path.join(platefolder, pidstr), pidstr+'.info')
    if not os.path.isfile(infop):
        return
    with open(infop, mode='r') as f:
        lines=f.readlines()
        infofiled=filedict_lines(lines)
    if not 'analyses' in infofiled.keys():
        return
    for ak, av in infofiled['analyses'].iteritems():
        if 'type' in av.keys() and av['type']==anatype:
            anapath=buildanapath(av['path'])
#            try:
#                anad=readana(anapath)
#            except:
#                anapath=os.path.join(r'L:\processes', anapath[52:].replace('.zip', ''))
#                try:
#                    anad=readana(anapath)
#                except:
#                    print 'error reading ana,',  anapath
#                    return
            ellist=getelements_plateidstr(infofiled, exclude_elements_list=['Ar', 'O'])
            #ananame=anad['name']
            ananame=av['path'].rpartition(r'/')[2]
            d[ananame]={'plate_id_str':pidstr, 'analysis':copy.copy(av), 'anapath':anapath, 'ellist':ellist}
#            if 'screening_map_id' in infofiled.keys():
#                d[ananame]['screening_map_id']=infofiled['screening_map_id']
#            exppath=buildexppath(anad['experiment_path'])
#            try:
#                expd=readexpasdict(exppath, returnzipclass=False)
#            except:
#                exppath=os.path.join(r'L:\processes', exppath[52:].replace('.zip', ''))
#                try:
#                    expd=readexpasdict(exppath, returnzipclass=False)
#                except:
#                    print 'error reading exp,',  exppath
#                    return
#            run_rel_path=expd['run__1']['run_path'].strip()
#            runtime=None
#            for rk, rv in infofiled['runs'].iteritems():
#                if rv['path'].strip()==run_rel_path:
#                    runtime=database_time_string_to_timestamp(rv['created_at'])
#                    break
#            if runtime is None:
#                print 'error finding run,', run_rel_path
#            if not 'prints' in infofiled.keys():
#                return
#            printkey, printd=get_most_recent_created_at(infofiled['prints'], beforetime=runtime)
#            if printkey is None:
#                return
#            d[ananame]['print']=copy.copy(printd)
#            
#            if not 'anneals' in infofiled.keys():
#                return
#            annealkey, anneald=get_most_recent_created_at(infofiled['anneals'], beforetime=runtime)
#            if annealkey is None:
#                return
#            d[ananame]['anneal']=copy.copy(anneald)
            
ana_catalog={}
for pidstr in os.listdir(platefolder):
    add_entry_for_each_analysis(ana_catalog, pidstr, anatype='ssrl')
    
#savep=r'K:\users\hte\ProjectSummaries\3 cation oxides\2018_ssrl_analysis\20181008_srrl_ana_search.pck'
#with open(savep, mode='wb') as f:
#    pickle.dump(ana_catalog, f)
