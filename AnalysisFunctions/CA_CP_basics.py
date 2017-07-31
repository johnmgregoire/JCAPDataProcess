import numpy, copy,sys,os
if __name__ == "__main__":
    sys.path.append(os.path.split(os.getcwd())[0])

sys.path.append(os.path.split(os.path.realpath(__file__))[0])

from fcns_math import *
from fcns_io import *
from csvfilewriter import createcsvfilstr
from Analysis_Master import *

referenceshiftfcn=lambda x, e0, redoxstr:(x-e0)*((-1)**(not redoxstr in ['FeCp2+/0','Fe(CN)6-3/-4','O2/H2O']))


class Analysis__Imax(Analysis_Master_nointer):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Imax'
        self.requiredkeys=['I(A)']
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=['I.A_max']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='I(A)'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=self.fomnames[0], colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')
    def fomtuplist_dataarr(self, dataarr, filed):
        return [(self.fomnames[0], numpy.max(dataarr[0]))]


class Analysis__Imin(Analysis_Master_nointer):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Imin'
        self.requiredkeys=['I(A)']
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=['I.A_min']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='I(A)'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=self.fomnames[0], colormap='jet_r', colormap_over_color='(0.,0.,0.)', colormap_under_color='(0.5,0.,0.)')
    def fomtuplist_dataarr(self, dataarr, filed):
        return [(self.fomnames[0], numpy.min(dataarr[0]))]


class Analysis__Ifin(Analysis_Master_nointer):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Ifin'
        self.requiredkeys=['I(A)']
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=['I.A_fin']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='I(A)'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=self.fomnames[0], colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')
    def fomtuplist_dataarr(self, dataarr, filed):
        return [(self.fomnames[0], dataarr[0][-1])]

class Analysis__Efin(Analysis__Ifin):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Efin'
        self.requiredkeys=['Ewe(V)']
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=['E.V_fin']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='Ewe(V)'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=self.fomnames[0], colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')

class Analysis__Etafin(Analysis_Master_inter):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Etafin'
        self.requiredkeys=['Ewe(V)']
        self.optionalkeys=[]
        self.requiredparams=['reference_e0', 'redox_couple_type']
        self.fomnames=['Eta.V_fin']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='Eta(V)'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=self.fomnames[0], colormap='jet_r', colormap_over_color='(0.,0.,0.)', colormap_under_color='(0.5,0.,0.)')
    def fomtuplist_rawlend_interlend(self, dataarr, filed):
        eta=referenceshiftfcn(dataarr[0], filed['reference_e0'], filed['redox_couple_type'])
        return [(self.fomnames[0], eta[-1])], dict([('Eta(V)', eta)]), {}


class Analysis__Iave(Analysis_Master_nointer):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams=dict([('duration_s', 2.), ('num_std_dev_outlier', 2.), ('num_pts_outlier_window', 999999), ('from_end', True)])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Iave'
        self.requiredkeys=['I(A)', 't(s)']
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=['I.A_ave']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='I(A)'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=self.fomnames[0], colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')

    def avefcn(self, x, t):
        if self.params['from_end']:
            x=x[::-1]
            t=t[::-1]
        x=x[numpy.abs(t-t[0])<self.params['duration_s']]
        x=removeoutliers_meanstd(x, self.params['num_pts_outlier_window']//2, self.params['num_std_dev_outlier'])
        return [(self.fomnames[0], x.mean())]

    def fomtuplist_dataarr(self, dataarr, filed):
        x, t=dataarr
        return self.avefcn(x, t)

class Analysis__Eave(Analysis__Iave):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams=dict([('duration_s', 2.), ('num_std_dev_outlier', 2.), ('num_pts_outlier_window', 999999), ('from_end', True)])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Eave'
        self.requiredkeys=['Ewe(V)', 't(s)']
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=['E.V_ave']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='Ewe(V)'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=self.fomnames[0], colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')

class Analysis__Etaave(Analysis_Master_inter, Analysis__Iave):#this order is improtant, i.e. get perform() from master and avefcn from Iave
    def __init__(self):
        self.analysis_fcn_version='2'# changed FOM label from E.V_ave to Eta.V_ave on 20160212
        self.dfltparams=dict([('duration_s', 2.), ('num_std_dev_outlier', 2.), ('num_pts_outlier_window', 999999), ('from_end', True)])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Etaave'
        self.requiredkeys=['Ewe(V)', 't(s)']
        self.optionalkeys=[]
        self.requiredparams=['reference_e0', 'redox_couple_type']
        self.fomnames=['Eta.V_ave']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='Eta(V)'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=self.fomnames[0], colormap='jet_r', colormap_over_color='(0.,0.,0.)', colormap_under_color='(0.5,0.,0.)')

    def fomtuplist_rawlend_interlend(self, dataarr, filed):
        t=dataarr[1]
        eta=referenceshiftfcn(dataarr[0], filed['reference_e0'], filed['redox_couple_type'])
        return self.avefcn(eta, t), dict([('Eta(V)', eta)]), {}

