import numpy, pickle, shutil
from matplotlib.ticker import FuncFormatter
import matplotlib.colors as colors
from fcns_math import *
import time
import zipfile

def myexpformat(x, pos):
    for ndigs in range(5):
        lab=(('%.'+'%d' %ndigs+'e') %x).replace('e+0','e').replace('e+','e').replace('e0','').replace('e-0','e-')
        if eval(lab)==x:
            return lab
    return lab
ExpTickLabels=FuncFormatter(myexpformat)

are_paths_equivalent=lambda path1, path2:os.path.normcase(os.path.abspath(path1))==os.path.normcase(os.path.abspath(path2))


def attemptnumericconversion(s, fcn=float):
    try:
        return fcn(s)
    except ValueError:
        return s

def attemptnumericconversion_tryintfloat(s):
    try:
        return ('.' in s and (float(s),) or (int(s),))[0]
    except ValueError:
        return s
#    if (s.replace('.', '', 1).replace('e', '', 1).replace('+', '', 1).replace('-', '', 1)).isalnum():
#        try:
#            return myeval(s)
#        except:
#            pass
#    return s

def getsamplenum_fn(fn):
    if fn.startswith('Sample'):
        return int(fn.partition('Sample')[2].partition('_')[0])
    elif fn[0].isdigit():
        return int(fn.partition('_')[0])
    else:
        print 'problem extracting sample number from ', fn
    return 0

def writecsv_smpfomd(p, csvfilstr,headerdict=dict([('csv_version', '1')])):
    headerlines=['#%s = %s' %(k,v) for k,v in headerdict.iteritems()]
    csvfilstr='\n'.join(headerlines+[csvfilstr])

    with open(p, mode='w') as f:
        f.write(csvfilstr)
    
def readechemtxt(path, mtime_path_fcn=None, lines=None):
    if lines is None:
        try:#need to sometimes try twice so might as well try 3 times
            f=open(path, mode='r')
        except:
            try:
                f=open(path, mode='r')
            except:
                f=open(path, mode='r')
        lines=f.readlines()
        f.close()
    d={}
    z=[]
    for count, l in enumerate(lines):
        if l.startswith('%'):
            a, b, c=l.strip('%').strip().partition('=')
            a=a.strip()
            c=c.strip()
            if a=='elements' or a=='column_headings' or a=='compositions':
                val=[]
                while len(c)>0:
                    b, garb, c=c.strip().replace('\\t', '\t').partition('\t')
                    val+=[b]
                if a=='compositions':
                    val=[attemptnumericconversion(v) for v in val]
                    try:
                        val=numpy.float32(val)
                        if numpy.any(numpy.isnan(val)):
                            raise
                    except:
                        val=numpy.ones(len(val), dtype='float32')/len(val)
                        pass
            elif a=='x' or a=='y':
                val=attemptnumericconversion(c.replace('mm', '').strip())
            else:
                val=attemptnumericconversion(c)
            d[a]=val
        else:
            break
    if len(lines[count:])==0:
        return {}
    try:
        z=[map(float, l.strip().replace('\\t', '\t').split('\t')) for l in lines[count:] if len(l.strip())>0]
    except:
        print l
        print '\t' in l
        print l.split('\t')
        print map(float, l.split('\t')) 
        raise
    for k, arr in zip(d['column_headings'], numpy.float32(z).T):
        d[k]=arr
    d['path']=path
    if not mtime_path_fcn is None:
        d['mtime']=mtime_path_fcn(path)
    return d

def convertstrvalstonum_nesteddict(expfiledict):
    def nestednumconvert(d):
        for k, v in d.iteritems():
            if isinstance(v, str):
                d[k]=attemptnumericconversion_tryintfloat(v)
            elif isinstance(v, dict):
                nestednumconvert(v)
    nestednumconvert(expfiledict)

def convertfilekeystolist(expfiledict):
    for k, rund in expfiledict.iteritems():
        if not k.startswith('run__'):
            continue
        for k2, techd in rund.iteritems():
            if not k2.startswith('files_technique__'):
                continue
            for k3, typed in techd.iteritems():
                for fn, keystr in typed.iteritems():
                    keys=keystr.partition(';')[2].split(',')
                    keys=[kv.strip() for kv in keys]
                    expfiledict[k][k2][k3][fn]=keys
        
