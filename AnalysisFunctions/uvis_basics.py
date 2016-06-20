import numpy, copy,os,sys
if __name__ == "__main__":
    sys.path.append(os.path.split(os.getcwd())[0])

sys.path.append(os.path.join(os.path.split(os.getcwd())[0],'AuxPrograms'))

from fcns_math import *
from fcns_io import *
from fcns_ui import *
from csvfilewriter import createcsvfilstr
from Analysis_Master import *
from scipy.signal import savgol_filter
from bgmath_fcn import *
import matplotlib.pyplot as plt
plt.ioff()

def handlenan_savgol_filter(d_arr, window_length, polyorder, delta=1.0, deriv=0,replacenan_value=0.1):
    nans=numpy.isnan(d_arr)    
    xarr=numpy.arange(len(d_arr))
    if len(nans)>1 and len(nans)<len(d_arr):
        d_arr[nans]=numpy.interp(xarr[nans],xarr[~nans],d_arr[~nans])
        naninds=numpy.where(numpy.isnan(d_arr))[0]
        if len(naninds)>1:
            d_arr[naninds]=numpy.array([numpy.nanmean(d_arr[max(0,nind-3):min(nind+3,len(d_arr))]) for nind in naninds])
    try:
        return savgol_filter(d_arr, window_length, polyorder, delta=1.0, deriv=0)
    except:
        nans=numpy.isnan(d_arr)
        if len(nans)>1:
            d_arr[nans]=replacenan_value
        return savgol_filter(d_arr, window_length, polyorder, delta=1.0, deriv=0)    

def BGgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=None, requiredkeys=[], optionalkeys=[], anadict=None):
    anak_ftklist=[(anak, [ftk for ftk in anav.keys() if 'files_run__' in ftk and 'inter_files' in anav[ftk].keys()]) for anak, anav in anadict.iteritems()\
    if anak.startswith('ana__') and True in ['files_' in ftk for ftk in anav.keys()]]

    Afiledlist=[dict({}, anakeys=[anak, ftk, typek, fnk], ana=anak, fn=fnk, sample_no=int(tagandkeys.split(';')[4].strip()), \
                                 nkeys=len(tagandkeys.split(';')[1].split(',')), num_header_lines=int(tagandkeys.split(';')[2]), \
                                 Akeyind=tagandkeys.split(';')[1].split(',').index('abs_smth_refadj_scl'), keys=tagandkeys.split(';')[1].split(',')) \
        for anak, ftkl in anak_ftklist \
        for ftk in ftkl \
        for fnk, tagandkeys in anadict[anak][ftk]['inter_files'].iteritems()\
        if 'abs_smth_refadj_scl' in tagandkeys and 'uvis_inter_interlen_file' in tagandkeys and not '_bg' in tagandkeys\
        ]
    if len(Afiledlist)==0:
        return 0, []
    num_files_considered, filedlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=requiredkeys, optionalkeys=optionalkeys)
    
    Asmp=[Ad['sample_no'] for Ad in Afiledlist]
    filedlist2=[dict(d, Afiled=Afiledlist[Asmp.index(d['sample_no'])]) for d in filedlist if (Asmp.count(d['sample_no'])==1)]#require that 1 previous Abs intermediate fiel be found for the given sample_no
    if len(filedlist2)==0:
        print 'length of filedlist2 is zero'
    return num_files_considered, filedlist2#inside of each dict in this list is a 'Afiled' with key 'fn'. That file in the analysis folder is an intermediate data arr whose column 'Akeyind' is the absorption array

    
def TRgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=None, requiredkeys=[], optionalkeys=[], ref_run_selection='all', gui_mode_bool=False):
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
            if gui_mode_bool :
                print 'NO REFERENCE DATA AVAILABLE FOR %s in %s' %(k, 'TRgetapplicablefilenames')
            return 0, [], {}
        refdict__filedlist[k]=filedlist
    num_files_considered, Tfiledlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=requiredkeys, optionalkeys=optionalkeys)
    ntemp, Rfiledlist=stdgetapplicablefilenames(expfiledict, usek, 'R_UVVIS', typek, runklist=runklist, requiredkeys=requiredkeys, optionalkeys=optionalkeys)
    Rsmp=[Rd['fn'].partition('_')[0] for Rd in Rfiledlist]
    Tfiledlist=[dict(Td, Rfiled=Rfiledlist[Rsmp.index(Td['fn'].partition('_')[0])]) for Td in Tfiledlist if Td['fn'].partition('_')[0] in Rsmp]

    return num_files_considered, Tfiledlist, refdict__filedlist
    
    
def DRgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=None, requiredkeys=[], optionalkeys=[], ref_run_selection='all',gui_mode_bool=False):
    if techk!='DR_UVVIS':
        return 0, [], {}
    
    #get all refs
    refdict__filedlist=dict([(('ref_dark', 'DR_UVVIS'), []), (('ref_light', 'DR_UVVIS'), [])])
    for k in refdict__filedlist.keys():
        uk, tk=k
#?   runklist,nkeys and keyinds,ntemp,temp,typek
        ntemp, filedlist=stdgetapplicablefilenames(expfiledict, uk, tk, typek, runklist=None, requiredkeys=requiredkeys, optionalkeys=optionalkeys)
#        filedlist is 
        if ref_run_selection.startswith('run__'):#filter to only use refs from user-specified list
            runlist=ref_run_selection.split(',')
            runlist=[s.strip() for s in runlist]
            filedlist=[d for d in filedlist if d['run'] in runlist]
#        print filedlist
        #print filedlist
        if len(filedlist)==0:
            if gui_mode_bool :
                print 'NO REFERENCE DATA AVAILABLE FOR %s in %s' %(k, 'DRgetapplicablefilenames')
            return 0, [], {}
        refdict__filedlist[k]=filedlist
    num_files_considered, DRfiledlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=requiredkeys, optionalkeys=optionalkeys)
    refdict__filedlist[k]=filedlist
    return num_files_considered, DRfiledlist, refdict__filedlist
    
def Tgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=None, requiredkeys=[], optionalkeys=[], ref_run_selection='all',gui_mode_bool=False):
    if techk!='T_UVVIS':
        return 0, [], {}
    
    #get all refs
    refdict__filedlist=dict([(('ref_dark', 'T_UVVIS'), []), (('ref_light', 'T_UVVIS'), [])])
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
            if gui_mode_bool :
                print 'NO REFERENCE DATA AVAILABLE FOR %s in %s' %(k, 'DRgetapplicablefilenames')
            return 0, [], {}
        refdict__filedlist[k]=filedlist
    num_files_considered, Tfiledlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=requiredkeys, optionalkeys=optionalkeys)

    return num_files_considered, Tfiledlist, refdict__filedlist

    
def stdcheckoutput(fomdlist, fomnames):
#?fomdlist
    nancount=[(not k in fomdlist) or numpy.isnan(d[k]) for d in fomdlist for k in fomnames].count(True)
    return nancount, 1.*nancount/(len(fomdlist)*len(fomnames))
    
def refadjust(data,min_mthd_allowed,max_mthd_allowed,min_limit=0.,max_limit=1.):
    min_rescaled=False;max_rescaled=False
    mini=numpy.nanmin(data)
    if mini>=min_mthd_allowed and mini<=min_limit:
        data=data-mini+min_limit+0.01
        min_rescaled=True
    maxi=numpy.nanmax(data)
    if maxi<=max_mthd_allowed and maxi>=max_limit:
        data=data/(maxi+0.01)
        max_rescaled=True
    return min_rescaled,max_rescaled,data
    
