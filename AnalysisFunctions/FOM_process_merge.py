import numpy, copy,sys,os
if __name__ == "__main__":
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
from scipy import interpolate
from fcns_math import *
from fcns_io import *
from fcns_ui import mygetopenfile
from FOM_process_basics import FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING, Analysis_Master_FOM_Process#, stdgetapplicablefomfiles

class Analysis__FOM_Merge_Aux_Ana(Analysis_Master_FOM_Process):
    def __init__(self):
        self.analysis_fcn_version='4'
        self.dfltparams={'select_ana': 'ana__1', 'select_fom_keys':'ALL', 'select_aux_keys':'ALL', 'remove_samples_not_in_aux':1, 'aux_ana_path':'self', 'aux_ana_ints':'ALL', 'match_plate_id':1, 'key_append_all_aux':'none'}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__FOM_Merge_Aux_Ana'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=[]
        self.plotparams=dict({}, plot__1={})#copied in the default getapplicablefomfiles
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})#get for each csv during .perform()
        self.auxfiledlist=[]
        self.auxpath=''
        self.previous_params=None
        self.auxd={}
    
    def getgeneraltype(self):#make this fucntion so it is inhereted
        return 'process_fom'
        
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None, calcFOMDialogclass=None):#just a wrapper around getapplicablefomfiles to keep same argument format as other AnalysisClasses
        if self.params['aux_ana_path']=='self' and len(calcFOMDialogclass.aux_ana_dlist)==0:#since "self" won't be found in aux ana, this only allows self to be used if no aux ana loaded. if loaded then aux_ana_path will be auto updated below
            if calcFOMDialogclass is None or not 'ana__1' in calcFOMDialogclass.anadict.keys():
                self.filedlist=[]
                return self.filedlist
        elif self.params['aux_ana_path']!='custom':
            if calcFOMDialogclass is None or len(calcFOMDialogclass.aux_ana_dlist)==0:
                self.filedlist=[]
                return self.filedlist
            if not (True in [self.params['aux_ana_path'] in auxd['auxexpanapath_relative'] for auxd in calcFOMDialogclass.aux_ana_dlist]):
                self.params['aux_ana_path']=auxd['auxexpanapath_relative']# if aux_ana_path not available or 'None', use the msot recently added one, which will be auxd due to the above iterator#20180329removed os.path.split
        #do not check if aux ana contains any valid foms - let user change params and validate there