def readbinary_selinds(p, nkeys, keyinds=None):
    with open(p, mode='rb') as f:
        b=numpy.fromfile(f,dtype='float32')
    b=b.reshape((nkeys,len(b)//nkeys))

    if keyinds is None:
        return b
    else:
        return b[keyinds]

def saverawdat_expfiledict(expfiledict, folder):
    datastruct_expfiledict(expfiledict, savefolder=folder)
def datastruct_expfiledict(expfiledict, savefolder=None):
    convertstrvalstonum_nesteddict(expfiledict)
    if not savefolder is None:
        openfnc=lambda fn:open(os.path.join(savefolder, fn+'.dat'), mode='wb')
        #savefcn=lambda d, keys:numpy.float64([d[k] for k in keys]).tofile(f)
    
    readfcn=readdatafiledict[expfiledict['exp_type']]    
    for k, rund in expfiledict.iteritems():
        if not k.startswith('run__'):
            continue
        runp=rund['run_path']
        
        zipbool=runp.endswith('.zip')
        if zipbool:
            archive=zipfile.ZipFile(runp, 'r')
            zipopenfcn=lambda fn:archive.open(fn, 'r')#rund['rcp_file'].partition('/')[0]+'/'+
        for k2, techd in rund.iteritems():
            if not k2.startswith('files_technique__'):
                continue
            for k3, typed in techd.iteritems():
                for fn, keystr in typed.iteritems():
                    if zipbool:
                        with zipopenfcn(fn) as f:
                            lines=f.readlines()
                    else:
                        p=os.path.join(runp, fn)
                        with open(p,'r') as f:
                            lines=f.readlines()
                    if savefolder is None:
                        expfiledict[k][k2][k3][fn]=readfcn(os.path.splitext(fn), lines)
                    else:
                        keys=keystr.partition(';')[2].split(',')
                        keys=[kv.strip() for kv in keys]
                        filed=readfcn(os.path.splitext(fn), lines)
                        x=numpy.float32([filed[kv] for kv in keys])
                        with openfnc(fn) as f:
                            x.tofile(f)
                            #savefcn(filed, keys)
                    
        if zipbool:
            archive.close()

    return expfiledict

def saveinterdata(p, interd, keys=None):
    if keys is None:
        keys=sorted(interd.keys())
    with open(p, mode='wb') as f:
        x=numpy.float32([interd[kv] for kv in keys])
        x.tofile(f)
    return keys
def saveexp_txt_dat(expfilestr, expfiledict, erroruifcn=None, saverawdat=True):
    #TODO: write routine to auto generate user path
    #savep='C:/Users/Gregoire/Documents/PythonCode/JCAP/JCAPCreateExperimentAndFOM/exp/sampleexp.exp'
    savep=None
    
    if savep is None or not os.path.isdir(os.path.split(savep)[0]):
        if erroruifcn is None:
            return
        savep=erroruifcn('bad autosave path')
        if len(savep)==0:
            return
    
    folder=os.path.split(savep)[0]

    #saveexpfiledict=datastruct_expfiledict(copy.deepcopy(expfiledict))    
    saveexpfiledict=copy.deepcopy(expfiledict)
    if saverawdat:
        #folder=os.path.join(os.path.split(savep)[0], 'raw_binary')
        folder=os.path.split(savep)[0]
        if os.path.isdir(folder):
            for fn in os.listdir(folder):
                os.remove(os.path.join(folder, fn))#cannot overwrite files because filename deduplication may be different from previous save
        else:
            os.mkdir(folder)
        saverawdat_expfiledict(saveexpfiledict, folder)
    else:
        convertstrvalstonum_nesteddict(saveexpfiledict)
    convertfilekeystolist(saveexpfiledict)
    
    with open(savep, mode='w') as f:
        f.write(expfilestr)
        
    dsavep=savep.replace('.exp', '.pck')
    with open(dsavep,'wb') as f:
        pickle.dump(saveexpfiledict, f)
    return saveexpfiledict, dsavep
        
def getarrfromkey(dlist, key):
    return numpy.array([d[key] for d in dlist])

def col_string(s):
    s=s.strip()
    if ('(' in s) and (')' in s):
        try:
            s=eval(s)
        except:
            return None
    cc=colors.ColorConverter()
    return cc.to_rgb(s)

def readsingleplatemaptxt(p, returnfiducials=False,  erroruifcn=None):
    try:
        f=open(p, mode='r')
    except:
        if erroruifcn is None:
            return []
        p=erroruifcn('bad autosave path')
        if len(p)==0:
            return []
        f=open(p, mode='r')

    ls=f.readlines()
    f.close()
    if returnfiducials:
        s=ls[0].partition('=')[2].partition('mm')[0].strip()
        if not ',' in s[s.find('('):s.find(')')]: #needed because sometimes x,y in fiducials is comma delim and sometimes not
            print 'WARNING: commas inserted into fiducials line to adhere to format.'
            print s
            s=s.replace('(   ', '(  ',).replace('(  ', '( ',).replace('( ', '(',).replace('   )', '  )',).replace(',  ', ',',).replace(', ', ',',).replace('  )', ' )',).replace(' )', ')',).replace('   ', ',',).replace('  ', ',',).replace(' ', ',',)
            print s
        fid=eval('[%s]' %s)
        fid=numpy.array(fid)
    for count, l in enumerate(ls):
        if not l.startswith('%'):
            break
    keys=ls[count-1][1:].split(',')
    keys=[(k.partition('(')[0]).strip() for k in keys]
    dlist=[]
    for l in ls[count:]:
        sl=l.split(',')
        d=dict([(k, myeval(s.strip())) for k, s in zip(keys, sl)])
        dlist+=[d]
    if returnfiducials:
        return dlist, fid
    return dlist

def getplatemappath_plateid(plateidstr, erroruifcn=None):
    #TODO write p in terms of plateidstr
    #p=os.path.join(os.getcwd(), '0037-04-0730-mp.txt')
    p='sdf'
    if (not os.path.isfile(p)) and not erroruifcn is None:
        p=erroruifcn('')
    return p

def readrcpfrommultipleruns(pathlist):
    techset=set([])
    typeset=set([])
    rcpdlist=[]
    for p in pathlist:
        if p.endswith('.zip'):
            rcpfn, lines=rcplines_zip(p)
        elif os.path.isdir(p):
            rcpfn, lines=rcplines_folder(p)
        elif p.endswith('.rcp'):
            with open(p, mode='r') as f:
                lines=f.readlines()
            rcpfn=os.path.split(p)[1]
        if len(lines)==0:
            continue
        rcpd=readrcplines(lines)
        techset=techset.union(set(rcpd['techlist']))
        typeset=typeset.union(set(rcpd['typelist']))
        rcpd['run_path']=p
        rcpd['rcp_file']=rcpfn
        if len(rcpd['filenamedlist'])==0:
            rcpd['plateidstr']=''
        else:
            rcpd['plateidstr']=rcpd['filenamedlist'][0]['plate']
        rcpdlist+=[rcpd]
    return techset, typeset, rcpdlist

def rcplines_folder(foldp):
    fns=[fn for fn in os.listdir(foldp) if fn.endswith('.rcp')]
    if len(fns)!=1:
        return []
    rcpfn=fns[0]
    p=os.path.join(foldp, rcpfn)
    f=open(p, mode='r')
    lines=f.readlines()
    f.close()
    return rcpfn, lines
    
def rcplines_zip(zipp):
    archive = zipfile.ZipFile(zipp, 'r')
    fns=[fn for fn in archive.namelist() if fn.endswith('.rcp')]
    if len(fns)!=1:
        return []
    rcpfn=fns[0]
    f=archive.open(rcpfn)
    lines=f.readlines()
    archive.close()
    return rcpfn, lines

indent='    '
getnumspaces=lambda a:len(a) - len(a.lstrip(' '))
def createnestparamtup(lines):
    ln=str(lines.pop(0).rstrip()).replace(chr(181), 'micro')
    
    numspaces=getnumspaces(ln)
    subl=[]
# this is supposed to fix the situation where an indented comment wasn't indetned but somehow duplicated the next line at 2 different indents
#    if ln.count(':')==2 and not 'path' in ln:
#        print getnumspaces(lines[0])>numspaces
#        ln, cln, newline=ln.partition(':')
#        ln+=cln
#        newline=' '*numspaces+indent+newline
#        print ln
#        print newline
#        print lines[0]
#        lines=[newline]+lines

    while len(lines)>0 and getnumspaces(lines[0])>numspaces:
        tu=createnestparamtup(lines)
        subl+=[tu]
    
    return (ln.lstrip(' '), subl)
def readrcp(p):
    f=open(p, mode='r')
    lines=f.readlines()
    f.close()
    return readrcplines(lines)
def readrcplines(lines):
    rcptuplist=[]
    lines=[l for l in lines if len(l.strip())>0]
    while len(lines)>0:
        rcptuplist+=[createnestparamtup(lines)]
    return interpretrcptuplist(rcptuplist)
    
def interpretrcptuplist(rcptuplist):
    rcptuplist_fns=[(i0, tup) for i0, tup in enumerate(rcptuplist) if tup[0].startswith('files_technique__')]
    

    plateidstrtemp=[tup[0].partition(':')[2].strip() for tup in rcptuplist if tup[0].startswith('plate_id')]
    if len(plateidstrtemp)!=1:
        print 'ERROR FINDING PLATE ID IN .rcp FILE. ', plateidstrtemp
        raise 'ERROR FINDING PLATE ID IN .rcp FILE.'
    plateidstr=plateidstrtemp[0]
    
    

    #sort files assumes that filenames are 2-deep nested by technieuqwe and then by filetype. technique labels must begin with files_technique__ but type keys can be anything
    techlist=[tup[0].partition('files_technique__')[2].partition(':')[0] for i0, tup in rcptuplist_fns]

    
#    filenametuplist=[]
#    for techstr, typfnslist in rcptuplist_fns:
#        tech=techstr.partition('files_technique__')[2].partition(':')[0]
#        for typestr, tuplist in typfnslist:
#            if ':' in typestr:
#                tp=typestr.partition(':')[0]
#                for fn, garb in tuplist:
#                    if fn.partition('Sample')[2].partition('_')[0].isdigit():
#                        filenametuplist+=[(tech, tp, int(fn.partition('Sample')[2].partition('_')[0]), fn)]
    makefndict=lambda pl, te, ty, sm, fn, i0, i1, i2:dict([('plate', pl), ('tech', te), ('type', ty), ('smp', sm), ('fn', fn), \
            ('tuplistinds', (i0, i1, i2)), \
            ('inexp', set([])), ('previnexp', set([]))])#inexp is set of data uses ("run_type" ) in which this file is used
    filenamedlist=[\
        makefndict(plateidstr, techstr.partition('files_technique__')[2].partition(':')[0], typestr.partition(':')[0], getsamplenum_fn(fn), fn, i0, i1, i2)\
        for i0, (techstr, typfnslist) in rcptuplist_fns\
        for i1, (typestr, tuplist) in enumerate(typfnslist)\
        for i2, (fn, garb) in enumerate(tuplist)\
        if ':' in typestr and (fn.startswith('Sample') or fn[0].isdigit())\
        ]


    typelist=[d['type'] for d in filenamedlist]
    typelist=list(set(typelist))
    if 'pstat_files' in typelist:
        temp=typelist.pop(typelist.index('pstat_files'))
        typelist=[temp]+typelist
        
    return dict([('plateidstr', plateidstr), ('rcptuplist', rcptuplist), ('techlist', techlist),('typelist', typelist), ('filenamedlist', filenamedlist)])
#rcpd=readrcp('20150422.145113.done/20150422.145113.rcp')
#rcpdlist=readrcpfrommultipleruns(['20150422.145113.done.zip', 'runfolder2'])

def partitionlineitem(ln):
    a, b, c=ln.strip().partition(':')
    return (a.strip(), c.strip())

def createdict_tup(nam_listtup):
    k_vtup=partitionlineitem(nam_listtup[0])
    if len(nam_listtup[1])==0:
        return k_vtup
    d=dict([createdict_tup(v) for v in nam_listtup[1]])
    return (k_vtup[0], d)
        
def readexpasdict(p, includerawdata=False):#create both a list of rcpd but also a corresponding 
    if p.endswith('.pck'):
        with open(p, mode='r') as f:
            expfiledict=pickle.load(f)
    elif p.endswith('.exp'):
        with open(p, mode='r') as f:
            lines=f.readlines()
        lines=[l for l in lines if len(l.strip())>0]
        exptuplist=[]
        while len(lines)>0:
            exptuplist+=[createnestparamtup(lines)]
        expfiledict=dict(\
        [createdict_tup(tup) for tup in exptuplist])
        
        #these tiems would have been performed before saving .pck so only perform for .exp
        convertstrvalstonum_nesteddict(expfiledict)
        convertfilekeystolist(expfiledict)
        
    else:
        return None
    if includerawdata:
        expfiledict=datastruct_expfiledict(expfiledict)
        
    return expfiledict

def readexpasrcpdlist(p, only_expparamstuplist=False):#create both a list of rcpd but also a corresponding 
    with open(p, mode='r') as f:
        lines=f.readlines()
    lines=[l for l in lines if len(l.strip())>0]
    exptuplist=[]
    while len(lines)>0:
        exptuplist+=[createnestparamtup(lines)]
    expparamstuplist=[tup for tup in exptuplist if not tup[0].startswith('run__')]
    if only_expparamstuplist:
        return expparamstuplist
        
    expruntuplists=[tup[1] for tup in exptuplist if tup[0].startswith('run__')]#loose the run__name but keep the things nested in there
    techset=set([])
    typeset=set([])
    rcpdlist=[]
    expdlist_use={}
    for count, tuplist in enumerate(expruntuplists):
        rcptuplist=[]
        expleveltuplist=[]
        for tup in tuplist:
            if tup[0].startswith('files_technique__'):
                rcptuplist+=[tup]
            elif tup[0].startswith('parameters:'):
                rcptuplist+=tup[1]
            else:
                expleveltuplist+=[tup]
            
        rcpd=interpretrcptuplist(rcptuplist)
        techset=techset.union(set(rcpd['techlist']))
        typeset=typeset.union(set(rcpd['typelist']))
        for k in ['run_path', 'rcp_file', 'run_use']:
            kl=[tup[0] for tup in expleveltuplist if tup[0].startswith(k)]
            if len(kl)!=1:
                print 'ERROR finding %s in a run in %s' %(k, p)
            v=kl[0].partition(':')[2].strip()
            if k=='run_use':
                run_use=v
            else:
                rcpd[k]=v
        if len(rcpd['filenamedlist'])==0:
            rcpd['plateidstr']=''
        else:
            rcpd['plateidstr']=rcpd['filenamedlist'][0]['plate']
        rcpd['filenamedlist']=[dict(d, inexp=set([run_use]), previnexp=set([run_use])) for d in rcpd['filenamedlist']]
        rcpdlist+=[rcpd]
        if run_use in expdlist_use.keys():
            expdlist_use[run_use]+=[rcpd]
        else:
            expdlist_use[run_use]=[rcpd]
        expdlist_use[run_use][-1]['rcpdlistind']=count
    return techset, typeset, rcpdlist, expparamstuplist, expdlist_use




def smp_dict_generaltxt(path, delim='\t', returnsmp=True, addparams=False, lines=None): # can have raw data files with UV-vis or ECHE styles or a fom file with column headings as first line, in which case smp=None
    if returnsmp:
        smp=None
        fn=os.path.split(path)[1]
        if fn.startswith('Sample'):
            s=fn.partition('Sample')[2].partition('_')[0]
            try:
                smp=eval(s)
            except:
                smp=None
        if smp is None:
            smp=getsamplefromheader(path=path)
    #    if smp is None:
    #        return None, {}
    if lines is None:
        f=open(path, mode='r')
        lines=f.readlines()
        f.close()
    if len(lines)==0:
        return None, {}
    if lines[0].startswith('%'):#for echem data files
        for count, l in enumerate(lines):
            if l.startswith('%column_headings='):
                chs=l.partition('%column_headings=')[2]
                firstdatalineind=count+1
                break
    elif lines[0][0].isdigit():#for uv-vis data files
        numheadlines=lines[0].rpartition(delim)[2].strip()
        try:
            numheadlines=eval(numheadlines)
        except:
            return None, {}
        chs=lines[numheadlines+1].strip()
        firstdatalineind=numheadlines+2
    elif lines[1][0].isdigit():#fom files or any file with first line headings and second line starts values
        chs=lines[0].strip()
        firstdatalineind=1
    elif lines[0][0]=='#':#for csv or anything with header noted by #
        for count, l in enumerate(lines):
            if l[0]!='#':
                break
        if lines[count][0].isdigit():# if column headings in last header line
            chs=lines[count-1][1:].strip()
            firstdatalineind=count
        else:#if column headings line doesn't start with #
            if not lines[count+1][0].isdigit():#but if the next line isn't data then abort
                return None, {}
            firstdatalineind=count+1
            chs=lines[count].strip()
    else:
        if returnsmp:
            return None, {}
        else:
            return {}
    
    
    d={}
    z=[]
    column_headings=chs.split(delim)
    column_headings=[s.strip() for s in column_headings]
    skipcols=['Date', 'Time']
    skipinds=[i for i, col in enumerate(column_headings) if col in skipcols]
    column_headings=[x for i, x in enumerate(column_headings) if i not in skipinds]
    myfloatfcn=lambda s:(len(s.strip())==0 and (float('NaN'),) or (float(s.strip()),))[0]#this turns emtpy string into NaN. given the .strip this only "works" if delimeter is not whitespace, e.g. csv
    z=[map(myfloatfcn, [x for i, x in enumerate(l.split(delim)) if i not in skipinds]) for l in lines[firstdatalineind:]]
    for k, arr in zip(column_headings, numpy.float32(z).T):
        d[k]=arr
    
    if addparams:
        for l in lines[:firstdatalineind]:
            if '=' in l:
                c='='
            elif ':' in l:
                c=':'
            else:
                continue
            k, garb, v=l.partition(c)
            d[k.strip().strip('%')]=attemptnumericconversion_tryintfloat(v.strip())
            
    if returnsmp:
        return smp, d
    else:
        return d

def applyfcn_txtfnlist_run(fcn, runp, fns, readbytes=1000):
    zipbool=runp.endswith('.zip')
    if zipbool:
        archive=zipfile.ZipFile(runp, 'r')
        zipopenfcn=lambda fn:archive.open(fn, 'r')#rund['rcp_file'].partition('/')[0]+'/'+
    returnlist=[]
    for fn in fns:
        if zipbool:
            with zipopenfcn(fn) as f:
                filestr=f.read(readbytes)
        else:
            p=os.path.join(runp, fn)
            with open(p,'r') as f:
                filestr=f.read(readbytes)
        returnlist+=[fcn(filestr=filestr)]
    if zipbool:
        archive.close()
    return returnlist
    
def gettimefromheader(**kwargs):#use either path or filestr as kwargument path=None, filestr=''
    trylist=getheadattrs(searchstrs=['Epoch', 'Date and Time'], **kwargs)
    if not trylist[0] is None:
        if isinstance(trylist[0], float):
            return trylist[0]
        else:
            return None
    if not trylist[1] is None:
        try:
            t=time.strptime(trylist[1],'%Y-%m-%d %H-%M-%S')
            return time.mktime(t)
        except:
            return None
    
def getsamplefromheader(**kwargs):#use either path or filestr as kwargument path=None, filestr=''
    trylist=getheadattrs(searchstrs=['Sample', 'Sample No', 'sample_no'], **kwargs)
    for v in trylist:
        if not v is None:
            return v
    return None
    
def getheadattrs(path=None, filestr='', searchstrs=['Sample', 'Sample No', 'sample_no'], readbytes=1000):
    if filestr is None:
        with open(path, mode='r') as f:
            filestr=f.read(readbytes)
    ret=[]
    for ss in searchstrs:
        if not ss in filestr:
            ret+=[None]
            continue
        vs=filestr.partition(ss)[2].partition('\n')[0].strip().strip(':').strip('=').strip()
        try:
            ret+=[eval(vs)]
        except:
            ret+=[None]
    return ret

readdatafiledict=dict([\
    ('eche', lambda ext, lines:ext=='.txt' and readechemtxt('', lines=lines) or smp_dict_generaltxt('', lines=lines, addparams=True,returnsmp=False)), \
    ('uvis', lambda ext, lines:smp_dict_generaltxt('', lines=lines, addparams=True,returnsmp=False)), \
    ])

def getanadefaultfolder(erroruifcn=None):
    #TODO: createdefault path
    folder='//htejcap.caltech.edu/share/home/users/hte/demo_proto/analysis/eche/temp'
    try:
        if not os.path.isdir(folder):
            os.mkdir(folder)
        return folder
    except:
        print folder
        if erroruifcn is None:
            return ''
        return erroruifcn('')
            
def saveana_tempfolder(anafilestr, srcfolder, erroruifcn=None, skipana=True, plateidstr=''):
    #TODO: write routine to auto generate user path
    #savep='C:/Users/Gregoire/Documents/PythonCode/JCAP/JCAPCreateExperimentAndFOM/exp/sampleexp.exp'
    savefolder=None
    try:
        if not os.path.isdir(savefolder):
            os.mkdir(savefolder)
    except:
        if erroruifcn is None:
            return
        savefolder=erroruifcn('bad autosave folder - select/create a folder to save Ana')
        if len(savefolder)==0:
            return
    if '.ana' in srcfolder and os.path.normpath(os.path.split(srcfolder)[0])==os.path.normpath(os.path.split(savefolder)[0]):
        try:
            os.rename(srcfolder, savefolder)
            return
        except:
            print 'Error renaming ', srcfolder
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)
    for fn in os.listdir(srcfolder):
        if skipana and fn.endswith('.ana'):
            continue
        shutil.copy(os.path.join(srcfolder, fn), os.path.join(savefolder, fn))
    savep=os.path.join(savefolder, '%s_%s.ana' %(time.strftime('%Y%m%d.%H%M%S'), plateidstr))
    with open(savep, mode='w') as f:
        f.write(anafilestr)
    
#p='//htejcap.caltech.edu/share/home/users/hte/demo_proto/experiment/eche/1/eche.pck'
#with open(p,mode='rb') as f:
#    d=pickle.load(f)
#folder='//htejcap.caltech.edu/share/home/users/hte/demo_proto/experiment/eche/1/raw_binary'
#keystr=d['run__1']['files_technique__CA6']['spectrum_files']['Sample765_x-46_y-42_Ni0Fe30Co0Ce20_CA6_TRANS0_20150422.145114.5.opt']
#keys=keystr.split(',')
#keys=[kv.strip() for kv in keys]
#                        
#saverawdat_expfiledict(d, folder)
#
#p='//htejcap.caltech.edu/share/home/users/hte/demo_proto/experiment/eche/1/raw_binary/Sample765_x-46_y-42_Ni0Fe30Co0Ce20_CA6_TRANS0_20150422.145114.5.opt.dat'
#with open(p, mode='rb') as f:
#    x=numpy.fromfile(f, dtype='float64')
#x=x.reshape((2, 1024))
#
#datastruct_expfiledict(d)
#datad=d['run__1']['files_technique__CA6']['spectrum_files']['Sample765_x-46_y-42_Ni0Fe30Co0Ce20_CA6_TRANS0_20150422.145114.5.opt']
#x2=numpy.float64([datad[k] for k in keys])