class Analysis__Iphoto(Analysis_Master_inter):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams=dict([\
  ('frac_illum_segment_start', 0.4), ('frac_illum_segment_end', 0.95), \
  ('frac_dark_segment_start', 0.4), ('frac_dark_segment_end', 0.95), \
  ('illum_key', 'Ach(V)'), ('illum_time_shift_s', 0.), ('illum_threshold', -1), \
  ('illum_invert', 1), ('num_illum_cycles', 2), ('from_end', True)\
                                       ])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Iphoto'
        self.requiredkeys=['I(A)', 'Ewe(V)', 't(s)', 'Toggle']#0th is array whose photoresponse is being calculate, -1th is the Illum signal, and the rest get processed along the way
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=['I.A_photo', 'I.A_photo_ill', 'I.A_photo_dark']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='I(A)'
        self.plotparams['plot__1']['series__2']='IllumBool'
        self.plotparams['plot__2']={}
        self.plotparams['plot__2']['x_axis']='t(s)_dark,t(s)_ill,t(s)_ill'
        self.plotparams['plot__2']['series__1']='I(A)_dark,I(A)_ill,I(A)_illdiff'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=self.fomnames[0], colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')
    #this is the default fcn but with requiredkeys changed to relfect user-entered illum key
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None, calcFOMDialogclass=None):
        self.requiredkeys[-1]=self.params['illum_key']
        self.num_files_considered, self.filedlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys, requiredparams=self.requiredparams)
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filedlist

    def photofcn(self, d):

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
    def fomtuplist_rawlend_interlend(self, dataarr, filed):
        d=dict([(k, v) for k, v in zip(self.requiredkeys, dataarr)])
        return self.photofcn(d)

class Analysis__Ephoto(Analysis__Iphoto):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams=dict([\
  ('frac_illum_segment_start', 0.4), ('frac_illum_segment_end', 0.95), \
  ('frac_dark_segment_start', 0.4), ('frac_dark_segment_end', 0.95), \
  ('illum_key', 'Toggle'), ('illum_time_shift_s', 0.), ('illum_threshold', 0.5), \
  ('illum_invert', 0), ('num_illum_cycles', 2), ('from_end', True)\
                                       ])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Ephoto'
        self.requiredkeys=['Ewe(V)', 'I(A)', 't(s)', 'Toggle']#0th is array whose photoresponse is being calculate, -1th is the Illum signal, and the rest get processed along the way
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=['E.V_photo', 'E.V_photo_ill', 'E.V_photo_dark']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='Ewe(V)'
        self.plotparams['plot__1']['series__2']='IllumBool'
        self.plotparams['plot__2']={}
        self.plotparams['plot__2']['x_axis']='t(s)_dark,t(s)_ill,t(s)_ill'
        self.plotparams['plot__2']['series__1']='Ewe(V)_dark,Ewe(V)_ill,Ewe(V)_illdiff'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=self.fomnames[0], colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')


