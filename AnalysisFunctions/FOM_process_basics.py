import numpy, copy,sys,os
if __name__ == "__main__":
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))

from fcns_math import *
from fcns_io import *
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

    if 'select_fom_keys' in params.keys() and not params['select_fom_keys'].startswith('ALL')>0:
        selkeyslist=params['select_fom_keys'].split(',')
        selkeyslist=[s.strip() for s in selkeyslist]
        keystestfcn=lambda tagandkeys: (True in [k in tagandkeys.split(';')[1].split(',') for k in selkeyslist]) and len(set(tagandkeys.split(';')[1].split(',')).intersection(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING))==len(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)
        keysfcn=lambda tagandkeys: list(set(tagandkeys.split(';')[1].split(',')).intersection(set(selkeyslist)))
    else:    
        keystestfcn=lambda tagandkeys: len(set(tagandkeys.split(';')[1].split(',')).intersection(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING))==len(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)
        #keysfcn=lambda tagandkeys: list(set(tagandkeys.split(';')[1].split(',')).difference(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING))
        #make keys list retain original order
        keysfcn=lambda tagandkeys: [k for k in tagandkeys.split(';')[1].split(',') if not k in FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING]
        
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
        self.dfltparams={'select_ana': 'ana__1', 'select_fom_keys':'ALL'}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis_Master_FOM_Process'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=[]
        self.plotparams=dict({}, plot__1={})
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
    
    
    def getgeneraltype(self):#make this fucntion so it is inhereted
        return 'process_fom'
        
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None, calcFOMDialogclass=None):#just a wrapper around getapplicablefomfiles to keep same argument format as other AnalysisClasses
        return self.getapplicablefomfiles(anadict)
        
    def getapplicablefomfiles(self, anadict):
        if not anadict is None and self.params['select_ana'] in anadict.keys() and 'plot_parameters' in anadict[self.params['select_ana']]:
            self.plotparams=copy.deepcopy(anadict[self.params['select_ana']]['plot_parameters'])
            
        self.num_ana_considered, self.filedlist=stdgetapplicablefomfiles(anadict, params=self.params)#has to be called filedlist tro work with other analysis fcns

        self.description='process %s' %self.params['select_ana']
        return self.filedlist
    
    def check_input(self, critfracapplicable=0):
        fracapplicable=1.*len(self.filedlist)/self.num_ana_considered
        return fracapplicable>critfracapplicable, \
        '%d ana__, %.2f of those available, do not meet requirements' %(self.num_ana_considered-len(self.filedlist), 1.-fracapplicable)
    def check_output(self, critfracnan=0.9):
        return True, \
        'No output check for Process FOM'

    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):#must have same arguments as regular AnaylsisClass
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
            if len(self.fomdlist)==0:
                print 'no foms calculated for ', fn
                continue
            self.writefom(destfolder, anak, anauserfomd=anauserfomd, strkeys_fomdlist=self.strkeys_fomdlist)#sample_no, plate_id and runint are explicitly required in csv selection above and are assume to be present here

        
class Analysis__FilterSmoothFromFile(Analysis_Master_FOM_Process):#THE PCK-BASED PROCESSING AS SAMPLE_NO BASED AND NEED NOT PAY ATTENTION TO PLATE_ID
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={'select_ana': 'ana__1', 'select_fom_keys':'ALL','ignore_if_any_nan':0, 'sorted_ind_start':0, 'sorted_ind_stop':999, 'nsig_remove_outliers':999., 'platemap_comp4plot_keylist':'A,B,C,D'}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__FilterSmoothFromFile'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=[]
        self.plotparams=dict({}, plot__1={})
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.filter_path__runint={}
    def getgeneraltype(self):#make this fucntion so it is inhereted
        return 'process_fom_from_file'
        
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
        self.dfltparams={'select_ana': 'ana__1', 'select_fom_keys':'ALL', 'crit_comp_dist':0.0005, 'sorted_ind_start':0, 'sorted_ind_stop':999}
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
        
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None, calcFOMDialogclass=None):#in addition to standard requirements, platemapdlist must be defined for all runs - for simplicity require for all runs in expfiledict even if they are not used in ana__x
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



