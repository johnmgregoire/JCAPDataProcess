import numpy, copy, operator
from scipy import interpolate
from scipy.signal import savgol_filter
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    
from fcns_io import *
from Analysis_Master import Analysis_Master_nointer
from scipy.integrate import cumtrapz
analysismasterclass=Analysis_Master_nointer()

def get_element_list_for_list_of_pidstr(l_plate_idstr, union_bool=False):
    if union_bool:
        all_els=[]
        for pidstr in l_plate_idstr:
            all_els+=getelements_plateidstr(pidstr)
        els_to_return=sorted(list(set(all_els)))
    else:
        els_to_return=set(getelements_plateidstr(l_plate_idstr[0]))
        for pidstr in l_plate_idstr[1:]:
            els_to_return=els_to_return.intersection(set(getelements_plateidstr(pidstr)))
        els_to_return=sorted(list(els_to_return))
    return els_to_return
        
def append_udi_to_ana(l_anapath=None, l_anak_comps=None, l_anak_patterns=None, pattern_key='pattern_files', compkeys='AtFrac', q_key='q.nm_processed',intensity_key='intensity.counts_processed', pattern_fn_search_str='', union_el_list=False, xykeys_compcsv=None):
    #if multiple ana paths, the 0th index is the master where the new will be appended, and in the resulting ana__ parameters ana_name,,anak, anak_comps will all be lists to let you know the source of the "merged aux" anas 
    
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
            if (len(found_comp_keys)>0 and isinstance(compkeys, str)) or len(found_comp_keys)==len(compkeys):
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
        
        if xykeys_compcsv is None:
            pmpath=getplatemappath_plateid(pidstr)
            pmlines, pmpath=get_lines_path_file(p=pmpath)
            pmdlist=readsingleplatemaptxt('', lines=pmlines)
            smps=[d['sample_no'] for d in pmdlist]
            fomd['x']=numpy.array([pmdlist[smps.index(smp)]['x'] for smp in fomd['sample_no']])
            fomd['y']=numpy.array([pmdlist[smps.index(smp)]['y'] for smp in fomd['sample_no']])
        else:
            xk, yk=xykeys_compcsv
            fomd['x']=fomd[xk]
            fomd['y']=fomd[yk]
    #get the elements whose comps were found in all ana
    
    els_for_udi_temp=get_element_list_for_list_of_pidstr(l_plate_idstr, union_bool=union_el_list)

    els_for_udi=[]
    for el in els_for_udi_temp:
        #check if el exists in at least one foe the comp anas
        for (pidstr, found_comp_keys) in zip(l_plate_idstr, l_found_comp_keys):
            kl=[k for k in found_comp_keys if (el+'.') in k]
            if len(kl)>0:
                els_for_udi+=[el]
                break
            
    if len(els_for_udi)<2:
        print '^^^aborting because only these elements found in ana compositions: ',  els_for_udi, pidstr
        return
    l_elkey_byel=[]
    #get the elkey  or None for each ana
    for (pidstr, found_comp_keys) in zip(l_plate_idstr, l_found_comp_keys):
        elkey_byel=[]
        for el in els_for_udi:
            kl=[k for k in found_comp_keys if (el+'.') in k]
            elkey_byel+=[None if len(kl)==0 else kl[0]]
        l_elkey_byel+=[elkey_byel]


    
    udi_dict={}
    udi_dict['ellabels']=els_for_udi
    udi_dict['compkeys']=els_for_udi
    udi_dict['xy']=[]
    udi_dict['plate_id']=[]
    udi_dict['comps']=[]
    udi_dict['Iarr']=[]
    udi_dict['runint']=[]
    udi_dict['sample_no']=[]
    udi_dict['pattern_fn']=[]
    
    smps_added_so_far=[]
    for count, (pidstr, elkey_byel, fomd, pattern_l_fn_fd, anap, (anadict, zipclass)) in enumerate(zip(l_plate_idstr, l_elkey_byel, l_comp_fomd, l_pattern_l_fn_fd, l_anapath, l_anadict_zipclass)):
        
        fomdsmps=list(fomd['sample_no'])
        patternsmps=[filed['sample_no'] for fn, filed, runint in pattern_l_fn_fd]
        inds=sorted([fomdsmps.index(smp) for smp in patternsmps if not (pidstr, smp) in smps_added_so_far])
        inds=[i for i in inds if not (True in [numpy.isnan(fomd[elkey][i]) for elkey in elkey_byel if not elkey is None])]#making sure none of the composition values is NaN. if elkey is None then that element isn't for this plate so don't penalize that
        newsmps=[fomdsmps[i] for i in inds]
        smps_added_so_far+=[(pidstr, smp) for smp in newsmps]
        udi_dict['xy']+=[[fomd['x'][i], fomd['y'][i]] for i in inds]
        for i in inds:
            cmp=numpy.array([0. if elkey is None else fomd[elkey][i] for elkey in elkey_byel])
            if cmp.sum()>0.:
                cmp/=cmp.sum()
            udi_dict['comps']+=[cmp]
        udi_dict['plate_id']+=[pidstr]*len(newsmps)
        udi_dict['sample_no']+=newsmps
        for count2, smp in enumerate(newsmps):
            pind=patternsmps.index(smp)
            fn, filed, runint=pattern_l_fn_fd[pind]
            udi_dict['runint']+=[runint]
            patternd=readcsvdict(get_file_path(anap, fn, zipclass), filed, returnheaderdict=False, zipclass=zipclass, includestrvals=False)
            if count==0 and count2==0:
                udi_dict['Q']=patternd[q_key]
            udi_dict['Iarr']+=[patternd[intensity_key]]
            udi_dict['pattern_fn']+=[fn]
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
    anadict[anak]['analysis_function_version']='2'
    anadict[anak]['analysis_general_type']='process_fom'
    anadict[anak]['description']='make udi with comps from %s and patterns from %s' %(','.join(l_anak_comps), ','.join(l_anak_patterns))
    anadict[anak]['plate_ids']=','.join(pidset)
    anadict[anak]['technique']=anadict['analysis_type']
    ananames=[ad['name'] for ad, zc in l_anadict_zipclass]
    anadict[anak]['parameters']={\
    'ana_file_type': pattern_key, \
    'ana_name': ','.join(ananames), \
    'anak': ','.join(l_anak_patterns), \
    'anak_comps': ','.join(l_anak_comps), \
    'pattern_source_analysis_name': anadict[l_anak_patterns[0]]['name'], \
    'plate_id': ','.join(pidset), \
    'q_key': q_key, \
    'intensity_key': intensity_key, \
    }
    auxanainds=[count for count, aname in enumerate(ananames) if ananames[0]!=aname]
    if len(auxanainds)>0:
        rel_path_list=[]
        for l_ind in auxanainds:
            rel_path_list+=[get_relative_path_for_exp_or_ana_full_path(os.path.split(l_anapath[l_ind])[0], exp=False)]
        anadict[anak]['parameters']['aux_ana_path']=','.join(rel_path_list)
        
    anadict[anak]['files_multi_run']={}
    anadict[anak]['files_multi_run']['fom_files']={}
    anadict[anak]['files_multi_run']['fom_files'][csvfn]=filedesc
    anadict[anak]['files_multi_run']['misc_files']={}
    anadict[anak]['files_multi_run']['misc_files'][udifn]='%s_udi_file' %anadict[anak]['technique']
    
    fs=strrep_filedict(anadict)
    with open(anap, mode='w') as f:
        f.write(fs)


