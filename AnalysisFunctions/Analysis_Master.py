import numpy, copy
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.split(os.getcwd())[0])

from fcns_math import *
from fcns_io import *
from csvfilewriter import createcsvfilstr
def echeparsetech(s):
    while len(s)>0 and s[-1].isdigit():
        s=s[:-1]
    return s
def stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=None, requiredkeys=[], optionalkeys=[]):
    if runklist is None:
        runklist=expfiledict.keys()
    runklist=[runk for runk in runklist \
    if runk.startswith('run__') and \
        expfiledict[runk]['run_use']==usek and \
        ('files_technique__'+techk) in expfiledict[runk].keys() and \
        typek in expfiledict[runk]['files_technique__'+techk].keys()]

    num_files_considered=numpy.int32([len(expfiledict[runk]['files_technique__'+techk][typek]) for runk in runklist]).sum()
    fn_nkeys_keyinds=[(fnk, len(keys), [keys.index(reqk) for reqk in requiredkeys+optionalkeys if reqk in keys])\
            for runk in runklist \
            for fnk, keys in expfiledict[runk]['files_technique__'+techk][typek].iteritems()\
            if not (False in [reqk in keys for reqk in requiredkeys])\
            ]
    filenames=[fn for fn, nkeys, reqkeyinds in fn_nkeys_keyinds]
    #fn_nkeys_keyinds is length of all files considered, filenames are the ones that meet requirements, which in this e case having all of the requiredkeys
    return num_files_considered, filenames, fn_nkeys_keyinds

    
def stdcheckoutput(fomdlist, fomnames):
    nancount=[(not k in fomdlist) or numpy.isnan(d[k]) for d in fomdlist for k in fomnames].count(True)
    return nancount, 1.*nancount/(len(fomdlist)*len(fomnames))

class Analysis_Master_nointer():
    def __init__(self):
        self.analysis_version='1'
        self.dfltparams=dict([])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis_Master1'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.fomnames=[]
        
    #this gets the applicable filenames and there may be other required filenames for analysis which can be saved locally and use in self.perform
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None):
        self.num_files_considered, self.filenames, self.fn_nkeys_keyinds=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys)
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filenames
    
    def check_input(self, critfracapplicable=0.9):
        fracapplicable=1.*len(self.filenames)/self.num_files_considered
        return fracapplicable>critfracapplicable, \
        '%d files, %.2f of those available, do not meet requirements' %(self.num_files_considered-len(self.filenames), 1.-fracapplicable)
    def check_output(self, critfracnan=0.9):
        numnan, fracnan=stdcheckoutput(self.fomdlist, self.fomnames)
        return fracnan>critfracnan, \
        '%d FOMs, %.2f of attempted calculations, are NaN' %(numnan, fracnan)
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak=''):
        self.fomfiledict={}
        self.interfiledict={}
        self.fomdlist=[]
        for fn, nkeys, reqkeyinds in self.fn_nkeys_keyinds:
            dataarr=readbinary_selinds(os.path.join(expdatfolder, fn+'.dat'), nkeys, keyinds=reqkeyinds)
            self.fomdlist+=[dict([('sample_no', getsamplenum_fn(fn))]+self.fomtuplist_dataarr(dataarr))]
            #writeinterdat
        fnf='%s__%s.csv' %(anak,'-'.join(self.fomnames))
        p=os.path.join(destfolder,fnf)
        self.csvfilstr=createcsvfilstr(self.fomdlist, self.fomnames)#, fn=fnf)
        writecsv_smpfomd(p, self.csvfilstr)
        self.fomfiledict[fnf]='csv_fom_file;'+','.join(['sample_no']+self.fomnames)
        
class Analysis_Master_inter(Analysis_Master_nointer):
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak=''):
        self.fomfiledict={}
        self.interfiledict={}
        self.fomdlist=[]
        for fn, nkeys, reqkeyinds in self.fn_nkeys_keyinds:
            dataarr=readbinary_selinds(os.path.join(expdatfolder, fn+'.dat'), nkeys, keyinds=reqkeyinds)
            fomtuplist, rawlend, interlend=self.fomtuplist_rawlend_interlend(dataarr)
            self.fomdlist+=[dict([('sample_no', getsamplenum_fn(fn))]+fomtuplist)]
            if len(rawlend.keys())>0:
                fnr='%s__%s_rawlen.dat' %(anak,fn[:-4])
                p=os.path.join(destfolder,fnr)
                kl=saveinterdata(p, rawlend)
                self.interfiledict[fnr]='%s;%s' %('eche_inter_rawlen_file', ','.join(kl))
            if 'rawselectinds' in interlend.keys():
                fni='%s__%s_interlen.dat' %(anak,fn[:-4])
                p=os.path.join(destfolder,fni)
                kl=saveinterdata(p, interlend)
                self.interfiledict[fni]='%s;%s' %('eche_inter_interlen_file', ','.join(kl))
        fnf='%s__%s.csv' %(anak,'-'.join(self.fomnames))
        p=os.path.join(destfolder,fnf)
        self.csvfilstr=createcsvfilstr(self.fomdlist, self.fomnames)#, fn=fnf)
        writecsv_smpfomd(p, self.csvfilstr)
        self.fomfiledict[fnf]='csv_fom_file;'+','.join(['sample_no']+self.fomnames)
