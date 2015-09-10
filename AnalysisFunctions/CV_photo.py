import numpy, copy,sys,os
if __name__ == "__main__":
    sys.path.append(os.path.split(os.getcwd())[0])

sys.path.append(os.path.split(os.path.realpath(__file__))[0])

from fcns_math import *
from fcns_io import *
from csvfilewriter import createcsvfilstr
from Analysis_Master import *
# import matplotlib.pyplot as plt


#this take a filedlist based on required keys in raw data and then finds samples where a required prior analysis was completed and encodes the path to the intermediate data in anadict
def ECHEPHOTO_checkcompletedanalysis_inter_filedlist(filedlist, anadict, requiredanalysis='Analysis__Iphoto'):
    anak_ftklist=[(anak, [ftk for ftk in anav.keys() if 'files_run__' in ftk]) for anak, anav in anadict.iteritems()\
           if anak.startswith('ana__') and anav['name']==requiredanalysis and True in ['files_' in ftk for ftk in anav.keys()]]

    
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
    filedlist=[dict(filed, ana__inter_filed=interfns[0], ana__inter_rawlen_filed=interfns[1]) \
          for filed, interfns in zip(filedlist, interfnks_filedlist) if len(interfns)==2]#2 is 1 for inter_files and then for inter_rawlenfiles. if less than 2 then the analysis wasn't done or failed, if >2 then analysis done multiple times
        
    return filedlist#inside of each filed are key lists ana__inter_filed and ana__inter_rawlen_filed that provide the path through anadict to get to the fn that mathces the fn in filed


