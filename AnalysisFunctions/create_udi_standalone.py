import numpy, copy, operator
from scipy import interpolate
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    
from fcns_io import *
from Analysis_Master import Analysis_Master_nointer

analysismasterclass=Analysis_Master_nointer()


def append_udi_to_ana(l_anapath=None, l_anak_comps=None, l_anak_patterns=None, pattern_key='pattern_files', compkeys='AtFrac', q_key='q.nm_processed',intensity_key='intensity.counts_processed', pattern_fn_search_str='', dq=None, q_log_space_coef=None, resamp_interp_order=1):
    if l_anapath is None:
        num_ana=userinputcaller(None, inputs=[('num_ana', int, '1')], title='Enter Number of ana to open')
        if num_ana is None:
            return
        l_anapath=[selectexpanafile(None, exp=False, markstr='Select .ana/.pck to import, or .zip file') for i in range(num_ana)]
        if None in l_anapath or 0 in [len(p) for p in l_anapath]:
            return
    else:
        num_ana=len(l_anapath)
    if num_ana==0 or not '.run' in l_anapath[0]:
        print 'can only append udi file to analysis with .run status'
        return
    l_fns=[os.path.split(p)[1] for p in l_anapath]

    if l_anak_comps is None or len(l_anak_comps)!=len(l_anapath):
        ans=userinputcaller(None, inputs=[('ana_ints_for_comps', str, ','.join(['1']*num_ana))], title='Enter ana__# vals containing comps for each .ana')
        if ans is None or ans.count(',')!=(num_ana-1):
            print 'error entering ana ints for comps: ', ans
            return
        l_anak_comps=['ana__%s' %s.strip() for s in ans.split(',')]
        
    if l_anak_patterns is None or len(l_anak_patterns)!=len(l_anapath):
        ans=userinputcaller(None, inputs=[('ana_ints_for_patterns', str, ','.join(['1']*num_ana))], title='Enter ana__# vals containing patterns for each .ana')
        if ans is None or ans.count(',')!=(num_ana-1):
            print 'error entering ana ints for patterns: ', ans
            return
        l_anak_patterns=['ana__%s' %s.strip() for s in ans.split(',')]
    
    l_anadict_zipclass=[readana(p, stringvalues=False, erroruifcn=None, returnzipclass=True) for p in l_anapath]
    get_file_path=lambda p, fn, zipclass: fn if zipclass else (os.path.join(os.path.split(p)[0], fn) if '.ana' in p else os.path.join(p, fn))
    l_found_comp_keys=[]
    l_comp_fomd=[]
    l_pattern_l_fn_fd=[]
    l_plate_idstr=[]
    #loop over each ana file, each being used for a ana__ for comps and another for patterns
    for count, (anap, (anadict, zipclass), anak_comps, anak_patterns) in enumerate(zip(l_anapath, l_anadict_zipclass, l_anak_comps, l_anak_patterns)):
        #get ana__ block plate_ids and make sure only 1
        fomd=None
        if isinstance(anadict[anak_comps]['plate_ids'], str) and ',' in anadict[anak_comps]['plate_ids']:
            print 'can only use ana__ with single plate_id: ', anap, anak_comps, anadict[anak_comps]['plate_ids']
            return
        l_plate_idstr+=[anadict[anak_comps]['plate_ids'].strip() if isinstance(anadict[anak_comps]['plate_ids'], str) else ('%d' %anadict[anak_comps]['plate_ids'])]
        
        #loop over all fom_files and find 1 that has comp foms
        for fn, filed in anadict[anak_comps]['files_multi_run']['fom_files'].iteritems():
            if isinstance(compkeys, str):
                found_comp_keys=[k for k in filed['keys'] if compkeys in k]
            else:
                found_comp_keys=[k for k in filed['keys'] if k in compkeys]
            found_comp_keys=sorted(found_comp_keys)
            if (len(found_comp_keys)>0 and isinstance(compkeys, str)) or len(selkeyinds)==len(compkeys):
                fomd=readcsvdict(get_file_path(anap, fn, zipclass), filed, returnheaderdict=False, zipclass=zipclass, includestrvals=False)
                l_found_comp_keys+=[found_comp_keys]
                l_comp_fomd+=[fomd]
                break
        if fomd is None:
            print 'error finding comps for ', anap
            return
        
        #get ana__ block plate_ids and make sure only 1 and that it is the same as comps
        if isinstance(anadict[anak_patterns]['plate_ids'], str) and ',' in anadict[anak_patterns]['plate_ids']:
            print 'can only use ana__ with single plate_id: ', anap, anak_comps, anadict[anak_patterns]['plate_ids']
            return
        pidstr=anadict[anak_patterns]['plate_ids'].strip() if isinstance(anadict[anak_patterns]['plate_ids'], str) else ('%d' %anadict[anak_patterns]['plate_ids'])
        if pidstr!=l_plate_idstr[-1]:
            print 'patterns and comps from different plate_id: ', anap, anak_comps, anadict[anak_comps]['plate_ids'], anak_patterns, anadict[anak_patterns]['plate_ids']
            return
        
        #get all pattern files from any files_run__ block that has them
        l_fn_fd=[]
        for filesrunk, filesrund in anadict[anak_patterns].iteritems():
            if not filesrunk.startswith('files_run__') or not pattern_key in filesrund.keys():
                continue
            runint=int(filesrunk.partition('files_run__')[2])
            for fn, filed in filesrund[pattern_key].iteritems():
                if not pattern_fn_search_str in fn:
                    continue
                if q_key in filed['keys'] and intensity_key in filed['keys'] and filed['sample_no'] in fomd['sample_no']:
                    l_fn_fd+=[(fn, filed, runint)]
        l_pattern_l_fn_fd+=[l_fn_fd]
        
        
        pmpath=getplatemappath_plateid(pidstr)
        pmlines, pmpath=get_lines_path_file(p=pmpath)
        pmdlist=readsingleplatemaptxt('', lines=pmlines)
        smps=[d['sample_no'] for d in pmdlist]
        fomd['x']=numpy.array([pmdlist[smps.index(smp)]['x'] for smp in fomd['sample_no']])
        fomd['y']=numpy.array([pmdlist[smps.index(smp)]['y'] for smp in fomd['sample_no']])
    #get the elements whose comps were found in all ana
    l_elkey_byel=[]
    for (pidstr, found_comp_keys) in zip(l_plate_idstr, l_found_comp_keys):
        els=getelements_plateidstr(pidstr)
        elkey_byel=[]
        for i, el in enumerate(els):

            kl=[k for k in found_comp_keys if (el+'.') in k]
            elkey_byel+=[None if len(kl)==0 else kl[0]]#use the elkey for the first match found - only 1 allowed
        l_elkey_byel+=[elkey_byel]
    elindset=set([i for i, k in enumerate(l_elkey_byel[0]) if not k is None])
    for elkey_byel in l_elkey_byel[1:]:
        elindset=elindset.intersection(set([i for i, k in enumerate(elkey_byel) if not k is None]))
    elinds=sorted(list(elindset))
    if len(elindset)<2:
        print '^^^aborting because only these elements found in all ana compositions: ',  [els[i] for i in elinds], pidstr
        [k for k in kl for kl in l_found_comp_keys]
    
    udi_dict={}
    udi_dict['ellabels']=[el for i, el in enumerate(els) if i in elinds]
    udi_dict['xy']=[]
    udi_dict['plate_id']=[]
    udi_dict['comps']=[]
    udi_dict['Iarr']=[]
    udi_dict['runint']=[]
    udi_dict['sample_no']=[]
    
    smps_added_so_far=[]
    for count, (pidstr, elkey_byel, comp_fomd, pattern_l_fn_fd, anap, (anadict, zipclass)) in enumerate(zip(l_plate_idstr, l_elkey_byel, l_comp_fomd, l_pattern_l_fn_fd, l_anapath, l_anadict_zipclass)):
        
        fomdsmps=list(fomd['sample_no'])
        patternsmps=[filed['sample_no'] for fn, filed, runint in pattern_l_fn_fd]
        inds=sorted([fomdsmps.index(smp) for smp in patternsmps if not smp in smps_added_so_far])
        inds=[i for i in inds if not (True in [numpy.isnan(fomd[elkey_byel[elind]][i]) for elind in elinds])]
        newsmps=[fomdsmps[i] for i in inds]
        smps_added_so_far+=newsmps
        udi_dict['xy']+=[[fomd['x'][i], fomd['y'][i]] for i in inds]
        for i in inds:
            cmp=numpy.array([fomd[elkey_byel[elind]][i] for elind in elinds])
            cmp/=cmp.sum()
            udi_dict['comps']+=[cmp]
        udi_dict['plate_id']+=[pidstr]*len(newsmps)
        udi_dict['sample_no']+=newsmps
        for smp in newsmps:
            pind=patternsmps.index(smp)
            fn, filed, runint=pattern_l_fn_fd[pind]
            udi_dict['runint']+=[runint]
            patternd=readcsvdict(get_file_path(anap, fn, zipclass), filed, returnheaderdict=False, zipclass=zipclass, includestrvals=False)
            if count==0:
                udi_dict['compkeys']=[elkey_byel[elind] for elind in elinds]
                udi_dict['Q']=patternd[q_key]
            udi_dict['Iarr']+=[patternd[intensity_key]]
            if len(udi_dict['Iarr'][-1])!=len(udi_dict['Q']):
                print 'not all patterns same length: ',  len(udi_dict['Iarr'][-1]), len(udi_dict['Q']), anap, fn
                return
    
    udi_dict['comps']=numpy.array(udi_dict['comps'])
    udi_dict['xy']=numpy.array(udi_dict['xy'])
    udi_dict['Iarr']=numpy.array(udi_dict['Iarr'])
    udi_dict['Q']=numpy.array(udi_dict['Q'])
    
    anap=l_anapath[0]
    anadict=l_anadict_zipclass[0][0]
    pidset=sorted(list(set(l_plate_idstr)))
    pidstr=l_plate_idstr[0]
    lastanak=sort_dict_keys_by_counter(anadict)[-1]
    anak='ana__%d' %(1+int(lastanak.partition('__')[2]))
    udifn=anak+'_'+'_'.join(pidset)+'.udi'
    csvfn=udifn[:-3]+'csv'
    udip=get_file_path(anap, udifn, False)
    anafolder=os.path.split(udip)[0]
    writeudifile(udip, udi_dict)
    
    analysismasterclass.fomdlist=[]
    analysismasterclass.fomnames=['pmx', 'pmy', 'Intensity.max']
    for i in range(len(udi_dict['Iarr'])):
        d={}
        d['sample_no']=udi_dict['sample_no'][i]
        d['Intensity.max']=max(udi_dict['Iarr'][i])
        d['pmx']=udi_dict['xy'][i][0]
        d['pmy']=udi_dict['xy'][i][1]
        d['runint']=udi_dict['runint'][i]
        d['plate_id']=int(udi_dict['plate_id'][i])
        for k, v in zip(udi_dict['compkeys'], udi_dict['comps'][i]):
            d[k]=v
            if i==0:
                analysismasterclass.fomnames+=[k]
        analysismasterclass.fomdlist+=[d]
    analysismasterclass.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
    analysismasterclass.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name='Intensity.max', colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')
    filedesc=analysismasterclass.writefom_bare(anafolder, csvfn, strkeys=[], floatkeys=None, intfomkeys=['runint','plate_id'])
    anadict[anak]={}
    anadict[anak]['name']='Analysis__Create_UDI'
    anadict[anak]['plate_ids']=','.join(pidset)
    anadict[anak]['technique']=anadict['analysis_type']
    anadict[anak]['parameters']={\
    'ana_file_type': pattern_key, \
    'ana_name': ','.join([ad['name'] for ad, zc in l_anadict_zipclass]), \
    'anak': ','.join(l_anak_patterns), \
    'anak_comps': ','.join(l_anak_comps), \
    'pattern_source_analysis_name': anadict[l_anak_patterns[0]]['name'], \
    'plate_id': ','.join(pidset), \
    'q_key': q_key, \
    'intensity_key': intensity_key, \
    }
    anadict[anak]['files_multi_run']={}
    anadict[anak]['files_multi_run']['fom_files']={}
    anadict[anak]['files_multi_run']['fom_files'][csvfn]=filedesc
    anadict[anak]['files_multi_run']['misc_files']={}
    anadict[anak]['files_multi_run']['misc_files'][udifn]='%s_udi_file' %anadict[anak]['technique']
    
    fs=strrep_filedict(anadict)
    with open(anap, mode='w') as f:
        f.write(fs)


