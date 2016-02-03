import numpy, copy
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.split(os.getcwd())[0])

from fcns_math import *
from fcns_io import *
from fcns_ui import *
from csvfilewriter import createcsvfilstr
from Analysis_Master import *
#from scipy.signal import savgol_filter
def savgol_filter(x, y, z, delta=0, deriv=0):
    return x
from bgmath_fcn import *
import matplotlib.pyplot as plt

def BGgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=None, requiredkeys=[], optionalkeys=[], anadict=None):
    anak_ftklist=[(anak, [ftk for ftk in anav.keys() if 'files_run__' in ftk and 'inter_files' in anav[ftk].keys()]) for anak, anav in anadict.iteritems()\
    if anak.startswith('ana__') and True in ['files_' in ftk for ftk in anav.keys()]]

    Afiledlist=[dict({}, anakeys=[anak, ftk, typek, fnk], ana=anak, fn=fnk, sample_no=int(tagandkeys.split(';')[4].strip()), \
                                 nkeys=len(tagandkeys.split(';')[1].split(',')), num_header_lines=int(tagandkeys.split(';')[2]), \
                                 Akeyind=tagandkeys.split(';')[1].split(',').index('abs_smth_scl'), keys=tagandkeys.split(';')[1].split(',')) \
        for anak, ftkl in anak_ftklist \
        for ftk in ftkl \
        for fnk, tagandkeys in anadict[anak][ftk]['inter_files'].iteritems()\
        if 'abs_smth_scl' in tagandkeys and 'uvis_inter_interlen_file' in tagandkeys\
        ]
    if len(Afiledlist)==0:
        return 0, []
    num_files_considered, filedlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=requiredkeys, optionalkeys=optionalkeys)
    
    Asmp=[Ad['sample_no'] for Ad in Afiledlist]
    filedlist2=[dict(d, Afiled=Afiledlist[Asmp.index(d['sample_no'])]) for d in filedlist if (Asmp.count(d['sample_no'])==1)]#require that 1 previous Abs intermediate fiel be found for the given sample_no
    if len(filedlist2)==0:
        aaa
    return num_files_considered, filedlist2#inside of each dict in this list is a 'Afiled' with key 'fn'. That file in the analysis folder is an intermediate data arr whose column 'Akeyind' is the absorption array


#def **************ECHEPHOTO_checkcompletedanalysis_inter_filedlist(filedlist, anadict, requiredanalysisoptions=['Analysis__TR_UVVIS']):
#    anak_ftklist=[(anak, [ftk for ftk in anav.keys() if 'files_run__' in ftk]) for anak, anav in anadict.iteritems()\
#           if anak.startswith('ana__') and (anav['name'] in requiredanalysisoptions) and True in ['files_' in ftk for ftk in anav.keys()]]
#
#    
#    #goes through all inter_files and inter_rawlen_files in all analyses with this correct 'name'. This could be multiple analysis on different runs but if anlaysis done multiple times with different parameters, there is no disambiguation so such sampels are skipped.
#    ##the 'ftk==('files_'+filed['run'])" condition means the run of the raw data is matched to the run in the analysis and this implied that the plate_id is match so matching sample_no would be sufficient, but matching the filename is easiest for now.  #('__'+os.path.splitext(filed['fn'])[0]) in fnk
#    #this used to use [anak, ftk, typek, fnk] but anadict is not available in perform() so use filename because it is the same .ana so should be in same folder
#    interfnks_filedlist=[\
#          [{'fn':fnk, 'keys':tagandkeys.split(';')[1].split(','), 'num_header_lines':int(tagandkeys.split(';')[2])}\
#            for anak, ftkl in anak_ftklist \
#            for ftk in ftkl \
#            for typek in ['inter_files', 'inter_rawlen_files']
#            for fnk, tagandkeys in anadict[anak][ftk][typek].iteritems()\
#                if ftk==('files_'+filed['run']) and int(tagandkeys.split(';')[4].strip())==filed['sample_no']\
#          ]
#        for filed in filedlist]
#    
#    #the keys anakeys__inter_file and anakeys__inter_rawlen_file assume there is only previous required analysis so this needs to be changed if combining multiple types of rpevious analysis
#    filedlist=[dict(filed, ana__inter_filed=interfns[0], ana__inter_rawlen_filed=interfns[1]) \
#          for filed, interfns in zip(filedlist, interfnks_filedlist) if len(interfns)==2]#2 is 1 for inter_files and then for inter_rawlenfiles. if less than 2 then the analysis wasn't done or failed, if >2 then analysis done multiple times
#        
#    return filedlist#inside of each filed are key lists ana__inter_filed and ana__inter_rawlen_filed that provide the path through anadict to get to the fn that mathces the fn in filed
#    
    
def TRgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=None, requiredkeys=[], optionalkeys=[], ref_run_selection='all'):
    if techk!='T_UVVIS':
        return 0, [], {}
    
    #get all refs
    refdict__filedlist=dict([(('ref_dark', 'T_UVVIS'), []), (('ref_light', 'T_UVVIS'), []), (('ref_dark', 'R_UVVIS'), []), (('ref_light', 'R_UVVIS'), [])])
    for k in refdict__filedlist.keys():
        uk, tk=k
#?   runklist,nkeys and keyinds,ntemp,temp,typek
        ntemp, filedlist=stdgetapplicablefilenames(expfiledict, uk, tk, typek, runklist=None, requiredkeys=requiredkeys, optionalkeys=optionalkeys)
#        filedlist is 
        if ref_run_selection.startswith('run__'):#filter to only use refs from user-specified list
            runlist=ref_run_selection.split(',')
            runlist=[s.strip() for s in runlist]
            filedlist=[d for d in filedlist if d['run'] in runlist]
        if len(filedlist)==0:
            return 0, [], {}
        refdict__filedlist[k]=filedlist
    num_files_considered, Tfiledlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=requiredkeys, optionalkeys=optionalkeys)
    ntemp, Rfiledlist=stdgetapplicablefilenames(expfiledict, usek, 'R_UVVIS', typek, runklist=runklist, requiredkeys=requiredkeys, optionalkeys=optionalkeys)
    Rsmp=[Rd['fn'].partition('_')[0] for Rd in Rfiledlist]
    Tfiledlist=[dict(Td, Rfiled=Rfiledlist[Rsmp.index(Td['fn'].partition('_')[0])]) for Td in Tfiledlist if Td['fn'].partition('_')[0] in Rsmp]

    return num_files_considered, Tfiledlist, refdict__filedlist

    
def stdcheckoutput(fomdlist, fomnames):
#?fomdlist
    nancount=[(not k in fomdlist) or numpy.isnan(d[k]) for d in fomdlist for k in fomnames].count(True)
    return nancount, 1.*nancount/(len(fomdlist)*len(fomnames))
    
def refadjust(data,min_mthd_allowed,max_mthd_allowed,min_limit=0.,max_limit=1.):
    min_rescaled=False;max_rescaled=False
    mini=numpy.min(data)
    if mini>=min_mthd_allowed and mini<=min_limit:
        data=data-mini+min_limit+0.01
        min_rescaled=True
    maxi=numpy.max(data)
    if maxi<=max_mthd_allowed and maxi>=max_limit:
        data=data/(maxi+0.01)
        max_rescaled=True
    return min_rescaled,max_rescaled,data
    
def binarray(data,bin_width=1):
#    Odd bin_width is expected for correct usage of median
    reddata=numpy.array([numpy.mean(data[loc:min(loc+bin_width,numpy.size(data))]) for loc in numpy.arange(0,numpy.size(data),bin_width)])
    reddata_idxs=[int(numpy.round(numpy.median(xrange(loc,min(loc+bin_width,numpy.size(data))))))\
    for loc in numpy.arange(0,numpy.size(data),bin_width)]
    return reddata_idxs,reddata
    
def check_inrange(data,min_limit=0.,max_limit=1.): return numpy.min(data)>=min_limit and numpy.max(data)<=max_limit
    
def check_wl(wl_2darray,axis=0):
    if axis:
        wl_2darray=wl_2darray.T
    return len(numpy.where(numpy.array([numpy.abs(wl_2darray[i][k]-wl_2darray[j][k]) for i in xrange(wl_2darray.shape[0]) \
    for j in xrange(0,i) for k in [0,-1]])>0.01)[0])==0
        
