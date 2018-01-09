import string, copy
# import time
import os, os.path  # , shutil
import sys
import numpy
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
import operator
import numpy as np
import re

projectroot = os.path.split(os.getcwd())[0]
sys.path.append(projectroot)
sys.path.append(os.path.join(projectroot, 'AuxPrograms'))
sys.path.append(os.path.join(projectroot, 'QtForms'))
sys.path.append(os.path.join(projectroot, 'AuxPrograms'))
sys.path.append(os.path.join(projectroot, 'OtherApps'))
sys.path.append(os.path.join(projectroot, 'BatchProcesses'))
sys.path.append(os.path.join(projectroot, 'AnalysisFunctions'))

# from fcns_math import *
from fcns_io import *
from fcns_ui import *


# from Analysis_Master import Analysis_Master_nointer
# analysismasterclass=Analysis_Master_nointer()

class setup_rcp_and_exp_ssrl():
    def __init__(self, import_path, calib_path, rcpext='.done', expext='.done', anaext='.done',
                 overwrite_runs=False, plate_idstr=None, access='hte',
                 pmidstr=None, sample_no_from_position_index=lambda i: (1 + i),
                 testmode=False):
        """
        the  data should be saved so that once import_path (folder containing spec
        file and a folder "images" with .tif) is given, 
        this class knows what to do to copy and name all rcp and exp files
        rcpext and expext should be set to .run for testing and then in standard 
        operation can make them .done
        overwrite_runs can be set to True to help with debugging but safer to keep 
        as False in case there is a mistkae, really overwrite of a .done run is 
        not allowed but this is not checked
        plate_idstr should be auto read but passing the string here overrides that
        access for the data is set here and can be public,hte,tri,muri
        pmidstr will be auto read from the .info file but if for some reason the 
        platemap used for xps is different this value can be overridden, which
        is dangerous but the sample_no generated for the .rcp/.exp must 
        correspond to the pmidstr
        sample_no_from_position_index should either be aq list of all the 
        sample_no in the order they were measured, or a lambda function like 
        the default value above when the sample_no were measured in order
        """
        self.access = access
        self.pmidstr = pmidstr
        self.import_path = import_path
        self.calib_path = calib_path
        self.sample_no_from_position_index = sample_no_from_position_index

        # hard coded definitions
        self.compname = 'HTE-SSRL-01'
        self.detectorname = 'Rayonix MarCCD'
        self.pixelsize = '79.0'
        self.datatype = 'ssrl'

        self.plate_idstr = plate_idstr
        iserror = self.parse_shell()
        if iserror:
            return

        self.rcpext = rcpext
        self.expext = expext
        self.anaext = anaext

        iserror = self.setup_folders(overwrite_runs, testmode)
        if iserror:
            return

        self.setup_file_dicts()
        self.add_all_files(testmode)
        self.save_rcp_exp(testmode)

    def setup_folders(self, overwrite_runs, testmode):
        if self.pmidstr is None:
            ans = getplatemappath_plateid(self.plate_idstr, erroruifcn=None, infokey='screening_map_id:',
                                          return_pmidstr=True)
            if ans is None:
                print 'aborting because failed retrieval of platemap id for plate :', self.plate_idstr
                return True
            self.pmidstr = ans[1]

        dropfolder = getdropfolder_exptype(self.datatype)

        if dropfolder is None:
            # messageDialog(None, 'Aborting SAVE because cannot find drop folder').exec_()
            print 'Aborting SAVE because cannot find drop folder'
            return True
        if (not testmode) and not os.path.isdir(dropfolder):
            os.mkdir(dropfolder)

        ellist = getelements_plateidstr(self.plate_idstr)
        rcplab = ''.join(ellist)
        self.rcpmainfoldname = '_'.join([timestampname()[:8], rcplab, get_serial_plate_id(self.plate_idstr)])

        rcpmainfolder = os.path.join(dropfolder, self.rcpmainfoldname)

        if (not testmode) and not os.path.isdir(rcpmainfolder):
            os.mkdir(rcpmainfolder)

        self.runfolderpath = os.path.join(rcpmainfolder, self.data_acquisition_timestamp + self.rcpext)

        if not testmode:
            if os.path.isdir(self.runfolderpath):
                if overwrite_runs:
                    shutil.rmtree(self.runfolderpath)
                else:
                    # messageDialog(None, 'Aborting SAVE because %s folder exists' %rcpmainfolder).exec_()
                    print 'Aborting SAVE because %s folder exists' % rcpmainfolder
                    return True
            os.mkdir(self.runfolderpath)
        return False

    def read_ssrl_calib(self, line_inds=None,
                        delim='='):  # add in the calib values to run parameters, although this calib may need to be manually overridden during the

        with open(self.calib_path, mode='r') as f:
            lines = f.readlines()
        if not line_inds is None:
            print 'lines are {}'.format(lines)
            lines = [lines[i] for i in line_inds]

        for l in lines:
            k, temp, v = l.partition(delim)
            self.run_params_dict[
                l.strip()] = v.strip()  # calib params are string vaslues even for the numbers so convert before sending to functions


        self.run_params_dict['detector_name'] = self.detectorname
        self.run_params_dict['pixel_size_micron'] = self.pixelsize

    def parse_shell(self):
        #unsure what file should be read here?
        #self.lines = [line for line in open(self.import_path)]
        #self.get_block_list()  # get the complete file as a list containing dicts
        #set the plateid
        if self.plate_idstr is None:  # ideally plate_id is read from the filename or spec file because it was entered
            # by user when starting data acquisition, but if it was passed in
            # the class init then ignore
            serial_no_str = os.path.split(self.import_path)[1].partition('_')[0].strip()
            if False in [c.isdigit() for c in serial_no_str]:
                print 'error reading plate_id for ', self.import_path
                return True
            if len(serial_no_str) >= 5:  # expect serial but this fails if plate_id
                self.plate_idstr = serial_no_str[:-1]
            else:
                self.plate_idstr = serial_no_str
        self.run_params_dict = {}

        p_files = os.listdir(self.import_path)
        shellfns = [fn for fn in p_files if not '.' in fn]
        self.speccsvfns = [fn for fn in p_files if  '.csv' in fn]
        self.shellfn = shellfns[0]
        with open(os.path.join(self.import_path, self.shellfn), mode='r') as f:
            lines = f.readlines()
        for l in lines:
            if l.startswith('#D'):
                ts = time.strptime(l[2:].strip(), '%a %b %d %H:%M:%S %Y')
                self.data_acquisition_timestamp = time.strftime('%Y%m%d.%H%M%S', ts)
            if l.startswith('#S'):
                scmd = l.partition('  ')[2].strip()
                if len(scmd) > 0:
                    self.run_params_dict['spec_command'] = scmd

        return False

    def strrep_generic_file_dict_value_sp(self, v):
        return filterchars(str(v), valid_chars="/<>-_.,; ()[]{}/%s%s%s" % (
            string.ascii_letters, string.digits, ''.join(['\\', '%', '&', '^', '!', '#', '*'])))

    def setup_file_dicts(self):
        self.expdict = {}
        self.expdict['experiment_type'] = self.datatype
        self.expdict['exp_version'] = '3'
        self.expdict['description'] = '%s run on plate_id %s' % (self.datatype, self.plate_idstr)
        self.expdict['created_by'] = self.datatype
        self.expdict['access'] = self.access
        runcount = 0
        runk = 'run__%d' % (runcount + 1)
        self.expdict[runk] = {}
        exprund = self.expdict[runk]
        self.rcpdict = {}
        rcpdict = self.rcpdict
        rcpdict['experiment_type'] = self.datatype
        # don't pay attention to this "technique_name" it is an artifact of previous data and does not have the
        # same meaning as e.g. XPSSURVEY
        rcpdict['technique_name'] = self.datatype
        rcpdict['rcp_version'] = '2'

        self.add_run_attr = lambda k, v: [d.update({k: v}) for d in [exprund, rcpdict]]

        self.add_run_attr('screening_map_id', self.pmidstr)

        self.add_run_attr('run_use', 'data')
        self.add_run_attr('plate_id', self.plate_idstr)
        self.add_run_attr('name', self.data_acquisition_timestamp)
        self.add_run_attr('access', self.access)

        self.add_run_attr('computer_name', self.compname)
        exprund['run_path'] = r'/%s/%s/%s/%s' % (
            self.datatype, self.compname.lower(), self.rcpmainfoldname, rcpdict['name'] + self.rcpext)
        exprund['rcp_file'] = rcpdict['name'] + '.rcp'

        rcpdict['parameters'] = {}
        exprund['parameters'] = {}
        self.add_run_param = lambda k, v: [d.update({k: v}) for d in [exprund['parameters'], rcpdict['parameters']]]

        self.add_run_param('plate_id', self.plate_idstr)

        for k, v in self.run_params_dict.iteritems():
            v = self.strrep_generic_file_dict_value_sp(v).strip('[').rstrip(
                ']')  # make lists comma delimited but without the brackets
            self.add_run_param(k, v)

        techdlist = []
        tech = 'SSRL'
        tk = 'files_technique__%s' % tech
        exprund[tk] = {}
        rcpdict[tk] = {}

        exprund[tk]['csv_spec_files'] = {}
        rcpdict[tk]['csv_spec_files'] = {}
        csvtechd = (rcpdict[tk]['csv_spec_files'], exprund[tk]['csv_spec_files'])

        exprund[tk]['meta_spec_files'] = {}
        rcpdict[tk]['meta_spec_files'] = {}
        metatechd = (rcpdict[tk]['meta_spec_files'], exprund[tk]['meta_spec_files'])

        exprund[tk]['image_files'] = {}
        rcpdict[tk]['image_files'] = {}
        tiftechd = (rcpdict[tk]['image_files'], exprund[tk]['image_files'])

        exprund[tk]['calib_files'] = {}
        rcpdict[tk]['calib_files'] = {}
        calibtechd = (rcpdict[tk]['calib_files'], exprund[tk]['calib_files'])

        exprund[tk]['shell_files'] = {}
        rcpdict[tk]['shell_files'] = {}
        shelltechd = (rcpdict[tk]['shell_files'], exprund[tk]['shell_files'])


        # messy fix for : : bug
        self.add_calib_file = lambda fn: [d.update({fn: filed_createflatfiledesc({'file_type': 'ssrl_calib_file'})})
                                          for d in calibtechd]
        self.add_speccsv_file = lambda fn: [
            d.update({fn: filed_createflatfiledesc({'file_type': 'ssrl_spec_csv_file'})})
            for d in csvtechd]
        self.add_metacsv_file = lambda fn, sample_no: [
            d.update({fn: filed_createflatfiledesc({'file_type': 'ssrl_meta_csv_file', 'sample_no': sample_no})})
            for d in metatechd]
        self.add_tif_file = lambda fn, sample_no: [
            d.update({fn: filed_createflatfiledesc({'file_type': 'ssrl_mar_tiff_file', 'sample_no': sample_no})})
            for d in tiftechd]
        self.add_shell_file = lambda fn: [
            d.update({fn: filed_createflatfiledesc({'file_type': 'ssrl_shell_file'})})
            for d in shelltechd]

    def add_all_files(self, testmode):
        # TODO read spec file to get x,y
        self.parse_shell()
        self.d = self.read_ssrl_calib()
        self.calib_fn = os.path.split(self.calib_path)[1]
        self.add_calib_file(self.calib_fn)
        self.add_shell_file(self.shellfn)
        #for now this is a for loop but because this would essentially correspond to dirrefent runs within a folder
        #there should be some better checking of it ... or better data aquisition rules because it is hard to tell a
        # z height adjustment from an actual measurement
        for fn in self.speccsvfns:
            self.add_speccsv_file(fn)

        fns = os.listdir(os.path.join(self.import_path, 'images'))
        self.speccsv_fns, self.tif_fns = [fn for fn in fns if '.txt' in fn], [fn for fn in fns if '.tif' in fn]

        ID_spec = np.array([j.split('_')[1].strip('.txt') for j in self.speccsv_fns]).astype(np.int)
        ID_tif = np.array([j.split('_')[1].strip('.tif') for j in self.tif_fns]).astype(np.int)

        #check if specs and tif are read in the same way so once spec are parsed
        # a simple map can be run on add_tif_file
        if not np.sum(np.argsort(ID_spec)-np.argsort(ID_tif)) == 0:
            argsort_ID_spec = np.argsort(ID_spec)
            self.tif_fns = self.tif_fns[argsort_ID_spec]

        position_index_of_file_index = lambda fi: fi
        sample_no_of_file_index = lambda fi: self.sample_no_from_position_index[
            position_index_of_file_index[position_index_of_file_index(fi)]] if isinstance(
            self.sample_no_from_position_index, list) else self.sample_no_from_position_index(
            position_index_of_file_index(fi))

        for fntif,fncsv in zip(enumerate(self.tif_fns),enumerate(self.speccsv_fns)):
            self.add_tif_file(fntif[1], sample_no_of_file_index(fntif[0]))
            self.add_metacsv_file(fncsv[1], sample_no_of_file_index(fncsv[0]))

    def save_rcp_exp(self, testmode):
        rcpfilestr = strrep_filedict(self.rcpdict)
        p = os.path.join(self.runfolderpath, self.rcpdict['name'] + '.rcp')
        if testmode:
            print 'THIS IS THE RCP FILE THAT WOULD BE SAVED:'
            print rcpfilestr
            print os.path.join(self.import_path, self.shellfn)
            return
        with open(p, mode='w') as f:
            f.write(rcpfilestr)
        # print 'rcp file saved to ', p
        saveexp_txt_dat(self.expdict, saverawdat=False, experiment_type=self.datatype, rundone=self.expext,
                        file_attr_and_existence_check=False, runtodonesavep=self.runfolderpath, savefolder=self.runfolderpath)
        # print 'exp file saved to ', dsavep
        if not testmode:
            shutil.copy(self.calib_path, os.path.join(self.runfolderpath, self.calib_fn))
            shutil.copy(os.path.join(self.import_path, self.shellfn), os.path.join(self.runfolderpath, self.shellfn))
            for fn in self.speccsvfns:
                shutil.copy(os.path.join(self.import_path, fn), os.path.join(self.runfolderpath, fn))

            img_path = os.path.join(self.import_path,'images')
            for fntif, fncsv in zip(self.tif_fns, self.speccsv_fns):
                shutil.copy(os.path.join(img_path, fntif), os.path.join(self.runfolderpath, fntif))
                shutil.copy(os.path.join(img_path, fncsv), os.path.join(self.runfolderpath, fncsv))
        print self.runfolderpath

#REMINDER: this class looks for the shellfile file (no file ending) that contains information
import_path = r'K:\experiments\ssrl\user\2017Jul\43557_CuPdZn_toredo'
calib_path = r'K:\experiments\ssrl\user\SSRLJan2017\calib\version_4.calib'
importclass = setup_rcp_and_exp_ssrl(import_path, calib_path, rcpext='.done', expext='.done', overwrite_runs=True,
                                     plate_idstr=None, access='hte', pmidstr=None,
                                     sample_no_from_position_index=lambda i: (1 + i), testmode=False)
