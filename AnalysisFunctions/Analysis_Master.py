import numpy, copy, operator
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.split(os.getcwd())[0])

from fcns_math import *
from fcns_io import *
from fcns_ui import *
from csvfilewriter import createcsvfilstr
def echeparsetech(s):
    while len(s)>0 and s[-1].isdigit():
        s=s[:-1]
    return s
def stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=None, requiredkeys=[], optionalkeys=[], requiredparams=[]):
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
                                     expkeys=[runk, 'files_technique__'+techk, typek, fnk], run=runk, fn=fnk, sample_no=v['sample_no'], \
                                     nkeys=len(v['keys']), num_header_lines=v['num_header_lines'], \
                                     reqkeyinds=[v['keys'].index(reqk) for reqk in requiredkeys if reqk in v['keys']], \
                                     optkeyinds=[(optk in v['keys'] and (v['keys'].index(optk),) or (None,))[0] for optk in optionalkeys])\
            for runk in runklist \
            for fnk, v in expfiledict[runk]['files_technique__'+techk][typek].iteritems()\
            if 'keys' in v.keys() and not (False in [reqk in v['keys'] for reqk in requiredkeys])\
            and not (False in [reqparam in expfiledict[runk]['parameters'].keys() for reqparam in requiredparams])\
            ]
    filedlist=[dict(d, keyinds=d['reqkeyinds']+[k for k in d['optkeyinds'] if not k is None]) for d in filedlist]

    filedlist=[dict(d, user_run_foms=expfiledict[d['run']]['user_run_foms'] if 'user_run_foms' in expfiledict[d['run']].keys() else {}) for d in filedlist]#has to be here because only place with access to expfiledict
    filedlist=[dict(d, run_foms=expfiledict[d['run']]['run_foms'] if 'run_foms' in expfiledict[d['run']].keys() else {}) for d in filedlist]#has to be here because only place with access to expfiledict
    
    return num_files_considered, filedlist


def getapplicablefilenames_byuse_tech_type(expfiledict, usek, techk, typek, runklist=None, requiredparams=[]):
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
                                     expkeys=[runk, 'files_technique__'+techk, typek, fnk], run=runk, fn=fnk, techk=techk, sample_no=v['sample_no'] if 'sample_no' in v.keys() else 0, \
                                     )\
            for runk in runklist \
            for fnk, v in expfiledict[runk]['files_technique__'+techk][typek].iteritems()\
            if not (False in [reqparam in expfiledict[runk]['parameters'].keys() for reqparam in requiredparams])\
            ]

    filedlist=[dict(d, user_run_foms=expfiledict[d['run']]['user_run_foms'] if 'user_run_foms' in expfiledict[d['run']].keys() else {}) for d in filedlist]#has to be here because only place with access to expfiledict
    filedlist=[dict(d, run_foms=expfiledict[d['run']]['run_foms'] if 'run_foms' in expfiledict[d['run']].keys() else {}) for d in filedlist]#has to be here because only place with access to expfiledict
    
    return num_files_considered, filedlist
    
