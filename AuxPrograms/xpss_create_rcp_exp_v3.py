import string, copy
#import time
import os, os.path#, shutil
import sys
import numpy
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
import operator
import numpy as np
import re
projectroot=os.path.split(os.getcwd())[0]
sys.path.append(projectroot)
sys.path.append(os.path.join(projectroot,'AuxPrograms'))
sys.path.append(os.path.join(projectroot,'QtForms'))
sys.path.append(os.path.join(projectroot,'AuxPrograms'))
sys.path.append(os.path.join(projectroot,'OtherApps'))
sys.path.append(os.path.join(projectroot,'BatchProcesses'))
sys.path.append(os.path.join(projectroot,'AnalysisFunctions'))

#from fcns_math import *
from fcns_io import *
from fcns_ui import *



class setup_rcp_and_exp_xpss():
    def __init__(self, import_path, rcpext='.done', expext='.done', 
                 overwrite_runs=False, plate_idstr=None, access='hte', 
                 pmidstr=None, sample_no_from_position_index=lambda i:(1+i), 
                 testmode=False):
        """
        the xpss data should be saved so that once import_path is given, 
        this class knows what to do to copy and name all rcp and exp files
        rcpext and expext should be set to .run for testing and then in standard 
        operation can make them .done
        overwrite_runs can be set to True to help with debugging but safer to keep 
        as False in case there is a mistkae, really overwrite of a .done run is 
        not allowed but this is not checked
        plate_idstr should be auto read but passing the string here overrides that
        access for the data is set here and can be public,hte,tri,muri
        pmidstr will be auto read from the .info file but if for some reason the 
        platempa used for xps is different this value can be overridden, which 
        is dangerous but the sample_no generated for the .rcp/.exp must 
        correspond to the pmidstr
        sample_no_from_position_index should either be aq list of all the 
        sample_no in the order they were measured, or a lambda function like 
        the default value above when the sample_no were measured in order
        """
        self.access=access
        self.pmidstr=pmidstr
        self.import_path=import_path
        self.sample_no_from_position_index=sample_no_from_position_index

        self.plate_idstr=plate_idstr
        self.parse_spec_files()
        self.datatype='xpss'


        self.rcpext=rcpext
        self.expext=expext
        iserror=self.setup_folders(overwrite_runs, testmode)
        if iserror:
            return
        
        self.setup_file_dicts()
        self.add_all_files(testmode)
        self.save_rcp_exp(testmode)
        
    
    def setup_folders(self, overwrite_runs, testmode):
        if self.pmidstr is None:
            ans=getplatemappath_plateid(self.plate_idstr, erroruifcn=None, infokey='screening_map_id:', return_pmidstr=True)
            if ans is None:
                print 'aborting because failed retrieval of platemap id for plate :', self.plate_idstr
                return True
            self.pmidstr=ans[1]

        dropfolder=self.getdropfolder_exptype(self.datatype)
        if dropfolder is None:
            #messageDialog(None, 'Aborting SAVE because cannot find drop folder').exec_()
            print 'Aborting SAVE because cannot find drop folder'
            return True
        if (not testmode) and not os.path.isdir(dropfolder):
            os.mkdir(dropfolder)
            
        ellist=getelements_plateidstr(self.plate_idstr)
        rcplab=''.join(ellist)
        self.rcpmainfoldname='_'.join([timestampname()[:8], rcplab, get_serial_plate_id(self.plate_idstr)])
        
        rcpmainfolder=os.path.join(dropfolder, self.rcpmainfoldname)
        
        if (not testmode) and not os.path.isdir(rcpmainfolder):
            os.mkdir(rcpmainfolder)
            
        
        self.runfolderpath=os.path.join(rcpmainfolder, self.data_acquisition_timestamp+self.rcpext)
        if not testmode:
            if os.path.isdir(self.runfolderpath):
                if overwrite_runs:
                    shutil.rmtree(self.runfolderpath)
                else:
                    #messageDialog(None, 'Aborting SAVE because %s folder exists' %rcpmainfolder).exec_()
                    print 'Aborting SAVE because %s folder exists' %rcpmainfolder
                    return True
            os.mkdir(self.runfolderpath)
        return False

    def get_block_list(self):
        block_identifier = 'Dataset filename'
        blockIDX = [i for i in range(len(self.lines)) if block_identifier in self.lines[i]]
        mid_l = np.sort(np.unique(np.diff(np.array(blockIDX))))[1]
        #get spectral blocks
        line_pos = 0
        self.pre_parsed = []
        units = ['eV', 'm', 'Counts']
        for i in range(1,len(blockIDX)):
            if blockIDX[i]-blockIDX[i-1] == mid_l:
                #then we have a spectral block and a dict containing all the info is created
                #block = lines[line_pos:line_pos]
                block_dict = {}
                content = self.lines[blockIDX[i-1]:blockIDX[i]]
                for c in content:
                    #strip away all unnessesary tabs and spaces
                    c = re.sub('[ \t]+' , ' ', c)
                    if len(c.split(' = '))>1:
                        key,val = c.split(' = ')
                        #this parses a list of values 
                        if ', ' in val:
                            #numeric data
                            val = np.array(val.strip('{').strip('}\n').split(', ')).astype(np.float)
                        else:
                            #this parses positional information
                            if type(val) is not 'float':
                                for unit in units:
                                    try:
                                        if unit in val:
                                            val = re.sub('[ \t]+' , ' ', val)
                                            val = np.float(val.strip('\n').strip(unit))
                                    except:
                                        pass
                        block_dict[key] = val
        
                self.pre_parsed.append(block_dict)
            else:
                #we have something else and go to next block
                pass
        #reminder: the for loop above seems to omit the image of the platen lets see if that is always nessesary

    def get_all_params(self):
        temp = {'technique':[],'passE':[],'stepE':[],'startE':[]}
        self.xpsspec = []
        for spec in self.pre_parsed[1::]:
            #generate a technique name
            method = spec[' 2 Scan type'].strip('\n').strip('F_')
            #this looks strange but somehowit sometimes won't find
            #the appropriate key for 3114 Chemical symbol or formula
            ID_ChemKey = [i for i in range(len(spec.keys())) if '3113' in spec.keys()[i]]
            element_an = spec[spec.keys()[ID_ChemKey[0]]].strip('\n')
            transition  = spec['3114 Transition or charge state'].strip('\n')
            temp['technique'].append('{}-{}{}'.format(method,element_an,transition))
            temp['passE'].append(spec[' 42 Pass energy'])
            temp['stepE'].append(spec[' 4 Spectrum scan step size'])
            #excitation energy is hardcoded to 1486.6 eV
            temp['startE'].append(1486.6-spec[' 3 Spectrum scan start'])
            self.xpsspec.append(spec[' 12 Ordinate values'])
        self.allparams = temp
        
    def get_params(self):
        self.get_all_params()
        self.params = {key:[] for key in self.allparams.keys()}
        #attention: this returns the techniques alphabetically sorted
        #and not how they appear in the file so ID sort needs to be performed
        val,IDx = np.unique(self.allparams['technique'],return_index=True)
        for ID in IDx[np.argsort(IDx)]:
            for key in self.allparams.keys():
                self.params[key].append(self.allparams[key][ID])
                
    def parse_spec_files(self):
        self.lines = [line for line in open(self.import_path)]
        self.get_block_list() #get the complete file as a list containing dicts
        #set the plateid
        if self.plate_idstr is None:#ideally plate_id is read from the filename or spec file because it was entered 
            #by user when starting data acquisition, but if it was passed in 
            #the class init then ignore
            IDStr = self.import_path.strip('.cal')[-4:]
            try:
                IDNum = np.int(IDStr)#
                self.plate_idstr=self.import_path.strip('.cal')[-4:]#forcing naming convention i.e. 4080.cal
            except(ValueError):
                print 'Filename {} not correct!'.format(IDStr)
        #generate meta file in which all important info is stored
        #in meta now the infor for each spectrum is stored
        self.get_params()
        #assuming these are unique technique names
        #print('Techniques: {}'.format(self.params['technique']))
        self.technique_names=self.params['technique']
        #parse date
        from dateutil.parser import parse
        self.data_acquisition_timestamp='20'+parse(self.pre_parsed[0][' 151 Date Acquired']).strftime('%d%y%m.%H%M%S') 
        self.run_params_dict = {}
        for key in self.params.keys():
            if key == 'technique':            
                self.technique_names = self.params['technique']
                self.run_params_dict['technique_names'] = self.technique_names
            else:
                self.run_params_dict[key]=self.params[key]
                
    def strrep_generic_file_dict_value_sp(self,v):
        return filterchars(str(v), valid_chars = "/<>-_.,; ()[]{}/%s%s%s" % (string.ascii_letters, string.digits,''.join(['\\','%','&','^','!','#','*'])))

    def setup_file_dicts(self):
        self.expdict={}
        self.expdict['experiment_type']=self.datatype
        self.expdict['exp_version']='3'
        self.expdict['description']='%s run on plate_id %s with %s' %(self.datatype, self.plate_idstr, ','.join(self.technique_names))
        self.expdict['created_by']=self.datatype
        self.expdict['access']=self.access
        runcount=0
        runk='run__%d' %(runcount+1)
        self.expdict[runk]={}
        exprund=self.expdict[runk]
        self.rcpdict={}
        rcpdict=self.rcpdict
        rcpdict['experiment_type']=self.datatype
        rcpdict['technique_name']=self.datatype#don't pay attention to this "technique_name" it is an artifact of previous data and does not have the same meaning as e.g. XPSSURVEY
        
        rcpdict['rcp_version']='2'
    
        self.add_run_attr=lambda k, v:[d.update({k:v}) for d in [exprund, rcpdict]]
        
        self.add_run_attr('screening_map_id', self.pmidstr)

        self.add_run_attr('run_use', 'data')
        self.add_run_attr('plate_id', self.plate_idstr)
        self.add_run_attr('name', self.data_acquisition_timestamp)
        self.add_run_attr('access', self.access)

        compname='HTE-XPSS-01'
        self.add_run_attr('computer_name', compname)
        exprund['run_path']=r'/%s/%s/%s/%s' %(self.datatype, compname.lower(), self.rcpmainfoldname, rcpdict['name']+self.rcpext)
        exprund['rcp_file']=rcpdict['name']+'.rcp'


        rcpdict['parameters']={}
        exprund['parameters']={}
        self.add_run_param=lambda k, v:[d.update({k:v}) for d in [exprund['parameters'], rcpdict['parameters']]]

        self.add_run_param('plate_id', self.plate_idstr)
        
        for k, v in self.run_params_dict.iteritems():
            v=self.strrep_generic_file_dict_value_sp(v).strip('[').rstrip(']')#make lists comma delimited but without the brackets
            self.add_run_param(k, v)
        
        
        techdlist=[]
        for count, tech in enumerate(['XPSS']+self.technique_names):
            tk='files_technique__%s' %tech
            exprund[tk]={}
            rcpdict[tk]={}
            if count==0:
                exprund[tk]['kratos_files']={}
                rcpdict[tk]['kratos_files']={}
                xpsstechd=(rcpdict[tk]['kratos_files'], exprund[tk]['kratos_files'])
            else:
                exprund[tk]['pattern_files']={}
                rcpdict[tk]['pattern_files']={}
                techdlist+=[(rcpdict[tk]['pattern_files'], exprund[tk]['pattern_files'])]
        #messy fix for : : bug
        self.add_kratos_file=lambda fn:[d.update({fn:filed_createflatfiledesc({'file_type':'xpss_kratos_file'})}) for d in xpsstechd]
        self.pattern_file_keys=['BE(eV)','Intensity']
        self.add_pattern_file=lambda tech, fn, nrows, sample_no:[d.update({fn:filed_createflatfiledesc({'file_type':'xpss_spectrum_csv','keys':self.pattern_file_keys,'num_header_lines':1,'num_data_rows':nrows,'sample_no':sample_no})}) for d in techdlist[self.technique_names.index(tech)]]
     
    def save_rcp_exp(self, testmode):
        rcpfilestr=strrep_filedict(self.rcpdict)
        p=os.path.join(self.runfolderpath, self.rcpdict['name']+'.rcp')
        if testmode:
            print 'THIS IS THE RCP FILE THAT WOULD BE SAVED:'
            print rcpfilestr
            return
        with open(p, mode='w') as f:
            f.write(rcpfilestr)
        #print 'rcp file saved to ', p
        saveexp_txt_dat(self.expdict, saverawdat=False, experiment_type=self.datatype, rundone=self.expext, file_attr_and_existence_check=False)
        #print 'exp file saved to ', dsavep
    
    def add_all_files(self, testmode):
        self.import_path#this path should be all that's necessary to 
        position_index_of_file_index=lambda fi:fi//len(self.technique_names)
        sample_no_of_file_index=lambda fi:self.sample_no_from_position_index[position_index_of_file_index[position_index_of_file_index(fi)]] if isinstance(self.sample_no_from_position_index, list) else self.sample_no_from_position_index(position_index_of_file_index(fi))
        kratosfn=os.path.split(self.import_path)[1]
        self.add_kratos_file(kratosfn)
        if not testmode:
            shutil.copy(self.import_path, os.path.join(self.runfolderpath, kratosfn))
        fns=['{}_XPS{}.csv'.format(sample_no_of_file_index(i),self.allparams['technique'][i]) for i in range(len(self.xpsspec))]
        for fileindex, fn in enumerate(fns):
            sample_no=sample_no_of_file_index(fileindex)
            tech=self.technique_names[fileindex%len(self.technique_names)]
            self.add_pattern_file(tech, fn, len(self.xpsspec[fileindex]), sample_no)
            y = self.xpsspec[fileindex]
            x = np.array([self.allparams['startE'][fileindex]+i*self.allparams['stepE'][fileindex] for i in range(len(self.xpsspec[fileindex]))])
            sav = np.array([x,y]).T
            if not testmode:
                np.savetxt(os.path.join(self.runfolderpath,fn),sav,delimiter=',',fmt='%3.4f, %0.0f',header=','.join(self.pattern_file_keys), comments='')
##example
#import_path = 'K:/experiments/xpss/user/MnFeCoNiCuZn/4082.cal'
#xpsimportclass=setup_rcp_and_exp_xpss(import_path, rcpext='.done', expext='.done', overwrite_runs=True, plate_idstr=None, access='tri', pmidstr=None, sample_no_from_position_index=lambda i:(1+i), testmode=True)
import_path = 'K:/experiments/xpss/user/MnFeCoNiCuZn/4082.cal'
sample_no = [i+1 for i in range(1972)]+[i+1 for i in range(34)]
xpsimportclass = setup_rcp_and_exp_xpss(import_path, rcpext='.done', expext='.done', overwrite_runs=True,
                                        plate_idstr=None, access='tri', pmidstr=None,
                                        sample_no_from_position_index=lambda i: sample_no[i], testmode=False)
