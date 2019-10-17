import sys
import shutil
import os
import pickle
import pandas as pd
from glob import glob
from copy import copy
sys.path.append(os.path.split(os.getcwd())[0])
sys.path.append(os.path.join(os.getcwd(), 'AuxPrograms'))

from fcns_io import timestampname, strrep_filedict, rcp_to_dict

# specify ana type
anatype = 'ecms'

# ana name, ana_int
anas_to_merge = [
    ("20191001.095236", 3),
    ("20191001.105217", 3),
    ("20191001.111155", 3),
    ("20191001.111521", 3),
    ("20191001.111725", 3),
    ("20191001.111836", 3),
]

tups_to_merge = [(anaint, glob('L:\\processes\\analysis\\%s\\%s.*\\*.ana' %
                               (anatype, anats))[0]) for anats, anaint in anas_to_merge]
aux_ana_ints = ','.join([str(i) for i, p in tups_to_merge])
aux_ana_path = ','.join([p.replace(r'L:\processes\analysis', '').replace(
    '\\', "/") for i, p in tups_to_merge])

new_ts = timestampname()
new_anadir = 'L:\\processes\\analysis\\%s\\%s.done' % (anatype, new_ts)
new_expdir = 'L:\\processes\\experiment\\%s\\%s.done' %(anatype, new_ts)
os.makedirs(new_anadir)
os.makedirs(new_expdir)

batchruncounts = 0
new_anad = {'name': new_ts,
            'analysis_type': anatype,
            'access': 'hte',
            'ana_version': '3',
            'created_by': anatype,
            'experiment_name': '%s' % (new_ts),
            'experiment_path': '/%s/%s.done' % (anatype, new_ts),
            'ana__1': {'name': 'Analysis__AppendFoms_GenExperiment',
                       "parameters": {
                           #'aux_ana_path': 'custom',
                           'append_ana_ints': aux_ana_ints,
                           'append_ana_path': aux_ana_path,
                       },
                       "analysis_fcn_version": 1,
                       "analysis_general_type": 'process_fom',
                       "run_use_option": 'data',
                       }
            }

new_expd = {'name': new_ts,
            'experiment_type': anatype,
            'access': 'hte',
            'exp_version': 3,
            'created_by': anatype,
            }

exp_plate_ids = []
exp_run_ids = []

fomdf_list = []
all_samples_list = []
common_cols = []

for anaidx, (anaint, anap) in enumerate(tups_to_merge):
    anad = rcp_to_dict(anap)
    anablk = anad['ana__%i' % (anaint)]
    expp = 'J:/hte_jcap_app_proto/experiment%s' % (anad['experiment_path'])
    expd = rcp_to_dict(expp)
    exp_run_ids += [int(x) for x in expd['run_ids'].strip().split(',')]
    exp_plate_ids += expd['plate_ids'].strip().split(',')

    run_blocks = [k for k in expd.keys() if 'run__' in k]
    run_blocks.sort(key=lambda x: int(x.replace('run__', '')))
    for rblk in run_blocks:
        # TODO: filter duplicate samples out of expd? perhaps not necessary if runint splits same sample nums
        new_expd['run__%i' % (int(rblk.replace('run__', '')) +
                              batchruncounts)] = copy(expd[rblk])

    fomcsv = [k for k, v in anablk['files_multi_run']
              ['fom_files'].items() if v.startswith('csv_fom_file')][0]
    ftype, colnamestr, skipstr, colnumstr = anablk['files_multi_run']['fom_files'][fomcsv].strip(
    ).split(';')
    colnames = colnamestr.strip().split(',')
    skipnum = int(skipstr)
    colnum = int(colnumstr)

    fomcsvp = os.path.join(os.path.dirname(anap), fomcsv)
    fomdf = pd.read_csv(fomcsvp, skiprows=skipnum, names=colnames)
    # check for existing samples
    ana_sample_list = [s for s in list(
        fomdf['sample_no'].values) if s not in all_samples_list]

    file_blocks = [k for k in anablk.keys() if 'files_run__' in k]
    file_blocks.sort(key=lambda x: int(x.replace('files_run__', '')))
    for fblk in file_blocks:
        newfblk = {}
        for subk in anablk[fblk].keys():  # update new ana dict
            newfblk[subk] = {}
            for fn, infostr in anablk[fblk][subk].items():
                if int(infostr.split(';')[-1]) in ana_sample_list:
                    newfn = '__'.join(['ana__1'] + fn.split('__')[2:])
                    newfblk[subk][newfn] = infostr
                    shutil.copy2(os.path.join(os.path.dirname(anap), fn),
                                 os.path.join(new_anadir, newfn))

        new_anad['ana__1']['files_run__%i' %
                           (int(fblk.replace('files_run__', ''))+batchruncounts)] = newfblk

    fomdf['runint'] = fomdf['runint']+batchruncounts
    fomdf.insert(3, 'anaidx', anaidx)
    fomdf_list.append(copy(fomdf))
    if anaidx > 0:
        common_cols = [k for k in common_cols if k in list(fomdf.columns)]
    else:
        common_cols = list(fomdf.columns)
    all_samples_list += ana_sample_list
    batchruncounts += len(run_blocks)