#        if len(self.getapplicablefomfiles(anadict))>0 and self.params['aux_ana_path']=='custom':#only run params for custom when user changes to "custom"
#            self.processnewparams(calcFOMDialogclass=calcFOMDialogclass, recalc_filedlist=False)
        self.processnewparams(calcFOMDialogclass=calcFOMDialogclass, recalc_filedlist=True)#not hasattr(self, 'filedlist'))
        return self.filedlist
    
    def processnewparams(self, calcFOMDialogclass=None, recalc_filedlist=True):
        self.processnewparams_merge(calcFOMDialogclass=calcFOMDialogclass, recalc_filedlist=recalc_filedlist)
        
    def processnewparams_merge(self, calcFOMDialogclass=None, recalc_filedlist=True, additionl_required_params_aux=[]):
        self.fomnames=[]
        if recalc_filedlist:#the parmas can change what fom files are in filedlist whcih determines which fom names must not be duplicated so need to reevaluate this every time params change
            self.getapplicablefomfiles(calcFOMDialogclass.anadict)
        
        custom_load_csv_bool=False
        if self.params['aux_ana_path']=='self':
            self.auxd=copy.deepcopy(calcFOMDialogclass.anadict)
            convertfilekeystofiled(self.auxd)
            self.auxpath=calcFOMDialogclass.tempanafolder
        elif self.params['aux_ana_path']=='custom':
            custom_load_csv_bool=True

            try:
                if self.previous_params is None or (not 'custom' in self.auxd) or (False in [self.previous_params[k]==v for k, v in self.params.iteritems()]):#first time through or a param has changed since end of last function call then open a file. if want to change the file will need tro change a parameter
                    self.auxd={}
                    self.auxd['custom']={}
                    self.auxd['custom']['files_multi_run']={}
                    self.auxd['custom']['files_multi_run']['fom_files']={}
                    p=mygetopenfile(parent=(None if (calcFOMDialogclass is None) else calcFOMDialogclass), markstr='Select .csv with 1 header line inlcuding sample_no')
                    if p is None or len(p)==0:
                        raise ValueError()
                    self.auxpath, fnk=os.path.split(p)
                    fileattrd=dict({}, fn=fnk, num_header_lines=1)#the 'keys' get defined within this trial reading
                    readcsvdict(p, fileattrd)
                    if not 'sample_no' in fileattrd['keys']:
                        print 'sample_no required as a column in .csv'
                        raise ValueError()
                    if False in [k==filterchars(k) for k in fileattrd['keys']]:
                        print 'a key in the selected .csv hs an illegal character'
                        raise ValueError()
                    self.auxd['custom']['files_multi_run']['fom_files'][fnk]=fileattrd
            except:
                print 'error reading custom .csv file'
                self.params=copy.copy(self.dfltparams)
                self.filedlist=[]
                return
        else:
            if not (True in [self.params['aux_ana_path'] in auxd['auxexpanapath_relative'] for auxd in calcFOMDialogclass.aux_ana_dlist]):
                self.params=copy.copy(self.dfltparams)#no aux_ana meet search so return to default, will also happen if there are no aux_ana open
                self.filedlist=[]
                return
            for auxd in calcFOMDialogclass.aux_ana_dlist:
                if self.params['aux_ana_path'] in auxd['auxexpanapath_relative']:#can only use 1 aux ana so use the first one found
                    self.params['aux_ana_path']=auxd['auxexpanapath_relative']
                    break
            self.auxpath=os.path.split(auxd['auxexpanapath'])[0]
            self.auxd=auxd
        if custom_load_csv_bool:
            anak_list=['custom']
        else:
            if self.params['aux_ana_ints']=='ALL':
                anak_list=sort_dict_keys_by_counter(self.auxd, keystartswith='ana__')
            else:
                anaintstrlist=self.params['aux_ana_ints'].split(',')
                anaintstrlist=[s.strip() for s in anaintstrlist]
                anak_list=[k for k in sort_dict_keys_by_counter(self.auxd, keystartswith='ana__') if k.partition('ana__')[2] in anaintstrlist]
                
            anak_list=[k for k in anak_list\
               if ('files_multi_run' in self.auxd[k].keys()) and ('fom_files' in self.auxd[k]['files_multi_run'].keys())]
           
        if self.params['select_aux_keys']=='ALL':
            keysearchlist=['']
        else:
            keysearchlist=self.params['select_aux_keys'].split(',')
            keysearchlist=[s.strip() for s in keysearchlist if len(s.strip())>0]
        
        keysfcn=lambda filed, aux_key_append, notallowedkeys: [k+aux_key_append for k in filed['keys'] if (not k in FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING) and \
                                                                                                                (not k+aux_key_append in FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING) and \
                                                                                                                (not k+aux_key_append in notallowedkeys) and \
                                                                                                                (True in [s in k for s in keysearchlist])]
        if custom_load_csv_bool:
            reqdkeysset=['plate_id'] if ('match_plate_id' in self.params.keys() and self.params['match_plate_id']) else []
            reqdkeysset=set(reqdkeysset+['sample_no'])
        else:
            reqdkeysset=FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING
        reqdkeysset=reqdkeysset.union(additionl_required_params_aux)
        keystestfcn=lambda filed: len(set(filed['keys']).intersection(reqdkeysset))==len(reqdkeysset)
        
        existkeys=[k for filed in self.filedlist for k in filed['process_keys'] if not k in additionl_required_params_aux]#don't allow aux key overlap with existing keys in any of the fom csvs in play
        
        if 'key_append_all_aux' in self.params.keys() and self.params['key_append_all_aux']!='none':
            aux_key_append=self.params['key_append_all_aux']
        else:
            aux_key_append=''
        
        self.auxfiledlist=[]
        for anak in anak_list:
            for fnk, filed in self.auxd[anak]['files_multi_run']['fom_files'].iteritems():
                if keystestfcn(filed) and len(keysfcn(filed, aux_key_append, existkeys))>0:
                    self.auxfiledlist+=\
                       [{'anakeys':[anak, 'files_multi_run', 'fom_files', fnk], 'ana':anak, 'fn':fnk, 'keys':filed['keys'], \
                       'num_header_lines':filed['num_header_lines'], 'process_keys':keysfcn(filed, aux_key_append, existkeys)}]
                    existkeys+=[self.auxfiledlist[-1]['process_keys']]#aux keys can be from multipleana__ blocks but only 1 ana_file
                
        auxkeylist=[k if len(aux_key_append)==0 else k[:-len(aux_key_append)] for filed in self.auxfiledlist for k in filed['process_keys']]