def savefomhist(p,fomdlist, histfom,nbins=50):
    arr=numpy.array([fomd[histfom] for fomd in fomdlist])
    nonan_arr=arr[~numpy.isnan(arr)]
    fig=plt.figure()
    hist, bins = numpy.histogram(nonan_arr, bins=nbins)
    center=(bins[:-1]+bins[1:])/2
    width=0.7*(bins[1]-bins[0])
    plt.bar(center,hist,align='center',width=width)
    plt.draw()
    plt.savefig(p,dpi=300)
    plt.close(fig)

class Analysis__TR_UVVIS(Analysis_Master_inter):
    def __init__(self):
        self.analysis_fcn_version='1'
      #TODO int, float, str or dict types and in dict the options are float, int, str  
        self.dfltparams=dict([('lower_wl',385),('upper_wl',950),('bin_width',3),('exclinitcols',0),('exclfincols',0),('reffilesmode', 'static'),\
        ('mthd','TR'),('abs_range',[(1.5,2.0),(2.0,2.5),(2.5,3.0)]),('max_mthd_allowed', 1.2),('min_mthd_allowed', -0.2),('window_length',9),('polyorder',4), \
        ('ref_run_selection', 'all'),('analysis_types',['DA','IA','DF','IF'])])
        
        #TODO: can create a parameter called "ref_run_selection" with default value "all" but could be ,e.g. "run__3,run__6,run__7,run__8,run__9"  \
#        and then if T dark, T light, R dark are runs 3,6,7 respectively then only these runs will be used (if run__2 is also T dark, it will be ignored). 
#        if run__8 and 9 are both R light, the min/max/etc function will be applied to the ensemble of refs in these runs
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__TR_UVVIS'
        #TODO: make intermediate column headings unique from raw
        self.requiredkeys=['Wavelength (nm)','Signal_0']
        self.optionalkeys=['Signal_'+str(x) for x in numpy.arange(1,11)]
        self.requiredparams=[]
        self.processnewparams()
#        print self.fomnames
        #TODO: update plotting defaults on both classes
        self.plotparams=dict({}, plot__1={'x_axis':'E'})
        self.plotparams['plot__1']['x_axis']='E'#this is a single key from raw or inter data
        self.plotparams['plot__1']['series__1']='abs_smth_scl'
#        ,t_smth'#list of keys
#        self.plotparams['plot__1']['series__2']=','.join([fom for fom in self.fomnames if 'abs_' not in fom])
        #in 'plot__1' can have max_value__1,min_value__1,max_value__2,min_value__2
        #self.plotparams['plot__1']['series__2'] for right hand axis
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=','.join(self.fomnames), colormap='jet', colormap_over_color='(0.5,0.,0.)',\
        colormap_under_color='(0.,0.,0.)')
        # also colormap_min_value,colormap_max_value
        
        self.fom_chkqualitynames=['abs_hasnan']
#        changed max_abs2ndderiv(nm^(-2)) to max_abs2ndderiv
        self.quality_foms=['max_abs2ndderiv','min_rescaled','max_rescaled','0<=T<=1','0<=R<=1','0<=T+R<=1']
        self.histfomnames=['max_abs2ndderiv']
        self.tauc_pow=dict([('DA',2),('IA',0.5),('DF',2./3.),('IF',1./3.)])

