#this class is not working as of yes

import pyFAI
import pyFAI.azimuthalIntegrator as az
import fabio
import os
import numpy as np
import pickle
class ssrl_integrator():
    def __init__(self,import_path,testmode=False,calibration_performed=True,truncate=True,trunc_factor=0.8):
        self.import_path = import_path
        self.testmode = testmode
        self.truncate = truncate
        self.f = trunc_factor

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

    def parse_calib(self):
        self.params = {}
        with open(self.calib_file) as fl:
            for line in fl.readlines():
                if '=' in line:
                    try:
                        self.params[line.split('=')[0]] = self.conv(line.split('=')[1].strip('\n'))
                    except ValueError:
                        print('Param for {} is not numeric but {}.'.format(*line.strip('\n').split('=')))
        self.params['pxs'] = 79

    def perform_integration(self):
        for fn in self.tif_fns:
            if self.truncate:
                Qchi = self.trunc_res(self.read_and_integrate_tiff(fn))
            else:
                self.read_and_integrate_tiff(fn)
            if not self.testmode:
                picklepfn = os.path.join(self.import_path,fn.replace('.tif','.qchi2'))
                with open(picklepfn,'wb') as qchi2binary:
                    pickle.dump(Qchi,qchi2binary)
            print '{} integrated and saved as .qchi2 to {}'.format(fn,picklepfn)

    def perform_calibration(self):
        pass

    def read_and_integrate_tiff(self, filen):
        #basic calculations
        rot = (np.pi * 2 - self.params['detect_tilt_alpha']) / np.pi * 180
        tilt = self.params['detect_tilt_delta'] / np.pi * 180
        d = self.params['detect_dist']*self.params['pxs']*0.001
        #open and integrate
        img = fabio.open(os.path.join(path,filen)).data
        model = az.AzimuthalIntegrator(wavelength=self.params['wavelenght'])
        model.setFit2D(d, self.params['bcenter_x'], self.params['bcenter_y'], tilt, rot, self.params['horsize'], self.params['versize'])
        Qchi, Q, chi = model.integrate2d(img, self.params['horsize'], self.params['versize'])
        Qv, Intens = model.integrate1d(img, self.params['horsize'])

        return {'Qchi':Qchi,'Q':Q,'chi':chi,'Qv':Qv,'Intens':Intens}

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

'''
exp_path = r'K:\users\helge.stein\test'
integrator = ssrl_integrator(exp_path)
'''