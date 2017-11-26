from __future__ import print_function
try:
    import xylib
except:
    print('VAMAS file cannot be parsed because xylib is not installed')

def get_vamas_as_dict_containing_blocks(filename):
    data_file = xylib.load_file(fi)
    nb = data_file.get_block_count()
    all_blocks = {}
    for block in range(nb):
        #basic info about the current block
        block = data_file.get_block(block)
        name = block.get_name()
        ncol = block.get_column_count()
        nrow = block.get_point_count()
        #get the column names and populate a dict with the values of each column
        #this is a little pedestrian but xylib forces you to do so
        col_names = [block.get_column(k).get_name() or ('column_%d' % k)
                     for k in range(1, ncol+1)]
        col_values = []
        # from xylib: column 0 is pseudo-column with point indices
        for i in range(len(col_names)):
            col_values.append([block.get_column(i+1).get_value(j) for j in range(nrow)])
        all_blocks[name] = {col_names[i]:col_values[j] for i,j in zip(range(ncol),range(len(col_names)))}
    return all_blocks

'''
#test the function
fi = '/Users/helgestein/Documents/PythonScripts/xps/testset.vms'
xps_data = get_vamas_as_dict_containing_blocks(fi)
#xps_data.keys()
#xps_data['wide 80eV/2'].keys()
import pylab as plt
import seaborn as sns
plt.plot(xps_data['wide 80eV/2']['Kinetic Energy'],xps_data['wide 80eV/2']['Intensity'])
plt.show()
'''
