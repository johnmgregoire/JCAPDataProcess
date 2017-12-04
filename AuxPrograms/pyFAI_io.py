import numpy as np
import pyFAI
import fabio
import numpy as np

def read_tiff(params, path, filen,img_size = 2048):
    #basic calculations
    rot = (np.pi * 2 - params['rot_ang']) / np.pi * 180
    tilt = params['tilt_ang'] / np.pi * 180
    d = params['distance']*params['pxs']*0.001
    #open and integrate
    img = fabio.open(folder_path+filename).data
    model = pyFAI.AzimuthalIntegrator(wavelength=params['lambda'])
    model.setFit2D(d, params['x'], params['y'], tilt, rot, params['pxs'], params['pxs'])
    Qchi, Q, chi = model.integrate2d(img, img_size, img_size)
    Qv, Intens = model.integrate1d(img, img_size)
    
    return {'Qchi':Qchi,'Q':Q,'chi':chi,'Qv':Qv,'Intens':Intens,'params':params}

def det_cutoff_pxs(Qchi,f=1.0):
    zer_h = np.array([np.sum(np.where(c==0,1,0)) for c in Qchi.T])
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
params = {'distance' : 2334.85362601, 'rot_ang' : 4.72370095632, 'tilt_ang' : 0.541102222503,
          'lambda' : 0.976, 'x' : 1431.18973336, 'y' : 2388.35677878,
          'imx' : 2048, 'imy' : 2048, 'pxs' : 79}

folder_path = ''
filename = '27830_0001.tif'


res = read_tiff(params, folder_path, filename)
tru = trunc_res(res)
'''
