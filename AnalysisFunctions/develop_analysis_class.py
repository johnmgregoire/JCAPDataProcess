import numpy, copy
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.split(os.getcwd())[0])

from fcns_math import *
from fcns_io import *
from csvfilewriter import createcsvfilstr
from Analysis_Master import *
    
def TRgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=None, requiredkeys=[], optionalkeys=[]):
    if techk!='T_UVVIS':
        return [], [], 0
    
    #get all refs
    refdict__fn_nkeys_keyinds=dict([(('ref_dark', 'T_UVVIS'), []), (('ref_light', 'T_UVVIS'), []), (('ref_dark', 'R_UVVIS'), []), (('ref_light', 'R_UVVIS'), [])])
    for k in refdict__fn_nkeys_keyinds.keys():
        uk, tk=k
#?   runklist,nkeys and keyinds,ntemp,temp,typek
        ntemp, temp, REFfn_nkeys_keyinds=stdgetapplicablefilenames(expfiledict, uk, tk, typek, runklist=None, requiredkeys=requiredkeys, optionalkeys=optionalkeys)
        if len(REFfn_nkeys_keyinds)==0:
            return [], [], 0
        refdict__fn_nkeys_keyinds[k]=REFfn_nkeys_keyinds
    num_files_considered, temp, Tfn_nkeys_keyinds=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=requiredkeys, optionalkeys=optionalkeys)
    ntemp, Rfilenames, Rfn_nkeys_keyinds=stdgetapplicablefilenames(expfiledict, usek, 'R_UVVIS', typek, runklist=runklist, requiredkeys=requiredkeys, optionalkeys=optionalkeys)
    Rsmp=[fn.partition('_')[0] for fn in Rfilenames]
    Tfn_Tnkeys_Tkeyinds_Rfn_Rnkeys_Rkeyinds=[(Tfn, nkeys, keyinds)+Rfn_nkeys_keyinds[Rsmp.index(Tfn.partition('_')[0])] for Tfn, nkeys, keyinds in Tfn_nkeys_keyinds if Tfn.partition('_')[0] in Rsmp]
    filenames=[tup[0] for tup in Tfn_Tnkeys_Tkeyinds_Rfn_Rnkeys_Rkeyinds]
    return num_files_considered, filenames, Tfn_Tnkeys_Tkeyinds_Rfn_Rnkeys_Rkeyinds, refdict__fn_nkeys_keyinds

def stdcheckoutput(fomdlist, fomnames):
#?fomdlist
    nancount=[(not k in fomdlist) or numpy.isnan(d[k]) for d in fomdlist for k in fomnames].count(True)
    return nancount, 1.*nancount/(len(fomdlist)*len(fomnames))