def append_resampled_merged_patterns_to_ana(l_anapath=None, l_anak_patterns=None,  l_pattern_fn_search_str=None, pattern_key='pattern_files', q_key='q.nm_processed',intensity_key='intensity.counts_processed', dq=None, q_log_space_coef=None, resamp_interp_order=1, pre_resamp_smooth_fcn=None, gradual_average_overlap_bool=True):
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
                if q_key in filed['keys'] and intensity_key in filed['keys']:
                    l_fn_fd+=[(fn, filed, runint)]
                    l_smps+=[filed['sample_no']]
        l_pattern_l_fn_fd+=[l_fn_fd]
        l_pattern_l_smps+=[l_smps]
    
    smps=set(l_pattern_l_smps[0])
    for l_smps in l_pattern_l_smps[1:]:
        smps=smps.intersection(set(l_smps))
    if len(smps)==0:
        print 'no sample_no in common among different pattern anas'
        gdfhfg
        return
    
    lsmps_reconstruction_area_error=[]
    lsmps_runint=[]
    lsmps_newfn=[]
    lsmps_I_resamp_flattened=[]
    for smpcount, smp in enumerate(smps):
        l_q=[]
        l_I=[]
        for count, (pattern_l_fn_fd, pattern_l_smps, anap, (anadict, zipclass), pattern_fn_search_str) in enumerate(zip(l_pattern_l_fn_fd, l_pattern_l_smps, l_anapath, l_anadict_zipclass, l_pattern_fn_search_str)):
            i=pattern_l_smps.index(smp)
            fn, filed, runint=pattern_l_fn_fd[i]
            if count==0:
                lsmps_runint+=[runint]#might be merging multiple runs but take the first
                newfn=fn[5:].partition('_')[2] if fn.startswith('ana__') else fn
                newfn=newfn.replace(pattern_fn_search_str, 'resampled')
                if not newfn.endswith('.csv'):
                    if '.' in newfn:
                        newfn=newfn.rpartition('.')[0]
                    newfn+='.csv'
                lsmps_newfn+=[newfn]
            patternd=readcsvdict(get_file_path(anap, fn, zipclass), filed, returnheaderdict=False, zipclass=zipclass, includestrvals=False)
            l_q+=[patternd[q_key]]
            if pre_resamp_smooth_fcn is None:
                l_I+=[patternd[intensity_key]]
            else:
                l_I+=[pre_resamp_smooth_fcn(patternd[intensity_key])]
        if smpcount==0:
            qmin=min([q.min() for q in l_q])
            qmax=max([q.max() for q in l_q])
            
            if not dq is None:
                L=int((qmax-qmin)//dq)+1
                q_resamp=numpy.linspace(qmin, qmax, L)
            elif not q_log_space_coef is None:
                L=numpts_log_spacing_coef(qmin, qmax, q_log_space_coef)#will round down num points to be sure q_rasmp within bounds of qmin,qmax
                q_resamp=qmin*(q_log_space_coef**(numpy.arange(L)))
            else:
                print 'resampling required for merging at this time'
                return
            #assume all patterns same l_q
            qresampfcn=lambda l_z: numpy.array([interpolate.InterpolatedUnivariateSpline(q, z, k=resamp_interp_order, ext='zeros')(q_resamp) for q,z in zip(l_q,l_z)])#functino resamps on whole array even if there are lots out of bounds. l_q is local var from smpcount==0 and is used for all later interps
            
            interp_mask_numpatterns_by_qresamp=qresampfcn(l_q)!=0#interpolate q values (could interp zeros but q is avaialble in the right size and nonzero) with 0 fill to see where q_resamp is beyond bounds of each qarr in l_q. This mask is 1 where interp is valid
            numpatterns_contributing_to_each_qresamp_val=interp_mask_numpatterns_by_qresamp.sum(axis=0, dtype=numpy.int32)
            resampinds_zerofill=numpy.where(numpatterns_contributing_to_each_qresamp_val==0)[0]
            resampinds_ave=numpy.where(numpatterns_contributing_to_each_qresamp_val>0)[0]
            if len(resampinds_zerofill)>0:
                print 'there are this many resampled q values that will be zero-filled: ', len(resampinds_zerofill)
            
            weights_2d=numpy.ones(interp_mask_numpatterns_by_qresamp.shape, dtype='float64')
            weights_2d[:, resampinds_zerofill]=0.#this has no consequence due to the zero fill in interp but makes sense to write. These inds have no input data from the patterns
            if gradual_average_overlap_bool and 2 in numpatterns_contributing_to_each_qresamp_val and numpy.all(numpatterns_contributing_to_each_qresamp_val<=2):
                startinds=numpy.where((numpatterns_contributing_to_each_qresamp_val[:-1]==1)&(numpatterns_contributing_to_each_qresamp_val[1:]==2))[0]+1
                stopinds=numpy.where((numpatterns_contributing_to_each_qresamp_val[:-1]==2)&(numpatterns_contributing_to_each_qresamp_val[1:]==1))[0]+1
                if len(stopinds)>0 and len(stopinds)==len(startinds):
                    for i, j in zip(startinds, stopinds):
                        activepatterns=numpy.where(interp_mask_numpatterns_by_qresamp[:, i]==True)[0]
                        #activepatterns is length 2  of pattern indeces tbeing combined from i:j. typically the 0th pattern is coming in from the left and should start with full weight and the 1st pattern start with no wieght and finishes with full. If 1st is coming in from left, flip their order
                        if interp_mask_numpatterns_by_qresamp[activepatterns[1], i-1]:#if the data point before i is active in the 1st pattern, then this pattern is the one with lower Q so reverse their order
                            activepatterns=activepatterns[::-1]
                        newweights=numpy.linspace(0., 1., j-i)
                        weights_2d[activepatterns[0], i:j]=1.-newweights
                        weights_2d[activepatterns[1], i:j]=newweights
            else:
                if gradual_average_overlap_bool:
                    print 'gradual overlap calculation not possible because only implemented for 2-pattern overlaps and the max num of pattern overlaps is ', numpatterns_contributing_to_each_qresamp_val.max(), anap
                for patternind in range(weights_2d.shape[0]):
                    weights_2d[patternind, resampinds_ave]=1./numpatterns_contributing_to_each_qresamp_val[resampinds_ave]#wieght each pattern to obtain mean
        resamparr=qresampfcn(l_I)
        I_resamp_flattened=(resamparr*weights_2d).sum(axis=0)
        #I_resamp_flattened[resampinds_ave]/=numpatterns_contributing_to_each_qresamp_val[resampinds_ave]
        lsmps_I_resamp_flattened+=[I_resamp_flattened]
        #in the individual integrals the overlapped regions will not be averaged so multiply out the averaging weights here,
        area_reconstructed_inresampledpattern=cumtrapz(resamparr.sum(axis=0), x=q_resamp)[-1]#this is done on the sum of interpolated patterns without the weights since the weights aren't applied below. i.e. overlapped portions are double counted here and int he next line
        area_patterns=numpy.sum([cumtrapz(Iarr, x=qarr)[-1] for qarr, Iarr in zip(l_q, l_I)])#these integrals cannot contain the weights_2d because they are nto resampled
        reconstruction_area_error=(area_reconstructed_inresampledpattern-area_patterns)/area_patterns
        lsmps_reconstruction_area_error+=[reconstruction_area_error]

    anap=l_anapath[0]
    anadict=l_anadict_zipclass[0][0]
    lastanak=sort_dict_keys_by_counter(anadict)[-1]
    anak='ana__%d' %(1+int(lastanak.partition('__')[2]))
    csvfn=anak+'_'+pidstr+'.csv'
    csvpath=get_file_path(anap, csvfn, False)
    anafolder=os.path.split(csvpath)[0]

    anadict[anak]={}
    anadict[anak]['name']='Analysis__Resamp_Merge_Patterns'
    anadict[anak]['analysis_function_version']='1.1'
    anadict[anak]['analysis_general_type']='process_fom'
    anadict[anak]['description']=''.join(['resample ', '' if len(l_anak_patterns)==1 else 'and merge',  ' patterns from ', ','.join(l_anak_patterns)])
    anadict[anak]['plate_ids']=pidstr
    anadict[anak]['technique']=anadict['analysis_type']
    tempstr='none' if l_pattern_fn_search_str is None else ','.join(l_pattern_fn_search_str)
    tempstr=tempstr.strip()
    if len(tempstr)==0:
        tempstr='none'
    anadict[anak]['parameters']={\
    'ana_file_type': pattern_key, \
    'ana_name': ','.join([ad['name'] for ad, zc in l_anadict_zipclass]), \
    'anak': ','.join(l_anak_patterns), \
    'pattern_source_analysis_name': anadict[l_anak_patterns[0]]['name'], \
    'plate_id': pidstr, \
    'q_key': q_key, \
    'intensity_key': intensity_key, \
    'pattern_fn_search_str': tempstr, \
    'q_resample_linear_interval':`dq`, \
    'q_resample_log_interval':`q_log_space_coef`, \
    'q_resample_interp_order':`resamp_interp_order`, \
    'gradual_average_overlap_bool':`gradual_average_overlap_bool`, \
    }
    newq_key=q_key+'_resampled'
    newintensity_key=intensity_key+'_resampled'
    analysismasterclass.fomdlist=[]
    analysismasterclass.fomnames=['Reconstruction_Area_Rel_Error']
    for smp, runint, reconstruction_area_error, I_resamp, newfn in zip(smps, lsmps_runint, lsmps_reconstruction_area_error, lsmps_I_resamp_flattened, lsmps_newfn):
        d={}
        d['sample_no']=smp
        d['Reconstruction_Area_Rel_Error']=reconstruction_area_error
        d['runint']=runint
        d['plate_id']=int(pidstr)
        analysismasterclass.fomdlist+=[d]
        
        filesrunk='files_run__%d' %runint
        if not filesrunk in anadict[anak].keys():
            anadict[anak][filesrunk]={}
            anadict[anak][filesrunk][pattern_key]={}
        fn='_'.join([anak, newfn])
        anadict[anak][filesrunk][pattern_key][fn]='%s_csv_pattern_file;%s,%s;1;%d;%d' %(anadict[anak]['technique'], newq_key, newintensity_key, len(q_resamp), smp)
        lines=['%s,%s' %(newq_key, newintensity_key)]
        lines+=['%.6e,%.6e' %t for t in zip(q_resamp, I_resamp)]
        s='\n'.join(lines)
        with open(os.path.join(anafolder, fn), mode='w') as f:
            f.write(s)
                    
    analysismasterclass.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
    analysismasterclass.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name='Reconstruction_Area_Rel_Error', colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')
    filedesc=analysismasterclass.writefom_bare(anafolder, csvfn, strkeys=[], floatkeys=None, intfomkeys=['runint','plate_id'])#floatkeys None uses fomnames
    anadict[anak]['files_multi_run']={}
    anadict[anak]['files_multi_run']['fom_files']={}
    anadict[anak]['files_multi_run']['fom_files'][csvfn]=filedesc

    fs=strrep_filedict(anadict)
    with open(anap, mode='w') as f:
        f.write(fs)


def numpts_log_q_sampling_calculator(qmin, qmax, q_peak, dq_peak, numppts_fwhm=8):
    L=1.+numpy.log(qmax/qmin)/numpy.log(dq_peak/q_peak+1.)
    return int(numpy.round(L*numppts_fwhm))

def log_spacing_coef_numpts(qmin, qmax, numpts):
    return (qmax/qmin)**(1./(numpts-1.))

def numpts_log_spacing_coef(qmin, qmax, q_log_space_coef, round_down_bool=True):
    L=1.+numpy.log(qmax/qmin)/numpy.log(q_log_space_coef)
    if round_down_bool:
        return int(L//1)
    else:
        return L
    
def percent_change_in_lattice_contsant(rho, num_shifted_patterns):
    return 100.*(rho**(num_shifted_patterns-1.)-1.)

smoothfcn=lambda Iraw: savgol_filter(Iraw, 31, 4)



##for xrds q going from 5.33065 to 27.5384, 700 data point resampling in log q makes the spacing 1.00235198 and with 10 shifted patterns would model 2.14% lattice constant change
#
#
##append_udi_to_ana(l_anapath=[p], l_anak_comps=['ana__7'], l_anak_patterns=['ana__2'], pattern_key='pattern_files', compkeys='AtFrac', q_key='q.nm_processed',intensity_key='intensity.counts_processed')
##append_udi_to_ana(l_anapath=[p], l_anak_comps=['ana__7'], l_anak_patterns=['ana__1'], pattern_key='pattern_files', compkeys='AtFrac', q_key='q.nm',intensity_key='intensity.counts')
#
#p=r'L:\processes\analysis\temp\20171017.101645.run\20171017.101645.ana'
#
#append_resampled_merged_patterns_to_ana(l_anapath=[p, p], l_anak_patterns=['ana__1', 'ana__1'],  l_pattern_fn_search_str=['1st_frame', '2nd_frame'], pattern_key='pattern_files', q_key='q.nm_processed',intensity_key='intensity.counts_processed', dq=None, q_log_space_coef=1.00235198, resamp_interp_order=3, pre_resamp_smooth_fcn=smoothfcn)
#append_resampled_merged_patterns_to_ana(l_anapath=[p, p], l_anak_patterns=['ana__2', 'ana__2'],  l_pattern_fn_search_str=['1st_frame', '2nd_frame'], pattern_key='pattern_files', q_key='q.nm',intensity_key='intensity.counts', dq=None, q_log_space_coef=1.00235198, resamp_interp_order=3, pre_resamp_smooth_fcn=smoothfcn)
#append_resampled_merged_patterns_to_ana(l_anapath=[p], l_anak_patterns=['ana__1'],  l_pattern_fn_search_str=['1st_frame'], pattern_key='pattern_files', q_key='q.nm_processed',intensity_key='intensity.counts_processed', dq=None, q_log_space_coef=1.00235198, resamp_interp_order=3, pre_resamp_smooth_fcn=smoothfcn)
#append_resampled_merged_patterns_to_ana(l_anapath=[p], l_anak_patterns=['ana__2'],  l_pattern_fn_search_str=['1st_frame'], pattern_key='pattern_files', q_key='q.nm',intensity_key='intensity.counts', dq=None, q_log_space_coef=1.00235198, resamp_interp_order=3, pre_resamp_smooth_fcn=smoothfcn)


#newanapath=buildanapath(r'L:\processes\analysis\ssrl\20171011.113240.run')
#append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=['ana__4'], l_anak_patterns=['ana__2'], pattern_key='pattern_files', compkeys='AtFrac', q_key='q.nm_processed',intensity_key='intensity.counts_processed')
#append_udi_to_ana(l_anapath=[newanapath], l_anak_comps=['ana__4'], l_anak_patterns=['ana__1'], pattern_key='pattern_files', compkeys='AtFrac', q_key='q.nm',intensity_key='intensity.counts')


