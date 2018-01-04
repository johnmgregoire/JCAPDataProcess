# -*- coding: utf-8 -*-
"""
Created on Wed Nov 7 17:02:32 2017

@author: helge.stein

-------this class is a work in progress-------
TODO: adjust perform function similar to CV photo that this class works smoothly with JCAPDataProcess
TODO: merge in sigmoidfitting for comparison
TODO: write files to spec into anafolder
"""


import sys, os

cwd = os.path.split(os.getcwd())[0]
if 'JCAPDataProcess-master' in cwd:
    projectroot = cwd
else:
    projectroot = r'K:\users\helge.stein\git\JCAPDataProcess-master'

sys.path.append(projectroot)
sys.path.append(os.path.join(projectroot, 'QtForms'))
sys.path.append(os.path.join(projectroot, 'AuxPrograms'))
sys.path.append(os.path.join(projectroot, 'OtherApps'))
sys.path.append(os.path.join(projectroot, 'BatchProcesses'))
sys.path.append(os.path.join(projectroot, 'AnalysisFunctions'))

from fcns_io import *

import numpy as np

from scipy.optimize import curve_fit  # curve fitting
from scipy.signal import savgol_filter as savgol  # smoothing
from scipy.signal import argrelextrema  # finding extrema in fast CVs
from get_raw_data_from_exp import *  # import data from DB

# sometimes pyearth fails to import ... the fix is to import it again
try:
    from pyearth import Earth as MARS
except:
    from pyearth import Earth as MARS