class Analysis__TR_UVVIS(Analysis_Master_inter):
    self.analysis_version='2.1'    
    self.dfltparams=dict([('lower_wavelength',385),('upper_wavelength',1050),('bin_width',3),('max_num_knots',8),\
        ('tol',1e-06),('maxtol',1e-03),('min_allowedslope',-2),('min_bgTP_diff',0.2),('min_bkgrdslope',-0.05),\
        ('min_bgbkgrdslopediff',0.2),('min_finseglength',0.1),('merge_bgslopediff_percent',10),\
        ('merge_linsegslopediff_percent',10),('min_TP_finseg_diff',0.2),('min_bgfinalseglength',0.2),\
        ('max_merge_differentialTP',0.02),('min_knotdist',0.05),('min_diff',0.1),('min_numpeaks',1),\
        ('exclinitcols',0),('exclfincols',0),('mthd','TR'),('reffilesmode', 'static'),('max_mthd_allowed', 1.2),\
        ('min_mthd_allowed', -0.2),('analtypes','DA,IA'),('redo', True),\
        ('delta_1stderiv',-1),('max_absolute_2ndderiv',0),('window_length',9),('polyorder',4)])
    
    self.params={}
    for typ in self.dfltparams['analtypes']:
        self.params[typ]=copy.copy(self.dfltparams)
        
    self.analysis_name='Analysis__TR_UVVIS'
    self.requiredkeys=['Wavelength (nm)','Signal_0']
    self.optionalkeys=['Signal_'+str(x) for x in numpy.arange(1,11)]
    self.fomnames=[item for sublist in [[x+'-abs_expl_'+y,x+'-bg_'+y,x+'-bgcode_'+y,x+'-bg_repr',x+'-code'+y+'-only']\
                         for x in ['DA','IA','DF','IF'] for y in [str(idx) for idx in xrange(4)] if self.params[x]]\
                         for item in sublist]+['abs_'+str(self.params['abs_range'][2*idx])+'-'+str(self.params['abs_range'][2*idx+1]) \
                         for idx in xrange(len(self.params['abs_range'])/2.)]+['abs_max2ndderiv','maxabsorp']\
                             
    self.fom_chkqualitynames=['maxabsorp',]
    self.quality_foms=['abs_max2ndderiv','minslope',self.params['mthd']+'-min_rescaled',self.params['mthd']+'-max_rescaled','0<T<1','0<R<1','1-T-R>0']
    
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None):
        self.num_files_considered, self.filenames, self.Tfn_Tnkeys_Tkeyinds_Rfn_Rnkeys_Rkeyinds, self.refdict__fn_nkeys_keyinds=\
              Tgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys, optionalkeys=self.optionalkeys)
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filenames

    def check_input(self, critfracapplicable=0.9):
        fracapplicable=1.*len(self.filenames)/len(self.fn_nkeys_keyinds)
        return fracapplicable>critfracapplicable, \
        '%d files, %.2f of those available, do not meet requirements' %(len(self.fn_nkeys_keyinds)-len(self.filenames), 1.-fracapplicable)

    def check_output(self, critfracnan=0.9):
        numnan, fracnan=stdcheckoutput(self.fomdlist, self.fom_chkqualitynames)
        return fracnan>critfracnan, \
        '%d samples, %.2f fraction of total samples have NaN in the absorption spectra' %(numnan, fracnan)
    

    def check_wl(self,wl_array,axis=0):
        if axis:
            wl_array=wl_array.T
        return len(numpy.where(numpy.array([numpy.abs(wl_array[i][k]-wl_array[j][k]) for i in xrange(wl_array.shape[0]) \
        for j in xrange(0,i) for k in [0,-1]])>0.01)[0])==0

        
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak=''):
        self.fomfiledict={}
        self.interfiledict={}
        self.fomdlist=[]
        refkeymap=[(('ref_dark', 'T_UVVIS'), 'Tdark'), (('ref_light', 'T_UVVIS'), 'Tlight'), (('ref_dark', 'R_UVVIS'), 'Rdark'), (('ref_light', 'R_UVVIS'), 'Rlight')]
        refd={}#refd will be a dictionary with 4 keys that makes a good started for the intermediate dictionary with raw-data-length arrays
        try:
            refd['wl']=numpy.float32([\
            (readbinary_selinds(os.path.join(expdatfolder, fn+'.dat'), nkeys, keyinds=keyinds)[0]) \
            for rktup,rk in refkeymap for fn, nkeys, keyinds in self.refdict__fn_nkeys_keyinds[rktup]])
        except:
            raise ValueError('Number of data points in reference files do not match')
            
        if not check_wl(refd['wl']):
            raise ValueError('Incompatible wavelengths in reference files')
        
        if self.params['reffilesmode']=='static':
            ref_fnd=dict([('Tdark',lambda x:numpy.min(x,axis=0)),('Tlight',lambda x:numpy.max(x,axis=0))\
            ('Rdark',lambda x:numpy.min(x,axis=0)),('Rlight',lambda x:numpy.max(x,axis=0))])
            for rktup, rk in refkeymap:
                refd[rk]=ref_fnd(numpy.float32([\
                    (readbinary_selinds(os.path.join(expdatfolder, fn+'.dat'), nkeys, keyinds=keyinds)[1:]).mean(axis=0) \
                    for fn, nkeys, keyinds in self.refdict__fn_nkeys_keyinds[rktup]]))
            refd_Tfn=lambda Tfn:refd
            #this trivial function costs no time and for nontrivial on-the-fly ref calculations, define a fcn with the same name
        else:#no other ref calculations supported at this time
            return
        
        for Tfn, Tnkeys, Tkeyinds, Rfn, Rnkeys, Rkeyinds in self.Tfn_Tnkeys_Tkeyinds_Rfn_Rnkeys_Rkeyinds:
            Tdataarr=readbinary_selinds(os.path.join(expdatfolder, Tfn+'.dat'), Tnkeys, keyinds=Tkeyinds)
            Rdataarr=readbinary_selinds(os.path.join(expdatfolder, Rfn+'.dat'), Rnkeys, keyinds=Rkeyinds)
            fomtuplist, rawlend, interlend=self.fomtuplist_rawlend_interlend(Tdataarr, Rdataarr, refd_Tfn(Tfn))
            self.fomdlist+=[dict([('sample_no', getsamplenum_fn(Tfn))]+fomtuplist)]
            if len(rawlend.keys())>0:
                fnr='%s__%s_rawlen.dat' %(anak,Tfn[:-4])
                p=os.path.join(destfolder,fnr)
                kl=saveinterdata(p, rawlend)
                self.interfiledict[fnr]='%s;%s' %('eche_inter_rawlen_file', ','.join(kl))
            if 'rawselectinds' in interlend.keys():
