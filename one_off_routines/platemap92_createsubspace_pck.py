import numpy as np
import itertools as it
import sys, copy,pickle, os, operator
import matplotlib.pyplot as plt

wd=os.getcwd()
PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.join(PyCodePath,'PythonCompositionPlots'))
from myquaternaryutility import QuaternaryPlot
from myternaryutility import TernaryPlot

sys.path.append(os.path.join(PyCodePath,'JCAPGeneratePrintCode'))
from readplatemap import *

p=r'J:\hte_jcap_app_proto\map\0092-04-0100-mp.txt'
dlist=readsingleplatemaptxt(p)
pmchans=['A','B','C','D','E']
#code 0 where theres nonzero in 5 elements (the ones with 0s are an error not worth fixing), also exlucde 5 end members comps
dlist=[d for d in dlist if d['code']==0 and np.array([d[k] for k in pmchans]).sum()>0. and np.array([d[k] for k in pmchans]).max()<1.]

comps_all=np.array([[d[k] for k in pmchans] for d in dlist])
print len(dlist)

intervs=40
#comps1=[(1.0*b/intervs, 1.0*c/intervs, 1.0*d/intervs, 1.0*(intervs-a-b-c-d)/intervs, 1.0*a/intervs) for a in np.arange(0,intervs+1)[::-1] for b in np.arange(0,intervs+1-a) for c in np.arange(0, intervs+1-a-b) for d in np.arange(0, intervs+1-a-b-c)][::-1]
#comps1=np.array(comps1)

tol=0.07



n=len(pmchans)

chaninds=range(n)

inds_comb=[s for s in it.permutations(chaninds, 2)]

def gen_target_comp(inds):
    i0,i1=inds
    c=np.zeros(n,dtype='float64')
    c[i0]=0.6667
    c[i1]=0.3333
    return c

within_tol_calc=lambda c, tc:(np.sum((c-tc)**2)/2.)**.5<=tol

subspace_dict={}
for indpair in inds_comb:
    tc=gen_target_comp(indpair)
    inds_dlist=np.array([i for i, c in enumerate(comps_all) if within_tol_calc(c, tc)])
    sortedtups=sorted([((comps_all[i]>0.).sum(dtype='int32'), comps_all[i][indpair[0]], comps_all[i][indpair[1]], dlist[i]['Sample'], i) for i in inds_dlist])
    
    inds_dlist2=map(operator.itemgetter(-1), sortedtups)
    subdlist=[dlist[i] for i in inds_dlist2]
    subspace_dict[indpair]={}
    subspace_dict[indpair]['sample_no_list']=[d['Sample'] for d in subdlist]
    subspace_dict[indpair]['sample_no_array']=np.array(subspace_dict[indpair]['sample_no_list'])
    comps1=copy.copy(comps_all[inds_dlist2, :])
    subspace_dict[indpair]['comps']=comps1
    subspace_dict[indpair]['comp_order_array']=(comps1>0.).sum(axis=1, dtype='int32')
    subspace_dict[indpair]['comp_dist_array']=np.array([(np.sum((c-tc)**2)/2.)**.5 for c in comps1])
    indtrio=sorted(list(set(chaninds).difference(set(indpair))))
    a_to_b=comps1[:, indpair[0]]/comps1[:, indpair[1]]
    ab_comp=comps1[:, indpair[0]]/(comps1[:, indpair[1]]+comps1[:, indpair[0]])
    subspace_dict[indpair]['host_ab_ratio_array']=a_to_b
    comporder=subspace_dict[indpair]['comp_order_array']
    subspace_dict[indpair]['subplot_info_each_alloy_chan']={}
    subplotd=subspace_dict[indpair]['subplot_info_each_alloy_chan']
    subplotd['alloy_chan_inds']=indtrio
    
    for i in indtrio:
        subplotd[i]={}
        ad=subplotd[i]
        j, k=sorted(list(set(indtrio).difference(set([i]))))
        ad['other_2_inds__subplot']=(j, k)
        tups_for_sorting=[(comporder[ind], c[i], a_to_b[ind], c[j], ind) for ind, c in enumerate(comps1) if comporder[ind]==2 or c[i]>0.]
        sortedtups=sorted(tups_for_sorting)
        ad['inds_from_spinel_space']=map(operator.itemgetter(-1), sortedtups)
        inds=ad['inds_from_spinel_space']
        ad['comp_order__subplot']=comporder[inds]
        ad['comps__subplot']=comps1[inds, :]
        ad['select_el_conc__subplot']=comps1[inds, i]
        ad['host_ab_ratio__subplot']=a_to_b[inds]
        ad['host_ab_comp__subplot']=ab_comp[inds]
        ad['sample_no_array__subplot']=subspace_dict[indpair]['sample_no_array'][inds]
        
        map(operator.itemgetter(-1), sortedtups)
        
        partialtups=[(tup[0], tup[1]) for tup in sortedtups]
        tupsetlist=sorted(list(set(partialtups)))
        row_index=[tupsetlist.index(tup) for tup in partialtups]
        ad['row_index__subplot']=row_index


        shape_types=numpy.zeros(len(row_index), dtype='int32')
        shape_types[np.where(ad['host_ab_ratio__subplot'][:-1]==ad['host_ab_ratio__subplot'][1:])[0]]=-1
        shape_types[np.where(shape_types==-1)[0]+1]=1
