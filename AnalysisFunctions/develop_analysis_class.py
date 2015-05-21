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
    nancount=[(not k in fomdlist) or numpy.isnan(d[k]) for d in fomdlist for k in fomnames].count(True)
    return nancount, 1.*nancount/(len(fomdlist)*len(fomnames))

class Analysis_T_UVVIS():
    def __init__(self):
        self.analysis_version='1'
        self.dfltparams=dict([('use_ave_ref', True)])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis_T_UVVIS'
        self.requiredkeys=['Wavelength (nm)', 'Signal_0']
        self.optionalkeys=['Signal_1']
        self.fomnames=['testfom']
        
    #this gets the applicable filenames and there may be other required filenames for analysis which can be saved locally and use in self.perform
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None):
        self.num_files_considered, self.filenames, self.Tfn_Tnkeys_Tkeyinds_Rfn_Rnkeys_Rkeyinds, self.refdict__fn_nkeys_keyinds=\
              TRgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys, optionalkeys=self.optionalkeys)
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filenames
    
    def check_input(self, critfracapplicable=0.9):
        fracapplicable=1.*len(self.filenames)/len(self.fn_nkeys_keyinds)
        return fracapplicable>critfracapplicable, \
        '%d files, %.2f of those available, do not meet requirements' %(len(self.fn_nkeys_keyinds)-len(self.filenames), 1.-fracapplicable)
    def check_output(self, critfracnan=0.9):
        numnan, fracnan=stdcheckoutput(self.fomdlist, self.fomnames)
        return fracnan>critfracnan, \
        '%d FOMs, %.2f of attempted calculations, are NaN' %(numnan, fracnan)
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak=''):
        self.fomfiledict={}
        self.interfiledict={}
        self.fomdlist=[]
        refkeymap=[(('ref_dark', 'T_UVVIS'), 'Tdark'), (('ref_light', 'T_UVVIS'), 'Tlight'), (('ref_dark', 'R_UVVIS'), 'Rdark'), (('ref_light', 'R_UVVIS'), 'Rlight')]
        refd={}#refd will be a dictionary with 4 keys that makes a a good started for the intermediate dictionary with raw-data-length arrays
        if self.params['use_ave_ref']:
            for rktup, rk in refkeymap:
                #this throws away the wavelength data for references but I vote that check be handled some other way or skipped
                refd[rk]=numpy.float32([\
                    (readbinary_selinds(os.path.join(expdatfolder, fn+'.dat'), nkeys, keyinds=keyinds)[1:]).mean(axis=0) \
                    for fn, nkeys, keyinds in self.refdict__fn_nkeys_keyinds[rktup]]).mean(axis=0)#this is mean of means
            refd_Tfn=lambda Tfn:refd #this trivial function costs no time and for nontrivial on-the-fly ref calculations, define a fcn with the same name
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
                fni='%s__%s_interlen.dat' %(anak,Tfn[:-4])
                p=os.path.join(destfolder,fni)
                kl=saveinterdata(p, interlend)
                self.interfiledict[fni]='%s;%s' %('eche_inter_interlen_file', ','.join(kl))
        fnf='%s__%s.csv' %(anak,'-'.join(self.fomnames))
        p=os.path.join(destfolder,fnf)
        self.csvfilstr=createcsvfilstr(self.fomdlist, self.fomnames)
        writecsv_smpfomd(p, self.csvfilstr)

        self.fomfiledict[fnf]='csv_fom_file;'+','.join(['sample_no']+self.fomnames)
    def fomtuplist_rawlend_interlend(self, Tdataarr, Rdataarr, refd):
        if Tdataarr.shape[1]!=Rdataarr.shape[1] or Tdataarr.shape[1]!=refd['Tdark'].shape[0]:
            return [('testfom', numpy.nan)], {}, {}
        interd_rawlen=copy.copy(refd)
        interd_rawlen['wl']=Tdataarr[0]
        interd_rawlen['T']=Tdataarr[1:].mean(axis=0)
        interd_rawlen['R']=Rdataarr[1:].mean(axis=0)
        interd_rawlen['Tfrac']=(interd_rawlen['T']-refd['Tdark'])/(refd['Tlight']-refd['Tdark'])
        interd_rawlen['Rfrac']=(interd_rawlen['R']-refd['Rdark'])/(refd['Rlight']-refd['Rdark'])
        interd_rawlen['Tover1minusR']=interd_rawlen['Tfrac']/(1.-interd_rawlen['Rfrac'])
        interd={}
        interd['partT']=interd_rawlen['T'][:100]
        interd['rawselectinds']=numpy.arange(100)
        return [('testfom', interd_rawlen['T'].mean())], interd_rawlen, interd
        
c=Analysis_T_UVVIS()
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
