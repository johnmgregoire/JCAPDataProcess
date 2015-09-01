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
  ('poly_fit_order', 3), ('num_cycles_omit_start', 0), \
  ('num_cycles_omit_end', 0), ('sweep_direction', -1), \
  ('i_at_pmax_tolerance', 0.01), ('num_points_slope_calc', 2), \
  ('pct_ewe_range_slope', 0.50), ('i_photo_base', None), \
  ('num_sweeps_to_fit', 1), ('use_sweeps_from_end', True) \
                                       ])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Pphotomax'
        # assume intermediate and raw data available
        self.requiredkeys=['t(s)', 'Ewe(V)', 'I(A)', 't(s)_dark', 'Ewe(V)_dark', 'I(A)_dark', 't(s)_ill', 'Ewe(V)_ill', 'I(A)_ill', 'IllumBool']
        self.optionalkeys=[]
        # Voc is almost always extrapolated, Vmicro will require i_photo_base parameter from previous analysis of Iphotomin_in_range
        self.fomnames=['Pphotomax', 'V_at_pmax', 'I_at_pmax', 'Voc_extrap', 'Isc', 'Fill_factor', 'Iphotomin_in_range', 'Vmicro']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='Ewe(V)'
        self.plotparams['plot__1']['series__1']='I(A)'
        self.plotparams['plot__1']['series__2']='IllumBool'
        self.plotparams['plot__2']={}
        self.plotparams['plot__2']['x_axis']='Ewe(V)_fitrng'
        self.plotparams['plot__2']['series__1']='I(A)_fit'
        self.plotparams['plot__2']['series__2']='I(A)_voclin'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name='Pphotomax', colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')
    
    # this is the default fcn but with requiredkeys changed to relfect user-entered illum key
    # def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
    #     self.requiredkeys[-1]=self.params['illum_key']
    #     self.num_files_considered, self.filedlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys)
    #     self.description='%s on %s' %(','.join(self.fomnames), techk)
    #     return self.filedlist


    def fomtuplist_rawlend_interlend(self, dataarr):
        d=dict([(k, v) for k, v in zip(self.requiredkeys, dataarr)])
        filed=dict() # dictionary that contains RCP parameters
        interd={}
        rawlend={}

        # extract sweep direction from dE/dt
        deltaE=numpy.subtract(d['Ewe(V)'][1:], d['Ewe(V)'][:-1])
        deltaE=numpy.sign(numpy.append(deltaE[0], deltaE)) # assume starting direction is the same as 2nd point
        anodstartinds=numpy.where(deltaE[1:]<deltaE[:-1])[0]+1
        cathstartinds=numpy.where(deltaE[1:]>deltaE[:-1])[0]+1
        if deltaE[0]>0:
            cathstartinds=numpy.append(0, cathstartinds)
        else:
            anodstartinds=numpy.append(0, anodstartinds)
        anodendinds, cathendinds = map(lambda inds: [i for i in inds-1 if i>0], [anodendinds, cathendinds])
        if deltaE[-1]>0:
            cathendinds=numpy.append(cathendinds, len(deltaE))
        else:
            anodendinds = numpy.append(anodendinds, len(deltaE))
        ## construct list of start, end t(s) tuples for each anodic and cathodic sweep (generalizes for >1 CV cycles)
        anodt_tpl, catht_tpl = map(lambda startendinds: [(d['t(s)'][start], d['t(s)'][end]) for start, end in startendinds], \
            [zip(anodstartinds, anodendinds), zip(cathstartinds, cathendinds)])
        ## for now, number of sweeps to fit from start or end of measurement will be 'consecutive' (i.e. fit to first three anodic sweeps, but never first + third)
        if self.params['use_sweeps_from_end']:
            anodt_tpl, catht_tpl = map(lambda t_tpl: t_tpl[-1*self.params['num_sweeps_to_fit']:], [anodt_tpl, catht_tpl])
        else:
            anodt_tpl, catht_tpl = map(lambda t_tpl: t_tpl[:self.params['num_sweeps_to_fit']], [anodt_tpl, catht_tpl])
        
        ## time tuples for chosen sweep direction (or both)
        sweepdir=self.params['sweep_direction']
        time_tpl = numpy.append(anodt_tpl, catht_tpl) if sweepdir==0 else anodt_tpl if sweepdir<0 else catht_tpl
        rangefunc = lambda t: any([t >= tstart & t < tend for tstart, tend in time_tpl])
        ## create _dark and _ill interd keys from fitted range
        cyc_start = self.params['num_cycles_omit_start']
        cyc_end = None if self.params['num_cycles_omit_end']==0 else -1*self.params['num_cycles_omit_end']
        for k in self.requiredkeys[3:6]:
            interd[k+'_fitrng']=d[k][map(rangefunc, d['t(s)_dark'])][cyc_start:cyc_end]
        for k in self.requiredkeys[6:9]:
            interd[k+'_fitrng']=d[k][map(rangefunc, d['t(s)_ill'])][cyc_start:cyc_end]
        
        fit_dark = numpy.polyfit(x=interd['Ewe(V)_dark_fitrng'], y=interd['I(A)_dark_fitrng'], deg=self.params['poly_fit_order'], full=True)
        fit_ill = numpy.polyfit(x=interd['Ewe(V)_ill_fitrng'], y=interd['I(A)_ill_fitrng'], deg=self.params['poly_fit_order'], full=True)
        fitcoeff_dark, fitresiduals_dark = fit_dark[0], fit_dark[1]
        fitcoeff_ill, fitresiduals_ill = fit_ill[0], fit_ill[1]
        diffcoeff = numpy.poly1d(fitcoeff_ill - fitcoeff_dark)
        fittedfunc = lambda x: numpy.polyval(diffcoeff, x)
        interd['poly_coeff'] = diffcoeff.c
        interd['Ewe(V)_fitrng'] = numpy.sort(numpy.append(interd['Ewe(V)_dark_fitrng'], interd['Ewe(V)_ill_fitrng']))
        interd['t(s)_fitrng'] = numpy.sort(numpy.append(interd['t(s)_dark_fitrng'], interd['t(s)_ill_fitrng']))
        interd['I(A)_fitrng'] = fittedfunc(interd['Ewe(V)_fitrng'])
        rawlend['I(A)_fit'] = fittedfunc(d['Ewe(V)'])
        rawlend['FitrngBool'] = map(rangefunc, d['t(s)'])
        
        eo = filed['reference_e0']
        isc = fittedfunc(eo)
        ## fom values are calculated from fitted Ewe(V) range instead of full range
        ewe = interd['Ewe(V)_fitrng']
        ewe_eo = ewe-eo
        iphoto = interd['I(A)_fitrng']
        ## index of minimum Iphoto in range or polynomial root 'nearest' eo, use rcp value 'redox_couple_type' to determine which side of eo
        iminsign = 1 if filed['redox_couple_type']=='O2/H2O' else -1
        ## what if all((iphoto*iminsign)<0)? -- then only reverse reaction current was observed, return smallest magnitude current index
        iminind = numpy.argmin(iphoto*iminsign) if all((iphoto*iminsign)>0) else numpy.argmin(numpy.absolute(iphoto)) if all((iphoto*iminsign)<0) else \
                numpy.where((ewe_eo==numpy.max(iminsign*ewe_eo[numpy.where(numpy.sign((iphoto)[1:])!=numpy.sign((iphoto)[:-1]))[0]+1])) & (ewe<eo if iminsign==1 else ewe>eo))[0]
        iphotomin = iphoto[iminind]
        iphotobase = self.params['i_photo_base']
        ## Vmicro only calculated when 'i_photo_base' is specified; manually/externally check I(A)_fit=i_photo_base was observed for all samples in analysis
        vmicro = numpy.nan if iphotobase==None else interd['Ewe(V)_fitrng'][numpy.argmin((iphoto-iphotobase)**2)]
        # pphoto = iphoto*ewe_eo*(-iminsign) # convention? positive/negative power?
        # pmaxind = numpy.argmax(pphoto) if iminsign>0 else numpy.argmin(pphoto)
        pphoto = numpy.absolute(iphoto*ewe_eo)
        pmaxind = numpy.argmax(pphoto)
        pphotomax = pphoto[pmaxind]
        iatpmax = interd['I(A)_fitrng'][pmaxind]
        vatpmax = ewe_eo[pmaxind]

        vocfitlen = self.params['num_points_slope_calc']
        ewe_vocrng = ewe[ewe<numpy.percentile(self.params['pct_ewe_range_slope'])] if iminsign>0 else ewe[ewe>numpy.percentile(self.params['pct_ewe_range_slope'])]
        ## Voc linear fit to # of consecutive points along Ewe(V)_fitrng;
        voclinfits = []
        for i in range(0, len(ewe_vocrng)-(vocfitlen-1)):
            voclinfits += numpy.polyfit(ewe_vocrng[i:i+vocfitlen], deg=1)
        maxslopeind = numpy.argmax([i[1] for i in voclinfits])
        voccoeff = voclinfits[maxslopeind]
        ## alternatively we can use numpy.polyder and solve for intercept
        # fittedder = numpy.polyder(diffcoeff)
        # slopes = numpy.polyval(fitteder, ewe_vocrng)
        # maxslopeind = numpy.argmax(slopes)
        # voccoeff = [fittedfunc(ewe_vocrng)[maxslopeind]-(slopes[maxslopeind]*ewe_vocrng[maxslopeind]), slopes[maxslopeind]]

        interd['voc_coeff'] = voccoeff
        interd['I(A)_voclin'] = numpy.polyval(voccoeff, ewe)
        ## CX says prototyping reports photoanode and photocathode Voc both as positive values
        voc = numpy.absolute((-1*voccoeff[0]/voccoeff[1])-eo)
        fillfactor = numpy.absolute(pphotomax/(voc*isc)) if iatpmax<=(isc*(1+self.params['i_at_pmax_tolerance'])) else numpy.nan

        fomtuplist=[]
        fomtuplist+=[('Pphotomax', pphotomax), ('V_at_pmax', vatpmax), ('I_at_pmax', iatpmax), \
                ('Voc_extrap', voc), ('Isc', isc), ('Iphotomin_in_range', iphotomin), ('Vmicro', vmicro), \
                ('Fill_factor', fillfactor)]

        return fomtuplist, rawlend, interd