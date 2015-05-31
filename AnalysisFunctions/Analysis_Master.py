import numpy, copy, operator
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
    filedlist=[dict({}, expkeys=[runk, 'files_technique__'+techk, typek, fnk], run=runk, fn=fnk, \
                                     nkeys=len(v['keys']), reqkeyinds=[v['keys'].index(reqk) for reqk in requiredkeys if reqk in v['keys']], \
                                     optkeyinds=[(optk in v['keys'] and (v['keys'].index(optk),) or (None,))[0] for optk in optionalkeys])\
            for runk in runklist \
            for fnk, v in expfiledict[runk]['files_technique__'+techk][typek].iteritems()\
            if not (False in [reqk in v['keys'] for reqk in requiredkeys])\
            ]
    filedlist=[dict(d, keyinds=d['reqkeyinds']+[k for k in d['optkeyinds'] if not k is None]) for d in filedlist]

    return num_files_considered, filedlist

    
def stdcheckoutput(fomdlist, fomnames):
    nancount=[(not k in fomdlist) or numpy.isnan(d[k]) for d in fomdlist for k in fomnames].count(True)
    return nancount, 1.*nancount/(len(fomdlist)*len(fomnames))

class Analysis_Master_nointer():
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams=dict([])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis_Master1'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.fomnames=[]
        self.plotparams={}
        self.csvheaderdict=dict({}, csv_version='1')
        
    def processnewparams(self):
        return
    #this gets the applicable filenames and there may be other required filenames for analysis which can be saved locally and use in self.perform
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
        self.num_files_considered, self.filedlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys)
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filedlist
    
    def check_input(self, critfracapplicable=0.9):
        fracapplicable=1.*len(self.filedlist)/self.num_files_considered
        return fracapplicable>critfracapplicable, \
        '%d files, %.2f of those available, do not meet requirements' %(self.num_files_considered-len(self.filedlist), 1.-fracapplicable)
    def check_output(self, critfracnan=0.9):
        numnan, fracnan=stdcheckoutput(self.fomdlist, self.fomnames)
        return fracnan<=critfracnan, \
        '%d FOMs, %.2f of attempted calculations, are NaN' %(numnan, fracnan)
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak=''):
        self.fomfiledict={}
        self.interfiledict={}
        self.fomdlist=[]
        for filed in self.filedlist:
            fn=filed['fn']
            dataarr=readbinary_selinds(os.path.join(expdatfolder, fn+'.dat'), filed['nkeys'], keyinds=filed['keyinds'])
            self.fomdlist+=[dict([('sample_no', getsamplenum_fn(fn))]+self.fomtuplist_dataarr(dataarr))]
            #writeinterdat
        fnf='%s__%s.csv' %(anak,'-'.join(self.fomnames))
        p=os.path.join(destfolder,fnf)
        self.csvfilstr=createcsvfilstr(self.fomdlist, self.fomnames)#, fn=fnf)
        totnumheadlines=writecsv_smpfomd(p, self.csvfilstr, headerdict=self.csvheaderdict)
        self.primarycsvpath=p
        self.fomfiledict[fnf]='%s;%s;%d;%d' %('csv_fom_file', ','.join(['sample_no']+self.fomnames), totnumheadlines, len(self.fomdlist))
        
class Analysis_Master_inter(Analysis_Master_nointer):
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak=''):
        self.fomfiledict={}
        self.interfiledict={}
        self.fomdlist=[]
        for filed in self.filedlist:
            fn=filed['fn']
            dataarr=readbinary_selinds(os.path.join(expdatfolder, fn+'.dat'), filed['nkeys'], keyinds=filed['keyinds'])
            fomtuplist, rawlend, interlend=self.fomtuplist_rawlend_interlend(dataarr)
            self.fomdlist+=[dict([('sample_no', getsamplenum_fn(fn))]+fomtuplist)]
            if len(rawlend.keys())>0:
                fnr='%s__%s_rawlen.txt' %(anak,os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fnr)
                kl=saveinterdata(p, rawlend, savetxt=True)
                self.interfiledict[fnr]='%s;%s;%d;%d' %('eche_inter_rawlen_file', ','.join(kl), 1, len(rawlend[kl[0]]))
            if 'rawselectinds' in interlend.keys():
                fni='%s__%s_interlen.txt' %(anak,os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fni)
                kl=saveinterdata(p, interlend, savetxt=True)
                self.interfiledict[fni]='%s;%s;%d;%d' %('eche_inter_interlen_file', ','.join(kl), 1, len(interlend[kl[0]]))
        fnf='%s__%s.csv' %(anak,'-'.join(self.fomnames))
        p=os.path.join(destfolder,fnf)
        self.csvfilstr=createcsvfilstr(self.fomdlist, self.fomnames)#, fn=fnf)
        totnumheadlines=writecsv_smpfomd(p, self.csvfilstr, headerdict=self.csvheaderdict)
        self.primarycsvpath=p
        self.fomfiledict[fnf]='%s;%s;%d;%d' %('csv_fom_file', ','.join(['sample_no']+self.fomnames), totnumheadlines, len(self.fomdlist))