#allow this to pass so the params can be changed to, e.g. "custom". If "perform" happens under this condition then the new .csv will be the same as the old.
#        if len(auxkeylist)==0:
#            print 'cannot find any unique aux fom keys'
#            self.params=copy.copy(self.dfltparams)
#            self.filedlist=[]
#            return
        self.params['select_aux_keys']=','.join(auxkeylist)
        self.previous_params=copy.copy(self.params)


    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):#must have same arguments as regular AnaylsisClass
        self.initfiledicts()

        matchplateidbool=bool(self.params['match_plate_id'])
        if matchplateidbool:
            matchplateidfcn=lambda tempfomd:tempfomd['plate_id']
        else:
            matchplateidfcn=lambda tempfomd:['']*len(tempfomd['sample_no'])#use emtpy strings so that matching tups look the same but plate_id is always empty string so it always matches
        for filed in self.filedlist:
            

            fn=filed['fn']
            try:
            #if 1:
                fomd, self.csvheaderdict=readcsvdict(os.path.join(destfolder, fn), filed, returnheaderdict=True, zipclass=None, includestrvals=False)#str vals not allowed because not sure how to "filter/smooth" and also writefom, headerdictwill be re-used in processed version
                
                if self.params['select_fom_keys']=='ALL':
                    keysearchlist=['']
                else:
                    keysearchlist=self.params['select_fom_keys'].split(',')
                    keysearchlist=[s.strip() for s in keysearchlist if len(s.strip())>0]
        
                process_keys=[k for k in filed['process_keys'] if (not 'aux_' in k) and (True in [s in k for s in keysearchlist]) and k in fomd.keys()]#new in v4, previously select_fom_keys ignored, but regardless don't all aux_ keys from prior fom csv because those are being added in the merge and don't want ambiguity
                #along_for_the_ride_keys=list(set(fomd.keys()).difference(set(process_keys)))
                auxfomd_list=[readcsvdict(os.path.join(self.auxpath, auxfiled['fn']), auxfiled, returnheaderdict=False, zipclass=None, includestrvals=False) for auxfiled in self.auxfiledlist]
                
                newfomd={}
                fomd_plt_smp_list=zip(matchplateidfcn(fomd), fomd['sample_no'])
                
                if self.params['remove_samples_not_in_aux']:
                    plt_smp_list=set(fomd_plt_smp_list)
                    for auxfomd in auxfomd_list:
                        plt_smp_list=plt_smp_list.intersection(zip(matchplateidfcn(auxfomd), auxfomd['sample_no']))
                    plt_smp_list=sorted(list(plt_smp_list))
                    inds=[fomd_plt_smp_list.index(tup) for tup in plt_smp_list]
                    for k in list(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)+process_keys:
                        newfomd[k]=fomd[k][inds]
                else:#keep all master ana sample_no and fill in nan if missing from aux
                    plt_smp_list=fomd_plt_smp_list
                    for k in list(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)+process_keys:
                        newfomd[k]=fomd[k]
                if len(plt_smp_list)==0:
                    print 'no samples match - skipping merge'
                    continue
                self.fomnames=process_keys
                self.strkeys_fomdlist=['aux_anak']
                newfomd['aux_anak']=numpy.array(['']*len(newfomd['sample_no']),dtype='|S8')#S8 is ana__NNN'
                plateidinanyaux=True in ['plate_id' in auxfomd.keys() for auxfomd in auxfomd_list]
                if plateidinanyaux and not matchplateidbool:
                    self.strkeys_fomdlist+=['aux_plate_id']
                    newfomd['aux_plate_id']=numpy.array(['']*len(newfomd['sample_no']),dtype='|S8')#plate_id presumably no more than 8 characters long
                for auxfomd, auxfiled in zip(auxfomd_list, self.auxfiledlist):
                    auxfomdinds, fomdinds=numpy.array([[count, plt_smp_list.index(tup)] for count, tup in enumerate(zip(matchplateidfcn(auxfomd), auxfomd['sample_no'])) if tup in plt_smp_list]).T
                    #newfomd['aux_anaint'][fomdinds]=int(auxfiled['ana'].partition('__')[2])
                    newfomd['aux_anak'][fomdinds]=auxfiled['ana']
                    if len(auxfomdinds)==0:#if no matching plate,sample then skip this column merge
                        continue
                    self.fomnames+=auxfiled['process_keys']
                    for k in auxfiled['process_keys']:
                        newfomd[k]=numpy.ones(len(newfomd['sample_no']), dtype='float64')*numpy.nan
                        newfomd[k][fomdinds]=auxfomd[k[:-len(self.params['key_append_all_aux'])] if self.params['key_append_all_aux']!='none' else k][auxfomdinds]
                    if 'plate_id' in auxfomd.keys() and not matchplateidbool:#if not matching by plate_id then the aux plate_id could be different so need to save it. This will arise for parent/child merges
                        newfomd['aux_plate_id'][fomdinds]=numpy.array(auxfomd['plate_id'][auxfomdinds],dtype='|S8')
                allkeys=list(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)+self.fomnames+self.strkeys_fomdlist#str=valued keys don't go into fomnames
                self.fomdlist=[dict(zip(allkeys, tup)) for tup in zip(*[newfomd[k] for k in allkeys])]
                
                #copy custom merge file to the ana
                if self.params['aux_ana_path']=='custom':
                    newfn='%s__%s' %(anak, auxfiled['fn'])
                    if not 'misc_files' in self.multirunfiledict.keys():
                        self.multirunfiledict['misc_files']={}
                    self.multirunfiledict['misc_files'][newfn]=\
                     '%s;%s;%d;%d' %('csv_fom_file', ','.join(auxfiled['keys']), auxfiled['num_header_lines'], auxfiled['num_data_rows'] if 'num_data_rows' in auxfiled else len(auxfomd_list[0]['sample_no']))
                    if not newfn in os.listdir(destfolder):#assume aux custom fn is unique from the ana-generated files in this folder. If the custom file copied already doesn't need to be copied again  
                        shutil.copy(os.path.join(self.auxpath, auxfiled['fn']), os.path.join(destfolder, newfn))

            except:
                if self.debugmode:
                    raiseTEMP
                print 'skipped filter/smooth of file ', fn
                self.fomdlist=[]
                continue

            if len(self.fomdlist)==0:
                print 'no foms calculated for ', fn
                continue

            print destfolder, anak, anauserfomd, self.strkeys_fomdlist
            self.writefom(destfolder, anak, anauserfomd=anauserfomd, strkeys_fomdlist=self.strkeys_fomdlist)#sample_no, plate_id and runint are explicitly required in csv selection above and are assume to be present here