#        should this be made self.multirunfomnames

    
    def getgeneraltype(self):#make this fucntion so it is inhereted
        return 'standard_with_multiple_data_use'
        
    def processnewparams(self):
        self.fomnames=['abs_'+str(self.params['abs_range'][idx][0])+'_'+str(self.params['abs_range'][idx][1]) \
                             for idx in xrange(len(self.params['abs_range']))]+['max_abs']
                                 
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
        self.num_files_considered, self.filedlist, self.refdict__filedlist=\
              TRgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys, optionalkeys=self.optionalkeys, ref_run_selection=self.params['ref_run_selection'])
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filedlist

    def check_input(self, critfracapplicable=0.9):
        fracapplicable=1.*len(self.filedlist)/self.num_files_considered
        return fracapplicable>critfracapplicable, \
        '%d files, %.2f of those available, do not meet requirements' %(len(self.filedlist)-self.num_files_considered, 1.-fracapplicable)

    def check_output(self, critfracnan=0.9):
        numnan, fracnan=stdcheckoutput(self.fomdlist, self.fom_chkqualitynames)
        return fracnan>critfracnan, \
        '%d samples, %.2f fraction of total samples have NaN in the absorption spectra' %(numnan, fracnan)
        
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}):
        self.initfiledicts(runfilekeys=['inter_rawlen_files','inter_files'])
        self.multirunfiledict['misc_files']={}
        self.fomdlist=[]
        refkeymap=[(('ref_dark', 'T_UVVIS'), 'Tdark'), (('ref_light', 'T_UVVIS'), 'Tlight'), (('ref_dark', 'R_UVVIS'), 'Rdark'), (('ref_light', 'R_UVVIS'), 'Rlight')]
        refd={}#refd will be a dictionary with 4 keys that makes a good start for the intermediate dictionary with raw-data-length arrays
        try:
            refd['wl']=numpy.float32([\
            self.readdata(os.path.join(expdatfolder, filed['fn']), filed['nkeys'], [filed['keyinds'][0]], num_header_lines=filed['num_header_lines'], zipclass=zipclass)[0] \
            for rktup,rk in refkeymap for filed in self.refdict__filedlist[rktup]])[:,::-1]
        except:
            raise ValueError('Number of data points in reference files do not match')
            
        if not check_wl(refd['wl']):
            raise ValueError('Incompatible wavelengths in reference files')
        
        if self.params['reffilesmode']=='static':
            ref_fnd=dict([('Tdark',lambda x:numpy.min(x,axis=0)),('Tlight',lambda x:numpy.max(x,axis=0)),\
            ('Rdark',lambda x:numpy.min(x,axis=0)),('Rlight',lambda x:numpy.max(x,axis=0))])
            refd_all={}
            for rktup, rk in refkeymap:
                refd_all[rk]=numpy.float32([\
                    self.readdata(os.path.join(expdatfolder, filed['fn']), filed['nkeys'], filed['keyinds'][1+self.params['exclinitcols']:len(filed['keyinds'])-self.params['exclfincols']], num_header_lines=filed['num_header_lines'], zipclass=zipclass).mean(axis=0) \
                    for filed in self.refdict__filedlist[rktup]])
                refd[rk]=ref_fnd[rk](refd_all[rk])[::-1]
            refd_fn=lambda fn:refd
            
            #this trivial function costs no time and for nontrivial on-the-fly ref calculations, define a fcn with the same name
        else:#no other ref calculations supported at this time
            return
        
        for filed in self.filedlist:
            fn=filed['fn']
#            print fn
            Rfiled=filed['Rfiled']
            Rfn=Rfiled['fn']
            Tdataarr=self.readdata(os.path.join(expdatfolder, fn), filed['nkeys'], filed['keyinds'], num_header_lines=filed['num_header_lines'], zipclass=zipclass)[:,::-1]
            Rdataarr=self.readdata(os.path.join(expdatfolder, Rfn), Rfiled['nkeys'], Rfiled['keyinds'], num_header_lines=Rfiled['num_header_lines'], zipclass=zipclass)[:,::-1]
