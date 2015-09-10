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
def stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=None, requiredkeys=[], optionalkeys=[], requiredparams=[]):
    requiredparams+=['plate_id']
    if runklist is None:
        runklist=expfiledict.keys()
    runklist=[runk for runk in runklist \
    if runk.startswith('run__') and \
        expfiledict[runk]['run_use']==usek and \
        ('files_technique__'+techk) in expfiledict[runk].keys() and \
        typek in expfiledict[runk]['files_technique__'+techk].keys()]

    num_files_considered=numpy.int32([len(expfiledict[runk]['files_technique__'+techk][typek]) for runk in runklist]).sum()
    filedlist=[dict(\
                        dict([(reqparam, expfiledict[runk]['parameters'][reqparam]) for reqparam in requiredparams]),\
                                     expkeys=[runk, 'files_technique__'+techk, typek, fnk], run=runk, fn=fnk, sample_no=v['sample_no'], \
                                     nkeys=len(v['keys']), num_header_lines=v['num_header_lines'], \
                                     reqkeyinds=[v['keys'].index(reqk) for reqk in requiredkeys if reqk in v['keys']], \
                                     optkeyinds=[(optk in v['keys'] and (v['keys'].index(optk),) or (None,))[0] for optk in optionalkeys])\
            for runk in runklist \
            for fnk, v in expfiledict[runk]['files_technique__'+techk][typek].iteritems()\
            if not (False in [reqk in v['keys'] for reqk in requiredkeys])\
            and not (False in [reqparam in expfiledict[runk]['parameters'].keys() for reqparam in requiredparams])\
            ]
    filedlist=[dict(d, keyinds=d['reqkeyinds']+[k for k in d['optkeyinds'] if not k is None]) for d in filedlist]

    return num_files_considered, filedlist


def stdcheckoutput(fomdlist, fomnames, filedlist):
    nancount=[(not k in d) or numpy.isnan(d[k]) for d in fomdlist for k in fomnames].count(True)
    nancount+=len(fomnames)*(len(filedlist)-len(fomdlist))#any missing fomd  (there is a filed but not fomd) counts as len(fomnames) wirth fo NaN
    return nancount, 1.*nancount/(len(fomdlist)*len(fomnames))

class Analysis_Master_nointer():
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams=dict([])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis_Master1'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=[]
        self.plotparams={}
        self.csvheaderdict=dict({}, csv_version='1')
        
    def processnewparams(self):
        return
    #this gets the applicable filenames and there may be other required filenames for analysis which can be saved locally and use in self.perform
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
        self.num_files_considered, self.filedlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys, requiredparams=self.requiredparams)
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filedlist
    
    def check_input(self, critfracapplicable=0.9):
        fracapplicable=1.*len(self.filedlist)/self.num_files_considered
        return fracapplicable>critfracapplicable, \
        '%d files, %.2f of those available, do not meet requirements' %(self.num_files_considered-len(self.filedlist), 1.-fracapplicable)
    def check_output(self, critfracnan=0.9):
        if len(self.fomdlist)==0:
            return False, 'No data'
        numnan, fracnan=stdcheckoutput(self.fomdlist, self.fomnames, self.filedlist)
        return fracnan<=critfracnan, \
        '%d FOMs, %.2f of attempted calculations, are NaN or missing' %(numnan, fracnan)
    def initfiledicts(self, runfilekeys=[]):
        self.multirunfiledict=dict({}, fom_files={})
        if len(runfilekeys)>0:
            runklist=sorted(list(set([filed['run'] for filed in self.filedlist])))
            self.runfiledict=dict([(runk, dict([(fk, {}) for fk in runfilekeys])) for runk in runklist])
        else:
            self.runfiledict={}
    def readdata(self, p, numkeys, keyinds, num_header_lines=0):
        pd=p+'.dat'
        if not os.path.isfile(pd):
            pd=prepend_root_exp_path(pd)
        try:
            dataarr=readbinary_selinds(pd, numkeys, keyinds)
            return dataarr
        except:
            pass
