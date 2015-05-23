# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:37:34 2013

@author: santosh
"""
import os,csv, numpy as np, copy, scipy as sp, math, pprint,sys,inspect
import matplotlib.pyplot as plt
plt.ion()
##from datamanipulation import *
from scipy import stats,signal
import matplotlib.cm as cm
from matplotlib import colors
import pickle
import time
import tkMessageBox
from scipy.signal import savgol_filter
import shutil

#This block averages a certain number of rows together to reduce the scale of the data
def reducedata(data,data_idxs=None,scale=1,axis=0):
    reddata_idxs=np.zeros(shape=(np.ceil(float(np.shape(data)[axis])/scale),))
    reddata=np.array([np.mean(data[loc:min(loc+scale,np.shape(data)[axis]),:],axis) for loc in np.arange(0,np.shape(data)[axis],scale)])
    if data_idxs!=None:
        reddata_idxs[loc//scale]=int(math.floor(np.median(data_idxs[loc:min(loc+scale,np.shape(data_idxs)[axis])])))
        return reddata,reddata_idxs
    else:
        return reddata
    

#This block takes the average of local data (size decided by variable order) around each point and checks if the 
#current data point is greater by upper 80 percentile by certain amount or lower by lower 20 percentile by certain amount. If the check is true then
#the data point is replaced by the local mean ...CONSIDER USING SOMEKING OF RATIOS WITH STD.. MAY BE X-MU/SIGMA > RATIO as criterion!!   
    

    
def readsignal(file,darkkey,refkey,darkdata,refdata,mthd,excludecols,lower_wavelength,upper_wavelength,rowredscale,max_mthd_allowed,min_mthd_allowed):
        data[key]['rawselectinds']=inds[((data[key]['raw_unprocessed'][:,0]>lower_wavelength)*(data[key]['raw_unprocessed'][:,0]<upper_wavelength))]
        data[key]['raw']=data[key]['raw_unprocessed'][(data[key]['raw_unprocessed'][:,0]>lower_wavelength)*(data[key]['raw_unprocessed'][:,0]<upper_wavelength),:]    
        data[key]['raw'],data[key]['rawselectinds']=reducedata(data[key]['raw'],data_idxs=data[key]['rawselectinds'],scale=rowredscale)
        data[key]['rawselectinds']=data[key]['rawselectinds'].tolist()
        data[key]['av-raw']=np.array(np.mean(data[key]['raw'][:, 1+excludecols[0]:np.shape(data[key]['raw'])[1]-excludecols[1]],1))
        data[key][mthd+'_unsmooth']=(data[key]['av-raw']-darkdata)/(refdata-darkdata)
        return measurement_info[key],data[key],col_heading[key]
#The above code block reads the measurement information into measurement_info and data is smoothed and corresponding refkey and darkkey are assigned

        
#//////mthd2abs
        dx=[data[key]['E'][1]-data[key]['E'][0]]
        num_idxs=np.size(data[key]['E'])
        dx+=[(data[key]['E'][idx+1]-data[key]['E'][idx-1])/2. for idx in xrange(1,num_idxs-1)]
        dx+=[data[key]['E'][-1]-data[key]['E'][-2]]
        dx=np.array(dx) 
        data[key]['abs_1stderiv']=savgol_filter(data[key]['abs'], window_length, polyorder, delta=1.0, deriv=1)/dx
        data[key]['abs_2ndderiv']=savgol_filter(data[key]['abs'], window_length, polyorder, delta=1.0, deriv=2)/(dx**2)
    
        if np.isnan(data[key]['abs']).any() or (data[key]['abs']<=0.).any():
            print data[key]['abs']
            nankeys.append(key)
            
    return data,nankeys
        

def rescale(data,max_mthd_allowed,min_mthd_allowed,min_min=0.,max_max=1.,mini=None,maxi=None):
    min_rescaled=False
    max_rescaled=False
    if mini==None:    
        mini=np.min(data)
    if maxi==None:
        maxi=np.max(data)
    if mini>=min_mthd_allowed and mini<=min_min:
        data=data-mini+min_min+0.01
        min_rescaled=True
    if maxi<=max_mthd_allowed and maxi>=max_max:
        data=data/(maxi+0.01)
        max_rescaled=True
    return min_rescaled,max_rescaled,data

    
#This block identifies peaks in the measurement corresponding to the mthd i.e post reduction,smoothing and correction with reference files 
#but prior to conversion to absorbance metric.
#Identifies local maxima with neighborhood defined by order and these local maxima should satisty that the criteria that they are greater than 

def residuals(params,xdata,ydata):
#    if 
    err=sum((np.abs(ydata-linpiecewise(params,xdata))/ydata)**2)
    return err
    
# params: zeroth index corresponds to the yfit value at x=x0. Next num_knots indices correspond to the knot positions. Next num_knots-1 indices correspond
#to slopes for the linear regions.  Piecewise linear addition to obtain the value of fitdata at a specific value of x. 
    
#Division by ydata is to ensure that errors at low absorbance values are given high importance and the ones
#at higher absorbance values are given lower importance (since the important region is where the absorbance starts increasing
#from low value prior to band gap to higher values...The noise at very high energy levels usually having high absorbance will not 
#effect the quality of the result a lot)
def linpiecewise(params,x):
    params=np.array(params)
    x=np.array(x)
    num_knots=np.size(params)//2
    fitdata=params[0]
    for loc in np.arange(1,num_knots):
        fitdata=fitdata+params[num_knots+loc]*(x>=(params[loc]-0.0001))*(x-(params[loc]))
    return fitdata

#xorder: if loc in data represents smaller value of energy to higher value of energy then xorder is increasing otherwise decreasing
#first constraint in cons is to ensure minimum knot distance min_knotdist. Second equality constraint indicates that the first and the last knot are fixed to the first and last values of x
#Initially knot locations are evenly spread out between xvalues of interest and all slopes are set to zero. tolerance is the tolerance for convergence of linear properties.

def linearfit(xdata,ydata,key,num_knots,min_knotdist,xorder,options,tol):
    if xorder=='increasing': sign=1
    elif xorder=='decreasing': sign=-1
    locs=np.arange(1,num_knots+1)
    cons=({'type':'ineq','fun':lambda params: params[locs[0:-1]+1]*sign-(params[locs[0:-1]]*sign+min_knotdist)},\
    {'type':'eq','fun':lambda params: np.array([params[1],params[num_knots]])-np.array([xdata[0],xdata[-1]],)})
    init_x=np.arange(xdata[0],xdata[-1],(xdata[-1]-xdata[0])/((num_knots-1)))
    if np.size(init_x)!=num_knots:
        init_x=np.hstack((init_x,xdata[-1]))
    else:
        init_x[-1]=xdata[-1]
    init_params=np.hstack((0,init_x,np.ones(num_knots-1)))
    res = sp.optimize.minimize(residuals,init_params, args=(xdata,ydata),constraints=cons, method='SLSQP',options=options,tol=tol)
    return res
    
def mergelinsegs(params,num_knots,max_merge_differentialTP,merge_linsegslopediff_percent,key):
    knots=params[1:num_knots+1]
    partial_slopes=params[num_knots+1:2*num_knots]
    slopes=np.empty(np.shape(partial_slopes))
    for loc in np.arange(0,np.shape(partial_slopes)[0]):
        slopes[loc]=np.sum(partial_slopes[0:loc+1])
    np.delete(partial_slopes,np.s_[0::],axis=None)    

    if merge_linsegslopediff_percent>=1:
        merge_linsegslopediff_percent=merge_linsegslopediff_percent/100.0
    while True:
        num_merges=0
        j=0
        loc=0        
        newslopes=np.empty(np.shape(slopes)[0])
        newknots=np.empty(np.shape(knots)[0])
        newslopes[0]=slopes[0]
        newknots[0:2]=knots[0:2]
        while loc <np.shape(slopes)[0]-1:
            medianslope=(newslopes[j]*(newknots[j+1]-newknots[j])+slopes[loc+1]*(knots[loc+2]-knots[loc+1]))/(knots[loc+2]-newknots[j])
            differentialTPdiff=(medianslope-newslopes[j])*(newknots[j+1]-newknots[j])
            TPdiff=newslopes[j]*(newknots[j+1]-newknots[j])
            if abs(differentialTPdiff)<min(max_merge_differentialTP,merge_linsegslopediff_percent*TPdiff):
                newslopes[j]=medianslope
                slopes[loc]=medianslope
                slopes[loc+1]=medianslope
                newknots[j+1]=knots[loc+2]
                loc=loc+1
                num_merges+=1
            else:
                j=j+1
                loc=loc+1
                newslopes[j]=slopes[loc]
                newknots[j]=knots[loc]
                newknots[j+1]=knots[loc+1]
        newslopes=np.delete(newslopes,np.s_[j+1::],axis=None)
        newknots=np.delete(newknots,np.s_[j+2::],axis=None)
        slopes=newslopes
        knots=newknots
        if num_merges==0:
            break
    num_knots=j+2

    partial_newslopes=np.empty(np.shape(newslopes)[0])
    partial_newslopes[0]=newslopes[0]
    for loc in np.arange(1,np.shape(newslopes)[0]):
        partial_newslopes[loc]=newslopes[loc]-newslopes[loc-1]   
    params=np.concatenate(([params[0]],newknots,partial_newslopes),axis=0)
    return params
    
#The block below creates data for each bg type and interacts with fitting, residual measurement functions to identify the best linear piecewise parameters which are then sent to calc_bandgap for bandgap calculations.
def fitresult(data,types,peaksexist,nankeys,keys,num_knots,tol,min_allowedslope,min_bgTP_diff,min_bkgrdslope,min_bgbkgrdslopediff,min_finseglength,merge_bgslopediff_percent,min_TP_finseg_diff,min_bgfinalseglength,max_merge_differentialTP,merge_linsegslopediff_percent,maxtol,plot=False,viewknots=True,min_knotdist=0.05,xorder='increasing',dispresult=False):
    tlinfit=0
    tcalcbg=0
    maxiter={'DA':1000,'DF':1000, 'IA':1000,'IF':1000}
    new_num_knots={};knots={};slopes={}; bgknots={};bkgrdknots={};bg={};abs_expl={};bgcode={};params={};fitdata={}
    for key in keys:
        new_num_knots[key]={};knots[key]={};slopes[key]={};bgknots[key]={};bkgrdknots[key]={};bg[key]={};abs_expl[key]={};bgcode[key]={};params[key]={};fitdata[key]={}
        if key not in peaksexist+nankeys:
            for type in types:
                options={'maxiter':maxiter[type],'disp':dispresult}
                t=time.time()
                yoffset=-np.min(data[key][type])+0.03 if np.min(data[key][type])<0.03 else 0
                res=linearfit(data[key]['E'],data[key][type]+yoffset,key,num_knots,min_knotdist,xorder,options,tol,plot=plot,viewknots=viewknots)
                if not res.success:
                    maxiter[type]=2000
                    options={'maxiter':maxiter[type],'disp':dispresult}
                    res=linearfit(data[key]['E'],data[key][type]+yoffset,key,num_knots,min_knotdist,xorder,options,tol,plot=plot,viewknots=viewknots)
                if not res.success:
                    maxiter[type]=2000
                    options={'maxiter':maxiter[type],'disp':dispresult}
                    for i in xrange(int(np.log10(tol)),int(np.log10(maxtol))+1,-1):
                        newtol=10.**i
                        res=linearfit(data[key]['E'],data[key][type]+yoffset,key,num_knots,min_knotdist,xorder,options,newtol,plot=plot,viewknots=viewknots)
                        if res.success:
                            break
                    maxiter[type]=1000
                tlinfit+=time.time()-t
                tempparams=res.x
                t=time.time()                
                if not res.success:
                    params[key][type],knots[key][type],slopes[key][type],bgknots[key][type],bkgrdknots[key][type],bg[key][type],abs_expl[key][type],fitdata[key][type]=np.ones([8,1])*np.NaN
                    bgcode[key][type]=[9]
                else:
                    params[key][type]=mergelinsegs(tempparams,num_knots,max_merge_differentialTP,merge_linsegslopediff_percent,key)
                    params[key][type],knots[key][type],slopes[key][type],bgknots[key][type],bkgrdknots[key][type],bg[key][type],abs_expl[key][type],bgcode[key][type]=calc_bandgap(params[key][type],
                np.size(params[key][type])/2,min_allowedslope,min_bgTP_diff,min_bkgrdslope,min_bgbkgrdslopediff,min_finseglength,
                merge_bgslopediff_percent,min_TP_finseg_diff,min_bgfinalseglength)
                
                    fitdata[key][type]=linpiecewise(params[key][type],data[key]['E'])-yoffset
                tcalcbg+=time.time()-t

        elif key in peaksexist:
            for type in types:
                params[key][type],knots[key][type],slopes[key][type],bgknots[key][type],bkgrdknots[key][type],bg[key][type],abs_expl[key][type],fitdata[key][type]=np.ones([8,1])*np.NaN
                bgcode[key][type]=[7]
        elif key in nankeys:
            for type in types:
                params[key][type],knots[key][type],slopes[key][type],bgknots[key][type],bkgrdknots[key][type],bg[key][type],abs_expl[key][type],fitdata[key][type]=np.ones([8,1])*np.NaN
                bgcode[key][type]=[8]

    return(params,knots,slopes,bgknots,bkgrdknots,bg,abs_expl,bgcode,fitdata,tlinfit,tcalcbg)
            
def calc_bandgap(params,num_knots,min_allowedslope,min_bgTP_diff,min_bkgrdslope,min_bgbkgrdslopediff,min_finseglength,merge_bgslopediff_percent,min_TP_finseg_diff ,min_bgfinalseglength):
    if merge_bgslopediff_percent>1:
        merge_bgslopediff_percent=merge_bgslopediff_percent/100
    knots=params[1:num_knots+1]
    partial_slopes=params[num_knots+1:2*num_knots]
    slopes=np.empty(np.shape(partial_slopes))
    for loc in np.arange(0,np.shape(partial_slopes)[0]):
        slopes[loc]=np.sum(partial_slopes[0:loc+1])
    np.delete(partial_slopes,np.s_[0::],axis=None)
    num_slopes=np.shape(slopes)[0]
    bgknots_lower=[]; bkgrdknots_lower=[]; bg=[]; abs_expl=[]; bgcode=[]
    if (knots[num_slopes]-knots[num_slopes-1])>=min_finseglength:
        num_segments=num_slopes
    else:
        num_segments=num_slopes-1
    tot_segs=num_segments
    for i in np.arange(1,num_segments-1):
        if slopes[i]<min_allowedslope:
            num_segments=i
#            bgcode=[1]
            break
    for i in np.arange(1,num_segments-1):
#        if 1 not in bgcode:
#==============================================================================
#           TPdiff.extend([(knots[i+1]-knots[i])*slopes[i]])min_TP_finseg_diff 
#==============================================================================
            if slopes[i]>slopes[i-1] and slopes[i]>0 and slopes[i-1]>min_bkgrdslope:
                TPdiff=(knots[i+1]-knots[i])*slopes[i]
                if TPdiff>=min_bgTP_diff:
                    if slopes[i]>slopes[i+1]:    
                        bgknots_lower.extend([i])
                        abs_expl.extend([TPdiff])
                        bgcode.extend([0])
                    else:            
                        if slopes[i+1]-slopes[i]<merge_bgslopediff_percent*(slopes[i]):
                            if i==num_segments-2 or (i!=num_segments-2 and slopes[i+2]<slopes[i+1]):
                                TPdiff=(knots[i+1]-knots[i])*slopes[i]
                                if TPdiff>=min_bgTP_diff:
                                    bgknots_lower.extend([i])
                                    abs_expl.extend([TPdiff])
                                    bgcode.extend([2])
    if np.size(bgknots_lower)==0:
        j=num_segments-1
        if slopes[j]>slopes[j-1] and slopes[j]>0 and slopes[j-1]>min_bkgrdslope:
          TPdiff=(knots[j+1]-knots[j])*slopes[j]
          if TPdiff>=min_TP_finseg_diff and knots[j+1]-knots[j]>min_bgfinalseglength:
              bgknots_lower.extend([j])
              abs_expl.extend([TPdiff])
              bgcode.extend([6])
   
    if np.size(bgknots_lower)!=0:
        for i in np.arange(0,np.shape(bgknots_lower)[0]):
            if i==0: low_limit=-1
            else: low_limit=bgknots_lower[i-1]
            if bgknots_lower[i]-1==low_limit:
                del bgknots_lower[i::]  
                del abs_expl[i::]
                del bgcode[i::]
                break
#            A band gap segments bkgrnd segment cannot be previous band gap segment
            for loc in np.arange(bgknots_lower[i]-1,low_limit,-1):
                if slopes[loc]<slopes[loc+1] and slopes[loc]>min_bkgrdslope:
                    if loc==low_limit+1:
                        bkgrdknots_lower.extend([loc])
#                        This block gets executed when the bkgrd segment is just to the right of the previous band gap segment
                        break
                    else: continue
                elif loc!=bgknots_lower[i]-1:
                    bkgrdknots_lower.extend([loc+1])                    
                    break
                else: 
                    temp=np.shape(bgknots_lower)[0]
                    del bgknots_lower[i::]  
                    del abs_expl[i::]
                    del bgcode[i::]
                    i=temp
#                    This block should never get executed because any bgknot will have corresponding bkgrdknot except
#                    when the previous segment is also a band gap segment taken care of bgknots_lower[i]-1==low_limit block above

    if np.size(bgknots_lower)!=0:
        if not (np.size(bgcode)==1 and bgcode[0]==1):

            if not (((np.size(abs_expl)==np.size(bgknots_lower)) and (np.size(bgknots_lower)==np.size(bkgrdknots_lower))) and (np.size(np.array(bgcode)[np.where(np.not_equal(bgcode,1))[0]])==np.size(bkgrdknots_lower))):
                raise ValueError('abs_expl,bgknots_lower,bgcodes and bkgrdknots_lower do not have the same size')
        for i in np.arange(0,np.shape(bkgrdknots_lower)[0]):
            if (slopes[bgknots_lower[i]]-slopes[bkgrdknots_lower[i]])<min_bgbkgrdslopediff:
                bgknots_lower[i],bkgrdknots_lower[i],abs_expl[i]=-1000*np.ones([3,])
                bgcode.extend([4])
        bgknots_lower=filter(lambda a: a != -1000, bgknots_lower)
        bkgrdknots_lower=filter(lambda a: a != -1000, bkgrdknots_lower)
        abs_expl=filter(lambda a: a != -1000, abs_expl)

        if np.size(bgknots_lower)==0:
            bgknots_lower,bkgrdknots_lower,bg,abs_expl=np.ones([4,1])*np.NaN
            bgcode.extend([5])
        else:   
            for i in np.arange(0,np.shape(bgknots_lower)[0]):
                [y1,y2]=linpiecewise(params,[knots[bgknots_lower][i],knots[bkgrdknots_lower][i]])
                [m1,m2]=[slopes[bgknots_lower[i]],slopes[bkgrdknots_lower[i]]]
                [x1,x2]=[knots[bgknots_lower[i]],knots[bkgrdknots_lower[i]]]
                bg.extend([(y1-y2-(m1*x1-m2*x2))/(m2-m1)])
                
    else:
        bgknots_lower,bkgrdknots_lower,bg,abs_expl=np.ones([4,1])*np.NaN        
        bgcode.extend([3])
    if num_segments!=tot_segs:
        if np.size(bgcode)==0:
            bgcode=[1]
        else:
            for idx,val in enumerate(bgcode):
                bgcode[idx]=[1.+val/100.]

    return(params,knots,slopes,bgknots_lower,bkgrdknots_lower,bg,abs_expl,bgcode)
    

def readdata(inputvars,dark,ref,files,mthd):
    #Note the fourth value in the split will be the key for reffiles and the second value in the split will be the key for samples.

    dark_initialized=0
    ref_initialized=0
    data={};measurement_info={};col_heading={}
    if inputvars['reffilesmode']=='static':
        darkkey=dark.keys()[0]
        refkey=ref.keys()[0]
        ref_initialized=1
        dark_initialized=1
    
    print 'Reading data files and generating abs functions...'
    for idx,fil in enumerate(files):
        marker=os.path.split(fil)[1].split('_')[2]
        key=os.path.split(fil)[1].split('_')[0]
        if inputvars['reffilesmode']=='eval':    
            if marker not in dark.keys() and marker not in ref.keys():
                if dark_initialized!=1:
                    for fl in files[idx+1:]:
                        darkmarker=os.path.split(fl)[1].split('_')[2]                
                        if darkmarker in dark.keys():
                            darkkey=darkmarker
                            dark_initialized=1
                            break
                    if dark_initialized!=1:
                        print 'No dark reference file was provided'
                if ref_initialized!=1:
                    for fl in files[idx+1:]:
                        refmarker=os.path.split(fl)[1].split('_')[2]
                        if refmarker in ref.keys():                    
                            refkey=refmarker
                            ref_initialized=1
                            break
                    if ref_initialized!=1:
                        print 'No white reference file was provided'
            if marker in dark.keys():
                darkkey=marker
                dark_initialized=1
            if marker in ref.keys():
                refkey=marker
                ref_initialized=1
            if dark_initialized==1 and ref_initialized==1 and marker not in dark.keys() and marker not in ref.keys():
                measurement_info[key],data[key],col_heading[key]=readsignal(fil,darkkey,refkey,dark[darkkey]['av-raw'],ref[refkey]['av-raw'],mthd,excludecols=[inputvars['exclinitcols'],inputvars['exclfincols']],lower_wavelength=inputvars['lower_wavelength'],upper_wavelength=inputvars['upper_wavelength'],rowredscale=inputvars['rowredscale'],max_mthd_allowed=inputvars['max_mthd_allowed'])
                data[key]['fn']=fil
        elif inputvars['reffilesmode']=='static':
            if dark_initialized==1 and ref_initialized==1 and marker not in dark.keys()[0] and marker not in ref.keys()[0]:
                data[key]={};measurement_info[key]={};col_heading[key]={}
                measurement_info[key],data[key],col_heading[key]=readsignal(fil,darkkey,refkey,dark[darkkey]['av-raw'],ref[refkey]['av-raw'],mthd,excludecols=[inputvars['exclinitcols'],inputvars['exclfincols']],lower_wavelength=inputvars['lower_wavelength'],upper_wavelength=inputvars['upper_wavelength'],rowredscale=inputvars['rowredscale'],max_mthd_allowed=inputvars['max_mthd_allowed'],min_mthd_allowed=inputvars['min_mthd_allowed'])
                data[key]['fn']=fil
    return [measurement_info,data,col_heading]
    
def identifypeaks(data,keys,delta_1stderiv,max_allowed_2ndderiv):
    max2ndderivs={}
    peaksexist=[]
    for key in keys:
        max2ndderivs[key]=np.max(data[key]['abs_2ndderiv'])
        peakidxs=np.where(np.logical_and((np.abs(data[key]['abs_2ndderiv'])>=max_allowed_2ndderiv),(np.abs(data[key]['abs_1stderiv'])<=delta_1stderiv)))[0]
        if np.size(peakidxs)>0:
            peaksexist+=[key]
    return max2ndderivs,peaksexist

def runuvvis(search_dir,dstDir,inputvars,codeversion,recipeversion,analtypes,human):
    def listfiles(search_dir):
        fn1=lambda fn:os.path.join(search_dir,fn)
        files=filter(os.path.isfile,map(fn1,os.listdir(search_dir)))
        files=filter(lambda x: x.split('.')[-1]=='smp',files)
        files=filter(lambda x: len((os.path.basename(x)).split('_'))==3,files)
        return files
    t=time.time()
    if inputvars['mthd']=='TR':
        extns=['refl','trans']
    else:
        extns=['']
    files={};darkfiles={};reffiles={};darkcode={};refcode={}
    if inputvars['mthd']=='TR':
        files['trans']=listfiles(search_dir)
        files['refl']=listfiles(os.path.join(os.path.split(search_dir)[0],'R_UVVIS'))
    else:
        files['']=listfiles(search_dir)
        
    for extn in extns:
        mthd=inputvars['mthd'] if extn=='' else extn      
        darkfiles[extn],reffiles[extn],darkcode[extn],refcode[extn]=listreffiles(files[extn],dict(inputvars),mthd=mthd)

    inddark={};indref={};dark={};ref={};data={};measurement_info={};col_heading={}

    for extn in extns:
        [inddark[extn],indref[extn],dark[extn],ref[extn]]=readrefsignal(eval('files[extn]'),[inputvars['exclinitcols'],inputvars['exclfincols']],\
        reffilesmode=inputvars['reffilesmode'],darkfiles=eval('darkfiles[extn]'),reffiles=eval('reffiles[extn]'),lower_wavelength=inputvars['lower_wavelength'],\
        upper_wavelength=inputvars['upper_wavelength'],rowredscale=inputvars['rowredscale'],darkcode=darkcode[extn],\
        refcode=refcode[extn])  
        mthd=inputvars['mthd'] if extn=='' else extn      
        measurement_info[extn],data[extn],col_heading[extn]=readdata(inputvars,dark[extn],ref[extn],files[extn],mthd)
    treadfiles=time.time()-t   
    if inputvars['mthd']=='TR':
        analyze_keys=[key for key in data['trans'].keys() if key in data['refl'].keys()]
    else:
        analyze_keys=data[extn].keys()
#    analyze_keys=[7]
#    analyze_keys=[str(val) for val in analyze_keys]
    data,nankeys=mthd2abs(data,inputvars['mthd'],analyze_keys,inputvars['max_mthd_allowed'],inputvars['min_mthd_allowed'],inputvars['window_length'],inputvars['polyorder'])
    print 'Number of nankeys are:'+str(len(nankeys))

    print 'Verifying absorption spectrum for peaks...'
      
    if not os.path.exists(dstDir):
        os.mkdir(dstDir)


    for mydict in ['inddark','indref']:
        for extn in extns:
            fig=plt.figure()
            for idx,key in enumerate((eval(mydict)[extn]).keys()):
                ax=fig.add_subplot(111)
                
                ax.plot(eval(mydict)[extn][key]['av-raw'],label=str(key))
                ax.legend(prop={'size':2})
            plt.savefig(os.path.join(dstDir,mydict+'_'+extn+'.png'),dpi=300)
        plt.close('all')

    max2ndderivs,peaksexist=identifypeaks(data,analyze_keys,inputvars['delta_1stderiv'],inputvars['max_absolute_2ndderiv'])
    hist, bins = np.histogram(max2ndderivs.values(), bins=50)
    center=(bins[:-1]+bins[1:])/2
    width=0.7*(bins[1]-bins[0])
    plt.bar(center,hist,align='center',width=width)
    plt.draw()
    plt.savefig(os.path.join(dstDir,'max2ndderivs.png'),dpi=300)
    plt.close('all')
    
    print 'Number of samples with peaks in spectrum are:'+str(len(peaksexist))

    print 'done'
    
    code0='Successful assignment of bandgap linear segment using simple rules'
    code1='Linear segment with a slope less than min_slope was found'
    code2='Succesful assignment of bandgap linear segment using a slightly higher slope at following segment criterion but bgdiff > min in current segment'
    code3='No linear segment was observed for band gap'
    code4='Band gap linear segment(s) deleted due to inability to identify background linear segment with sufficient difference in slope'
    code5='All Band gap lin segs deleted due to inability to identify background linear segment with sufficient difference in slope'
    code6='Final segment has slope higher than previous and explains bgdiff>min this check occurs only when no band gap has been found with other criteria above'
#    There is a chance that you are underestimating band gaps
    code7='Peaks were found in the' + inputvars['mthd'] + 'spectrum'
    code8='NaNs were found in the absorption spectrum'
    code9='Linear fitting failed'
    
    tauc_pow={'DA':2.,'DF':2./3.,'IA':1./2.,'IF':1./3.}

    for key in analyze_keys:
        for types in ['DA','DF','IA','IF']:
            data[key][types]=(data[key]['abs']*data[key]['E'])**(tauc_pow[types])
            data[key][types]=data[key][types]/np.max(data[key][types])
            data[key][types+'_1stderiv']=savgol_filter(data[key][types], inputvars['window_length'], inputvars['polyorder'], delta=1.0, deriv=1)
            data[key][types+'_2ndderiv']=savgol_filter(data[key][types], inputvars['window_length'], inputvars['polyorder'], delta=1.0, deriv=2)
            data[key][types+'_unscaled']=(data[key]['abs_unscaled']*data[key]['E'])**(tauc_pow[types])



    print analtypes
    t=time.time()
    params,knots,slopes,bgknots,bkgrdknots,bg,abs_expl,bgcode,fitdata,tlinfit,tcalcbg=fitresult(data,analtypes,peaksexist,nankeys,analyze_keys,num_knots=inputvars['num_knots'],\
    tol=inputvars['tol'],min_allowedslope=inputvars['min_allowedslope'],min_bgTP_diff=inputvars['min_bgTP_diff'],min_bkgrdslope=inputvars['min_bkgrdslope'],\
    min_bgbkgrdslopediff=inputvars['min_bgbkgrdslopediff'],min_finseglength=inputvars['min_finseglength'],\
    merge_bgslopediff_percent=inputvars['merge_bgslopediff_percent'],min_TP_finseg_diff=inputvars['min_TP_finseg_diff'],\
    min_bgfinalseglength=inputvars['min_bgfinalseglength'],max_merge_differentialTP=inputvars['max_merge_differentialTP'],\
    merge_linsegslopediff_percent=inputvars['merge_linsegslopediff_percent'],maxtol=inputvars['maxtol'],plot=False,viewknots=True,min_knotdist=inputvars['min_knotdist'],xorder='increasing',\
    dispresult=False)
    t=time.time()-t
    print 'Time spent in math is:'+str(t)
    
    for typ in analtypes:
        hist, bins = np.histogram(np.array([np.min(params[key][typ]) for key in params.keys()]), bins=50)
        center=(bins[:-1]+bins[1:])/2
        width=0.7*(bins[1]-bins[0])
        plt.bar(center,hist,align='center',width=width)
        plt.draw()
        plt.savefig(os.path.join(dstDir,'minslopes_'+typ+'.png'),dpi=300)
        plt.close('all')
    
    uncompute={}
    for types in analtypes:
        uncompute[types]=[]
    for key in bg.keys():
        for types in analtypes:
            if np.size(bg[key][types])==1:
                if np.isnan(bg[key][types]):
                    if key not in peaksexist or nankeys:
                        uncompute[types].append(key)

                     
    for key in bg.keys():
        for types in analtypes:
            bg[key][types]=np.array(bg[key][types])
            abs_expl[key][types]=np.array(abs_expl[key][types])
            if not np.isnan(bg[key][types]).all():
                bg[key][types+'-repr']=bg[key][types][np.argmax(abs_expl[key][types][np.where(~np.isnan(abs_expl[key][types]))[0]])]
            else:
                bg[key][types+'-repr']=np.NaN
            if np.size(bg[key][types])==1 and bgcode[key][types][0]==0:
                bg[key][types+'-code0-only']=bg[key][types][0]
            else:
                bg[key][types+'-code0-only']=np.NaN
        
    for typ in analtypes:
        hist, bins = np.histogram(np.array([np.max(abs_expl[key][typ]) for key in abs_expl.keys()]), bins=50)
        center=(bins[:-1]+bins[1:])/2
        width=0.7*(bins[1]-bins[0])
        plt.bar(center,hist,align='center',width=width)
        plt.draw()
        plt.savefig(os.path.join(dstDir,'abs_expl_'+typ+'.png'),dpi=300)
        plt.close('all')
    
    addstr='_' if len(extns)>1 else ''
        
    for extn in extns:
        for key in bg.keys():
            if not key in measurement_info.keys():
                measurement_info[key]={}
            for key2 in eval('measurement_info[extn]')[key].keys():
                measurement_info[key][key2+addstr+extn]=eval('measurement_info[extn]')[key][key2]
            data[key]['fn']=data[extn][key]['fn']
                
#    print measurement_info.keys()
    for key in bg.keys():
        for extn in extns:
            measurement_info[key]['sample_no'+addstr+extn]=int(measurement_info[key].pop('Sample No'+addstr+extn))
        for key2 in ['sample_no','Plate ID']:
            if len(extns)>1:
                if measurement_info[key][key2+addstr+extns[0]]==measurement_info[key][key2+addstr+extns[1]]:
                    try:
                        measurement_info[key][key2]=int(measurement_info[key].pop(key2+addstr+extn))
                    except:
                        if key2 in ['sample_no','Plate ID']:
                            raise ValueError('A value is expected for '+ key2)  
                        else:
                            pass
            else:
                try:
                    measurement_info[key][key2]=int(measurement_info[key].pop(key2+addstr+extn))
                except:
                    if key2 in ['sample_no','Plate ID']:
                        raise ValueError('A value is expected for '+ key2)  
                    else:
                        pass

    numbgs={}
    
    for types in analtypes: 
        numbgs[types]=np.shape(bg[key][types])[0]
        for loc in np.arange(0,np.shape(bg[key][types])[0]):
            if np.isnan(np.array([bg[key][types][loc] for key in bg.keys()])).all():
                numbgs[types]=loc
                break

    
    print 'The destination directory is',dstDir   
    
    abs_fomranges=[(1.5,2.0),(2.0,2.5),(2.5,3.0)]
    for key in bg.keys():
            fom={}
            raw_arrays={}
            intermediate_arrays={}
            picklename= '_'.join(os.path.splitext(os.path.split(data[key]['fn'])[1])[0].split('_')[:-1]\
            +[time.strftime("%Y%m%d")+'.'+time.strftime("%H%M%S")])
            for types in analtypes:
                for curr_dict  in ['bg','bgcode','abs_expl']:
                    for loc in np.arange(0,numbgs[types]):
                        fom[types+'-'+curr_dict+'_'+str(loc)]=eval(curr_dict)[key][types][loc]
                fom[types+'-bg_repr']=bg[key][types+'-repr']
                fom[types+'-code0-only']=bg[key][types+'-code0-only']
#                print intermediate_arrays['rawselectinds']
                if not np.isnan(fitdata[key][types]).any():
                    intermediate_arrays['fitdata'+'-'+str(types)]=fitdata[key][types]
                
#                intermediate_arrays['leftdiff']=leftdiff[key]
#                intermediate_arrays['rightdiff']=rightdiff[key]
                for curr_dict in ['params','bgknots','bkgrdknots']:
                    intermediate_arrays[types+'-'+curr_dict]=eval(curr_dict)[key][types]
            
            savepath = os.path.join(dstDir, picklename+'.pck')

            fom['maxabsorp']=np.max(data[key]['abs_unscaled'])
            fom[inputvars['mthd']+'-min_rescaled']=int(data[key]['min_rescaled'])
            fom[inputvars['mthd']+'-max_rescaled']=int(data[key]['max_rescaled'])

            if inputvars['mthd']=='TR':
                extns=['trans','refl']
            else:
                extns=['']
            for lval,hval in abs_fomranges:
#                print np.where(np.logical_and(data[extn][key]['E']>=lval,data[extn][key]['E']<hval))[0]
                fom['abs_'+str(lval)+'-'+str(hval)]=np.sum(data[key]['abs_unscaled']\
                [np.where(np.logical_and(data[key]['E']>=lval,data[key]['E']<hval))[0]])
    
            fom['abs_max2ndderiv']=max2ndderivs[key]
            
            for extn in extns:
                
                for col in xrange(np.shape(eval('data[extn]')[key]['raw_unprocessed'])[1]):
                    raw_arrays[eval('col_heading[extn]')[key][col]+addstr+extn]=eval('data[extn]')[key]['raw_unprocessed'][:,col]
                for key2 in ['av-raw']:
                    intermediate_arrays[key2+addstr+extn]=data[extn][key][key2]
                if not extn=='':
                    intermediate_arrays[extn+'_unsmooth']=eval('data[extn]')[key][extn+'_unsmooth']
                intermediate_arrays['dark'+addstr+extn]=eval('dark[extn]')[eval('data[extn]')[key]['darkkey']]['av-raw']
                intermediate_arrays['ref'+addstr+extn]=eval('ref[extn]')[eval('data[extn]')[key]['refkey']]['av-raw']
            
            for key2 in [inputvars['mthd'],inputvars['mthd']+'_unsmooth','abs_unsmooth','abs_unscaled','abs_1stderiv','abs_2ndderiv']:
                intermediate_arrays[key2]=data[key][key2]
            intermediate_arrays['rawselectinds']=data[extn][key]['rawselectinds']

            if inputvars['mthd']=='TR':
                addnllist=['abs','E']+['TR_unscaled','TR']+analtypes+[x+'_1stderiv' for x in analtypes]\
                +[x+'_2ndderiv' for x in analtypes]+[x+'_unscaled' for x in analtypes]\
                +['1-T-R_unscaled','1-T-R_unsmooth']
            elif inputvars['mthd'] in ['trans','refl']:
                addnllist=['abs','E']+analtypes+[inputvars['mthd']+'_unscaled']+analtypes+[x+'_1stderiv' for x in analtypes] +[x+'_2ndderiv' for x in analtypes]
            else:
                raise ValueError('mthd should be either TR or refl or trans')
            for key2 in addnllist:
                intermediate_arrays[key2]=data[key][key2]
                
#                print intermediate_arrays.keys()

            with open(savepath,'wb') as pckfile:
                saveDict=dict([(k, v) for k, v in zip(\
                    ["version", "measurement_info", "fom", "raw_arrays", \
                    "intermediate_arrays", "function_parameters"], \
                    [codeversion, measurement_info[key], fom, raw_arrays, intermediate_arrays, inputvars])])
                pickle.dump(saveDict,pckfile)
                
                
    recipepath = os.path.join(dstDir,'recipefile')
    shutil.copyfile(inputvars['recipe_fl'],recipepath)
                         
    akey=bg.keys()[0]
    serial_num=str(measurement_info[akey]['Plate ID'])+str(np.mod(np.sum([int(x) for x in str(measurement_info[akey]['Plate ID'])]),10))
    csvfn=serial_num+'-'+'-c'+codeversion+'-r'+recipeversion+'-'+inputvars['mthd']+'.csv'
    dlmtr=','
    csvpath=os.path.join(dstDir,csvfn)
    with open(csvpath,'wb') as f:
        f.write('#description = "Optical %s measurement of %s band gaps"' %(human[inputvars['mthd']],'-'.join(analtypes))+'\r\n')      
        header=['sample_no']
        for types in analtypes:
            for curr_dict  in ['bg','bgcode','abs_expl']:
                for loc in xrange(numbgs[types]):
                    header+=[types+'-'+curr_dict+'_'+str(loc)]
            header+=[types+'-code0-only']
            header+=[types+'-'+'bg_repr']
                        
        for lval,hval in abs_fomranges:
            header+=['abs_'+str(lval)+'-'+str(hval)]
        header+=['maxabsorp']
        header+=[inputvars['mthd']+'-min_rescaled']
        header+=[inputvars['mthd']+'-max_rescaled']
        header+=['abs_max2ndderiv']
        
        header=dlmtr.join(header)
        f.write(header+'\r\n')
        
        for key in sorted(bg.keys()):
            nr=[measurement_info[key]['sample_no']]
            for types in analtypes:
                for loc in xrange(numbgs[types]):
                    for curr_dict  in ['bg','bgcode','abs_expl']:
                            nr+=[eval(curr_dict)[key][types][loc]]
                nr+=[bg[key][types+'-code0-only']]
                nr+=[bg[key][types+'-repr']]
            for lval,hval in abs_fomranges:
                nr+=[np.sum(data[key]['abs_unscaled']\
                [np.where(np.logical_and(data[key]['E']>=lval,data[key]['E']<hval))[0]])]
            nr+=[np.max(data[key]['abs_unscaled'])]
            nr+=[int(data[key]['min_rescaled'])]
            nr+=[int(data[key]['max_rescaled'])]
            nr+=[max2ndderivs[key]]
            nr=[str(x) for x in nr]
            nr=dlmtr.join(nr)
            nr=nr.replace('nan','NaN')
            f.write(nr+'\r\n')
                    
                
    grtrthanones=0;lessthanzeros=0;lessthanminallowed=0;grtrthanmaxallowed=0
    
    for key in bg.keys():
        if np.max(data[key][inputvars['mthd']+'_unscaled']>=1.):
            grtrthanones+=1
        if np.max(data[key][inputvars['mthd']+'_unscaled']>inputvars['max_mthd_allowed']):
            grtrthanmaxallowed+=1
        if np.max(data[key][inputvars['mthd']+'_unscaled']<=0.):
            lessthanzeros+=1
        if np.max(data[key][inputvars['mthd']+'_unscaled']<inputvars['min_mthd_allowed']):
            lessthanminallowed+=0
            
    savepath = os.path.join(dstDir,'logfile.txt')
    with open(savepath,'w') as f:
        for types in analtypes:
            f.write('Number of uncalculable bgs of type '+str(types)+' is '+str(np.size(uncompute[types]))+'\n')
        f.write('Number of samples that have peaks  in spectrum is:'+str(len(peaksexist))+'\n')
        f.write('Number of samples that have NaNs or out of bounds values in spectrum is:'+str(len(nankeys))+'\n')
        f.write('Number of samples with > 1 value of '+inputvars['mthd']+'_unscaled'+' is '+str(grtrthanones)+'\n')
        f.write('Number of samples with >'+str(inputvars['max_mthd_allowed'])+' value of '+inputvars['mthd']+'_unscaled'+' is '+str(grtrthanmaxallowed)+'\n')
        f.write('Number of samples with < 0 value of '+inputvars['mthd']+'_unscaled'+' is '+str(lessthanzeros)+'\n')
        f.write('Number of samples with <'+str(inputvars['min_mthd_allowed'])+' value of '+inputvars['mthd']+'_unscaled'+' is '+str(lessthanminallowed))
        f.write('\nCode used is '+inspect.getfile(inspect.currentframe()))
    print 'time for reading files is:'+str(treadfiles)
    print 'time for linear fitting is:'+str(tlinfit)
    print 'time for calculating band gap is:'+str(tcalcbg)
        
#    string=''
#    for types in analtypes:
#        string+='Number of uncalculable bgs of type '+str(types)+' is '+str(np.size(uncompute[types]))+'\n'
#        string+='Number of samples that have peaks  in spectrum is:'+str(len(peaksexist))+'\n'
#        string+='Number of samples that have NaNs or out of bounds trans and refl values in spectrum is:'+str(len(nankeys))+'\n'
#    string+='Number of samples with > 1 value of '+inputvars['mthd']+'_unscaled'+' is '+str(grtrthanones)+'\n'
#    string+='Number of samples with >'+str(inputvars['max_mthd_allowed'])+' value of '+inputvars['mthd']+'_unscaled'+' is '+str(grtrthanmaxallowed)+'\n'
#    string+='Analysis time ='+str(time.time()-starttime)
#    tkMessageBox.showinfo(message='Analysis Complete'+'\n'+string)