def stdcheckoutput(fomdlist, fomnames, filedlist):
    nancount=[(not k in d) or (isinstance(d[k], float) and numpy.isnan(d[k])) for d in fomdlist for k in fomnames].count(True)
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
    
    def getgeneraltype(self):#make this fucntion so it is inhereted
        return 'standard'
    
    def prepareanafilestuples__runk_typek_multirunbool(self):
        runk_typek_b=sorted([('multi_run', typek, True) for typek in self.multirunfiledict.keys() if len(self.multirunfiledict[typek])>0])
        runk_typek_b+=sorted([(runk, typek, False) for runk, rund in self.runfiledict.iteritems() for typek in rund.keys() if len(rund[typek])>0])
        return runk_typek_b
    def processnewparams(self, calcFOMDialogclass=None):
        return
    #this gets the applicable filenames and there may be other required filenames for analysis which can be saved locally and use in self.perform
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None, calcFOMDialogclass=None):
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
    def initfiledicts(self, runfilekeys=[], runklist=None):
        self.multirunfiledict=dict({}, fom_files={})
        if len(runfilekeys)>0:
            if runklist is None:
                runklist=sorted(list(set([filed['run'] for filed in self.filedlist])))
            self.runfiledict=dict([(runk, dict([(fk, {}) for fk in runfilekeys])) for runk in runklist])
        else:
            self.runfiledict={}
    
    def prepare_filedlist(self, filedlist, expfiledict, expdatfolder=None, expfolderzipclass=None, fnk='fn'):
        #for every dict in filedlist, updates by reference to add keys readfcn and readfcn_args that can be called to get the data arr for that file, for zip or folder, .dat or ascii
        #some similarities to buildrunpath_selectfile but since trying to batch prepare things can't use this file-by-file approach
        #[d.update([('AAA', 5)]) for d in filedlist]
        #return []
        closeziplist=[]
        runk_or_none=None
        if (not expfolderzipclass) or (not expdatfolder is None):# and not os.path.isdir(expdatfolder)):#if zipclass is an open .zip then don't need the path, but if not and expdat folder provided but is not absolute path, make it an absolute path
            expdatfolder=prepend_root_exp_path(expdatfolder)
        if expfolderzipclass is None and expdatfolder is None:#read all from runfolders
            runk_or_none=[d['run'] for d in filedlist]
        elif expfolderzipclass is None:
            expfolderzipclass=gen_zipclass(expdatfolder)
            if bool(expfolderzipclass):
                closeziplist+=[expfolderzipclass]#close this at the end of perform only if it was created here
                
        if runk_or_none is None:
            #first an exp folde r(not zip) and then an exp zip are handled for raw .dat file. if the .dat file exists then d.update returns None and otherwise the runk is put fofr further processing below
            if not bool(expfolderzipclass):
                expfns=os.listdir(expdatfolder)
                runk_or_none=[\
                  d.update([('readfcn', readbinary_selinds), ('readfcn_args', (os.path.join(expdatfolder, d[fnk]+'.dat'), d['nkeys'])), ('readfcn_kwargs', {'keyinds':d['keyinds'], 'zipclass':False})])\
                      if (d[fnk]+'.dat') in expfns else d['run'] for d in filedlist]
            else:
                runk_or_none=[\
                  d.update([('readfcn', readbinary_selinds), ('readfcn_args', (os.path.join(expdatfolder, d[fnk]+'.dat'), d['nkeys'])), ('readfcn_kwargs', {'keyinds':d['keyinds'], 'zipclass':expfolderzipclass})])\
                      if expfolderzipclass.fn_in_archive(d[fnk]+'.dat') else d['run'] for d in filedlist]
        
        runstoopen=list(set([runk for runk in runk_or_none if not runk is None]))
        for runk in runstoopen:
            runp=expfiledict[runk]['run_path']
            runp=buildrunpath(runp)
            runzipclass=gen_zipclass(runp)
            if bool(runzipclass):
                pathjoinfcn=lambda fn:fn
                closeziplist+=[runzipclass]#don't leave runzipclass open after perform finished
            else:
                pathjoinfcn=lambda fn:os.path.join(runp, fn)
            [\
              d.update([('readfcn', readtxt_selectcolumns), ('readfcn_args', (pathjoinfcn(d[fnk]), )), ('readfcn_kwargs', {'num_header_lines':d['num_header_lines'], 'selcolinds':d['keyinds'], 'zipclass':runzipclass, 'delim':None})])\
                for rk, d in zip(runk_or_none, filedlist) if rk==runk]
        
        return closeziplist
    def readdata(self, p, numkeys, keyinds, num_header_lines=0, zipclass=None):
        if not (os.path.isdir(os.path.split(p)[0]) or os.path.isdir(os.path.split(os.path.split(p)[0])[0])):
            p=prepend_root_exp_path(p)
        try:
            pd=p+'.dat'
            dataarr=readbinary_selinds(pd, numkeys, keyinds, zipclass=zipclass)
            return dataarr
        except:
            pass