class Analysis__FOM_Merge_PlatemapComps(Analysis_Master_FOM_Process):
    def __init__(self):
        self.analysis_fcn_version='2'
        self.dfltparams={'select_ana': 'ana__1', 'select_fom_keys':'ALL', 'key_append_conc':'.PM.Loading', 'key_append_atfrac':'.PM.AtFrac', 'tot_conc_label':'Tot.PM.Loading', 'value_when_missing':'nan'}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__FOM_Merge_PlatemapComps'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=[]
        self.plotparams=dict({}, plot__1={})#copied in the default getapplicablefomfiles
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})#get for each csv during .perform()

    
    def getgeneraltype(self):#make this fucntion so it is inhereted
        return 'process_fom'
        
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None, calcFOMDialogclass=None):#just a wrapper around getapplicablefomfiles to keep same argument format as other AnalysisClasses
        if True in [not 'platemapdlist' in rund.keys() for runk, rund in calcFOMDialogclass.expfiledict.iteritems() if runk.startswith('run__')]:
            #all platemaps must be available
            self.filedlist=[]
            return self.filedlist
        if len(self.getapplicablefomfiles(anadict))>0:
            self.processnewparams()
        return self.filedlist
    
    def processnewparams(self, calcFOMDialogclass=None):
        self.fomnames=[]
        try:
            self.value_when_missing=numpy.nan if self.params['value_when_missing']=='NaN' else float(self.params['value_when_missing'])
        except:
            self.value_when_missing=numpy.nan
        self.params['value_when_missing']=`self.value_when_missing`

    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):#must have same arguments as regular AnaylsisClass
        self.initfiledicts()

        for filed in self.filedlist:
            

            fn=filed['fn']
            try:
            #if 1:
                fomd, self.csvheaderdict=readcsvdict(os.path.join(destfolder, fn), filed, returnheaderdict=True, zipclass=None, includestrvals=False)#str vals not allowed because not sure how to "filter/smooth" and also writefom, headerdictwill be re-used in processed version
                
                process_keys=filed['process_keys']
                
                if not 'plate_id' in fomd.keys():
                    print 'no plate_id - skipped filter/smooth of file ', fn
                    self.fomdlist=[]
                    continue
                allplateids=sorted(list(set(fomd['plate_id'])))
                
                self.fomnames=copy.copy(process_keys)
                for pid in allplateids:
                    
                    pmpath, pmidstr=getplatemappath_plateid(str(pid), return_pmidstr=True)
                    #pmpath, pmidstr=r'J:\hte_jcap_app_proto\map\0068-04-0100-mp.txt', '69'#for 1-off override
                    platemapdlist=readsingleplatemaptxt(pmpath, erroruifcn=None)
                    
                    els, tup_multielementink=getelements_plateidstr(str(pid), multielementink_concentrationinfo_bool=True, return_defaults_if_none=True)
                    if not tup_multielementink is None:
                        errorbool, tupormessage=tup_multielementink
                        if errorbool:
                            errorreadingmultielementinfo
                        cels_set_ordered, conc_el_chan=tupormessage
                
                    else:
                        cels_set_ordered=els
                        conc_el_chan=numpy.zeros((len(els), len(els)), dtype='float64')
                        numpy.fill_diagonal(conc_el_chan, 1.)
                    tot_conc_label=None if len(self.params['tot_conc_label'])==0 else self.params['tot_conc_label']
                    calc_comps_multi_element_inks(platemapdlist, cels_set_ordered, conc_el_chan, key_append_conc=self.params['key_append_conc'], key_append_atfrac=self.params['key_append_atfrac'], tot_conc_label=tot_conc_label)
                    newfomnames=[el+self.params['key_append_conc'] for el in cels_set_ordered]+\
                                          [el+self.params['key_append_atfrac'] for el in cels_set_ordered]+\
                                          ([] if tot_conc_label is None else [tot_conc_label])
                    newfomnames=[lab for lab in newfomnames if not (lab in process_keys or lab in FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)]
                    
                    fomdinds_plate=numpy.where((fomd['plate_id']==pid)&(fomd['sample_no']>0))[0]
                    smps=fomd['sample_no'][fomdinds_plate]
                    pmsmps=[pmd['sample_no'] for pmd in platemapdlist]
                    pminds=[pmsmps.index(smp) for smp in smps]
                    for k in newfomnames:
                        if not k in self.fomnames:
                            fomd[k]=numpy.ones(len(fomd['sample_no']), dtype='float64')*self.value_when_missing
                            self.fomnames+=[k]
                        fomd[k][fomdinds_plate]=numpy.array([platemapdlist[pmind][k] for pmind in pminds])
                self.strkeys_fomdlist=[]
                allkeys=list(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)+self.fomnames
                self.fomdlist=[dict(zip(allkeys, tup)) for tup in zip(*[fomd[k] for k in allkeys])]

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



