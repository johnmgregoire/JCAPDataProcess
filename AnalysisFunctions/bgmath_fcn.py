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
import shutil

def residuals(params,xdata,ydata): return sum((np.abs(ydata-linpiecewise(params,xdata))/ydata)**2)
#Division by ydata is to ensure that errors at low absorbance values are given high importance and the ones
#at higher absorbance values are given lower importance (since the important region is where the absorbance starts increasing
#from low value prior to band gap to higher values...The noise at very high energy levels usually having high absorbance will not 
#effect the quality of the result a lot)

   
# params: zeroth index corresponds to the yfit value at x=x0. Next num_knots indices correspond to the knot positions. Next num_knots-1 indices correspond
#to slopes for the linear regions.  Piecewise linear addition to obtain the value of fitdata at a specific value of x. 
def linpiecewise(y0,knots,slopes,x):
    fitdata=y0
    for loc in np.arange(0,np.size(knots)-1):
        fitdata+=slopes[loc]*(x>=(knots[loc]-0.0001))*(np.min(knots[loc+1],x)-(knots[loc]))
    return fitdata

#xorder: if loc in data represents smaller value of energy to higher value of energy then xorder is increasing otherwise decreasing
#first constraint in cons is to ensure minimum knot distance min_knotdist. Second equality constraint indicates that the first and the last knot are fixed to the first and last values of x
#Initially knot locations are evenly spread out between xvalues of interest and all slopes are set to zero. tolerance is the tolerance for convergence of linear properties.

def linearfit(xdata,ydata,num_knots,min_knotdist,xorder,options,tol):
    if xorder=='increasing': sign=1
    elif xorder=='decreasing': sign=-1
    locs=np.arange(1,num_knots+1)
    cons=({'type':'ineq','fun':lambda params: params[locs[0:-1]+1]*sign-(params[locs[0:-1]]*sign+min_knotdist)},\
    {'type':'eq','fun':lambda params: np.array([params[1],params[num_knots]])-np.array([xdata[0],xdata[-1]],)})
    init_params=np.hstack((ydata[0],np.arange(xdata[0],xdata[-1]+10.**(-4),(xdata[-1]-xdata[0])/(num_knots-1))\
    ,np.ones(num_knots-1)*(ydata[-1]-ydata[0])/(xdata[-1]-xdata[0])))
    res = sp.optimize.minimize(residuals,init_params, args=(xdata,ydata),constraints=cons, method='SLSQP',options=options,tol=tol)
    return res
    
def mergelinsegs(params,num_knots,max_merge_differentialTP,merge_linsegslopediff_percent):
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
            medianslope=(newslopes[j]*(newknots[j+1]-newknots[j])+slopes[loc+1]*(knots[loc+2]-knots[loc+1]))\
            /(knots[loc+2]-newknots[j])
            differentialTPdiff=(medianslope-newslopes[j])*(newknots[j+1]-newknots[j])
            TPdiff=newslopes[j]*(newknots[j+1]-newknots[j])
            TPdiffn=slopes[loc+1]*(knots[loc+2]-knots[loc+1])
            if abs(differentialTPdiff)<min(max_merge_differentialTP,merge_linsegslopediff_percent*(TPdiff+TPdiffn)):
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
def fitresult(data,bgtyp,max_numbgs,num_knots,tol,min_allowedslope,min_bgTP_diff,min_bkgrdslope,min_bgbkgrdslopediff,\
min_finseglength,merge_bgslopediff_percent,min_TP_finseg_diff,min_bgfinalseglength,max_merge_differentialTP,\
merge_linsegslopediff_percent,maxtol,min_knotdist=0.05,xorder='increasing',dispresult=False):
    linfitd={}
    yoffset=-np.min(data[bgtyp])+0.03 if np.min(data[bgtyp])<0.03 else 0
    for maxiter in [1000,2000]:
        res=linearfit(data['E'],data[bgtyp]+yoffset,num_knots,min_knotdist,xorder,{'maxiter':maxiter,'disp':dispresult},tol)
        if res.success:
            break
    if not res.success:
        maxiter=2000
        for i in xrange(int(np.log10(tol)),int(np.log10(maxtol))+1,-1):
            newtol=10.**i
            res=linearfit(data['E'],data[bgtyp]+yoffset,num_knots,min_knotdist,xorder,{'maxiter':maxiter,'disp':dispresult},newtol)
            if res.success:
                break
    if not res.success:
        return [{},{'bgcode_0':9}]
    else:
        tempparams=res.x             
        tempparams[0]-=yoffset
        tempparams=mergelinsegs(tempparams,num_knots,max_merge_differentialTP,merge_linsegslopediff_percent)
        linfitd,fomd=calc_bandgap(tempparams,np.size(tempparams)/2,min_allowedslope,\
        min_bgTP_diff,min_bkgrdslope,min_bgbkgrdslopediff,min_finseglength,merge_bgslopediff_percent,\
        min_TP_finseg_diff,min_bgfinalseglength)
        data['linfit']=linpiecewise(linfitd['y0'],linfitd['knots'],linfitd['slopes'],data['E'])
        fomd['bg_repr']=fomd['bg_'+str(np.argmax([fomd['abs_expl_'+str(idx)] for idx \
        in xrange(max_numbgs) if not np.isnan(fomd['abs_expl_'+str(idx)])]))]
        fomd['bgcode0-only']=fomd['bg_0'] if fomd['bgcode_1']==np.nan and fomd['bgcode_0']==0 else np.NaN
    return [linfitd,fomd]
            