#        shape_types=[0]
#        count=0
#        for rprev, r in zip(ad['host_ab_ratio__subplot'][:-1], ad['host_ab_ratio__subplot'][1:]):
#            rprev, r=ad['a_to_b'][indnow], ad['a_to_b'][indnext]
#            if rprev!=r:
#                count+=1
#                shape_types+=[0]
#            else:
#                shape_types[-1]=1
#                shape_types+=[2]
            #square_index+=[count]
        ad['shape_types__subplot']=shape_types
#        plt.figure()
#        for x, y, t, o in zip(ad['host_ab_ratio__subplot'], ad['row_index__subplot'], ad['shape_types__subplot'], ad['comp_order__subplot']):
#            v0=[(-1, -1), (-1, 1), (1, 1), (1, -1)]
#            v1=[(-1, 1), (1, 1), (1, -1)]
#            v2=[(-1, -1), (-1, 1),(1, -1)]
#            varr=[v0, v1, v2]
#            plt.plot(x, y,c=['b', 'm', 'orange', 'g'][o-2], mec='k', marker=varr[t], ms=20)#['s', 'v', '^'][t]
#        plt.ylim(-.5, 7.5)
#        plt.xlim(1.4, 2.9)
#        plt.show()

sp=r'K:\users\hte\ProjectSummaries\spinel_alloys\platemap_comps\0092-subspace_subplot_dict.pck'
with open(sp, mode='wb') as f:pickle.dump(subspace_dict, f)