#        pt=<buildrunpath>(p)
#        dataarr=readtxt_selectcolumns(pt, selcolinds=keyinds, delim=None, num_header_lines=num_header_lines)
        return dataarr
        
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak=''):
        self.initfiledicts()
        self.fomdlist=[]
        for filed in self.filedlist:
            if numpy.isnan(filed['sample_no']):
                if self.debugmode:
                    raiseTEMP
                continue
            fn=filed['fn']
            #try:
            dataarr=self.readdata(os.path.join(expdatfolder, fn), filed['nkeys'], filed['keyinds'], num_header_lines=filed['num_header_lines'])
#            except:
#                if self.debugmode:
#                    raiseTEMP
#                continue
            self.fomdlist+=[dict(self.fomtuplist_dataarr(dataarr, filed), sample_no=filed['sample_no'], plate_id=filed['plate_id'], run=filed['run'], runint=int(filed['run'].partition('run__')[2]))]
            #writeinterdat
        self.writefom(destfolder, anak)
    def writefom(self, destfolder, anak):
        fnf='%s__%s.csv' %(anak,'-'.join(self.fomnames[:3]))#name file by foms but onyl inlcude the 1st 3 to avoid long names
        self.csvfilstr=createcsvfilstr(self.fomdlist, self.fomnames, intfomkeys=['runint','plate_id'])#, fn=fnf)
        if destfolder is None:
            return

        p=os.path.join(destfolder,fnf)
        totnumheadlines=writecsv_smpfomd(p, self.csvfilstr, headerdict=self.csvheaderdict)
        self.primarycsvpath=p
        self.multirunfiledict['fom_files'][fnf]='%s;%s;%d;%d' %('csv_fom_file', ','.join(['sample_no', 'runint', 'plate_id']+self.fomnames), totnumheadlines, len(self.fomdlist))
        
class Analysis_Master_inter(Analysis_Master_nointer):
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak=''):
        self.initfiledicts(runfilekeys=['inter_rawlen_files','inter_files'])
        self.fomdlist=[]
        for filed in self.filedlist:
            if numpy.isnan(filed['sample_no']):
                if self.debugmode:
                    raiseTEMP
                continue
            fn=filed['fn']
            dataarr=self.readdata(os.path.join(expdatfolder, fn), filed['nkeys'], filed['keyinds'], num_header_lines=filed['num_header_lines'])
            try:
                dataarr=self.readdata(os.path.join(expdatfolder, fn), filed['nkeys'], filed['keyinds'], num_header_lines=filed['num_header_lines'])
            except:
                if self.debugmode:
                    raiseTEMP
                continue
            fomtuplist, rawlend, interlend=self.fomtuplist_rawlend_interlend(dataarr, filed)
            if not numpy.isnan(filed['sample_no']):#do not save the fom but can save inter data
                self.fomdlist+=[dict(fomtuplist, sample_no=filed['sample_no'], plate_id=filed['plate_id'], run=filed['run'], runint=int(filed['run'].partition('run__')[2]))]
            if destfolder is None:
                continue
            if len(rawlend.keys())>0:
                fnr='%s__%s_rawlen.txt' %(anak,os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fnr)
                kl=saveinterdata(p, rawlend, savetxt=True)
                self.runfiledict[filed['run']]['inter_rawlen_files'][fnr]='%s;%s;%d;%d;%d' %('eche_inter_rawlen_file', ','.join(kl), 1, len(rawlend[kl[0]]), filed['sample_no'])
            if 'rawselectinds' in interlend.keys():
                fni='%s__%s_interlen.txt' %(anak,os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fni)
                kl=saveinterdata(p, interlend, savetxt=True)
                self.runfiledict[filed['run']]['inter_files'][fni]='%s;%s;%d;%d;%d' %('eche_inter_interlen_file', ','.join(kl), 1, len(interlend[kl[0]]), filed['sample_no'])
        self.writefom(destfolder, anak)