def append_resampled_merged_patterns_to_ana(l_anapath=None, l_anak_patterns=None,  l_pattern_fn_search_str=None, pattern_key='pattern_files', q_key='q.nm_processed',intensity_key='intensity.counts_processed'):
    if l_anapath is None:
        num_ana=userinputcaller(None, inputs=[('num_ana', int, '1')], title='Enter Number of ana to open')
        if num_ana is None:
            return
        l_anapath=[selectexpanafile(None, exp=False, markstr='Select .ana/.pck to import, or .zip file') for i in range(num_ana)]
        if None in l_anapath or 0 in [len(p) for p in l_anapath]:
            return
    else:
        num_ana=len(l_anapath)
    if num_ana==0 or not '.run' in l_anapath[0]:
        print 'can only append udi file to analysis with .run status'
        return
    l_fns=[os.path.split(p)[1] for p in l_anapath]
        
    if l_anak_patterns is None or len(l_anak_patterns)!=len(l_anapath):
        ans=userinputcaller(None, inputs=[('ana_ints_for_patterns', str, ','.join(['1']*num_ana))], title='Enter ana__# vals containing patterns for each .ana')
        if ans is None or ans.count(',')!=(num_ana-1):
            print 'error entering ana ints for patterns: ', ans
            return
        l_anak_patterns=['ana__%s' %s.strip() for s in ans.split(',')]
    if l_pattern_fn_search_str is None or len(l_pattern_fn_search_str)!=len(l_anapath):
        ans=userinputcaller(None, inputs=[('pattern_fn_search_per_anakey', str, ','.join(['.csv']*num_ana))], title='Enter for each ana__ in each .ana, select the search string, emtpy string to use all pattern files')
        if ans is None or ans.count(',')!=(num_ana-1):
            print 'error entering ana ints for search string: ', ans
            return
        l_pattern_fn_search_str=['%s' %s.strip() for s in ans.split(',')]
        
    l_anadict_zipclass=[readana(p, stringvalues=False, erroruifcn=None, returnzipclass=True) for p in l_anapath]
    get_file_path=lambda p, fn, zipclass: fn if zipclass else (os.path.join(os.path.split(p)[0], fn) if '.ana' in p else os.path.join(p, fn))

    l_pattern_l_fn_fd=[]
    l_pattern_l_smps=[]
    #loop over each ana file, each being used for a ana__ for comps and another for patterns
    for count, (anap, (anadict, zipclass), anak_patterns, pattern_fn_search_str) in enumerate(zip(l_anapath, l_anadict_zipclass, l_anak_patterns, l_pattern_fn_search_str)):
        #get ana__ block plate_ids and make sure only 1 and that it is the same as previous ana__
        if isinstance(anadict[anak_patterns]['plate_ids'], str) and ',' in anadict[anak_patterns]['plate_ids']:
            print 'can only use ana__ with single plate_id: ', anap, anadict[anak_patterns]['plate_ids']
            return
        pidstrtemp=anadict[anak_patterns]['plate_ids'].strip() if isinstance(anadict[anak_patterns]['plate_ids'], str) else ('%d' %anadict[anak_patterns]['plate_ids'])
        if count==0:
            pidstr=pidstrtemp
        elif pidstr!=pidstrtemp:
            print 'cannot merge patterns from different plate_ids: ', anap, anak_patterns, anadict[anak_patterns]['plate_ids']
            return
        
        #get all pattern files from any files_run__ block that has them
        l_fn_fd=[]
        l_smps=[]
        for filesrunk, filesrund in anadict[anak_patterns].iteritems():
            if not filesrunk.startswith('files_run__') or not pattern_key in filesrund.keys():
                continue
            runint=int(filesrunk.partition('files_run__')[2])
            for fn, filed in filesrund[pattern_key].iteritems():
                if not pattern_fn_search_str in fn:
                    continue
                if q_key in filed['keys'] and intensity_key in filed['keys'] and filed['sample_no'] in fomd['sample_no']:
                    l_fn_fd+=[(fn, filed, runint)]
                    l_smps+=[filed['sample_no']]
        l_pattern_l_fn_fd+=[l_fn_fd]
        l_pattern_l_smps+=[l_smps]
    
    smps=set(l_pattern_l_smps[0])
    for l_smps in l_pattern_l_smps[0]:
        smps=smps.intersection(set(l_smps))
    if len(smps)==0:
        print 'no sample_no in common among different pattern anas'
        return
    
    l_qresampfcn=[]
    for smpcount, smp in enumerate(smps):
        l_q=[]
        l_I=[]
        for count, (pidstr, pattern_l_fn_fd, pattern_l_smps, anap, (anadict, zipclass)) in enumerate(zip(l_plate_idstr, l_pattern_l_fn_fd, l_pattern_l_smps, l_anapath, l_anadict_zipclass)):
            i=pattern_l_smps.index(smp)
            fn, filed, runint=pattern_l_fn_fd[i]
            patternd=readcsvdict(get_file_path(anap, fn, zipclass), filed, returnheaderdict=False, zipclass=zipclass, includestrvals=False)
            l_q+=[patternd[q_key]]
            l_I+=[patternd[intensity_key]]
        if smpcount==0:
            qmin=min([q.min() for q in l_q])
            qmax=max([q.max() for q in l_q])
            
            if not dq is None:
                L=(qmax-qmin)//dq+1
                q_resamp=numpy.linspace(qmin, qmax, L)
            elif not q_log_space_coef is None:
                q_resamp=qmin**(numpy.arange(q_log_space_coef))
            else:
                print 'resampling required for merging at this time'
                return
            #assume all patterns same l_q
            qresampfcn=lambda z: interpolate.interp1d(q, z, kind=resamp_interp_order, fill_value=(z.min(), z.max()))(q_resamp)
