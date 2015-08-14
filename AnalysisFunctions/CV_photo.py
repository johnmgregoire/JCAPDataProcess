import numpy, copy,sys,os
if __name__ == "__main__":
    sys.path.append(os.path.split(os.getcwd())[0])

sys.path.append(os.path.split(os.path.realpath(__file__))[0])

from fcns_math import *
from fcns_io import *
from csvfilewriter import createcsvfilstr
from Analysis_Master import *


class Analysis__Ifin(Analysis_Master_nointer):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Ifin'
        self.requiredkeys=['I(A)']
        self.optionalkeys=[]
        self.fomnames=['I(A)_fin']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='I(A)'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name='I(A)_fin', colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')
    def fomtuplist_dataarr(self, dataarr):
        return [('I(A)_fin', dataarr[0][-1])]
        
class Analysis__Iave(Analysis_Master_nointer):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams=dict([('duration_s', 2.), ('num_std_dev_outlier', 2.), ('num_pts_outlier_window', 999999), ('from_end', True)])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Iave'
        self.requiredkeys=['I(A)', 't(s)']
        self.optionalkeys=[]
        self.fomnames=['I(A)_ave']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='I(A)'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name='I(A)_ave', colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')
    def fomtuplist_dataarr(self, dataarr):
        x, t=dataarr
        if self.params['from_end']:
            x=x[::-1]
            t=t[::-1]
        x=x[numpy.abs(t-t[0])<self.params['duration_s']]
        x=removeoutliers_meanstd(x, self.params['num_pts_outlier_window']//2, self.params['num_std_dev_outlier'])
        return [('I(A)_ave', x.mean())]

class Analysis__Pphotomax(Analysis_Master_inter):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams=dict([\
  ('frac_illum_segment_start', 0.4), ('frac_illum_segment_end', 0.95), \
  ('frac_dark_segment_start', 0.4), ('frac_dark_segment_end', 0.95), \
  ('illum_key', 'Toggle'), ('illum_time_shift_s', 0.), ('illum_threshold', 0.5), \
  ('illum_invert', 0), ('num_illum_cycles', 2), ('from_end', True)\
                                       ])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Pphotomax'
        #note that IllumBool is an intermediate of Iphoto caclualtion
        self.requiredkeys=['I(A)', 'Ewe(V)', 't(s)', 'IllumBool']#0th is array whose photoresponse is being calculate, -1th is the Illum signal, and the rest get processed along the way
        self.optionalkeys=[]
        #possible names, should eb changed 
        self.fomnames=['Pphotomax','Voc_interp', 'Vmicro', 'Isc']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='I(A)'
        self.plotparams['plot__1']['series__2']='IllumBool'
        self.plotparams['plot__2']={}
        self.plotparams['plot__2']['x_axis']='t(s)_dark,t(s)_ill,t(s)_ill'
        self.plotparams['plot__2']['series__1']='I(A)_dark,I(A)_ill,I(A)_illdiff'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name='I(A)_photo', colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name='I(A)_photo', colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')
    #this is the default fcn but with requiredkeys changed to relfect user-entered illum key
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
        self.requiredkeys[-1]=self.params['illum_key']
        self.num_files_considered, self.filedlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys)
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filedlist
    def fomtuplist_rawlend_interlend(self, dataarr):

        d=dict([(k, v) for k, v in zip(self.requiredkeys, dataarr)])
        ikey=self.params['illum_key']
        tshift=self.params['illum_time_shift_s']
        interdict={}
        if tshift!=0:
            newikey='IllumMod'
            illumtimeshift(d, ikey, 't(s)', tshift)
        if self.params['illum_invert']:
            d[ikey]=-1*d[ikey]

        interd={}
        err=calcdiff_ill_caller(d, interd, ikey=ikey, thresh=self.params['illum_threshold'], \
            ykeys=[self.requiredkeys[0]], xkeys=list(self.requiredkeys[1:-1]), \
            illfracrange=(self.params['frac_illum_segment_start'], self.params['frac_illum_segment_end']), \
            darkfracrange=(self.params['frac_dark_segment_start'], self.params['frac_dark_segment_end']))
        fomtuplist=[]
        for count, suffix in enumerate(['_illdiff', '_ill', '_dark']):
            illkey=self.requiredkeys[0]+suffix
            fomk=self.fomnames[count]
            #try:
            if err or len(interd[illkey])==0:
                return [(fomk, numpy.nan) for fomk in self.fomnames], {}, {}

            ncycs=self.params['num_illum_cycles']
            fromend=self.params['from_end']
            if fromend:
                arr=interd[illkey][::-1]
            else:
                arr=interd[illkey]
            arr=arr[numpy.logical_not(numpy.isnan(arr))]
            if len(arr)<ncycs:
                fomtuplist+=[(fomk, numpy.nan)]
            else:
                fomtuplist+=[(fomk, arr[:ncycs].mean())]

        return fomtuplist, dict([('IllumBool', d['IllumBool'])]), interd
        #except:
        #    pass
        return [(fomk, numpy.nan) for fomk in self.fomnames], {}, {}
