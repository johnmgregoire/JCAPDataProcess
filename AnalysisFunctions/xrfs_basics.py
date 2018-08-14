import numpy, copy,sys,os
if __name__ == "__main__":
    sys.path.append(os.path.split(os.getcwd())[0])

sys.path.append(os.path.split(os.path.realpath(__file__))[0])

from fcns_math import *
from fcns_io import *
from csvfilewriter import createcsvfilstr
from Analysis_Master import *
from FOM_process_basics import FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING


def getapplicablefilenames_specific_usetypetech(expfiledict, usek, techk, typek, runklist=None, requiredparams=[], specificuse='data', specifictech=None, specifictype=None):
    if not ((specificuse is None or usek==specificuse) and (specifictech is None or techk==specifictech) and (specifictype is None or typek==specifictype)):
        return 0, {}
    ###from here down is like stdgetapplicablefilenames but without the keys and sample_no, etc. that would be ready from filleattr
    requiredparams=[(rp+techk) if rp.endswith('__') else rp for rp in requiredparams]
    requiredparams+=['plate_id']
    if runklist is None:
        runklist=expfiledict.keys()
    runklist=[runk for runk in runklist \
    if runk.startswith('run__') and \
        (usek in expfiledict[runk]['run_use']) and \
        ('files_technique__'+techk) in expfiledict[runk].keys() and \
        typek in expfiledict[runk]['files_technique__'+techk].keys()]

    num_files_considered=numpy.int32([len(expfiledict[runk]['files_technique__'+techk][typek]) for runk in runklist]).sum()
    filedlist=[dict(\
                        dict([(reqparam, expfiledict[runk]['parameters'][reqparam]) for reqparam in requiredparams]),\
                                     expkeys=[runk, 'files_technique__'+techk, typek, fnk], run=runk, fn=fnk\
                                )\
            for runk in runklist \
            for fnk in expfiledict[runk]['files_technique__'+techk][typek].keys()\
            if not (False in [reqparam in expfiledict[runk]['parameters'].keys() for reqparam in requiredparams])\
            ]


    filedlist=[dict(d, user_run_foms=expfiledict[d['run']]['user_run_foms'] if 'user_run_foms' in expfiledict[d['run']].keys() else {}) for d in filedlist]#has to be here because only place with access to expfiledict
    filedlist=[dict(d, run_foms=expfiledict[d['run']]['run_foms'] if 'run_foms' in expfiledict[d['run']].keys() else {}) for d in filedlist]#has to be here because only place with access to expfiledict

    return num_files_considered, filedlist


def getapplicable_runs_paramsonly(expfiledict, usek, runklist=None, requiredparams=[]):

    requiredparams+=['plate_id']
    if runklist is None:
        runklist=expfiledict.keys()
    runklist=[runk for runk in runklist \
    if runk.startswith('run__') and \
        (usek in expfiledict[runk]['run_use'])]

    num_files_considered=len(runklist)
    filedlist=[dict(\
                        dict([(reqparam, expfiledict[runk]['parameters'][reqparam]) for reqparam in requiredparams]),\
                                     run=runk, runparamd=expfiledict[runk]['parameters'], runint=int(runk.partition('run__')[2])\
                                        )\
            for runk in runklist \
            if not (False in [reqparam in expfiledict[runk]['parameters'].keys() for reqparam in requiredparams])\
            ]
    return num_files_considered, filedlist
    
class Analysis__XRFS_EDAX(Analysis_Master_nointer):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={'quant_method': 'FP No Stds', 'Inte_append': '.CPS', 'Wt_append': '.WtPerc', 'At_append': '.AtPerc'}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__XRFS_EDAX'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=['StgLabel', 'StagX', 'StagY', 'StagZ', 'StagR']
        self.plotparams={}#dict({}, plot__1={})
        #self.plotparams['plot__1']['x_axis']='t(s)'
        #self.plotparams['plot__1']['series__1']='I(A)'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=self.fomnames[0], colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')

    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None, calcFOMDialogclass=None):
        self.num_files_considered, self.filedlist=getapplicablefilenames_specific_usetypetech(expfiledict, usek, techk, typek, runklist=runklist, specificuse=None, specifictech='XRFS', specifictype='batch_summary_files')
        self.description='reformatting of XRFS batch_summary_files'
