import numpy, copy,sys,os
if __name__ == "__main__":
    sys.path.append(os.path.split(os.getcwd())[0])

sys.path.append(os.path.split(os.path.realpath(__file__))[0])

from fcns_math import *
from fcns_io import *
from csvfilewriter import createcsvfilstr
from Analysis_Master import *





#    def stdgetapplicablefomfiles(anadict, params={}):
#    
#    if 'select_ana_keys' in params.keys() and params['select_ana_keys'].startswith('ana__'):#filter to only use refs from user-specified list
#        analist=params['select_ana_keys'].split(',')
#        analist=[s.strip() for s in analist]
#    else:
#        analist=[anak for anak in anadict.keys() if anak.startswith('ana__')]
#    
#    if 'analysis_name_contains' in params.keys():
#        analysis_name_contains=params['analysis_name_contains'].strip()
#    else:
#        analysis_name_contains=''
#    
#    anak_list=[anak for anak, anav in anadict.iteritems()\
#           if (anak in analist) and (analysis_name_contains in anav['name']) and ('files_multi_run' in anav.keys()) and ('fom_files' in anav['files_multi_run'].keys())]
#
#    if 'select_fom_keys' in params.keys() and len(params['select_fom_keys'].strip())>0:
#        selkeyslist=params['select_fom_keys'].split(',')
#        selkeyslist=[s.strip() for s in selkeyslist]
#        keystestfcn=lambda tagandkeys: True in [k in tagandkeys.split(';')[1].split(',') for k in selkeyslist]
#        keysfcn=lambda tagandkeys: list(set(tagandkeys.split(';')[1].split(',')).intersection(set(selkeyslist)))
#    else:    
#        keystestfcn=lambda tagandkeys: len(set(tagandkeys.split(';')[1].split(',')).difference(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING))>0
#        keysfcn=lambda tagandkeys: list(set(tagandkeys.split(';')[1].split(',')).difference(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING))
#        
#        #goes through all inter_files and inter_rawlen_files in all analyses with this correct 'name'. This could be multiple analysis on different runs but if anlaysis done multiple times with different parameters, there is no disambiguation so such sampels are skipped.
#    ##the 'ftk==('files_'+filed['run'])" condition means the run of the raw data is matched to the run in the analysis and this implied that the plate_id is match so matching sample_no would be sufficient, but matching the filename is easiest for now.  #('__'+os.path.splitext(filed['fn'])[0]) in fnk
#    #this used to use [anak, ftk, typek, fnk] but anadict is not available in perform() so use filename because it is the same .ana so should be in same folder
#    filedlist=\
#          [{'anakeys':[anak, 'files_multi_run', 'fom_files', fnk], 'ana':anak, 'fn':fnk, 'keys':tagandkeys.split(';')[1].split(','), 'num_header_lines':int(tagandkeys.split(';')[2]), 'process_keys':keysfcn(tagandkeys)}\
#            for anak in anak_list \
#            for fnk, tagandkeys in anadict[anak]['files_multi_run']['fom_files'].iteritems()\
#                if keystestfcn(tagandkeys)\
#          ]
#
#    return len([anak for anak in anadict.keys() if anak.startswith('ana__')]), filedlist

FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING=set(['sample_no', 'runint', 'plate_id'])
def stdgetapplicablefomfiles(anadict, params={}):
    
    if (not 'select_ana' in params.keys()) or (not params['select_ana'] in anadict.keys()) or (not isinstance(anadict[params['select_ana']], dict)):
        return len([anak for anak in anadict.keys() if anak.startswith('ana__')]), []
        
    anak_list=[anak for anak, anav in anadict.iteritems()\
           if (anak==params['select_ana'].strip()) and ('files_multi_run' in anav.keys()) and ('fom_files' in anav['files_multi_run'].keys())]#only 1 anak allowed but still keep as list and below list could have multiple fom_files in the same ana__x

    if 'select_fom_keys' in params.keys() and len(params['select_fom_keys'].strip('*'))>0:
        selkeyslist=params['select_fom_keys'].split(',')
        selkeyslist=[s.strip() for s in selkeyslist]
        keystestfcn=lambda tagandkeys: (True in [k in tagandkeys.split(';')[1].split(',') for k in selkeyslist]) and len(set(tagandkeys.split(';')[1].split(',')).intersection(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING))==len(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)
        keysfcn=lambda tagandkeys: list(set(tagandkeys.split(';')[1].split(',')).intersection(set(selkeyslist)))
    else:    
        keystestfcn=lambda tagandkeys: len(set(tagandkeys.split(';')[1].split(',')).intersection(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING))==len(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)
        keysfcn=lambda tagandkeys: list(set(tagandkeys.split(';')[1].split(',')).difference(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING))
        
        #goes through all inter_files and inter_rawlen_files in all analyses with this correct 'name'. This could be multiple analysis on different runs but if anlaysis done multiple times with different parameters, there is no disambiguation so such sampels are skipped.
    ##the 'ftk==('files_'+filed['run'])" condition means the run of the raw data is matched to the run in the analysis and this implied that the plate_id is match so matching sample_no would be sufficient, but matching the filename is easiest for now.  #('__'+os.path.splitext(filed['fn'])[0]) in fnk
    #this used to use [anak, ftk, typek, fnk] but anadict is not available in perform() so use filename because it is the same .ana so should be in same folder
    filedlist=\
          [{'anakeys':[anak, 'files_multi_run', 'fom_files', fnk], 'ana':anak, 'fn':fnk, 'keys':tagandkeys.split(';')[1].split(','), 'num_header_lines':int(tagandkeys.split(';')[2]), 'process_keys':keysfcn(tagandkeys)}\
            for anak in anak_list \
            for fnk, tagandkeys in anadict[anak]['files_multi_run']['fom_files'].iteritems()\
                if keystestfcn(tagandkeys)\
          ]

    return len([anak for anak in anadict.keys() if anak.startswith('ana__')]), filedlist


class Analysis_Master_FOM_Process(Analysis_Master_nointer):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={'select_ana': 'ana__1', 'select_fom_keys':'*'}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis_Master_FOM_Process'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=[]
        self.plotparams=dict({}, plot__1={})
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
    
    
    def getgeneraltype(self):#make this fucntion so it is inhereted
        return 'processfom'
        
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):#just a wrapper around getapplicablefomfiles to keep same argument format as other AnalysisClasses
        return self.getapplicablefomfiles(anadict)
        
    def getapplicablefomfiles(self, anadict):
        if not anadict is None and self.params['select_ana'] in anadict.keys() and 'plot_parameters' in anadict[self.params['select_ana']]:
            self.plotparams=copy.deepcopy(anadict[self.params['select_ana']]['plot_parameters'])
            
        self.num_ana_considered, self.filedlist=stdgetapplicablefomfiles(anadict, params=self.params)#has to be called filedlist tro work with other analysis fcns
        #self.filedlist=[dict(d, user_run_foms={}) for d in self.filedlist]#has to be here because only place with access to expfiledict
        self.description='process %s' %self.params['select_ana']
        return self.filedlist
    
    def check_input(self, critfracapplicable=0):
        fracapplicable=1.*len(self.filedlist)/self.num_ana_considered
        return fracapplicable>critfracapplicable, \
        '%d ana__, %.2f of those available, do not meet requirements' %(self.num_ana_considered-len(self.filedlist), 1.-fracapplicable)
    def check_output(self, critfracnan=0.9):
        return True, \
        'No output check for Process FOM'

    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}):#must have same arguments as regular AnaylsisClass
        self.initfiledicts()
        for filed in self.filedlist:
            self.strkeys_fomdlist=[]
#            if numpy.isnan(filed['sample_no']):
#                if self.debugmode:
#                    raiseTEMP
#                continue
            fn=filed['fn']
            try:
                fomd, self.csvheaderdict=readcsvdict(os.path.join(destfolder, fn), filed, returnheaderdict=True, zipclass=None, includestrvals=False)#str vals not allowed because not sure how to "filter/smooth" and also writefom, headerdictwill be re-used in processed version
                self.fomnames=list(set(fomd.keys()).difference(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING))#this is to emulate otherAnalysisClass for self.writefom()
                process_keys=filed['process_keys']
                along_for_the_ride_keys=list(set(fomd.keys()).difference(set(process_keys)))
                #dataarr=self.readdata(os.path.join(destfolder, fn), len(filed['keys']), None, num_header_lines=filed['num_header_lines'], zipclass=None)
                self.fomdlist=self.process_fomd(fomd, process_keys, along_for_the_ride_keys)#this function "transposes" data to emulate AnalysisClass
            except:
                if self.debugmode:
                    raiseTEMP
                print 'skipped filter/smooth of file ', fn
                self.fomdlist=[]
                continue
            self.writefom(destfolder, anak, anauserfomd=anauserfomd, strkeys_fomdlist=self.strkeys_fomdlist)#sample_no, plate_id and runint are explicitly required in csv selection above and are assume to be present here

        