def refadjust_TR(Tdata,Rdata,mthd_smth,Tref,Rref,min_mthd_allowed,ch_ref='T',min_limit=0,max_limit=1.):
    min_rescaled=False;max_rescaled=False    
    mini=numpy.nanmin(mthd_smth)
    mini_idx=numpy.nanargmin(mthd_smth)
    sdata=eval(ch_ref+'data')
    sdark=eval(ch_ref+'dark')
    sref=eval(ch_ref+'ref')
    
    if mini>=min_mthd_allowed and mini<=min_limit:
        x=(sdata[mini_idx]-(1.-0.01)*sdark[mini_idx])/(0.01*sref[mini_idx])
        mthd_smth_refadj=(sdata-sdark)/(x*sref-sdark)
        min_rescaled=True
    maxi=numpy.nanmax(data)
    maxi_idx=numpy.nanargmax(mthd_smth)
    
    if maxi<=max_mthd_allowed and maxi>=max_limit:
        x=(sdata[maxi_idx]-(1.-0.99)*sdark[maxi_idx])/(0.99*sref[maxi_idx])
        mthd_smth_refadj=(sdata-sdark)/(x*sref-sdark)
        max_rescaled=True
        
    if not min_rescaled or max_rescaled:
        return mthd_smth
    else:
        return mthd_smth_refadj
        
        
def binarray(data,bin_width=1):
#    Odd bin_width is expected for correct usage of median
    reddata=numpy.array([numpy.mean(data[loc:min(loc+bin_width,numpy.size(data))]) for loc in numpy.arange(0,numpy.size(data),bin_width)])
    reddata_idxs=[int(numpy.round(numpy.median(xrange(loc,min(loc+bin_width,numpy.size(data))))))\
    for loc in numpy.arange(0,numpy.size(data),bin_width)]
    return reddata_idxs,reddata
    
def check_inrange(data,min_limit=0.,max_limit=1.): return numpy.min(data)>min_limit and numpy.max(data)<max_limit
    
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
        self.dfltparams=dict([('lower_wl',370),('upper_wl',1020),('bin_width',3),('exclinitcols',0),('exclfincols',0),('reffilesmode', 'static'),\
        ('mthd','TR'),('abs_range',[(1.5,2.0),(2.0,2.5),(2.5,3.0)]),('max_mthd_allowed', 1.2),('min_mthd_allowed', -0.2),('window_length',45),('polyorder',4), \
        ('ref_run_selection', 'all'),('analysis_types',['DA','IA','DF','IF']),('chkoutput_wlrange',[410,850])])
        
#         "ref_run_selection" has default value "all" but could be ,e.g. "run__3,run__6,run__7,run__8,run__9"  \
#        and then if T dark, T light, R dark are runs 3,6,7 respectively then only these runs will be used (if run__2 is also T dark, it will be ignored). 
#        if run__8 and 9 are both R light, the min/max/etc function will be applied to the ensemble of refs in these runs
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__TR_UVVIS'
        
        self.requiredkeys=['Wavelength (nm)','Signal_0']
        self.optionalkeys=['Signal_'+str(x) for x in numpy.arange(1,11)]
        self.requiredparams=[]
        self.qualityfoms=['min_rescaled','max_rescaled','0<T<1','0<R<1','0<T+R<1']
        self.fom_chkqualitynames=['abs_hasnan']
        self.histfomnames=['max_abs2ndderiv','min_abs1stderiv']

        self.processnewparams()
        #TODO: update plotting defaults on both classes
        self.plotparams=dict({}, plot__1={'x_axis':'hv'})
        self.plotparams['plot__1']['x_axis']='hv'#this is a single key from raw or inter data
        self.plotparams['plot__1']['series__1']='abs_smth_refadj,abs_smth_refadj_scl'
        self.plotparams['plot__1']['series__2']='abs_smth'
#        ,t_smth'#list of keys
        #in 'plot__1' can have max_value__1,min_value__1,max_value__2,min_value__2
        #self.plotparams['plot__1']['series__2'] for right hand axis
        self.tauc_pow=dict([('DA',2),('IA',0.5),('DF',2./3.),('IF',1./3.)])


    
    def getgeneraltype(self):#make this fucntion so it is inhereted
        return 'standard_with_multiple_data_use'
        
    def processnewparams(self):
        self.fomnames=['abs_'+str(self.params['abs_range'][idx][0])+'_'+str(self.params['abs_range'][idx][1]) \
                             for idx in xrange(len(self.params['abs_range']))]+['max_abs']
        
        if self.params['window_length'] %2!=1:
            self.params['window_length']+=1
            
        if numpy.array([str(x).strip()=='' for x in self.params.values()]).any():
            self.params=copy.copy(self.dfltparams)
            idialog=messageDialog(self, 'You enetered invalid parameters. They are being restored to defaults. Please try again.')
            idialog.exec_()
        
        if self.params['reffilesmode'] not in ['time','static']:
            self.params['reffilesmode']='static'
            idialog=messageDialog(self, 'Pls use static or time as options for reffilesmode, resetting to static. Please try again for time option.')
            idialog.exec_()
            
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        for idx,fom in enumerate(self.fomnames):
            self.csvheaderdict['plot_parameters']['plot__'+str(idx+1)]=dict({}, fom_name=fom,\
            colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')
        self.qualityfomcsvheaderdict=dict({}, csv_version='1', plot_parameters={})
        for idx,qfom in enumerate(self.qualityfoms):
            self.qualityfomcsvheaderdict['plot_parameters']['plot__'+str(idx+1)]=dict({}, fom_name=qfom,\
            colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')

                                 
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
        self.num_files_considered, self.filedlist, self.refdict__filedlist=\
              TRgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys, optionalkeys=self.optionalkeys, ref_run_selection=self.params['ref_run_selection'], gui_mode_bool=self.gui_mode_bool)
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filedlist

    def check_input(self, critfracapplicable=0.9):
        fracapplicable=1.*len(self.filedlist)/self.num_files_considered
        return fracapplicable>critfracapplicable, \
        '%d files, %.2f of those available, do not meet requirements' %(len(self.filedlist)-self.num_files_considered, 1.-fracapplicable)

    def check_output(self, critfracnan=0.9):
        numnan, fracnan=stdcheckoutput(self.fomdlist, self.fom_chkqualitynames)
        return fracnan>critfracnan, \
        '%d samples, %.2f fraction of total samples have NaN in the absorption spectra in the wavelength range %.2f to %.2f' %(numnan, fracnan,self.params['chkoutput_wlrange'][0],self.params['chkoutput_wlrange'][1])
    
    def setuprefdata(self, refkeymap, static_ref_fnd, anak='', destfolder=None):
        #All filed , T, R and ref, prepared for file reading here
        
        refd={}#refd will be a dictionary with 4 keys that makes a good start for the intermediate ref dictionary with raw-data-length arrays
        refd_all={}            
        for count, (rktup, rk) in enumerate(refkeymap):
            #ref3d first index is files, second index is data column, e.g. wavelength, signal1, and 3rd index is data point
            refdat3d=[filed['readfcn'](*filed['readfcn_args'], **filed['readfcn_kwargs'])[:,::-1] for filed in self.refdict__filedlist[rktup]]
            
            if count==0:
                refd['wl_fullrng']=refdat3d[0][0]
            #only check the new wl arrays, if everythign is good refd['wl_fullrng'] does not need to be update, refdat2d[0] is the wl for each file
            if (not numpy.all(numpy.array([len(refdat2d[0]) for refdat2d in refdat3d])==len(refd['wl_fullrng'])))\
                or not check_wl(numpy.array([refd['wl_fullrng']]+[refdat2d[0] for refdat2d in refdat3d])):
                if self.debugmode:
                    raise ValueError('Incompatible wavelengths in reference files')
                return True, None
            #all data arrays will be the same length because if not, the wl length check above would fail, refdat2d[1:] takes all columns except wl
            refd_all[rk]=numpy.float32([refdat2d[1:].mean(axis=0) for refdat2d in refdat3d])#this mean is over the signal1,2,3 so that each refd_all[rk] has first index of ref filed so it is indexed the same as self.refdict__filedlist[rktup] (second index is data ooint)

        if self.params['reffilesmode']=='static':
            
            for rktup, rk in refkeymap:
                refd[rk]=static_ref_fnd[rk](refd_all[rk])
            refd_fn=lambda sample_no: refd
            
            #this trivial function costs no time and for nontrivial on-the-fly ref calculations, define a fcn with the same name
        elif self.params['reffilesmode']=='time':
            for filed in self.filedlist:            
                refd[filed['sample_no']]={}
                try:
                    smp_time_fcn=lambda fd: int(fd['fn'].split('_')[-1].split('.')[0])
                    smp_time=smp_time_fcn(filed)
                except:
                    smp_time_fcn=lambda fd: int(fd['fn'].split('_')[-2].split('.')[0])
                    smp_time=smp_time_fcn(filed)
                for rktup,rk in refkeymap:
                    ref_time_arr=numpy.array([smp_time_fcn(ref_filed) for ref_filed in self.refdict__filedlist[rktup]])
                    refd[filed['sample_no']][rk]=refd_all[rk][numpy.argmin((ref_time_arr-smp_time)**2)]
                refd[filed['sample_no']]['wl_fullrng']=refd['wl_fullrng']
            refd_fn=lambda sample_no:refd[sample_no]
        else:
            if self.debugmode:
                raise ValueError('invalid reffilesmode')
            return True, None
            
        if not destfolder is None:
            for rktup,rk in refkeymap:
                fn_refimg='%s__%s.png' %(anak,rk)
    #            print rk,numpy.shape(refd_all[rk])
                fig=plt.figure()
                ax=fig.add_subplot(111)
                for sig,fn in zip(refd_all[rk],[filed['fn'] for filed in self.refdict__filedlist[rktup]]):
                    ax.plot(refd['wl_fullrng'],sig,label=os.path.basename(fn))

                box = ax.get_position()
                ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
# Put a legend to the right of the current axis
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize=8)
                plt.draw()
                p=os.path.join(destfolder,fn_refimg)
                plt.savefig(p,dpi=300)
                plt.close(fig)
                self.multirunfiledict['misc_files'][fn_refimg]='img_ref_file;'
            
        return False, refd_fn
        
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):#TODO propogate , expfiledict=None
        self.initfiledicts(runfilekeys=['inter_rawlen_files','inter_files'])
        self.multirunfiledict['misc_files']={}
        
        self.fomdlist=[]
        refkeymap=[(('ref_dark', 'T_UVVIS'), 'Tdark'), (('ref_light', 'T_UVVIS'), 'Tlight'), (('ref_dark', 'R_UVVIS'), 'Rdark'), (('ref_light', 'R_UVVIS'), 'Rlight')]
        
        static_ref_fnd=dict([('Tdark',lambda x:numpy.min(x,axis=0)),('Tlight',lambda x:numpy.max(x,axis=0)),\
            ('Rdark',lambda x:numpy.min(x,axis=0)),('Rlight',lambda x:numpy.max(x,axis=0))])
            

   
        for filed in [fd for rktup,rk in refkeymap for fd in self.refdict__filedlist[rktup]]:
            #'keyinds is ordered the same as required_keys and then optinoal_keys, but not anymore for ref data
            filed['keyinds']=[0]+filed['keyinds'][1+self.params['exclinitcols']:len(filed['keyinds'])-self.params['exclfincols']]#update the keyinds to keep zero index, which is the wl, and then select other columns
            if len(filed['keyinds'])==1:#only wavelength left so need to abort analysis
                if self.debugmode:
                    raise ValueError('select ref columns resulted in no remaining Signals')
                self.writefom(destfolder, anak, anauserfomd=anauserfomd, createdummyfomdlist=True)
                return
        
        closeziplist=self.prepare_filedlist(\
            [d for filed in self.filedlist for d in [filed, filed['Rfiled']]]+\
            [fd for rktup,rk in refkeymap for fd in self.refdict__filedlist[rktup]], \
                expfiledict, expdatfolder=expdatfolder, expfolderzipclass=zipclass, fnk='fn')#combine the filed, Rfiled, etc. together in 1 list so that any runzips are only opened once
        
        referror, refd_fn=self.setuprefdata(refkeymap,  static_ref_fnd, anak=anak, destfolder=destfolder)
        if referror:
            self.writefom(destfolder, anak, anauserfomd=anauserfomd, createdummyfomdlist=True)
            for zc in closeziplist:
                zc.close()
            return
    
        ####filed['readfcn'](*filed['readfcn_args'], **filed['readfcn_kwargs'])[:,::-1]         , expfiledict=None

        
        for filed in self.filedlist:
            fn=filed['fn']