class Analysis__Etaphoto(Analysis__Iphoto):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams=dict([\
  ('frac_illum_segment_start', 0.4), ('frac_illum_segment_end', 0.95), \
  ('frac_dark_segment_start', 0.4), ('frac_dark_segment_end', 0.95), \
  ('illum_key', 'Toggle'), ('illum_time_shift_s', 0.), ('illum_threshold', 0.5), \
  ('illum_invert', 0), ('num_illum_cycles', 2), ('from_end', True)\
                                       ])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Etaphoto'
        self.requiredkeys=['Ewe(V)', 'I(A)', 't(s)', 'Toggle']#0th is array whose photoresponse is being calculate, -1th is the Illum signal, and the rest get processed along the way
        self.optionalkeys=[]
        self.requiredparams=['reference_e0', 'redox_couple_type']
        self.fomnames=['Eta.V_photo', 'Eta.V_photo_ill', 'Eta.V_photo_dark']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='Ewe(V)'
        self.plotparams['plot__1']['series__2']='IllumBool'
        self.plotparams['plot__2']={}
        self.plotparams['plot__2']['x_axis']='t(s)_dark,t(s)_ill,t(s)_ill'
        self.plotparams['plot__2']['series__1']='Eta(V)_dark,Eta(V)_ill,Eta(V)_illdiff'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=self.fomnames[0], colormap='jet_r', colormap_over_color='(0.,0.,0.)', colormap_under_color='(0.5,0.,0.)')

    def fomtuplist_rawlend_interlend(self, dataarr, filed):
        d=dict([(k, v) for k, v in zip(self.requiredkeys, dataarr)])
        fomtuplist, rawlend, interlend=self.photofcn(d)
        #names are from fomlist so correct, just shift values
        fomtuplist=[(k, referenceshiftfcn(v, filed['reference_e0'], filed['redox_couple_type'])) for k, v in fomtuplist]

        #rawlend just has IllumBool so add Eta(V)
        rawlend['Eta(V)']=referenceshiftfcn(dataarr[0], filed['reference_e0'], filed['redox_couple_type'])

        #names in interlendict are based on Ewe(V)key so fix these.
        keystochange=[k for k in interlend.keys() if k.startswith('Ewe')]
        for oldk in keystochange:
            newk='Eta'+oldk[3:]
            interlend[newk]=referenceshiftfcn(interlend[oldk], filed['reference_e0'], filed['redox_couple_type'])
            del interlend[oldk]

        return fomtuplist, rawlend, interlend





class Analysis__E_Ithresh(Analysis_Master_nointer):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams=dict([\
  ('i_thresh', 1.e-5), ('num_consec_points', 20), \
  ('above_bool', 1), ('skip_time_at_start_s', 0.)\
                                       ])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__E_Ithresh'
        self.requiredkeys=['Ewe(V)', 'I(A)', 't(s)']
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=['E.V_Ithresh']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='Ewe(V)'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=self.fomnames[0], colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')

    def threshfcn(self, dataarr):
        t=dataarr[2]
        tstart=self.params['skip_time_at_start_s']

        startind=numpy.argmin((t-tstart)**2)

        v, i, t=dataarr[:, startind:]
        icrit=self.params['i_thresh']
        if not self.params['above_bool']:
            i*=-1
            icrit*=-1
        b=numpy.int16(i>=icrit)
        n=self.params['num_consec_points']
        bconsec=[b[i:i+n].prod() for i in range(len(b)-n)]
        if True in bconsec:
            i=bconsec.index(True)
            fom=v[i:i+n].mean()
        else:
            fom=numpy.nan
        return [(self.fomnames[0], fom)]

    def fomtuplist_dataarr(self, dataarr, filed):
        return self.threshfcn(dataarr)



class Analysis__Eta_Ithresh(Analysis_Master_inter, Analysis__E_Ithresh):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams=dict([\
  ('i_thresh', 1.e-5), ('num_consec_points', 20), \
  ('above_bool', 1), ('skip_time_at_start_s', 0.)\
                                       ])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Eta_Ithresh'
        self.requiredkeys=['Ewe(V)', 'I(A)', 't(s)']
        self.optionalkeys=[]
        self.requiredparams=['reference_e0', 'redox_couple_type']
        self.fomnames=['Eta.V_Ithresh']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='Ewe(V)'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name=self.fomnames[0], colormap='jet_r', colormap_over_color='(0.,0.,0.)', colormap_under_color='(0.5,0.,0.)')

    def fomtuplist_rawlend_interlend(self, dataarr, filed):
        fomtuplist=self.threshfcn(dataarr)

        fomtuplist=[(k, referenceshiftfcn(v, filed['reference_e0'], filed['redox_couple_type'])) for k, v in fomtuplist]

        eta=referenceshiftfcn(dataarr[0], filed['reference_e0'], filed['redox_couple_type'])
        return fomtuplist, dict([('Eta(V)', eta)]), {}