class Analysis__FilterSmoothFromFile(Analysis_Master_FOM_Process):#THE PCK-BASED PROCESSING AS SAMPLE_NO BASED AND NEED NOT PAY ATTENTION TO PLATE_ID
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={'select_ana': 'ana__1', 'select_fom_keys':'*','ignore_if_any_nan':0, 'sorted_ind_start':0, 'sorted_ind_stop':999, 'nsig_remove_outliers':999.}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__FilterSmoothFromFile'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=[]
        self.plotparams=dict({}, plot__1={})
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.filter_path__runint={}
    
    def process_fomd(self, fomd, process_keys, along_for_the_ride_keys):
        i0=self.params['sorted_ind_start']
        i1=self.params['sorted_ind_stop']
        numstd=self.params['nsig_remove_outliers']
        ignorebool=self.params['ignore_if_any_nan']
        runintset=sorted(list(set(fomd['runint'])))
        
        d_smpstoave__runint={}
        for runint in runintset:
            with open(self.filter_path__runint[runint], mode='rU') as f:
                d_smpstoave__runint[runint]=pickle.load(f)

        d_smpstoave=dict([(sample_no, d_smpstoave__runint[runint][sample_no]) for (runint, sample_no) in zip(fomd['runint'], fomd['sample_no']) if sample_no in d_smpstoave__runint[runint].keys()])#creates sample-index dict that combines all runs and potentially plates. THE PCK-BASED PROCESSING AS SAMPLE_NO BASED AND NEED NOT PAY ATTENTION TO PLATE_ID
        smplist=list(fomd['sample_no'])
        smpkey_reprinds=[(sample_no, smplist.index(sample_no)) for sample_no in d_smpstoave.keys()]
        
        
        fomdlist=[]
        strk='SmpRunPlate_Association'
        for smpkey, repind in smpkey_reprinds:
            inds=[smplist.index(sample_no) for sample_no in d_smpstoave[smpkey] if sample_no in smplist]
            fd={}
            fd[strk]=';'.join(['_'.join([str(fomd[k][i]) for k in ['sample_no', 'runint', 'plate_id']]) for i in inds])
            for k in along_for_the_ride_keys:
                fd[k]=fomd[k][repind]
            for k in process_keys:
                arr=fomd[k][inds]
                if numpy.all(numpy.isnan(arr)) or (ignorebool and numpy.any(numpy.isnan(arr))):
                    fd[k]=numpy.nan
                    continue
                arr=arr[numpy.logical_not(numpy.isnan(arr))]
                #stddevremoval***
                
                if len(arr)>1 and numstd<999.:
                    arr2=numpy.abs((arr-arr.mean())/arr.std())
                    while (len(arr)>1) and numpy.max(arr2)>numstd:
                        arr=numpy.delete(arr, arr2.argmax())
                        arr2=numpy.abs((arr-arr.mean())/arr.std())
                arr=arr[numpy.argsort(arr)]
                fd[k]=arr[i0:i1].mean()
            fomdlist+=[fd]
        self.strkeys_fomdlist=[strk]
        return fomdlist

class Analysis__AveCompDuplicates(Analysis_Master_FOM_Process):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={'select_ana': 'ana__1', 'select_fom_keys':'*', 'crit_comp_dist':0.0005, 'sorted_ind_start':0, 'sorted_ind_stop':999}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__AveCompDuplicates'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=[]
        self.plotparams=dict({}, plot__1={})