#            print fn
            Rfiled=filed['Rfiled']
            Rfn=Rfiled['fn']
            Tdataarr=filed['readfcn'](*filed['readfcn_args'], **filed['readfcn_kwargs'])[:,::-1]
            Rdataarr=Rfiled['readfcn'](*Rfiled['readfcn_args'], **Rfiled['readfcn_kwargs'])[:,::-1]
#            print numpy.shape(Tdataarr),numpy.shape(Rdataarr)
            fomdict,rawlend,interlend=self.fomd_rawlend_interlend(Tdataarr, Rdataarr, refd_fn(filed['sample_no']))
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

            if 'rawselectinds' in interlend.keys():
                fni='%s__%s_interlen.txt' %(anak, os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fni)
                kl=saveinterdata(p, interlend, savetxt=True)
                self.runfiledict[filed['run']]['inter_files'][fni]='%s;%s;%d;%d;%d' %('uvis_inter_interlen_file', ','.join(kl), 1, len(interlend[kl[0]]), filed['sample_no'])
        
        self.writefom(destfolder, anak, anauserfomd=anauserfomd)
        
        for zc in closeziplist:
            zc.close()
            
        if destfolder is None:#dont' do anything with quality items if output not being saved
            return
        
        fnf='%s__%s.csv' %(anak,'qualityfoms')
        #TODO: if quality foms are integers, append them to the intfomkeys and pass [] as 2nd argument
#        qualitycsvfilstr=createcsvfilstr(self.fomdlist, self.qualityfoms, intfomkeys=['runint','plate_id']) if qualityfoms are not integers
        qualitycsvfilstr=createcsvfilstr(self.fomdlist, [], intfomkeys=['runint','plate_id']+self.qualityfoms)#, fn=fnf)
        p=os.path.join(destfolder,fnf)
        totnumheadlines=writecsv_smpfomd(p, qualitycsvfilstr, headerdict=dict({}, csv_version=self.qualityfomcsvheaderdict['csv_version']))
        self.multirunfiledict['misc_files'][fnf]=\
            '%s;%s;%d;%d' %('csv_fom_file', ','.join(['sample_no', 'runint', 'plate_id']+self.qualityfoms), totnumheadlines, len(self.fomdlist))

        for histfom in self.histfomnames:   
            fnhist='%s__%s.png' %(anak,histfom)
            p=os.path.join(destfolder,fnhist)        
            savefomhist(p,self.fomdlist, histfom)
            self.multirunfiledict['misc_files'][fnhist]='hist_fom_file;'
        


    def fomd_rawlend_interlend(self, Tdataarr, Rdataarr, refd):
        if Tdataarr.shape[1]!=Rdataarr.shape[1] or Tdataarr.shape[1]!=refd['Tdark'].shape[0]:
            return [('testfom', numpy.nan)], {}, {}
