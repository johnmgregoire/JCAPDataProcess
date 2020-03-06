import sys
import os
from time import sleep
############
projectroot = os.path.split(os.getcwd())[0]
sys.path.append(projectroot)
sys.path.append(os.path.join(projectroot, 'QtForms'))
sys.path.append(os.path.join(projectroot, 'AuxPrograms'))
sys.path.append(os.path.join(projectroot, 'OtherApps'))


from DBPaths import *
from SaveImagesApp import *
from fcns_ui import *
from fcns_io import *
from VisualizeBatchFcns import choosexyykeys
from VisualizeDataApp import visdataDialog
from CalcFOMApp import calcfomDialog
from CreateExperimentApp import expDialog
from merge_interp_xrfs_single_plate_id import merge_interp_xrfs_single_plate_id


class MainMenu(QMainWindow):
    def __init__(self, previousmm, execute=True):  # , TreeWidg):
        super(MainMenu, self).__init__(None)
        self.setWindowTitle('HTE Experiment and FOM Data Processing')
        self.calcui = calcfomDialog(
            self, title='Calculate FOM from EXP', guimode=False)


interpd = {}
# with open('K:/users/guevarra/mp_followup/output/ana_interp_list_20190911.tsv', 'r') as f:
# with open('K:/users/guevarra/mp_followup/output/ana_interp_list_20190917.tsv', 'r') as f:
with open('K:/users/guevarra/mp_followup/output/ana_interp_list_20190918.tsv', 'r') as f:
    for l in f.readlines():
        p = l.strip().split('\t')
        interpd[p[0]] = p[1].split(', ')

for anats, keylist in interpd.items():
    try:
    # if 1:
        mainapp = QApplication(sys.argv)
        form = MainMenu(None)
        calcui = form.calcui
        print(anats, keylist)
        merge_interp_xrfs_single_plate_id(
            calcui=calcui,
            ananame='eche/'+anats,
            pidstr=None,
            l_anak_to_merge=keylist,
            xrfs_ana_int='highest containing search string',
            atfrac_search_string='AtFrac',
            interpmerge=True,
            save_extension='.done',
            interpkeys='platemap_xy_line')

        # anasavefolder = calcui.saveana(
        #     dontclearyet=False, anatype=anadestchoice, rundone=anasaveextension)
        calcui.close()
        sleep(0.5)
        mainapp.quit()
        sleep(0.5)
        del calcui
        del mainapp
    except:
        print('Error processing %s' % (anats))
        calcui.close()
        sleep(0.5)
        mainapp.quit()
        sleep(0.5)
        del calcui
        del mainapp

# openwindow()