#        self.plotparams['plot__1']['x_axis']='t(s)'
#        self.plotparams['plot__1']['series__1']='I(A)'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):#in addition to standard requirements, platemapdlist must be defined for all runs - for simplicity require for all runs in expfiledict even if they are not used in ana__x
        if False in ['platemapdlist' in rund.keys() for runk, rund in expfiledict.iteritems() if runk.startswith('run__')]:
            self.num_ana_considered=1
            self.filedlist=[]
            return []
        self.platemapdlist_runint=dict([(int(runk.partition('__')[2]), rund['platemapdlist']) for runk, rund in expfiledict.iteritems() if runk.startswith('run__')])
        return self.getapplicablefomfiles(anadict)
    
    def process_fomd(self, fomd, process_keys, along_for_the_ride_keys):
        compdelta=self.params['crit_comp_dist']
        i0=self.params['sorted_ind_start']
        i1=self.params['sorted_ind_stop']
        
        samples_runint=dict([(runint, [d['sample_no'] for d in dlist]) for runint, dlist in self.platemapdlist_runint.iteritems()])
        platemapsampled=lambda runint, sample_no:self.platemapdlist_runint[runint][samples_runint[runint].index(sample_no)] if sample_no in samples_runint[runint] else None
        indstoprocess=range(len(fomd['sample_no']))
        mappedplated=[platemapsampled(runint, sample_no) for (runint, sample_no) in zip(fomd['runint'], fomd['sample_no'])]
        code=numpy.array([d['code'] for d in mappedplated])
        comps=numpy.float32([[d[el] if el in d.keys() else 0. for el in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']] for d in mappedplated])#comps are NOT normalized so that different thicknesses tdo not get averaged together
        inds_compsdist=lambda c1:numpy.where(numpy.float32([((c1-c2)**2).sum()/2.**.5 for c2 in comps])<=compdelta)[0]
        fomdlist=[]
        strk='SmpRunPlate_Association'
        while len(indstoprocess)>0:
            if numpy.any(numpy.isnan(comps[indstoprocess[0]])):
                inds=[indstoprocess[0]]
            else:
                inds=inds_compsdist(comps[indstoprocess[0]])
            repind=inds[numpy.argmin(code[inds])]
            fd={}
            fd[strk]=';'.join(['_'.join([str(fomd[k][i]) for k in ['sample_no', 'runint', 'plate_id']]) for i in inds])
            for k in along_for_the_ride_keys:
                fd[k]=fomd[k][repind]
            for k in process_keys:
                arr=fomd[k][inds]
                arr=arr[numpy.logical_not(numpy.isnan(arr))]
                if len(arr)==0:
                    fd[k]=numpy.nan
                    continue
                arr=arr[numpy.argsort(arr)]
                fd[k]=arr[i0:i1].mean()
            fomdlist+=[fd]
            indstoprocess=sorted(list(set(indstoprocess).difference(set(inds))))
        self.strkeys_fomdlist=[strk]
        return fomdlist

##SIMPLE DUMMY DATA TEST
#c=Analysis__AveCompDuplicates()
#
#c.platemapdlist_runint={}
#c.platemapdlist_runint[1]=[{'sample_no':4, 'A':.4, 'C':0, 'code':100}, {'sample_no':6, 'A':.4, 'C':0.2, 'code':0}, {'sample_no':8, 'A':.2, 'C':0.2, 'code':0}]
#c.platemapdlist_runint[2]=[{'sample_no':9, 'A':.4, 'C':0., 'code':0}, {'sample_no':11, 'A':.41, 'C':0.2, 'code':0}]
#c.params['crit_comp_dist']=0.01
#c.params['sorted_ind_start']=-1
#fomd={'sample_no':numpy.array([4, 6, 8, 9, 11]), 'runint':numpy.array([1, 1, 1, 2, 2]), 'z':numpy.array([1., 10., 100., 1000., 10000.])}
#fdl=c.process_fomd(fomd, ['z'], ['sample_no','runint'])

##TEST ANALYSIS__AVECOMPDUPLICATES
#exppath=r'\\htejcap.caltech.edu\share\home\processes\experiment\temp\20151019.165501.done\20151019.165501.exp'
#anapath=r'\\htejcap.caltech.edu\share\home\processes\analysis\temp\20151020.145208.run\20151020.145208.ana'
#expfiledict, expzipclass=readexpasdict(exppath, includerawdata=False, erroruifcn=None, returnzipclass=True)
#anadict=readana(anapath, stringvalues=True)
#destfolder=os.path.split(anapath)[0]
#
#FilterSmoothMapDict={}
#
#for runk, rund in expfiledict.iteritems():
#    if runk.startswith('run__') and not 'platemapdlist' in rund.keys()\
#             and 'parameters' in rund.keys() and isinstance(rund['parameters'], dict)\
#             and 'plate_id' in rund['parameters'].keys():
#        rund['platemapdlist']=readsingleplatemaptxt(getplatemappath_plateid(str(rund['parameters']['plate_id'])))
#    if runk.startswith('run__') and not 'platemap_id' in rund.keys():
#        rund['platemap_id']=getplatemapid_plateidstr(str(rund['parameters']['plate_id']))
#platemapids=[rund['platemap_id'] for runk, rund in expfiledict.iteritems() if runk.startswith('run__') and 'platemap_id' in rund]
#FilterSmoothMapDict=generate_filtersmoothmapdict_mapids(platemapids)
#
#c=Analysis__AveCompDuplicates()
#c.params['crit_comp_dist']=0.0005
#c.getapplicablefilenames(expfiledict, '', '', '', runklist=None, anadict=anadict)
#c.perform(destfolder)
#
#
#
#filed=c.filedlist[0]
#fn=filed['fn']
#fomd, csvheaderdict=readcsvdict(os.path.join(destfolder, fn), filed, returnheaderdict=True, zipclass=None, includestrvals=False)#str vals not allowed because not sure how to "filter/smooth" and also writefom, headerdictwill be re-used in processed version
#fomnames=list(set(fomd.keys()).difference(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING))#this is to emulate otherAnalysisClass for self.writefom()
#process_keys=filed['process_keys']
#along_for_the_ride_keys=list(set(fomd.keys()).difference(set(process_keys)))
#compdelta=c.params['crit_comp_dist']
#i0=c.params['sorted_ind_start']
#i1=c.params['sorted_ind_stop']
#samples_runint=dict([(runint, [d['sample_no'] for d in dlist]) for runint, dlist in c.platemapdlist_runint.iteritems()])
#
#platemapsampled=lambda runint, sample_no:c.platemapdlist_runint[runint][samples_runint[runint].index(sample_no)] if sample_no in samples_runint[runint] else None
#indstoprocess=range(len(fomd['sample_no']))
#mappedplated=[platemapsampled(runint, sample_no) for (runint, sample_no) in zip(fomd['runint'], fomd['sample_no'])]
#code=numpy.array([d['code'] for d in mappedplated])
#comps=numpy.float32([[d[el] if el in d.keys() else 0. for el in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']] for d in mappedplated])#comps are NOT normalized so that different thicknesses tdo not get averaged together
#inds_compsdist=lambda c1:numpy.where(numpy.float32([((c1-c2)**2).sum()/2.**.5 for c2 in comps])<=compdelta)[0]
#fomdlist=[]
#
#if numpy.any(numpy.isnan(comps[indstoprocess[0]])):
#    inds=[indstoprocess[0]]
#else:
#    inds=inds_compsdist(comps[indstoprocess[0]])
#repind=inds[numpy.argmin(code[inds])]
#
#k=process_keys[0]
#arr=fomd[k][inds]
#arr=arr[numpy.logical_not(numpy.isnan(arr))]
#
#arr=arr[numpy.argsort(arr)]
#ans=arr[i0:i1].mean()


###TEST Analysis__FilterSmoothFromFile
#exppath=r'\\htejcap.caltech.edu\share\home\processes\experiment\temp\20151020.090148.done\20151020.090148.exp'
#anapath=r'\\htejcap.caltech.edu\share\home\processes\analysis\temp\20151020.203002.run\20151020.203002.ana'
#
#
#expfiledict, expzipclass=readexpasdict(exppath, includerawdata=False, erroruifcn=None, returnzipclass=True)
#anadict=readana(anapath, stringvalues=True)
#destfolder=os.path.split(anapath)[0]
#
#FilterSmoothMapDict={}
#
#for runk, rund in expfiledict.iteritems():
#    if runk.startswith('run__') and not 'platemapdlist' in rund.keys()\
#             and 'parameters' in rund.keys() and isinstance(rund['parameters'], dict)\
#             and 'plate_id' in rund['parameters'].keys():
#        rund['platemapdlist']=readsingleplatemaptxt(getplatemappath_plateid(str(rund['parameters']['plate_id'])))
#    if runk.startswith('run__') and not 'platemap_id' in rund.keys():
#        rund['platemap_id']=getplatemapid_plateidstr(str(rund['parameters']['plate_id']))
#platemapids=[rund['platemap_id'] for runk, rund in expfiledict.iteritems() if runk.startswith('run__') and 'platemap_id' in rund]
#FilterSmoothMapDict=generate_filtersmoothmapdict_mapids(platemapids)
#
#c=Analysis__FilterSmoothFromFile()
#c.filter_path__runint={}
#c.filter_path__runint[1]=r'\\htejcap.caltech.edu\share\home\experiments\eche\FilterSmoothMaps\0049-04-0830-mp_dneighbor_code130.pck'
#
#c.getapplicablefomfiles(anadict)
#c.perform(destfolder)
#
#
#
#filed=c.filedlist[0]
#fn=filed['fn']
#fomd, csvheaderdict=readcsvdict(os.path.join(destfolder, fn), filed, returnheaderdict=True, zipclass=None, includestrvals=False)#str vals not allowed because not sure how to "filter/smooth" and also writefom, headerdictwill be re-used in processed version
#fomnames=list(set(fomd.keys()).difference(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING))#this is to emulate otherAnalysisClass for self.writefom()
#process_keys=filed['process_keys']
#along_for_the_ride_keys=list(set(fomd.keys()).difference(set(process_keys)))
#compdelta=c.params['crit_comp_dist']
#i0=c.params['sorted_ind_start']
#i1=c.params['sorted_ind_stop']
#
#
#i0=c.params['sorted_ind_start']
#i1=c.params['sorted_ind_stop']
#numstd=c.params['nsig_remove_outliers']
#ignorebool=c.params['ignore_if_any_nan']
#runintset=sorted(list(set(fomd['runint'])))
#        
#d_smpstoave__runint={}
#for runint in runintset:
#    with open(c.filter_path__runint[runint], mode='rU') as f:
#        d_smpstoave__runint[runint]=pickle.load(f)
#
#d_smpstoave=dict([(sample_no, d_smpstoave__runint[runint][sample_no]) for (runint, sample_no) in zip(fomd['runint'], fomd['sample_no']) if sample_no in d_smpstoave__runint[runint].keys()])#creates sample-index dict that combines all runs and potentially plates. THE PCK-BASED PROCESSING AS SAMPLE_NO BASED AND NEED NOT PAY ATTENTION TO PLATE_ID
#smplist=list(fomd['sample_no'])
#smpkey_reprinds=[(sample_no, smplist.index(sample_no)) for sample_no in d_smpstoave.keys()]
#strk='strk'
#smpkey, repind = smpkey_reprinds[0]
#inds=[smplist.index(sample_no) for sample_no in d_smpstoave[smpkey] if sample_no in smplist]
#fd={}
#fd[strk]=';'.join(['_'.join([str(fomd[k][i]) for k in ['sample_no', 'runint', 'plate_id']]) for i in inds])
#for k in along_for_the_ride_keys:
#    fd[k]=fomd[k][repind]
#for k in process_keys:
#    arr=fomd[k][inds]
#    if numpy.all(numpy.isnan(arr)) or (ignorebool and numpy.any(numpy.isnan(arr))):
#        fd[k]=numpy.nan
#        continue
#    arr=arr[numpy.logical_not(numpy.isnan(arr))]
#   #stddevremoval***
#    
#    if len(arr)>1 and numstd<999.:
#        arr2=numpy.abs((arr-arr.mean())/arr.std())
#        while (len(arr)>1) and numpy.max(arr2)>numstd:
#            arr=numpy.delete(arr, arr2.argmax())
#            arr2=numpy.abs((arr-arr.mean())/arr.std())
#    arr=arr[numpy.argsort(arr)]
#    fd[k]=arr[i0:i1].mean()
#    
