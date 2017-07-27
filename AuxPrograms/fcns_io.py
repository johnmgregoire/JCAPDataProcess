import numpy, pickle, shutil, string
from matplotlib.ticker import FuncFormatter
import matplotlib.colors as colors
from fcns_math import *
from fcns_ui import mygetopenfile
import time
import zipfile
from operator import itemgetter
from DBPaths import *
from re import compile as regexcompile
def myexpformat(x, pos):
    for ndigs in range(5):
        lab=(('%.'+'%d' %ndigs+'e') %x).replace('e+0','e').replace('e+','e').replace('e0','').replace('e-0','e-')
        if eval(lab)==x:
            return lab
    return lab
ExpTickLabels=FuncFormatter(myexpformat)

are_paths_equivalent=lambda path1, path2:os.path.normcase(os.path.abspath(path1))==os.path.normcase(os.path.abspath(path2))

def filterchars(s, valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)):
    return ''.join([c for c in s if c in valid_chars])


def attemptnumericconversion(s, fcn=float):
    try:
        return fcn(s)
    except ValueError:
        return s

def attemptnumericconversion_tryintfloat(s):
    try:
        return (('.' in s or 'E' in s or 'e' in s) and (float(s),) or (int(s),))[0]
    except ValueError:
        return s
#    if (s.replace('.', '', 1).replace('e', '', 1).replace('+', '', 1).replace('-', '', 1)).isalnum():
#        try:
#            return myeval(s)
#        except:
#            pass
#    return s
class ZipClass():#TODO: zipclass instances are kept open in a few places and closed if something else opened but otherwise left open. could close these when the python application closed (an ExitRoutine)
    def __init__(self, zp):
        self.archive=zipfile.ZipFile(zp, 'r')
        self.splitfn=lambda p: os.path.split(p)[1] if '.zip' in p else p
        self.zipopenfcn= lambda fn: self.archive.open(self.splitfn(fn), 'r')
    def fn_in_archive(self, fn):
        return self.splitfn(fn) in self.archive.namelist()
    def first_fn_endswith(self, endswithstr):
        fnl=[fnv for fnv in self.archive.namelist() if fnv.endswith(endswithstr)]
        if len(fnl)==0:
            return None
        return fnl[0]

    def close(self):
        self.archive.close()
    def readlines(self, fn):
        with self.zipopenfcn(fn) as f:
            ans=f.readlines()
        return ans
    def read(self, fn):
        with self.zipopenfcn(fn) as f:
            ans=f.read()
        return ans
    def loadpck(self, fn):
        with self.zipopenfcn(fn) as f:
            ans=pickle.load(f)
        return ans
    def readarr(self, fn, dtype='float32'):
        with self.zipopenfcn(fn) as f:
            ans=numpy.frombuffer(f.read(), dtype=dtype)#if not in a .zip this file would need be opened as 'rb' but .zip doesn't have that option because maybe it reads bytes as default but i think converts them to string so if get an error reading a binary array from a .zip, this is suspect
        return ans

def gen_zipclass(p):
    if '.zip' in p:
        if not p.endswith('.zip'):
            p=p.partition('.zip')[0]+'.zip'
        zipclass=ZipClass(p)
    else:
        zipclass=False
    return zipclass

def copyanafiles(src, dest):
    zipclass=gen_zipclass(src)

    if zipclass:
        for fn in zipclass.archive.namelist():
            if fn.endswith('ana') or fn.endswith('pck'):
                continue
            zipclass.archive.extract(fn, dest)
        zipclass.close()
    else:
        for fn in os.listdir(src):
            if fn.endswith('ana') or fn.endswith('pck'):
                continue
            shutil.copy(os.path.join(src, fn), os.path.join(dest, fn))
def selectexpanafile(parent, exp=True, markstr=None):#TODO support getting exp and ana from .zip
    if exp:
        fold=tryprependpath(EXPFOLDERS_J+EXPFOLDERS_L, '')
        ext='.exp'
        if markstr is None:
            markstr='open EXP'
    else:
        fold=tryprependpath(ANAFOLDERS_J+ANAFOLDERS_L, '')
        ext='.ana'
        if markstr is None:
            markstr='open ANA'

    p=mygetopenfile(parent, xpath=fold, markstr=markstr, filename=ext )
    if p.endswith('.zip'):
        archive=zipfile.ZipFile(p, 'r')
        fnl=[fn for fn in archive.namelist() if fn.endswith(ext) and not fn.startswith('._')]
        archive.close()
        if len(fnl)==0:
            print 'tried opening %s in a .zip file but could not find one' %ext
            return ''
        p=os.path.join(p, fnl[0]) #presumable only 1 .exp or .ana in any .zip
    return p

def removefiles(folder, fns):
    for fn in fns:
        os.remove(os.path.join(folder, fn))

def getsamplenum_fnline(fnline):
    if fnline.count(';')==2:#the optional sample_no is after the 2nd ;
        if fnline.startswith('0_'):
            return 0
        return int(fnline.rpartition(';')[2].strip())
    else:
        return getsamplenum_fn(fnline)
def getsamplenum_fn(fn):
    if fn.startswith('Sample'):
        return int(fn.partition('Sample')[2].partition('_')[0])
    elif fn[0].isdigit():
        if fn.startswith('0_'):
            return 0
        try:
            return int(fn.partition('_')[0])
        except:
            pass
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

def getarrs_filed(p, filed, selcolinds=None, trydat=True, zipclass=None):
    closezip=False
    if zipclass is None:#only close zip if opened it here (not if it was passed)
        zipclass=gen_zipclass(p)
        closezip=bool(zipclass)
    if trydat:
        pdat=p if p.endswith('.dat') else (p+'.dat')
        if os.path.isfile(pdat) or (zipclass and zipclass.fn_in_archive(pdat)):
            ans=readbinary_selinds(pdat, len(filed['keys']), keyinds=selcolinds, zipclass=zipclass)
            if closezip:
                zipclass.close()
            return ans

    if not ((os.path.isfile(p) or (zipclass and zipclass.fn_in_archive(p)))):
        if closezip:
            zipclass.close()
        return None
    ans=readtxt_selectcolumns(p, selcolinds=selcolinds, delim=None, num_header_lines=filed['num_header_lines'], zipclass=zipclass)
    if closezip:
        zipclass.close()
    return ans