class Analysis__Process_XRFS_Stds(Analysis_Master_FOM_Process):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={'select_ana': 'ana__1', 'nmol_CPS_list':'','nmol_CPS_lib_file': '.csv', 'transition_list_for_stds':'ALL', 'transition_list_for_comps':'ALL', 'transition_ratio_list':'NONE'}#nmol_CPS_list is comma-delim values, to override library, for other params user can type substrings, e.g. .csv to find any library file or Fe to find Fe.K, rations typed as comma-delim of form "Fe:La.L"
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Process_XRFS_Stds'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=['tube_voltage', 'tube_current', 'spot_size', 'chamber_atmosphere', 'amp_time']
        self.fomnames=['Tot.nmol']
        self.plotparams=dict({}, plot__1={})
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        

        self.plotparams['plot__1']['x_axis']='sample_no'
        self.plotparams['plot__1']['series__1']='Tot.nmol'
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=self.fomnames[0], colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')
        
        self.cpsendswithstr='.CPS'
    
    
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None, calcFOMDialogclass=None):#just a wrapper around getapplicablefomfiles to keep same argument format as other AnalysisClasses
        if runklist is None or len(runklist)==0:
            return []
        if len(self.getapplicablefomfiles(anadict))==0:
            return []
        #get the params for each filed and each run (there will be at least 1 of these and then make sure all params there and all equal
        reqparams_list=[[(reqparam, expfiledict[runk]['parameters'][reqparam]) for reqparam in self.requiredparams if reqparam in expfiledict[runk]['parameters'].keys()] for filed in self.filedlist for runk in runklist]
        if len(reqparams_list[0])!=len(self.requiredparams) or False in [l==reqparams_list[0] for l in reqparams_list[1:]]:
            self.filedlist=[]
            return []
        
        for filed in self.filedlist:
            filed.update(reqparams_list[0])
        self.processnewparams()
        return self.filedlist
        
        
    def getapplicablefomfiles(self, anadict):