#        if len(self.filedlist)>0:
#            self.processnewparams(calcFOMDialogclass=calcFOMDialogclass)
        self.fomnames=['StgLabel', 'StagX', 'StagY', 'StagZ', 'StagR']#to reset this after function used
        return self.filedlist

    def processnewparams(self, calcFOMDialogclass=None):
        return

    def perform(self, destfolder, expdatfolder=None, writeinterdat=False, anak='', zipclass=None, expfiledict=None, anauserfomd={}):#zipclass intended to be the class with open zip archive if expdatfolder is a .zip so that the archive is not repeatedly opened
        self.initfiledicts()
        self.strkeys_fomdlist=[]

        #go through the files once to read data and sample_no.txt
        for filed in self.filedlist:
            fn=filed['fn']


            runp=expfiledict[filed['run']]['run_path']

            runp=buildrunpath(runp)
            runzipclass=gen_zipclass(runp)
            p=os.path.join(runp, fn)

            filed['batch_summary']=read_xrfs_batch_summary_csv(p, select_columns_headings__maindict=self.fomnames, \
                                                                                        include_inte_wt_at_subdicts=True, include_transitionslist_bool=True, read_sample_no_bool=True)


            if 'StgLabel' in self.fomnames and not ('StgLabel' in filed['batch_summary'].keys()):
                self.fomnames.remove('StgLabel')

        #            except:
#                if self.debugmode:
#                    raiseTEMP
#                fomtuplist=[(k, numpy.nan) for k in self.fomnames]
#                pass

        #prepare union of all transitions with the parameter-specified modifications to transitions to creat fom names. None of the 3 midifications should be dientical but this is not checked.
        alltransitions=[]
        for filed in self.filedlist:
            for tr in filed['batch_summary']['transitionslist']:#to preserve order
                if not tr in alltransitions:
                    alltransitions+=[tr]
        batchdictkey_appendstr=[(k, self.params[k.strip('%')+'_append']) for k in ['Inte', 'Wt%', 'At%']]
        keymodfcn=lambda k, a:'%s.%s%s' %(k[:-1], k[-1:], a)
        trfoms=[keymodfcn(tr, s) for k, s in batchdictkey_appendstr for tr in alltransitions]
        self.fomnames=trfoms+self.fomnames
        #go through each file and make the fomdlist entries for each samples_no therein, which may contain duplicate sample_no but those should be differentiated by runint
        self.fomdlist=[]
        for filed in self.filedlist:
            fomd={}
            trfomsmissing=copy.copy(self.fomnames)
            for batchdictkey, appendstr in batchdictkey_appendstr:
                for tk in filed['batch_summary']['transitionslist']:
                    savek=keymodfcn(tk, appendstr)
                    trfomsmissing.pop(trfomsmissing.index(savek))
                    fomd[savek]=filed['batch_summary'][batchdictkey][tk]
            for savek in filed['batch_summary'].keys():
                if savek in trfomsmissing:#for example StagX
                    trfomsmissing.pop(trfomsmissing.index(savek))
                    fomd[savek]=filed['batch_summary'][savek]

            fomd['sample_no']=filed['batch_summary']['sample_no']

            #this zips the fomd arrays into tuple lists. the second line makes a dict for eachof those, adding to it a list of NaN tuples for the missing keys, and the 1st adn 3rd lines add to that dict the common values
            self.fomdlist+=[dict(\
            dict(zip(self.fomnames+['sample_no'], tup)+[(missk, numpy.nan) for missk in trfomsmissing]), \
            plate_id=filed['plate_id'], runint=int(filed['run'].partition('run__')[2]))\
                                        for tup in zip(*[fomd[k] for k in self.fomnames+['sample_no']])]

        self.csvheaderdict['plot_parameters']['plot__1']['fom_name']=trfoms[0]
        allkeys=list(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)+self.fomnames#+self.strkeys_fomdlist#str=valued keys don't go into fomnames


        self.writefom(destfolder, anak, anauserfomd=anauserfomd, strkeys_fomdlist=self.strkeys_fomdlist)#sample_no, plate_id and runint are explicitly required in csv selection above and are assume to be present here