def calc_bandgap(params,num_knots,max_numbgs,min_allowedslope,min_bgTP_diff,min_bkgrdslope,min_bgbkgrdslopediff,\
min_finseglength,merge_bgslopediff_percent,min_TP_finseg_diff ,min_bgfinalseglength):
    if merge_bgslopediff_percent>1:
        merge_bgslopediff_percent=merge_bgslopediff_percent/100
    knots=params[1:num_knots+1]
    slopes=params[num_knots+1:2*num_knots]
    num_slopes=np.shape(slopes)[0]
    bgknots_lower=[]; bkgrdknots_lower=[]; bg=[]; abs_expl=[]; bgcode=[]
    if (knots[num_slopes]-knots[num_slopes-1])>=min_finseglength:
        num_segments=num_slopes
    else:
        num_segments=num_slopes-1
    tot_segs=num_segments
    for i in np.arange(0,tot_segs-1):
        if slopes[i]<min_allowedslope:
            num_segments=i+1
#THERE COULD BE SOME PROBLEM HERE REVISIT
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
            bgknots_lower,bkgrdknots_lower,bg,abs_expl=np.ones([max_numbgs,1])*np.NaN
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
                
    fomd=dict([(lstk+'_'+str(idx),eval(lstk)[idx]) for lstk in ['bgknots_lower', \
    'bkgrdknots_lower', 'bg','abs_expl','bgcode'] for idx in xrange(max_numbgs)])
    linfitd=dict(dict([(lstk+'_'+str(idx),eval(lstk)[idx]) for lstk in ['bgknots_lower', \
    'bkgrdknots_lower'] for idx in xrange(max_numbgs)]),knots=knots,slopes=slopes,y0=params[0])
    return [linfitd,fomd]
    

    
def identifypeaks(data,typ,delta_1stderiv,max_allowed_2ndderiv):\
return len(np.where(np.logical_and((np.abs(data[typ+'_2ndderiv'])>=max_allowed_2ndderiv),\
(np.abs(data[typ+'_1stderiv'])<=delta_1stderiv)))[0])>0


def runuvvis(data,inputvars,fomnames):
#    Energy should be part of the initial intermediate data since this is needed for visualization
    data['E']=1239.8/data['wl']
#####
    bgtyp=inputvars['analtypes'][0]
    if np.isnan(data[bgtyp]).any():
        return [{'DA-bgcode_0':8},{}]
#Implementation of second round of filtering in cases where peaks exist is currently unsupported
    if identifypeaks(data,'abs',inputvars['delta_1stderiv'],inputvars['max_absolute_2ndderiv']):
        return [{'DA-bgcode_0':7},{}]
    
    code0='Successful assignment of bandgap linear segment using simple rules'
    code1='Linear segment with a slope less than min_slope was found'
    code2='Succesful assignment of bandgap linear segment using a slightly higher slope at following segment criterion but bgdiff > min in current segment'
    code3='No linear segment was observed for band gap'
    code4='Band gap linear segment(s) deleted due to inability to identify background linear segment with sufficient difference in slope'
    code5='All Band gap lin segs deleted due to inability to identify background linear segment with sufficient difference in slope'
    code6='Final segment has slope higher than previous and explains bgdiff>min this check occurs only when no band gap has been found with other criteria above'
#    There is a chance that you are underestimating band gaps
    code7='Peaks were found in the mthd spectrum'
    code8='NaNs were found in the absorption spectrum'
    code9='Linear fitting failed'
    
    linfitd,fomd=fitresult(data,bgtyp,\
    num_knots=inputvars['num_knots'],tol=inputvars['tol'],min_allowedslope=inputvars['min_allowedslope'],\
    min_bgTP_diff=inputvars['min_bgTP_diff'],min_bkgrdslope=inputvars['min_bkgrdslope'],\
    min_bgbkgrdslopediff=inputvars['min_bgbkgrdslopediff'],min_finseglength=inputvars['min_finseglength'],\
    merge_bgslopediff_percent=inputvars['merge_bgslopediff_percent'],min_TP_finseg_diff=inputvars['min_TP_finseg_diff'],\
    min_bgfinalseglength=inputvars['min_bgfinalseglength'],max_merge_differentialTP=inputvars['max_merge_differentialTP'],\
    merge_linsegslopediff_percent=inputvars['merge_linsegslopediff_percent'],maxtol=inputvars['maxtol'],\
    min_knotdist=inputvars['min_knotdist'],xorder='increasing',dispresult=False)

    for dct in ['linfitd','fomd']:    
        for key in eval(dct).keys():
            if bgtyp not in key:
                dct[bgtyp+'-'+key]=eval(dct).pop(key)
    return linfitd,fomd