class Analysis__Filter_Linear_Projection(Analysis_Master_FOM_Process):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={'select_ana': 'ana__1', 'select_fom_keys':'ALL', 'max_dist_from_line':1., 'keys_param_space':'x,y', 'line_start':'0.,0.', 'line_stop':'100.,150.', 'allow_beyond_endpts':0, 'is_comp_space':0}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Filter_Linear_Projection'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=[]
        self.plotparams=dict({}, plot__1={})#copied in the default getapplicablefomfiles
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})#get for each csv during .perform()

    
    def getgeneraltype(self):#make this fucntion so it is inhereted
        return 'process_fom'
        
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None, calcFOMDialogclass=None):#just a wrapper around getapplicablefomfiles to keep same argument format as other AnalysisClasses
        if True in [not 'platemapdlist' in rund.keys() for runk, rund in calcFOMDialogclass.expfiledict.iteritems() if runk.startswith('run__')]:
            #all platemaps must be available
            self.filedlist=[]
            return self.filedlist
        if len(self.getapplicablefomfiles(anadict))>0:
            self.processnewparams(calcFOMDialogclass=calcFOMDialogclass)
        return self.filedlist
    
    def processnewparams(self, calcFOMDialogclass=None):
        self.fomnames=[]
        
        l_ndims=[self.params[k].count(',')+1 for k in ['keys_param_space', 'line_start', 'line_stop']]
        nd=l_ndims[0]
        if False in [nd==v for v in l_ndims]:
            print 'param_space dimensions do not match'
            self.filedlist=[]
            return
        if nd>(4 if self.params['is_comp_space'] else 3):
            print 'param_space must be no bigger than 3D or quaternary'
            self.filedlist=[]
            return
        try:
            self.endpoints=numpy.float64([[float(v.strip()) for v in self.params[k].split(',')] for k in ['line_start', 'line_stop']])
        except:
            print 'error calculating end points from %s and %s' %(self.params['line_start'], self.params['line_stop'])
            self.filedlist=[]
            return
        list_pmkeys=[rund['platemapdlist'][0].keys() if 'platemapdlist' in rund.keys() else None for runk, rund in calcFOMDialogclass.expfiledict.iteritems() if runk.startswith('run__')]
        if None in list_pmkeys:#require that all runs in exp have platemap loaded, but once loaded the keys can come from any platemap (union of platemap keys)
            self.platemapkeys=[]
        else:
            self.platemapkeys=list(set([k for l in list_pmkeys for k in l]))
        filed_k_tups=[(filed, k) for filed in self.filedlist for k in filed['keys']]#allow process_keys and things like sample_no
        existkeys=[k for filed, k in filed_k_tups]
        
        self.fomfromfilebool_key__params_space=[]
        allowablefiledselected=False
        for k in self.params['keys_param_space'].split(','):
            k=k.strip()
            #exact match in platemap - search platemap first since using from here doesn't preclude analysis of a single .csv
            if k in self.platemapkeys:
                self.fomfromfilebool_key__params_space+=[(False, k)]
                continue
            #exact match in a single csv filed
            if k in existkeys:
                filed, kv=filed_k_tups[existkeys.index(k)]
                self.fomfromfilebool_key__params_space+=[(True, kv)]
                if allowablefiledselected:
                    if not filed in self.filedlist:
                        self.filedlist=[]
                        print 'param space has to be from platemap or a single csv'
                        return
                else:
                    self.filedlist=[filed]#if using key from filed then make it the only one to be analyzed
                    allowablefiledselected=True
                continue
            
            #contains match in platemap
            matchkeys=[(count, kv) for count, kv in enumerate(self.platemapkeys) if k in kv]
            
            if len(matchkeys)>0:
                count, kv=matchkeys[0]
                self.fomfromfilebool_key__params_space+=[(False, kv)]
                continue
                
            #contains match in a single csv filed
            matchkeys=[(count, kv) for count, kv in enumerate(existkeys) if k in kv]
            if len(matchkeys)>0:
                count, kv=matchkeys[0]
                filed, kv=filed_k_tups[count]
                self.fomfromfilebool_key__params_space+=[(True, kv)]
                if allowablefiledselected:
                    if not filed in self.filedlist:
                        self.filedlist=[]
                        print 'param space has to be from platemap or a single csv'
                        return
                else:
                    self.filedlist=[filed]#if using key from filed then make it the only one to be analyzed
                    allowablefiledselected=True
                continue
            
            print 'cannot find source for param space key %s' %k
            self.filedlist=[]#cannot find a key
            return
        self.params['keys_param_space']=','.join([k for filedbool, k in self.fomfromfilebool_key__params_space])
        
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):#must have same arguments as regular AnaylsisClass
        self.initfiledicts()

        
        for filed in self.filedlist:
            
            #self.fomfromfilebool_key__params_space has filed but can only be this filed since if using keys from a filed then filedlist is limited to only this filed
            fn=filed['fn']
            try:
            #if 1:
                fomd, self.csvheaderdict=readcsvdict(os.path.join(destfolder, fn), filed, returnheaderdict=True, zipclass=None, includestrvals=False)#str vals not allowed because not sure how to "filter/smooth" and also writefom, headerdictwill be re-used in processed version
                
                process_keys=filed['process_keys']
                
                pmkeys=[axisk for fomfromfilebool, axisk in self.fomfromfilebool_key__params_space if not fomfromfilebool]
                pmaxes_pmkeys=[]
                if len(pmkeys)>0:
                    pmaxes_pmkeys=[]
                    for k in pmkeys:
                        runints=sorted(list(set(fomd['runint'])))
                        axisvals=numpy.ones(len(fomd['runint']), dtype='float64')*numpy.nan
                        for runint in runints:
                            runinds=numpy.where(fomd['runint']==runint)[0]
                            platemapdlist=expfiledict['run__%d' %runint]['platemapdlist']
                            smps=[d['sample_no'] for d in platemapdlist]
                            axisvals[runinds]=numpy.array([platemapdlist[smps.index(smp)][k] if k in platemapdlist[smps.index(smp)].keys() else numpy.nan for smp in fomd['sample_no'][runinds]])
                        pmaxes_pmkeys+=[axisvals]
                arr_of_xyz=numpy.array([fomd[axisk] if fomfromfilebool else pmaxes_pmkeys.pop(0) for fomfromfilebool, axisk in self.fomfromfilebool_key__params_space]).T
                #if fomfromfilebool then get the key from filed, the only one in self.filedlist. could be mroe than 1 if fomfromfilebool is False

                filterlined=filterbydistancefromline(arr_of_xyz, self.endpoints[0], self.endpoints[1], self.params['max_dist_from_line'], \
                   betweenpoints=not bool(self.params['allow_beyond_endpts']), invlogic=False, returnonlyinds=False, is_composition=bool(self.params['is_comp_space']))

                inds=filterlined['select_inds']
                if len(inds)==0:
                    self.fomdlist=[]
                    continue
                newkeys=['dist_from_line', 'norm_dist_along_line']
                for k in newkeys:
                    fomd[k]=filterlined[k]
                self.fomnames=process_keys+newkeys
                
                self.strkeys_fomdlist=[]
                allkeys=list(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)+self.fomnames
                self.fomdlist=[dict(zip(allkeys, tup)) for tup in zip(*[fomd[k][inds] for k in allkeys])]
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