#        print Tdataarr[0][0:5],Rdataarr[0][0:5],refd['wl'][0][0:5]
        if not check_wl(numpy.array(numpy.s_[Tdataarr[0],Rdataarr[0],refd['wl_fullrng']])):
            raise ValueError('Wavelength incompatibility between Tdata, Rdata and ref')
        inter_rawlend=copy.copy(refd)
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
            inter_rawlend['1-T-R_fullrng']=1.-inter_rawlend['T'+'_fullrng']-inter_rawlend['R'+'_fullrng']
            inter_rawlend['abs'+'_fullrng']=-numpy.log(inter_rawlend[anal_expr+'_fullrng'])
            inds=numpy.where(numpy.logical_and(inter_rawlend['wl_fullrng']>self.params['lower_wl'],inter_rawlend['wl_fullrng']<self.params['upper_wl']))[0]
            for key in ['T','R',anal_expr,'abs','1-T-R','wl']:            
                keystr =zip(['_unsmth'],['_fullrng'])[0] if key!='wl' else zip([''],['_fullrng'])[0]
                bin_idxs,inter_selindd[key+keystr[0]]=binarray(inter_rawlend[key+keystr[1]][inds],bin_width=self.params['bin_width'])
                
            inter_selindd['hv']=1239.8/inter_selindd['wl']
            inter_selindd['rawselectinds']=inds[bin_idxs]
            for sigtype in ['T','R',anal_expr,'abs','1-T-R']:
                inter_selindd[sigtype+'_smth']=handlenan_savgol_filter(inter_selindd[sigtype+'_unsmth'], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=0)
            fomd['min_rescaled'],fomd['max_rescaled'],inter_selindd[anal_expr+'_smth'+'_refadj']=refadjust(inter_selindd[anal_expr+'_smth'], \
            self.params['min_mthd_allowed'],self.params['max_mthd_allowed'])
            inter_selindd['abs_smth_refadj']=-numpy.log(inter_selindd[anal_expr+'_smth_refadj'])
            inter_selindd['abs_smth_refadj_scl']=inter_selindd['abs_smth_refadj']/numpy.nanmax(inter_selindd['abs_smth_refadj'])
            chkoutput_inds=numpy.where(numpy.logical_and(inter_selindd['wl']>self.params['chkoutput_wlrange'][0],inter_selindd['wl']<self.params['chkoutput_wlrange'][1]))[0]
            fomd['abs_hasnan']=numpy.isnan(inter_selindd['abs_smth_refadj'][chkoutput_inds]).any()
            fomd['max_abs']=numpy.nanmax(inter_selindd['abs_smth_refadj'])
            for key in ['abs_'+str(self.params['abs_range'][idx][0])+'_'+str(self.params['abs_range'][idx][1]) for idx in xrange(len(self.params['abs_range']))]:
                inds=numpy.where(numpy.logical_and(inter_selindd['wl']<1239.8/float(key.split('_')[1]),inter_selindd['wl']>1239.8/float(key.split('_')[-1])))[0]
                fomd[key]=numpy.nansum(inter_selindd['abs_smth_refadj'][inds])
            for sig_str,sigkey in zip(['T','R','T+R'],['T_smth','R_smth','1-T-R_smth']):
                fomd['0<'+sig_str+'<1']=check_inrange(inter_selindd[sigkey])
                         
            dx=[inter_selindd['hv'][1]-inter_selindd['hv'][0]]
            dx+=[(inter_selindd['hv'][idx+1]-inter_selindd['hv'][idx-1])/2. for idx in xrange(1,len(inter_selindd['rawselectinds'])-1)]
            dx+=[inter_selindd['hv'][-1]-inter_selindd['hv'][-2]]
            dx=numpy.array(dx) 
            inter_selindd['abs_1stderiv']=handlenan_savgol_filter(inter_selindd['abs_smth_refadj_scl'], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=1)/(dx)
            inter_selindd['abs_2ndderiv']=handlenan_savgol_filter(inter_selindd['abs_smth_refadj_scl'], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=2)/(dx**2)
            fomd['max_abs2ndderiv']=numpy.nanmax(inter_selindd['abs_2ndderiv'])
            fomd['min_abs1stderiv']=numpy.nanmin(inter_selindd['abs_1stderiv'])
            
            for typ in self.params['analysis_types']:
                inter_selindd[typ+'_unscl']=(inter_selindd['abs_smth_refadj']*inter_selindd['hv'])**self.tauc_pow[typ]
                inter_selindd[typ]=inter_selindd[typ+'_unscl']/numpy.max(inter_selindd[typ+'_unscl'])
                fomd[typ+'_minslope']=numpy.min(handlenan_savgol_filter(inter_selindd[typ], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=1)/(dx))
                if len(numpy.where(numpy.isnan(inter_selindd[typ]))[0]) > 0 or len(numpy.where(numpy.isinf(numpy.abs(inter_selindd[typ])))[0])>0:
                    fomd[typ+'_minslope']=numpy.min(handlenan_svagol_filter(inter_selindd[typ], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=1)/(dx))        
        return fomd,inter_rawlend,inter_selindd
        




class Analysis__DR_UVVIS(Analysis__TR_UVVIS):
    def __init__(self):
        self.analysis_fcn_version='1'
      #TODO int, float, str or dict types and in dict the options are float, int, str  
        self.dfltparams=dict([('lower_wl',385),('upper_wl',950),('bin_width',3),('exclinitcols',0),('exclfincols',0),('reffilesmode', 'static'),\
        ('mthd','DR'),('abs_range',[(1.5,2.0),(2.0,2.5),(2.5,3.0)]),('max_mthd_allowed', 1.2),('min_mthd_allowed', -0.2),('window_length',45),('polyorder',4), \
        ('ref_run_selection', 'all'),('analysis_types',['DA','IA','DF','IF']),('chkoutput_wlrange',[410,850])])
        
        # "ref_run_selection" has default value "all" but could be ,e.g. "run__3,run__6,run__7,run__8,run__9"  \
#        and then if T dark, T light, R dark are runs 3,6,7 respectively then only these runs will be used (if run__2 is also T dark, it will be ignored). 
#        if run__8 and 9 are both R light, the min/max/etc function will be applied to the ensemble of refs in these runs
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__DR_UVVIS'
        #TODO: make intermediate column headings unique from raw
        self.requiredkeys=['Wavelength (nm)','Signal_0']
        self.optionalkeys=['Signal_'+str(x) for x in numpy.arange(1,11)]
        self.requiredparams=[]
        self.fom_chkqualitynames=['abs_hasnan']
        self.qualityfoms=['min_rescaled','max_rescaled','0<DR<1']
        self.histfomnames=['max_abs2ndderiv','min_abs1stderiv']
        self.processnewparams()

        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='hv'#this is a single key from raw or inter data
        self.plotparams['plot__1']['series__1']='abs_smth_refadj_scl'
#        ,t_smth'#list of keys
#        self.plotparams['plot__1']['series__2']=','.join([fom for fom in self.fomnames if 'abs_' not in fom])
        #in 'plot__1' can have max_value__1,min_value__1,max_value__2,min_value__2
        #self.plotparams['plot__1']['series__2'] for right hand axis

        # also colormap_min_value,colormap_max_value
        self.tauc_pow=dict([('DA',2),('IA',0.5),('DF',2./3.),('IF',1./3.)])


    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
        self.num_files_considered, self.filedlist, self.refdict__filedlist=\
        DRgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys, optionalkeys=self.optionalkeys, ref_run_selection=self.params['ref_run_selection'])
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filedlist
        
        
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):
        self.initfiledicts(runfilekeys=['inter_rawlen_files','inter_files'])
        self.multirunfiledict['misc_files']={}
        self.fomdlist=[]
        refkeymap=[(('ref_dark', 'DR_UVVIS'), 'DRdark'), (('ref_light', 'DR_UVVIS'), 'DRlight')]
        
        static_ref_fnd=dict([('DRdark',lambda x:numpy.min(x,axis=0)),('DRlight',lambda x:numpy.max(x,axis=0))])

   
        for filed in [fd for rktup,rk in refkeymap for fd in self.refdict__filedlist[rktup]]:
            #'keyinds is ordered the same as required_keys and then optinoal_keys, but not anymore for ref data
            filed['keyinds']=[0]+filed['keyinds'][1+self.params['exclinitcols']:len(filed['keyinds'])-self.params['exclfincols']]#update the keyinds to keep zero index, which is the wl, and then select other columns
            if len(filed['keyinds'])==1:#only wavelength left so need to abort analysis
                if self.debugmode:
                    raise ValueError('select ref columns resulted in no remaining Signals')
                self.writefom(destfolder, anak, anauserfomd=anauserfomd, createdummyfomdlist=True)
                return
        
        closeziplist=self.prepare_filedlist(\
            [filed for filed in self.filedlist]+\
            [fd for rktup,rk in refkeymap for fd in self.refdict__filedlist[rktup]], \
                expfiledict, expdatfolder=expdatfolder, expfolderzipclass=zipclass, fnk='fn')#combine the filed, Rfiled, etc. together in 1 list so that any runzips are only opened once
        
        referror, refd_fn=self.setuprefdata(refkeymap,  static_ref_fnd, anak=anak, destfolder=destfolder)
        if referror:
            self.writefom(destfolder, anak, anauserfomd=anauserfomd, createdummyfomdlist=True)
            for zc in closeziplist:
                zc.close()
            return
        
        
        for filed in self.filedlist:
            fn=filed['fn']
            DRdataarr=filed['readfcn'](*filed['readfcn_args'], **filed['readfcn_kwargs'])[:,::-1]