#    if not anadict is None and self.params['select_ana'] in anadict.keys() and 'plot_parameters' in anadict[self.params['select_ana']]:
#        self.plotparams=copy.deepcopy(anadict[self.params['select_ana']]['plot_parameters'])
            
        self.num_ana_considered, self.filedlist=stdgetapplicablefomfiles(anadict, params=self.params)#has to be called filedlist tro work with other analysis fcns
        #only allow filed that are XRFS and have a .CPS fom
        self.filedlist=[filed for filed in self.filedlist \
        if 'technique' in anadict[filed['ana']].keys() and anadict[filed['ana']]['technique']=='XRFS' and (True in [k.endswith(self.cpsendswithstr) for k in filed['process_keys']])\
        ]

       
        self.description='process %s' %self.params['select_ana']
        return self.filedlist
    
    def processnewparams(self, calcFOMDialogclass=None):
        self.fomnames=['Tot.nmol']
        if len(self.filedlist)!=1:
            self.filedlist=[]
            return
        filed=self.filedlist[0]
        
        filed['trans_keys']=[k for k in filed['process_keys'] if k.endswith(self.cpsendswithstr)]
        filed['trans_list']=[k[:-len(self.cpsendswithstr)] for k in filed['trans_keys']]
        for count, (paramkey, unitstr) in enumerate([('transition_list_for_stds', '.nmol'), ('transition_list_for_comps', '.AtFrac')]):
            trans_list=filed['trans_list']
            if not (self.params[paramkey]=='NONE' or self.params[paramkey]=='ALL'):
                searchstrs=self.params[paramkey].split(',')
                trans_list=[k for k in trans_list if True in [ss in k for ss in searchstrs]]
                if len(trans_list)==0:
                    self.params[paramkey]='NONE'
            
            if count==0:
                transition_list_for_stds=trans_list
            else:
                if self.params[paramkey]=='NONE':
                    continue
                trans_list=[tr for tr in trans_list if tr in transition_list_for_stds]
            self.params[paramkey]=','.join(trans_list)
            self.fomnames+=[tr+unitstr for tr in trans_list]
        
        if len(transition_list_for_stds)==0:
            self.params=copy.copy(self.dfltparams)
            self.filedlist=[]
            return
        
        if not self.params['transition_ratio_list']=='NONE':

            ratio_trans_list=self.params['transition_ratio_list'].replace(' ','').replace(':',',').replace('_',',').split(',')
            
            translist_ratioorder=[[k for k in filed['trans_list'] if ss in k] for ss in ratio_trans_list]#search to match and better only find 1 match per user entry
            translist_ratioorder=[None if len(l)!=1 else l[0] for l in translist_ratioorder]

            if len(translist_ratioorder)==0 or (len(translist_ratioorder)%2)!=0 or None in translist_ratioorder:
                self.params['transition_ratio_list']='NONE'
            else:
                newfoms=[]
                for i in range(len(translist_ratioorder)//2):
                    tri, trj=translist_ratioorder[2*i], translist_ratioorder[2*i+1]
                    if not (tri in transition_list_for_stds and trj in transition_list_for_stds):
                        continue
                    newfoms+=['_'.join([tri, trj])]
                self.fomnames+=newfoms
                self.params['transition_ratio_list']=','.join(newfoms)


        #no exisintg after here - can do some kind of calculation and worst case is all nmol/CPS are 0
        if len(self.params['nmol_CPS_list'])>0:
            try:
                nmolcps_list=[float(sv) for sv in self.params['nmol_CPS_list'].split(',')]
                if len(nmolcps_list)>len(transition_list_for_stds):
                    raise#don't allow too many values to be entered
                nmolcps_list+=[0]*(len(transition_list_for_stds)-len(nmolcps_list))
            except:
                nmolcps_list=[0]*len(transition_list_for_stds)
        else:
            nmolcps_list=[0]*len(transition_list_for_stds)
            
        if 0 in nmolcps_list:#need to get at least 1 value from file - don't abort anywhere in here because want to give user option to change parameters if default params returns zeros for nmol/cps values
            fileparamstr='-'.join([(fmt %sv)[:4] for fmt,sv in zip(['%d', '%d', '%s', '%s', '%.1f'], [filed[k] for k in self.requiredparams])])
            tup=get_xrfs_stds_csv(startswithstr=fileparamstr, searchstr=self.params['nmol_CPS_lib_file'])
            if not tup is None:
                xrfs_stds_dict, csvfn=tup
                self.params['nmol_CPS_lib_file']=csvfn
                for i in range(len(nmolcps_list)):
                    nmcps=nmolcps_list[i]
                    tr=filed['trans_list'][i]
                    if nmcps>0 or not tr in xrfs_stds_dict.keys():
                        continue
                    nmolcps_list[i]=xrfs_stds_dict[tr]
        
        self.params['nmol_CPS_list']=','.join(['%.4f' %v if v>0. else '0' for v in nmolcps_list])
            

    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):#must have same arguments as regular AnaylsisClass
        self.initfiledicts()
        
        
        for filed in self.filedlist:
