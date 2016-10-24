import numpy, copy, operator
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.split(os.getcwd())[0])

from fcns_math import *
from stack_plot_fcn import stackplot




class Std_Stack_Plot():
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams=dict([])
        self.params=copy.copy(self.dfltparams)
        self.stackplot_name='Std_Stack_Plot'



    def processnewparams(self, StackPlotDialogclass=None):
        return
    
    def stackplot(self, ax, StackPlotDialogclass=None, stackplotkwargs={'alpha':1., 'lw':0, 'zorder':1}):
        
        stackplot(ax, StackPlotDialogclass.stackplotd['xarr'], StackPlotDialogclass.stackplotd['stackarr_keysbyxpts'], colors=StackPlotDialogclass.stackcolors, **stackplotkwargs)

StackClasses=[Std_Stack_Plot()]