#            print numpy.shape(DRdataar)
            fomdict,rawlend,interlend=self.fomd_rawlend_interlend(DRdataarr,refd_fn(filed['sample_no']))
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

            if 'rawselectinds' in interlend.keys():
                fni='%s__%s_interlen.txt' %(anak, os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fni)
                kl=saveinterdata(p, interlend, savetxt=True)
                self.runfiledict[filed['run']]['inter_files'][fni]='%s;%s;%d;%d;%d' %('uvis_inter_interlen_file', ','.join(kl), 1, len(interlend[kl[0]]), filed['sample_no'])
        
        self.writefom(destfolder, anak, anauserfomd=anauserfomd)
        for zc in closeziplist:
            zc.close()
            
        if destfolder is None:#dont' do anything with quality items if output not being saved
            return
        
        fnf='%s__%s.csv' %(anak,'qualityfoms')
        #TODO: if quality foms are integers, append them to the intfomkeys and pass [] as 2nd argument
        qualitycsvfilstr=createcsvfilstr(self.fomdlist, self.qualityfoms, intfomkeys=['runint','plate_id'])#, fn=fnf)
        p=os.path.join(destfolder,fnf)
        totnumheadlines=writecsv_smpfomd(p, qualitycsvfilstr, headerdict=self.qualityfomcsvheaderdict)
        self.multirunfiledict['misc_files'][fnf]=\
            '%s;%s;%d;%d' %('csv_fom_file', ','.join(['sample_no', 'runint', 'plate_id']+self.qualityfoms), totnumheadlines, len(self.fomdlist))

        for histfom in self.histfomnames:   
            fnhist='%s__%s.png' %(anak,histfom)
            p=os.path.join(destfolder,fnhist)        
            savefomhist(p,self.fomdlist, histfom)
            self.multirunfiledict['misc_files'][fnhist]='hist_fom_file;'


    def fomd_rawlend_interlend(self, DRdataarr, refd):
        if DRdataarr.shape[1]!=refd['DRdark'].shape[0]:
            return [('testfom', numpy.nan)], {}, {}
#        print DRdataarr[0][0:5],refd['wl'][0][0:5]
        if not check_wl(numpy.array(numpy.s_[DRdataarr[0],refd['wl_fullrng']])):
            raise ValueError('Wavelength incompatibility between DRdata and ref')
        inter_rawlend=copy.copy(refd)
        inter_selindd={}
        fomd={}
        if self.params['exclinitcols']+self.params['exclfincols']>=DRdataarr.shape[1]:
            raise ValueError('Insufficient signals to remove %d initial signals and %d end signals'\
            %(self.params['exclinitcols'],self.params['exclfincols']))
        else:
            inter_rawlend['DR_av-signal']=DRdataarr[1+self.params['exclinitcols']:DRdataarr.shape[0]-self.params['exclfincols']].mean(axis=0)
            inter_rawlend['DR_fullrng']=(inter_rawlend['DR_av-signal']-refd['DRdark'])/(refd['DRlight']-refd['DRdark'])
            inter_rawlend['abs'+'_fullrng']=(1.-inter_rawlend['DR_fullrng'])**2./(2.*inter_rawlend['DR_fullrng'])
            inds=numpy.where(numpy.logical_and(inter_rawlend['wl_fullrng']>self.params['lower_wl'],inter_rawlend['wl_fullrng']<self.params['upper_wl']))[0]
            for key in ['DR','wl','abs']:            
                keystr =zip(['_unsmth'],['_fullrng'])[0] if key!='wl'else zip([''],['_fullrng'])[0]
                bin_idxs,inter_selindd[key+keystr[0]]=binarray(inter_rawlend[key+keystr[1]][inds],bin_width=self.params['bin_width'])

            inter_selindd['hv']=1239.8/inter_selindd['wl']
            inter_selindd['rawselectinds']=inds[bin_idxs]
            for sigtype in ['DR','abs']:
                inter_selindd[sigtype+'_smth']=handlenan_savgol_filter(inter_selindd[sigtype+'_unsmth'], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=0)

            fomd['min_rescaled'],fomd['max_rescaled'],inter_selindd['DR'+'_smth'+'_refadj']=refadjust(inter_selindd['DR'+'_smth'],\
            self.params['min_mthd_allowed'],self.params['max_mthd_allowed'])
            inter_selindd['abs'+'_smth_refadj']=(1.-inter_selindd['DR'+'_smth_refadj'])**2./(2.*inter_selindd['DR'+'_smth_refadj'])
            inter_selindd['abs_smth_refadj_scl']=inter_selindd['abs_smth_refadj']/numpy.nanmax(inter_selindd['abs_smth_refadj'])
            chkoutput_inds=numpy.where(numpy.logical_and(inter_selindd['wl']>self.params['chkoutput_wlrange'][0],inter_selindd['wl']<self.params['chkoutput_wlrange'][1]))[0]
            fomd['abs_hasnan']=numpy.isnan(inter_selindd['abs_smth_refadj'][chkoutput_inds]).any()
#        ADD ANOTHER PARAMETER FOR CHECK WAVELENGTH WHICH IS MORE CONSERVATIVE THAN THE WAVELENGTH USED FOR CALCULATIONS HERE
            fomd['max_abs']=numpy.nanmax(inter_selindd['abs_smth_refadj'])
            for key in ['abs_'+str(self.params['abs_range'][idx][0])+'_'+str(self.params['abs_range'][idx][1]) for idx in xrange(len(self.params['abs_range']))]:
                inds=numpy.where(numpy.logical_and(inter_selindd['wl']<1239.8/float(key.split('_')[1]),inter_selindd['wl']>1239.8/float(key.split('_')[-1])))[0]
                fomd[key]=numpy.nansum(inter_selindd['abs_smth_refadj'][inds])
            for sig_str,sigkey in zip(['DR'],['DR_smth']):
                fomd['0<'+sig_str+'<1']=check_inrange(inter_selindd[sigkey])
#            WHAT ARE THESE FOMS FOR
            dx=[inter_selindd['hv'][1]-inter_selindd['hv'][0]]
            dx+=[(inter_selindd['hv'][idx+1]-inter_selindd['hv'][idx-1])/2. for idx in xrange(1,len(inter_selindd['rawselectinds'])-1)]
            dx+=[inter_selindd['hv'][-1]-inter_selindd['hv'][-2]]
            dx=numpy.array(dx) 
            inter_selindd['abs_1stderiv']=handlenan_savgol_filter(inter_selindd['abs_smth_refadj_scl'], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=1)/(dx)
            inter_selindd['abs_2ndderiv']=handlenan_savgol_filter(inter_selindd['abs_smth_refadj_scl'], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=2)/(dx**2)
            fomd['max_abs2ndderiv']=numpy.nanmax(inter_selindd['abs_2ndderiv'])
            fomd['min_abs1stderiv']=numpy.nanmin(inter_selindd['abs_1stderiv'])
            for typ in self.params['analysis_types']:
                inter_selindd[typ+'_unscl']=(inter_selindd['abs_smth_refadj']*inter_selindd['hv'])**self.tauc_pow[typ]
                inter_selindd[typ]=inter_selindd[typ+'_unscl']/numpy.max(inter_selindd[typ+'_unscl'])
                fomd[typ+'_minslope']=numpy.min(handlenan_savgol_filter(inter_selindd[typ], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=1)/(dx))
        
        return fomd,inter_rawlend,inter_selindd
        