#            keylist_lists=[[], [], []]
#            for count, paramk in enumerate(['transition_list_for_stds', 'transition_list_for_comps', 'transition_ratio_list']):
#                if not self.params[paramk]=='NONE':
#                    if count<2:
#                        keylist_lists[count]=[filed['trans_keys'][filed['trans_list'].index(tr)] for tr in self.params[paramk].split(',')]
#                    else:
#                        keylist_lists[count]=[[filed['trans_keys'][filed['trans_list'].index(tr)] for tr in trpair.split(':')] for trpair in self.params[paramk].split(',')]
#
#                [filed['trans_keys'][filed['trans_list'].index(tr)] for tr in self.params[paramk].split(',')]
            
            transition_list_for_stds=self.params['transition_list_for_stds'].split(',')
            transition_list_csvkeys=[filed['trans_keys'][filed['trans_list'].index(tr)] for tr in transition_list_for_stds]
            if self.params['transition_list_for_comps']=='NONE':
                trans_inds_comps=[]
            else:
                trans_inds_comps=[transition_list_for_stds.index(tr) for tr in self.params['transition_list_for_comps'].split(',')]
            
            if self.params['transition_ratio_list']=='NONE':
                trans_ind_numer_ratios=[]
                trans_ind_denom_ratios=[]
            else:
                trans_ind_numer_ratios, trans_ind_denom_ratios=numpy.array([[transition_list_for_stds.index(tr) for tr in trpair.split('_')] for trpair in self.params['transition_ratio_list'].split(',')]).T
                trans_ind_numer_ratios=list(trans_ind_numer_ratios)
                trans_ind_denom_ratios=list(trans_ind_denom_ratios)
            nmolcpsarr=numpy.float32(self.params['nmol_CPS_list'].split(','))
            
            compsfcn=lambda nmolarr:nmolarr[trans_inds_comps]/nmolarr[trans_inds_comps].sum()
            ratiofcn=lambda nmolarr:nmolarr[trans_ind_numer_ratios]/nmolarr[trans_ind_denom_ratios]
            
            self.strkeys_fomdlist=[]

            fn=filed['fn']
            try:
                xrffomd, csvheaderdict=readcsvdict(os.path.join(destfolder, fn), filed, returnheaderdict=True, zipclass=None, includestrvals=False)#str vals not allowed because not sure how to "filter/smooth" and also writefom, headerdictwill be re-used in processed version
                self.fomdlist=[dict(zip(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING, tup)) for tup in zip(*[xrffomd[k] for k in FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING])]
                
                nmol_bysample_bytrans=numpy.float32([xrffomd[k]*nmolcps for k, nmolcps in zip(transition_list_csvkeys, nmolcpsarr)]).T
                [fomd.update(zip(self.fomnames, [nmolarr.sum()]+list(nmolarr)+list(compsfcn(nmolarr))+list(ratiofcn(nmolarr)))) for fomd, nmolarr in zip(self.fomdlist, nmol_bysample_bytrans)]
                
            except:
                if self.debugmode:
                    raiseTEMP
                print 'skipped XRF analysis of file ', fn
                self.fomdlist=[]
                continue
            if len(self.fomdlist)==0:
                print 'no foms calculated for ', fn
                continue
            self.writefom(destfolder, anak, anauserfomd=anauserfomd, strkeys_fomdlist=self.strkeys_fomdlist)




class Analysis__Process_B_Relative_To_A_Matching_Sample(Analysis_Master_nointer):#this is within a single fom csv. if want to combine fom csvs use Analysis__FOM_Merge_Aux_Ana first
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={'select_ana': 'ana__1', 'fom_keys_B':'ALL', 'fom_keys_A':'ALL', 'runints_B':2, 'runints_A':1, 'method':'A_minus_B'}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Process_B_Relative_To_A_Matching_Sample'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=[]
        self.plotparams=dict({}, plot__1={})
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
    
    
    def getgeneraltype(self):#make this fucntion so it is inhereted
        return 'process_fom'
        
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None, calcFOMDialogclass=None):#just a wrapper around getapplicablefomfiles to keep same argument format as other AnalysisClasses
        return self.getapplicablefomfiles(anadict)
        
    def getapplicablefomfiles(self, anadict):
        if not anadict is None and self.params['select_ana'] in anadict.keys() and 'plot_parameters' in anadict[self.params['select_ana']]:
            self.plotparams=copy.deepcopy(anadict[self.params['select_ana']]['plot_parameters'])
            
        self.num_ana_considered, self.filedlist=stdgetapplicablefomfiles(anadict, params=self.params)#has to be called filedlist tro work with other analysis fcns

        self.description='process %s' %self.params['select_ana']
        return self.filedlist
    
    def check_input(self, critfracapplicable=0):
        fracapplicable=1.*len(self.filedlist)/self.num_ana_considered
        return fracapplicable>critfracapplicable, \
        '%d ana__, %.2f of those available, do not meet requirements' %(self.num_ana_considered-len(self.filedlist), 1.-fracapplicable)
    def check_output(self, critfracnan=0.9):
        return True, \
        'No output check for Process FOM'

    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):#must have same arguments as regular AnaylsisClass
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
            if len(self.fomdlist)==0:
                print 'no foms calculated for ', fn
                continue
            self.writefom(destfolder, anak, anauserfomd=anauserfomd, strkeys_fomdlist=self.strkeys_fomdlist)#sample_no, plate_id and runint are explicitly required in csv selection above and are assume to be present here
            
