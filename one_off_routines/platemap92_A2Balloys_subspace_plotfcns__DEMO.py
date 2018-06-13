import matplotlib.pyplot as plt
from platemap92_A2Balloys_subspace_plotfcns_v1 import *

#this creates fake data that should be replaced by fomd being the fom csv dictionary
fake_sample_no=np.arange(1, 2200, dtype='int32')
fake_fom=np.float32(fake_sample_no)
fomd={'sample_no':fake_sample_no, 'x':fake_fom}

#this creates a dictionary where keys are sample_no and values are colors - do this once for whole library
sample_color_dict=create_sample_color_dict(fomd, 'x', fake_fom.min(), fake_fom.max(), cm.jet)

#make the plot of A2B - type spinels with no additionall alloying elements and all alloying elements containing X (provided these 3 inds, the others selected automatically) in the provided axes. labelaxes=False to facilitate making an array of subspaces with ax=subplot()
ax=plt.gca()
plot_spinel_subspace(ax, 0, 1, 2,  ellabels=['A','B','C','D','E'], sample_color_dict=sample_color_dict, labelaxes=True)


#make summary plot of all D2E spinels, i.e. 3 panels for each of A,B,C alloying
plt.figure(figsize=(12, 4))
for count in range(3):
    ax=plt.subplot(1, 3, count+1)
    plot_spinel_subspace(ax, 3, 4, count,  ellabels=['A','B','C','D','E'], sample_color_dict=sample_color_dict, labelaxes=False)
plt.subplots_adjust(left=0, right=1, wspace=0, hspace=0)
plt.show()
