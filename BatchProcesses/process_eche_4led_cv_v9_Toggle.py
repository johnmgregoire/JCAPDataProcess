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
            self.expui = expDialog(self, title='Create/Edit an Experiment')
            self.calcui = calcfomDialog(
                self, title='Calculate FOM from EXP', guimode=False)
            self.visdataui = visdataDialog(
                self, title='Visualize Raw, Intermediate and FOM data', GUIMODE=False)

        def visui_exec(self, show=False):
            if self.visdataui is None:
                self.visdataui = visdataDialog(
                    self, title='Visualize Raw, Intermediate and FOM data')
            if show:
                self.visdataui.show()

        def visexpana(self, anafiledict=None, anafolder=None, experiment_path=None, show=False):
            self.visui_exec(show=show)
            if not (anafiledict is None or anafolder is None):
                self.visdataui.importana(
                    anafiledict=anafiledict, anafolder=anafolder)
            elif not experiment_path is None:
                self.visdataui.importexp(experiment_path=experiment_path)


def process_run(rf, ksl):
    runfolder = rf
    keepsmplist = ksl
    runfoldername = os.path.join('eche', 'hte-eche-05', '%s' % (runfolder))
    keepsmpstr = ','.join([str(x) for x in keepsmplist])

    mainapp = QApplication(sys.argv)

    form = MainMenu(None)

    expui = form.expui
    expui.SampleListLineEdit.setText(keepsmpstr)
    calcui = form.calcui
    visdataui = form.visdataui

    def select_ana_fcn(calcui, analabel):
        calcui.FOMProcessNamesComboBox.setCurrentIndex(0)
        cb = calcui.AnalysisNamesComboBox
        for i in range(1, int(cb.count())):
            if (str(cb.itemText(i)).partition('(')[0].partition('__')[2]) == analabel:

                cb.setCurrentIndex(i)
                calcui.getactiveanalysisclass()
                return True
        return False

    def select_procana_fcn(calcui, analabel):
        cb = calcui.FOMProcessNamesComboBox
        for i in range(1, int(cb.count())):
            if (str(cb.itemText(i)).partition('(')[0].partition('__')[2]) == analabel:
                cb.setCurrentIndex(i)
                calcui.getactiveanalysisclass()
                return True
        return False

    def updateanalysisparams(calcui, paramd):
        calcui.analysisclass.params.update(paramd)
        calcui.processeditedparams()

    def select_techtype(searchstr):
        qlist = calcui.TechTypeButtonGroup.buttons()
        typetechfound = False
        for button in qlist:
            if searchstr in str(button.text()).strip():
                button.setChecked(True)
                typetechfound = True
                break
        calcui.fillanalysistypes(
            calcui.TechTypeButtonGroup.checkedButton())
        if not typetechfound:
            calcui.exec_()
            raiseerror

    def plot_new_fom(visdataui, fom_name):
        cb = visdataui.fomplotchoiceComboBox
        for i in range(0, int(cb.count())):
            if str(cb.itemText(i)) == fom_name:
                cb.setCurrentIndex(i)
                visdataui.filterandplotfomdata()
                return True

        return False

    if expname is None:
        if os.path.isdir(runfoldername):
            runsrcfolder = runfoldername
        else:
            runsrcfolder = tryprependpath(RUNFOLDERS, runfoldername)

        expui.importruns_folder(folderp=runsrcfolder)

        expui.ExpTypeLineEdit.setText('eche')
        expui.UserNameLineEdit.setText('eche')
        expui.savebinaryCheckBox.setChecked(False)

        expui.RunTypeLineEdit.setText('data')

        mainitem = expui.techtypetreefcns.typewidgetItem
        for i in range(mainitem.childCount()):
            mainitem.child(i).setCheckState(0, Qt.Checked)
        expui.editexp_addmeasurement()

        saveexpfiledict, exppath = expui.saveexp(
            exptype=expdestchoice, rundone=expsaveextension)

    else:
        saveexpfiledict = None
        exppath = buildexppath(expname)

    print exppath

    analysis_to_do_tups = [
        ('CA1', 'Iphoto', False, {'illum_key': illum_key}, True), ('CA2', 'Iphoto', False, {'illum_key': illum_key}, True), (
            'CA3', 'Iphoto', False, {'illum_key': illum_key}, True), ('CA4', 'Iphoto', False, {'illum_key': illum_key}, True),
        ('CA1', 'SpectralPhoto', False, {}, False),
        ('CV5', 'Iphoto', False, {'illum_key': illum_key}, False),
        ('CV5', 'Pphotomax', False, {
            'v_extend_lower': -0.1, 'v_extend_upper': 0, 'sweep_direction': 'anodic'}, True),
        ('CV5', 'Pphotomax', False, {
            'v_extend_lower': .03, 'v_extend_upper': 0, 'sweep_direction': 'anodic'}, True),
        ('CV5', 'Pphotomax', False, {
            'v_extend_lower': -0.1, 'v_extend_upper': 0, 'sweep_direction': 'cathodic'}, True),
        ('CV5', 'Pphotomax', False, {
            'v_extend_lower': .03, 'v_extend_upper': 0, 'sweep_direction': 'cathodic'}, True),
    ]
    if ananame is None:
        calcui.importexp(exppath=exppath)

        currentana = 1
        for count, (techtypesearch, ana_fcn, isprocess, paramd, cm2convertbool) in enumerate(analysis_to_do_tups):
            print 'calculating ana__%s, %s' % (currentana, ana_fcn)
            select_techtype(techtypesearch)
            if isprocess:
                if not select_procana_fcn(calcui, ana_fcn):
                    calcui.exec_()
                    raiseerror
            else:
                if not select_ana_fcn(calcui, ana_fcn):
                    calcui.exec_()
                    raiseerror
            if len(paramd) > 0:
                updateanalysisparams(calcui, paramd)
            print 'parameters updated, performing calculation'

            calcuierror = calcui.analyzedata()
            currentana += 1

            if calcuierror:
                calcui.exec_()
                raiseerror
            if cm2convertbool:
                print 'converting to m*/cm2'
                calcui.batch_set_params_for_photo_mAcm2_scaling(
                    measurement_area=measurement_area_override)

                calcuierror = calcui.analyzedata()
                currentana += 1
                if calcuierror:
                    calcui.exec_()
                    raiseerror

        pidstr =`calcui.expfiledict['run__1']['parameters']['plate_id']`
        merge_interp_xrfs_single_plate_id(calcui, ananame=None, pidstr=pidstr, l_anak_to_merge=[
            'ana__2', 'ana__4', 'ana__6', 'ana__8', 'ana__12'], save_extension=None)
        anasavefolder = calcui.saveana(
            dontclearyet=True, anatype=anadestchoice, rundone='.run')
        calcui.viewresult(anasavefolder=anasavefolder, show=False)
    else:
        anapath = buildanapath(ananame)
        anasavefolder = os.path.split(anapath)[0]
        visdataui.importana(p=anapath)

    visdataui.stdcsvplotchoiceComboBox.setCurrentIndex(9)
    visdataui.plot_preparestandardplot()
    choosexyykeys(visdataui, ['E.eV_illum', 'EQE', 'None'])
    for fn, filed in visdataui.anafiledict['ana__9']['files_multi_run']['sample_vector_files'].iteritems():
        p = os.path.join(anasavefolder, fn)
        vectrofiled = readcsvdict(
            p, filed, returnheaderdict=False, zipclass=None, includestrvals=False, delim=',')
        if numpy.all(vectrofiled['EQE'] > mineqeforplot):
            filed['path'] = os.path.join(anasavefolder, fn)
            filed['zipclass'] = False
            visdataui.plotxy(filed=filed)
            imagesidialog = visdataui.savefigs(justreturndialog=True)
            imagesidialog.widget_plow_dlist[0]['item'].setCheckState(
                0, Qt.Unchecked)  # plate
            imagesidialog.widget_plow_dlist[1]['item'].setCheckState(
                0, Qt.Unchecked)  # code
            imagesidialog.widget_plow_dlist[2]['item'].setCheckState(
                0, Qt.Checked)  # xy
            imagesidialog.prependfilenameLineEdit.setText(
                'ana__9-sample%d-' % filed['sample_no'])
            imagesidialog.ExitRoutine()

    stdplotinds = [2, 4, 6, 8, 12, 14, 16, 18]
    for i in stdplotinds:
        visdataui.stdcsvplotchoiceComboBox.setCurrentIndex(i)
        visdataui.plot_preparestandardplot()
        inds = numpy.where(numpy.logical_not(
            numpy.isnan(visdataui.fomplotd['fom'])))[0]
        if len(inds) > 0:
            samplestoplot = list(visdataui.fomplotd['sample_no'][inds])
            filterinds = [ind for ind, smp in enumerate(
                visdataui.fomplotd['sample_no']) if smp in samplestoplot]
            for k in visdataui.fomplotd.keys():
                if isinstance(visdataui.fomplotd[k], numpy.ndarray):
                    visdataui.fomplotd[k] = visdataui.fomplotd[k][filterinds]
                else:
                    print k
            vmin = max(0, visdataui.fomplotd['fom'].min())*0.99
            vmax = numpy.percentile(visdataui.fomplotd['fom'], 95.)
            if visdataui.fomplotd['fom'].max() < 1.1*vmax:
                vmax = visdataui.fomplotd['fom'].max()
            if not numpy.all((visdataui.fomplotd['fom'] < vmin) | (visdataui.fomplotd['fom'] > vmax)):
                visdataui.vminmaxLineEdit.setText(
                    '%.3f,%.3f' % (vmin, vmax))
                visdataui.plotfom()
                visdataui.vminmaxLineEdit.setText('')
                imagesidialog = visdataui.savefigs(justreturndialog=True)
                imagesidialog.widget_plow_dlist[0]['item'].setCheckState(
                    0, Qt.Checked)  # plate
                imagesidialog.widget_plow_dlist[1]['item'].setCheckState(
                    0, Qt.Unchecked)  # code
                imagesidialog.widget_plow_dlist[2]['item'].setCheckState(
                    0, Qt.Unchecked)  # xy
                imagesidialog.ExitRoutine()
        if i >= 12:
            inds = numpy.where(numpy.logical_not(numpy.isnan(visdataui.fomplotd['fom'])) & (
                visdataui.fomplotd['fom'] >= crit_pmax_mwcm2_for_fillfactor))[0]
            if len(inds) > 0:
                samplestoplot = list(visdataui.fomplotd['sample_no'][inds])
                plot_new_fom(visdataui, 'Fill_factor')
                filterinds = [ind for ind, smp in enumerate(
                    visdataui.fomplotd['sample_no']) if smp in samplestoplot]
                for k in visdataui.fomplotd.keys():
                    if isinstance(visdataui.fomplotd[k], numpy.ndarray):
                        visdataui.fomplotd[k] = visdataui.fomplotd[k][filterinds]
                    else:
                        print k
                vmin = max(0, visdataui.fomplotd['fom'].min())*0.99
                vmax = min(0.8, visdataui.fomplotd['fom'].max())*1.01
                if not numpy.all((visdataui.fomplotd['fom'] < vmin) | (visdataui.fomplotd['fom'] > vmax)):
                    visdataui.vminmaxLineEdit.setText(
                        '%.3f,%.3f' % (vmin, vmax))
                    visdataui.plotfom()
                    visdataui.vminmaxLineEdit.setText('')
                    imagesidialog = visdataui.savefigs(
                        justreturndialog=True)
                    imagesidialog.widget_plow_dlist[0]['item'].setCheckState(
                        0, Qt.Checked)  # plate
                    imagesidialog.widget_plow_dlist[1]['item'].setCheckState(
                        0, Qt.Unchecked)  # code
                    imagesidialog.widget_plow_dlist[2]['item'].setCheckState(
                        0, Qt.Unchecked)  # xy
                    # if need to convert to .done and skipped the fill factor plot, try this - not tested
                    if i == stdplotinds[-1] and 'done' in anasaveextension:
                        imagesidialog.doneCheckBox.setChecked(Qt.Checked)
                        imagesidialog.ExitRoutine()
                        visdataui.importana(p=imagesidialog.newanapath)
                    else:
                        imagesidialog.ExitRoutine()
            # if need to convert to .done and skipped the fill factor plot, try this resave of last image- not tested
            elif i == stdplotinds[-1] and 'done' in anasaveextension:
                imagesidialog = visdataui.savefigs(justreturndialog=True)
                imagesidialog.doneCheckBox.setChecked(Qt.Checked)
                imagesidialog.ExitRoutine()
                visdataui.importana(p=imagesidialog.newanapath)

    mainapp.quit()


