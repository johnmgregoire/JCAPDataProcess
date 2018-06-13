import numpy as np

import pickle
import matplotlib.colors as colors
import matplotlib.cm as cm

p=r'K:\users\hte\ProjectSummaries\spinel_alloys\platemap_comps\0092-subspace_subplot_dict.pck'
with open(p, mode='rb') as f:subspace_dict=pickle.load(f)


def get_colors_fom_cmap(fomarr, vmin, vmax, cmap):#if need over/under colors those should have been already set via cmap.set_under, cmap.set_over
    norm=colors.Normalize(vmin=vmin, vmax=vmax, clip=False)
    sm=cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array(fomarr)
    cols=np.float32(map(sm.to_rgba, fomarr))[:, :3]
    return cols

def create_sample_color_dict(fomd, fomk, vmin, vmax, cmap):#fomd has column headings including sample_no and fomk is the column heading of desired fom, then this creates a dict where keys are sample numbers and values are colors according the fom and cmap
    return dict(zip(fomd['sample_no'], get_colors_fom_cmap(fomd[fomk], vmin, vmax, cmap)))
    
def plot_spinel_subspace(ax, Aind_A2B, Bind_A2B, ind_primaryalloyelement,  ellabels=['A','B','C','D','E'], sample_color_dict=None, labelaxes=True):
    

    A, B, X=Aind_A2B, Bind_A2B, ind_primaryalloyelement
    ad=subspace_dict[(A, B)]['subplot_info_each_alloy_chan'][X]
    
    Y, Z=ad['other_2_inds__subplot']

    for ind, (x, y, t, c, o, s) in enumerate(zip(ad['host_ab_comp__subplot'], ad['row_index__subplot'], ad['shape_types__subplot'], ad['comps__subplot'], ad['comp_order__subplot'], ad['sample_no_array__subplot'])):
        v0=[(-1, -1), (-1, 1), (1, 1), (1, -1)]
        v1=[(-1, -1), (-1, 1),(1, -1)]
        v2=[(-1, 1), (1, 1), (1, -1)]
        
        varr=[v0, v1, v2]
        
        if sample_color_dict is None:
            col=['b', 'm', 'orange', 'g'][o-2]
        elif s in sample_color_dict.keys():
            col=sample_color_dict[s]
            if np.isnan(col).sum():
                col=None
        else:
            col=None
        if not col is None : #if color not provided or color contains nan then skip plotting
            ax.plot(x, y, c=col, mec='k', marker=varr[t], ms=20)#['s', 'v', '^'][t]
            s=''.join(['%s$_{%.3f}$' %(ellabels[ind], c[ind]) for ind in [X, Y, Z] if c[ind]>0])
            if t==1:
                ax.text(x, y-0.5, s, va='bottom', ha='center')
            else:
                ax.text(x, y+0.5, s, va='top', ha='center')
        
    ax.plot([0.667], [0], 'kx')
    ax.set_ylim(-.5, 7.5)
    ax.set_xlim(.58, .75)
    ax.set_yticklabels([])
    if labelaxes:
        ax.set_ylabel('compositional complexity (arb)')
        ax.set_xlim(.58, .75)
        ax.set_xlabel('%s/(%s+%s)' %(ellabels[A], ellabels[A], ellabels[B]))
    else:
        ax.set_xticklabels([])



