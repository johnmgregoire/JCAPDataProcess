#this class is not working as of yes

import pyFAI
import pyFAI.azimuthalIntegrator as az
import fabio
import os
import numpy as np
    class ssrl_integrator():
        def __init__(self,import_path,testmode):
            self.import_path = import_path
            self.testmode = testmode

            #TODO proper code to find calib file from .rcp/.exp
            fns = os.listdir(os.path.join(self.import_path, 'images'))
            self.calib_file = [fn for fn in fns if 'calib' in fn]
            self.speccsv_fns, self.tif_fns = [fn for fn in fns if '.txt' in fn], [fn for fn in fns if '.tif' in fn]
            self.parse_calib()
            self.perform_integration()

        def parse_calib(self):
            pass

        def perform_integration(self):
            pass

        def perform_calibration(self):
            pass

        def read_tiff(params, path, filen,img_size = 2048):
            #basic calculations
            rot = (np.pi * 2 - params['rot_ang']) / np.pi * 180
            tilt = params['tilt_ang'] / np.pi * 180
            d = params['distance']*params['pxs']*0.001
            #open and integrate
            img = fabio.open(os.path.join(path,filen)).data
            model = az.AzimuthalIntegrator(wavelength=params['lambda'])
            model.setFit2D(d, params['x'], params['y'], tilt, rot, params['pxs'], params['pxs'])
            Qchi, Q, chi = model.integrate2d(img, img_size, img_size)
            Qv, Intens = model.integrate1d(img, img_size)

            return {'Qchi':Qchi,'Q':Q,'chi':chi,'Qv':Qv,'Intens':Intens,'params':params}

        def det_cutoff_pxs(Qchi,f=1.0):
            zer_h = np.array([np.sum(np.where(c==0,1,0)) for c in Qchi.T])
            img_size = len(Qchi)
            ID = np.where(zer_h < img_size*f)[0]
            h_min,h_max = np.min(ID),np.max(ID)

            zer_v = np.array([np.sum(np.where(c==0,1,0)) for c in Qchi])
            ID = np.where(zer_v < img_size*f)[0]
            v_min,v_max = np.min(ID),np.max(ID)
            return h_min,h_max,v_min,v_max

        def trunc_res(res,f=0.8):
            h_min,h_max,v_min,v_max = det_cutoff_pxs(res['Qchi'],f=f)
            ret = {}
            ret['Qchi'] = res['Qchi'][v_min:v_max,h_min:h_max]
            ret['Q'] = res['Q'][h_min:h_max]
            ret['chi'] = res['chi'][v_min:v_max]
            ret['Qv'] = res['Qv'][h_min:h_max]
            ret['Intens'] = res['Intens'][h_min:h_max]
            return ret


'''
example calib file
imagetype=uncorrected-q
dtype=uint16
horsize=2048
versize=2048
region_ulc_x=0.0
region_ulc_y=0.0
bcenter_x=835.494902365
bcenter_y=2462.62397658
detect_dist=2693.18805687
detect_tilt_alpha=4.70363646847
detect_tilt_delta=0.243126320799
wavelenght=0.9762
Qconv_const=0.00238987059185
'''

params = {'distance' : 2334.85362601, 'rot_ang' : 4.72370095632, 'tilt_ang' : 0.541102222503,
          'lambda' : 0.976, 'x' : 1431.18973336, 'y' : 2388.35677878,
          'imx' : 2048, 'imy' : 2048, 'pxs' : 79}

path = r'K:\users\helge.stein\test'
fn = '39675_0011.tif'

#res = read_tiff(params, path, fn)
#res = trunc_res(res)

#import matplotlib.pyplot as plt
#plt.plot(res['Qv'],res['Intens'])
#plt.show()

