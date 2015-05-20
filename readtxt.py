import os.path, numpy
#sample number can be provided as "Sample####_*"  in filename or in header
def smp_dict_generaltxt(path, delim='\t'): # can have raw data files with UV-vis or ECHE styles or a fom file with column headings as first line, in which case smp=None
    smp=None
    fn=os.path.split(path)[1]
    if fn.startswith('Sample'):
        s=fn.partition('Sample')[2].partition('_')[0]
        try:
            smp=eval(s)
        except:
            smp=None
    if smp is None:
        smp=getsamplefromheader(path)
#    if smp is None:
#        return None, {}
    
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
        return None, {}
    
    
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
    return smp, d
    

    
def getsamplefromheader(path):
    trylist=getheadattrs(path, searchstrs=['Sample', 'Sample No', 'sample_no'])
    for v in trylist:
        if not v is None:
            return v
    return None
    
def getheadattrs(path, searchstrs=['Sample', 'Sample No', 'sample_no'], readbytes=1000):
    f=open(path, mode='r')
    s=f.read(readbytes)
    f.close()
    ret=[]
    for ss in searchstrs:
        if not ss in s:
            ret+=[None]
            continue
        vs=s.partition(ss)[2].partition('\n')[0].strip().strip(':').strip('=').strip()
        try:
            ret+=[eval(vs)]
        except:
            ret+=[None]
    return ret