class Analysis__PlatemapComps(Analysis_Master_nointer):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={'key_append_conc':'.PM.Loading', 'key_append_atfrac':'.PM.AtFrac', 'tot_conc_label':'Tot.PM.Loading', 'other_keys_to_include':'x,y,code'}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__PlatemapComps'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=['elements', 'map_id']
        self.fomnames=[]
        self.plotparams=dict({}, plot__1={})#copied in the default getapplicablefomfiles
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})#get for each csv during .perform()
        self.description='calculate platemap compositions for inkj exp'
  
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None, calcFOMDialogclass=None):#just a wrapper around getapplicablefomfiles to keep same argument format as other AnalysisClasses
        
        if True in [not 'platemapdlist' in rund.keys() for runk, rund in calcFOMDialogclass.expfiledict.iteritems() if runk.startswith('run__')]:
            #all platemaps must be available
            self.filedlist=[]
            return self.filedlist
            
        self.num_files_considered, self.filedlist=getapplicable_runs_paramsonly(expfiledict, usek, runklist=None, requiredparams=self.requiredparams)

        return self.filedlist
    
    def processnewparams(self, calcFOMDialogclass=None):
        self.fomnames=[]


    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):#must have same arguments as regular AnaylsisClass
        self.initfiledicts()
        for filed in self.filedlist:
            try:
            #if 1:
                pid =filed['plate_id']
            
                els=filed['elements'].split(',')
                errbool, (cels_set_ordered, conc_el_chan)=get_multielementink_concentrationinfo(filed['runparamd'], els, return_defaults_if_none=True)#None if nothing to report, (True, str) if error, (False, (cels_set_ordered, conc_el_chan)) with the set of elements and how to caclualte their concentration from the platemap                
                pmkeys_to_include=[k.strip() for k in self.params['other_keys_to_include'].split(',')]
                
                
                    
                pmpath=getplatemappath_plateid('', pmidstr=str(filed['map_id']), return_pmidstr=False)
                #pmpath, pmidstr=r'J:\hte_jcap_app_proto\map\0068-04-0100-mp.txt', '69'#for 1-off override
                platemapdlist=readsingleplatemaptxt(pmpath, erroruifcn=None)
                
                
                tot_conc_label=None if len(self.params['tot_conc_label'])==0 else self.params['tot_conc_label']
                calc_comps_multi_element_inks(platemapdlist, cels_set_ordered, conc_el_chan, key_append_conc=self.params['key_append_conc'], key_append_atfrac=self.params['key_append_atfrac'], tot_conc_label=tot_conc_label)
                newfomnames=[el+self.params['key_append_conc'] for el in cels_set_ordered]+\
                                      [el+self.params['key_append_atfrac'] for el in cels_set_ordered]+\
                                      ([] if tot_conc_label is None else [tot_conc_label])
                newfomnames=[lab for lab in newfomnames if not (lab in FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)]
            
                self.fomnames=[k for k in (newfomnames+pmkeys_to_include) if k in platemapdlist[0]]
                if 'code' in self.fomnames:
                    num_intfoms_at_start_of_fomdlist=1
                    self.fomnames.pop(self.fomnames.index('code'))
                    self.fomnames=['code']+self.fomnames
                else:
                    num_intfoms_at_start_of_fomdlist=0
                for d in platemapdlist:
                    d['plate_id']=filed['plate_id']
                    d['runint']=filed['runint']
                
                self.strkeys_fomdlist=[]
                allkeys=list(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)+self.fomnames
                self.fomdlist=platemapdlist

            except:
                if self.debugmode:
                    raiseTEMP
                print 'skipped calculation of ', pid
                self.fomdlist=[]
                continue
            if len(self.fomdlist)==0:
                print 'no foms calculated for ', fn
                continue
            
            plotfomname=self.params['tot_conc_label'] if self.params['tot_conc_label'] in self.fomnames else self.fomnames[0]
            self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=plotfomname, colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')
            self.writefom(destfolder, anak, anauserfomd=anauserfomd, strkeys_fomdlist=self.strkeys_fomdlist, num_intfoms_at_start_of_fomdlist=num_intfoms_at_start_of_fomdlist)#sample_no, plate_id and runint are explicitly required in csv selection above and are assume to be present here
            
