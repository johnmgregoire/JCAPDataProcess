import numpy, copy, sys, os
if __name__ == "__main__":
    sys.path.append(os.path.split(os.getcwd())[0])

sys.path.append(os.path.split(os.path.realpath(__file__))[0])

from fcns_math import *
from fcns_io import *
import json
from scipy.optimize import curve_fit
#from scipy.optimize import minimize_scalar
from csvfilewriter import createcsvfilstr
from Analysis_Master import *

# import matplotlib.pyplot as plt


#this take a filedlist based on required keys in raw data and then finds samples where a required prior analysis was completed and encodes the path to the intermediate data in anadict
def ECHEPHOTO_checkcompletedanalysis_inter_filedlist(
        filedlist,
        anadict,
        requiredanalysis='Analysis__Iphoto',
        tech='',
        gui_mode_bool=False):
    anak_ftklist=[(anak, [ftk for ftk in anav.keys() if 'files_run__' in ftk]) for anak, anav in anadict.iteritems()\
           if anak.startswith('ana__') and anav['name']==requiredanalysis and True in ['files_' in ftk for ftk in anav.keys()]]

    if len(tech) > 0:
        #if tech=None then don't filter by technique. also if techniuqe not in anad then technique qill not be matched and the ==2 below will require only 1 Iphoto in the existing .ana.
        #otherwise this will require techniques to match so that Iphoto on different techniques in the existing .ana won't cause an excess of matches that exceed the ==2 requirement
        anak_ftklist = [(anak, ftkl) for anak, ftkl in anak_ftklist
                        if (not 'technique' in anadict[anak].keys()
                            ) or anadict[anak]['technique'] == tech]
    #goes through all inter_files and inter_rawlen_files in all analyses with this correct 'name'. This could be multiple analysis on different runs but if anlaysis done multiple times with different parameters, there is no disambiguation so such sampels are skipped.
    ##the 'ftk==('files_'+filed['run'])" condition means the run of the raw data is matched to the run in the analysis and this implied that the plate_id is match so matching sample_no would be sufficient, but matching the filename is easiest for now.  #('__'+os.path.splitext(filed['fn'])[0]) in fnk
    #this used to use [anak, ftk, typek, fnk] but anadict is not available in perform() so use filename because it is the same .ana so should be in same folder
    interfnks_filedlist=[\
          [{'fn':fnk, 'keys':tagandkeys.split(';')[1].split(','), 'num_header_lines':int(tagandkeys.split(';')[2])}\
            for anak, ftkl in anak_ftklist \
            for ftk in ftkl \
            for typek in ['inter_files', 'inter_rawlen_files']
            for fnk, tagandkeys in anadict[anak][ftk][typek].iteritems()\
                if ftk==('files_'+filed['run']) and int(tagandkeys.split(';')[4].strip())==filed['sample_no']\
          ]
        for filed in filedlist]

    #the keys anakeys__inter_file and anakeys__inter_rawlen_file assume there is only previous required analysis so this needs to be changed if combining multiple types of rpevious analysis
    filedlist2=[dict(filed, ana__inter_filed=interfns[0], ana__inter_rawlen_filed=interfns[1]) \
          for filed, interfns in zip(filedlist, interfnks_filedlist) if len(interfns)==2]#2 is 1 for inter_files and then for inter_rawlenfiles. if less than 2 then the analysis wasn't done or failed, if >2 then analysis done multiple times

    if gui_mode_bool and len(filedlist2) == 0 and len(
            anak_ftklist
    ) > 0:  #the ==2 requirement was not met, which may mean that there was more than 1 Iphoto for that technique
        print 'When looking for %s on %s for subsequent analysis, the following ana__ were found, and the requirement is for only 1 ana__ with matching technique:' % (
            requiredanalysis, tech)
        print [anak for anak, ftkl in anak_ftklist]
    return filedlist2  #inside of each filed are key lists ana__inter_filed and ana__inter_rawlen_filed that provide the path through anadict to get to the fn that mathces the fn in filed