# user-entered parameters for mA/cm2 calculation ond chooseing eqe plots
# measurement_area_override=0.58 # for 1.48 mm diameter spot
measurement_area_override = 0.39  # for 1.8 mm diameter spot
mineqeforplot = 1.e-3
crit_pmax_mwcm2_for_fillfactor = .06
illum_key = 'Toggle'
expsaveextension = '.run'
anasaveextension = '.run'

# providing these paths will skip the generation of the exp/ana
expname = None
ananame = None

expdestchoice = 'eche'
anadestchoice = 'eche'

process_tups = (
    # ('20191025_SbCrO_54065', [11758, 11763, 11769, 11775, 11781, 11787, 11793, 11799, 11805, 11811, 11817, 11822, 11828,
    #                          11834, 11840, 11846, 11852, 11858, 11864, 11870, 11876, 11882, 11887, 11893, 11899, 11905, 11911, 11917, 11923]),
    # ('20191008_FeSbO_54155', [16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262, 16268,
    #                          16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363, 16369]),
    # ('20191119_NbMnO_27841', [16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262, 16268,
    #                          16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363]),
    # ('20191029_CuInO_46550', [16192, 16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262,
    #                          16268, 16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363]),
    # ('20191030_SbCoO_22981', [16192, 16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262,
    #                          16268, 16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363]),
    # ('20191009_SbCuO_41308', [16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262, 16268,
    #                          16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16357, 16363, 16369]),
    # ('20191031_SbNiO_22835', [16192, 16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262, 16268,
    #                          16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363, 16369]),
    # ('20191025_SbCrO_54076', [16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262, 16268,
    #                          16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363]),
    # ('20191028_SnMnO_27953', [16192, 16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262,
    #                          16268, 16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357]),
    # ('20191003_PbSbO_54357', [16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262, 16268,
    #                          16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363]),
    # ('20191031_PbSbO_22970', [16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262, 16268,
    #                          16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363]),
    # ('20191119_ZnSbO_23005', [16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262,
    #                          16268, 16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357]),
    # ('20191007_CoSbO_54403', [16203, 16209, 16215, 16221, 16227, 16233, 16239, 16251, 16257, 16262, 16268, 16274,
    #                          16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363, 16369]),
    # ('20191030_FeSbO_22868', [16192, 16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262,
    #                          16268, 16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16351, 16357, 16363]),
    # ('20191004_BiSbO_54166', [16203, 16209, 16233, 16245, 16251, 16257, 16262, 16268, 16274, 16280,
    #                          16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363]),
    # ('20191007_YSbO_54368', [16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262, 16268,
    #                         16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363]),
    # ('20191028_MnCuO_42130', [11787, 11793, 11799, 11805, 11811, 11817, 11822, 11828, 11834, 11840,
    #                          11846, 11852, 11858, 11864, 11870, 11876, 11882, 11893, 11899, 11905, 11911, 11917, 11923]),
    # ('20191008_ZnSbO_54177', [16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262, 16268,
    #                          16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363, 16369]),
    ('20191031_BiSbO_35312', [16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262, 16268,
                              16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363]),
    # ('20191029_TaMnO_39956', [16192, 16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262, 16268,
    #                          16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363, 16369]),
    # ('20191022_NiSbO_54425', [16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262, 16268,
    #                          16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363]),
    # ('20191029_WBiO_46583', [16192, 16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257, 16262,
    #                         16268, 16274, 16280, 16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363]),
    # ('20191021_FeSbO_57181', [16198, 16203, 16221, 16227, 16239, 16251, 16257, 16262, 16268, 16274, 16280,
    #                          16286, 16292, 16298, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357, 16363]),
    ('20191022_FeSbO_57170', [11758, 11763, 11769, 11775, 11781, 11787, 11793, 11799, 11805, 11811, 11817, 11822, 11828,
                              11834, 11840, 11846, 11852, 11858, 11864, 11870, 11876, 11882, 11887, 11893, 11899, 11905, 11911, 11917, 11923]),
    # ('20191009_InSbO_54188', [16192, 16198, 16203, 16209, 16215, 16221, 16227, 16233, 16239, 16245, 16251, 16257,
    #                          16262, 16268, 16274, 16280, 16286, 16292, 16304, 16310, 16316, 16322, 16327, 16333, 16339, 16345, 16351, 16357])
)

for runfolder, keepsmplist in process_tups:
    process_run(runfolder, keepsmplist)