class Analysis__Pphotomax(Analysis_Master_inter):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams=dict([\
  ('poly_fit_order', 3), ('num_cycles_omit_start', 0), \
  ('num_cycles_omit_end', 0), ('sweep_direction', -1), \
  ('i_at_pmax_tolerance', 0.01), ('num_points_slope_calc', 3), \
  ('pct_ewe_range_slope', 50), ('i_photo_base', None), \
  ('num_sweeps_to_fit', 1), ('use_sweeps_from_end', True) \
                                       ])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__Pphotomax'
        # assume intermediate and raw data available
        self.requiredkeys=['t(s)', 'Ewe(V)']#, 't(s)_dark', 'Ewe(V)_dark', 'I(A)_dark', 't(s)_ill', 'Ewe(V)_ill', 'I(A)_ill', 'IllumBool']#these intermediate keys are not tested for explicitly, ontly through the custom getapplicablefilenames below
        self.optionalkeys=[]
        self.requiredparams=['reference_e0', 'redox_couple_type']
        # Voc is almost always extrapolated, Vmicro will require i_photo_base parameter from previous analysis of Iphotomin_in_range
        self.fomnames=['Pmax.W', 'Vpmax.V', 'Ipmax.A', 'Voc.V', 'Isc.A', 'Iphotomin.A', 'Vmicro.V', 'Fill_factor']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='Ewe(V)'
        self.plotparams['plot__1']['series__1']='I(A)'
        self.plotparams['plot__1']['series__2']='IllumBool'
        self.plotparams['plot__2']={}
        self.plotparams['plot__2']['x_axis']='Ewe(V)_fitrng'
        self.plotparams['plot__2']['series__1']='I(A)_fitrng'
        self.plotparams['plot__2']['series__2']='I(A)_voclinfitrng'
        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name='Pmax.W', colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')
    
    # this is the default fcn but with requiredkeys changed to relfect user-entered illum key
    # def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
    #     self.requiredkeys[-1]=self.params['illum_key']
    #     self.num_files_considered, self.filedlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys)
    #     self.description='%s on %s' %(','.join(self.fomnames), techk)
    #     return self.filedlist

    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
        self.num_files_considered, self.filedlist=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys, requiredparams=self.requiredparams)
        self.filedlist=ECHEPHOTO_checkcompletedanalysis_inter_filedlist(self.filedlist, anadict, requiredanalysis='Analysis__Iphoto')#this is the only place that require dprevious analysis is specified. It is assumed that if this analysis complete and files are present, we know that certain keys exist without explicitely testing for them
        
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filedlist    
        
    def readdata(self, p, numkeys, keyinds, num_header_lines=0):
        try:
            pd=buildexppath(p+'.dat')
            dataarr=readbinary_selinds(pd, numkeys, keyinds)
            return dataarr
        except:
            pass
        pt=buildexppath(p)
        dataarr=readtxt_selectcolumns(pt, selcolinds=keyinds, delim=None, num_header_lines=num_header_lines)
        return dataarr
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak=''):
        self.initfiledicts(runfilekeys=['inter_rawlen_files','inter_files', 'misc_files'])
        #self.multirunfiledict['misc_files']={}
        self.fomdlist=[]
        for filed in self.filedlist:
            datadict={}
            if numpy.isnan(filed['sample_no']):
                if self.debugmode:
                    raiseTEMP
                continue
            fn=filed['fn']
            # print 'sample_no is ', filed['sample_no']
            try:
                #since using raw, inter and rawlen_inter data, just put them all into a datadict. all of the inter arrays are included
                dataarr=self.readdata(os.path.join(expdatfolder, fn), filed['nkeys'], filed['keyinds'], num_header_lines=filed['num_header_lines'])
                for k, v in zip(self.requiredkeys, dataarr):
                    datadict[k]=v
                for interfiled in [filed['ana__inter_filed'], filed['ana__inter_rawlen_filed']]:
                    tempdataarr=self.readdata(os.path.join(destfolder, interfiled['fn']), len(interfiled['keys']), range(len(interfiled['keys'])), num_header_lines=interfiled['num_header_lines'])
                    for k, v in zip(interfiled['keys'], tempdataarr):
                        datadict[k]=v
            except:
                if self.debugmode:
                    raiseTEMP
                continue
            
            fomtuplist, rawlend, interlend, miscfilestr=self.fomtuplist_rawlend_interlend(datadict, filed)#is stdgetapplicable names all self.requiredparams are put into filed so could parse them out here but most efficient to pass by reference the whole filed and the caclulcations treat it is a paramd
            if not numpy.isnan(filed['sample_no']):#do not save the fom but can save inter data
                self.fomdlist+=[dict(fomtuplist, sample_no=filed['sample_no'], plate_id=filed['plate_id'], run=filed['run'], runint=int(filed['run'].partition('run__')[2]))]
            if destfolder is None:
                continue
            if len(rawlend.keys())>0:
                fnr='%s__%s_rawlen.txt' %(anak,os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fnr)
                kl=saveinterdata(p, rawlend, savetxt=True)
                self.runfiledict[filed['run']]['inter_rawlen_files'][fnr]='%s;%s;%d;%d;%d' %('eche_inter_rawlen_file', ','.join(kl), 1, len(rawlend[kl[0]]), filed['sample_no'])
            if 'rawselectinds' in interlend.keys():
                fni='%s__%s_interlen.txt' %(anak,os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fni)
                kl=saveinterdata(p, interlend, savetxt=True)
                self.runfiledict[filed['run']]['inter_files'][fni]='%s;%s;%d;%d;%d' %('eche_inter_interlen_file', ','.join(kl), 1, len(interlend[kl[0]]), filed['sample_no'])
            if not miscfilestr is None and isinstance(miscfilestr, str) and len(miscfilestr)>0:
                fnm='%s__%s_polycoeff.txt' %(anak,os.path.splitext(fn)[0])
                p=os.path.join(destfolder,fnm)        
                with open(p, mode='w') as f:
                    f.write(miscfilestr)
                self.runfiledict[filed['run']]['misc_files'][fnm]='eche_polycoeff_file;%d' %filed['sample_no']
            
        self.writefom(destfolder, anak)
        
    def fomtuplist_rawlend_interlend(self, datadict, paramd):
        d=datadict
        interd={}
        rawlend={}

        # get trimmed t(s), Ewe(V) using rawselectinds
        ewetrim=[v for i, v in enumerate(d['Ewe(V)']) if i in d['rawselectinds']]
        ttrim=[v for i, v in enumerate(d['t(s)']) if i in d['rawselectinds']]
        illdiff=d['I(A)_illdiff']

        # extract sweep direction from dE/dt
        deltaE=numpy.subtract(ewetrim[1:], ewetrim[:-1])
        deltaE=numpy.sign(numpy.append(deltaE[0], deltaE)) # assume starting direction is the same as 2nd point
        
        anodstartinds=numpy.where(deltaE[1:]>deltaE[:-1])[0]
        cathstartinds=numpy.where(deltaE[1:]<deltaE[:-1])[0]

        if deltaE[0]>0:
            anodstartinds=numpy.append(0, anodstartinds)
        else:
            cathstartinds=numpy.append(0, cathstartinds)
        
        anodendinds, cathendinds = map(lambda inds: [i-1 for i in inds if i>0], [cathstartinds, anodstartinds])

        if deltaE[-1]>0:
            anodendinds=numpy.append(anodendinds, len(deltaE)-1).astype(int)
        else:
            cathendinds=numpy.append(cathendinds, len(deltaE)-1).astype(int)
        
        ## construct list of start, end t(s) tuples for each anodic and cathodic sweep (generalizes for >1 CV cycles)
        anodstartendinds = [(start, end) for start, end in zip(anodstartinds, anodendinds)]
        cathstartendinds = [(start, end) for start, end in zip(cathstartinds, cathendinds)]

        anodt_tpl, catht_tpl = map(lambda startendinds: [(ttrim[start], ttrim[end]) for (start, end) in startendinds], \
            [anodstartendinds, cathstartendinds])
        
        ## for now, number of sweeps to fit from start or end of measurement will be 'consecutive' (i.e. fit to first three anodic sweeps, but never first + third)
        if self.params['use_sweeps_from_end']:
            anodt_tpl, catht_tpl = map(lambda t_tpl: t_tpl[-1*self.params['num_sweeps_to_fit']:], [anodt_tpl, catht_tpl])
        else:
            anodt_tpl, catht_tpl = map(lambda t_tpl: t_tpl[:self.params['num_sweeps_to_fit']], [anodt_tpl, catht_tpl])
        
        ## time tuples for chosen sweep direction (or both)
        sweepdir=self.params['sweep_direction']
        time_tpl = numpy.append(anodt_tpl, catht_tpl) if sweepdir==0 else anodt_tpl if sweepdir<0 else catht_tpl
        rangefunc = lambda t: any([t >= tstart and t < tend for tstart, tend in time_tpl])
        ## create _dark and _ill interd keys from fitted range
        cyc_start = self.params['num_cycles_omit_start']
        cyc_end = None if self.params['num_cycles_omit_end']==0 else -1*self.params['num_cycles_omit_end']
        
        ttrim_fitrng = [ttrim[i] for i, v in enumerate(map(rangefunc, ttrim)) if v][cyc_start:cyc_end]
        ewetrim_fitrng = [ewetrim[i] for i, v in enumerate(map(rangefunc, ttrim)) if v][cyc_start:cyc_end]
        iphoto_fitrng = [illdiff[i] for i, v in enumerate(map(rangefunc, ttrim)) if v][cyc_start:cyc_end]

        fit = numpy.polyfit(x=ewetrim_fitrng, y=iphoto_fitrng, deg=self.params['poly_fit_order'], full=True)
        fitcoeff = fit[0]
        fitresiduals = fit[1]
        fittedfunc = lambda x: numpy.polyval(fitcoeff, x)
        miscfilestr=','.join(['%.3e' %v for v in fitcoeff]) #if this algorithm can "fail" and return NaN for foms then make miscfilestr=None

        interd['Ewe(V)_fitrng'] = numpy.array([d['Ewe(V)'][i] for i, v in enumerate(map(rangefunc, d['t(s)'])) if v])
        interd['I(A)_fitrng'] = fittedfunc(interd['Ewe(V)_fitrng'])
        interd['t(s)_fitrng'] = numpy.array([d['t(s)'][i] for i, v in enumerate(map(rangefunc, d['t(s)'])) if v])
        rawinds=numpy.arange(len(d['t(s)']))
        interd['rawselectinds'] = numpy.array([rawinds[i] for i, v in enumerate(map(rangefunc, d['t(s)'])) if v])
        
        rawlend['I(A)_fit'] = fittedfunc(d['Ewe(V)'])
        rawlend['FitrngBool'] = map(rangefunc, d['t(s)'])
        
        eo = paramd['reference_e0']
        isc = fittedfunc(eo)
        ## fom values are calculated from fitted Ewe(V) range instead of full range
        ewe = interd['Ewe(V)_fitrng']
        ewe_eo = ewe-eo
        iphoto = interd['I(A)_fitrng']
        ## index of minimum Iphoto in range or polynomial root 'nearest' eo, use rcp value 'redox_couple_type' to determine which side of eo
        iminsign = 1 if paramd['redox_couple_type']=='O2/H2O' else -1
        iminind = numpy.argmin(iphoto) if all(iphoto>0) else numpy.argmax(iphoto) if all(iphoto<0) else None
        iphotomin = 0 if iminind==None else iphoto[iminind]
        iphotobase = self.params['i_photo_base']
        ## Vmicro only calculated when 'i_photo_base' is specified; manually/externally check I(A)_fit=i_photo_base was observed for all samples in analysis
        vmicro = numpy.nan if iphotobase==None else interd['Ewe(V)_fitrng'][numpy.argmin((iphoto-iphotobase)**2)]
        pphoto = iphoto*ewe_eo*(-1*iminsign)
        pmaxind = numpy.argmax([v for i, v in enumerate(pphoto) if iphoto[i]>0]) if iminsign > 0 else numpy.argmin([v for i, v in enumerate(pphoto) if iphoto[i]<0])
        pphotomax = pphoto[pmaxind]
        iatpmax = interd['I(A)_fitrng'][pmaxind]

        vocfitlen = self.params['num_points_slope_calc']
        ewe_vocrng = [e for e in ewe if e < numpy.percentile(ewe, self.params['pct_ewe_range_slope'])] if iminsign > 0 else [e for e in ewe if e > numpy.percentile(ewe, self.params['pct_ewe_range_slope'])]

        ## Voc linear fit to # of consecutive points along Ewe(V)_fitrng;
        voclinfits = []
        for i in range(len(ewe_vocrng)-vocfitlen):
            linfit = numpy.polyfit(x=ewe_vocrng[i:i+vocfitlen], y=fittedfunc(ewe_vocrng[i:i+vocfitlen]), deg=1)
            voclinfits += [linfit.tolist()]
        maxslopeind = numpy.argmax(numpy.array([i[0] for i in voclinfits]))
        voccoeff = voclinfits[maxslopeind]
        # print voccoeff
        # plt.plot(ewe, iphoto)
        # plt.plot(ewe, numpy.polyval(voccoeff, ewe))
        # plt.show()
        interd['I(A)_voclinfitrng'] = numpy.polyval(numpy.poly1d(voccoeff), ewe)
        ## CX says prototyping reports photoanode and photocathode Voc both as positive values
        voc = numpy.absolute((-1*voccoeff[1]/voccoeff[0])-eo)
        vatpmax = numpy.absolute(ewe_eo[pmaxind])
        fillfactor = numpy.absolute(pphotomax/(voc*isc)) if iatpmax<=(isc*(1+self.params['i_at_pmax_tolerance'])) and numpy.absolute(pphotomax)<numpy.absolute(voc*isc) else numpy.nan

        fomtuplist=[]
        fomtuplist+=[('Pmax.W', pphotomax), ('Vpmax.V', vatpmax), ('Ipmax.A', iatpmax), \
                ('Voc.V', voc), ('Isc.A', isc), ('Iphotomin.A', iphotomin), ('Vmicro.V', vmicro), \
                ('Fill_factor', fillfactor)]

        return fomtuplist, rawlend, interd, miscfilestr
        

#c=Analysis__Pphotomax()
#c.debugmode=True
##p_exp='/home/dan/htehome/processes/experiment/temp/20150904.112552.done/20150904.112552.exp'
##p_ana='/home/dan/htehome/processes/analysis/temp/20150904.113437.done/20150904.113437.ana'
#p_exp='//htejcap.caltech.edu/share/home/processes/experiment/temp/20150904.112552.done/20150904.112552.exp'
#p_ana='//htejcap.caltech.edu/share/home/processes/analysis/temp/20150904.113437.done/20150904.113437.ana'
#expd=readexpasdict(p_exp)
#usek='data'
#techk='CV3'
#typek='pstat_files'
#anadict=openana(p_ana, stringvalues=True, erroruifcn=None)
#filenames=c.getapplicablefilenames(expd, usek, techk, typek, runklist=['run__1', 'run__2'], anadict=anadict)
#c.perform(os.path.split(p_ana)[0], expdatfolder=os.path.split(p_exp)[0], writeinterdat=False, anak='ana__2')
#print 'THESE FOM FILES WRITTEN'
#for k, v in c.multirunfiledict.items():
#    print k, v
#print 'THESE FOMs CALCULATED'
#print c.fomdlist