#            print np.shape(Tdataarr),np.shape(Rdataarr)
            fomdict,rawlend,interlend=self.fomd_rawlend_interlend(Tdataarr, Rdataarr, refd_fn(fn))
            if not numpy.isnan(filed['sample_no']):#do not save the fom but can save inter data
                fomdict=dict(fomdict, sample_no=filed['sample_no'], plate_id=filed['plate_id'], run=filed['run'], runint=int(filed['run'].partition('run__')[2]))
                self.fomdlist+=[fomdict]
            if destfolder is None:
                continue
            if len(rawlend.keys())>0:
                fnr='%s__%s_rawlen.txt.dat' %(anak, os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fnr)
                kl=saveinterdata(p, rawlend, savetxt=True)
                self.runfiledict[filed['run']]['inter_rawlen_files'][fnr]='%s;%s;%d;%d;%d' %('uvis_inter_rawlen_file', ','.join(kl), 1, len(rawlend[kl[0]]), filed['sample_no'])

            if 'rawselectinds' in interlend.keys():
                fni='%s__%s_interlen.txt.dat' %(anak, os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fni)
                kl=saveinterdata(p, interlend, savetxt=True)
                self.runfiledict[filed['run']]['inter_files'][fni]='%s;%s;%d;%d;%d' %('uvis_inter_interlen_file', ','.join(kl), 1, len(interlend[kl[0]]), filed['sample_no'])
        
        self.writefom(destfolder, anak, anauserfomd=anauserfomd)
        
        if destfolder is None:#dont' do anything with quality items if output not being saved
            return
        
        fnf='%s__%s.csv' %(anak,'qualityfoms')
        #TODO: if quality foms are integers, append them to the intfomkeys and pass [] as 2nd argument
        qualitycsvfilstr=createcsvfilstr(self.fomdlist, self.quality_foms, intfomkeys=['runint','plate_id'])#, fn=fnf)
        p=os.path.join(destfolder,fnf)
        totnumheadlines=writecsv_smpfomd(p, qualitycsvfilstr, headerdict=dict({}, csv_version=self.csvheaderdict['csv_version']))
        self.multirunfiledict['misc_files'][fnf]=\
            '%s;%s;%d;%d' %('csv_fom_file', ','.join(['sample_no', 'runint', 'plate_id']+self.quality_foms), totnumheadlines, len(self.fomdlist))

        for histfom in self.histfomnames:   
            fnhist='%s__%s.png' %(anak,histfom)
            p=os.path.join(destfolder,fnhist)        
            savefomhist(p,self.fomdlist, histfom)
            self.multirunfiledict['misc_files'][fnhist]='hist_fom_file;'
        
        for rktup,rk in refkeymap:
            fn_refimg='%s__%s.png' %(anak,rk)
#            print rk,numpy.shape(refd_all[rk])
            fig=plt.figure()
            for sig,fn in zip(refd_all[rk],[filed['fn'] for filed in self.refdict__filedlist[rktup]]):
                plt.plot(refd['wl'][0],sig,label=os.path.basename(fn))
            plt.legend()
            plt.draw()
            p=os.path.join(destfolder,fn_refimg)
            plt.savefig(p,dpi=300)
            plt.close(fig)
            self.multirunfiledict['misc_files'][fn_refimg]='img_ref_file;'

    def fomd_rawlend_interlend(self, Tdataarr, Rdataarr, refd):
        if Tdataarr.shape[1]!=Rdataarr.shape[1] or Tdataarr.shape[1]!=refd['Tdark'].shape[0]:
            return [('testfom', numpy.nan)], {}, {}