#        pt=<buildrunpath>(p) could try to build the run path but assume that if expdatfolder exists then the appropriate .dat is there
        dataarr=readtxt_selectcolumns(p, selcolinds=keyinds, delim=None, num_header_lines=num_header_lines, zipclass=zipclass)#this could read ascii version in .ana for anlaysis that builds on analysis (e.g. CV_photo), or hypothetically in .exp but nothing as of 201509 that write ascii to .exp - this may be needed for on-the-fly
        return dataarr
    
    def genuserfomdlist(self, anauserfomd, appendtofomdlist=True):
        
        #user_run_foms and run_foms shoudl not have any overlapping keys, if they are present their items will be appended and filtered for overlap with fom names and anauserfoms 
        userfomdlist=[dict(\
        [(k, v) for k, v in \
            ((d['user_run_foms'].items() if 'user_run_foms' in d.keys() else []) \
            +(d['run_foms'].items() if 'run_foms' in d.keys() else [])) \
                            if not (k in self.fomnames or k in anauserfomd.keys())]\
        ) for d in self.filedlist]
        
        userfomdlist=[dict([(k, v) for k, v in d['run_foms'].iteritems() if not (k in self.fomnames or k in anauserfomd.keys())]) if 'run_foms' in d.keys() else {} for d in self.filedlist]
        #if anything is str, then all will be str
        strkeys=set([k for d in userfomdlist for k, v in d.iteritems() if isinstance(v, str)])
        floatkeys=list(set([k for d in userfomdlist for k in d.keys()]).difference(strkeys))
        strkeys=list(strkeys)
        
        #fill i missing values withappropriate defaults. would also filter any unnecesary keys but there aren't and it wouldn't be necessary anyway
        userfomdlist=[dict([(k, str(d[k]) if k in d.keys() else '') for k in strkeys]+[(k, float(d[k]) if k in d.keys() else numpy.nan) for k in floatkeys]) for d in userfomdlist]

        if len(userfomdlist)<len(self.fomdlist):#for typicaly analysis filedlit and fomdlit are same length but for process fom filedlist is only the fom files and fomdlist is arbitrary length - in this case shouldn't have anr run-based FOMs anyway so this is just a formality
            userfomdlist=[userfomdlist[0]]*len(self.fomdlist)
        
        anauserfomd=dict([(k, v) for k, v in anauserfomd.iteritems() if not k in self.fomnames])
        strkeys+=[k for k, v in anauserfomd.iteritems() if isinstance(v, str)]
        floatkeys+=[k for k, v in anauserfomd.iteritems() if not isinstance(v, str)]
        
        userfomdlist=[dict(d, **anauserfomd) for d in userfomdlist]
        
        if appendtofomdlist:
            self.fomdlist=[dict(d, **userd) for d, userd in zip(self.fomdlist, userfomdlist)]#adds user foms to fomdlist dicts but the corresponding keys are NOT in self.fomnames
        return sorted(strkeys), sorted(floatkeys), userfomdlist
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, expfiledict=None, anauserfomd={}):#zipclass intended to be the class with open zip archive if expdatfolder is a .zip so that the archive is not repeatedly opened
        self.initfiledicts()
        closeziplist=self.prepare_filedlist(self.filedlist, expfiledict, expdatfolder=expdatfolder, expfolderzipclass=zipclass, fnk='fn')
        self.fomdlist=[]
        for filed in self.filedlist:
#            if numpy.isnan(filed['sample_no']):
#                if self.debugmode:
#                    raiseTEMP
#                continue
            fn=filed['fn']
            try:
                dataarr=filed['readfcn'](*filed['readfcn_args'], **filed['readfcn_kwargs'])
                fomtuplist=self.fomtuplist_dataarr(dataarr, filed)
            except:
                if self.debugmode:
                    raiseTEMP
                fomtuplist=[(k, numpy.nan) for k in self.fomnames]
                pass
            self.fomdlist+=[dict(fomtuplist, sample_no=filed['sample_no'], plate_id=filed['plate_id'], run=filed['run'], runint=int(filed['run'].partition('run__')[2]))]
            #writeinterdat
        self.writefom(destfolder, anak, anauserfomd=anauserfomd)
        for zc in closeziplist:
            zc.close()

    def writefom(self, destfolder, anak, anauserfomd={}, fn=None, strkeys_fomdlist=[], createdummyfomdlist=False, num_intfoms_at_start_of_fomdlist=0):#self.fomnames assumed to be float, createdummyfomdlist is for writing all NaN and aborting analysis
        if createdummyfomdlist:
            self.fomdlist=[dict([(k, numpy.nan) for k in self.fomnames], sample_no=filed['sample_no'], plate_id=filed['plate_id'], run=filed['run'], runint=int(filed['run'].partition('run__')[2])) for filed in self.filedlist]
        strkeys, floatkeys, userfomdlist=self.genuserfomdlist(anauserfomd)
        
        if fn is None:
            fn='%s__%s.csv' %(anak,'-'.join(self.fomnames[:3]))#name file by foms but onyl inlcude the 1st 3 to avoid long names
        self.multirunfiledict['fom_files'][fn]=\
          self.writefom_bare(destfolder, fn, strkeys=strkeys+strkeys_fomdlist, floatkeys=floatkeys+self.fomnames[num_intfoms_at_start_of_fomdlist:], intfomkeys=['runint','plate_id']+self.fomnames[:num_intfoms_at_start_of_fomdlist])
        
    def writefom_bare(self, destfolder, fn, strkeys=[], floatkeys=None, intfomkeys=['runint','plate_id']):
        if floatkeys is None:
            floatkeys=self.fomnames
        self.csvfilstr=createcsvfilstr(self.fomdlist, floatkeys, intfomkeys=intfomkeys, strfomkeys=strkeys)#, fn=fnf)self.fomnames
        if destfolder is None:
            return
        
        allfomnames=['sample_no']+intfomkeys+strkeys+floatkeys#this is the order in createcsvfilstr and doesn't allow int userfoms
        
        p=os.path.join(destfolder,fn)
        totnumheadlines=writecsv_smpfomd(p, self.csvfilstr, headerdict=self.csvheaderdict)
        self.primarycsvpath=p#every writefom goes through here to set the primarycsvpath for the analysis class
        return '%s;%s;%d;%d' %('csv_fom_file', ','.join(allfomnames), totnumheadlines, len(self.fomdlist))
        
