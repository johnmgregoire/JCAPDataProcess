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
            try:
                anad=readana(anapath)
            except:
                anapath=os.path.join(r'L:\processes', anapath[52:].replace('.zip', ''))
                try:
                    anad=readana(anapath)
                except:
                    print 'error reading ana,',  anapath
                    return
            
            ananame=anad['name']
            d[ananame]={'plate_id_str':pidstr, 'analysis':copy.copy(av)}
            exppath=buildexppath(anad['experiment_path'])
            try:
                expd=readexpasdict(exppath, returnzipclass=False)
            except:
                exppath=os.path.join(r'L:\processes', exppath[52:].replace('.zip', ''))
                try:
                    expd=readexpasdict(exppath, returnzipclass=False)
                except:
                    print 'error reading exp,',  exppath
                    return
            run_rel_path=expd['run__1']['run_path'].strip()
            runtime=None
            for rk, rv in infofiled['runs'].iteritems():
                if rv['path'].strip()==run_rel_path:
                    runtime=database_time_string_to_timestamp(rv['created_at'])
                    break
            if runtime is None:
                print 'error finding run,', run_rel_path
            if not 'prints' in infofiled.keys():
                return
            printkey, printd=get_most_recent_created_at(infofiled['prints'], beforetime=runtime)
            if printkey is None:
                return
            d[ananame]['print']=copy.copy(printd)
            
            if not 'anneals' in infofiled.keys():
                return
            annealkey, anneald=get_most_recent_created_at(infofiled['anneals'], beforetime=runtime)
            if annealkey is None:
                return
            d[ananame]['anneal']=copy.copy(anneald)
            
imag_ana_catalog={}
for pidstr in os.listdir(platefolder):
    add_entry_for_each_analysis(imag_ana_catalog, pidstr, anatype='imag')
    
savep=r'K:\users\hte\ProjectSummaries\metr_imag_classification\20180208_imag_metadata_dict_by_ananame.pck'
with open(savep, mode='wb') as f:
    pickle.dump(imag_ana_catalog, f)
