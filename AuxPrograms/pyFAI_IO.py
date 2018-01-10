import pyFAI.azimuthalIntegrator as az
import fabio
import os, sys
import numpy as np
import pickle
import time
import scipy.misc

projectroot=os.path.split(os.getcwd())[0]
sys.path.append(projectroot)
sys.path.append(os.path.join(projectroot,'QtForms'))
sys.path.append(os.path.join(projectroot,'AuxPrograms'))
sys.path.append(os.path.join(projectroot,'OtherApps'))
sys.path.append(os.path.join(projectroot,'BatchProcesses'))
sys.path.append(os.path.join(projectroot,'AnalysisFunctions'))

from fcns_io import *

#TODO: fix plateidstr

class ssrl_integrator():
    def __init__(self,import_path,plate_idstr=None,access='HTE',testmode=False,calibration_performed=True,truncate=True,trunc_factor=0.8):
        self.import_path = import_path
        self.testmode = testmode
        self.truncate = truncate
        self.f = trunc_factor
        self.access = access
        self.plate_idstr = plate_idstr

        self.datatype = 'SSRL_datatype'

        #TODO maybe better code to find calib file from .rcp/.exp
        fns = os.listdir(self.import_path)

        #read the calibration and tif file names
        self.calib_file = os.path.join(self.import_path,*[fn for fn in fns if 'calib' in fn])

        self.speccsv_fns, self.tif_fns = [fn for fn in fns if '.txt' in fn], [fn for fn in fns if '.tif' in fn]

        if calibration_performed:
            self.parse_calib()
        else:
            #not integrated at the moment but there is a gui from pyFAI to do this
            self.perform_calibration()
        #do the actual integration if testmode=true no files will be written
        self.perform_integration()
        self.setup_file_dicts()

    def parse_calib(self):
        self.params = {}
        with open(self.calib_file) as fl:
            for line in fl.readlines():
                if '=' in line:
                    try:
                        self.params[line.split('=')[0]] = self.conv(line.split('=')[1].strip('\n'))
                    except ValueError:
                        print('Param for {} is not numeric but {}.'.format(*line.strip('\n').split('=')))
        self.params['pxs'] = 79 #magic factor

    def perform_integration(self):
        for fn in self.tif_fns:
            if self.truncate:
                Qchi = self.trunc_res(self.read_and_integrate_tiff(fn))
                self.Qchi = Qchi
            else:
                self.read_and_integrate_tiff(fn)
            if not self.testmode:
                fn_npy = os.path.join(self.import_path,fn.replace('.tif','.npy'))
                fn_png = os.path.join(self.import_path,fn.replace('.tif', '.png'))
                with open(fn_npy,'wb') as npy:
                    #save the qchi using numpy
                    np.save(npy,Qchi['Qchi'],allow_pickle=False)
                scipy.misc.imsave(fn_png, Qchi['Qchi'])
                fn_1d = os.path.join(self.import_path, 'ana_1_'+fn.strip('.tif')+'_processed.csv')
                with open(fn_1d,'wb')as f1d:
                    np.savetxt(f1d,np.array([Qchi['Qv']*10e10,Qchi['Intens']]).T,
                               delimiter=',',header='q.nm,intensity.counts',comments='', fmt='%.5f,%.5f')
            print '{} integrated and saved as .npy to {}'.format(fn,fn_npy)
        #assuming the image meta infos like qvals etc are the same in a run
        picklepfn = os.path.join(self.import_path, 'pck2d_chi_q_vals.pck')
        with open(picklepfn, 'wb') as qchi2binary:
            # save the qchi using numpy
            d = {'q_invA':Qchi['Qv']*10e10, 'q_invnm':Qchi['Qv']*10e9, 'chi_deg':Qchi['chi']+90, 'chi_rad':(Qchi['chi']+90)/180.*np.pi}
            pickle.dump(d, qchi2binary)

    def perform_calibration(self):
        pass

    def read_and_integrate_tiff(self, filen):
        #basic calculations
        rot = (np.pi * 2 - self.params['detect_tilt_alpha']) / np.pi * 180
        tilt = self.params['detect_tilt_delta'] / np.pi * 180
        d = self.params['detect_dist']*self.params['pxs'] *0.001
        #open and integrate
        img = fabio.open(os.path.join(self.import_path,filen)).data
        model = az.AzimuthalIntegrator(wavelength=self.params['wavelenght'])
        model.setFit2D(d, self.params['bcenter_x'], self.params['bcenter_y'], tilt, rot, self.params['pxs'], self.params['pxs'])
        Qchi, Q, chi = model.integrate2d(img, 1024, 1024,unit='q_nm^-1')
        Qv, Intens = model.integrate1d(img, self.params['horsize'],unit='q_nm^-1')

        return {'Qchi':Qchi, 'Q':Q, 'chi':chi, 'Qv':Qv, 'Intens':Intens}

    def det_cutoff_pxs(self, Qchi,f=1.0):
        zer_h = np.array([np.sum(np.where(c==0,1,0)) for c in Qchi.T])
        img_size = len(Qchi)
        ID = np.where(zer_h < img_size*f)[0]
        h_min,h_max = np.min(ID),np.max(ID)

        zer_v = np.array([np.sum(np.where(c==0,1,0)) for c in Qchi])
        ID = np.where(zer_v < img_size*f)[0]
        v_min,v_max = np.min(ID),np.max(ID)
        return h_min,h_max,v_min,v_max

    def trunc_res(self, res):
        h_min,h_max,v_min,v_max = self.det_cutoff_pxs(res['Qchi'],f=self.f)
        ret = {}
        ret['Qchi'] = res['Qchi'][v_min:v_max,h_min:h_max]
        ret['Q'] = res['Q'][h_min:h_max]
        ret['chi'] = res['chi'][v_min:v_max]
        ret['Qv'] = res['Qv'][h_min:h_max]
        ret['Intens'] = res['Intens'][h_min:h_max]
        return ret

    def conv(self, stringy):
        try:
            return int(stringy)
        except ValueError:
            return float(stringy)



exp_path = r'K:\users\helge.stein\20180108_CuPdZnAr_43557\20170727.130926.done'
integrator = ssrl_integrator(exp_path,plate_idstr='test')




'''
import matplotlib.pyplot as plt
plt.plot(integrator.Qchi['Qv'],integrator.Qchi['Intens'])
plt.show()
plt.imshow((integrator.Qchi['Qchi']))
plt.show()
'''