class mars_class():
    def __init__(self, exp_path, filekeystoget, testmode=True, plate_idstr=None, access='hte', filetype='pstat_files',
                 pot_shift=0, curr_factor=1):
        #this is modeled after CV_photo
        self.analysis_fcn_version = '1'
        self.analysis_name = 'Analysis__ORR'
        self.requiredkeys = [
            't(s)', 'Ewe(V)','I(A)'
        ]
        self.optionalkeys = []
        self.requiredparams = ['reference_e0', 'reference_vrhe', 'redox_couple_type']
        self.fomnames = [
            'noise_lvl','curr_lminter_model','lminter','zinter','max_slope',
            'redpot_f_var','oxpot_f_var','oxpot_f','redpot_f','curr_lminter_data'
        ]

        #as this anaclass requires a fast and slow cv scan the data should also be viewable
        self.plotparams = dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis'] = 'Ewe(V)'
        self.plotparams['plot__1']['series__1'] = 'I(A)'
        self.plotparams['plot__1']['series__2'] = 'Y_h'
        self.plotparams['plot__2'] = {}
        self.plotparams['plot__2']['x_axis'] = 'Ewe(V)'
        self.plotparams['plot__2']['series__1'] = 'smY'
        self.plotparams['plot__2']['series__2'] = 'srYs'
        self.plotparams['plot__3'] = {}
        self.plotparams['plot__2']['x_axis'] = 'Ewe(V)_fast'
        self.plotparams['plot__2']['series__1'] = 'I(A)_fast'
        self.plotparams['plot__2']['series__2'] = 'srYf'
        self.csvheaderdict = dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1'] = dict(
            {},
            fom_name='Pmax.W',
            colormap='jet',
            colormap_over_color='(0.5,0.,0.)',
            colormap_under_color='(0.,0.,0.)')

        # init all necessary values
        self.exp_path = exp_path
        self.filekeystoget = filekeystoget
        self.plate_idstr = plate_idstr
        self.access = access
        self.filetype = filetype
        self.pot_shift = pot_shift
        self.curr_factor = curr_factor
        self.testmode = testmode
        self.fomdict = {}
        self.potID = 1  # hardcoded .. if this ever changes this will produce an error
        self.currID = 3

        self.get_data()
        #self.perform_sig()
        self.perform_mars()
        #self.perform_amars()
        #self.write_data()


    def get_data(self):
        self.data = {key: get_file_dicts_containing_data( self.exp_path, [key], self.filetype, sample_list=None) for key in
                     self.filekeystoget}

        self.cv_keys = [key for key in self.filekeystoget if 'CV' in key]
        print 'CV keys {}'.format(self.cv_keys)

        '''
        this seems a bit off but I want this class to be able to tell without user input which
        CV is the fast and which is the slow one (i.e. the .rcp)
        '''
        fn = {cv_key:self.data[cv_key].keys() for cv_key in self.cv_keys}
        print(fn)
        scanspeeds = {}
        for cv_key in self.cv_keys:
            for f in fn[cv_key]:
                t, pot = self.data[cv_key][f]['data_arr'][0, :], self.data[cv_key][f]['data_arr'][1, :]
            #this just needs to run once
            scanspeeds[cv_key] = np.abs(np.diff(pot) / np.diff(t)).mean()
        self.fast_cv_key = scanspeeds.keys()[np.argmax(scanspeeds.values())]
        self.slow_cv_key = scanspeeds.keys()[np.argmin(scanspeeds.values())]
        print 'Done importing data!'


    def marsmodelorr(self, use_smY=True, slope_trunc=0.00001, savgol_window=151, savgol_order=3, ex_order=51):
        Xf, Yf = self.Xf_, self.Yf_
        X, Y = self.X_, self.Y_
        fom = {}
        # smooth the data
        smY = savgol(Y, savgol_window, savgol_order)
        # perform mars
        model = MARS()
        if use_smY:
            model.fit(X, smY)
        else:
            model.fit(X, Y)
        Y_h = model.predict(X)
        '''
        calculate dydx based on mars model to get knots and intercepts as this is 
        complicated to extract from hinge functions
        '''
        diff1 = np.diff(Y_h) / np.diff(X)
        tdiff1 = diff1 - np.nanmin(diff1)
        tdiff1 = tdiff1 / np.nanmax(tdiff1)
        #calculate slopes of linear segments
        ID = [i for i in range(1, len(tdiff1)) if np.abs(tdiff1[i] - tdiff1[i - 1]) > slope_trunc]
        ID.insert(0, 0)
        ID.append(np.argmax(X))  # this might cause an error
        slopes = [np.nanmean(diff1[ID[i - 1]:ID[i]]) for i in range(1, len(ID) - 1)]
        a = [Y_h[ID[i]] - slopes[i] * X[ID[i]] for i in range(len(ID) - 2)]
        IDM, IDm = np.argmax(slopes), np.argmin(np.abs(slopes))
        # intercept of highest slope and zero as well as highest slope and lowest slope
        fom['zinter'] = -a[IDM] / slopes[IDM]
        fom['lminter'] = (a[IDM] - a[IDm]) / (slopes[IDm] - slopes[IDM])
        fom['max_slope'] = slopes[IDM]
        fom['curr_lminter_model'] = fom['lminter'] * slopes[IDM] + a[IDM]
        fom['curr_lminter_data'] = np.mean(Y[np.where(np.abs(X - fom['lminter']) < 0.5)[0]])
        # calculate how the CV curves kight look like without the 'ORR part'
        srYs = smY - model.predict(X)
        srYf = savgol(Yf - model.predict(Xf), savgol_window, savgol_order)
        # calculate their derivative
        dsrYf = savgol(np.diff(srYf) / np.diff(Xf), savgol_window, savgol_order)
        # find the extrema in the derivatives for extraction of redox pots
        redID_f = argrelextrema(srYf, np.less, order=ex_order)
        oxID_f = argrelextrema(srYf, np.greater, order=ex_order)
        # calc some more foms like position of redox waves
        fom['redpot_f'], fom['redpot_f_var'] = np.nanmean(Xf[redID_f]), np.nanstd(Xf[redID_f])
        fom['oxpot_f'], fom['oxpot_f_var'] = np.nanmean(Xf[oxID_f]), np.nanstd(Xf[oxID_f])
        fom['X'], fom['Xf'] = X, Xf
        fom['srYs'], fom['srYf'], fom['smY'] = srYs, srYf, smY
        fom['Y'], fom['Yf'], fom['Y_h'] = Y, Yf, Y_h
        fom['noise_lvl'] = np.sum((Y_h - Y) ** 2, axis=0)
        self.fom = fom

    def perform_mars(self):
        fn = {cv_key: self.data[cv_key].keys() for cv_key in self.cv_keys}
        for fs, ff in zip(fn[self.slow_cv_key],fn[self.fast_cv_key]):
            sample_no = self.data[self.slow_cv_key][fs]['sample_no']
            self.X_, self.Y_ = self.data[self.slow_cv_key][fs]['data_arr'][self.potID, :], \
                               self.data[self.slow_cv_key][fs]['data_arr'][self.currID, :]
            self.Xf_, self.Yf_ = self.data[self.fast_cv_key][ff]['data_arr'][self.potID, :], \
                                 self.data[self.fast_cv_key][ff]['data_arr'][self.currID, :]
            self.marsmodelorr()
            self.fom['sample_no'] = sample_no
            print('Finished Sample #{}'.format(sample_no))
            self.fomdict[self.fom['sample_no']] = self.fom

    def save_data(self):
        pass