class Analysis_Master_inter(Analysis_Master_nointer):
    def make_inter_fn_start(self, anak, runint=None):
        if runint is None:
            return anak
        else:
            return '%s__run__%d' %(anak,runint)
        
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):
        self.initfiledicts(runfilekeys=['inter_rawlen_files','inter_files'])
        closeziplist=self.prepare_filedlist(self.filedlist, expfiledict, expdatfolder=expdatfolder, expfolderzipclass=zipclass, fnk='fn')
        self.fomdlist=[]
        for filed in self.filedlist:
            if numpy.isnan(filed['sample_no']):
                if self.debugmode:
                    raiseTEMP
                continue
            fn=filed['fn']
            try:
                dataarr=filed['readfcn'](*filed['readfcn_args'], **filed['readfcn_kwargs'])
                fomtuplist, rawlend, interlend=self.fomtuplist_rawlend_interlend(dataarr, filed)
            except:
                if self.debugmode:
                    raiseTEMP
                fomtuplist, rawlend, interlend=[(k, numpy.nan) for k in self.fomnames], {}, {}#if error have the sample written below so fomdlist stays commensurate with filedlist, but fill everythign with NaN and no interdata
                pass
            runint=int(filed['run'].partition('run__')[2])
            if not numpy.isnan(filed['sample_no']):#do not save the fom but can save inter data
                self.fomdlist+=[dict(fomtuplist, sample_no=filed['sample_no'], plate_id=filed['plate_id'], run=filed['run'], runint=runint)]
            if destfolder is None:
                continue
            if len(rawlend.keys())>0:
                fnr='%s__%s_rawlen.txt' %(self.make_inter_fn_start(anak,runint), os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fnr)
                kl=saveinterdata(p, rawlend, savetxt=True)
                self.runfiledict[filed['run']]['inter_rawlen_files'][fnr]='%s;%s;%d;%d;%d' %('eche_inter_rawlen_file', ','.join(kl), 1, len(rawlend[kl[0]]), filed['sample_no'])
            if 'rawselectinds' in interlend.keys():
                fni='%s__%s_interlen.txt' %(self.make_inter_fn_start(anak,runint), os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fni)
                kl=saveinterdata(p, interlend, savetxt=True)
                self.runfiledict[filed['run']]['inter_files'][fni]='%s;%s;%d;%d;%d' %('eche_inter_interlen_file', ','.join(kl), 1, len(interlend[kl[0]]), filed['sample_no'])
        self.writefom(destfolder, anak, anauserfomd=anauserfomd)
        for zc in closeziplist:
            zc.close()

def gethighestanak(anadict, getnextone=False):
    kfcn=lambda i:'ana__%d' %i
    i=1
    while kfcn(i) in anadict.keys():
        i+=1
    if getnextone:
        anak=kfcn(i)
    else:
        anak=kfcn(i-1)
        if not anak in anadict.keys():
            return None
    return anak

class calcfom_mock_class():
    def __init__(self, savefolder):
        self.expfolder=None
        self.anadict={}
        self.anadict['ana_version']='3'
        self.tempanafolder=savefolder
        self.userfomd={}
        self.expfiledict=[]
        self.expzipclass=False
        self.guimode=False
        self.paramsdict_le_dflt={}
        self.paramsdict_le_dflt['description']='custom analysis'

    
def calcfom_analyzedata_calcfomdialogclass(self, checkinputbool=True):#this argument is called self sothsi function appears the same as it would as part of the calcfomdialogclass
    #minimal requirements of self: expfolder,anadict,tempanafolder,userfomd,expfiledict,expzipclass,guimode,paramsdict_le_dflt['description']
    if self.analysisclass is None:
        return 'no analysis class defined'
    if checkinputbool:
        checkbool, checkmsg=self.analysisclass.check_input()
        if not checkbool:
            if self.guimode:
                idialog=messageDialog(self, 'Continue analysis? '+checkmsg)
                if not idialog.exec_():
                    return 'user canceled analysis because: ', checkmsg
            else:
                return checkmsg

    expdatfolder=self.expfolder
    
    anak=gethighestanak(self.anadict, getnextone=True)
    #try:
    if 1:
        self.analysisclass.perform(self.tempanafolder, expdatfolder=expdatfolder, anak=anak, zipclass=self.expzipclass, expfiledict=self.expfiledict, anauserfomd=self.userfomd)