class Analysis__Pphotomax(Analysis_Master_inter):
    def __init__(self):
        self.analysis_fcn_version = '3'  # version 3 don't detect redox couple, use calc_vs_HER instead
        self.dfltparams=dict([\
  ('weight', False), ('num_cycles_omit_start', 0), \
  ('num_cycles_omit_end', 0), ('sweep_direction', -1), \
  ('i_photo_base', 1E-8), ('num_sweeps_to_fit', 1), \
  ('use_sweeps_from_end', True), ('v_extend_upper', 0.1), \
  ('v_extend_lower', 0.1), ('v_interp_step', 0.001), \
  ('allow_nan_iphoto_pct', 0.1), ('log_ftol', -8), ('max_log_ftol', -5), ('calc_vs_HER', 0) \
                                       ])
        self.params = copy.copy(self.dfltparams)
        self.analysis_name = 'Analysis__Pphotomax'
        # assume intermediate and raw data available
        self.requiredkeys = [
            't(s)', 'Ewe(V)'
        ]  #, 't(s)_dark', 'Ewe(V)_dark', 'I(A)_dark', 't(s)_ill', 'Ewe(V)_ill', 'I(A)_ill', 'IllumBool']#these intermediate keys are not tested for explicitly, ontly through the custom getapplicablefilenames below
        self.optionalkeys = []
        self.requiredparams = ['reference_e0', 'reference_vrhe', 'redox_couple_type']
        # for logistic fit, lim(iphoto) approaches 0/1 as potential -> -infinity/+infinity, Voc here is the intercept between fitted function and iphotobase
        self.fomnames = [
            'Pmax.W', 'Vpmax.V', 'Ipmax.A', 'Voc.V', 'Isc.A', 'Fill_factor', 'RSS'
        ]
        self.plotparams = dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis'] = 'Ewe(V)'
        self.plotparams['plot__1']['series__1'] = 'I(A)'
        self.plotparams['plot__1']['series__2'] = 'IllumBool'
        self.plotparams['plot__2'] = {}
        self.plotparams['plot__2']['x_axis'] = 'Ewe(V)_fitrng'
        self.plotparams['plot__2']['series__1'] = 'I(A)_predfit'
        self.plotparams['plot__2']['series__2'] = 'P(W)_predfit'
        self.csvheaderdict = dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1'] = dict(
            {},
            fom_name='Pmax.W',
            colormap='jet',
            colormap_over_color='(0.5,0.,0.)',
            colormap_under_color='(0.,0.,0.)')

    # this is the default fcn but with requiredkeys changed to relfect user-entered illum key
    # def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
    #     self.requiredkeys[-1]=self.params['illum_key']
    #     self.num_files_considered, self.filedlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys)
    #     self.description='%s on %s' %(','.join(self.fomnames), techk)
    #     return self.filedlist
    def getgeneraltype(self):  #make this fucntion so it is inhereted
        return 'analysis_of_ana'

    def getapplicablefilenames(self,
                               expfiledict,
                               usek,
                               techk,
                               typek,
                               runklist=None,
                               anadict=None,
                               calcFOMDialogclass=None):
        self.num_files_considered, self.filedlist = stdgetapplicablefilenames(
            expfiledict,
            usek,
            techk,
            typek,
            runklist=runklist,
            requiredkeys=self.requiredkeys,
            requiredparams=self.requiredparams)
        #this is the only place that require dprevious analysis is specified. It is assumed that if this analysis complete and files are present, we know that certain keys exist without explicitely testing for them
        self.filedlist = ECHEPHOTO_checkcompletedanalysis_inter_filedlist(
            self.filedlist,
            anadict,
            requiredanalysis='Analysis__Iphoto',
            tech=techk,
            gui_mode_bool=self.gui_mode_bool)

        self.description = '%s on %s' % (','.join(self.fomnames), techk)
        return self.filedlist

    def perform(self,
                destfolder,
                expdatfolder=None,
                writeinterdat=True,
                anak='',
                zipclass=None,
                anauserfomd={},
                expfiledict=None):
        self.initfiledicts(
            runfilekeys=['inter_rawlen_files', 'inter_files', 'misc_files'])
        closeziplist = self.prepare_filedlist(
            self.filedlist,
            expfiledict,
            expdatfolder=expdatfolder,
            expfolderzipclass=zipclass,
            fnk='fn')

        self.fomdlist = []
        for filed in self.filedlist:
            datadict = {}
            if numpy.isnan(filed['sample_no']):
                if self.debugmode:
                    raiseTEMP
                continue
            fn = filed['fn']

            try:
                #since using raw, inter and rawlen_inter data, just put them all into a datadict. all of the inter arrays are included
                dataarr = filed['readfcn'](*filed['readfcn_args'],
                                           **filed['readfcn_kwargs'])
                for k, v in zip(self.requiredkeys, dataarr):
                    datadict[k] = v
                for interfiled in [
                        filed['ana__inter_filed'],
                        filed['ana__inter_rawlen_filed']
                ]:
                    tempdataarr = self.readdata(
                        os.path.join(destfolder, interfiled['fn']),
                        len(interfiled['keys']),
                        range(len(interfiled['keys'])),
                        num_header_lines=interfiled['num_header_lines']
                    )  #no zipclass for destfolder and no self.prepare_filedlist because this files must be here for this action on intermediate data
                    for k, v in zip(interfiled['keys'], tempdataarr):
                        datadict[k] = v
                fomtuplist, rawlend, interlend, miscfilestr = self.fomtuplist_rawlend_interlend(
                    datadict, filed
                )
            except:
                if self.debugmode:
                    raiseTEMP
                fomtuplist, rawlend, interlend, miscfilestr = [(
                    k, numpy.nan) for k in self.fomnames], {}, {}, None
                pass

            if not numpy.isnan(filed['sample_no']
                               ):  #do not save the fom but can save inter data
                self.fomdlist += [
                    dict(
                        fomtuplist,
                        sample_no=filed['sample_no'],
                        plate_id=filed['plate_id'],
                        run=filed['run'],
                        runint=int(filed['run'].partition('run__')[2]))
                ]
            if destfolder is None:
                continue
            if len(rawlend.keys()) > 0:
                fnr = '%s__%s_rawlen.txt' % (anak, os.path.splitext(fn)[0])
                p = os.path.join(destfolder, fnr)
                kl = saveinterdata(p, rawlend, savetxt=True)
                self.runfiledict[filed['run']]['inter_rawlen_files'][
                    fnr] = '%s;%s;%d;%d;%d' % (
                        'eche_inter_rawlen_file', ','.join(kl), 1,
                        len(rawlend[kl[0]]), filed['sample_no'])
            if 'rawselectinds' in interlend.keys():
                fni = '%s__%s_interlen.txt' % (anak, os.path.splitext(fn)[0])
                p = os.path.join(destfolder, fni)
                kl = saveinterdata(p, interlend, savetxt=True)
                self.runfiledict[filed['run']]['inter_files'][
                    fni] = '%s;%s;%d;%d;%d' % (
                        'eche_inter_interlen_file', ','.join(kl), 1,
                        len(interlend[kl[0]]), filed['sample_no'])
            if not miscfilestr is None and isinstance(
                    miscfilestr, str) and len(miscfilestr) > 0:
                fnm = '%s__%s_fitcoeff.txt' % (anak, os.path.splitext(fn)[0])
                p = os.path.join(destfolder, fnm)
                with open(p, mode='w') as f:
                    f.write(miscfilestr)
                self.runfiledict[filed['run']]['misc_files'][
                    fnm] = 'eche_polycoeff_file;%d' % filed['sample_no']

        self.writefom(destfolder, anak, anauserfomd=anauserfomd)
        for zc in closeziplist:
            zc.close()

    def fomtuplist_rawlend_interlend(self, datadict, paramd):
        d = datadict
        interd = {}
        rawlend = {}

        # get trimmed t(s), Ewe(V) using rawselectinds
        # ewetrim = [v for i, v in enumerate(d['Ewe(V)']) if i in d['rawselectinds']]
        # ttrim = [v for i, v in enumerate(d['t(s)']) if i in d['rawselectinds']]

        ewetrim = d['Ewe(V)_ill']
        ttrim = d['t(s)_ill']
        illdiff = d['I(A)_illdiff']

        # take care of NaNs
        allowed_nan_cycs = self.params['allow_nan_iphoto_pct'] * len(illdiff)
        naninds = numpy.where(numpy.isnan(illdiff))[0]
        if len(naninds) < allowed_nan_cycs:
            ttrim = numpy.array([v for i,v in enumerate(ttrim) if not i in naninds])
            ewetrim = numpy.array([v for i,v in enumerate(ewetrim) if not i in naninds])
            illdiff = numpy.array([v for i,v in enumerate(illdiff) if not i in naninds])
        else:
            fomtuplist = [('Pmax.W', numpy.nan), ('Vpmax.V', numpy.nan), ('Ipmax.A', numpy.nan), \
                    ('Voc.V', numpy.nan), ('Isc.A', numpy.nan), ('Fill_factor', numpy.nan), \
                    ('RSS', numpy.nan)]
            miscfilestr = None
            return fomtuplist, rawlend, interd, miscfilestr

        # extract sweep direction from dE/dt
        deltaE = numpy.subtract(ewetrim[1:], ewetrim[:-1])
        deltaE = numpy.sign(numpy.append(
            deltaE[0],
            deltaE))  # assume starting direction is the same as 2nd point

        anodstartinds = numpy.where(deltaE[1:] > deltaE[:-1])[0]
        cathstartinds = numpy.where(deltaE[1:] < deltaE[:-1])[0]

        if deltaE[0] > 0:
            anodstartinds = numpy.append(0, anodstartinds)
        else:
            cathstartinds = numpy.append(0, cathstartinds)

        anodendinds, cathendinds = map(
            lambda inds: [i - 1 for i in inds if i > 0],
            [cathstartinds, anodstartinds])

        if deltaE[-1] > 0:
            anodendinds = numpy.append(anodendinds,
                                       len(deltaE) - 1).astype(int)
        else:
            cathendinds = numpy.append(cathendinds,
                                       len(deltaE) - 1).astype(int)

        ## construct list of start, end t(s) tuples for each anodic and cathodic sweep (generalizes for >1 CV cycles)
        anodstartendinds = [(start, end)
                            for start, end in zip(anodstartinds, anodendinds)]
        cathstartendinds = [(start, end)
                            for start, end in zip(cathstartinds, cathendinds)]

        anodt_tpl, catht_tpl = map(lambda startendinds: [(ttrim[start], ttrim[end]) for (start, end) in startendinds], \
            [anodstartendinds, cathstartendinds])

        ## for now, number of sweeps to fit from start or end of measurement will be 'consecutive' (i.e. fit to first three anodic sweeps, but never first + third)
        if self.params['use_sweeps_from_end']:
            anodt_tpl, catht_tpl = map(
                lambda t_tpl: t_tpl[-1 * self.params['num_sweeps_to_fit']:],
                [anodt_tpl, catht_tpl])
        else:
            anodt_tpl, catht_tpl = map(
                lambda t_tpl: t_tpl[:self.params['num_sweeps_to_fit']],
                [anodt_tpl, catht_tpl])

        ## time tuples for chosen sweep direction (or both)
        sweepdir = self.params['sweep_direction']
        time_tpl = numpy.append(
            anodt_tpl, catht_tpl
        ) if sweepdir == 0 else anodt_tpl if sweepdir < 0 else catht_tpl
        rangefunc = lambda t: any([t >= tstart and t < tend for tstart, tend in time_tpl])
        ## create _dark and _ill interd keys from fitted range
        cyc_start = self.params['num_cycles_omit_start']
        cyc_end = None if self.params[
            'num_cycles_omit_end'] == 0 else -1 * self.params[
                'num_cycles_omit_end']

        ttrim_fitrng = numpy.array([ttrim[i] for i, v in enumerate(map(rangefunc, ttrim)) if v][cyc_start:cyc_end], dtype=float)
        ewetrim_fitrng = numpy.array([ewetrim[i] for i, v in enumerate(map(rangefunc, ttrim)) if v][cyc_start:cyc_end], dtype=float)
        iphoto_fitrng = numpy.array([illdiff[i] for i, v in enumerate(map(rangefunc, ttrim)) if v][cyc_start:cyc_end], dtype=float)

        # Fitting
        fpl = lambda t, Cl, Cu, A, k: (Cl + ((Cu - Cl) / (1 + numpy.exp((A - t) / k))))
        weight = self.params['weight']
        ywt = 1/(iphoto_fitrng**weight) if weight else None


        weight = self.params['weight']
        mintol = self.params['log_ftol']
        maxtol = self.params['max_log_ftol']
        tolind=0
        tollist=numpy.logspace(mintol, maxtol, maxtol-mintol+1)

        while tolind<len(tollist):
            try:
                popt, pcov = curve_fit(fpl, ewetrim_fitrng, iphoto_fitrng, sigma=ywt, maxfev=2000, ftol=tollist[tolind])
                break
            except RuntimeError:
                tolind+=1
                pass
        if tolind==len(tollist):
            fomtuplist = [('Pmax.W', numpy.nan), ('Vpmax.V', numpy.nan), ('Ipmax.A', numpy.nan), \
                    ('Voc.V', numpy.nan), ('Isc.A', numpy.nan), ('Fill_factor', numpy.nan), \
                    ('RSS', numpy.nan)]
            miscfilestr = None
            return fomtuplist, rawlend, interd, miscfilestr

        fittedfunc = lambda x: fpl(x, *popt)
        fitcoeff = popt
        fiterrs = pcov.diagonal()**0.5
        fitresiduals = iphoto_fitrng - fittedfunc(ewetrim_fitrng)
        rss = numpy.sum(fitresiduals**2)

        jsondict = {
            'coeffs': fitcoeff.tolist(),
            'errors': fiterrs.tolist(),
            'covariance': pcov.tolist(),
            'log_ftol': tollist[tolind],
            'function': 'fpl = lambda t, Cl, Cu, A, k: (Cl + ((Cu - Cl) / (1 + numpy.exp((A - t) / k))))'
        }
        miscfilestr = json.dumps(jsondict)

        # fom calculations on trimmed data (limited sweeps and cycles)
        vrhe = paramd['reference_vrhe']
        # eo = paramd['reference_e0']
        eo = vrhe + 1.229 # don't detect OER/HER from rcp, just assume OER and check calc_vs_HER param
        if self.params['calc_vs_HER']:
            ewe_eo = ewetrim_fitrng - vrhe
            isc = fittedfunc(-1*vrhe)
        else:
            ewe_eo = eo - ewetrim_fitrng
            isc = fittedfunc(eo)
        iphoto = fittedfunc(ewetrim_fitrng)

        #iminsign = 1 if paramd['redox_couple_type'] == 'O2/H2O' else -1
        pphoto = iphoto * ewe_eo #* iminsign

        # interpolate voltage stepping for higher res, less quantized vatpmax
        minewe = numpy.round(numpy.min(d['Ewe(V)']), 3)
        maxewe = numpy.round(numpy.max(d['Ewe(V)']), 3)
        vstep = self.params['v_interp_step']
        extlo = self.params['v_extend_lower']
        exthi = self.params['v_extend_upper']
        ewesmooth = numpy.arange(start=minewe-extlo, \
                                   stop=maxewe+exthi, \
                                   step=vstep)
        iphotosmooth = fittedfunc(ewesmooth)
        if self.params['calc_vs_HER']:
            pphotosmooth = iphotosmooth * (ewesmooth - vrhe) #* iminsign
            pmaxind = numpy.argmin(pphotosmooth)
            pphotomax = pphotosmooth[pmaxind]
            iatpmax = iphotosmooth[pmaxind]
            vatpmax = (ewesmooth - vrhe)[pmaxind] #*iminsign
        else:
            pphotosmooth = iphotosmooth * (eo-ewesmooth) #* iminsign
            pmaxind = numpy.argmax(pphotosmooth)
            pphotomax = pphotosmooth[pmaxind]
            iatpmax = iphotosmooth[pmaxind]
            vatpmax = (eo-ewesmooth)[pmaxind] #*iminsign

        # rawlend assignments
        rawinds = numpy.arange(len(d['t(s)']))
        rawlend['I(A)_pred'] = fittedfunc(d['Ewe(V)'])
        if self.params['calc_vs_HER']:
            rawlend['P(W)_pred'] = fittedfunc(d['Ewe(V)']) * (d['Ewe(V)'] - vrhe) #* (iminsign)
        else:
            rawlend['P(W)_pred'] = fittedfunc(d['Ewe(V)']) * (eo - d['Ewe(V)']) #* (iminsign)
        rawlend['FitrngBool'] = map(rangefunc, d['t(s)'])
        # interd assignemnts
        interd['Ewe(V)_fitrng'] = ewetrim_fitrng
        interd['I(A)_fitrng'] = iphoto_fitrng
        interd['t(s)_fitrng'] = ttrim_fitrng
        interd['I(A)_residuals_fitrng'] = fitresiduals
        interd['I(A)_pred_fitrng'] = iphoto
        interd['P(W)_pred_fitrng'] = pphoto
        interd['rawselectinds'] = numpy.array(
            [rawinds[i] for i, v in enumerate(map(rangefunc, d['t(s)'])) if v and i in d['rawselectinds']])

        ## Voc/FF calculation: report both photoanode and photocathode Voc as positive values
        if self.params['calc_vs_HER']:
            iphotobase = -1.0*self.params['i_photo_base']
            voc = ewesmooth[numpy.argmin((iphotosmooth-iphotobase)**2)] - vrhe
        else:
            iphotobase = self.params['i_photo_base']
            voc = eo - ewesmooth[numpy.argmin((iphotosmooth-iphotobase)**2)]
        fillfactor = numpy.absolute(pphotomax / (voc * isc))

        # NaN those crazy fillfactors ### leave this alone and report RSS
        # if fillfactor>1:
        #     fillfactor = numpy.nan
        #     voc = numpy.nan

        fomtuplist = [('Pmax.W', pphotomax), ('Vpmax.V', vatpmax), ('Ipmax.A', iatpmax), \
                ('Voc.V', voc), ('Isc.A', isc), ('Fill_factor', fillfactor), \
                ('RSS', rss)]

        return fomtuplist, rawlend, interd, miscfilestr
