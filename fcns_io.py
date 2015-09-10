import numpy, pickle, shutil
from matplotlib.ticker import FuncFormatter
import matplotlib.colors as colors
from fcns_math import *
from fcns_ui import mygetopenfile
import time
import zipfile
from operator import itemgetter
from DBPaths import *
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

def openexpanafile(parent, exp=True, markstr=None):#TODO support getting exp and ana from .zip
    if exp:
        fold0, fold1=EXPFOLDER_J, EXPFOLDER_K
        ext='.exp'
        if markstr is None:
            markstr='open EXP'
    else:
        fold0, fold1=ANAFOLDER_J, ANAFOLDER_K
        ext='.ana'
        if markstr is None:
            markstr='open ANA'
    if not os.path.isdir(fold0):
        fold0=fold1
    return mygetopenfile(parent, xpath=fold0, markstr=markstr, filename=ext )

def removefiles(folder, fns):
    for fn in fns:
        os.remove(os.path.join(folder, fn))

def getsamplenum_fnline(fnline):
    if fnline.count(';')==2:#the optional sample_no is after the 2nd ;
        return int(fnline.rpartition(';')[2].strip())
    else:
        return getsamplenum_fn(fnline)
def getsamplenum_fn(fn):
    if fn.startswith('Sample'):
        return int(fn.partition('Sample')[2].partition('_')[0])
    elif fn[0].isdigit():
        return int(fn.partition('_')[0])
    else:
        print 'problem extracting sample number from ', fn
    return 0

def writecsv_smpfomd(p, csvfilstr,headerdict=dict([('csv_version', '1')]), replaceheader=False):#replaceheader is to the headerdict portino of the header and replace with headdict. csvfilestr is ignored in this case
    if replaceheader:
        with open(p, mode='r') as f:
            lines=f.readlines()
        numheaddictlines=int(lines[0].split('\t')[-1].strip())
        csvfilstr=''.join(lines[numheaddictlines+1:])
    headerstr=strrep_filedict(headerdict)
    numheaddictlines=headerstr.count('\n')+1
    numcols=csvfilstr.partition('\n')[0].count(',')+1
    firstline='%d\t%d\t%d\t%d' %(1, numcols, csvfilstr.count('\n'), numheaddictlines)
    csvfilstr='%s\n%s\n%s' %(firstline, headerstr, csvfilstr)
    with open(p, mode='w') as f:
        f.write(csvfilstr)
    return numheaddictlines+2


#p='//htejcap.caltech.edu/share/home/users/hte/demo_proto/experiment/eche/1/Sample236_x-24_y-70_Ni0Fe10Co0Ce90_CA2.txt'
#filed={}
#filed['file_type']= 'eche_gamry_txt_file'
#filed['keys']= ['t(s)', 'Ewe(V)', 'Ach(V)', 'I(A)', 'Toggle']
#filed['num_data_rows']= '250'
#filed['num_header_lines']= '15'
#filed['sample_no']=236
#selcolinds=[4]

def getarrs_filed(p, filed, selcolinds=None, trydat=True):
    if trydat:
        pdat=p+'.dat'
        if os.path.isfile(pdat):
            return readbinary_selinds(pdat, len(filed['keys']), keyinds=selcolinds)
    if not os.path.isfile(p):
        return None
    return readtxt_selectcolumns(p, selcolinds=selcolinds, delim=None, num_header_lines=filed['num_header_lines'])