#TODO
            Iarr=qresampfcn(patternd[intensity_key])

    
    udi_dict['comps']=numpy.array(udi_dict['comps'])
    udi_dict['xy']=numpy.array(udi_dict['xy'])
    udi_dict['Iarr']=numpy.array(udi_dict['Iarr'])
    udi_dict['Q']=numpy.array(udi_dict['Q'])
    
    anap=l_anapath[0]
    anadict=l_anadict_zipclass[0][0]
    pidset=sorted(list(set(l_plate_idstr)))
    pidstr=l_plate_idstr[0]
    lastanak=sort_dict_keys_by_counter(anadict)[-1]
    anak='ana__%d' %(1+int(lastanak.partition('__')[2]))
    udifn=anak+'_'+'_'.join(pidset)+'.udi'
    csvfn=udifn[:-3]+'csv'
    udip=get_file_path(anap, udifn, False)
    anafolder=os.path.split(udip)[0]
    writeudifile(udip, udi_dict)
    
    analysismasterclass.fomdlist=[]
    analysismasterclass.fomnames=['pmx', 'pmy', 'Intensity.max']
    for i in range(len(udi_dict['Iarr'])):
        d={}
        d['sample_no']=udi_dict['sample_no'][i]
        d['Intensity.max']=max(udi_dict['Iarr'][i])
        d['pmx']=udi_dict['xy'][i][0]
        d['pmy']=udi_dict['xy'][i][1]
        d['runint']=udi_dict['runint'][i]
        d['plate_id']=int(udi_dict['plate_id'][i])
        for k, v in zip(udi_dict['compkeys'], udi_dict['comps'][i]):
            d[k]=v
            if i==0:
                analysismasterclass.fomnames+=[k]
        analysismasterclass.fomdlist+=[d]
    analysismasterclass.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
    analysismasterclass.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name='Intensity.max', colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')
    filedesc=analysismasterclass.writefom_bare(anafolder, csvfn, strkeys=[], floatkeys=None, intfomkeys=['runint','plate_id'])
    anadict[anak]={}
    anadict[anak]['name']='Analysis__Create_UDI'
    anadict[anak]['plate_ids']=','.join(pidset)
    anadict[anak]['technique']=anadict['analysis_type']
    anadict[anak]['parameters']={\
    'ana_file_type': pattern_key, \
    'ana_name': ','.join([ad['name'] for ad, zc in l_anadict_zipclass]), \
    'anak': ','.join(l_anak_patterns), \
    'anak_comps': ','.join(l_anak_comps), \
    'pattern_source_analysis_name': anadict[l_anak_patterns[0]]['name'], \
    'plate_id': ','.join(pidset), \
    'q_key': q_key, \
    'intensity_key': intensity_key, \
    }
    anadict[anak]['files_multi_run']={}
    anadict[anak]['files_multi_run']['fom_files']={}
    anadict[anak]['files_multi_run']['fom_files'][csvfn]=filedesc
    anadict[anak]['files_multi_run']['misc_files']={}
    anadict[anak]['files_multi_run']['misc_files'][udifn]='%s_udi_file' %anadict[anak]['technique']
    
    fs=strrep_filedict(anadict)
    with open(anap, mode='w') as f:
        f.write(fs)


