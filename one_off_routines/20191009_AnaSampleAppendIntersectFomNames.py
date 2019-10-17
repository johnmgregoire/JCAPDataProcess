'''
routine for appending ECMS anas into a source ana (creates a copy), but doesn't
work with VisualizeDataApp since auxiliary anas won't have experiments/runs that
exist in source experiment/runs; may be useful only for fom csv merging
'''

import sys
import shutil
import os
import pickle
import pandas as pd
from glob import glob
sys.path.append(os.path.split(os.getcwd())[0])
sys.path.append(os.path.join(os.getcwd(), 'AuxPrograms'))
from fcns_io import readana, timestampname, strrep_filedict

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

### append anas, first ana in list will be used as source

paths_to_merge = [p for p in glob('L:\\processes\\analysis\\%s\\*\\*.ana' %(anatype)) if any([a in p for a,i in anas_to_merge])]

source_anap = paths_to_merge[0]
source_anai = anas_to_merge[0][1]
source_dict = readana(source_anap)

source_fn=source_dict['ana__%i' %(source_anai)]['files_multi_run']['fom_files'].keys()[0]
source_skip=source_dict['ana__%i' %(source_anai)]['files_multi_run']['fom_files'][source_fn]['num_header_lines']
source_csv_path=os.path.join(os.path.dirname(source_anap), source_fn)
keep_cols=source_dict['ana__%i' %(source_anai)]['files_multi_run']['fom_files'][source_fn]['keys']

source_df = pd.read_csv(source_csv_path, skiprows=source_skip, names=keep_cols)
source_df.insert(3, 'anaidx', 0)

keep_cols=keep_cols[:3] + ['anaidx'] + keep_cols[3:]
fom_dict = {k: list(source_df[k].values) if source_df[k].dtype!='float64' else ['%.3e' %x for x in source_df[k].values] for k in keep_cols}

for i in range(len(paths_to_merge[1:])):
    merge_anap = paths_to_merge[1:][i]
    merge_anai = anas_to_merge[1:][i][1]
    merge_dict = readana(merge_anap)

    merge_fn=merge_dict['ana__%i' %(merge_anai)]['files_multi_run']['fom_files'].keys()[0]
    merge_skip=merge_dict['ana__%i' %(merge_anai)]['files_multi_run']['fom_files'][merge_fn]['num_header_lines']
    merge_csv_path=os.path.join(os.path.dirname(merge_anap), merge_fn)
    merge_cols=merge_dict['ana__%i' %(merge_anai)]['files_multi_run']['fom_files'][merge_fn]['keys']

    merge_df = pd.read_csv(merge_csv_path, skiprows=merge_skip, names=merge_cols)
    merge_df = merge_df[~(merge_df['sample_no'].astype('str') + '_' + merge_df['plate_id'].astype('str')).isin(['%i_%i' %(s, p) for s, p in zip(fom_dict['sample_no'], fom_dict['plate_id'])])]
    merge_df.insert(3, 'anaidx', i+1)

    merge_cols=merge_cols[:3] + ['anaidx'] + merge_cols[3:]
    keep_cols = [k for k in keep_cols if k in merge_cols]
    aux_dict = {k: list(merge_df[k].values) if merge_df[k].dtype!='float64' else ['%.3e' %x for x in merge_df[k].values] for k in merge_cols}

    for k in keep_cols:
        fom_dict[k]+=aux_dict[k]


last_ana_int = max([int(s.replace('ana__', '')) for s in source_dict.keys() if 'ana__' in s])
new_ana_fn = 'ana__%i__' %(last_ana_int+1) + '__'.join(source_fn.split('__')[2:])

new_ana_block = {
    "name": "Analysis__Append_Sample_Plate_FOM_Intersection",
    "parameters": {
        'aux_ana_ints': ','.join([str(i) for a,i in anas_to_merge]),
        'aux_ana_path': ','.join(['self']+[p.replace(r'L:\processes\analysis', '').replace('\\', "/") for p in paths_to_merge[1:]]),
        'select_ana': 'ana__%i' %(source_anai),
        'select_aux_keys': ','.join(keep_cols[4:]),
        'select_fom_keys': ','.join(keep_cols[4:]),
    },
    "analysis_fcn_version": 1,
    "analysis_general_type": source_dict['ana__%i' %(source_anai)]['analysis_general_type'],
    "plot_parameters": source_dict['ana__%i' %(source_anai)]['plot_parameters'],
    "plate_ids": ','.join([str(p) for p in set(fom_dict['plate_id'])]),
    "description": '; '.join(['process ana__%i' %(source_anai)] + source_dict['ana__%i' %(source_anai)]['description'].split('; ')[1:]),
    "run_use_option": "data",
    "files_multi_run": {
        "fom_files": {
            new_ana_fn: {
                "file_type": "csv_fom_file",
                "keys": keep_cols,
                "num_data_rows": len(fom_dict['sample_no']),
                "num_header_lines": 9
            }
        }
    }
}


source_dict['ana__%i' %(last_ana_int+1)] = new_ana_block
new_ts = timestampname()
source_dict["name"] = new_ts

new_anadir = 'L:\\processes\\analysis\\%s\\%s.run' %(anatype, new_ts)



os.makedirs(new_anadir)

source_anadir = os.path.dirname(source_anap)
source_files = [f for f in os.listdir(source_anadir) if os.path.basename(source_anap)[:-4] not in f]
for f in source_files:
    shutil.copy2(os.path.join(source_anadir, f), os.path.join(new_anadir, f))

anafilestr = strrep_filedict(source_dict)
# remove trailing ;0 at the end of fom_files description
anastrlist = anafilestr.split('\n')
anastrlist = [l[:-2] if 'csv_fom_file' in l and l.endswith(';0') else l for l in anastrlist]
anafilestr = '\n'.join(anastrlist)

with open(os.path.join(new_anadir, '%s.ana' %(new_ts)), 'w') as f:
    f.write(anafilestr)

pickle.dump(source_dict, open(os.path.join(new_anadir, '%s.pck' %(new_ts)), 'w'))


fomstrlist = ['1\t%i\t%i\t7' %(len(keep_cols), len(fom_dict['sample_no']))] + \
             ['csv_version: 1'] + \
             ['plot_parameters:'] + \
             ['    plot__1:'] + \
             ['        colormap: viridis'] + \
             ['        colormap_over_color: (0.993248, 0.906157, 0.143936)'] + \
             ['        colormap_under_color: (0.267004, 0.004874, 0.329415)'] + \
             ['        fom_name: max.FETotal'] + \
             [','.join(keep_cols)] + \
             [','.join(z) for z in zip(*[[str(x) for x in fom_dict[k]] for k in keep_cols])]
fomfilestr='\n'.join(fomstrlist)

with open(os.path.join(new_anadir, new_ana_fn), 'w') as f:
    f.write(fomfilestr)
