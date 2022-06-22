import sys, os
import matplotlib.pyplot as plt
import numpy as np
import operator
############
projectroot=os.path.split(os.getcwd())[0]
sys.path.append(projectroot)
sys.path.append(os.path.join(projectroot,'QtForms'))
sys.path.append(os.path.join(projectroot,'AuxPrograms'))
sys.path.append(os.path.join(projectroot,'OtherApps'))


from fcns_io import *
from fcns_ui import *



import matplotlib.colors as colors
import matplotlib.cm as cm


fomkl=['max.FETotal','H2.charge.C','CH4.charge.C','C2H4.charge.C']

def get_colors_fom_cmap(fomarr, vmin, vmax, cmap):#if need over/under colors those should have been already set via cmap.set_under, cmap.set_over
    norm=colors.Normalize(vmin=vmin, vmax=vmax, clip=False)
    sm=cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array(fomarr)
    cols=np.float32(list(map(sm.to_rgba, fomarr)))[:, :3]
    return cols
 

#plt.plot([0,1],[0,1])
#plt.show()

anap=r'L:\processes\analysis\temp\20190407.164248.run\20190407.164248.ana'#None

anad=readana(anap)

#plt.Figure()
anakl=sort_dict_keys_by_counter(anad)[2:]

plt.clf()
for fomcount,fomk in enumerate(fomkl):
    plt.subplot(len(fomkl),1,fomcount+1)
    labs=[]
    yl=[]
    for count, anak in enumerate(anakl):
        lab=anad[anak]['parameters']['loss_fcn']
        labs+=[lab]
        fn, fd=list(anad[anak]['files_multi_run']['fom_files'].items())[0]
        fomd=readcsvdict(os.path.join(os.path.split(anap)[0], fn), fd, returnheaderdict=False, zipclass=None, includestrvals=True)
        y=[tup[1] for tup in sorted(zip(fomd['sample_no'], fomd[fomk]))]
        yl+=[y]
    
    yarr=np.array(yl)
    smps=sorted(list(fomd['sample_no']))
    
    cols=get_colors_fom_cmap(list(range(len(smps))), 0, len(smps)-1, 'jet')
    
    #ytext=lambda count: (yarr.max()-yarr.min())/(len(smps)+2)*(count+1)+y.min()
    for count, (col, y, smp) in enumerate(zip(cols, yarr.T, smps)):
        plt.plot(list(range(len(y))), y, '-', marker='o', label=repr(smp),c=col)
        #plt.text(len(anakl)+1, ytext(count), `smp`, col=col)
    
    plt.xlim(-0.5, len(anakl)+1.5)
    plt.legend(loc=1)
    
    plt.ylabel(fomk)
    ax=plt.gca()
    ax.set_xticks(list(range(len(labs))))
    ax.set_xticklabels(labs,rotation=30.)
plt.subplots_adjust(left=.1,right=.99,top=.99,bottom=.12,hspace=.07)
plt.suptitle(os.path.split(anap)[1])
plt.show()