def numpts_log_q_sampling_calculator(qmin, qmax, q_peak, dq_peak, numppts_fwhm=8):
    L=1.+numpy.log(qmax/qmin)/numpy.log(dq_peak/q_peak+1.)
    return int(numpy.round(L*numppts_fwhm))

def log_spacing_coef_numpts(qmin, qmax, numpts):
    return (qmax/qmin)**(1./(numpts-1.))

def percent_change_in_lattice_contsant(rho, num_shifted_patterns):
    return 100.*(rho**(num_shifted_patterns-1.)-1.)

#for xrds q going from 5.33065 to 27.5384, 700 data point resampling in log q makes the spacing 1.00235198 and with 10 shifted patterns would model 2.14% lattice constant change

#p=r'L:\processes\analysis\temp\20171005.180913.run\20171005.180913.ana'
p=r'L:\processes\analysis\ssrl\20171012.133143.run\20171012.133143.ana'

#append_udi_to_ana(l_anapath=[p], l_anak_comps=['ana__7'], l_anak_patterns=['ana__2'], pattern_key='pattern_files', compkeys='AtFrac', q_key='q.nm_processed',intensity_key='intensity.counts_processed')
#append_udi_to_ana(l_anapath=[p], l_anak_comps=['ana__7'], l_anak_patterns=['ana__1'], pattern_key='pattern_files', compkeys='AtFrac', q_key='q.nm',intensity_key='intensity.counts')



