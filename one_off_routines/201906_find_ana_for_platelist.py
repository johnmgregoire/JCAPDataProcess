import numpy, copy, operator
import time,pickle
if __name__ == "__main__":
    import os, sys
    #__file__=r'D:\Google Drive\Documents\PythonCode\JCAP\JCAPDataProcess\AnalysisFunctions\ecms.py'
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AnalysisFunctions'))
from fcns_io import *
from fcns_ui import *


serial_list='35929,27830,27830,35884,35941,31026,35749,31060,31082,41353,35491,27852,35547,35839,35907,35772,35558,35378'.split(',')
typelist=['xrfs']

plate_list=[s[:-1] for s in serial_list]
resultsd={}
for pid in plate_list:
    resultsd[pid]=[]
    d=importinfo(pid)
    resultsd[pid]+=[''.join(getelements_plateidstr(pid))]
    if not 'analyses' in d:
        continue
    l=[]
    for k,ad in d['analyses'].items():
        if ad['type'] in typelist:
            l+=[(float(os.path.split(ad['path'])[1][:15]),ad['path'])]
    resultsd[pid]+=[t[1] for t in sorted(l)[::-1]]

for k,v in resultsd.items():
    print ','.join([k]+v)