#        print Tdataarr[0][0:5],Rdataarr[0][0:5],refd['wl'][0][0:5]
        if not check_wl(numpy.array(numpy.s_[Tdataarr[0],Rdataarr[0],refd['wl'][0]])):
            raise ValueError('Wavelength incompatibility between Tdata, Rdata and ref')
        inter_rawlend=copy.copy(refd)
        inter_rawlend['wl']=refd['wl'][0]
        inter_selindd={}
        fomd={}
        anal_expr=self.params['mthd']
        if self.params['exclinitcols']+self.params['exclfincols']>=Tdataarr.shape[1]:
            raise ValueError('Insufficient signals to remove %d initial signals and %d end signals'\
            %(self.params['exclinitcols'],self.params['exclfincols']))
        else:
            inter_rawlend['T_av-signal']=Tdataarr[1+self.params['exclinitcols']:Tdataarr.shape[0]-self.params['exclfincols']].mean(axis=0)
            inter_rawlend['R_av-signal']=Rdataarr[1+self.params['exclinitcols']:Rdataarr.shape[0]-self.params['exclfincols']].mean(axis=0)
            inter_rawlend['T_fullrng']=(inter_rawlend['T_av-signal']-refd['Tdark'])/(refd['Tlight']-refd['Tdark'])
            inter_rawlend['R_fullrng']=(inter_rawlend['R_av-signal']-refd['Rdark'])/(refd['Rlight']-refd['Rdark'])
            inter_rawlend[anal_expr+'_fullrng']=inter_rawlend['T_fullrng']/(1.-inter_rawlend['R_fullrng'])
            inds=numpy.where(numpy.logical_and(inter_rawlend['wl']>self.params['lower_wl'],inter_rawlend['wl']<self.params['upper_wl']))[0]
            for key in ['T','R',anal_expr,'wl']:            
                keystr =zip(['_unsmth'],['_fullrng'])[0] if key!='wl'else zip([''],[''])[0]
                bin_idxs,inter_selindd[key+keystr[0]]=binarray(inter_rawlend[key+keystr[1]][inds],bin_width=self.params['bin_width'])
            
            inter_selindd['E']=1239.8/inter_selindd['wl']
            inter_selindd['rawselectinds']=inds[bin_idxs]
            for sigtype in ['T','R']:
                inter_selindd[sigtype+'_smth']=savgol_filter(inter_selindd[sigtype+'_unsmth'], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=0)
            inter_selindd['1-T-R_unsmth']=1.-inter_selindd['T'+'_unsmth']-inter_selindd['R'+'_unsmth']
            inter_selindd['1-T-R_smth']=1.-inter_selindd['T'+'_smth']-inter_selindd['R'+'_smth']
            inter_selindd[anal_expr+'_smth']=inter_selindd['T_smth']/(1.-inter_selindd['R_smth'])            
            fomd['min_rescaled'],fomd['max_rescaled'],inter_selindd[anal_expr+'_smth']=refadjust(inter_selindd[anal_expr+'_smth'],\
            self.params['min_mthd_allowed'],self.params['max_mthd_allowed'])
            inter_selindd['abs_unsmth']=-numpy.log(inter_selindd[anal_expr+'_unsmth'])            
            inter_selindd['abs_smth']=-numpy.log(inter_selindd[anal_expr+'_smth'])
            inter_selindd['abs_smth_scl']=inter_selindd['abs_smth']/numpy.nanmax(inter_selindd['abs_smth'])
            fomd['abs_hasnan']=np.isnan(inter_selindd['abs_smth']).any()
            fomd['max_abs']=numpy.nanmax(inter_selindd['abs_smth'])
            for key in ['abs_'+str(self.params['abs_range'][idx][0])+'_'+str(self.params['abs_range'][idx][1]) for idx in xrange(len(self.params['abs_range']))]:
                inds=numpy.where(numpy.logical_and(inter_selindd['wl']<1239.8/float(key.split('_')[1]),inter_selindd['wl']>1239.8/float(key.split('_')[-1])))[0]
                fomd[key]=numpy.nansum(inter_selindd['abs_smth_scl'][inds])
            for sig_str,sigkey in zip(['T','R','T+R'],['T_smth','R_smth','1-T-R_smth']):
                fomd['0<='+sig_str+'<=1']=check_inrange(inter_selindd[sigkey])
                         
            dx=[inter_selindd['E'][1]-inter_selindd['E'][0]]
            dx+=[(inter_selindd['E'][idx+1]-inter_selindd['E'][idx-1])/2. for idx in xrange(1,len(inter_selindd['rawselectinds'])-1)]
            dx+=[inter_selindd['E'][-1]-inter_selindd['E'][-2]]
            dx=numpy.array(dx) 
            inter_selindd['abs_1stderiv']=savgol_filter(inter_selindd['abs_smth_scl'], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=1)/(dx)
            inter_selindd['abs_2ndderiv']=savgol_filter(inter_selindd['abs_smth_scl'], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=2)/(dx**2)
            fomd['max_abs2ndderiv']=numpy.nanmax(inter_selindd['abs_2ndderiv'])
            
            for typ in self.params['analysis_types']:
                inter_selindd[typ+'_unscl']=(inter_selindd['abs_smth']*inter_selindd['E'])**self.tauc_pow[typ]
                inter_selindd[typ]=inter_selindd[typ+'_unscl']/numpy.max(inter_selindd[typ+'_unscl'])
                fomd[typ+'_minslope']=np.min(savgol_filter(inter_selindd[typ], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=1)/(dx))
        
        return fomd,inter_rawlend,inter_selindd
        