#        except:
#            idialog=messageDialog(self, 'Analysis Crashed. Nothing saved')
#            if not idialog.exec_():
#                removefiles(self.tempanafolder, [k for rund in \
#                   ([self.analysisclass.multirunfiledict]+self.analysisclass.runfiledict.items()) for typed in rund.items() for k in typed.keys()])
#                return
    runk_typek_b=self.analysisclass.prepareanafilestuples__runk_typek_multirunbool()
    killana=False
    if len(runk_typek_b)==0:
        killana=True
        checkmsg='no analysis output'
    else:
        checkbool, checkmsg=self.analysisclass.check_output()
        if not checkbool:
            if self.guimode:
                idialog=messageDialog(self, 'Keep analysis? '+checkmsg)
                if not idialog.exec_():
                    killana=True
            else:
                killana=True
            if killana:
                removefiles(self.tempanafolder, [k for d in \
                        ([self.analysisclass.multirunfiledict]+self.analysisclass.runfiledict.values()) for typed in d.values() for k in typed.keys()])
            
    if killana:
        return checkmsg#anadict not been modified yet
    
    self.anadict[anak]={}
    
    self.activeana=self.anadict[anak]
    if not checkbool:
        self.activeana['check_output_message']=checkmsg
    for runk, typek, b in runk_typek_b:
        frunk='files_'+runk
        if not frunk in self.activeana.keys():
            self.activeana[frunk]={}
        if b:
            self.activeana[frunk][typek]=copy.deepcopy(self.analysisclass.multirunfiledict[typek])
        else:
            self.activeana[frunk][typek]=copy.deepcopy(self.analysisclass.runfiledict[runk][typek])
            
    self.activeana['name']=self.analysisclass.analysis_name
    self.activeana['analysis_fcn_version']=self.analysisclass.analysis_fcn_version
    self.activeana['run_use_option']=self.usek
    self.activeana['plot_parameters']=self.analysisclass.plotparams
    plateidsliststr=','.join('%d' %i for i in sorted(list(set([d['plate_id'] for d in self.analysisclass.fomdlist]))))
    self.activeana['plate_ids']="''" if len(plateidsliststr)==0 else plateidsliststr
    le, desc=self.paramsdict_le_dflt['description']
    s=str(le.text()).strip()
    if not (len(s)==0 or 'null' in s):
        desc=s
    desc+='; run '+','.join('%d' %i for i in sorted(list(set([d['runint'] for d in self.analysisclass.fomdlist]))))
    desc+='; plate_id '+plateidsliststr
    self.activeana['description']=desc
    le.setText('')#clear description to clear any user-entered comment
    if len(self.analysisclass.params)>0:
        self.activeana['parameters']={}
    for k, v in self.analysisclass.params.iteritems():
        if isinstance(v, dict):
            self.activeana['parameters'][k]={}
            for k2, v2 in v.iteritems():
                self.activeana['parameters'][k][v2]=str(v2)
        else:
            self.activeana['parameters'][k]=str(v)
    
    #the A,B,C,D order is editable as a analysisclass paramete and if it is not the nontrivial case, bump it up to an ana__ key for ease in finding in visualization
    if 'parameters' in self.activeana.keys() and 'platemap_comp4plot_keylist' in self.activeana['parameters'].keys() and self.activeana['parameters']['platemap_comp4plot_keylist']!='A,B,C,D':
        self.activeana['platemap_comp4plot_keylist']=self.activeana['parameters']['platemap_comp4plot_keylist']

    gentype=self.analysisclass.getgeneraltype()
    if 'process_fom' in gentype:
        if 'from_file' in gentype:
            self.activeana['process_fom_from_file_paths']=','.join(sorted(list(set([compareprependpath(FOMPROCESSFOLDERS, p) for p in self.analysisclass.filter_path__runint.values()]))))
    else:
        self.activeana['technique']=self.techk
    self.activeana['analysis_general_type']=gentype


    self.fomdlist=self.analysisclass.fomdlist
    self.filedlist=self.analysisclass.filedlist
    self.fomnames=self.analysisclass.fomnames
    self.csvheaderdict=self.analysisclass.csvheaderdict
    self.primarycsvpath=self.analysisclass.primarycsvpath

    return False#false means no error