bigdf = pd.concat(fomdf_list, ignore_index=True)
fom_dict = {k: list(bigdf[k].values) if bigdf[k].dtype != 'float64' else [
    '%.3e' % x for x in bigdf[k].values] for k in common_cols}


pidstr = ','.join([str(pid) for pid in set(exp_plate_ids)])
runstr = ','.join([str(run) for run in set(fomdf['runint'])])

new_anad['ana__1']["plot_parameters"] = anablk['plot_parameters']
new_anad['ana__1']["plate_ids"] = pidstr
new_anad['ana__1']["description"] = 'Combine anas, append csv_fom_files, copy files_run_, and generate exps; run %s; plate_id %s' % (
    runstr, pidstr)
common_colstr = ','.join([k for k in common_cols if k not in [
                         'sample_no', 'runint', 'plate_id', 'anaidx']])
new_anad['ana__1']['parameters']['select_fom_keys'] = common_colstr
# use last fomcsv filename for new file
new_ana_fn = '__'.join(['ana__1'] + fomcsv.split('__')[2:])
new_anad['ana__1']['files_multi_run'] = {"fom_files": {
    new_ana_fn: 'csv_fom_file;%s;9;%i' % (','.join(common_cols), len(fom_dict['sample_no']))}}
new_anad['description'] = 'Analysis__AppendFoms_GenExperiment on plate_id %s' % (pidstr)

new_expd['plate_ids'] = pidstr
new_expd['description'] = expd['description']

fomstrlist = ['1\t%i\t%i\t7' % (len(common_cols), len(fom_dict['sample_no']))] + \
             ['csv_version: 1'] + \
             ['plot_parameters:'] + \
             ['    plot__1:'] + \
             ['        colormap: viridis'] + \
             ['        colormap_over_color: (0.993248, 0.906157, 0.143936)'] + \
             ['        colormap_under_color: (0.267004, 0.004874, 0.329415)'] + \
             ['        fom_name: max.FETotal'] + \
             [','.join(common_cols)] + \
             [','.join(z) for z in zip(*[[str(x) for x in fom_dict[k]]
                                         for k in common_cols])]
fomfilestr = '\n'.join(fomstrlist)
with open(os.path.join(new_anadir, new_ana_fn), 'w') as f:
    f.write(fomfilestr)


def dict_to_rcp(d, level=0):
    essentialkeys = ['name', 'ana_version' 'exp_version', 'analysis_type', 'experiment_type',
                     'description', 'plate_ids', 'run_ids', 'created_by', 'access', 'parameters', 'run_use_option']
    prekeys = [k for k in essentialkeys if k in d.keys()]
    postkeys = [k for k in d.keys() if k not in prekeys and k.split(
        '__')[-1].isdigit()]
    midkeys = [k for k in d.keys() if k not in prekeys and k not in postkeys]
    postkeys.sort(key=lambda x: int(x.split('__')[-1]))
    midkeys.sort()
    strlist = []
    for k in prekeys + midkeys + postkeys:
        v = d[k]
        if isinstance(v, dict):
            strlist.append(' '*(4*level) + '%s:' % (k))
            strlist += dict_to_rcp(v, level+1)
        else:
            strlist.append(' '*(4*level) + '%s: %s' % (k, str(v)))
    return(strlist)


new_anastrlist = dict_to_rcp(new_anad)
anafilestr = '\n'.join(new_anastrlist)

with open(os.path.join(new_anadir, '%s.ana' % (new_ts)), 'w') as f:
    f.write(anafilestr)

new_expstrlist = dict_to_rcp(new_expd)
expfilestr = '\n'.join(new_expstrlist)

with open(os.path.join(new_expdir, '%s.exp' % (new_ts)), 'w') as f:
    f.write(expfilestr)


print('merged ana:  ' + os.path.join(new_anadir, '%s.ana' % (new_ts)))
print('merged exp:  ' + os.path.join(new_expdir, '%s.exp' % (new_ts)))