#? What the hell is Tfn[:-4]
                fni='%s__%s_interlen.dat' %(anak,Tfn[:-4])
                p=os.path.join(destfolder,fni)
                kl=saveinterdata(p, interlend)
                self.interfiledict[fni]='%s;%s' %('eche_inter_interlen_file', ','.join(kl))
        for foml in [self.fomnames,self.quality_foms]:
            fnf='%s__%s.csv' %(anak,'-'.join(self.fomnames))
            p=os.path.join(destfolder,fnf)
            self.csvfilstr=createcsvfilstr(self.fomdlist, foml)
            writecsv_smpfomd(p, self.csvfilstr)
            
        self.fomfiledict[fnf]='csv_fom_file;'+','.join(['sample_no']+self.fomnames)
        

    def fomtuplist_rawlend_interlend(self, Tdataarr, Rdataarr, refd):
        if Tdataarr.shape[1]!=Rdataarr.shape[1] or Tdataarr.shape[1]!=refd['Tdark'].shape[0]:
            return [('testfom', numpy.nan)], {}, {}
        if not check_wl(np.array(Tdataarr[0],Rdataarr[0],refd['wl'])):
            raise ValueError('Wavelength incompatibility between Tdata, Rdata and ref')
        inter_rawlend=copy.copy(refd)
        if self.params['exclinitcols']-(Tdataarr.shape[1]-self.params['exclfincols'])<=0:
            raise ValueError('Insufficient signals to remove %d init signals and %d end signals'\
            %(self.params['exclinitcols'],self.params['exclfincols']))
        else:
            inter_rawlend['trans_signal']=Tdataarr[1+self.params['exclinitcols']:Tdataarr.shape[1]-self.params['exclfincols']].mean(axis=0)
            inter_rawlend['refl_signal']=Rdataarr[1+self.params['exclinitcols']:Tdataarr.shape[1]-self.params['exclfincols']].mean(axis=0)
            inter_rawlend['trans']=(interd_rawlen['trans_signal']-refd['Tdark'])/(refd['Tlight']-refd['Tdark'])
            inter_rawlend['refl']=(interd_rawlen['refl_signal']-refd['Rdark'])/(refd['Rlight']-refd['Rdark'])
        fomtuplist,rawlend,interlend=runuvvis(inter_rawlend,self.params)

        return fomtuplist, rawlend, interlend
        
        
        
        
        
        
#class Analysis_T_UVVIS():
#    def __init__(self):
#        self.analysis_version='2.1'
#        self.dfltparams=dict([('use_ave_ref', True)])
#        self.params=copy.copy(self.dfltparams)
#        self.analysis_name='Analysis_T_UVVIS'
#        self.requiredkeys=['Wavelength (nm)', 'Signal_0']
#        self.optionalkeys=['Signal_'+str(x) for x in numpy.arange(1,11)]
#        self.fomnames=['testfom']
#        self.fomqualitynames=[]
#    #this gets the applicable filenames and there may be other required filenames for analysis which can be saved locally and use in self.perform
#    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None):
#        self.num_files_considered, self.filenames, self.Tfn_Tnkeys_Tkeyinds_Rfn_Rnkeys_Rkeyinds, self.refdict__fn_nkeys_keyinds=\
#              Tgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys, optionalkeys=self.optionalkeys)
#        self.description='%s on %s' %(','.join(self.fomnames), techk)
#        return self.filenames
#    
#    def check_input(self, critfracapplicable=0.9):
#        fracapplicable=1.*len(self.filenames)/len(self.fn_nkeys_keyinds)
#        return fracapplicable>critfracapplicable, \
#        '%d files, %.2f of those available, do not meet requirements' %(len(self.fn_nkeys_keyinds)-len(self.filenames), 1.-fracapplicable)
#    def check_output(self, critfracnan=0.9):
#        numnan, fracnan=stdcheckoutput(self.fomdlist, self.fomqualitynames)
#        return fracnan>critfracnan, \
#        '%d FOMs, %.2f of attempted calculations, are NaN' %(numnan, fracnan)

        
c=Analysis__TR_UVVIS()
p_exp='//htejcap.caltech.edu/share/home/users/hte/demo_proto/experiment/4/eche.pck'
p_ana='//htejcap.caltech.edu/share/home/users/hte/demo_proto/analysis/uvistemp'
expd=readexpasdict(p_exp)
usek='data'
techk='T_UVVIS'
typek='spectrum_files'
filenames=c.getapplicablefilenames(expd, usek, techk, typek, runklist=None)
c.perform(p_ana, expdatfolder=os.path.split(p_exp)[0], writeinterdat=True, anak='ana__0')
print 'THESE FOM FILES WRITTEN'
for k, v in c.fomfiledict.items():
    print k, v
print 'THESE INTERMEDIATE DATA FILES WRITTEN'
for k, v in c.interfiledict.items():
    print k, v
print 'THESE FOMs CALCULATED'
print c.fomdlist

for k, v in c.interfiledict.items():
    if '_996_' in k and 'wl' in v:
        break
keys=v.partition(';')[2].split(',')
xi=keys.index('wl')
yi=keys.index('Tover1minusR')
x, y=readbinary_selinds(os.path.join(p_ana, k), len(keys), keyinds=[xi, yi])
import pylab
pylab.plot(x, y)
pylab.show()