#    
class Analysis__BG(Analysis_Master_inter):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.analysis_name='Analysis__BG'
        self.dfltparams=dict([('num_knots',8),('lower_wl',385),('upper_wl',950),\
            ('tol',1e-06),('maxtol',1e-03),('min_allowedslope',-2),('min_bgTP_diff',0.2),('min_bkgrdslope',-0.05),\
            ('min_bgbkgrdslopediff',0.2),('min_finseglength',0.1),('merge_bgslopediff_percent',10),\
            ('merge_linsegslopediff_percent',10),('min_TP_finseg_diff',0.2),('min_bgfinalseglength',0.2),\
            ('max_merge_differentialTP',0.02),('min_knotdist',0.05),\
            ('abs_minallowedslope',-1),('max_absolute_2ndderiv',0),('analysis_types',['DA']),\
            ('maxbgspersmp',4),('chkoutput_types',['DA'])])
#        CHANGE DEFAULT PARAMETERS TO DA AND IA
        self.params=copy.copy(self.dfltparams)
        self.processnewparams()
        self.requiredkeys=[]#required keys aren't needed for selecting applicable files because the requiremenets for inter_files will be sufficient. Only put requireded_keys that are need in the analysis and these required_keys are of the raw data not inter_data
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fom_chkqualitynames=[bgtyp+'_bg_exists' for bgtyp in self.params['chkoutput_types']]
        self.histfomnames=[bgtyp+'_fit_minslope' for bgtyp in self.params['analysis_types']]
        
        self.plotparams=dict({}, plot__1={'x_axis':'E'})
        self.plotparams['plot__1']['x_axis']='E'#this is a single key from raw or inter data
        self.plotparams['plot__1']['series__1']=self.params['analysis_types'][0]
        
        
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=','.join(self.fomnames), colormap='jet', colormap_over_color='(0.5,0.,0.)',\
        colormap_under_color='(0.,0.,0.)')
        
        
        
    def getgeneraltype(self):#make this fucntion so it is inhereted
        return 'analysis_of_ana'
        
    def processnewparams(self):
        self.fomnames=[item for sublist in [[x+'_abs_expl_'+y,x+'_bg_'+y,x+'_bgcode_'+y,x+'_bg_repr',x+'_code'+'0'+'_only']\
                             for x in self.params['analysis_types'] for y in [str(idx) for idx in xrange(self.params['maxbgspersmp'])]]\
                             for item in sublist]
<<<<<<< HEAD
#    return default params if the new params are incorrect check outputtypes is subset of analtypes
#                              requeired analysis n [An__TR,An__DR]

=======
        
        #check self.params
        if things_are_bad:
            self.params=copy.copy(self.dfltparams)
            idialog=messageDialog(self, 'You enetered ivnalide parameters. They are begin restored to defaults. Please try again.')
            idialog.exec_()
            
>>>>>>> origin/master
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
        self.num_files_considered, self.filedlist=\
              BGgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys,\
              optionalkeys=self.optionalkeys,anadict=anadict)
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filedlist
    def check_input(self, critfracapplicable=0.9):
        fracapplicable=1.*len(self.filedlist)/self.num_files_considered
        return fracapplicable>critfracapplicable, \
        '%d files, %.2f of those available, do not meet requirements' %(len(self.filedlist)-self.num_files_considered, 1.-fracapplicable)

    def check_output(self, critfracnan=0.5):
        numnan, fracnan=stdcheckoutput(self.fomdlist, self.fom_chkqualitynames)
        numnan_abs,fracnan_abs=stdcheckoutput(self.fomdlist, ['abs_hasnan'])
        return fracnan/fracnan_abs>critfracnan, \
        '%d samples, %.2f fraction of total samples with no NaN in absorption have calculable band gaps' %(numnan, fracnan)

    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}):
        self.initfiledicts(runfilekeys=['inter_rawlen_files','inter_files', 'misc_files'])
        self.multirunfiledict['misc_files']={}
        self.fomdlist=[]      
        #inside of each dict in this list is a 'Afiled' with key 'fn'. That file in the analysis \