def readbinary_selinds(p, nkeys, keyinds=None):
    with open(p, mode='rb') as f:
        b=numpy.fromfile(f,dtype='float32')
    b=b.reshape((nkeys,len(b)//nkeys))

    if keyinds is None:
        return b
    else:
        return b[keyinds]
        
def readtxt_selectcolumns(p, selcolinds=None, delim='\t', num_header_lines=1, floatintstr=float):
    with open(p, mode='r') as f:
        lines=f.readlines()[num_header_lines:]
    if delim is None:
        if lines[0].count(',')>lines[0].count('\t'):
            delim=','
        else:
            delim='\t'
    if selcolinds is None:
        selcolinds=range(lines[0].count(delim)+1)
    if len(selcolinds)==0:
        return numpy.array([[]])
    elif len(selcolinds)==1:
        fcn=lambda ls:(ls[selcolinds[0]],)
    else:
        fcn=itemgetter(*selcolinds)
    z=[map(floatintstr, fcn(l.strip().split(delim))) for l in lines if len(l.strip())>0]
    return numpy.array(z).T

def readcsvdict(p, fileattrd, returnheaderdict=False):
    d={}
    arr=readtxt_selectcolumns(p, delim=',', num_header_lines=fileattrd['num_header_lines'], floatintstr=str)
    for k, a in zip(fileattrd['keys'], arr):
        if '.' in a[0] or 'NaN' in a:
            d[k]=numpy.float32(a)
        else:
            d[k]=numpy.int32(a)
    if not returnheaderdict:
        return d
    with open(p, mode='r') as f:
        lines=[f.readline() for count in range(fileattrd['num_header_lines'])]
        lines=lines[1:-1]
        tuplist=[]
        while len(lines)>0:
            tuplist+=[createnestparamtup(lines)]
            headerdict=dict(\
            [createdict_tup(tup) for tup in tuplist])
    return d, headerdict
    
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
    d['num_header_lines']=count
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
    d['num_data_rows']=len(arr)
    d['path']=path
    if not mtime_path_fcn is None:
        d['mtime']=mtime_path_fcn(path)
    return d

def convertstrvalstonum_nesteddict(expfiledict, skipkeys=['experiment_type', 'analysis_type', 'name', 'description', 'created_by']):
    def nestednumconvert(d):
        for k, v in d.iteritems():
            if isinstance(v, str) and not k in skipkeys:
                d[k]=attemptnumericconversion_tryintfloat(v)
            elif isinstance(v, dict):
                nestednumconvert(v)
    nestednumconvert(expfiledict)


def createfileattrdict(fileattrstr):
    type_keys_heads_rows=fileattrstr.split(';')
    d={}
    d['file_type']=type_keys_heads_rows[0]
    if len(type_keys_heads_rows)==0 or len(type_keys_heads_rows[1].strip())==0:
        #only file_type
        return d
    if len(type_keys_heads_rows)==2:
        #only file_type and sample_no
        d['sample_no']=int(type_keys_heads_rows[-1].strip())
        return d
    keys=type_keys_heads_rows[1].split(',')
    keys=[kv.strip() for kv in keys]
    
    d['keys']=keys
    d['num_header_lines']=int(type_keys_heads_rows[2].strip())
    d['num_data_rows']=int(type_keys_heads_rows[3].strip())
    if len(type_keys_heads_rows)==5:#only valid sample_no str should be in file attributes
        d['sample_no']=int(type_keys_heads_rows[-1].strip())
    else:
        d['sample_no']=0#numpy.nan #this is top keep all sample_no as int instead of mixing int and lofat. this should not be confused with the 0 used as sample_no for uvvis ref spectra because by the time we get here the run_use has already been defined
    return d
def convertfilekeystofiled(exporanafiledict):
    for k, rund in exporanafiledict.iteritems():
        if not (k.startswith('run__') or k.startswith('ana__')):
            continue
        for k2, techd in rund.iteritems():
            if not k2.startswith('files_'):
                continue
            for k3, typed in techd.iteritems():
                for fn, keystr in typed.iteritems():
                    d=createfileattrdict(keystr)
                    exporanafiledict[k][k2][k3][fn]=d
def importfomintoanadict(anafiledict, anafolder):#assumes convertfilekeystofiled already run on anafiledict
    for anak, anad in anafiledict.iteritems():
        if (not anak.startswith('ana__')) or not 'files_multi_run' in anad.keys():
            continue
        for typek, typed in anad['files_multi_run'].keys():
            for fn, fileattrd in typed.iteritems():
                anafiledict[anak]['files_multi_run'][typek][fn]=readcsvdict(os.path.join(anafolder, fn), fileattrd)


def saverawdat_expfiledict(expfiledict, folder):
    datastruct_expfiledict(expfiledict, savefolder=folder)
def datastruct_expfiledict(expfiledict, savefolder=None):#savefolder will save binary arrays and also update the expfiledict to include num header lines and data rows
    if savefolder is None:
        convertstrvalstonum_nesteddict(expfiledict)
    if not savefolder is None:
        openfnc=lambda fn:open(os.path.join(savefolder, fn+'.dat'), mode='wb')
        #savefcn=lambda d, keys:numpy.float64([d[k] for k in keys]).tofile(f)
    
    readfcn=readdatafiledict[expfiledict['experiment_type']]    
    for k, rund in expfiledict.iteritems():
        if not k.startswith('run__'):
            continue
        runp=rund['run_path']

        zipbool=runp.endswith('.zip')
        
        if ((not zipbool) and not os.path.isdir(runp)) or (zipbool and not os.path.isfile(runp)):
            runp=os.path.join(RUNFOLDER, runp.strip('/'))
        
        if zipbool:
            archive=zipfile.ZipFile(runp, 'r')
            zipopenfcn=lambda fn:archive.open(fn, 'r')#rund['rcp_file'].partition('/')[0]+'/'+
        for k2, techd in rund.iteritems():
            if not k2.startswith('files_technique__'):
                continue
            for k3, typed in techd.iteritems():
                for fn, fileattrstr in typed.iteritems():
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
                        keys=fileattrstr.partition(';')[2].partition(';')[0].split(',')
                        keys=[kv.strip() for kv in keys]
                        filed=readfcn(os.path.splitext(fn), lines)
                        x=numpy.float32([filed[kv] for kv in keys])
                        with openfnc(fn) as f:
                            x.tofile(f)
                            #savefcn(filed, keys)***
                        if fileattrstr.count(';')==2:#valid sample_no in place and was there is .rcp file
                            first2attrs, garb, samplestr=fileattrstr.rpartition(';')
                            s='%s;%d;%d;%s' %(first2attrs.strip(), filed['num_header_lines'], filed['num_data_rows'], samplestr.strip())
                        elif fileattrstr.count(';')==4:#full info already , e.g. due to import of line from .exp
                            s=fileattrstr
                        else:#probably read from .rcp and fileattrstr.count(';') is 1 and separates file_type and keys so take that and append headerlines and datarows
                            s='%s;%d;%d' %(fileattrstr.strip(), filed['num_header_lines'], filed['num_data_rows'])
                        expfiledict[k][k2][k3][fn]=s
        if zipbool:
            archive.close()

    return expfiledict

def saveinterdata(p, interd, keys=None, savetxt=True, fmt='%.4e'):
    if keys is None:
        keys=sorted(interd.keys())
    if savetxt:
        arr=numpy.array([[fmt %v for v in interd[kv]] for kv in keys]).T
        s='\t'.join(keys)+'\n'
        s+='\n'.join(['\t'.join(a) for a in arr])
        with open(p, mode='w') as f:
            f.write(s)
    if savetxt or not p.endswith('.dat'):
        p+='.dat'
    with open(p, mode='wb') as f:
        x=numpy.float32([interd[kv] for kv in keys])
        x.tofile(f)
    return keys
    
def buildexppath(p):
    if os.path.isfile(p):
        return p
    p=p.strip(chr(47)).strip(chr(92))
    if os.path.isfile(os.path.join(EXPFOLDER_J, p)):
        return os.path.join(EXPFOLDER_J, p)
    elif os.path.isfile(os.path.join(EXPFOLDER_K, p)):
        return os.path.join(EXPFOLDER_K, p)
    else:
        return p

#don't have a buuild runpath yet, presumably because don't need it if all data is convereted to .dat

def saveexp_txt_dat(expfiledict, erroruifcn=None, saverawdat=True, experiment_type='temp', rundone='.run', runtodonesavep=None, savefolder=None):#for the num headerlines and rows to be written to .exp, saverawdat must be true
    
    if runtodonesavep is None and savefolder is None:
        timename=time.strftime('%Y%m%d.%H%M%S')
        expfiledict['name']=timename
        savep=os.path.join(os.path.join(os.path.join(EXPFOLDER_K, experiment_type), timename+rundone), timename+'.exp')
        
        if savep is None or not os.path.isdir(os.path.split(os.path.split(savep)[0])[0]):
            if erroruifcn is None:
                return
            savep=erroruifcn('bad autosave path')
            if len(savep)==0:
                return
    elif savefolder is None:
        savep=runtodonesavep.replace('.run', '.done').replace('.pck', '.exp')
        os.rename(os.path.split(runtodonesavep)[0], os.path.split(savep)[0])
    else:
        savep=os.path.join(savefolder, os.path.split(savefolder)[1]+'.exp')
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
        saverawdat_expfiledict(saveexpfiledict, folder)#the filename attributes get update here
    
    for rund in saveexpfiledict.itervalues():
        if isinstance(rund, dict) and 'run_path' in rund.keys():
            rp=rund['run_path']
            if os.path.normpath(rp).startswith(os.path.normpath(RUNFOLDER)):
                rp=os.path.normpath(rp)[len(os.path.normpath(RUNFOLDER)):]
            rp=rp.replace(chr(92),chr(47))
            rund['run_path']=rp
            
    expfilestr=strrep_filedict(saveexpfiledict)
    with open(savep, mode='w') as f:
        f.write(expfilestr)
    convertstrvalstonum_nesteddict(saveexpfiledict)
    convertfilekeystofiled(saveexpfiledict)

    dsavep=savep.replace('.exp', '.pck')
    with open(dsavep,'wb') as f:
        pickle.dump(saveexpfiledict, f)
    return saveexpfiledict, dsavep

def strrep_filedict(filedict):
    keys=[k for k in filedict.keys() if 'version' in k]#assume this is not a dictionary
    keys+=sorted([k for k, v in filedict.iteritems() if not isinstance(v, dict) and not 'version' in k])
    sl=[k+': '+str(filedict[k]) for k in keys]
    dkeys=[k for k, v in filedict.iteritems() if isinstance(v, dict) and not '__' in k]
    dkeys+=sorted([k for k, v in filedict.iteritems() if isinstance(v, dict) and '__' in k])
    return ('\n'.join(sl+[strrep_filed_nesting(k, filedict[k]) for k in dkeys])).strip()
        
def strrep_filed_nesting(k, v, indent='    ', indentlevel=0):
    itemstr=indent*indentlevel+k
    if not isinstance(v, dict):
        return itemstr+': '+str(v)
    sl=[itemstr+':']
    keys=[nestk for nestk in v.keys() if 'version' in nestk]#assume this is not a dictionary
    keys+=sorted([nestk for nestk, nestv in v.iteritems() if not isinstance(nestv, dict) and not 'version' in nestk])
    sl+=[indent*(indentlevel+1)+nestk+': '+str(v[nestk]) for nestk in keys]
    dkeys=sorted([nestk for nestk, nestv in v.iteritems() if isinstance(nestv, dict) and not 'files_' in nestk])
    dkeys+=sorted([nestk for nestk, nestv in v.iteritems() if isinstance(nestv, dict) and 'files_' in nestk])
    return '\n'.join(sl+[strrep_filed_nesting(nestk, v[nestk], indentlevel=indentlevel+1) for nestk in dkeys])

    
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
        p=erroruifcn('bad platemap path')
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
    if not 'sample_no' in keys:
        dlist=[dict(d, sample_no=d['Sample']) for d in dlist]
    if returnfiducials:
        return dlist, fid
    return dlist

def getplatemappath_plateid(plateidstr, erroruifcn=None):
    p=''
    fld=os.path.join(PLATEFOLDER, plateidstr)
    if os.path.isdir(fld):
        l=[fn for fn in os.listdir(fld) if fn.endswith('map')]+['None']
        p=os.path.join(fld, l[0])
    if (not os.path.isfile(p)) and not erroruifcn is None:
        p=erroruifcn('', PLATEMAPBACKUP)
    return p
    
def getinfopath_plateid(plateidstr, erroruifcn=None):
    p=''
    fld=os.path.join(PLATEFOLDER, plateidstr)
    if os.path.isdir(fld):
        l=[fn for fn in os.listdir(fld) if fn.endswith('info')]+['None']
        p=os.path.join(fld, l[0])
    if (not os.path.isfile(p)) and not erroruifcn is None:
        p=erroruifcn('', PLATEMAPBACKUP)
    if (not os.path.isfile(p)):
        return None
    return p
    
def getelements_plateidstr(plateidstr):
    p=getinfopath_plateid(plateidstr)
    if p is None:
        return None
    with open(p, mode='r') as f:
        filestr=f.read(1000)
    searchstr='        elements: '
    if not searchstr in filestr:
        return None
    s=filestr.partition(searchstr)[2].partition('\n')[0].strip()
    return s.split(',')
    
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
    ln=str(lines.pop(0).rstrip())
    numspaces=getnumspaces(ln)
    subl=[]
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
#    def fixfiletuplist(filetuplist):
#        
#    for i0, tup in enumerate(rcptuplist):
#        if tup[0].startswith('files_technique__'):
#            rcptuplist[i0]=(tup[0], [(tup2[0], fixfiletuplist(tup2[1])) for tup2 in tup[1]])
            
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
    
    appendsampleifmissing=lambda sm, fnline: ((fnline.count(';')==1 and sm>0) and ('%s;%d' %(fnline, sm),) or (fnline,))[0]#append sample number if it is valid and was missing
    #!!!!! sample_no could be appended here using "appendsampleifmissing(sm, fnline)" but this filedictionary isn't used in creating the .exp. rcptuplist is used so the sample_no will only be in the .exp if it is in the .rcp.   getsamplenum_fnline will get the invalid sample numbers to but those shouldn't be used anywhere.
    makefndict=lambda pl, te, ty, sm, fnline, i0, i1, i2:dict([('plate', pl), ('tech', te), ('type', ty), ('smp', sm), ('fn', fnline), \
            ('tuplistinds', (i0, i1, i2)), \
            ('inexp', set([])), ('previnexp', set([]))])#inexp is set of data uses ("run_type" ) in which this file is used
    filenamedlist=[\
        makefndict(plateidstr, techstr.partition('files_technique__')[2].partition(':')[0], typestr.partition(':')[0], getsamplenum_fnline(fnline), fnline, i0, i1, i2)\
        for i0, (techstr, typfnslist) in rcptuplist_fns\
        for i1, (typestr, tuplist) in enumerate(typfnslist)\
        for i2, (fnline, garb) in enumerate(tuplist)\
        if ':' in typestr and (fnline.startswith('Sample') or fnline[0].isdigit())\
        ] # the " and (fnline.startswith('Sample') or fnline[0].isdigit()" is to validate expected eche and uvis files but should not be necessary moving forward.


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
        
def readexpasdict(p, includerawdata=False, erroruifcn=None):#create both a list of rcpd but also a corresponding 
    if not ((p.endswith('exp') or p.endswith('pck')) and os.path.exists(p)):
        if erroruifcn is None:
            return {}
        p=erroruifcn('select exp file')
        if len(p)==0:
            return {}
        
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
        convertfilekeystofiled(expfiledict)
        
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




def smp_dict_generaltxt(path, delim='\t', returnsmp=True, addparams=False, lines=None, returnonlyattrdict=False): # can have raw data files with UV-vis or ECHE styles or a fom file with column headings as first line, in which case smp=None
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
    lines=[l for l in lines if len(l)>0]
    if delim is None or len(delim)==0:
        if lines[-1].count(',')>lines[-1].count('\t'):
            delim=','
        else:
            delim='\t'
    if len(lines)==0:
        if returnsmp:
            return None, {}
        else:
            return {}
    if lines[0].startswith('%'):#for echem data files
        for count, l in enumerate(lines):
            if l.startswith('%column_headings='):
                chs=l.partition('%column_headings=')[2]
                firstdatalineind=count+1
                break
    elif lines[0][0].isdigit():#for uv-vis data files (and for csv also so use \t
        numheadlines=lines[0].rpartition('\t')[2].strip()
        try:
            numheadlines=eval(numheadlines)
        except:
            if returnsmp:
                return None, {}
            else:
                return {}
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
                if returnsmp:
                    return None, {}
                else:
                    return {}
            firstdatalineind=count+1
            chs=lines[count].strip()
    else:
        if returnsmp:
            return None, {}
        else:
            return {}
    
    column_headings=chs.split(delim)
    column_headings=[s.strip() for s in column_headings]
    
    if returnonlyattrdict:
        d={}
        d['keys']=column_headings
        d['num_header_lines']=firstdatalineind
        d['num_data_rows']=len(lines)-firstdatalineind
        if smp is None:
            d['sample_no']=numpy.nan
        else:
            d['sample_no']=smp
        return smp, d
    d={}
    z=[]
    
    skipcols=['Date', 'Time']
    skipinds=[i for i, col in enumerate(column_headings) if col in skipcols]
    column_headings=[x for i, x in enumerate(column_headings) if i not in skipinds]
    myfloatfcn=lambda s:(len(s.strip())==0 and (float('NaN'),) or (float(s.strip()),))[0]#this turns emtpy string into NaN. given the .strip this only "works" if delimeter is not whitespace, e.g. csv
    z=[map(myfloatfcn, [x for i, x in enumerate(l.split(delim)) if i not in skipinds]) for l in lines[firstdatalineind:]]
    for k, arr in zip(column_headings, numpy.float32(z).T):
        d[k]=arr
    
    if addparams:
        d['num_header_lines']=firstdatalineind
        d['num_data_rows']=len(arr)
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
    
    if ((not zipbool) and not os.path.isdir(runp)) or (zipbool and not os.path.isfile(runp)):
        runp=os.path.join(RUNFOLDER, runp.strip('/'))

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
    folder='//htejcap.caltech.edu/share/home/users/hte/demo_proto/analysis/temp'
    
    timename=time.strftime('%Y%m%d.%H%M%S')
    
    folder=os.path.join(os.path.join(ANAFOLDER_K, 'temp'), timename+'.run')
    
    try:
        if not os.path.isdir(folder):
            os.mkdir(folder)
        return folder
    except:
        print folder
        if erroruifcn is None:
            return ''
        return erroruifcn('')
            
def saveana_tempfolder(anafilestr, srcfolder, erroruifcn=None, skipana=True, anadict=None, analysis_type='temp', savefolder=None):
    
    if srcfolder.endswith('.run') and savefolder is None:
        rootfold, typefold=os.path.split(os.path.split(srcfolder)[0])
        if typefold=='temp':
            savefolder=os.path.join(os.path.join(rootfold, analysis_type), os.path.split(srcfolder)[1][:-3]+'done')
        else:
            savefolder=srcfolder[:-3]+'done'#replace run with done
        timename=os.path.split(srcfolder)[1][:-4]#remove .run
    elif savefolder is None:
        timename=time.strftime('%Y%m%d.%H%M%S')
        savefolder=os.path.join(os.path.join(ANAFOLDER_K, analysis_type), timename+'.done')
    else:
        timename=os.path.split(savefolder)[1]
    try:
        if not os.path.isdir(savefolder):
            os.mkdir(savefolder)
    except:
        if erroruifcn is None:
            return
        savefolder=erroruifcn('bad autosave folder - select/create a folder to save Ana')
        if len(savefolder)==0:
            return
#    if '.ana' in srcfolder and os.path.normpath(os.path.split(srcfolder)[0])==os.path.normpath(os.path.split(savefolder)[0]):
#        try:
#            os.rename(srcfolder, savefolder)
#            return
#        except:
#            print 'Error renaming ', srcfolder
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)
    for fn in os.listdir(srcfolder):
        if skipana and fn.endswith('.ana'):
            continue
        shutil.move(os.path.join(srcfolder, fn), os.path.join(savefolder, fn))
    os.rmdir(srcfolder)
    savep=os.path.join(savefolder, '%s.ana' %timename)
    with open(savep, mode='w') as f:
        f.write(anafilestr)
    if anadict is None:
        return
    saveanadict=copy.deepcopy(anadict)
    convertstrvalstonum_nesteddict(saveanadict)
    convertfilekeystofiled(saveanadict)
    with open(savep.replace('.ana', '.pck'), mode='w') as f:
        pickle.dump(saveanadict, f)

def openana(p, erroruifcn=None, stringvalues=False):
    if not ((p.endswith('ana') or p.endswith('pck')) and os.path.exists(p)):
        if erroruifcn is None:
            return {}
        p=erroruifcn('select ana/pck file to open')
        if len(p)==0:
            return {}
    if stringvalues and p.endswith('pck'):
        p=p.rpartition('pck')[0]+'ana'
    if not os.path.exists(p):
        if erroruifcn is None:
            return {}
        p=erroruifcn('for text-only must use .ana file')
        if len(p)==0:
            return {}
    if p.endswith('pck'):
        with open(p, mode='r') as f:
            anadict=pickle.load(f)
    else:
        with open(p, mode='r') as f:
            lines=f.readlines()
        lines=[l for l in lines if len(l.strip())>0]
        tuplist=[]
        while len(lines)>0:
            tuplist+=[createnestparamtup(lines)]
        anadict=dict(\
        [createdict_tup(tup) for tup in tuplist])
        if not stringvalues:
            convertfilekeystofiled(anadict)
            convertstrvalstonum_nesteddict(anadict)
    return anadict
    
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