class Analysis__FOM_Interp_Merge_Ana(Analysis__FOM_Merge_Aux_Ana):
    def __init__(self):
        self.analysis_fcn_version='6'
        self.dfltparams={'select_ana': 'ana__1', 'select_fom_keys':'ALL', 'select_aux_keys':'ALL', 'aux_ana_path':'self', 'aux_ana_ints':'ALL', 'interp_keys':'platemap_xy', 'fill_value':'extrapolate', 'kind':'linear', 'interp_is_phasemap':0, 'interp_is_comp':0, 'num_pts_in_extrapolation':6, 'plate_ids':'ALL'}
        #remove_samples_not_in_aux not used and is effectively =0 here, select_aux_keys is the keys which will be interpolated and must not be in the destination ana and must not include interp_keys, interp_keys can be a keyword for using platemap or a list of 1 (for interp1d) or 2 (2d) keys that are present in both ana being merged.
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__FOM_Interp_Merge_Ana'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=[]
        self.plotparams=dict({}, plot__1={})#copied in the default getapplicablefomfiles
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})#get for each csv during .perform()
        self.auxfiledlist=[]
        self.auxpath=''
        
        
    
    def processnewparams(self, calcFOMDialogclass=None, recalc_filedlist=True):
        interp_keys=self.params['interp_keys']
        if interp_keys=='platemap_xy':
            self.interp_type='xy'
        elif interp_keys=='platemap_xy_line':
            self.interp_type='xy_line'
        else:
            self.interp_type=[s.strip() for s in interp_keys.split(',')]
        
        self.processnewparams_merge(calcFOMDialogclass=calcFOMDialogclass, recalc_filedlist=recalc_filedlist, additionl_required_params_aux=self.interp_type if isinstance(self.interp_type, list) else [])
        
        
        for filed in self.filedlist:
            filed['process_keys']=[k for k in filed['process_keys'] if not k in self.params['select_aux_keys'].split(',')] # these keys will be interpolated. process_keys are those coming along for the ride
            if isinstance(self.interp_type, list):#if interp keys are used they better be in all destination filed. note this check is for process_keys assumintg things like sample_no and runint will not be used for interpolation
                for k in self.interp_type:
                    if not k in filed['process_keys']:
                        self.params=copy.copy(self.dfltparams)
                        self.filedlist=[]
                        return
        self.need_to_extrapolate_separately=False
        #if self.interp_type is a list then at this point its keys are in all filed prcess_keys and auxfiled['process_keys']. Merge doesn't allow these overlaps but required here
        if (self.interp_type=='xy' or (isinstance(self.interp_type, list) and len(self.interp_type)==2)) and self.params['fill_value']=='extrapolate':
            self.need_to_extrapolate_separately=True
            #self.interpkwargs={'fill_value':None}
            self.interpkwargs={'fill_value':numpy.nan}
            self.interpkwargs['method']=self.params['kind']
        elif 'nan' in self.params['fill_value'] or 'NaN' in self.params['fill_value']:
            self.interpkwargs={'fill_value':numpy.nan}
            self.interpkwargs['kind']=self.params['kind']
            self.interpkwargs['bounds_error']=False
        elif ',' in self.params['fill_value']:#this not supported in scipy 0.16 so will cause error
            a, b, c=self.params['fill_value'].partition(',')
            a=float(a.strip())
            c=float(c.strip())
            self.interpkwargs={'fill_value':(a, c)}
            self.interpkwargs['kind']=self.params['kind']
            self.interpkwargs['bounds_error']=False
        elif self.params['fill_value']=='extrapolate':#this case only needed for 1d extrapolation since standard scipy is 0.16 and it doesn't support extrapolation
            self.need_to_extrapolate_separately=True
            self.interpkwargs={'fill_value':numpy.nan}
            self.interpkwargs['kind']=self.params['kind']
            self.interpkwargs['bounds_error']=False
        else:
            self.interpkwargs={'fill_value':float(self.params['fill_value'])}
            self.interpkwargs['kind']=self.params['kind']
            self.interpkwargs['bounds_error']=False
        
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):#must have same arguments as regular AnaylsisClass
        self.initfiledicts()
        self.strkeys_fomdlist=[]
       
        for filed in self.filedlist:
            

            fn=filed['fn']
            try:
            #if 1:
                fomd, self.csvheaderdict=readcsvdict(os.path.join(destfolder, fn), filed, returnheaderdict=True, zipclass=None, includestrvals=False)#str vals not allowed because not sure how to "filter/smooth" and also writefom, headerdictwill be re-used in processed version
                
                process_keys=filed['process_keys']
                #along_for_the_ride_keys=list(set(fomd.keys()).difference(set(process_keys)))
                auxfomd_list=[readcsvdict(os.path.join(self.auxpath, auxfiled['fn']), auxfiled, returnheaderdict=False, zipclass=None, includestrvals=False) for auxfiled in self.auxfiledlist]
                
                if self.params['plate_ids']!='ALL':
                    pids=[int(s.strip()) for s in self.params['plate_ids'].split(',')]
                    for count in range(len(auxfomd_list)):
                        auxfomd=auxfomd_list[count]
                        if not 'plate_id' in auxfomd.keys():
                            continue
                        boolarr=numpy.array([pid in pids for pid in auxfomd['plate_id']])
                        for k in auxfomd.keys():
                            auxfomd[k]=auxfomd[k][boolarr]
                        
                newfomd={}
                for k in list(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)+process_keys:
                    newfomd[k]=fomd[k]
                
                keys_to_interp=self.params['select_aux_keys'].split(',')
                if self.params['interp_is_phasemap']==1:#need to sort so that phase con calculation so it can be used for mask in shift calculation
                    sorttup=lambda k: (0 if k.startswith('phase_concentration.') else 1, int(k.partition('.')[2]) if k.partition('.')[2].isdigit() else 99999, k)
                    keys_to_interp=[tup[2] for tup in sorted([sorttup(k) for k in keys_to_interp])]
                self.fomnames=process_keys+keys_to_interp
                
                if self.interp_type in ['xy', 'xy_line']:
                    
                    
                    for runint in list(set(fomd['runint'])):#use the first platemaqp you find and aux better be same platemap
                        rund=expfiledict['run__%d' %runint]
                        if 'platemapdlist' in rund.keys():
                            dl=rund['platemapdlist']
                            smps=[d['Sample'] for d in dl]
                            xl=[d['x'] for d in dl]
                            yl=[d['y'] for d in dl]
                            break
                    if self.interp_type=='xy':
                        fcn=interpolate.griddata#interpolate.interp2d
                        num_interpdim=2
                        allkeys=['x', 'y']+keys_to_interp
                        self.src_x_then_y=[[] for i in range(len(allkeys))]
                        for auxfomd, auxfiled in zip(auxfomd_list, self.auxfiledlist):
                            xaux=[xl[smps.index(smp)] for smp in auxfomd['sample_no']]
                            yaux=[yl[smps.index(smp)] for smp in auxfomd['sample_no']]
                            toappend=[tup for tup in zip(xaux, yaux, *[auxfomd[k] for k in allkeys[num_interpdim:]]) if (not numpy.nan in tup) and not True in [newval in l for newval, l in zip(tup, self.src_x_then_y[:num_interpdim])]]#num pts by num data arrays, don't allow the interp coords to be duplicated
                            for i in range(len(allkeys)):
                                self.src_x_then_y[i]+=[tup[i] for tup in toappend]
                        dest_x=numpy.float64([[xl[smps.index(smp)], yl[smps.index(smp)]] for smp in fomd['sample_no']])
                    elif self.interp_type=='xy_line':
                        fcn=interpolate.interp1d
                        num_interpdim=1
                        allkeys=['x_line']+keys_to_interp
                        self.src_x_then_y=[[] for i in range(len(allkeys))]
                        xaux_all=[xl[smps.index(smp)] for auxfomd in auxfomd_list for smp in auxfomd['sample_no']]
                        yaux_all=[yl[smps.index(smp)] for auxfomd in auxfomd_list for smp in auxfomd['sample_no']]
                        #all x,y used here and then duplicates screend out below
                        m,b=numpy.polyfit(xaux_all,yaux_all,1)# fit set of x,y to line to get slope
                        rot=numpy.arctan(m) #find rotation angle and rotation transform to remove the slope, i.e. turn into a horizontal line where only x coordinate is needed
                        c,s=numpy.cos(-rot),numpy.sin(-rot)
                        linparam=lambda x, y:x*c-y*s
                        for auxfomd, auxfiled in zip(auxfomd_list, self.auxfiledlist):#****
                            xaux=numpy.array([xl[smps.index(smp)] for smp in auxfomd['sample_no']])
                            yaux=numpy.array([yl[smps.index(smp)] for smp in auxfomd['sample_no']])
                            toappend=[tup for tup in zip(linparam(xaux, yaux), *[auxfomd[k] for k in allkeys[num_interpdim:]]) if (not numpy.nan in tup) and not True in [newval in l for newval, l in zip(tup, self.src_x_then_y[:num_interpdim])]]#num pts by num data arrays, don't allow the interp coords to be duplicated
                            for i in range(len(allkeys)):
                                self.src_x_then_y[i]+=[tup[i] for tup in toappend]
                        dest_x=numpy.float64([linparam(xl[smps.index(smp)], yl[smps.index(smp)]) for smp in fomd['sample_no']])
                        newfomd['Posn_along_line']=dest_x
                        self.fomnames+=['Posn_along_line']
                else:
                    if len(self.interp_type)==2:
                        #fcn=interpolate.interp2d
                        fcn=interpolate.griddata
                        num_interpdim=2
                        dest_x=numpy.float64([fomd[self.interp_type[0]], fomd[self.interp_type[1]]]).T
                    else:
                        fcn=interpolate.interp1d
                        num_interpdim=1
                        dest_x=fomd[self.interp_type[0]]
                    allkeys=self.interp_type+keys_to_interp
                    self.src_x_then_y=[[] for i in range(len(allkeys))]
                    for auxfomd, auxfiled in zip(auxfomd_list, self.auxfiledlist):
                        toappend=[tup for tup in zip(*[auxfomd[k] for k in allkeys]) if (not numpy.nan in tup) and not True in [newval in l for newval, l in zip(tup, self.src_x_then_y[:num_interpdim])]]#num pts by num data arrays
                        for i in range(len(allkeys)):
                            self.src_x_then_y[i]+=[tup[i] for tup in toappend]
                    
                for k, dataind in zip(keys_to_interp, range(num_interpdim, len(allkeys))):
                    
                    zvals=numpy.array(self.src_x_then_y[dataind])
                    
                    if self.params['interp_is_phasemap']==1 and k.startswith('shift_factor.'):
                        maskkey='phase_concentration.'+k.partition('.')[2]
                        if maskkey in keys_to_interp:
                            maskdataind=keys_to_interp.index(maskkey)+num_interpdim
                            inds=numpy.where(numpy.array(self.src_x_then_y[maskdataind])>0.)[0]#phase map only has meaningful shift values when phase conc is nonzero
                            destinds=numpy.where(newfomd[maskkey]>0.)[0]#not only mask but only interp where necessary, phase_conc already interpolated so can set shift to 0 where phase_conc is already 0.
                            if len(inds)<=1:#can't interp with 1 point. may need to increase this threshold and use nearest interp
                                newfomd[k]=numpy.zeros(len(dest_x), dtype='float64')
                                newfomd[k][destinds]=zvals[inds].mean()
                                continue
                            d_x=dest_x[destinds]
                        else:#don't bother interpolating if shift doesn't have a matching phase conc
                            newfomd[k]=numpe.ones(len(dest_x), dtype='float64')*nump.nan
                            continue
                    else:
                        inds=numpy.where(numpy.logical_not(numpy.isnan(zvals)))[0]
                        d_x=dest_x
                    zvals=zvals[inds]
                    if num_interpdim==1:
                        xvals=numpy.array(self.src_x_then_y[0])[inds]
                        intrp1dfcn=fcn(xvals, zvals, **self.interpkwargs)
                        ans=intrp1dfcn(d_x)
                        if self.need_to_extrapolate_separately:
                            naninds=numpy.where(numpy.isnan(ans))[0]
                            if len(naninds)>0:
                                ans[naninds]=linear_1d_extrapolation(xvals, numpy.array(zvals), d_x[naninds], num_pts_in_lin_fit=self.params['num_pts_in_extrapolation'])
                    else:
                        xvals=numpy.float64(self.src_x_then_y[:num_interpdim]).T
                        xvals=xvals[inds]
                        ans=fcn(xvals, zvals, d_x, **self.interpkwargs)
                        if self.need_to_extrapolate_separately:
                            naninds=numpy.where(numpy.isnan(ans))[0]
                            if len(naninds)>0:
                                ans[naninds]=linear_2d_extrapolation(xvals, numpy.array(zvals), d_x[naninds], num_pts_in_lin_fit=self.params['num_pts_in_extrapolation'])
                    if self.params['interp_is_phasemap']==1 and k.startswith('shift_factor.'):
                        newfomd[k]=numpy.zeros(len(dest_x), dtype='float64')
                        newfomd[k][destinds]=ans
                    else:
                        newfomd[k]=ans
                
                if self.params['interp_is_comp']:
                    keystonormalize=keys_to_interp
                elif self.params['interp_is_phasemap']:
                    keystonormalize=[k for k in keys_to_interp if k.startswith('phase_concentration.')]
                else:
                    keystonormalize=[]
                if len(keystonormalize)>0:
                    keys_to_interp_orig=[k.replace('AtFrac', 'InterpRaw') if 'AtFrac' in k else (k+'InterpRaw') for k in keystonormalize]
                    self.fomnames+=keys_to_interp_orig
                    for k, kraw in zip(keystonormalize, keys_to_interp_orig):
                        newfomd[kraw]=newfomd[k]
                        newfomd[k][newfomd[k]<0]=0.
                    normarr=numpy.float64([newfomd[k] for k in keystonormalize]).sum(axis=0)
                    for k in keystonormalize:
                        newfomd[k]/=normarr
                
                    
                allkeys=list(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)+self.fomnames+self.strkeys_fomdlist#str=valued keys don't go into fomnames
                self.fomdlist=[dict(zip(allkeys, tup)) for tup in zip(*[newfomd[k] for k in allkeys])]

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