class Analysis__T_UVVIS(Analysis__TR_UVVIS):
    def __init__(self):
        self.analysis_fcn_version='1'
      #TODO int, float, str or dict types and in dict the options are float, int, str  
        self.dfltparams=dict([('lower_wl',370),('upper_wl',1020),('bin_width',3),('exclinitcols',0),('exclfincols',0),('reffilesmode', 'static'),\
        ('mthd','T'),('abs_range',[(1.5,2.0),(2.0,2.5),(2.5,3.0)]),('max_mthd_allowed', 1.2),('min_mthd_allowed', -0.2),('window_length',45),('polyorder',4), \
        ('ref_run_selection', 'all'),('analysis_types',['DA','IA','DF','IF']),('chkoutput_wlrange',[410,850])])
        
        #TODO: can create a parameter called "ref_run_selection" with default value "all" but could be ,e.g. "run__3,run__6,run__7,run__8,run__9"  \
#        and then if T dark, T light, R dark are runs 3,6,7 respectively then only these runs will be used (if run__2 is also T dark, it will be ignored). 
#        if run__8 and 9 are both R light, the min/max/etc function will be applied to the ensemble of refs in these runs
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__T_UVVIS'
        #TODO: make intermediate column headings unique from raw
        self.requiredkeys=['Wavelength (nm)','Signal_0']
        self.optionalkeys=['Signal_'+str(x) for x in numpy.arange(1,11)]
        self.requiredparams=[]
        self.fom_chkqualitynames=['abs_hasnan']
        self.qualityfoms=['min_rescaled','max_rescaled','0<T<=1']
        self.histfomnames=['max_abs2ndderiv','min_abs1stderiv']
        self.processnewparams()
        #TODO: update plotting defaults on both classes
        self.plotparams=dict({}, plot__1={'x_axis':'hv'})
        self.plotparams['plot__1']['x_axis']='hv'#this is a single key from raw or inter data
        self.plotparams['plot__1']['series__1']='abs_smth_refadj_scl'
#        ,t_smth'#list of keys
#        self.plotparams['plot__1']['series__2']=','.join([fom for fom in self.fomnames if 'abs_' not in fom])
        #in 'plot__1' can have max_value__1,min_value__1,max_value__2,min_value__2
        #self.plotparams['plot__1']['series__2'] for right hand axis

        # also colormap_min_value,colormap_max_value
        

        self.tauc_pow=dict([('DA',2),('IA',0.5),('DF',2./3.),('IF',1./3.)])

#        should this be made self.multirunfomnames

    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
        self.num_files_considered, self.filedlist, self.refdict__filedlist=\
              Tgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys, optionalkeys=self.optionalkeys, ref_run_selection=self.params['ref_run_selection'])
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filedlist

    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):
        self.initfiledicts(runfilekeys=['inter_rawlen_files','inter_files'])
        self.multirunfiledict['misc_files']={}
        self.fomdlist=[]
        refkeymap=[(('ref_dark', 'T_UVVIS'), 'Tdark'), (('ref_light', 'T_UVVIS'), 'Tlight')]
        
        
        
        static_ref_fnd=dict([('Tdark',lambda x:numpy.min(x,axis=0)),('Tlight',lambda x:numpy.max(x,axis=0))])

   
        for filed in [fd for rktup,rk in refkeymap for fd in self.refdict__filedlist[rktup]]:
            #'keyinds is ordered the same as required_keys and then optinoal_keys, but not anymore for ref data
            filed['keyinds']=[0]+filed['keyinds'][1+self.params['exclinitcols']:len(filed['keyinds'])-self.params['exclfincols']]#update the keyinds to keep zero index, which is the wl, and then select other columns
            if len(filed['keyinds'])==1:#only wavelength left so need to abort analysis
                if self.debugmode:
                    raise ValueError('select ref columns resulted in no remaining Signals')
                self.writefom(destfolder, anak, anauserfomd=anauserfomd, createdummyfomdlist=True)
                return
        
        closeziplist=self.prepare_filedlist(\
            [filed for filed in self.filedlist]+\
            [fd for rktup,rk in refkeymap for fd in self.refdict__filedlist[rktup]], \
                expfiledict, expdatfolder=expdatfolder, expfolderzipclass=zipclass, fnk='fn')#combine the filed, Rfiled, etc. together in 1 list so that any runzips are only opened once
        
        referror, refd_fn=self.setuprefdata(refkeymap,  static_ref_fnd, anak=anak, destfolder=destfolder)
        if referror:
            self.writefom(destfolder, anak, anauserfomd=anauserfomd, createdummyfomdlist=True)
            for zc in closeziplist:
                zc.close()
            return
        
        for filed in self.filedlist:
            fn=filed['fn']
            Tdataarr=filed['readfcn'](*filed['readfcn_args'], **filed['readfcn_kwargs'])[:,::-1]
#            print numpy.shape(DRdataar)
            fomdict,rawlend,interlend=self.fomd_rawlend_interlend(Tdataarr, refd_fn(filed['sample_no']))
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

            if 'rawselectinds' in interlend.keys():
                fni='%s__%s_interlen.txt' %(anak, os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fni)
                kl=saveinterdata(p, interlend, savetxt=True)
                self.runfiledict[filed['run']]['inter_files'][fni]='%s;%s;%d;%d;%d' %('uvis_inter_interlen_file', ','.join(kl), 1, len(interlend[kl[0]]), filed['sample_no'])
        
        self.writefom(destfolder, anak, anauserfomd=anauserfomd)
        for zc in closeziplist:
            zc.close()

        if destfolder is None:#dont' do anything with quality items if output not being saved
            return
        
        fnf='%s__%s.csv' %(anak,'qualityfoms')
        #TODO: if quality foms are integers, append them to the intfomkeys and pass [] as 2nd argument
        qualitycsvfilstr=createcsvfilstr(self.fomdlist, self.qualityfoms, intfomkeys=['runint','plate_id'])#, fn=fnf)
        p=os.path.join(destfolder,fnf)
        totnumheadlines=writecsv_smpfomd(p, qualitycsvfilstr, headerdict=self.qualityfomcsvheaderdict)
        self.multirunfiledict['misc_files'][fnf]=\
            '%s;%s;%d;%d' %('csv_fom_file', ','.join(['sample_no', 'runint', 'plate_id']+self.qualityfoms), totnumheadlines, len(self.fomdlist))

        for histfom in self.histfomnames:   
            fnhist='%s__%s.png' %(anak,histfom)
            p=os.path.join(destfolder,fnhist)        
            savefomhist(p,self.fomdlist, histfom)
            self.multirunfiledict['misc_files'][fnhist]='hist_fom_file;'
        


    def fomd_rawlend_interlend(self, Tdataarr, refd):
        if Tdataarr.shape[1]!=refd['Tdark'].shape[0]:
            return [('testfom', numpy.nan)], {}, {}
#        print DRdataarr[0][0:5],refd['wl'][0][0:5]
        if not check_wl(numpy.array(numpy.s_[Tdataarr[0],refd['wl_fullrng']])):
            raise ValueError('Wavelength incompatibility between Tdata and ref')
        inter_rawlend=copy.copy(refd)