'''
#model after this class
class Analysis__Iphoto(Analysis_Master_inter):
    def __init__(self):
        self.analysis_fcn_version='2'
        self.dfltparams=dict([\
  ('frac_illum_segment_start', 0.4), ('frac_illum_segment_end', 0.95), \
  ('frac_dark_segment_start', 0.4), ('frac_dark_segment_end', 0.95), \
  ('illum_key', 'Toggle'), ('illum_time_shift_s', 0.), ('illum_threshold', 0.5), \
  ('illum_invert', 0), ('num_illum_cycles', 2), ('from_end', True)\
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
        requiredparams=self.requiredparams
        if self.params['illum_key']=='t(s)':
            self.echem_params_key='echem_params__'+techk
            requiredparams+=[self.echem_params_key]#['toggle_dark_time_init', 'toggle_illum_time', 'toggle_illum_duty', 'toggle_illum_period']
            
        self.num_files_considered, self.filedlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys, requiredparams=requiredparams)
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filedlist

    def photofcn(self, d, filed):

        ikey=self.params['illum_key']
        tshift=self.params['illum_time_shift_s']
        interdict={}
        if tshift!=0:
            newikey='IllumMod'
            illumtimeshift(d, ikey, 't(s)', tshift)
        if self.params['illum_invert']:
            d[ikey]=-1*d[ikey]

        interd={}
        
        if self.params['illum_key']=='t(s)':
            ikey=[filed[self.echem_params_key][k] for k in ['toggle_dark_time_init', 'toggle_illum_time', 'toggle_illum_duty', 'toggle_illum_period']]
        
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
        return self.photofcn(d, filed)

'''



'''
#sigmoid fitting from old script
def splitLVS(X, Y):  # split the linear sweeps
    up = np.reshape(np.where(np.diff(X) > 0), -1, 1)
    down = np.reshape(np.where(np.diff(X) > 0), -1, 1)
    iup = np.argsort(X[up])
    idown = np.argsort(X[down])
    return X[up[iup]], Y[up[iup]], X[down], Y[up]

def fitSigmoid(Xu, Yu):  # fit a sigmoid to data that allows assymetry
    fpl = lambda t, Cl, Cu, A, k: (Cl + ((Cu - Cl) / (1 + np.exp((A - t) / k))))
    tpl = lambda t, Cu, A, k: (Cu / (1 + np.exp((A - t) / k)))
    fpl_2shapes = lambda t, Cl, Cu, A, k, k2: fpl(t, Cl, Cu, A, fpl(t, k, k2, A, min(k, k2)))
    popt, pcov = curve_fit(fpl, Xu, Yu, maxfev=1000000)
    # calculations
    x = popt[2]
    y = fpl(popt[2], *popt)
    dydx_fpl = lambda x, A, B, C, D: ((B - A) * np.exp((C + x) / D)) / (D * (np.exp(C / D) + np.exp(x / D)) ** 2)
    m = dydx_fpl(popt[2], *popt)
    a = y - m * x
    intercept = -a / m
    overpotential = 1.23 - intercept
    # print popt
    fom = {}
    fom['popt'], fom['pcov'], fom['intercept'], fom['overpotential'], fom[
        'slope'] = popt, pcov, intercept, overpotential, m
    return fom

fomlist_sig = []
for i in range(len(data['files_technique__CV2'][1][:])):
    sample_no = data['files_technique__CV2'][2][i]
    X, Y = data['files_technique__CV4'][0][:, i], data['files_technique__CV4'][1][:, i]
    ID = np.argsort(X)
    Ysm = savgol(Y[ID], 151, 3)
    fomlist_sig.append([fitSigmoid(X[ID], Ysm), sample_no])
    print(i)
    
fomlist = []
for i in range(len(data['files_technique__CV2'][1][:])):
    sample_no = data['files_technique__CV2'][2][i]
    X, Y = data['files_technique__CV4'][0][:, i], data['files_technique__CV4'][1][:, i]
    # Xm,Ym = data[1][0][:,i],data[1][1][:,i]
    Xf, Yf = data['files_technique__CV2'][0][i], data['files_technique__CV2'][1][i]
    # xdict = {'fast':Xf,'mid':Xm,'slow':X}
    # ydict = {'fast':Yf,'mid':Ym,'slow':Y}
    xdict = {'fast': Xf, 'slow': X}
    ydict = {'fast': Yf, 'slow': Y}
    fomlist.append([marsmodelorr(xdict, ydict), sample_no])
    print(i)
# run a test
'''

expname = r'\eche\20171218.222905.done'
filekeystoget = ['files_technique__CV2', 'files_technique__CV4', 'files_technique__CA5']
ftype = 'pstat_files'

mc = mars_class(exp_path=expname, filekeystoget=filekeystoget,filetype=ftype)
