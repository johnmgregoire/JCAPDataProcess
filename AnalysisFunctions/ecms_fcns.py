import numpy, copy, operator
import time, pickle, zipfile

if __name__ == "__main__":
    import os, sys
    #__file__=r'D:\Google Drive\Documents\PythonCode\JCAP\JCAPDataProcess\AnalysisFunctions\ecms.py'
    sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AuxPrograms'))
    sys.path.append(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0], 'AnalysisFunctions'))

from fcns_math import *
from fcns_io import *
from fcns_ui import *
from csvfilewriter import createcsvfilstr, createcsvfilstr_bare
from Analysis_Master import *
from FOM_process_basics import *
import numpy as np
from scipy import signal
from scipy.optimize import minimize_scalar
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


loss_fcn_dict={\
'L2_5x_positive':lambda resid: np.where(resid>0.,5.*resid**2,resid**2),\
'L2':lambda resid: resid**2,\
'L1':lambda resid: np.abs(resid),\
'LogCosh_1E9':lambda resid: np.log(np.cosh(resid*1.e9)),\
'L2_5x_first_half':lambda resid: np.where(np.arange(len(resid))<(len(resid)//2),5.*resid**2,resid**2),\
'L2_3x_first_half_3x_positive':lambda resid: np.where(np.arange(len(resid))<(len(resid)//2),3.*np.where(resid>0.,3.*resid**2,resid**2),np.where(resid>0.,3.*resid**2,resid**2)),\
'L2_3x_first_half_5x_positive':lambda resid: np.where(np.arange(len(resid))<(len(resid)//2),3.*np.where(resid>0.,5.*resid**2,resid**2),np.where(resid>0.,5.*resid**2,resid**2)),\
'L2_inv_prop_to_time':lambda resid: (np.arange(len(resid))+1.)[::-1]*resid**2,\
}


import matplotlib.colors as colors
import matplotlib.cm as cm

def get_colors_fom_cmap(fomarr, vmin, vmax, cmap):#if need over/under colors those should have been already set via cmap.set_under, cmap.set_over
    norm=colors.Normalize(vmin=vmin, vmax=vmax, clip=False)
    sm=cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array(fomarr)
    cols=np.float32(map(sm.to_rgba, fomarr))[:, :3]
    return cols

def read_ecms_simulation_data(ms_simulation_model,species_list):
    fold=tryprependpath(ECMSPROCESSFOLDERS, '', testfile=False, testdir=True)
    fold=os.path.join(fold,ms_simulation_model)

    d={}

    p=os.path.join(fold,'model_params.npy')
    d['model_params']=np.load(p, allow_pickle=False)

    p=os.path.join(fold,'metadata.txt')
    with open(p,mode='r') as f: metad=filedict_lines(f.readlines())

    d['metadata']=metad
    d['echem_profile']={}
    for k,v in d['metadata'].iteritems():
        if not isinstance(v,str):
            continue
        d['metadata'][k]=[attemptnumericconversion_tryintfloat(v2) for v2 in v.split(',')] if ',' in v else attemptnumericconversion_tryintfloat(v)
    for k,v in metad['echem_profile'].iteritems():
        d['echem_profile'][k]=np.array([attemptnumericconversion_tryintfloat(v2) for v2 in v.split(',')]) if ',' in v else attemptnumericconversion_tryintfloat(v)

    for s in species_list:
        p=os.path.join(fold,'library_%s.npy' %s)
        d[s]={}
        arr=np.load(p, allow_pickle=False)
        for count,k in enumerate(metad['library_array_names']):
            d[s][k]=arr[count]
    return d


#p=r'K:\experiments\anec\2019 ECMS\rcp\demo_181102 CuZn library_43962\20181102_MS_43962\20181102_mass__2.csv'
def read_hiden_csv(p):
    if p.startswith('/'):
        p = ('J:/hte_jcap_app_proto/run%s' %(p))
        target = os.path.basename(p)
        zipfn = os.path.dirname(p) if '.zip' in p else '%s.zip' %(os.path.dirname(p))
        with zipfile.ZipFile(zipfn) as zf:
            with zf.open(target, 'rU') as f:
                lines=f.readlines()
    else:
        with open(p,mode='r') as f:
            lines=f.readlines()

    date_time_str=[l.strip() for l in lines if l.startswith('"Date",')][0]
    ms_start_time=time.strptime(' '.join(date_time_str.split(',')[1::2]), '%m/%d/%Y %I:%M:%S %p')
    i=[count for count,l in enumerate(lines) if l.startswith('"Time",')][0]
    msl=[]
    vl=[]

    for l in lines[i+1:]:
        ms,v=l.split(',')[1:3]
        msl+=[int(ms)]
        vl+=[float(v)]
    return ms_start_time,np.array(msl),np.array(vl)

def get_time_struct_dta(p):
    with open(p,mode='r') as f:
        lines=f.readlines()
    s=''
    for k in ['DATE','TIME']:
        lst=[l for l in lines if l.startswith(k)][0].split('\t')
        s+=lst[2].strip()+' '
    return time.strptime(s, '%m/%d/%Y %H:%M:%S ')


def eche_split_current_by_sweep_and_generate_intended_voltage(tech,sim_lib_dict,echem_t,echem_i,smooth_paramd=None,time_delta=0.5):
    if tech.startswith('CV'):
        sim_basis_v=echem_t*np.nan
        sweep_currents=[]
        profd=sim_lib_dict['echem_profile']
        segment_index_arr=[]
        for count,(t0,t1,v0,v1) in enumerate(zip(profd['sweep_endpoint_times_s'],profd['sweep_endpoint_times_s'][1:],profd['sweep_endpoint_potentials_vrhe'],profd['sweep_endpoint_potentials_vrhe'][1:])):
            inds=np.where((echem_t>=t0) & (echem_t<=t1))[0]
            fr=(echem_t[inds]-t0)/(t1-t0)
            sim_basis_v[inds]=v0+fr*(v1-v0)
            sweep_currents+=[echem_i[inds]]
            segment_index_arr+=[count]*len(inds)#TODO. nothing here makes this be the correct total length because echem_t may be longer (go beyond bounds of the profile)
        for nanind in np.where(np.isnan(sim_basis_v))[0]:
            goodinds=np.where(np.logical_not(np.isnan(sim_basis_v)))[0]
            replace_ind=goodinds[np.argmin((echem_t[goodinds]-echem_t[nanind])**2)]
            if np.abs(echem_t[replace_ind]-echem_t[nanind])<time_delta:
                sim_basis_v[nanind]=sim_basis_v[replace_ind]
        if smooth_paramd is None or smooth_paramd['SGfilter_order']==0 or smooth_paramd['SGfilter_nptsoneside']<3:
            return sweep_currents,sim_basis_v,np.hstack(sweep_currents),np.array(segment_index_arr)
        smooth_sweep_currents=[signal.savgol_filter(arr, 2*smooth_paramd['SGfilter_nptsoneside']+1, smooth_paramd['SGfilter_order']) for arr in sweep_currents]
        echem_i_smooth=np.hstack(smooth_sweep_currents)
        echem_i_smooth[:int(smooth_paramd['SGfilter_nptsoneside']*1.5)]=echem_i[:int(smooth_paramd['SGfilter_nptsoneside']*1.5)]#replace first 0.75 window with raw data due to initial transient
        return sweep_currents,sim_basis_v,echem_i_smooth,np.array(segment_index_arr)
    else:
        print 'technique not supperted for ecms analysis'


###these lines for seeding line by line execution of perform
if 0:#in spyder open new concolse, run __file__ and then up to and include MainMenu definition in CalcFomApp. then run __file__= and code up to here, then run rest of thiss sectino, then run specific load to prepare running perform line by line
    mainapp=QApplication(sys.argv)
    form=MainMenu(None, execute=False, modifyanainplace=False,guimode=False)
    calcFOMDialogclass=form.calcui

if 0:
    calcFOMDialogclass.importexp(exppath=r'L:\processes\experiment\temp\20190403.132935.done\20190403.132935.exp')
    cb=calcFOMDialogclass.AnalysisNamesComboBox
    selind=[i for i in range(int(cb.count())) if str(cb.itemText(i)).startswith('Analysis__ECMS_Time_Join')]
    cb.setCurrentIndex(selind[0])
    calcFOMDialogclass.analysisclass.params['eche_techniques']='CV3,CV6,CV9'
    calcFOMDialogclass.processeditedparams()
    calcFOMDialogclass.getactiveanalysisclass()
    destfolder, expdatfolder, writeinterdat, anak, zipclass, anauserfomd, expfiledict=calcFOMDialogclass.tempanafolder, calcFOMDialogclass.expfolder, True, 'ana__99', calcFOMDialogclass.expzipclass, {}, calcFOMDialogclass.expfiledict
    self=calcFOMDialogclass.analysisclass
elif 0:
    calcFOMDialogclass.clearanalysis()
    calcFOMDialogclass.importana(p=r'L:\processes\analysis\temp\20190403.135546.run\20190403.135546.ana')
    for i in range(1, int(calcFOMDialogclass.FOMProcessNamesComboBox.count())):
        if (str(calcFOMDialogclass.FOMProcessNamesComboBox.itemText(i)).partition('(')[0])=='Analysis__ECMS_Fit_MS':
            break
    calcFOMDialogclass.FOMProcessNamesComboBox.setCurrentIndex(i)
    calcFOMDialogclass.getactiveanalysisclass()
    calcFOMDialogclass.analysisclass.params['eche_techniques']='CV3'
    calcFOMDialogclass.analysisclass.params['loss_fcn']='L2_3x_first_half_5x_positive'
    calcFOMDialogclass.processeditedparams()

    destfolder, expdatfolder, writeinterdat, anak, zipclass, anauserfomd, expfiledict=calcFOMDialogclass.tempanafolder, calcFOMDialogclass.expfolder, True, 'ana__99', calcFOMDialogclass.expzipclass, {}, calcFOMDialogclass.expfiledict
    self=calcFOMDialogclass.analysisclass


class Analysis__ECMS_Time_Join(Analysis_Master_inter):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={'eche_techniques':'CV3,CV6,CV9','masses':'2,15,26','mass_spec_lag_time_s':5.,'post_eche_time_for_MS_settle_s':60.}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__ECMS_Time_Join'

        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=['reference_vrhe']

        self.fomnames=['num_MS_masses']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='Ewe(Vrhe)'

        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name='num_masses', colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')


    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None, calcFOMDialogclass=None):

        self.processnewparams(calcFOMDialogclass=calcFOMDialogclass)
        return self.filedlist

    def processnewparams(self, calcFOMDialogclass=None):
        expfiledict=calcFOMDialogclass.expfiledict
        try:
            self.eche_techniques=self.params['eche_techniques'].split(',')#ultimatley get this from CV* in params
            self.masses=self.params['masses'].split(',')
        except:
            self.filedlist=[]
        self.num_files_considered, self.filedlist_ms=getapplicablefilenames_byuse_tech_type(expfiledict,'data','HidenMID','hiden_single_mass_files')
        self.filedlist=[d for tech in self.eche_techniques for d in getapplicablefilenames_byuse_tech_type(expfiledict,'data',tech,'pstat_files',requiredparams=self.requiredparams)[1]]
        self.description='%s on %s' %(','.join(self.fomnames), ','.join(self.eche_techniques))

    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):
        if destfolder is None:
            return

        self.initfiledicts(runfilekeys=['inter_rawlen_files','inter_files'])
        self.fomnames=[self.fomnames[0]]
        self.fomnames+=['eche_technique','fn_eche']#not supposed to put the string foms here but usine writefombare so it's ok
        self.fomnames+=['fn_mass__%s' %mass for mass in self.masses]#here fns are per sample,plate,technique
        for filed in self.filedlist_ms:
            mass=filed['fn'].rpartition('__')[2].partition('.')[0]
            if not mass in self.masses:
                continue
            p=os.path.join(expfiledict[filed['run']]['run_path'],filed['fn'])
            filed['mass']=mass
            filed['start_time'],filed['ms_time_ms'],filed['ms_torr']=read_hiden_csv(p)
            filed['start_time']=time.mktime(filed['start_time'])
            filed['end_time']=filed['start_time']+filed['ms_time_ms'][-1]/1000.
            filed['epoch(s)']=filed['ms_time_ms']/1000.+filed['start_time']-self.params['mass_spec_lag_time_s']
        self.filedlist_ms=[fd for fd in self.filedlist_ms if 'epoch(s)' in fd.keys()]#remove the ones not matching masses
        self.fomdlist=[]
        for filed in self.filedlist:
            if numpy.isnan(filed['sample_no']):
                if self.debugmode:
                    raiseTEMP
                continue
            fomd=dict([(k, '') for k in self.fomnames[1:]])#fill empty string for all file paths and tech so that if not found it still exists
            fn=filed['fn']
            p=os.path.join(expfiledict[filed['run']]['run_path'],fn)
            if fn.endswith('.DTA'):
                dtemp=read_dta_pstat_file(p, searchstr='CURVE')
                datadict=mock_eche_dict_from_dta_dict(dtemp)
                filed['start_time']=time.mktime(get_time_struct_dta(p))
                filed['end_time']=filed['start_time']+datadict['t(s)'][-1]
            else:
                datadict=readechemtxt(p, interpretheaderbool=True)
                filed['end_time']=datadict['Epoch']-2082844800.# 2082844800 is the s between the LV and python epochs and the labview eposh is at file save so subtract the duration of the measurement to get start time
                filed['start_time']=filed['end_time']-datadict['t(s)'][-1]
                for k in datadict.keys():
                    if not k in ['t(s)','Ewe(V)','I(A)']:
                        del datadict[k]

            datadict['t(s)']=np.float64(datadict['t(s)'])
            datadict['Ewe(Vrhe)']=datadict['Ewe(V)']-filed['reference_vrhe']
            datadict['epoch(s)']=datadict['t(s)']+filed['start_time']

            fnr = '%s__%s_rawlen.txt' % (anak, os.path.splitext(fn)[0])
            rp = os.path.join(destfolder, fnr)
            kl = saveinterdata(rp, datadict, savetxt=True)
            self.runfiledict[filed['run']]['inter_rawlen_files'][
                        fnr] = '%s;%s;%d;%d;%d' % (
                            'eche_inter_rawlen_file', ','.join(kl), 1,
                            len(datadict[kl[0]]), filed['sample_no'])
            fomd['fn_eche']=fnr
            fomd['eche_technique']=filed['techk']

            num_ms_found=0
            for msfiled in self.filedlist_ms:
                if msfiled['start_time']<=filed['start_time'] and msfiled['end_time']>=filed['end_time']:
                    num_ms_found+=1
                    msinds=np.where((msfiled['epoch(s)']>=filed['start_time']) & (msfiled['epoch(s)']<=(filed['end_time']+self.params['post_eche_time_for_MS_settle_s'])))[0]
                    inds=[-1 if ms_epoch>datadict['epoch(s)'][-1] else np.argmin((datadict['epoch(s)']-ms_epoch)**2) for ms_epoch in msfiled['epoch(s)'][msinds]]
                    interlend={}
                    interlend['rawselectinds']=inds
                    interlend['ms_adjusted_epoch(s)_mass__%s' %msfiled['mass']]=msfiled['epoch(s)'][msinds]
                    interlend['MS(torr)_mass__%s' %msfiled['mass']]=msfiled['ms_torr'][msinds]
                    indsarr=np.array(inds)
                    for k in datadict.keys():
                        if 't(s)' in k:
                            continue
                        interlend[k+'_MS']=datadict[k][inds]
                        if 'Ewe' in k:#for MS beyond the end of eche time, assume open circuit, NaN=unknown potential and 0 current
                            interlend[k+'_MS'][indsarr==-1]=np.nan
                        elif 'I' in k:
                            interlend[k+'_MS'][indsarr==-1]=0.
                    #the t(s)_MS is still on the echem time scale but use the MS time values (not the closest ones) and let the time extend beyond the end of the echem
                    interlend['t(s)_MS']=msfiled['epoch(s)'][msinds]-datadict['epoch(s)'][0]

                    fni = '%s__mass__%s_%s_interlen.txt' % (anak, msfiled['mass'], os.path.splitext(fn)[0])
                    p = os.path.join(destfolder, fni)
                    fmtd=dict([(k,'%.2f' if 'epoch' in k else ('%d' if k=='rawselectinds' else '%.4e')) for k in interlend.keys()])
                    kl = saveinterdata(p, interlend, savetxt=True,fmt=fmtd)
                    self.runfiledict[filed['run']]['inter_files'][
                        fni] = '%s;%s;%d;%d;%d' % (
                            'ecms_interlen_file', ','.join(kl), 1,
                            len(interlend[kl[0]]), filed['sample_no'])
                    fomd['fn_mass__%s' %msfiled['mass']]=fni
            if num_ms_found==0:
                print 'DID NOT FIND MS DATA FOR ',fn
            fomd[self.fomnames[0]]=num_ms_found

            self.fomdlist+=[dict(fomd, sample_no=filed['sample_no'], plate_id=filed['plate_id'], runint=int(filed['run'].partition('run__')[2]))]
        ffn='%s__%s.csv' %(anak,'-'.join(self.fomnames[:3]))#name file by foms but onyl inlcude the 1st 3 to avoid long names
        self.multirunfiledict['fom_files'][ffn]=\
        self.writefom_bare(destfolder, ffn, floatkeys=[], intfomkeys=['runint','plate_id', self.fomnames[0]], strkeys=self.fomnames[1:])

class Analysis__ECMS_Calibration(Analysis_Master_nointer):
    def __init__(self):
        self.analysis_fcn_version='1'
        self.dfltparams={'masses':'2,15,26','baseline_times_to_ave_wrt_valve_open_s':'300.,600.','frac_cal_duration_to_use':'0.5,0.95',\
            'instrument_QE_masses':'3.8,1.6,0.75','modelling_basis__mM_torr':'3.96e+07,1.01e+08,2.57e+08'\
            }#assumes masses matches species and each species is 100% of the mass signal, need more complicated params otherwise, in particualr would need different QE for each species contributing to each mass signal
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__ECMS_Calibration'

        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=['params_calibration__1']

        self.fomnames=['num_MS_masses']

        self.plotparams={}

        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name='num_masses', colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')

    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None, calcFOMDialogclass=None):
        self.num_files_considered, self.filedlist=getapplicablefilenames_byuse_tech_type(expfiledict,'data','HidenMID','hiden_single_mass_files', requiredparams=self.requiredparams)

        self.description='ECMS calibration - no samples'
        return self.filedlist


    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):
        if destfolder is None:
            return
        self.initfiledicts(runfilekeys=[])

        base_r0,base_r1=[float(s.strip()) for s in self.params['baseline_times_to_ave_wrt_valve_open_s'].split(',')]
        cal_frac0,cal_frac1=[float(s.strip()) for s in self.params['frac_cal_duration_to_use'].split(',')]
        masses=self.params['masses'].split(',')

        misccsvdlist=[]
        for filed in self.filedlist:
            mass=filed['fn'].rpartition('__')[2].partition('.')[0]
            if not mass in masses:
                continue
            p=os.path.join(expfiledict[filed['run']]['run_path'],filed['fn'])
            filed['mass']=mass
            filed['start_time'],filed['ms_time_ms'],filed['ms_torr']=read_hiden_csv(p)
            cald=filed['params_calibration__1']
            concentration_mM=[float(s.strip()) for s in cald['concentration_mM'].split(',')][masses.index(mass)]
            QE=[float(s.strip()) for s in self.params['instrument_QE_masses'].split(',')][masses.index(mass)]
            ref_cal_factor=[float(s.strip()) for s in self.params['modelling_basis__mM_torr'].split(',')][masses.index(mass)]
            species=[s.strip() for s in cald['species'].split(',')][masses.index(mass)]
            base_t0=base_r0*1000.+cald['time_open_pervaporator_valve_ms']
            base_t1=base_r1*1000.+cald['time_open_pervaporator_valve_ms']
            cal_t0=cald['time_switch_to_calibration_ms']+1000.*cald['duration_s']*cal_frac0
            cal_t1=cald['time_switch_to_calibration_ms']+1000.*cald['duration_s']*cal_frac1
            base_inds=np.where((filed['ms_time_ms']>=base_t0) & (filed['ms_time_ms']<=base_t1))
            cal_inds=np.where((filed['ms_time_ms']>=cal_t0) & (filed['ms_time_ms']<=cal_t1))
            base_torr=filed['ms_torr'][base_inds].mean()
            cal_torr=filed['ms_torr'][cal_inds].mean()
            cal_factor=concentration_mM/cal_torr
            misccsvdict={}
            misccsvdict['species']=species
            misccsvdict['mass']=mass
            misccsvdict['baseline.torr']=base_torr
            misccsvdict['cal_signal.torr']=cal_torr
            misccsvdict['cal_slope.mM_torr']=cal_factor
            misccsvdict['instrument_QE']=QE
            misccsvdict['QE_wrt_modelling_basis']=ref_cal_factor/cal_factor
            misccsvdlist+=[misccsvdict]

        csvfn='%s__ecms_calibration.csv' %anak

        filedesc,filestr=createcsvfilstr_bare(misccsvdlist,None,strfomkeys=['species','mass'],return_file_desc=True)
        cal_p=os.path.join(destfolder, csvfn)
        with open(cal_p,mode='w') as f:
            f.write(filestr)
        self.multirunfiledict['misc_files']={}
        self.multirunfiledict['misc_files'][csvfn]=filedesc

        self.fomdlist=[]
        self.primarycsvpath=''
    def check_output(self):
        return True, 'nothing checked - only misc output'



##TEMP
#anak='ana__3'
#destfolder=r'K:\experiments\anec\2019 ECMS\rcp\demo_181102 CuZn library_43962\tempana'
#exppath=r'L:\processes\experiment\temp\20190322.114442.done'
#expfiledict=readexpasdict(buildexppath(exppath))
#
#
#anapath=r'L:\processes\analysis\temp\20190326.122440.done'
#anafiledict=readana(buildanapath(anapath),stringvalues=True)
#destfolderTEMP=anapath
#self=Analysis__ECMS_Fit_MS()#TEMP
#self.getapplicablefilenames(expfiledict,'','','',anadict=anafiledict)#TEMP
#
#loss_fcn=loss_fcn_dict[self.params['loss_fcn']]
#species=[s.strip() for s in self.params['species'].split(',')]
#sim_lib_dict=read_ecms_simulation_data(self.params['ms_simulation_model'],species)

#if self.cal_filed is None or self.data_filed_dict is None:
#    return
#
#cal_p=os.path.join(destfolderTEMP,self.cal_filed['fn'])
#calfomd=readcsvdict(cal_p, self.cal_filed, returnheaderdict=False,includestrvals=True)
#
#
#
##TEMP
##self.runfiledict={}
##self.runfiledict['run__1']={}
##self.runfiledict['run__1']['inter_rawlen_files']={}
##self.runfiledict['run__1']['inter_files']={}
#anauserfomd={}


class Analysis__ECMS_Fit_MS(Analysis_Master_FOM_Process):
    def __init__(self):
        self.analysis_fcn_version='2'
        self.dfltparams={'ms_simulation_model':'1G_v2','species':'H2,CH4,C2H4','eche_techniques':'CV9','max_per_species_FE':1.1,'loss_fcn':'L2_3x_first_half_5x_positive','select_ana':'ana__1','cal_ana':'ana__2','voltage_error_V':0.01,'num_voltage_errors_to_abort':30, 'SGfilter_nptsoneside':64,'SGfilter_order':3,'ignore_FE_time_start_end_s':8.,'resistance_to_compensate_Ohm':60.,'max_current_valid_FE':-0.00003,'min_max_each_fit_param':'0.1,1.6;-1.4,-0.4'}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__ECMS_Fit_MS'
        self.requiredkeys=[]
        self.optionalkeys=[]
        self.requiredparams=[]
        self.fomnames=['max.FETotal']
        self.plotparams=dict({}, plot__1={})
        self.plotparams['plot__1']['x_axis']='t(s)'
        self.plotparams['plot__1']['series__1']='FE_Total'

        self.csvheaderdict=dict({}, csv_version='1', plot_parameters={})
        self.csvheaderdict['plot_parameters']['plot__1']=dict({}, fom_name='max.FETotal', colormap='jet', colormap_over_color='(0.5,0.,0.)', colormap_under_color='(0.,0.,0.)')


    def getapplicablefomfiles(self, anadict):#called by getapplicablefilenames
        if not anadict is None and self.params['select_ana'] in anadict.keys():
            self.num_ana_considered, self.filedlist=stdgetapplicablefomfiles(anadict, params={'select_ana':self.params['select_ana'],'select_fom_keys':'num_MS_masses'})

    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None, calcFOMDialogclass=None):#just a wrapper around getapplicablefomfiles to keep same argument format as other AnalysisClasses
        self.getapplicablefomfiles(anadict)
        self.processnewparams(calcFOMDialogclass=calcFOMDialogclass,anadict=anadict)
        '''
        the 'process_fom' types of analysis must call processnewparams during getapplicable filenames because usually the ana__k needs
        to be updated in getapplicablefilenames before prcoessing new params and if there is an error therin the fieldlist will be set to [] so
        getapplicablefilenames does not need to be run again
        '''
        return self.filedlist

    def processnewparams(self, calcFOMDialogclass=None,anadict=None): #called after getapplicablefomfiles in getapplicablefilenames
        self.description=''
        if anadict is None:
            if calcFOMDialogclass is None:
                self.filedlist=[]
                return
            anadict=calcFOMDialogclass.anadict
        if not self.params['cal_ana'] in anadict.keys():
            self.filedlist=[]
            return

        try:
            fn,keystr=anadict[self.params['cal_ana']]['files_multi_run']['misc_files'].items()[0]
            self.cal_filed=createfileattrdict(keystr, fn=fn)
            self.cal_filed['fn']=fn
        except:
            self.cal_filed=None
            self.filedlist=[]
            return

        try:
            self.data_filed_dict={}
            for k,v in anadict[self.params['select_ana']].iteritems():
                if not k.startswith('files_'):
                    continue
                for k2,v2 in v.iteritems():
                    for fn,keystr in v2.iteritems():
                        self.data_filed_dict[fn]=createfileattrdict(keystr, fn=fn)
        except:
            self.data_filed_dict=None
            self.filedlist=[]
            return

        try:
            strlist=self.params['min_max_each_fit_param'].split(';')
            self.minmax_fitpars=[eval(s) for s in strlist]
        except:
            self.data_filed_dict=None
            self.filedlist=[]
            return
        self.description='Fit ECMS from %s calibrated by %s to the %s models' %(self.params['select_ana'], self.params['cal_ana'],self.params['ms_simulation_model'])
    def perform(self, destfolder, expdatfolder=None, writeinterdat=True, anak='', zipclass=None, anauserfomd={}, expfiledict=None):
        '''
        fom_csv are 1 file per technique
            within each fom_csv there is per sample,plate
                max.FETotal that is the sum over species and max over time
            eche_technique
                fn_bestfit_eche
                fn_bestfit_species__<sp>
                fn_fitsummary_species__<sp>
                <sp>_bestfit.fitloss
                <sp>_bestfit.<param>
                <sp>.maxFE
                <sp>.charge.C
                <sp>.Ip1.A

        misc_files includes a fit_summary per technique per sample,plate per species and includes fits of all model parameter sets and is saved as fn_fitsummary_species__<sp>
        The best fit from the fit_summary is exported in fawlen and interlen files


        inter_rawlen files are per tehcnique, per sample,plate and fn saved as fn_bestfit_eche
            length is that of the echem data and inlcudes
            Ip(A)__<sp>
            FE__<sp>
            Ip(A)_Total
            FE_Total
            Soltn_conc(mM)__<sp>
            Ismooth(A)
            Fit_MS(torr)__<sp>

        iterlen files are per technique per sample,plate per species and saved as fn_bestfit_species__<sp>
            length is that of the MS data and includes
            Ip(A)
            Soltn_conc(mM)
            Adjusted_MS(torr)
            Fit_MS(torr)
            rawselectinds
            Loss_contribution
        '''
        if destfolder is None:
            return

        if self.cal_filed is None or self.data_filed_dict is None:
            return

        loss_fcn=loss_fcn_dict[self.params['loss_fcn']]
        species=[s.strip() for s in self.params['species'].split(',')]
        sim_lib_dict=read_ecms_simulation_data(self.params['ms_simulation_model'],species)

        #this check function looks for True when par out of range, but only checks if minmax provided correctly, so defaults to allow pars
        check_pars_out_of_range=lambda pars: True in [(v<minmax[0] or v>minmax[1]) for minmax,v in zip(self.minmax_fitpars,pars) if isinstance(minmax,tuple) and len(minmax)==2]
        allow_fit_par_inds=[ind for ind,model_pars in enumerate(sim_lib_dict['model_params']) if not check_pars_out_of_range(model_pars)]

        cal_p=os.path.join(destfolder,self.cal_filed['fn'])
        calfomd=readcsvdict(cal_p, self.cal_filed, returnheaderdict=False,includestrvals=True)

        filed=self.filedlist[0]
                    #self.strkeys_fomdlist=[]

        fn=filed['fn']
        fig=plt.Figure()#figsize not working? figsize=(30,7))

        canvas=FigureCanvas(fig)


        datafomd=readcsvdict(os.path.join(destfolder, fn), filed, returnheaderdict=False, zipclass=None, includestrvals=True)
        runintset=sorted(list(set(datafomd['runint'])))

        runklist=['run__%d' %ri for ri in runintset]
        self.initfiledicts(runfilekeys=['inter_rawlen_files','inter_files'],runklist=runklist)
        self.multirunfiledict['misc_files']={}



        tech_list=list(datafomd['eche_technique'])
        tech_set=sorted(list(set(tech_list)))

        summ_plot_fom_keys=['Echem.charge.C']+['%s.charge.C' %sp for sp in species]+['Other.charge.C']

        techd_fomdlist={}
        for techcount,tech in enumerate(tech_set):#per technique
            if not tech in self.params['eche_techniques']:#direct search in param string
                continue
            self.fomnames=['max.FETotal']#reset every technique in case keys are different
            self.strkeys_fomdlist=['eche_technique','fn_bestfit_eche']
            techd_fomdlist[tech]=[]

            pid_sid_datafomind__this_tech=sorted([(pid,sid,count) for count,(pid,sid,te) in enumerate(zip(datafomd['plate_id'],datafomd['sample_no'],tech_list)) if te==tech])
            datafominds=[tup[2] for tup in pid_sid_datafomind__this_tech]

            tech_summary_plot_data=dict([('FE__%s' %sp,[[] for i in range(len(datafominds))]) for sp in species],fomlistd=dict([(fomk,[]) for fomk in summ_plot_fom_keys]))
            #each FE__ is a list by sample and then a list by CV segment and then a x,y tuple

            for smpcount, datafomind in enumerate(datafominds):# per sample,plate

                fig.clf()
                fomd={}
                rawlend={}


                for k in list(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING)+['eche_technique']:
                    fomd[k]=datafomd[k][datafomind]


                fn_eche=datafomd['fn_eche'][datafomind]
                fnlabel='__'.join(fn_eche.split('__')[2:]).rpartition('_rawlen')[0]
                fnr = '%s__%s_rawlen.txt' % (anak, fnlabel)
                fomd['fn_bestfit_eche']=fnr
                fnrm0 = '%s__%s_rawlen.png' % (anak, fnlabel)
                fnrm1 = '%s__%s_rawlen.svg' % (anak, fnlabel)

                p=os.path.join(destfolder,fn_eche)
                fd=self.data_filed_dict[fn_eche]
                inds=[fd['keys'].index(k) for k in 't(s),Ewe(Vrhe),I(A)'.split(',')]
                echem_t,echem_v,echem_i=getarrs_filed(p,fd,selcolinds=inds)

                sweep_currents,sim_basis_v,echem_i_smooth,segment_index_arr=eche_split_current_by_sweep_and_generate_intended_voltage(tech,sim_lib_dict,echem_t,echem_i,smooth_paramd=self.params)
                vdiff=echem_v-sim_basis_v
                if np.isnan(sim_basis_v).sum()>0 or (np.abs(vdiff)>self.params['voltage_error_V']).sum()>self.params['num_voltage_errors_to_abort']:#echem_t contains points beyond the profile time
                    print 'measured voltages do not match the echem_profile. Aborting'
                    continue
                echem_fe_test_inds=(echem_t>self.params['ignore_FE_time_start_end_s']) & ((echem_t[-1]-echem_t)>self.params['ignore_FE_time_start_end_s']) & (echem_i_smooth<self.params['max_current_valid_FE'])

                rawlend['segment_index']=segment_index_arr
                rawlend['Ismooth(A)']=echem_i_smooth
                rawlend['EweSimulated(Vrhe)']=sim_basis_v
                rawlend['Ewe.Error(V)']=vdiff
                rawlend['valid_FE_bool']=np.int32(echem_fe_test_inds)
                rawlend['Ewe(compensatedVrhe)']=sim_basis_v-echem_i_smooth*self.params['resistance_to_compensate_Ohm']

                for spcount,sp in enumerate(species):
                    fni = '%s__species__%s_%s_interlen.txt' % (anak, sp, fnlabel)
                    ki='fn_bestfit_species__%s' %sp
                    fnm = '%s__species__%s_%s_fitsummary.pck' % (anak, sp, fnlabel)
                    fnim0 = '%s__species__%s_%s_fitsummary.png' % (anak, sp, fnlabel)
                    fnim1 = '%s__species__%s_%s_fitsummary.svg' % (anak, sp, fnlabel)
                    km='fn_fitsummary_species__%s' %sp
                    for k,v in [(ki,fni),(km,fnm)]:
                        if not k in self.strkeys_fomdlist:
                            #self.fomnames+=[k]
                            self.strkeys_fomdlist+=[k]
                        fomd[k]=v


                    calind=list(calfomd['species']).index(sp)
                    cald={}
                    for k,v in calfomd.iteritems():
                        cald[k]=v[calind]

                    msfn=datafomd['fn_mass__%d' %cald['mass']][datafomind]
                    p=os.path.join(destfolder,msfn)
                    fd=self.data_filed_dict[msfn]
                    inds=[fd['keys'].index(k) for k in ('t(s)_MS,rawselectinds,MS(torr)_mass__%d'%cald['mass']).split(',')]
                    ms_t,rsinds,ms_torr=getarrs_filed(p,fd,selcolinds=inds)

                    ms_sig=ms_torr[:]
                    ms_sig-=cald['baseline.torr']
                    ms_sig/=cald['QE_wrt_modelling_basis']


                    inds=[np.argmin((t-echem_t)**2) for t in ms_t]
                    echem_i_smooth_at_ms_times=echem_i_smooth[inds]
                    echem_i_smooth_at_ms_times[ms_t>echem_t[-1]]=np.nan


                    def get_sim_arrs_paramind_timewerteche(paramind,timewrteche):
                        mod_t=sim_lib_dict[sp]['time(s)'][paramind]
                        inds=[np.argmin((t-mod_t)**2) for t in timewrteche]
                        mod_t=mod_t[inds]
                        mod_c,mod_ip,mod_out=[sim_lib_dict[sp][k][paramind][inds] for k in ['conc_in_soltn(M)','Ip(A)','output(torr)']]
                        mod_out*=cald['instrument_QE']
                        return mod_t,mod_c,mod_ip,mod_out

                    interlend={}
                    fitsummarydlist=[]
                    l_fitloss=[]
                    interlend['rawselectinds']=rsinds
                    interlend['Adjusted_MS(torr)__%s' %sp]=ms_sig

                    for model_pars_ind in allow_fit_par_inds:
                        model_pars=sim_lib_dict['model_params'][model_pars_ind]
                        mod_t,mod_c,mod_ip,mod_out=get_sim_arrs_paramind_timewerteche(model_pars_ind,ms_t)
                        emod_t,emod_c,emod_ip,emod_out=get_sim_arrs_paramind_timewerteche(model_pars_ind,echem_t)

                        max_fe_i1_is_1=max((-emod_ip/echem_i_smooth)[echem_fe_test_inds])
                        Ip_1_max=self.params['max_per_species_FE']/max_fe_i1_is_1

                        resid_fcn=lambda Ip_1: loss_fcn(Ip_1*mod_out - ms_sig)
                        res = minimize_scalar(lambda x:np.sum(resid_fcn(x)))
                        Ip_1 = res.x
                        Ip_1=0. if Ip_1<0. else (Ip_1_max if Ip_1>Ip_1_max else Ip_1)

                        fitsummaryd={}
                        fitsummaryd['model_params']=model_pars
                        fitsummaryd['Loss_contribution']=resid_fcn(Ip_1)
                        fitsummaryd['Residual']=Ip_1*mod_out - ms_sig
                        fitsummaryd['Fit_MS(torr)']=Ip_1*mod_out
                        fitsummaryd['Adjusted_MS(torr)']=ms_sig
                        fitsummaryd['Ip(A)']=Ip_1*mod_ip
                        fitsummaryd['FE']=-Ip_1*mod_ip/echem_i_smooth_at_ms_times
                        fitsummaryd['Soltn_conc(mM)']=Ip_1*mod_c
                        fitsummaryd['Ip_1']=Ip_1
                        fitsummaryd['Ip_1_max']=Ip_1_max
                        fitsummaryd['t(s)_MS_model']=mod_t
                        fitloss=fitsummaryd['Loss_contribution'].sum()
                        l_fitloss+=[fitloss]
                        fitsummaryd['fitloss']=fitloss

                        fitsummarydlist+=[fitsummaryd]
                    bestfitind=np.argmin(l_fitloss)
                    for k in ['Ip(A)','Soltn_conc(mM)','Adjusted_MS(torr)','Fit_MS(torr)','Loss_contribution']:
                        interlend['%s__%s' %(k,sp)]=fitsummarydlist[bestfitind][k]
                    Ip_1_bestfit=fitsummarydlist[bestfitind]['Ip_1']


                    mod_t,mod_c,mod_ip,mod_out=get_sim_arrs_paramind_timewerteche(allow_fit_par_inds[bestfitind],echem_t)

                    rawlend['Ip(A)__%s' %sp]=-Ip_1_bestfit*mod_ip
                    rawlend['Soltn_conc(mM)__%s' %sp]=Ip_1_bestfit*mod_c
                    rawlend['Fit_MS(torr)__%s' %sp]=Ip_1_bestfit*mod_out
                    rawlend['FE__%s' %sp]=-Ip_1_bestfit*mod_ip/echem_i_smooth

                    fomd['%s_bestfit.fitloss' %sp]=fitsummarydlist[bestfitind]['fitloss']
                    fomd['%s.maxFE' %sp]=max(rawlend['FE__%s' %sp][echem_fe_test_inds])
                    fomd['%s.charge.C' %sp]=(rawlend['Ip(A)__%s' %sp][:-1]*(echem_t[1:]-echem_t[:-1])).sum()

                    fomd['%s.Ip1.A' %sp]=Ip_1_bestfit
                    for parname,v in zip(sim_lib_dict['metadata']['parameter_names'],sim_lib_dict['model_params'][allow_fit_par_inds[bestfitind]]):
                        fomd['%s_bestfit.%s' %(sp,parname)]=v

                    #########start plotting section
                    plt.clf()
                    ax1=plt.subplot(1,2, 1)
                    ax2=plt.subplot(1,2,2)

                    plt.subplots_adjust(left=.08, bottom=.08, right=.96, top=.94, wspace=0.43)
                    ax=ax2
                    ax.cla()
                    plt.sca(ax)
                    partups=[tuple(arr) for arr in sim_lib_dict['model_params'][allow_fit_par_inds,:2]]
                    partups_set=sorted(list(set(partups)))
                    plotdata=[]
                    repvals=[np.min([v for v,t in zip(l_fitloss,partups) if t==pt]) for pt in partups_set]
                    xv,yv=np.array(partups_set).T
                    sm=ax.scatter(xv,yv,c=repvals,vmin=min(repvals),vmax=max(repvals),cmap='jet_r',linewidths=0.)
                    cb=plt.colorbar(sm)
                    cb.set_label('loss per param set')
                    ax.set_xlabel(sim_lib_dict['metadata']['parameter_names'][0])
                    ax.set_ylabel(sim_lib_dict['metadata']['parameter_names'][1])

                    ax=ax1
                    ax.cla()
                    plt.sca(ax)
                    for fitdcount,fitd in enumerate(fitsummarydlist):
                        st={'lw':1.5,'c':'r'} if fitdcount==bestfitind else {'lw':0.7,'c':'grey'}
                        ax.plot(fitd['t(s)_MS_model'],fitd['Fit_MS(torr)'],'-',**st)
                    ax.plot(fitd['t(s)_MS_model'],fitd['Adjusted_MS(torr)'],'ko',ms=6)#just use the last fitd since these arrays the same for every fitd
                    ax.set_ylabel('Adj. MS(torr) %s' %sp)
                    ax.set_xlabel('echem time (s)')
                    axt=ax.twinx()
                    axt.plot(echem_t,rawlend['FE__%s' %sp],'b-')
                    axt.set_ylabel('FE__%s' %sp)


                    #########finish plotting section


                    p=os.path.join(destfolder, fnim0)
                    self.multirunfiledict['misc_files'][fnim0]='ecms_fitsummary_png_file;'
                    plt.savefig(p, dpi=300)
                    p=os.path.join(destfolder, fnim1)
                    self.multirunfiledict['misc_files'][fnim1]='ecms_fitsummary_svg_file;'
                    plt.savefig(p)
                    #plt.show()
                    p = os.path.join(destfolder, fni)
                    fmtd=dict([(k,'%d' if k=='rawselectinds' else '%.4e') for k in interlend.keys()])
                    kl = saveinterdata(p, interlend, savetxt=True,fmt=fmtd)
                    self.runfiledict['run__%d' %fomd['runint']]['inter_files'][
                            fni] = '%s;%s;%d;%d;%d' % (
                                'ecms_interlen_file', ','.join(kl), 1,
                                len(interlend[kl[0]]), fomd['sample_no'])
                    p=os.path.join(destfolder, fnm)
                    with open(p,mode='wb') as f:
                        pickle.dump(fitsummarydlist,f)

                    self.multirunfiledict['misc_files'][fnm]='ecms_fitsummary_pck_file;'

                for s in ['Ip(A)','FE']:
                    rawlend['%s_Total' %s]=np.array([rawlend[k] for k in rawlend.keys() if k.startswith(s)]).sum(axis=0)

                fomd['max.FETotal']=np.max(rawlend['FE_Total'])
                totcharge_species=np.sum([fomd['%s.charge.C' %sp] for sp in species])
                fomd['Echem.charge.C']=(echem_i_smooth[:-1]*(echem_t[1:]-echem_t[:-1])).sum()
                fomd['Other.charge.C']=fomd['Echem.charge.C']-totcharge_species

                ###start plot section
                cols=['b', 'g','r', 'c', 'm', 'y']
                plt.clf()
                ax1=plt.subplot(1,3, 1)
                ax2=plt.subplot(1,3,2)
                ax3=plt.subplot(1,3,3)
                plt.subplots_adjust(left=.11, bottom=.08, right=.96, top=.94, wspace=0.28)
                for ax, s, st, loc in [(ax1, 'Ip(A)__', 'Ismooth(A)', 4), (ax2, 'FE__', 'FE_Total', 1)]:
                    ax.cla()
                    plt.sca(ax)
                    for i, sp in enumerate(species):
                        c=cols[i%len(cols)]
                        ax.plot(echem_t, rawlend[s+sp], c+'-', label=sp)
                    ax.plot(echem_t, rawlend[st], 'k-', label=st)
                    if st=='Ismooth(A)':
                        ax.plot(echem_t, echem_i, 'k:', label='I(A)')
                    ax.set_xlabel('echem time (s)')
                    ax.set_ylabel(s)
                    plt.legend(loc=loc, fontsize='small', frameon=False)

                ax=ax3
                ax.cla()
                plt.sca(ax)

                for segi in range(max(segment_index_arr)+1):
                    ls='--' if (segi%2)==1 else '-'
                    inds=np.where(segment_index_arr==segi)[0]
                    ax.plot(echem_v[inds],echem_i[inds],'b'+ls)
                    ax.plot(rawlend['Ewe(compensatedVrhe)'][inds],echem_i_smooth[inds],'k'+ls)
                    axr=ax.twinx()
                    axr.plot(echem_v,rawlend['Ewe.Error(V)'],'r'+ls)

                    for sp in species:
                        k='FE__%s' %sp
                        tech_summary_plot_data[k][smpcount]+=[(rawlend['Ewe(compensatedVrhe)'][inds],rawlend[k][inds])]
                for fomk in summ_plot_fom_keys:
                    tech_summary_plot_data['fomlistd'][fomk]+=[fomd[fomk] if fomk in fomd.keys() else np.nan]


                    #tech_summary_plot_data=[]
                plt.plot([],[],'b-',label='raw I(V)')
                plt.plot([],[],'k-',label='smooth I(compV)')
                plt.plot([],[],'r-',label='Verror(V)')
                plt.legend(loc=loc, fontsize='small', frameon=False)

                ###finish plot section
                p=os.path.join(destfolder, fnrm0)
                self.multirunfiledict['misc_files'][fnrm0]='ecms_png_file;'
                plt.savefig(p, dpi=300)
                p=os.path.join(destfolder, fnrm1)
                self.multirunfiledict['misc_files'][fnrm1]='ecms_svg_file;'
                plt.savefig(p)

                rp = os.path.join(destfolder, fnr)
                kl = saveinterdata(rp, rawlend, savetxt=True)
                self.runfiledict['run__%d' %fomd['runint']]['inter_rawlen_files'][
                            fnr] = '%s;%s;%d;%d;%d' % (
                                'eche_inter_rawlen_file', ','.join(kl), 1,
                                len(rawlend[kl[0]]), fomd['sample_no'])

                techd_fomdlist[tech]+=[fomd]

                for k in fomd.keys():
                    if not k in self.fomnames+self.strkeys_fomdlist+list(FOMKEYSREQUIREDBUTNEVERUSEDINPROCESSING):
                       self.fomnames+=[k]

            #start summary plot
            fig.clf()
            max_samples_to_plot=15
            smps=[tup[1] for tup in pid_sid_datafomind__this_tech][:max_samples_to_plot]
            cols=get_colors_fom_cmap(range(len(smps)), 0, len(smps)-1, 'jet')

            for spcount,sp in enumerate(species[:3]):
                ax=plt.subplot(2,2,spcount+1)
                k='FE__%s' %sp
                for count, (col, seglist, smp) in enumerate(zip(cols, tech_summary_plot_data[k], smps)):
                    for segcount,(x,y) in enumerate(seglist):
                        ls='--' if segcount%2==1 else '-'
                        ax.plot(x,y,ls,c=col)
                ax.set_xlabel('Ewe(compensatedVrhe)')
                ax.set_ylabel(k)
            ax=plt.subplot(2,2,4)
            smprange=range(len(smps))
            for fomc,fomm,fomk in zip(['k','y','m','c','grey'],['o','s','<','>','x'],summ_plot_fom_keys):
                ax.plot(smprange,tech_summary_plot_data['fomlistd'][fomk][:max_samples_to_plot],'-',marker=fomm,label=fomk.partition('.')[0],c=fomc,ms=4)
            ax.set_ylabel('Charge (C)')
            ax.set_xticks(smprange)
            ax.set_xticklabels(['%d' %smp for smp in smps],rotation=45.)
            for ticklabel, tickcolor in zip(ax.get_xticklabels(), cols):
                ticklabel.set_color(tickcolor)

            plt.xlim(-0.5, len(smps)+2.9)
            plt.legend(loc=1,fontsize='small', frameon=False,numpoints=1,handlelength =0)
            plt.subplots_adjust(left=.11, bottom=.11, right=.96, top=.97, wspace=0.25,hspace=.12)

            fnsummim='%s__tech__%s__Jp_FE' %(anak,tech)
            p=os.path.join(destfolder, fnsummim+'.png')
            self.multirunfiledict['misc_files'][fnsummim+'.png']='ecms_png_file;'
            plt.savefig(p, dpi=300)
            p=os.path.join(destfolder, fnsummim+'.svg')
            self.multirunfiledict['misc_files'][fnsummim+'.svg']='ecms_svg_file;'
            plt.savefig(p)
            #end summary plot

            self.fomdlist=techd_fomdlist[tech]
            self.writefom(destfolder, anak, anauserfomd=anauserfomd, strkeys_fomdlist=self.strkeys_fomdlist,fn='%s__tech__%s__%s.csv' %(anak,tech, '-'.join(self.fomnames[:3])))