def readbinary_selinds(p, nkeys, keyinds=None, zipclass=None):
    closezip=False
    if zipclass is None:
        zipclass=gen_zipclass(p)
        closezip=bool(zipclass)

    if zipclass:
        b=zipclass.readarr(p)
    else:
        with open(p, mode='rb') as f:
            b=numpy.fromfile(f,dtype='float32')
    b=b.reshape((nkeys,len(b)//nkeys))

    if closezip:
        zipclass.close()

    if keyinds is None:
        return b
    else:
        return b[keyinds]

def readtxt_selectcolumns(p, selcolinds=None, delim='\t', num_header_lines=1, floatintstr=float, zipclass=None, lines=None):
    if lines is None:
        closezip=False
        if zipclass is None:
            zipclass=gen_zipclass(p)
            closezip=bool(zipclass)

        if zipclass:
            lines=zipclass.readlines(p)[num_header_lines:]
        else:
            with open(p, mode='r') as f:
                lines=f.readlines()[num_header_lines:]

        if closezip:
            zipclass.close()
    else:
        lines=lines[num_header_lines:]
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


def readcsvdict(p, fileattrd, returnheaderdict=False, zipclass=None, includestrvals=False, delim=','):
    d={}
    arr=readtxt_selectcolumns(p, delim=delim, num_header_lines=fileattrd['num_header_lines'], floatintstr=str, zipclass=zipclass)

    if not 'keys' in fileattrd.keys():
        with open(p, mode='r') as f:
            lines=f.readlines()
            ks=lines[fileattrd['num_header_lines']-1].split(',')
            ks=[k.strip() for k in ks]
            fileattrd['keys']=ks
    for k, a in zip(fileattrd['keys'], arr):
        if '.' in a[0] or 'NaN' in a:
            d[k]=numpy.float32(a)
        elif a[0].isdigit():
            d[k]=numpy.int32(a)
        elif includestrvals:
            d[k]=a#a string array that is onlcude included if "requested" via includestrvals

    if not returnheaderdict:
        return d

    if zipclass:
        lines=zipclass.readlines(p)[:fileattrd['num_header_lines']]
    else:
        with open(p, mode='r') as f:
            lines=f.readlines()[:fileattrd['num_header_lines']]

    lines=lines[1:-1]
    tuplist=[]
    while len(lines)>0:
        tuplist+=[createnestparamtup(lines)]
    headerdict=dict(\
        [createdict_tup(tup) for tup in tuplist])
    return d, headerdict

def get_xrfs_stds_csv(startswithstr='', searchstr='.csv', transkey='transition', nmolcpskey='nmol.CPS'):

    fold=tryprependpath(XRFSPROCESSFOLDERS, '', testfile=False, testdir=True)
    if fold is None:
        return None
    csvfns=sorted([(fn.partition('__')[2][:8], fn) for fn in os.listdir(fold) if fn.startswith(startswithstr) and searchstr in fn])#sort by 8 character date after the __
    if len(csvfns)==0:
        return None
    csvfn=csvfns[-1][1]
    with open(os.path.join(fold, csvfn), mode='r') as f:
        lines=f.readlines()
    colheads=[sv.strip() for sv in lines[0].split(',')]
    if not (transkey in colheads and nmolcpskey in colheads):
        return None
    inds=[colheads.index(transkey), colheads.index(nmolcpskey)]
    arr=readtxt_selectcolumns('', selcolinds=inds, delim=',', num_header_lines=1, floatintstr=str, zipclass=None, lines=lines)
    xrfs_stds_dict=dict([(trans.strip(), float(nmolcps.strip())) for trans, nmolcps in arr.T])
    return xrfs_stds_dict, csvfn

def readechemtxt(path, mtime_path_fcn=None, lines=None, interpretheaderbool=True):
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
            if not interpretheaderbool:
                continue
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
    if len(z)==0:#no data
        nrows=0
    else:
        for k, arr in zip(d['column_headings'], numpy.float32(z).T):
            d[k]=arr
        nrows=len(arr)

    d['num_data_rows']=nrows
    d['path']=path
    if not mtime_path_fcn is None:
        d['mtime']=mtime_path_fcn(path)
    return d


def readxrfbatchcsv(path, mtime_path_fcn=None, lines=None):
    if lines is None:
        try:#need to sometimes try twice so might as well try 3 times
            f=open(path, mode='rU')
        except:
            try:
                f=open(path, mode='rU')
            except:
                f=open(path, mode='rU')
        lines=f.readlines()
        f.close()
    d={}
    z=[]
    for count, l in enumerate(lines):
        if not l.startswith('Inte'):
            continue
        else:
            break
    rawheadings=(l[:-1] if l.endswith(',') else l).replace(' ', '').strip().split(',') # remove final comma if it exists
    inds=[i for i, x in enumerate(rawheadings) if x in ['Inte', 'Wt%', 'At%', 'StgLabel']]
    prefixes=[rawheadings[i] for i in inds]
    xrfheadings=[prefixes[i]+'_'+x for i in range(len(inds)-1) for j, x in enumerate(rawheadings) if (j>=inds[i] and j<inds[i+1] and j not in prefixes)]
    stgheadings=rawheadings[max(inds):]
    d['column_headings']=xrfheadings+stgheadings # reformatted column_headings for uniqueness
    d['num_header_lines']=count+1
    if len(lines[count:])==0:
        return {}
    def tryfloat(x):
        try:
            return(float(x))
        except:
            return('NaN')
    try:
        z=[map(tryfloat, (l[:-1] if l.endswith(',') else l).replace(' ', '').replace('\x00', '').strip().split(',')) for l in lines[count+1:] if len(l.strip())>0]
    except:
        print l
        print '\t' in l
        print l.replace(' ', '').replace('\x00', '').strip().split(',')
        print map(float, l.replace(' ', '').replace('\x00', '').strip().split(','))
        raise
    if len(z)==0:#no data
        nrows=0
    else:
        for k, arr in zip(d['column_headings'], numpy.float32(z).T):
            if (k not in ['Inte_Inte', 'Wt%_Wt%', 'At%_At%', '']):
                d[k]=arr
            else:
                d['column_headings'].remove(k)
        nrows=len(arr)

    d['num_data_rows']=nrows
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


def createfileattrdict(fileattrstr, fn=''):
    fileattrstr=fileattrstr.replace(';;', ';') #201601 see that images_files has double ;  due to no column headings - not sure if this is corerect protocal but change it here to pick up the sample_no
    type_keys_heads_rows=fileattrstr.split(';')
    d={}
    d['file_type']=type_keys_heads_rows[0]
    if len(type_keys_heads_rows)==1 or len(type_keys_heads_rows[1].strip())==0:
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
        if fn.startswith('0_') or len(type_keys_heads_rows[-1].strip())==0:#to avoid issue with uvis data having sample_no for ref files
            d['sample_no']=0
        else:
            d['sample_no']=int(type_keys_heads_rows[-1].strip())
    else:
        d['sample_no']=0#numpy.nan #this is top keep all sample_no as int instead of mixing int and float. this should not be confused with the 0 used as sample_no for uvvis ref spectra because by the time we get here the run_use has already been defined
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
                    d=createfileattrdict(keystr, fn=fn)
                    exporanafiledict[k][k2][k3][fn]=d
def importfomintoanadict(anafiledict, anafolder):#assumes convertfilekeystofiled already run on anafiledict
    for anak, anad in anafiledict.iteritems():
        if (not anak.startswith('ana__')) or not 'files_multi_run' in anad.keys():
            continue
        for typek, typed in anad['files_multi_run'].keys():
            for fn, fileattrd in typed.iteritems():
                anafiledict[anak]['files_multi_run'][typek][fn]=readcsvdict(os.path.join(anafolder, fn), fileattrd)


def saverawdat_expfiledict(expfiledict, folder, saverawdat=True):
    datastruct_expfiledict(expfiledict, savefolder=folder, saverawdat=saverawdat)
def datastruct_expfiledict(expfiledict, savefolder=None, trytoappendmissingsample=True, saverawdat=True):#savefolder will save binary arrays and also update the expfiledict to include num header lines and data rows
    if savefolder is None:
        convertstrvalstonum_nesteddict(expfiledict)
    if not savefolder is None:
        openfnc=lambda fn:open(os.path.join(savefolder, fn+'.dat'), mode='wb')
        #savefcn=lambda d, keys:numpy.float64([d[k] for k in keys]).tofile(f)
    filedeletedbool=False
    readfcn=readdatafiledict[expfiledict['experiment_type']]
    for k, rund in expfiledict.iteritems():
        if not k.startswith('run__'):
            continue
        runp=rund['run_path']

        zipbool=runp.endswith('.zip')

        if ((not zipbool) and not os.path.isdir(runp)) or (zipbool and not os.path.isfile(runp)):
            runp=tryprependpath(RUNFOLDERS, runp)

        if zipbool:
            archive=zipfile.ZipFile(runp, 'r')
            zipopenfcn=lambda fn:archive.open(fn, 'r')#rund['rcp_file'].partition('/')[0]+'/'+
        for k2, techd in rund.iteritems():
            if not k2.startswith('files_technique__'):
                continue
            if 'XRFS' in k2:
                def openandreadlinesfcn(fn):
                    if zipbool:
                        with zipopenfcn(fn) as f:
                            lines=f.readlines()
                    else:
                        p=os.path.join(runp, fn)
                        with open(p,'r') as f:
                            lines=f.readlines()
                        #if not '\n' in fs:

                    return lines
                expfiledict[k][k2]=create_techd_for_xrfs_exp(techd, openandreadlinesfcn)#if zip then another ziplcass will be opened in here
                continue
            for k3, typed in techd.iteritems():
                #define functions by file and exp type to avoid having to find the function using each file label like "eche_gamry_txt_file"
                if not saverawdat:
                    if k3=='spectrum_files':#for eche and uvis
                        numhead_numdata_fcn=lambda lines: get_numhead_numdata_smpoptfiles(lines)
                        readlinesfcn=lambda f:f.readlines(50)#only need the first lines so read 50 bytes
                    elif k3=='pstat_files':
                        if 'eche' in expfiledict['experiment_type']:
                            numhead_numdata_fcn=lambda lines: get_numhead_numdata_echetxtfiles(lines)
                            readlinesfcn=lambda f:f.readlines()
                        elif 'pets' in expfiledict['experiment_type']:
                            numhead_numdata_fcn=lambda lines: get_numhead_numdata_petsdtafiles(lines)
                            readlinesfcn=lambda f:f.readlines(1000)#only need the header so read
                    else:
                        print 'NO FILE READER AVAILABLE FOR FILE TYPE ', k3

                for fn, fileattrstr in typed.items():#here do not use iteritems since possible for entries to be deleted in the loop and cannot modify dictionary being iterated
                    try:
                        if zipbool:
                            with zipopenfcn(fn) as f:
                                if saverawdat:
                                    lines=f.readlines()
                                else:
                                    lines=readlinesfcn(f)
                        else:
                            p=os.path.join(runp, fn)
                            with open(p,'r') as f:
                                if saverawdat:
                                    lines=f.readlines()
                                else:
                                    lines=readlinesfcn(f)
                    except:#this exception should only occur if the filename was in the .rcp and then put into .exp but the file doesn't actually exist
                        print 'ERROR: %s does not exist in folder %s, so it is being deleted from %s/%s/%s' %(fn, runp, k, k2, k3)
                        del expfiledict[k][k2][k3][fn]
                        filedeletedbool=True
                        continue
                    if savefolder is None and saverawdat:#save raw data into the dictionary. empty files allowed here but not below - not supported for all exp types
                        expfiledict[k][k2][k3][fn]=readfcn(os.path.splitext(fn), lines)
                    else:
                        if k3 in ['image_files'] or k3.startswith('binary'):#list here the types of files that should not be converted to binary
                            s=fileattrstr#no sample_no appended or any modifications made to file attr str  for image_files, etc.
                        else:
                            if saverawdat:
                                keys=fileattrstr.partition(';')[2].partition(';')[0].split(',')
                                keys=[kv.strip() for kv in keys]
                                filed=readfcn(os.path.splitext(fn), lines)
                            else:
                                filed=numhead_numdata_fcn(lines)
                            if filed['num_data_rows']==0:#no data in file
                                print 'ERROR: %s in folder %s has no data, so it is being deleted from %s/%s/%s' %(fn, runp, k, k2, k3)
                                del expfiledict[k][k2][k3][fn]
                                filedeletedbool=True
                                continue
                            if saverawdat:
                                x=numpy.float32([filed[kv] for kv in keys])
                                with openfnc(fn) as f:
                                    x.tofile(f)

                            if fileattrstr.count(';')==2:#valid sample_no in place and was there is .rcp file
                                first2attrs, garb, samplestr=fileattrstr.rpartition(';')
                                if fn.startswith('0_'):#get rid of sample_no from ref data in uvis
                                    s='%s;%d;%d' %(first2attrs.strip(), filed['num_header_lines'], filed['num_data_rows'])
                                else:
                                    s='%s;%d;%d;%s' %(first2attrs.strip(), filed['num_header_lines'], filed['num_data_rows'], samplestr.strip())
                            elif fileattrstr.count(';')==4:#full info already , e.g. due to import of line from .exp or a completed .rcp
                                s=fileattrstr
                            elif fileattrstr.count(';')==1:#probably read from .rcp and fileattrstr contains file_type and keys so take that and append headerlines and datarows
                                s='%s;%d;%d' %(fileattrstr.strip(), filed['num_header_lines'], filed['num_data_rows'])
                                if trytoappendmissingsample:
                                    try:
                                        tempsmp=getsamplenum_fn(fn)
                                        if not tempsmp>0:
                                            raise
                                        s+=(';%d' %tempsmp)
                                    except:
                                        pass
                            elif fileattrstr.count(';')==3:#file_type;keys;nhead;ndata but missing sample
                                s=fileattrstr.strip()
                                if trytoappendmissingsample:
                                    try:
                                        tempsmp=getsamplenum_fn(fn)
                                        if not tempsmp>0:
                                            raise
                                        s+=(';%d' %tempsmp)
                                    except:
                                        pass
                        expfiledict[k][k2][k3][fn]=s
        if zipbool:
            archive.close()
    if filedeletedbool:
        cleanup_empty_filed_in_expfiledict(expfiledict)
    return expfiledict

def cleanup_empty_filed_in_expfiledict(expfiledict):
    #delete 3rd level down, where there are no fielnames for a given file type
    for k, rund in expfiledict.iteritems():
        if not k.startswith('run__'):
            continue
        for k2, techd in rund.iteritems():
            if not k2.startswith('files_technique__'):
                continue
            for k3 in techd.keys():
                if len(techd[k3])==0:#there are no more filenames of this type
                    del expfiledict[k][k2][k3]


    #delete 2nd level down, where there are no file types for a given technique
    for k, rund in expfiledict.iteritems():
        if not k.startswith('run__'):
            continue
        for k2 in rund.keys():
            if not k2.startswith('files_technique__'):
                continue
            if len(rund[k2])==0:#there are no more filenames of this type
                del expfiledict[k][k2]
                searchstr=k2.partition('files_technique')[2]
                for k2other in rund.keys():
                    if searchstr in k2other:
                        del expfiledict[k][k2other]
#        filekeysleftinrun=[k_run for k_run in expfiledict[k].keys() if 'files_technique__' in k_run]
#        if len(filekeysleftinrun)==0:
#            del expfiledict[k]
    #stopping here, menaing that it is conceivable that a run__ block may not hav any files_technique__ which means that it does not have files and is a useless run

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

def tryprependpath(preppendfolderlist, p, testfile=True, testdir=True):
    #if (testfile and os.path.isfile(p)) or (testdir and os.path.isdir(p)):
    if os.path.isfile(p):
        return p
    p=p.strip(chr(47)).strip(chr(92))
    for folder in preppendfolderlist:
        pp=os.path.join(folder, p)
        if (testdir and os.path.isdir(pp)) or (testfile and os.path.isfile(pp)):
            return pp
    return ''

def compareprependpath(preppendfolderlist, p, replaceslash=True):
    for folder in preppendfolderlist:
        if os.path.normpath(p).startswith(os.path.normpath(folder)):
            p=os.path.normpath(p)[len(os.path.normpath(folder)):]
            break
    if replaceslash:
        p=p.replace(chr(92),chr(47))
    return p

def prepend_root_exp_path(p, exp=True):
    parentfoldtemp, subfold=os.path.split(p)#in tryprependpath, parentfoldtemp has its leading and trailing slashes removed
    for parentfold in [tryprependpath(EXPFOLDERS_J if exp else ANAFOLDERS_J, parentfoldtemp), \
                            tryprependpath(EXPFOLDERS_L if exp else ANAFOLDERS_L, parentfoldtemp)]:
        if len(parentfold)==0:
            continue
        if os.path.isfile(os.path.join(parentfold, subfold)):
            return os.path.join(parentfold, subfold)
        if subfold.count('.')>1:
            subfold='.'.join(subfold.split('.')[:2])
        subfoldl=[s for s in os.listdir(parentfold) if s.startswith(subfold)]
        if len(subfoldl)>0:
            return os.path.join(parentfold, subfoldl[0])
    #print 'cannot find folder %s in %s' %(subfold, parentfold)
    return p
def buildexppath(experiment_path_folder, ext_str='.exp'):#exp path is the path of the .exp ascii file , which is different from the experiment_path in an .ana file which is the folder path
    p=experiment_path_folder
    fn=os.path.split(p)[1][:15]+ext_str #15 characters in YYYYMMDD.HHMMSS

    if (not os.path.isdir(p) or os.path.isdir(os.path.split(p)[0])) or not os.path.isabs(p):
        if ext_str=='.exp':
            p=prepend_root_exp_path(p)
        else:
            p=prepend_root_exp_path(p, exp=False)

    #from here down : turn an exp folder into an exp file
    if os.path.isfile(os.path.join(p, fn)):
        return os.path.join(p, fn)
    if '.zip' in p:
        return os.path.join(p, fn)#hope this works out without checking if it is actually there

    fnl=[s for s in os.listdir(p) if s.endswith(ext_str)]
    if len(fnl)==0:
        print 'cannot find %s file in %s' %(ext_str, p)
        return p
    return os.path.join(p, fnl[0])#shouldn't be multiple .exp but if so take the first one found
def buildanapath(analysis_path_folder):
    return buildexppath(analysis_path_folder, ext_str='.ana')

def buildrunpath(runp):
    #if user makes .exp with a folder on K or intr computer and this run_path is used but the file is gone opr path changed to ..copied, then should bepossible to find this run as a .zip on J but that is not attempted here
    p=tryprependpath(RUNFOLDERS, runp)
    if len(p)==0:
        foldrel, oldrcpfn=os.path.split(runp)
        fold=tryprependpath(RUNFOLDERS, foldrel)
        if len(fold)==0:
            return ''
        newfns=[fn for fn in os.listdir(fold) if fn.startswith(oldrcpfn[:15])]
        if len(newfns)==1:
            p=os.path.join(fold, newfns[0])
    return p

def buildrunpath_selectfile(fn, expfolder_fullpath, runp=None, expzipclass=None, returnzipclass=False):

    returnvalfcn=lambda val:(val, expzipclass) if returnzipclass else val

    if expzipclass is None:
        expzipclass=gen_zipclass(expfolder_fullpath)
    if expzipclass:
        if expzipclass.fn_in_archive(fn+'.dat'):
            return returnvalfcn(os.path.join(expfolder_fullpath, fn+'.dat'))
        if expzipclass.fn_in_archive(fn):
            return returnvalfcn(os.path.join(expfolder_fullpath, fn))
    if os.path.isfile(os.path.join(expfolder_fullpath, fn+'.dat')):
        return returnvalfcn(os.path.join(expfolder_fullpath, fn+'.dat'))
    if os.path.isfile(os.path.join(expfolder_fullpath, fn)):
        return returnvalfcn(os.path.join(expfolder_fullpath, fn))

    if runp is None:
        return None
    runp_fullpath=buildrunpath(runp)
    runzipclass=gen_zipclass(runp_fullpath)

    returnvalfcn=lambda val:(val, runzipclass) if returnzipclass else val

    if runzipclass:
        if runzipclass.fn_in_archive(fn):
            return returnvalfcn(os.path.join(runp_fullpath, fn))
    if os.path.isfile(os.path.join(runp_fullpath, fn)):
        return returnvalfcn(os.path.join(runp_fullpath, fn))
    return None

def saveexp_txt_dat(expfiledict, erroruifcn=None, saverawdat=True, experiment_type='temp', rundone='.run', runtodonesavep=None, savefolder=None, file_attr_and_existence_check=True):#for the num headerlines and rows to be written to .exp, saverawdat must be true

    if runtodonesavep is None and savefolder is None:
        timename=timestampname()
        expfiledict['name']=timename
        Kfold=tryprependpath(EXPFOLDERS_L, '')#one of these better exist
        savep=os.path.join(os.path.join(os.path.join(Kfold, experiment_type), timename+rundone), timename+'.exp')

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

    folder=os.path.split(savep)[0]
    if os.path.isdir(folder):
        for fn in os.listdir(folder):
            os.remove(os.path.join(folder, fn))#cannot overwrite files because filename deduplication may be different from previous save
    else:
        os.mkdir(folder)
    # if raw data is not saved and a fielname exists in an .rcp->.exp but the file is not real, there will be erros down the line.
    if file_attr_and_existence_check or saverawdat:
        saverawdat_expfiledict(saveexpfiledict, folder, saverawdat=saverawdat)#the filename attributes get update here, and any filenames for which a fiel cannot be found is removed from saveexpfiledict btu not from expfiledict

    for rund in saveexpfiledict.itervalues():
        if isinstance(rund, dict) and 'run_path' in rund.keys():
            rp=rund['run_path']
            rp=compareprependpath(RUNFOLDERS, rp)
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
    sl=['' if len(k)==0 else (k+': '+str(filedict[k])) for k in keys]
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

def get_lines_path_file(p=None, erroruifcn=None):
    try:
        f=open(p, mode='r')
    except:
        if erroruifcn is None:
            return [], ''
        p=erroruifcn('bad platemap path')
        if len(p)==0:
            return [], ''
        f=open(p, mode='r')

    ls=f.readlines()
    f.close()
    return ls, p
def readsingleplatemaptxt(p, returnfiducials=False,  erroruifcn=None, lines=None):
    if lines is None:
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
    else:
        ls=lines
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
    samplelines=[l for l in ls[count:] if l.count(',')==(len(keys)-1)]
    for l in samplelines:
        sl=l.split(',')
        d=dict([(k, myeval(s.strip())) for k, s in zip(keys, sl)])
        dlist+=[d]
    if not 'sample_no' in keys:
        dlist=[dict(d, sample_no=d['Sample']) for d in dlist]
    if returnfiducials:
        return dlist, fid
    return dlist

#def getplatemappath_plateid(plateidstr, erroruifcn=None):
#    p=''
#    fld=os.path.join(tryprependpath(PLATEFOLDERS, ''), plateidstr)
#    if os.path.isdir(fld):
#        l=[fn for fn in os.listdir(fld) if fn.endswith('map')]+['None']
#        p=os.path.join(fld, l[0])
#    if (not os.path.isfile(p)) and not erroruifcn is None:
#        p=erroruifcn('', tryprependpath(PLATEFOLDERS[::-1], ''))
#    return p

def getplatemappath_plateid(plateidstr, erroruifcn=None, infokey='screening_map_id:', return_pmidstr=False):
    p=''
    pmidstr=''
    infop=getinfopath_plateid(plateidstr)
    if infop is None:
        if not erroruifcn is None:
            p=erroruifcn('', tryprependpath(PLATEMAPFOLDERS, ''))
        return (p, pmidstr) if return_pmidstr else p
    with open(infop, mode='r') as f:
        s=f.read(1000)
    pmfold=tryprependpath(PLATEMAPFOLDERS, '')
    if pmfold=='' or not infokey in s:
        if not erroruifcn is None:
            p=erroruifcn('', tryprependpath(PLATEMAPFOLDERS, ''))
        return (p, pmidstr) if return_pmidstr else p
    pmidstr=s.partition(infokey)[2].partition('\n')[0].strip()
    fns=[fn for fn in os.listdir(pmfold) if fn.startswith('0'*(4-len(pmidstr))+pmidstr+'-') and fn.endswith('-mp.txt')]
    if len(fns)!=1:
        if not erroruifcn is None:
            p=erroruifcn('', tryprependpath(PLATEMAPFOLDERS, ''))
        return (p, pmidstr) if return_pmidstr else p
    p=os.path.join(pmfold, fns[0])
    return (p, pmidstr) if return_pmidstr else p

def getinfopath_plateid(plateidstr, erroruifcn=None):
    p=''
    fld=os.path.join(tryprependpath(PLATEFOLDERS, ''), plateidstr)
    if os.path.isdir(fld):
        l=[fn for fn in os.listdir(fld) if fn.endswith('info')]+['None']
        p=os.path.join(fld, l[0])
    if (not os.path.isfile(p)) and not erroruifcn is None:
        p=erroruifcn('', '')
    if (not os.path.isfile(p)):
        return None
    return p

def importinfo(plateidstr):
    fn=plateidstr+'.info'
    p=tryprependpath(PLATEFOLDERS, os.path.join(plateidstr, fn), testfile=True, testdir=False)
    if not os.path.isfile(p):
        return None
    with open(p, mode='r') as f:
        lines=f.readlines()
    infofiled=filedict_lines(lines)
    return infofiled

def getelements_plateidstr(plateidstr_or_filed, multielementink_concentrationinfo_bool=False,print_key_or_keyword='screening_print_id', exclude_elements_list=['']):#print_key_or_keyword can be e.g. "print__3" or screening_print_id
    if isinstance(plateidstr_or_filed, dict):
        infofiled=plateidstr_or_filed
    else:
        infofiled=importinfo(plateidstr_or_filed)
        if infofiled is None:
            return None
    requiredkeysthere=lambda infofiled: ('screening_print_id' in infofiled.keys()) if print_key_or_keyword=='screening_print_id' \
                                                           else (print_key_or_keyword in infofiled['prints'].keys())
    while not ('prints' in infofiled.keys() and requiredkeysthere(infofiled)):
        if not 'lineage' in infofiled.keys() or not ',' in infofiled['lineage']:
            return None
        parentplateidstr=infofiled['lineage'].split(',')[-2].strip()
        infofiled=importinfo(parentplateidstr)
    if print_key_or_keyword=='screening_print_id':
        printdlist=[printd for printd in infofiled['prints'].values() if 'id' in printd.keys() and printd['id']==infofiled['screening_print_id']]
        if len(printdlist)==0:
            return None
        printd=printdlist[0]
    else:
        printd=infofiled['prints'][print_key_or_keyword]
    if not 'elements' in printd.keys():
        return None
    els=[x for x in printd['elements'].split(',') if x not in exclude_elements_list]

    if multielementink_concentrationinfo_bool:
        return els, get_multielementink_concentrationinfo(printd,els)
    return els

def get_multielementink_concentrationinfo(printd, els):#None if nothing to report, (True, str) if error, (False, (cels_set_ordered, conc_el_chan)) with the set of elements and how to caclualte their concentration from the platemap

    searchstr1='concentration_elements'
    searchstr2='concentration_values'
    if not (searchstr1 in printd.keys() and searchstr2 in printd.keys()):
        return None
    cels=printd[searchstr1]
    concstr=printd[searchstr2]
    conclist=[float(s) for s in concstr.split(',')]

    cels=[cel.strip() for cel in cels.split(',')]
    cels_set=set(cels)
    if len(cels_set)<len(cels) or True in [conclist[0]!=cv for cv in conclist]:#concentrations available where an element is used multiple times. or 1 of the concentrations is different from the rest
        els_printchannels=[regexcompile("[A-Z][a-z]*").findall(el) for el in els]
        els_tuplist=[(el, i, j) for i, l in enumerate(els_printchannels) for j, el in enumerate(l)]
        cels_tuplist=[]
        for cel in cels:
            while len(els_tuplist)>0:
                tup=els_tuplist.pop(0)
                if tup[0]==cel:
                    cels_tuplist+=[tup]
                    break
        if len(cels_tuplist)!=len(cels):
            return True,  'could not find the concentration_elements in order in the elements list'
        cels_set_ordered=[]
        for cel, chanind, ind_elwithinchan in cels_tuplist:
            if not cel in cels_set_ordered:
                cels_set_ordered+=[cel]

        conc_el_chan=numpy.zeros((len(cels_set_ordered), cels_tuplist[-1][1]+1), dtype='float32')#tthe number of elements in the net composition space by the max ink channel
        for (cel, chanind, ind_elwithinchan), conc in zip(cels_tuplist, conclist):
            conc_el_chan[cels_set_ordered.index(cel), chanind]=conc
        #for a given platemap sample with x being the 8-component vecotr of ink channel intensity, the unnormalized concentration of cels_set_ordered is conc_el_chan*x[:conc_el_chan.shape[0]]
        return False, (cels_set_ordered, conc_el_chan)
    return None
#
#def getplatemapid_plateidstr(plateidstr, erroruifcn=None):
#    p=getinfopath_plateid(plateidstr)
#    s=None
#    if not p is None:
#        with open(p, mode='r') as f:
#            filestr=f.read(10000)
#        searchstr='        map_id: '
#        if searchstr in filestr:
#            s=filestr.partition(searchstr)[2].partition('\n')[0].strip()
#    if s is None and not erroruifcn is None:
#        s=erroruifcn('Enter Platemap ID')
#    return s

def getscreeningmapid_plateidstr(plateidstr, erroruifcn=None):
    p=getinfopath_plateid(plateidstr)
    s=None
    if not p is None:
        with open(p, mode='r') as f:
            filestr=f.read(10000)
        searchstr='screening_map_id:'
        if searchstr in filestr:
            s=filestr.partition(searchstr)[2].partition('\n')[0].strip()
    if s is None and not erroruifcn is None:
        s=erroruifcn('Enter Screening Map ID')
    return s

def generate_filtersmoothmapdict_mapids(platemapids, requirepckforallmapids=True):#gives 2 layers nested dict, first layer of keys are mapids strings, second layer are filter names and those values are the file path to the .pck
#find pcks with matching mapid in the root folder or 1 level of subfolders. onyl matches mapid before the first '-'
    fold=tryprependpath(FOMPROCESSFOLDERS, '', testfile=False, testdir=True)
    if fold is None:
        return {}
    platemapids=[str(v) for v in list(set(platemapids))]
    d=dict([(str(v), {}) for v in platemapids])
    #assemble list of root and subfolders
    foldlist=[fold]+[os.path.join(fold, fn) for fn in os.listdir(fold) if os.path.isdir(os.path.join(fold, fn))]
    #loop through all filnames and mtch mapid, name is between the first '_' and '.pck'
    for fold2 in foldlist:
        for fn in os.listdir(fold2):
            id=fn.partition('-')[0].lstrip('0')
            if not id in platemapids:
                continue
            filtername=fn.partition('_')[2].rstrip('.pck')
            d[id][filtername]=os.path.join(fold2, fn)
    if len(platemapids)<=1 or not requirepckforallmapids:
        return d
    kl=set(d[platemapids[0]])
    for id in platemapids[1:]:
        kl=kl.intersection(set(d[id]))
    for dv in d.values():
        for kv in dv.keys():
            if not kv in kl:
                dv.pop(kv)
    return d

def readrcpfrommultipleruns(pathlist, rcpdictadditions=None):
    if rcpdictadditions is None:
        rcpdictadditions=[[] for p in pathlist]

    techset=set([])
    typeset=set([])
    rcpdlist=[]
    for p, tupl in zip(pathlist, rcpdictadditions):
        remstr=None

        if p.endswith('.zip'):
            rcpfn, lines, remstr=rcplines_zip(p)
        elif os.path.isdir(p):
            rcpfn, lines=rcplines_folder(p)
            if rcpfn is None:
                continue
        elif p.endswith('.rcp'):
            with open(p, mode='r') as f:
                lines=f.readlines()
            p, rcpfn=os.path.split(p)
        else:
            print 'check if this is a valid file: ', p
            continue
        if len(lines)==0:
            continue
        if remstr is None:
            fns=[fn for fn in os.listdir(p) if fn.endswith('.rem')]
            if len(fns)>0:
                with open(os.path.join(p, fns[0]), mode='r') as f:
                    remstr=f.read()
            else:
                remstr=''
        if len(remstr)>0:
            tupl+=rcpdtuple_remstr(remstr)
        rcpd=readrcplines(lines, prepend_rcp_rupl=tupl)

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

def rcpdtuple_remstr(remstr):
    remdlist=eval(remstr.strip())
    tupl=[('run_comment__%d:' %(count+1), [\
     (('%s: "%s"' %(k, str(v))) if k=='comment' else ('%s: %s' %(k, str(v))), [])\
            for k, v in remd.iteritems()]) for count, remd in enumerate(remdlist) if not '(type new note here)' in remd.values()]
    return tupl
def rcplines_folder(foldp):
    fns=[fn for fn in os.listdir(foldp) if fn.endswith('.rcp')]
    if len(fns)!=1:
        return None, None
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
        return '', [], ''
    rcpfn=fns[0]
    f=archive.open(rcpfn)
    lines=f.readlines()
    f.close()
    fns=[fn for fn in archive.namelist() if fn.endswith('.rem')]

    if len(fns)>0:#only use 1st file, which can take an aribtrary number of comments
        f=archive.open(fns[0])
        remstr=f.read()
        f.close()
    else:
        remstr=''
    archive.close()
    return rcpfn, lines, remstr

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
def readrcplines(lines, prepend_rcp_rupl=[]):
    rcptuplist=prepend_rcp_rupl#start this tuplist off with prepend items not in the .rcp, which must be done here because when the index strucutrues are built in interpretrcptuplist the rcptuplist and rcpd should be considered read-only
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
        ]
        #if ':' in typestr and (fnline.startswith('Sample') or fnline[0].isdigit())\
        #] # the " and (fnline.startswith('Sample') or fnline[0].isdigit()" is to validate expected eche and uvis files but should not be necessary moving forward.


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

def filedict_lines(lines):
    lines=[l for l in lines if len(l.strip())>0]
    exptuplist=[]
    while len(lines)>0:
        exptuplist+=[createnestparamtup(lines)]
    return dict([createdict_tup(tup) for tup in exptuplist])
def readexpasdict(p, includerawdata=False, erroruifcn=None, returnzipclass=False, createfiledicts=True):#create both a list of rcpd but also a corresponding ...     - p can be a file path or a zip file path with a joined filename
    if not ((p.endswith('exp') or p.endswith('pck')) and (os.path.exists(p) or ('.zip' in p and os.path.exists(os.path.split(p)[0])) ) ):#if .zip only tests if the zip file exists
        if erroruifcn is None:
            if returnzipclass:
                return {}, False
            else:
                return {}
        p=erroruifcn('select exp file')
        if len(p)==0:
            if returnzipclass:
                return {}, False
            else:
                return {}
    zipclass=gen_zipclass(p)

    if p.endswith('.pck'):
        if zipclass:
            expfiledict=zipclass.loadpck(p)
        else:
            with open(p, mode='r') as f:
                expfiledict=pickle.load(f)
    elif p.endswith('.exp'):
        if zipclass:
            lines=zipclass.readlines(p)
        else:
            with open(p, mode='r') as f:
                lines=f.readlines()
        expfiledict=filedict_lines(lines)

        #these tiems would have been performed before saving .pck so only perform for .exp
        convertstrvalstonum_nesteddict(expfiledict)
        if createfiledicts:
            convertfilekeystofiled(expfiledict)

    else:
        if returnzipclass:
            return None, False
        else:
            if zipclass:
                zipclass.close()
            return None
    if includerawdata:
        expfiledict=datastruct_expfiledict(expfiledict)

    if returnzipclass:
        return expfiledict, zipclass
    else:
        if zipclass:
            zipclass.close()
        return expfiledict


def readexpasrcpdlist(p, only_expparamstuplist=False):#create both a list of rcpd but also a corresponding
    zipclass=gen_zipclass(p)

    if zipclass:
        lines=zipclass.readlines(p)
    else:
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


def get_numhead_numdata_smpoptfiles(lines):
    a, b, numdata, numhead=lines[0].split('\t')
    numdata=int(numdata)
    numhead=int(numhead)+2
    return {'num_header_lines': numhead,'num_data_rows': numdata}

def get_numhead_numdata_echetxtfiles(lines):
    numhead=map(operator.itemgetter(0),lines).count('%')
    numdata=len(lines)-numhead
    return {'num_header_lines': numhead,'num_data_rows': numdata}

def get_numhead_numdata_petsdtafiles(lines):
    for count, l in enumerate(lines):
        if l.startswith('CURVE\tTABLE\t'):
            numdata=int(l.partition('CURVE\tTABLE\t')[2].strip())
            break
    numhead=count+3
    return {'num_header_lines': numhead,'num_data_rows': numdata}

def read_dta_pstat_file(path, lines=None, addparams=False):
    if lines is None:
        f=open(path, mode='r')
        lines=f.readlines()
        f.close()
    filed=get_numhead_numdata_petsdtafiles(lines)
    d={}
    if addparams:
        for k, v in filed:
            d[k]=v
    if filed['num_data_rows']==0:
        return d
    delim='\t'
    allkeys=lines[filed['num_header_lines']-2].strip().split(delim)
    skipinds=[i for i, k in enumerate(allkeys) if k in ['IERange', 'Over']]
    keys=[k for i, k in enumerate(allkeys) if not i in skipinds]
    myfloatfcn=lambda s:(len(s.strip())==0 and (float('NaN'),) or (float(s.strip()),))[0]#this turns emtpy string into NaN. given the .strip this only "works" if delimeter is not whitespace, e.g. csv
    z=[map(myfloatfcn, [x for i, x in enumerate(l.strip().split(delim)) if not i in skipinds]) for l in lines[filed['num_header_lines']:]]

    for k, arr in zip(keys, numpy.float32(z).T):
        d[k]=arr
    return  d

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
        if smp is None and not fn.startswith('0_'):
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
    if len(lines)<=1:
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
            d['sample_no']=0#numpy.nan
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

    if len(z)==0:#NO DATA!
        nrows=0
    else:
        for k, arr in zip(column_headings, numpy.float32(z).T):
            d[k]=arr
        nrows=len(arr)
    if addparams:
        d['num_header_lines']=firstdatalineind
        d['num_data_rows']=nrows
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
        runp=tryprependpath(RUNFOLDERS, runp)

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

#need interpretheaderbool on eche to get the column_headings?
readdatafiledict=dict([\
    ('eche', lambda ext, lines:ext=='.txt' and readechemtxt('', lines=lines, interpretheaderbool=False) or smp_dict_generaltxt('', lines=lines, addparams=True,returnsmp=False)), \
    ('uvis', lambda ext, lines:smp_dict_generaltxt('', lines=lines, addparams=True,returnsmp=False)), \
    ('pets', lambda ext, lines:read_dta_pstat_file('', lines=lines, addparams=True)), \
    ('xrfs', lambda ext, lines:None), \
    ])

def getanadefaultfolder(erroruifcn=None):

    timename=time.strftime('%Y%m%d.%H%M%S')

    folder=os.path.join(os.path.join(tryprependpath(ANAFOLDERS_L, ''), 'temp'), timename+'.incomplete')

    try:
        if not os.path.isdir(folder):
            os.mkdir(folder)
        return folder
    except:
        print folder
        if erroruifcn is None:
            return ''
        return erroruifcn('')

def timestampname():
    return time.strftime('%Y%m%d.%H%M%S')
def saveana_tempfolder(anafilestr, srcfolder, erroruifcn=None, skipana=True, anadict=None, analysis_type='temp', rundone='.run', movebool=True, savefolder=None, saveanafile=True):

    if srcfolder.endswith('.incomplete') and savefolder is None:
        rootfold, typefold=os.path.split(os.path.split(srcfolder)[0])
        if typefold=='temp':
            savefolder=os.path.join(os.path.join(rootfold, analysis_type), os.path.split(srcfolder)[1].rpartition('.')[0]+rundone)
        else:
            savefolder=srcfolder.rpartition('.')[0]+rundone#replace incomplete with run or done
        timename=os.path.split(srcfolder)[1].partition('.incomplete')[0]
    elif savefolder is None:
        timename=timestampname()
        savefolder=os.path.join(os.path.join(tryprependpath(ANAFOLDERS_L, ''), analysis_type), timename+rundone)
    else:
        timename=os.path.split(savefolder)[1]
        if timename.count('.')>1:
            timename='.'.join(timename.split('.')[:2])
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
    if len(srcfolder)>0:
        if os.path.normpath(srcfolder)!=os.path.normpath(savefolder):#may be the same folder in which case skip to writing the .ana
            for fn in os.listdir(srcfolder):
                if fn.startswith('.') or '.db' in fn:
                    continue
                if skipana and (fn.endswith('.ana') or fn.endswith('.pck')):
                    continue
                if movebool:
                    shutil.move(os.path.join(srcfolder, fn), os.path.join(savefolder, fn))
                else:
                    shutil.copy(os.path.join(srcfolder, fn), os.path.join(savefolder, fn))
            if movebool:
                try:
                    os.rmdir(srcfolder)
                except:
                    print 'The old folder still exists due to a problem deleting it: ', srcfolder
    if saveanafile:
        savep=os.path.join(savefolder, '%s.ana' %timename)
        saveanafiles(savep, anafilestr=anafilestr, anadict=anadict)
    return savefolder

def saveanafiles(anapath, anafilestr=None, anadict=None, changeananame=False):
    if changeananame and not anadict is None:
        anadict['name']='.'.join(os.path.split(anapath)[1].split('.')[:2])
    if anafilestr is None:
        if anadict is None:
            print 'nothing saved to ', anapath
            return
        anafilestr=strrep_filedict(anadict)

    with open(anapath, mode='w') as f:
        f.write(anafilestr)
    if anadict is None:
        return
    saveanadict=copy.deepcopy(anadict)
    convertstrvalstonum_nesteddict(saveanadict)
    convertfilekeystofiled(saveanadict)
    with open(anapath.replace('.ana', '.pck'), mode='w') as f:
        pickle.dump(saveanadict, f)

def readana(p, erroruifcn=None, stringvalues=False, returnzipclass=False):
    if not  (((p.endswith('ana') or p.endswith('pck')) and (os.path.exists(p)) or ('.zip' in p and os.path.exists(os.path.split(p)[0])) ) ):# if .zip only tests fo existence of .zip file
        if erroruifcn is None:
            if returnzipclass:
                return {}, False
            else:
                return {}
        p=erroruifcn('select ana/pck file to open')
        if len(p)==0:
            if returnzipclass:
                return {}, False
            else:
                return {}
    if stringvalues and p.endswith('pck'):
        p=p.rpartition('pck')[0]+'ana'
    if not (os.path.exists(p) or ('.zip' in p and os.path.exists(os.path.split(p)[0])) ):# if .zip only tests fo existence of .zip file
        if erroruifcn is None:
            if returnzipclass:
                return {}, False
            else:
                return {}
        p=erroruifcn('for text-only must use .ana file')
        if len(p)==0:
            if returnzipclass:
                return {}, False
            else:
                return {}
    zipclass=gen_zipclass(p)
    if zipclass and p.endswith('.zip'):#can get here with either a .zip path or a .zip joined with a filename. if .zip get the .ana
        fnl=[fn for fn in zipclass.archive.namelist() if fn.endswith('.ana') and not fn.startswith('._')]
        if len(fnl)==0:
            if returnzipclass:
                return {}, False
            else:
                return {}
        p=os.path.join(p, fnl[0])
    if p.endswith('pck'):
        if zipclass:
            anadict=zipclass.loadpck(p)
        else:
            with open(p, mode='r') as f:
                anadict=pickle.load(f)
    else:
        if zipclass:
            lines=zipclass.readlines(p)
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
    if returnzipclass:
        return anadict, zipclass
    else:
        if zipclass:
            zipclass.close()
        return anadict

def create_techd_for_xrfs_exp(techd, openandreadlinesfcn):#not tested. 20170112 - this deifnitely has issues like  doesn't hjave these attributes, and looks like it is meant to add sample_no to each spectrum file but in example I see the sample_no is already there
    if not ('batch_summary_files' in techd.keys() and 'spectrum_files' in techd.keys() and len(techd['batch_summary_files'])==1):
        return techd#assume all fileattr lines have file_type;keys;numhead;numdata and there's no way to get sample_no so just leave the techd along
    batchcsv_fn, batchcsv_fileattrstr=techd['batch_summary_files'].items()[0]
    if not ('Inte' in batchcsv_fileattrstr and 'StgLabel' in batchcsv_fileattrstr and batchcsv_fileattrstr.count(';')==3):
        return techd
    ft, keystr, numheadstr, numdatstr=batchcsv_fileattrstr.split(';')
    nh=int(numheadstr.strip())
    keys=keystr.split(',')
    selcolinds=[keys.index('Inte'), keys.index('StgLabel')]
    lines=openandreadlinesfcn(batchcsv_fn)
    filelabs, stglabs=readtxt_selectcolumns('', selcolinds=selcolinds, delim='\t', num_header_lines=nh, lines=lines, floatintstr=str)
    typed=techd['spectrum_files']
    for fn, fileattrstr in typed.iteritems():
        fnlab=fn.partition('_')[0]
        if not fnlab in fnlabs:
            continue
        smpstr=stglabs[fnlabs.index(fnlab)]
        typed[fn]='%s;%s' %(fileattrstr, smpstr)
#p=r'K:\experiments\xrfs\rcp template\20160104-VCuMn-21964.done\long1.CSV'
#ans=readtxt_selectcolumns(p, selcolinds=None, delim=',', num_header_lines=7, lines=[], floatintstr=str)


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

def get_data_rcp_dict__echerunfile(run_path, file_name):
    if not run_path.endswith('.zip'):
        run_path+='.zip'
    runp=tryprependpath(RUNFOLDERS,run_path)
    zc=ZipClass(runp)
    rcpfn=[fn for fn in zc.archive.namelist() if fn.endswith('.rcp')][0]
    rcplines=zc.readlines(rcpfn)
    d=filedict_lines(rcplines)
    #d['reference_vrhe']
    datalines=zc.readlines(file_name)
    datad=readechemtxt('', lines=datalines, interpretheaderbool=True)
    for k, v in datad.iteritems():
        d[k]=v
    return d

def writeudifile(p, udi_dict):#ellabels, comps, xy, Q, Iarr, sample_no and plate_id
    metastrlist=[];mtrpnstrlist=[]
    compstrlist=[]
    depstrlist=[]
    countstrlist=[]
    if 'ellabels' in udi_dict.keys() and 'comps' in udi_dict.keys():
        els=udi_dict['ellabels']
        elstr=','.join(els)
        metastrlist+=['M=%d' %(len(els)), 'Elements=%s' %(elstr), 'Composition=%s' %(elstr)]
        for lab, carr in zip(els, udi_dict['comps'].T):
            compstrlist+=[lab+'='+','.join(['%.4f' %v for v in carr])]

    if 'xy' in udi_dict.keys():
        metastrlist+=['Deposition=X,Y']
        if 'plate_id' in udi_dict.keys():
            if isinstance(udi_dict['plate_id'], (list, numpy.ndarray)) and isinstance(udi_dict['plate_id'][0], (int, float, str)):
                if isinstance(udi_dict['plate_id'][0], str):
                    udi_dict['plate_id']=list(udi_dict['plate_id'])
                else:
                    udi_dict['plate_id']=['%d' %v for v in udi_dict['plate_id']]
            elif not isinstance(udi_dict['plate_id'], (list, numpy.ndarray)):
                if isinstance(udi_dict['plate_id'], (int, float)):
                    udi_dict['plate_id']='%d' %udi_dict['plate_id']
                udi_dict['plate_id']=[udi_dict['plate_id']]*len(udi_dict['xy'])
        for lab, arr, fmt in [('X=', udi_dict['xy'][:, 0], '%.2f'), ('Y=', udi_dict['xy'][:, 1], '%.2f')]+\
                ([('sample_no=', udi_dict['sample_no'], '%d')] if 'sample_no' in udi_dict.keys() else [])+\
                ([('plate_id=', udi_dict['plate_id'], '%s')] if 'plate_id' in udi_dict.keys() else []):
            depstrlist+=[lab+','.join([fmt %v for v in arr])]




    if 'Motorpns' in udi_dict.keys() and 'mxy' in udi_dict.keys():
        metastrlist+=['Motorpns=%s' %(','.join(udi_dict['Motorpns']))]
        for lab, arr, fmt in [('mX=', udi_dict['mxy'][:, 0], '%.2f'), ('mY=', udi_dict['mxy'][:, 1], '%.2f')]+\
                ([('specind=', udi_dict['specind'], '%d')] if 'specind' in udi_dict.keys() else []):
            if not  numpy.any(numpy.isnan(arr)):
                mtrpnstrlist+=[lab+','.join([fmt %v for v in arr])]

    if 'Normalize' in udi_dict.keys():
        metastrlist+=['Normalize=%s' %(udi_dict['Normalize'])]

    if 'CompType' in udi_dict.keys():
        metastrlist+=['CompType=%s' %(udi_dict['CompType'])]

    qcounts=udi_dict['Iarr']
    metastrlist+=['N=%d' %len(qcounts)]

    for i in range(len(qcounts)+1):
        if i==0:
            #countstrlist+=['Q=']
            l='Q='
            arr1=udi_dict['Q']
        else:
            #countstrlist+=['I%d=' %i]
            l='I%d=' %i
            arr1=qcounts[i-1]
        countstrlist+=[l+','.join(['%.5e' %v for v in arr1])]

    metastr='\n'.join(['// Metadata']+metastrlist)
    mtrpndata='\n'.join(['// Motorpns data']+mtrpnstrlist) if len(mtrpnstrlist)>0 else ''
    depstr='\n'.join(['// Deposition data']+depstrlist) if len(depstrlist)>0 else ''
    compstr='\n'.join(['// Composition data']+compstrlist) if len(compstrlist)>0 else ''
    countstr='\n'.join(['//Integrated counts data']+countstrlist)

    filestr='\n\n'.join([metastr, mtrpndata, depstr, compstr, countstr])
    filestr=filestr.replace('nan','NaN')
    f=open(p, mode='w')
    f.write(filestr)
    f.close()


def create_udi_anas(udipath, udi_dict, anadict=None, anafolder=None, anadict_comps=None, anafolder_comps=None):
    #TODO open anadict and anadict_comps if they are paths

    csvp=os.path.join(anafolder_comps, udi_dict['fom_file_comps'])
    csvfiled=anadict_comps[udi_dict['anak_comps']]['files_multi_run']['fom_files'][udi_dict['fom_file_comps']]
    compsfomd=readcsvdict(csvp, csvfiled, returnheaderdict=False)
    compkeys=[k for k in csvfiled['keys'] if udi_dict['fomname_split_comps'] in k]
    udi_dict['ellabels']=[k.partition(udi_dict['fomname_split_comps'])[0] for k in compkeys]

    smp_fn_filed=sorted([(filed['sample_no'], fn, filed) for anarunk in [anarunk for anarunk in anadict[udi_dict['anak']].keys() if anarunk.startswith('files_')] \
              for fn, filed in anadict[udi_dict['anak']][anarunk][udi_dict['ana_file_type']].items() \
                  if 'sample_no' in filed.keys() and filed['sample_no'] in compsfomd['sample_no'] and 'keys' in filed.keys() and udi_dict['q_key'] in filed['keys'] and udi_dict['intensity_key'] in filed['keys']])
    if len(smp_fn_filed)==0:
        return

    smps=[smp for smp, fn, filed in smp_fn_filed]
    udi_dict['sample_no']=numpy.array(smps)
    compsmplist=list(compsfomd['sample_no'])
    inds_compsfomd=[compsmplist.index(smp) for smp in smps]
    udi_dict['comps']=numpy.array([compsfomd[k][inds_compsfomd] for k in compkeys]).T

    udi_dict['Iarr']=[]
    for smp, fn, filed in smp_fn_filed:
        p=os.path.join(anafolder, fn)
        datad=readcsvdict(p, filed, returnheaderdict=False)
        qvals=datad[udi_dict['q_key']]
        if 'Q' in udi_dict.keys():
            if len(qvals)!=len(udi_dict['Q']) or ((udi_dict['Q']-qvals)**2).sum()>(.01*(qvals**2).sum()):#proxy for equivlanet q arrays
                print 'incommensute q arrays - cancelling udi'
                return
        else:
            udi_dict['Q']=qvals
        udi_dict['Iarr']+=[datad[udi_dict['intensity_key']]]
    udi_dict['Iarr']=numpy.array(udi_dict['Iarr'])

    pmap_path=getplatemappath_plateid(str(udi_dict['plate_id']))
    pmdlist=readsingleplatemaptxt(pmap_path)
    pmsmps=[d['sample_no'] for d in pmdlist]
    udi_dict['xy']=numpy.array([[pmdlist[pmsmps.index(smp)]['x'], pmdlist[pmsmps.index(smp)]['y']] for smp in smps])

    writeudifile(udipath, udi_dict)

def readudi(fl,fltyp='src'):
    def getval(valstr,dtype=numpy.float32,sep=','):
        if sep in valstr:
            return [dtype(x) for x in valstr.split(sep)]
        else:
            return dtype(valstr)
    dtypes=dict([('Metadata',str),('Motorpns data',numpy.float32),('Deposition data',numpy.float32),('Composition data',numpy.float32),('Integrated counts data',numpy.float32)])

    filed={}
    if fltyp=='src':
        with open(fl,'r') as fls:
            for line in fls.readlines():
                line=line.rstrip('\n')
                if line.startswith('//'):
                    key=line.split('//')[-1].strip()
                    filed[key]={}
                elif line.strip()!='':
                    try:
                        filed[key]=dict(filed[key].items()+[(line.split('=')[0],getval(line.split('=')[-1],dtype=dtypes[key]))])
                    except:
                            print 'Error encountered for line %s' %(line)
#                        continue
        datad={}
        Ikeys=filed['Integrated counts data'].keys()
        Ikeys.remove('Q')
        datad['Iarr']=numpy.array([filed['Integrated counts data'][idx] for idx in sorted(Ikeys,key=lambda x: int(x.split('I')[-1])) if idx.startswith('I')])
        try:
            datad['mxy']=numpy.array([filed['Motorpns data'][x] for x in ['mX','mY']]).T
        except:
            pass
        datad['xy']=numpy.array([filed['Deposition data'][x] for x in ['X','Y']]).T
        datad['comps']=numpy.array([filed['Composition data'][x] for x in filed['Metadata']['Composition']])
        try:
            datad=dict(datad.items()+filed['Metadata'].items()+[(mkey,filed['Motorpns data'][mkey]) for mkey in filed['Motorpns data'].keys() if mkey not in ['mX,mY']]+\
        [(dkey,filed['Deposition data'][dkey]) for dkey in filed['Deposition data'].keys() if dkey not in ['X','Y']]+[('Q',filed['Integrated counts data']['Q'])])
        except:
            datad=dict(datad.items()+filed['Metadata'].items()+\
        [(dkey,filed['Deposition data'][dkey]) for dkey in filed['Deposition data'].keys() if dkey not in ['X','Y']]+[('Q',filed['Integrated counts data']['Q'])])
        datad['ellabels']=datad.pop('Elements',None)
        datad['comps']=datad['comps'].T
    return datad


def sort_dict_keys_by_counter(d, keystartswith='ana__'):
    try:
        sorttups=sorted([(int(k[len(keystartswith):]), k) for k in d.keys() if k.startswith(keystartswith)])
        kl=map(operator.itemgetter(1), sorttups)
    except:
        kl=sorted([k for k in d.keys() if k.startswith(keystartswith)])
    return kl

def copyfolder_1level(srcfolder, savefolder, movebool=False):
    if os.path.normpath(srcfolder)==os.path.normpath(savefolder):
        return 'Cannot copy - same folder'
    if not os.path.isdir(savefolder):
        try:
            os.mkdir(savefolder)
        except:
            return 'Cannot copy - could not create source directory'

    for fn in os.listdir(srcfolder):
        if fn.startswith('.'):
            continue
        if movebool:
            shutil.move(os.path.join(srcfolder, fn), os.path.join(savefolder, fn))
        else:
            shutil.copy(os.path.join(srcfolder, fn), os.path.join(savefolder, fn))
    return False

def gen_pathd_absorrel_expanapath(p, desttype='eche', exp=False, only_check_temp=False):#p is the folder of an exp or ana , validate that it is where it should be (on J or K in desttype folder) or give new destpath
    if not (os.path.isdir(p) and os.path.isabs(p)):
        srcabs=prepend_root_exp_path(p, exp=exp)
    else:
        srcabs=p
    if '.copied' in srcabs: #found probably on J maybe on K but if so copied which means can't be temp
        return None
    if only_check_temp:
        kfold=tryprependpath(EXPFOLDERS_L if exp else ANAFOLDERS_L, '')
        if os.path.normpath(srcabs).startswith(os.path.normpath(kfold)) and (not 'temp' in p) and ('.done' in srcabs):#p is on K and not in temp so probably in a good place
            return None
        return {}#if onyl checking in temp and it is in temp (or not on K) then can't provide a solution
    deststartswith=tryprependpath(EXPFOLDERS_L if exp else ANAFOLDERS_L, desttype)
    if os.path.normpath(srcabs).startswith(os.path.normpath(deststartswith)):#already in desired place, could be in subfolder and don't check that as of now
        if not ('.run' in p):#then presumably is .done in K and will go to J soon
            return None
        #else this is going to make a .done copy in K and .run will stay there and will get cleaned up later
    foldname=os.path.split(p)[1].replace('.run', '.done')
    dest=os.path.join(deststartswith, foldname)
    destrel=(r'/'+os.path.join(desttype, foldname)).replace(chr(92),chr(47))
    return {'destabs':dest, 'destrel':destrel, 'srcabs':srcabs, 'srcrel':p}



def find_paths_in_ana_need_copy_to_anatype(anad, anatype):#find which ana=-containing paths are not on J or in anatype folder
    needcopy_dlist=[]
    for k, v in anad.iteritems():
        if k=='experiment_path':
            d=gen_pathd_absorrel_expanapath(v, desttype=anatype, exp=True)
            if d is None:
                continue
            d['anadkeylist']=['experiment_path']
            needcopy_dlist+=[d]
        elif k.startswith('ana__'):
            kl=[k]
            if 'parameters' in v.keys():
                kl+=['parameters']
                for count, auxk in enumerate(['aux_ana_path', 'aux_exp_path']):
                    if auxk in v['parameters'].keys():
                        d=gen_pathd_absorrel_expanapath(v['parameters'][auxk], desttype=anatype, exp=(count==1), only_check_temp=True)
                        if d is None:
                            continue
                        #d['anadkeylist']=kl+[auxk]
                        #needcopy_dlist+=[d]
                        needcopy_dlist+=[None]#an aux could be xrfs so not needed to be copied to this place but just can't be in temp
    return needcopy_dlist
###

def get_serial_plate_id(pid):
    if isinstance(pid, int):
        pid='%d' %pid
    checksum=numpy.array([eval(ch) for ch in pid]).sum()%10
    return '%s%d' %(pid, checksum)

def read_xrfs_batch_summary_csv(p, zipclass=None, select_columns_headings__maindict=[], include_inte_wt_at_subdicts=True, include_transitionslist_bool=False, read_sample_no_bool=False, includestrvals=False):
    d={}
    closezip=False
    if zipclass is None:#only close zip if opened it here (not if it was passed)
        zipclass=gen_zipclass(p)
        closezip=bool(zipclass)
    if zipclass:
        lines=zipclass.read(p).split('\r')
        if read_sample_no_bool:
            sp=os.path.join(os.path.split(p)[0], 'sample_no.txt')
            slines=zipclass.readlines(sp)
    else:
        with open(p, mode='r') as f:
            lines=f.read().split('\r')
        if read_sample_no_bool:
            sp=os.path.join(os.path.split(p)[0], 'sample_no.txt')
            with open(sp, mode='r') as f:
                slines=f.readlines()
    if read_sample_no_bool:
        d['sample_no']=[int(s.strip()) for s in slines if len(s.strip())>0]
    keys=None
    for count, l in enumerate(lines):
        if l.startswith('Inte,'):
            keys=l.strip().replace(' ','').split(',')
            lines=lines[count+1:]
            break
    if keys is None:
        return None


    if len(select_columns_headings__maindict)>0:
        selcolinds=[keys.index(s) for s in select_columns_headings__maindict]
        strarr=readtxt_selectcolumns('', selcolinds=selcolinds, delim=',', num_header_lines=0, lines=lines, floatintstr=str)
        for k, a in zip(select_columns_headings__maindict, strarr):
            if '.' in a[0] or 'NaN' in a:
                d[k]=numpy.float32([v.strip() for v in a])
            elif a[0].strip().isdigit():
                d[k]=numpy.int32([v.strip() for v in a])
            elif includestrvals:
                d[k]=numpy.array([v.strip() for v in a])
    if include_inte_wt_at_subdicts:
        column_headings_sub_dict=['Inte', 'Wt%', 'At%']
        section_start_inds=[keys.index(s) for s in column_headings_sub_dict]
        num_transition_columns=section_start_inds[1]-section_start_inds[0]-1
        if include_transitionslist_bool:
            starti=section_start_inds[0]
            d['transitionslist']=keys[starti+1:starti+1+num_transition_columns]
        for starti, section_key in zip(section_start_inds, column_headings_sub_dict):
            d[section_key]={}
            d2=d[section_key]
            selcolinds=range(starti+1, starti+1+num_transition_columns)
            arr=readtxt_selectcolumns('', selcolinds=selcolinds, delim=',', num_header_lines=0, lines=lines, floatintstr=float)
            for ki, a in zip(selcolinds, arr):
                d2[keys[ki]]=a
    if closezip:
        zipclass.close()
    return d