#        print numpy.shape(inter_rawlend['wavelength'])
        inter_selindd={}
        fomd={}
        if self.params['exclinitcols']+self.params['exclfincols']>=Tdataarr.shape[1]:
            raise ValueError('Insufficient signals to remove %d initial signals and %d end signals'\
            %(self.params['exclinitcols'],self.params['exclfincols']))
        else:
            inter_rawlend['T_av-signal']=Tdataarr[1+self.params['exclinitcols']:Tdataarr.shape[0]-self.params['exclfincols']].mean(axis=0)
            inter_rawlend['T_fullrng']=(inter_rawlend['T_av-signal']-refd['Tdark'])/(refd['Tlight']-refd['Tdark'])
            inter_rawlend['abs'+'_fullrng']=-numpy.log(inter_rawlend['T_fullrng'])
            inds=numpy.where(numpy.logical_and(inter_rawlend['wl_fullrng']>self.params['lower_wl'],inter_rawlend['wl_fullrng']<self.params['upper_wl']))[0]
            for key in ['T','abs','wl']:            
                keystr =zip(['_unsmth'],['_fullrng'])[0] if key!='wl'else zip([''],['_fullrng'])[0]
                bin_idxs,inter_selindd[key+keystr[0]]=binarray(inter_rawlend[key+keystr[1]][inds],bin_width=self.params['bin_width'])
        
#            print numpy.shape(inter_selindd['wl'])
            inter_selindd['hv']=1239.8/inter_selindd['wl']
            inter_selindd['rawselectinds']=inds[bin_idxs]
            for sigtype in ['T','abs']:
                inter_selindd[sigtype+'_smth']=handlenan_savgol_filter(inter_selindd[sigtype+'_unsmth'], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=0)


            fomd['min_rescaled'],fomd['max_rescaled'],inter_selindd['abs'+'_smth'+'_refadj']=refadjust(inter_selindd['abs'+'_smth'],\
            self.params['min_mthd_allowed'],self.params['max_mthd_allowed'])
            inter_selindd['abs_smth_refadj_scl']=inter_selindd['abs_smth_refadj']/numpy.nanmax(inter_selindd['abs_smth_refadj'])
            chkoutput_inds=numpy.where(numpy.logical_and(inter_selindd['wl']>self.params['chkoutput_wlrange'][0],inter_selindd['wl']<self.params['chkoutput_wlrange'][1]))[0]
            fomd['abs_hasnan']=numpy.isnan(inter_selindd['abs_smth_refadj'][chkoutput_inds]).any()
#        ADD ANOTHER PARAMETER FOR CHECK WAVELENGTH WHICH IS MORE CONSERVATIVE THAN THE WAVELENGTH USED FOR CALCULATIONS HERE
            fomd['max_abs']=numpy.nanmax(inter_selindd['abs_smth_refadj'])
            for key in ['abs_'+str(self.params['abs_range'][idx][0])+'_'+str(self.params['abs_range'][idx][1]) for idx in xrange(len(self.params['abs_range']))]:
                inds=numpy.where(numpy.logical_and(inter_selindd['wl']<1239.8/float(key.split('_')[1]),inter_selindd['wl']>1239.8/float(key.split('_')[-1])))[0]
                fomd[key]=numpy.nansum(inter_selindd['abs_smth_refadj'][inds])
            for sig_str,sigkey in zip(['T'],['T_smth']):
                fomd['0<'+sig_str+'<1']=check_inrange(inter_selindd[sigkey])
                         
            dx=[inter_selindd['hv'][1]-inter_selindd['hv'][0]]
            dx+=[(inter_selindd['hv'][idx+1]-inter_selindd['hv'][idx-1])/2. for idx in xrange(1,len(inter_selindd['rawselectinds'])-1)]
            dx+=[inter_selindd['hv'][-1]-inter_selindd['hv'][-2]]
            dx=numpy.array(dx) 
            inter_selindd['abs_1stderiv']=handlenan_savgol_filter(inter_selindd['abs_smth_refadj_scl'], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=1)/(dx)
            inter_selindd['abs_2ndderiv']=handlenan_savgol_filter(inter_selindd['abs_smth_refadj_scl'], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=2)/(dx**2)
            fomd['max_abs2ndderiv']=numpy.nanmax(inter_selindd['abs_2ndderiv'])
            fomd['min_abs1stderiv']=numpy.nanmin(inter_selindd['abs_1stderiv'])
            for typ in self.params['analysis_types']:
                inter_selindd[typ+'_unscl']=(inter_selindd['abs_smth_refadj']*inter_selindd['hv'])**self.tauc_pow[typ]
                inter_selindd[typ]=inter_selindd[typ+'_unscl']/numpy.max(inter_selindd[typ+'_unscl'])
                fomd[typ+'_minslope']=numpy.min(handlenan_savgol_filter(inter_selindd[typ], self.params['window_length'], self.params['polyorder'], delta=1.0, deriv=1)/(dx))
        

        
        return fomd,inter_rawlend,inter_selindd
#    
class Analysis__BG(Analysis_Master_inter):
    def __init__(self):
        self.analysis_name='Analysis__BG'
        self.analysis_fcn_version='1'
        self.dfltparams=dict([('num_knots',8),('lower_wl',390),('upper_wl',940),\
            ('tol',1e-06),('maxtol',1e-03),('min_allowedslope',-2),('min_bgTP_diff',0.1),('min_bkgrdslope',-0.05),\
            ('min_bgbkgrdslopediff',0.2),('min_finseglength',0.1),('merge_bgslopediff_percent',0),\
            ('merge_linsegslopediff_percent',0),('min_TP_finseg_diff',0.2),('min_bgfinalseglength',0.2),\
            ('max_merge_differentialTP',0.02),('min_knotdist',0.05),\
            ('abs_minallowedslope',-10),('max_absolute_2ndderiv',350000),('analysis_types','DA,IA'),\
            ('maxbgspersmp',4),('chkoutput_types','DA,IA')])