#
#
#n=len(comps1[0])
#
#inds=range(n)
#
#inds_comb=[list(s) for s in it.permutations(inds, 2)]
#
#def gen_target_comp(inds):
#    i0,i1=inds
#    c=np.zeros(n,dtype='float64')
#    c[i0]=0.6667
#    c[i1]=0.3333
#    return c
#    
#inds_comb=inds_comb[:1]
#
#target_comps=[gen_target_comp(inds) for inds in inds_comb]
#
#
#within_tol_calc=lambda c, tc:(np.sum((c-tc)**2)/2.)**.5<=tol
#
#comps=np.array([c for c in comps1 if True in [within_tol_calc(c, tc) for tc in target_comps]])
#
##with open(sp,mode='wb') as f:
##    pickle.dump(comps,f)
##
##print len(comps), len(comps1)
#
#
##inds=np.where(comps[:, 2:].sum(axis=1)==0.)[0]
##print comps[inds]
#
#print 'num comps'
#print len(comps)
#print 'num comps in unary,...quinary spaces'
#print [len(np.where((comps>0.).sum(axis=1)==n)[0]) for n in range(1, 6)]
#print 'num A conc in unary,...quinary spaces'
#print [len(set(comps[np.where((comps>0.).sum(axis=1)==n)[0]][:, 0])) for n in range(1, 6)]
#
#n=2
#qcomps=comps[np.where((comps>0.).sum(axis=1)==n)[0]]
#inds=np.argsort(qcomps[:, 1])
#print 'binary comps'
#for i in inds:
#    print qcomps[i]
#n=3
#qcomps=comps[np.where((comps>0.).sum(axis=1)==n)[0]]
#inds=np.argsort(qcomps[:, 1])
#print 'ternary comps'
#for i in inds:
#    print qcomps[i]
#n=5
#qcomps=comps[np.where((comps>0.).sum(axis=1)==n)[0]]
#inds=np.argsort(qcomps[:, 1])
#print 'quinary comps'
#for i in inds:
#    print qcomps[i]
#
#plt.figure()
#tc=TernaryPlot((1, 1, 1))
#
#i=np.argmin(comps[:, 0])
#cencomp=comps[i]
#cencomp=np.array([0.6667, 0.3333, 0., 0., 0.])
#rad=np.array([tc.compdist(cencomp, c) for c in comps])
#ternadds=comps[:, 2:]
#inds=np.where(ternadds.sum(axis=1)>0)[0]
##rad=rad[inds]
##ternadds=ternadds[inds]
#ternadds_norm=ternadds/ternadds.sum(axis=1)[:, np.newaxis]
#
#xa=np.zeros(len(rad), dtype='float64')
#ya=np.zeros(len(rad), dtype='float64')
#xa[inds], ya[inds]=tc.toCart(ternadds_norm[inds])
#xcen, ycen=tc.toCart([np.ones(3, dtype='float64')/3.])
#xa-=xcen[0]
#ya-=ycen[0]
#ang=np.array([0. if xv==0. else np.arctan2(yv, xv) for xv, yv in zip(xa, ya)])
#rad[xa==0.]=0.
#zp=comps[:, 0]/comps[:, :2].sum(axis=1)-0.6667
#radxy=np.sqrt(rad**2-zp**2)
#xp=rad*np.cos(ang)
#yp=rad*np.sin(ang)
#
#cols=np.zeros((len(rad), 3), dtype='float64')
#cols[inds, :]=tc.rgb_comp(ternadds_norm[inds])
#plt.clf()
#plt.subplot(111, projection='3d')
#ax=plt.gca()
#ax.set_axis_off()
#ax.set_aspect('equal')
#ax.figure.hold('True')
#
##for xv, yv, zv, c in zip(xp, yp, zp, cols):
##    print xv, yv, zv, c
##    ax.scatter([xv], [yv], [zv], color=c, edgecolor='none')
#ax.scatter(xp, yp, zp, color=cols, edgecolor='none')
#
#ax.set_aspect(1.)
#plt.show()
#
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
#from quaternary_faces_shells import ternaryfaces_shells
#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#try:
#    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
#except ImportError:
#    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
#from matplotlib.figure import Figure
#
#
#class plotwidget(FigureCanvas):
#    def __init__(self, parent, width=12, height=6, dpi=72, projection3d=False):
#
#        #plotdata can be 2d array for image plot or list of 2 1d arrays for x-y plot or 2d array for image plot or list of lists of 2 1D arrays
#        self.projection3d=projection3d
#        self.fig=Figure(figsize=(width, height), dpi=dpi)
#        if projection3d:
#            self.axes=self.fig.add_subplot(111, navigate=True, projection='3d')
#        else:
#            self.axes=self.fig.add_subplot(111, navigate=True)
#
#        self.axes.hold(True)
#        FigureCanvas.__init__(self, self.fig)
#        self.setParent(parent)
#        #self.parent=parent
#        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
#        FigureCanvas.updateGeometry(self)
#        #NavigationToolbar(self, parent)
#        NavigationToolbar(self, self)
#
#        self.mpl_connect('button_press_event', self.myclick)
#        self.clicklist=[]
#        self.cbax=None
#    
#
#    def myclick(self, event):
#        if not (event.xdata is None or event.ydata is None):
#            arrayxy=[event.xdata, event.ydata]
#            print 'clicked on image: array indeces ', arrayxy, ' using button', event.button
#            self.clicklist+=[arrayxy]
#            self.emit(SIGNAL("genericclickonplot"), [event.xdata, event.ydata, event.button, event.inaxes])
#
#class dialog(QDialog):
#    def __init__(self, comps, parent=None, title='', folderpath=None):
#        super(dialog, self).__init__(parent)
#
#        
#        plotw=plotwidget(self)
#        
#        ax=plotw.axes
#        
#
#        inds=np.where(comps[:, -1]==0.)[0]
#        comps=comps[inds, :-1]
#        #print comps.shape
#        stpquat=QuaternaryPlot(ax)
#        ax.cla()
#        cols=stpquat.rgb_comp(comps)
#        #stpquat.scatter(comps, c=cols, s=100, edgecolors='none')
#        #stpquat.label()
#
#        self.tf=ternaryfaces_shells(ax, nintervals=intervs)
#        self.tf.label()
#        self.tf.scatter(comps, cols, skipinds=[0, 1, 2, 3], s='patch')
#        
#        #only select comps
#        plotw2=plotwidget(self, projection3d=True)
#        
#        
#        ax=plotw2.axes
#        #unary
#        
#        stpquat=QuaternaryPlot(ax)
#
#        stpquat.scatter(comps, c=cols, s=100, edgecolors='none')
#        stpquat.label()
#
#        
#        QObject.connect(plotw, SIGNAL("genericclickonplot"), self.plotclick)
#        QObject.connect(plotw2, SIGNAL("genericclickonplot"), self.plotclick)
#        
#        mainlayout=QGridLayout()
#        mainlayout.addWidget(plotw, 0, 0)
#        mainlayout.addWidget(plotw2, 1, 0)
#
#        
#        self.setLayout(mainlayout)
#    
#    def plotclick(self, coords_button_ax):
#        xc, yc, button, ax=coords_button_ax
#        print self.tf.toComp(xc, yc)
#        
#class MainMenu(QMainWindow):
#    def __init__(self):
#        super(MainMenu, self).__init__(None)
#        
#        x=dialog(comps)
#        x.exec_()
#        
#mainapp=QApplication(sys.argv)
#form=MainMenu()
#form.show()
#form.setFocus()
#mainapp.exec_()