#        folder is an intermediate data arr whose column 'Akeyind' is the absorption array
        for filed in self.filedlist:
            fn=filed['fn']
            Afiled=filed['Afiled']
            Afn=Afiled['fn']
            rawlend={}
#            print filed.keys(),filed['nkeys']
            Adataarr=self.readdata(os.path.join(destfolder, Afn), Afiled['nkeys'], None, num_header_lines=Afiled['num_header_lines'], zipclass=None)#the inter_data cannot be zipped because it is from the active ana, inds=None will return all inds
            for k, v in zip(Afiled['keys'], Adataarr):
                rawlend[k]=v
#            print rawlend.keys()
            fomdict,linfitd,selindd=self.fomd_rawlend_interlend(rawlend)#use datadict as the argument or use the necessary keys like 'wl' amd 'abs_smth_scl'
            if not numpy.isnan(filed['sample_no']):#do not save the fom but can save inter data
                fomdict=dict(fomdict, sample_no=filed['sample_no'], plate_id=filed['plate_id'], run=filed['run'], runint=int(filed['run'].partition('run__')[2]))
                self.fomdlist+=[fomdict]
            if destfolder is None:
                continue
                
            if len(rawlend.keys())>0:
                fnr='%s__%s_rawlen.txt' %(anak, os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fnr)
                kl=saveinterdata(p, rawlend, savetxt=True)
                self.runfiledict[filed['run']]['inter_rawlen_files'][fnr]='%s;%s;%d;%d;%d' %('uvis_inter_rawlen_file', ','.join(kl), 1, len(rawlend[kl[0]]), filed['sample_no'])

            if 'rawselectinds' in selindd.keys():
                fni='%s__%s_interlen.txt' %(anak, os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fni)
                kl=saveinterdata(p, selindd, savetxt=True)
                self.runfiledict[filed['run']]['inter_files'][fni]='%s;%s;%d;%d;%d' %('uvis_inter_interlen_file', ','.join(kl), 1, len(selindd[kl[0]]), filed['sample_no'])

#            if len(linfitd.keys())>0:
#                print linfitd
#                fnp='%s__%s_linfitparams' %(anak, os.path.splitext(fn)[0])
#                p=os.path.join(destfolder,fnp)
#                kl=saveinterdata(p, linfitd, savetxt=False)
##                linfitd has values that are scalars and arrays and this is a problem at   x=numpy.float32([interd[kv] for kv in keys]) on line 453 in saveinterdata
#                self.runfiledict[filed['run']]['misc_files'][fnp]='%s;%s;%d;%d;%d' %('uvis_inter_linfitparams_dat_file', ','.join(kl), 1, len(linfitd[kl[0]]), filed['sample_no'])
#

        if destfolder is None:
            return

            
        for histfom in self.histfomnames:   
            fnhist='%s__%s.png' %(anak,histfom)
            p=os.path.join(destfolder,fnhist)        
            savefomhist(p,self.fomdlist, histfom)
            self.multirunfiledict['misc_files'][fnhist]='hist_fom_file;'
        
    def fomd_rawlend_interlend(self, rawlend):
        inter_selindd={}
        fomd={}
#        print rawlend.keys()
        inter_selindd['rawselectinds']=numpy.where(numpy.logical_and(rawlend['E']<1239.8/self.params['lower_wl'],rawlend['E']>1239.8/self.params['upper_wl']))[0]
#        print inter_selindd['rawselectinds']
        
        for key in rawlend.keys():
            if key!='rawselectinds':
                inter_selindd[key]=rawlend[key][inter_selindd['rawselectinds']]
        inter_linfitd,fomd=runuvvis(inter_selindd,self.params)                
        bgexists_fcn=lambda x: 1 if x+'_bg_0' in fomd.keys() and not np.isnan(fomd[x+'_bg_0']) else 0
        minslope_fcn=lambda x: np.min(inter_linfitd[typ+'_slopes']) if typ+'_slopes' in inter_linfitd.keys() else np.NaN
        for typ in self.params['analysis_types']:
            fomd[typ+'_bg_exists']=bgexists_fcn(typ)
            fomd[typ+'_fit_minslope']=minslope_fcn(typ)
        return fomd,inter_linfitd,inter_selindd