#        try:
#            print self.csvheaderdict.keys()
#        except:
#            pass
        self.params=copy.copy(self.dfltparams)
        self.processnewparams()
        self.requiredkeys=[]#required keys aren't needed for selecting applicable files because the requiremenets for inter_files will be sufficient. Only put requireded_keys that are need in the analysis and these required_keys are of the raw data not inter_data
        self.optionalkeys=[]
        self.requiredparams=[]

        
        
        
    def getgeneraltype(self):#make this fucntion so it is inhereted
        return 'analysis_of_ana'

    def rtn_defaults(self):
        self.params=copy.copy(self.dfltparams)
        idialog=messageDialog(self, 'You enetered invalid parameters. They are being restored to defaults. Please try again.')
        idialog.exec_()
        
    def processnewparams(self):
        if not isinstance(self.params['analysis_types'],list):
            try:
                self.params['analysis_types']=self.params['analysis_types'].split(',')
            except:
                self.rtn_defaults
        
        if not isinstance(self.params['chkoutput_types'],list):
            try:
                self.params['chkoutput_types']=self.params['chkoutput_types'].split(',')          
            except:
                self.rtn_defaults

        if numpy.array([str(x).strip()=='' for x in self.params.values()]).any() or set(self.params['chkoutput_types'])>set(self.params['analysis_types']):
            self.rtn_defaults
      
        self.fomnames=[item for sublist in [[x+'_abs_expl_'+y,x+'_bg_'+y,x+'_bgcode_'+y,x+'_bg_repr',x+'_bgcode_repr',x+'_bgslope_repr',x+'_bkgrdslope_repr',x+'_code'+'0'+'_only']\
                             for x in self.params['analysis_types'] for y in [str(idx) for idx in xrange(self.params['maxbgspersmp'])]]\
                             for item in sublist]
                                 
        self.fom_chkqualitynames=[bgtyp+'_bg_0' for bgtyp in self.params['chkoutput_types']]
        self.histfomnames=[bgtyp+'_fit_minslope' for bgtyp in self.params['analysis_types']]
        
        self.plotparams=dict({}, plot__1={'x_axis':'hv'})
        self.plotparams['plot__1']['x_axis']='hv'#this is a single key from raw or inter data
        self.plotparams['plot__1']['series__1']=self.params['analysis_types'][0]
        self.csvheaderdict={'csv_version':'1','plot_parameters':{}}
        np_ana=5
        for idx in xrange(len(self.params['analysis_types'])):
            self.csvheaderdict['plot_parameters']['plot__'+str(np_ana*idx+1)]=dict({}, fom_name=self.params['analysis_types'][idx]+'_'+'bg_0',\
            colormap='jet_r', colormap_over_color='(0.5,0.5,0.5)', colormap_under_color='(0.,0.,0.)')
            self.csvheaderdict['plot_parameters']['plot__'+str(np_ana*idx+2)]=dict({}, fom_name=self.params['analysis_types'][idx]+'_'+'bg_repr',\
            colormap='jet_r', colormap_over_color='(0.5,0.5,0.5)', colormap_under_color='(0.,0.,0.)')
            self.csvheaderdict['plot_parameters']['plot__'+str(np_ana*idx+3)]=dict({}, fom_name=self.params['analysis_types'][idx]+'_'+'bgcode_repr',\
            colormap='jet_r', colormap_over_color='(0.5,0.5,0.5)', colormap_under_color='(0.,0.,0.)')
            self.csvheaderdict['plot_parameters']['plot__'+str(np_ana*idx+4)]=dict({}, fom_name=self.params['analysis_types'][idx]+'_'+'bgslope_repr',\
            colormap='jet_r', colormap_over_color='(0.5,0.5,0.5)', colormap_under_color='(0.,0.,0.)')
            self.csvheaderdict['plot_parameters']['plot__'+str(np_ana*idx+5)]=dict({}, fom_name=self.params['analysis_types'][idx]+'_'+'bkgrdslope_repr',\
            colormap='jet_r', colormap_over_color='(0.5,0.5,0.5)', colormap_under_color='(0.,0.,0.)')

    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
        self.num_files_considered, self.filedlist=\
              BGgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys,\
              optionalkeys=self.optionalkeys,anadict=anadict)
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filedlist


    def check_input(self, critfracapplicable=0.9):
        fracapplicable=1.*len(self.filedlist)/self.num_files_considered
        return fracapplicable>critfracapplicable, \
        '%d files, %.2f fraction of those available, do not meet requirements' %(len(self.filedlist)-self.num_files_considered, 1.-fracapplicable)

    def check_output(self, critfracnan=0.5):
        tfracnan=0;tfracnan_abs=0;ostrl=[]
        numnan_abs,fracnan_abs=stdcheckoutput(self.fomdlist, ['abs_hasnan_bg'])
        tfracnan_abs+=fracnan_abs
        for nm in self.fom_chkqualitynames:
            numnan, fracnan=stdcheckoutput(self.fomdlist, [nm])            
            tfracnan+=fracnan
            ostrl.append('%d samples, %.2f fraction of total samples with no NaN in absorption have no %s band gaps; ' %(numnan, fracnan,nm))
        tfracnan/=len(self.fom_chkqualitynames)            
        ostr=';'.join(ostrl)
        return tfracnan/tfracnan_abs>critfracnan, ostr
        
    def savelinfitd(self,p):
        maxknots={};maxbgs={};reqkeys=[]
        rdlmtr='\r\n'
        cdlmtr=','
        for typ in self.params['analysis_types']:            
            maxknots[typ]=numpy.max(numpy.array([int(k.split('_')[-1]) for linfitd in self.linfitdlist for k,v in linfitd.items() if typ+'_'+'knots' in k]))+1
            maxbgs[typ]=numpy.max(numpy.array([int(k.split('_')[-1] )for linfitd in self.linfitdlist for k,v in linfitd.items() if typ+'_'+'bgknots_lower' in k]))+1
            reqkeys+=[typ+'_'+'knots_'+str(x) for x in xrange(maxknots[typ])]
            reqkeys+=[typ+'_'+'slopes_'+str(x) for x in xrange(maxknots[typ]-1)]
            reqkeys+=[typ+'_'+'bgknots_lower_'+str(x) for x in xrange(maxbgs[typ])]
            reqkeys+=[typ+'_'+'bkgrdknots_lower_'+str(x) for x in xrange(maxbgs[typ])]
        wstr=''        
        for idx,linfitd in enumerate(self.linfitdlist):
            linfitd=dict(linfitd.items()+[(rk,numpy.NaN) for rk in reqkeys if rk not in linfitd.keys()])
            if idx==0:
                wstr+=cdlmtr.join(['sample_no']+[k for k in sorted(linfitd.keys()) if k!='sample_no'])+rdlmtr
            wstr+=str(linfitd['sample_no'])+cdlmtr
            wstr+=cdlmtr.join([str(numpy.round(linfitd[k],decimals=4)) for k in sorted(linfitd.keys()) if k!='sample_no'])
            wstr+=rdlmtr
        wstr.rstrip(rdlmtr)
        wstr=wstr.replace('nan','NaN')
        with open(p,'w') as ps:
            ps.write(wstr)

    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):
        
        self.initfiledicts(runfilekeys=['inter_rawlen_files','inter_files', 'misc_files'])
        self.multirunfiledict['misc_files']={}
        self.fomdlist=[]     
        self.linfitdlist=[]
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
                linfitd=dict(linfitd,sample_no=filed['sample_no'])
                self.linfitdlist+=[linfitd]
                
            if destfolder is None:
                continue
            
            self.writefom(destfolder, anak, anauserfomd=anauserfomd)
   
            if 'rawselectinds' in selindd.keys():
                fni='%s__%s_interlen.txt' %(anak, os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fni)
                kl=saveinterdata(p, selindd, savetxt=True)
                self.runfiledict[filed['run']]['inter_files'][fni]='%s;%s;%d;%d;%d' %('uvis_inter_interlen_file', ','.join(kl), 1, len(selindd[kl[0]]), filed['sample_no'])

        if destfolder is None:
            return
       
        if len(self.linfitdlist)>0:
#                print linfitd.keys()
            fn_linfit='%s__%s' %(anak,'linfitparams.csv')
            self.multirunfiledict['misc_files'][fn_linfit]='csv_linfitparams'+'_file;'
            p=os.path.join(destfolder,fn_linfit)
            self.savelinfitd(p)
            
        for histfom in self.histfomnames:   
            fnhist='%s__%s.png' %(anak,histfom)
            p=os.path.join(destfolder,fnhist)        
            savefomhist(p,self.fomdlist, histfom)
            self.multirunfiledict['misc_files'][fnhist]='hist_fom_file;'
        
    def fomd_rawlend_interlend(self, rawlend):
        inter_selindd={}
        abs2bg_inds=numpy.where(numpy.logical_and(rawlend['hv']<1239.8/self.params['lower_wl'],rawlend['hv']>1239.8/self.params['upper_wl']))[0]
#        print inter_selindd['rawselectinds']
        
        for key in rawlend.keys():
                inter_selindd[key]=rawlend[key][abs2bg_inds]
        
        for typ in ['DA','IA','DF','IF']:
            if typ in inter_selindd.keys():
                inter_selindd[typ]=inter_selindd[typ]/(numpy.nanmax(inter_selindd[typ]))
            
#        print inter_selindd.keys()
        inter_linfitd,fomd=runuvvis(inter_selindd,self.params)                
#        bgexists_fcn=lambda x: 1 if x+'_bg_0' in fomd.keys() and not numpy.isnan(fomd[x+'_bg_0']) else 0
        minslope_fcn=lambda x: numpy.nanmin(x) if x!=[] else numpy.NaN
        for typ in self.params['analysis_types']:
#            fomd[typ+'_bg_exists']=bgexists_fcn(typ)
            temparr=[v for k,v in inter_linfitd.items() if typ+'_slopes' in k]
            fomd[typ+'_fit_minslope']=minslope_fcn(temparr)
        for k in self.fomnames:
            if k not in fomd.keys():
                fomd[k]=numpy.NaN
        for key in inter_selindd.keys():
            if key in rawlend.keys() and 'rawselectinds' not in key:
                inter_selindd[key+'_bg']=inter_selindd.pop(key)
        fomd['abs_hasnan_bg']=numpy.isnan(rawlend['abs_smth_refadj_scl']).any()
        return fomd,inter_linfitd,inter_selindd

