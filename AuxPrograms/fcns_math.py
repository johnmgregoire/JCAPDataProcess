import numpy, scipy, scipy.optimize, scipy.interpolate
import os, os.path, time, copy, pylab, operator
from scipy import interp
import matplotlib.pyplot as plt

def myeval(c):
    if c=='None':
        c=None
    elif c=='nan' or c=='NaN':
        c=numpy.nan
    else:
        temp=c.lstrip('0')
        if (temp=='' or temp=='.') and '0' in c:
            c=0
        else:
            c=eval(temp)
    return c
    

def get_dict_item_keylist(d, keylist):
    return reduce(lambda d, k: d[k], keylist, d)
    
def removeoutliers_meanstd(arr, nptsoneside, nsig, gapptsoneside=0): #avrages maximum of 2*nptoneside points and usees distance from mean scaled by std compared to nsig to determine if the value should be replaced by the mean. if gapptsoneside>0, will do this leaving a gap around the point in question and using nptsoneside-gaps points for the mean and std
    if nptsoneside==1 and gapptsoneside==0:
        return removesinglepixoutliers(arr, critratiotoneighbors=nsig)
    nsig=max(nsig, 1.)
    nptsoneside=max(nptsoneside, 2.)
    gapptsoneside=min(gapptsoneside, nptsoneside-2.)
    for gap in range(gapptsoneside+1):
        starti=numpy.uint32([max(i-(nptsoneside-gap), 0) for i in range(len(arr))])
        stopi=numpy.uint32([min(i+(nptsoneside-gap)+1, len(arr)) for i in range(len(arr))])
        #print [numpy.append(arr[i0:i], arr[i+1:i1]) for i, i0, i1 in zip(range(len(arr)), starti, stopi)][8]
        #print [(((numpy.append(arr[i0:i], arr[i+1:i1]).mean()-arr[i]))**2, (numpy.append(arr[i0:i], arr[i+1:i1]).std()*nsig)**2) for i, i0, i1 in zip(range(len(arr)), starti, stopi)][8]
        arr=numpy.array([(((numpy.append(arr[i0:i], arr[i+1:i1]).mean()-arr[i]))**2<(numpy.append(arr[i0:i], arr[i+1:i1]).std()*nsig)**2 and (arr[i],) or (numpy.append(arr[i0:i], arr[i+1:i1]).mean(),))[0] for i, i0, i1 in zip(range(len(arr)), starti, stopi)], dtype=arr.dtype)
    return arr
    
def CalcArrSS(x, WeightExp=1., TestPts=10):
    p=WeightExp
    i=TestPts
    s0=x[:i].std()/i**p+1
    while x[:i].std()/i**p<s0 and i<len(x):
        s0=x[:i].std()/i**p
        i+=TestPts
    return x[:i].mean()


def xx(x, WeightExp=1., TestPts=10):
    p=WeightExp
    i=TestPts
    s0=x[:i].std()/i**p+1
    while x[:i].std()/i**p<s0 and i<len(x):
        s0=x[:i].std()/i**p
        i+=TestPts
    return i
    
def concat_extrap_ends(x, npts, polyorder=1, lowside=True, highside=True):
    i=numpy.arange(npts, dtype='float64')
    if lowside:
        ans=scipy.polyfit(-1*(i+1.), x[:npts], polyorder)
        x=numpy.concatenate([scipy.polyval(list(ans), i[::-1]), x])
    if highside:
        ans=scipy.polyfit(-1*(i[::-1]-1.), x[-1*npts:], polyorder)
        x=numpy.concatenate([x, scipy.polyval(list(ans), i)])
    return x    
    
def lininterpbetweenregularpoints(existy, interval):
    existy=numpy.array(existy)
    x=numpy.arange(interval,dtype='float32')/interval
    diff=existy[1:]-existy[:-1]
    o=numpy.outer(diff,x)
    return numpy.concatenate([arr+start for arr,start in zip(o,existy[:-1])]+[existy[-1:]])
    
def interpwithinarr(existind, existy, order=3, interpplotax=None, interpcols=['k', 'r']):
    if order==1:
        existind=numpy.array(existind)
        diff=existind[1:]-existind[:-1]
        if numpy.all(diff==diff[0]):
            return lininterpbetweenregularpoints(existy, diff[0])
    interind=sorted(list(set(numpy.arange(max(existind)+1))-set(existind)))
    yfull=numpy.zeros(max(existind)+1, existy.dtype)
    yfull[existind]=existy[:]
    yfull[interind]=scipy.interpolate.spline(existind, existy, interind, order=order)
    if not interpplotax is None:
        interpplotax.plot(existind, existy, interpcols[0])
        interpplotax.plot(interind,  yfull[interind], interpcols[1])
    return yfull
    
def savgolsmooth(x, nptsoneside=7, order = 4, dx=1.0, deriv=0, binprior=0): #based on scipy cookbook. x is 1-d array, window is the number of points used to smooth the data, order is the order of the smoothing polynomial, will return the smoothed "deriv"th derivative of x
    if nptsoneside<=1:
        return x
    if binprior>1:
        origlen=len(x)
        x=numpy.array([x[i*binprior:(i+1)*binprior].mean() for i in range(origlen//binprior)])
        dx*=binprior
    side=numpy.uint16(max(nptsoneside, numpy.ceil(order/2.)))
    s=numpy.r_[2*x[0]-x[side:0:-1],x,2*x[-1]-x[-2:-1*side-2:-1]]
    # a second order polynomal has 3 coefficients
    b = numpy.mat([[k**i for i in range(order+1)] for k in range(-1*side, side+1)])
    m = numpy.linalg.pinv(b).A[deriv] #this gives the dth ? of the base array (.A) of the pseudoinverse of b

    # precompute the offset values for better performance
    offsets = range(-1*side, side+1)
    offset_data = zip(offsets, m)

    smooth_data=[numpy.array([(weight * s[i + offset]) for offset, weight in offset_data]).sum() for i in xrange(side, len(s) - side)]
    smooth_data=numpy.array(smooth_data)/(dx**deriv)
    
    if binprior>1:    
        ia=numpy.arange(binprior, dtype='float32')/binprior
        xr=numpy.concatenate([ia*(b-a)+a for a, b in zip(smooth_data[:-1], smooth_data[1:])])
        xr=numpy.concatenate([(smooth_data[1]-smooth_data[0])*ia[:binprior//2]+smooth_data[0], xr, (smooth_data[-1]-smooth_data[-2])*ia[:binprior//2]+smooth_data[-1]])
        smooth_data=numpy.concatenate([xr, (smooth_data[-1]-smooth_data[-2])*ia[:origlen-len(xr)]+smooth_data[-1]])


    return smooth_data

class fitfcns: #datatuples are x1,x2,...,y
    #.finalparams .sigmas .parnames useful, returns fitfcn(x)
    def genfit(self, fcn, initparams, datatuple, markstr='unspecified', parnames=[], interaction=0,  maxfev=2000, weights=None, optimizerfcn=None):
        self.maxfev=maxfev
        self.performfit=True
        self.initparams=initparams
        self.sigmas=scipy.zeros(len(initparams))
        self.parnames=parnames
        self.finalparams=initparams
        self.error=False
        if weights is None:
            def wts(x):
                return 1.
        elif weights=='parabolic':
            a=(datatuple[0][0]+datatuple[0][-1])/2.0
            b=(datatuple[0][-1]-datatuple[0][0])/2.0
            def wts(x):
                return 1.0+((x-a)/b)**2

        def res1(p, x1, y):
            return (y-fcn(p, x1))*wts(x1)

        def res2(p, x1,x2,y):
            return y-fcn(p, x1, x2)

        def res3(p, x1,x2,x3, y):
            return y-fcn(p, x1, x2, x3)

        def res4(p, x1,x2,x3,x4,  y):
            return y-fcn(p, x1, x2, x3, x4)

        resdic={1:res1,  2:res2,  3:res3,  4:res4}
        self.resfcn=resdic[len(datatuple)-1]
        i=0
        for arr in datatuple:  #if the numerical data is given as a list or tuple then convert to arrays. regardless convert to float64 because leastsq REQUIRES THIS
            datatuple=datatuple[0:i]+tuple([numpy.float64(arr)])+datatuple[i+1:]
            i=i+1
        while self.performfit:
            self.sigmas=scipy.zeros(len(self.finalparams))
            if not optimizerfcn is None:
                try:
                    self.finalparams=optimizerfcn(self.resfcn,self.initparams, args=datatuple, maxfun=self.maxfev, xtol=1.e-10, ftol=1.e-10)
                    self.error=0
                except:
                    self.error=1
            else:
                fitout = scipy.optimize.leastsq(self.resfcn,self.initparams, args=datatuple, maxfev=self.maxfev, full_output=1)#, warning=False)
                self.performfit=False
                self.finalparams=fitout[0]
                if not fitout[4] in [1, 2]:
                    print 'Fitting Error ', fitout[4], ' at ', markstr,': ', fitout[3]
                    self.error=True
                else:
                    #self.finalparams=fitout[0]
                    self.covmat=fitout[1]
                    try:
                        self.sigmas=scipy.array([self.covmat[i, i] for i in range(len(self.sigmas))])
                    except:
                        pass

        def fitfcn(x):
            return fcn(self.finalparams, x)
        return fitfcn

    def poly(self, p, x):#both must be numpy arrays
        return numpy.array([p[i]*(x**i) for i in range(p.size)]).sum(0)

    def polyfit(self, datatuple, initparams, markstr='unspecified', interaction=0,  maxfev=2000, weights=None):
        #initparams can be an array of coefficients [constant,lin term, quad term,...] or an integer indicating the order of the polynomial
        if isinstance(initparams, int):
            initparams=numpy.ones(initparams+1)
        else:
            initparams=numpy.float64(initparams)
        parnames=[]
        i=0
        for par in initparams:
            parnames+=[''.join(('coef', `i`))]
            i+=1

        return self.genfit(self.poly, initparams, datatuple, markstr, parnames, interaction, maxfev, weights=weights)


    def gaussianfit(self, datatuple, initparams=scipy.array([1, 0, 1]), markstr='unspecified', interaction=0, showplot=True, maxfev=2000, weights=None):
        return self.genfit(self.gaussian, initparams, datatuple, markstr, parnames=['coef', 'center', 'sigma'], interaction=interaction, maxfev=maxfev, weights=weights)

    def gaussian(self, p, x):
        return p[0]*scipy.exp(-0.5*((x-p[1])/p[2])**2)

    def lorentzianfit(self, datatuple, initparams=scipy.array([1, 0, 1]), markstr='unspecified', interaction=0, showplot=True, maxfev=2000, weights=None):
        return self.genfit(self, self.lorentzian, initparams, datatuple, markstr, parnames=['coef', 'center', 'gamma'], interaction=interaction, maxfev=maxfev, weights=weights)

    def lorentzian(self, p, x):
        return (p[0]/scipy.pi)*p[2]/((x-p[1])**2+p[2]**2)

def Gaussian(pars, x):
    return pars[2]*numpy.exp(-0.5*((x-pars[0])/pars[1])**2) 

def Lorentzian(pars, x):#defined in nontraditional way so that pars[2] is the peak height
    return pars[2]/(1+((x-pars[0])/pars[1])**2)

def GaussLorentz(pars, x):
    gw=min(max(pars[3], 0.), 1.)
    return gw*Gaussian(pars, x)+(1.-gw)*Lorentzian(pars, x)
    
def GaussHalfLorentz(pars, x):
    return .5*Gaussian(pars, x)+.5*Lorentzian(pars, x)

PeakFcnLibrary={'Gaussian':Gaussian, 'Lorentzian':Lorentzian, 'GaussHalfLorentz':GaussHalfLorentz}

def fitpeakset(X, Y, initpars, peakfcn, negpeaks=True, optimizerfcn=None, nsigcut=3.):#peak function must be a function that accepts a list of 3 parameters (the reshape 3 needs to be changed if num params differs)
    numgauss=len(initpars)
    if numgauss==0:
        return (numpy.float32([]), numpy.float32([]), 0.)
    if nsigcut is None:
        imin=0
        imax=len(X)
    else:
        xmin=initpars[0][0]
        xmax=initpars[0][0]
        for p, w, h in initpars:
            xmin=min(xmin, p-w*nsigcut)
            xmax=max(xmax, p+w*nsigcut)
        imin=numpy.argmin((X-xmin)**2)
        imax=numpy.argmin((X-xmax)**2)
    
    zeroedpeakinds=[]
    repeatwithpkremoved=True #peaks are removed if their fitted height is <0. At the end, these peaks are added to the fit parameter list with 0 height and 0 error
    while repeatwithpkremoved:
        initparscpy=copy.copy(list(initpars))
        for pkind in reversed(zeroedpeakinds):#reverse so opo gets the right index
            initparscpy.pop(pkind)
        if len(initparscpy)==0:
            break
        initparsflat=numpy.float64(initparscpy).flatten()
        def fitfcn(p, x):
            allpars=numpy.reshape(p, (p.size//initpars.shape[1], initpars.shape[1]))
            if isinstance(x, numpy.ndarray):
                val=numpy.zeros(x.size, dtype='float32')
            else:
                val=0.0
            for pars in allpars:
                val+=peakfcn(pars, x)
            return val
#        def residfcn(p, x, y):
#            err=y-fitfcn(p, x)
#            return err
        Ya=numpy.float64(Y[imin:imax])
        Xa=numpy.float64(X[imin:imax])
        
        #if not optimizerfcn is None:
        ff=fitfcns()
        ff.genfit(fitfcn, initparsflat, (Xa, Ya), optimizerfcn=optimizerfcn)
        finalparams=ff.finalparams
#        else:
#            fitout=scipy.optimize.leastsq(residfcn, initparsflat, args=(X, Y), full_output=1)
#            if not (fitout[4] in [1, 2]):
#                print 'Fitting Error', fitout[4],': ', fitout[3]
#            finalparams=numpy.float32(fitout[0])
        finalparamsshaped=numpy.reshape(finalparams, (len(finalparams)//initpars.shape[1], initpars.shape[1]))
        if negpeaks:
            repeatwithpkremoved=False
        else:
            negpeakinds=numpy.where(finalparamsshaped[:, 2]<0)[0]
            zeroedpeakinds+=list(negpeakinds)
            zeroedpeakinds.sort()
            repeatwithpkremoved=len(negpeakinds)>0
#        print '^^^^^^^^^^^^^^^'
#        print initparsflat
#        print finalparamsshaped
#        pylab.plot(X, Y, 'b.')
#        pylab.show()
#    if not (fitout[1] is None):
#        covmat=fitout[1]
#        sigmas=numpy.float32([covmat[i, i] for i in range(len(finalparams))])
#    else:
#        print 'COVARIANCE NOT CALCULATED:', fitout[4],': ', fitout[3]
#        sigmas=numpy.zeros(len(finalparams), dtype='float32')
        sigmas=ff.sigmas
    finalresid=numpy.sqrt((ff.resfcn(finalparams, X, Y)**2).sum())
    #pylab.plot(X, Y, 'k.', X, fitfcn(finalparams, X), 'r-')

    sigmashaped=numpy.reshape(sigmas, (len(finalparams)//initpars.shape[1], initpars.shape[1]))
    for pkind in zeroedpeakinds:
        finalparamsshaped=list(finalparamsshaped)
        sigmashaped=list(sigmashaped)
        temp=copy.copy(initpars[pkind][:])
        temp[2]=0.#zero the height
        finalparamsshaped.insert(pkind, temp)
        sigmashaped.insert(pkind, numpy.zeros(initpars.shape[1], dtype='float64'))
        finalparamsshaped=numpy.float64(finalparamsshaped)
        sigmashaped=numpy.float64(sigmashaped)
    return (finalparamsshaped, sigmashaped, finalresid)
    
def arrayzeroind1d(arr, postoneg=False, negtopos=True):
    sarr=numpy.sign(arr)
    if postoneg:
        zeroind=numpy.where(sarr[:-1]>sarr[1:])[0]
        if negtopos:
            zeroind=numpy.append(zeroind, numpy.where(sarr[:-1]*sarr[1:]<=0)[0])
    else:#assume that if not postoneg then negtopos
        zeroind=numpy.where(sarr[:-1]*sarr[1:]<=0)[0]
    return (1.0*zeroind*arr[(zeroind+1,)]-(zeroind+1)*arr[(zeroind,)])/(arr[(zeroind+1,)]-arr[(zeroind,)]) #returns array of the floating point "index" linear interpolation between 2 indeces

def clustercoordsbymax1d(arr, pkind, critsepind):#results will be sorted. wherever there are peak indeces too close together. the peak index next to the peak index with highest arr value gets removed
    pkind.sort()
    indindslow=numpy.where((pkind[1:]-pkind[:-1])<critsepind)[0]
    indindshigh=indindslow+1
    while indindslow.size>0:
        maxindindindlow=numpy.nanargmax(arr[pkind[(indindslow,)]])
        maxindindindhigh=numpy.nanargmax(arr[pkind[(indindshigh,)]])
        if arr[pkind[indindslow[maxindindindlow]]]>arr[pkind[indindshigh[maxindindindhigh]]]:
            pkind=numpy.delete(pkind, indindshigh[maxindindindlow])
        else:
            pkind=numpy.delete(pkind, indindslow[maxindindindhigh])

        indindslow=numpy.where((pkind[1:]-pkind[:-1])<critsepind)[0]
        indindshigh=indindslow+1
    return pkind
    
def peaksearch1dSG(x, dx=1., critpeakheight=10, critsepind=5, critcurve=None, firstdernpts=7, firstderorder=1, secdernpts=14, secderorder=1, pospeaks=True, negpeaks=True):
    #dx is delta q for one index. zeros of the first derivative of inn are grouped together if within critsepind. only negative slope in the firstder is used so no secder is necessary unless specify a critical curvature in count nm^2
    if not (pospeaks or negpeaks):
        return numpy.float32([])
    ifirstder=savgolsmooth(x, nptsoneside=firstdernpts, order=firstderorder, dx=dx, deriv=1)
    fullpkind=numpy.float32([])
    if pospeaks:
        zeroind=arrayzeroind1d(ifirstder, postoneg=True, negtopos=False)
        temp=numpy.where(x[(numpy.uint32(numpy.round(zeroind)),)]>critpeakheight)
        fullpkind=numpy.append(fullpkind, zeroind[temp])
    if negpeaks:
        zeroind=arrayzeroind1d(ifirstder, postoneg=False, negtopos=True)
        temp=numpy.where(x[(numpy.uint32(numpy.round(zeroind)),)]<(-1*critpeakheight))
        fullpkind=numpy.append(fullpkind, zeroind[temp])
        
    if fullpkind.size==0:
        return fullpkind
    pkind=clustercoordsbymax1d(x, numpy.uint32(numpy.round(fullpkind)), critsepind)
    if critcurve is not None:
        isecder=savgolsmooth(x, nptsoneside=secdernpts, order=secderorder, dx=dx, deriv=2)
        temp=numpy.where(numpy.abs(isecder[(numpy.uint32(numpy.round(pkind)),)])>(critcurve))
        pkind=numpy.array(pkind)[temp]
#    pkind=list(pkind)
#    pkind.reverse()#highest to smallest for pairing below
    return numpy.array(pkind, dtype=numpy.float32)
    
def removeoutliers_meanstd(arr, nptsoneside, nsig, gapptsoneside=0): #avrages maximum of 2*nptoneside points and usees distance from mean scaled by std compared to nsig to determine if the value should be replaced by the mean. if gapptsoneside>0, will do this leaving a gap around the point in question and using nptsoneside-gaps points for the mean and std
    if nptsoneside==1 and gapptsoneside==0:
        return removesinglepixoutliers(arr, critratiotoneighbors=nsig)
    nsig=max(nsig, 1.)
    nptsoneside=max(nptsoneside, 2.)
    gapptsoneside=min(gapptsoneside, nptsoneside-2.)
    for gap in range(gapptsoneside+1):
        starti=numpy.uint32([max(i-(nptsoneside-gap), 0) for i in range(len(arr))])
        stopi=numpy.uint32([min(i+(nptsoneside-gap)+1, len(arr)) for i in range(len(arr))])
        #print [numpy.append(arr[i0:i], arr[i+1:i1]) for i, i0, i1 in zip(range(len(arr)), starti, stopi)][8]
        #print [(((numpy.append(arr[i0:i], arr[i+1:i1]).mean()-arr[i]))**2, (numpy.append(arr[i0:i], arr[i+1:i1]).std()*nsig)**2) for i, i0, i1 in zip(range(len(arr)), starti, stopi)][8]
        arr=numpy.array([(((numpy.append(arr[i0:i], arr[i+1:i1]).mean()-arr[i]))**2<(numpy.append(arr[i0:i], arr[i+1:i1]).std()*nsig)**2 and (arr[i],) or (numpy.append(arr[i0:i], arr[i+1:i1]).mean(),))[0] for i, i0, i1 in zip(range(len(arr)), starti, stopi)], dtype=arr.dtype)
    return arr

def removesinglepixoutliers(arr,critratiotoneighbors=1.5):
    c=numpy.where((arr[1:-1]>(critratiotoneighbors*arr[:-2]))*(arr[1:-1]>(critratiotoneighbors*arr[2:])))
    c0=c[0]+1
    #print len(c0), ' pixels being replaced'
    arr[c0]=(arr[c0-1]+arr[c0+1])/2
    return arr

def clustercoordsbymax1d(arr, pkind, critqsepind):#results will be sorted. wherever there are peak indeces too close together. the peak index next to the peak index with highest arr value gets removed
    pkind.sort()
    indindslow=numpy.where((pkind[1:]-pkind[:-1])<critqsepind)[0]
    indindshigh=indindslow+1
    while indindslow.size>0:
        maxindindindlow=numpy.argmax(arr[pkind[(indindslow,)]])
        maxindindindhigh=numpy.argmax(arr[pkind[(indindshigh,)]])
        if arr[pkind[indindslow[maxindindindlow]]]>arr[pkind[indindshigh[maxindindindhigh]]]:
            pkind=numpy.delete(pkind, indindshigh[maxindindindlow])
        else:
            pkind=numpy.delete(pkind, indindslow[maxindindindhigh])

        indindslow=numpy.where((pkind[1:]-pkind[:-1])<critqsepind)[0]
        indindshigh=indindslow+1
    return pkind
    


def findlinearsegs(y, dydev_frac,  dydev_nout, dn_segstart,  SGnpts=10, plotbool=False, dx=1., dydev_abs=0., maxfracoutliers=.5, critdy_fracmaxdy=None, critdy_abs=None, npts_SGconstdy=2):
    if 2*npts_SGconstdy+dydev_nout>=len(y):
        print 'array not long enough to find linear segments'
        return [], [], [], [], []
    dy=savgolsmooth(y, nptsoneside=SGnpts, order = 2, dx=dx, deriv=1)
#    lenconstdy=numpy.array([(dy[i]==0. and (0, ) or \
#    (numpy.all((numpy.abs((dy[i:]-dy[i])/dy[i])<=dydev_frac)|(numpy.abs(dy[i:]-dy[i])<=dydev_abs)) and (len(dy)-i, ) or \
#    (numpy.where(numpy.logical_not((numpy.abs((dy[i:]-dy[i])/dy[i])<=dydev_frac)|(numpy.abs(dy[i:]-dy[i])<=dydev_abs)))[0][:dydev_nout][-1],)))[0] for i in range(len(dy)-dydev_nout)])
    lenconstdy=numpy.array([(dy[i]==0. and (0, ) or \
    (numpy.all(numpy.abs(dy[i:]-dy[i])<max(numpy.abs(dy[i]*dydev_frac), dydev_abs)) and (len(dy)-i, ) or \
    (numpy.where(numpy.logical_not(numpy.abs(dy[i:]-dy[i])<max(numpy.abs(dy[i]*dydev_frac), dydev_abs)))[0][:dydev_nout][-1],)))[0] for i in range(len(dy)-dydev_nout)])
    #print len(y), len(lenconstdy), lenconstdy.max()
    
    if len(lenconstdy)==0:
        len_segs=[]
        istart_segs=[]
    else:
        lendn=savgolsmooth(numpy.float32(lenconstdy), nptsoneside=npts_SGconstdy, order = 1, dx=1.0, deriv=1, binprior=0)
        if plotbool:
            pylab.figure()
            pylab.plot(lenconstdy)
            pylab.ylabel('initial len of consecutive "constant dy" points')
            pylab.figure()
            pylab.plot(lendn)
            pylab.ylabel('lendn = deriv of len of const dy pts')
        istart_segs=numpy.where((lendn[:-1]>0)&(lendn[1:]<0))[0]
        if numpy.any(lenconstdy[:npts_SGconstdy+1]>=lenconstdy[npts_SGconstdy+1]):
            itemp=numpy.argmax(lenconstdy[:npts_SGconstdy])
            if not itemp in istart_segs:
                istart_segs=numpy.append(itemp, istart_segs)
        istart_segs[(istart_segs<npts_SGconstdy*2)]=npts_SGconstdy*2
        istart_segs[(istart_segs>len(y)-1-npts_SGconstdy*2)]=len(y)-1-npts_SGconstdy*2
        istart_segs+=numpy.array([numpy.argmax(lenconstdy[i-npts_SGconstdy*2:i+npts_SGconstdy*2]) for i in istart_segs])-npts_SGconstdy*2
        istart_segs=numpy.array(clustercoordsbymax1d(lenconstdy, istart_segs, dn_segstart))
        istart_segs=istart_segs[lenconstdy[istart_segs]>=dydev_nout/maxfracoutliers]
        
        #
        #istart=numpy.array([i for i in istart if (numpy.abs(i-istart)<dn_segstart).sum()==1 or numpy.all(lenconstdy[numpy.abs(i-istart)<dn_segstart]<=lenconstdy[i])])
        #istart=numpy.array([((numpy.abs(i-istart)<dn_segstart).sum()==1 and (i,) or (numpy.median(, ))[0] for i in istart)
        len_segs=lenconstdy[istart_segs]

    if not critdy_abs is None:
        critdy_fracmaxdy=critdy_abs/numpy.abs(dy).max()
    if not critdy_fracmaxdy is None:
        istart_constsegs, len_constsegs, garb, garb=findzerosegs(dy, critdy_fracmaxdy,  dydev_nout, dn_segstart,  SGnpts=SGnpts, plotbool=plotbool, dx=1., maxfracoutliers=maxfracoutliers)
#        if len(istart_constsegs)>0:
#            print istart_constsegs, len_constsegs
        temp=[[i, l] for i, l in zip(istart_constsegs, len_constsegs) if numpy.min((istart_segs-i)**2)>dn_segstart**2]
        if len(temp)>0:
            istart_constsegs, len_constsegs=numpy.array(temp).T
            istart_segs=numpy.append(istart_segs, istart_constsegs)
            len_segs=numpy.append(len_segs, len_constsegs)        
    if len(istart_segs)==0:
        return numpy.array([]), numpy.array([]), numpy.array([]), numpy.array([]), dy
        
    #dy_segs=numpy.array([dy[i:i+l].mean() for i, l in zip(istart_segs, len_segs)])
    #interc_segs=numpy.array([(y[i:i+l]-(i+numpy.arange(l))*d).mean() for i, l, d in zip(istart_segs, len_segs, dy_segs)])

    fitdy_segs, fitinterc_segs=numpy.array([numpy.polyfit(dx*(i+numpy.arange(l)), y[i:i+l], 1) for i, l in zip(istart_segs, len_segs)]).T
    
    if plotbool:
        pylab.figure()
        pylab.plot(y)
        cols=['g', 'c', 'y', 'm']
        for count, (i, l, fd, fy0) in enumerate(zip(istart_segs, len_segs, fitdy_segs, fitinterc_segs)):
            if l==max(len_segs):
                c='r'
            else:
                c=cols[count%len(cols)]
            pylab.plot(i, fy0+i*fd*dx, 'g*')
            #pylab.plot(i+numpy.arange(l),numpy.arange(l)*d+y0, 'g-')
            pylab.plot(i+numpy.arange(l),(i+numpy.arange(l))*fd*dx+fy0, '-', color=c, lw=2)

        pylab.figure()
        pylab.plot(dy)
        pylab.ylabel('dy')
        for count, (i, l, fd) in enumerate(zip(istart_segs, len_segs, fitdy_segs)):
            if l==max(len_segs):
                c='r'
            else:
                c=cols[count%len(cols)]
            pylab.plot(i, fd, 'g*')
            pylab.plot(i+numpy.arange(l),numpy.ones(l)*fd, '-', color=c, lw=2)
        pylab.figure()
        pylab.plot(lenconstdy, 'ko')
        pylab.plot(istart_segs, len_segs, 'r.')
        pylab.ylabel('len of consecutive "constant dy" points ')
    return istart_segs, len_segs, fitdy_segs, fitinterc_segs, dy # fit intercept is wrt the beginning of the array, index=0 not x=0

def findmatchinglinearsegs(y, dydev_frac,  dydev_nout, dn_segstart,  SGnpts=10, plotbool=False, dx=1., dydev_abs=0., maxfracoutliers=.5, critdy_fracmaxdy=None, critdy_abs=None):
    dy=savgolsmooth(y, nptsoneside=SGnpts, order = 2, dx=dx, deriv=1)
#    lenconstdy=numpy.array([(numpy.any(dyall[:,i]==0.) and (0,) or \
#    (numpy.all([(numpy.abs((dy[i:]-dyall[:,i].mean())/dyall[:,i].mean())<=dydev_frac)|(numpy.abs(dy[i:]-dy[i])<=dydev_abs)) and (len(dy)-i, ) or \
#    (numpy.where(numpy.logical_not((numpy.abs((dy[i:]-dy[i])/dy[i])<=dydev_frac)|(numpy.abs(dy[i:]-dy[i])<=dydev_abs)))[0][:dydev_nout][-1],)))[0] for i in range(len(dy)-dydev_nout)])

    nptstemp=2
    lendn=savgolsmooth(numpy.float32(lenconstdy), nptsoneside=nptstemp, order = 1, dx=1.0, deriv=1, binprior=0)
    istart_segs=numpy.where((lendn[:-1]>0)&(lendn[1:]<0))[0]
    istart_segs[(istart_segs<nptstemp*2)]=nptstemp*2
    istart_segs[(istart_segs>len(y)-1-nptstemp*2)]=len(y)-1-nptstemp*2
    istart_segs+=numpy.array([numpy.argmax(lenconstdy[i-nptstemp*2:i+nptstemp*2]) for i in istart_segs])-nptstemp*2
    istart_segs=numpy.array(clustercoordsbymax1d(lenconstdy, istart_segs, dn_segstart))
    istart_segs=istart_segs[lenconstdy[istart_segs]>=dydev_nout/maxfracoutliers]
    
    #
    #istart=numpy.array([i for i in istart if (numpy.abs(i-istart)<dn_segstart).sum()==1 or numpy.all(lenconstdy[numpy.abs(i-istart)<dn_segstart]<=lenconstdy[i])])
    #istart=numpy.array([((numpy.abs(i-istart)<dn_segstart).sum()==1 and (i,) or (numpy.median(, ))[0] for i in istart)
    len_segs=lenconstdy[istart_segs]

    if not critdy_abs is None:
        critdy_fracmaxdy=critdy_abs/numpy.abs(dy).max()
    if not critdy_fracmaxdy is None:
        istart_constsegs, len_constsegs, garb, garb=findzerosegs(dy, critdy_fracmaxdy,  dydev_nout, dn_segstart,  SGnpts=SGnpts, plotbool=plotbool, dx=1., maxfracoutliers=maxfracoutliers)
#        if len(istart_constsegs)>0:
#            print istart_constsegs, len_constsegs
        temp=[[i, l] for i, l in zip(istart_constsegs, len_constsegs) if numpy.min((istart_segs-i)**2)>dn_segstart**2]
        if len(temp)>0:
            istart_constsegs, len_constsegs=numpy.array(temp).T
            istart_segs=numpy.append(istart_segs, istart_constsegs)
            len_segs=numpy.append(len_segs, len_constsegs)        
    if len(istart_segs)==0:
        return numpy.array([]), numpy.array([]), numpy.array([]), numpy.array([]), dy
        
    #dy_segs=numpy.array([dy[i:i+l].mean() for i, l in zip(istart_segs, len_segs)])
    #interc_segs=numpy.array([(y[i:i+l]-(i+numpy.arange(l))*d).mean() for i, l, d in zip(istart_segs, len_segs, dy_segs)])

    fitdy_segs, fitinterc_segs=numpy.array([numpy.polyfit(dx*(i+numpy.arange(l)), y[i:i+l], 1) for i, l in zip(istart_segs, len_segs)]).T
    
    if plotbool:
        pylab.figure()
        pylab.plot(y)
        cols=['g', 'c', 'y', 'm']
        for count, (i, l, fd, fy0) in enumerate(zip(istart_segs, len_segs, fitdy_segs, fitinterc_segs)):
            if l==max(len_segs):
                c='r'
            else:
                c=cols[count%len(cols)]
            pylab.plot(i, fy0+i*fd*dx, 'g*')
            #pylab.plot(i+numpy.arange(l),numpy.arange(l)*d+y0, 'g-')
            pylab.plot(i+numpy.arange(l),(i+numpy.arange(l))*fd*dx+fy0, '-', color=c, lw=2)

        pylab.figure()
        pylab.plot(dy)
        pylab.ylabel('dy')
        for count, (i, l, fd) in enumerate(zip(istart_segs, len_segs, fitdy_segs)):
            if l==max(len_segs):
                c='r'
            else:
                c=cols[count%len(cols)]
            pylab.plot(i, fd, 'g*')
            pylab.plot(i+numpy.arange(l),numpy.ones(l)*fd, '-', color=c, lw=2)
        pylab.figure()
        pylab.plot(lenconstdy, 'ko')
        pylab.plot(istart_segs, len_segs, 'r.')
        pylab.ylabel('len of consecutive "constant dy" points ')
    return istart_segs, len_segs, fitdy_segs, fitinterc_segs, dy # fit intercept is wrt the beginning of the array, index=0 not x=0
    
def findzerosegs(y, yzero_maxfrac,  ydev_nout, dn_segstart,  SGnpts=10, plotbool=False, dx=1., maxfracoutliers=.5):#ydev_nout is number of outliers allowed in segment, dn_segstart is how close to each other the segments are allowed to start
    if ydev_nout>=len(y):
        print 'array not long enough to find zero segments'
        return [], [], [], []
    y=savgolsmooth(y, nptsoneside=SGnpts, order = 2)
    yzero_maxfrac=numpy.abs(y).max()*yzero_maxfrac
    lenzeroy=numpy.array([\
    (numpy.all(numpy.abs(y[i:])<=yzero_maxfrac) and (len(y)-i, ) or \
    (numpy.where(numpy.abs(y[i:])>yzero_maxfrac)[0][:ydev_nout][-1],))[0] for i in range(len(y)-ydev_nout)])

    nptstemp=2
    lendn=savgolsmooth(numpy.float32(lenzeroy), nptsoneside=nptstemp, order = 1, dx=1.0, deriv=1, binprior=0)
    
    
    istart_segs=numpy.where((lendn[:-1]>0)&(lendn[1:]<0))[0]
    if numpy.any(lenzeroy[:nptstemp+1]>=lenzeroy[nptstemp+1]):
        itemp=numpy.argmax(lenzeroy[:nptstemp])
        if not itemp in istart_segs:
            istart_segs=numpy.append(itemp, istart_segs)
    istart_segs[(istart_segs<nptstemp*2)]=nptstemp*2
    istart_segs[(istart_segs>len(y)-1-nptstemp*2)]=len(y)-1-nptstemp*2
    istart_segs+=numpy.array([numpy.argmax(lenzeroy[i-nptstemp*2:i+nptstemp*2]) for i in istart_segs])-nptstemp*2
    istart_segs=numpy.array(clustercoordsbymax1d(lenzeroy, istart_segs, dn_segstart))
    istart_segs=istart_segs[lenzeroy[istart_segs]>ydev_nout/maxfracoutliers]
    
    if len(istart_segs)==0:
        return numpy.array([]), numpy.array([]), numpy.array([]), numpy.array([])
        
    #istart=numpy.array([i for i in istart if (numpy.abs(i-istart)<dn_segstart).sum()==1 or numpy.all(lenconstdy[numpy.abs(i-istart)<dn_segstart]<=lenconstdy[i])])
    #istart=numpy.array([((numpy.abs(i-istart)<dn_segstart).sum()==1 and (i,) or (numpy.median(, ))[0] for i in istart)
    len_segs=lenzeroy[istart_segs]

    #dy_segs=numpy.array([dy[i:i+l].mean() for i, l in zip(istart_segs, len_segs)])
    #interc_segs=numpy.array([(y[i:i+l]-(i+numpy.arange(l))*d).mean() for i, l, d in zip(istart_segs, len_segs, dy_segs)])

    fitdy_segs, fitinterc_segs=numpy.array([numpy.polyfit(dx*(i+numpy.arange(l)), y[i:i+l], 1) for i, l in zip(istart_segs, len_segs)]).T
    
    if plotbool:
        pylab.figure()
        pylab.plot(y)
        cols=['g', 'c', 'y', 'm']
        for count, (i, l, fd, fy0) in enumerate(zip(istart_segs, len_segs, fitdy_segs, fitinterc_segs)):
            if l==max(len_segs):
                c='r'
            else:
                c=cols[count%len(cols)]
            pylab.plot(i, fy0+i*fd*dx, 'g*')
            #pylab.plot(i+numpy.arange(l),numpy.arange(l)*d+y0, 'g-')
            pylab.plot(i+numpy.arange(l),(i+numpy.arange(l))*fd*dx+fy0, '-', color=c, lw=2)


        for count, (i, l, fd) in enumerate(zip(istart_segs, len_segs, fitdy_segs)):
            if l==max(len_segs):
                c='r'
            else:
                c=cols[count%len(cols)]
            pylab.plot(i, fd, 'g*')
            pylab.plot(i+numpy.arange(l),numpy.ones(l)*fd, '-', color=c, lw=2)
        pylab.figure()
        pylab.plot(lenzeroy, 'ko')
        pylab.plot(istart_segs, lenzeroy[istart_segs], 'r.')
        pylab.ylabel('len of consecutive "zero" points')
    return istart_segs, len_segs, fitdy_segs, fitinterc_segs # fit intercept is wrt the beginning of the array, index=0 not x=0

def reggrid(x, y):
    if not numpy.all((x[:-1]-x[1:])==(x[1]-x[0])):
        xg=numpy.linspace(x.min(), x.max(), len(x))
        yg=interp(xg, x, y)
        return xg, yg
    else:
        return x, y


def calcmeandt_dlist(dlist):
    for d in dlist:
        d['dt']=(d['t(s)'][1:]-d['t(s)'][:-1]).mean()

def calcmeandEdt_dlist(dlist):
    for d in dlist:
        d['dt']=(d['t(s)'][1:]-d['t(s)'][:-1]).mean()
        d['dE']=(numpy.abs(d['Ewe(V)'][1:]-d['Ewe(V)'][:-1])).mean()
        d['dEdt']=d['dE']/d['dt']
        
def calcsegind_dlist(dlist, SGpts=8):
    if not 'dt' in dlist[0].keys():
        calcmeandt_dlist(dlist)
    for d in dlist:
        d['Ewe(V)_dtSG']=savgolsmooth(d['Ewe(V)'], nptsoneside=SGpts, order = 1, dx=d['dt'], deriv=1, binprior=0)
        rising=d['Ewe(V)_dtSG']>=0
        d['segind']=numpy.empty(len(rising), dtype='uint16')
        endptcorr=int(1.5*SGpts)#remove possibiliies of segment breaks within 1.5SGpts of the edges
        rising[:endptcorr+1]=rising[endptcorr+2]
        rising[-endptcorr-1:]=rising[-endptcorr-2]
        inds=numpy.where(rising[:-1]!=rising[1:])[0]
        inds=numpy.concatenate([[0], inds, [len(rising)]])
        for count, (i0, i1) in enumerate(zip(inds[:-1], inds[1:])):
            d['segind'][i0:i1]=count
        d['segprops_dlist']=[]
        for si, i0 in zip(range(d['segind'].max()+1), inds[:-1]):
            d['segprops_dlist']+=[{}]
            d['segprops_dlist'][-1]['rising']=rising[i0+1]
            inds2=numpy.where(d['segind']==si)[0]
            d['segprops_dlist'][-1]['inds']=inds2
            d['segprops_dlist'][-1]['npts']=len(d['segprops_dlist'][-1]['inds'])
            d['segprops_dlist'][-1]['dEdt']=d['Ewe(V)_dtSG'][inds2][SGpts:-SGpts].mean()

def manualsegind_dlist(dlist, istart=[0], SGpts=8):
    if not 'dt' in dlist[0].keys():
        calcmeandt_dlist(dlist)
        
    for d in dlist:
        d['Ewe(V)_dtSG']=savgolsmooth(d['Ewe(V)'], nptsoneside=SGpts, order = 1, dx=d['dt'], deriv=1, binprior=0)
        d['segprops_dlist']=[]
        d['segind']=numpy.empty(len(d['Ewe(V)']), dtype='uint16')
        iend=istart[1:]+[len(d['Ewe(V)'])]
        for count, (i0, i1) in enumerate(zip(istart, iend)):
            d['segind'][i0:i1]=count
            d['segprops_dlist']+=[{}]
            inds2=numpy.arange(i0, i1)
            d['segprops_dlist'][-1]['inds']=inds2
            d['segprops_dlist'][-1]['npts']=i1-i0
            d['segprops_dlist'][-1]['dEdt']=d['Ewe(V)_dtSG'][inds2][SGpts:-SGpts].mean()
            d['segprops_dlist'][-1]['rising']=d['segprops_dlist'][-1]['dEdt']>0.
            
def SegSG_dlist(dlist, SGpts=10, order=1, k='I(A)'):
    kSG=k+'_SG'
    for d in dlist:
        d[kSG]=numpy.zeros(d[k].shape, dtype='float32')
        for segd in d['segprops_dlist']:
            inds=segd['inds']
            d[kSG][inds]=numpy.float32(savgolsmooth(d[k][inds], nptsoneside=SGpts, order = order, deriv=0, binprior=0))

def SegdtSG_dlist(dlist, SGpts=10, order=1, k='I(A)', dxk='dt'):
    kSG=k+'_dtSG'
    for d in dlist:
        if not kSG in d.keys() and dxk in d.keys():
            continue
        d[kSG]=numpy.zeros(d[k].shape, dtype='float32')
        for segd in d['segprops_dlist']:
            inds=segd['inds']
            d[kSG][inds]=numpy.float32(savgolsmooth(d[k][inds], nptsoneside=SGpts, order = order, deriv=1, binprior=0, dx=d[dxk]))

        
def calcIllum_LVsettings(d, lv4tuple, savekey='Illumcalc'):
    lv_dark, lv_ill, lv_duty, lv_period=lv4tuple
    illum=numpy.zeros(len(d['t(s)']), dtype='bool')
    indsill=numpy.where((d['t(s)']>lv_dark)&(d['t(s)']<=lv_ill))[0]
    till=d['t(s)'][indsill]
    till-=till[0]
    cycfrac=(till%lv_period)/lv_period
    illum[indsill[cycfrac<=lv_duty]]=1
    d[savekey]=illum
    
def calcdiff_stepill(d, interd, ikey='Illum', ykeys=['Ewe(V)'], xkeys=['t(s)', 'I(A)'], illfracrange=(.4, .95), darkfracrange=(.4, .95)):
    if isinstance(ikey, list) or isinstance(ikey, numpy.ndarray):
        calcIllum_LVsettings(d, ikey, savekey='Illumcalc')
        illum=d['Illumcalc']
    else:
        illum=d[ikey]!=0
    istart_len_calc=lambda startind, endind, fracrange: (startind+numpy.floor(fracrange[0]*(endind-startind)), numpy.ceil((fracrange[1]-fracrange[0])*(endind-startind)))
    riseinds=numpy.where(illum[1:]&numpy.logical_not(illum[:-1]))[0]+1
    fallinds=numpy.where(numpy.logical_not(illum[1:])&illum[:-1])[0]+1
    
    if len(fallinds)==0 and len(riseinds)==0:
        print 'insufficient light cycles'
        return 1
    if illum[0]:
        illstart=0
        illend=fallinds[0]
        darkstart=fallinds[0]
        if len(riseinds)==0:
            darkend=len(illum)
        else:
            darkend=riseinds[0]
    else:
        darkstart=0
        darkend=riseinds[0]
        illstart=riseinds[0]
        if len(fallinds)==0:
            illend=len(illum)
        else:
            illend=fallinds[0]

    ill_istart, ill_len=istart_len_calc(illstart, illend, illfracrange)
    dark_istart, dark_len=istart_len_calc(darkstart, darkend, darkfracrange)

    inds_ill=[range(int(ill_istart), int(ill_istart+ill_len))]
    inds_dark=[range(int(dark_istart), int(dark_istart+dark_len))]


    d['inds_ill']=inds_ill
    d['inds_dark']=inds_dark

    getillvals=lambda arr:numpy.array([arr[inds].mean() for inds in inds_ill])
    getdarkvals=lambda arr:numpy.array([arr[inds].mean() for inds in inds_dark])
    
    interd['rawselectinds']=numpy.int32(numpy.round(getdarkvals(numpy.arange(len(d[ikey])))))
    for k in xkeys+ykeys:#these are len 1 arrays that will get saved as itnermediate data
        interd[k+'_ill']=getillvals(d[k])
        interd[k+'_dark']=getdarkvals(d[k])
    for k in ykeys:
        #d[k+'_illdiffmean']=d[k+'_ill'][0]-d[k+'_dark'][0]
        interd[k+'_illdiff']=numpy.array([d[k+'_ill'][0]-d[k+'_dark'][0]])
    return 0
        
def calcdiff_choppedill(d, interd, ikey='Illum', ykeys=['I(A)'], xkeys=['t(s)', 'Ewe(V)'], illfracrange=(.4, .95), darkfracrange=(.4, .95)):
    if isinstance(ikey, list) or isinstance(ikey, numpy.ndarray):
        calcIllum_LVsettings(d, ikey, savekey='Illumcalc')
        illum=d['Illumcalc']
    else:
        illum=d[ikey]!=0
    istart_len_calc=lambda startind, endind, fracrange: (startind+numpy.floor(fracrange[0]*(endind-startind)), numpy.ceil((fracrange[1]-fracrange[0])*(endind-startind)))
    riseinds=numpy.where(illum[1:]&numpy.logical_not(illum[:-1]))[0]+1
    fallinds=numpy.where(numpy.logical_not(illum[1:])&illum[:-1])[0]+1
    if len(fallinds)==0 or len(riseinds)==0:
        print 'insufficient light cycles'
        return 1
    riseinds=riseinds[riseinds<fallinds[-1]]#only consider illum if there is a dark before and after
    fallinds=fallinds[fallinds>riseinds[0]]
    if len(fallinds)==0 or len(riseinds)==0:
        print 'insufficient light cycles'
        return 1
    ill_istart, ill_len=istart_len_calc(riseinds, fallinds, illfracrange)
    darkstart, darkend=numpy.where(numpy.logical_not(illum))[0][[0, -1]]
    dark_istart, dark_len=istart_len_calc(numpy.concatenate([[darkstart], fallinds]), numpy.concatenate([riseinds, [darkend]]), darkfracrange)


    #inds_ill=[range(int(i0), int(i0+ilen)) for i0, ilen in zip(ill_istart, ill_len)]
    #inds_dark=[range(int(i0), int(i0+ilen)) for i0, ilen in zip(dark_istart, dark_len)]

    indstemp=[(range(int(i0ill), int(i0ill+ilenill)), range(int(i0dark), int(i0dark+ilendark))) for i0ill, ilenill, i0dark, ilendark in zip(ill_istart, ill_len, dark_istart, dark_len) if ilenill>0 and ilendark>0]
    inds_ill=map(operator.itemgetter(0), indstemp)
    inds_dark=map(operator.itemgetter(1), indstemp)
    if dark_len[-1]>0:
        inds_dark+=[range(int(dark_istart[-1]), int(dark_istart[-1]+dark_len[-1]))]
    else:
        inds_ill=inds_ill[:-1]

    d['inds_ill']=inds_ill
    d['inds_dark']=inds_dark

    getillvals=lambda arr:numpy.array([arr[inds].mean() for inds in inds_ill])
    getdarkvals=lambda arr:numpy.array([arr[inds].mean() for inds in inds_dark])
    
    #use the average dark inds as rawselectinds - ideally this would be the il inds but there are one less ill and don't want to endfill the selectinds with nan
    interd['rawselectinds']=numpy.int32(numpy.round(getdarkvals(numpy.arange(len(d[ikey])))))
    
    for k in xkeys+ykeys:
        interd[k+'_ill']=numpy.append(getillvals(d[k]), numpy.nan)
        interd[k+'_dark']=getdarkvals(d[k])
    for k in ykeys:
        interd[k+'_illdiff']=interd[k+'_ill']-0.5*(interd[k+'_dark']+numpy.append(interd[k+'_dark'], numpy.nan)[1:])
#        d[k+'_illdiffmean']=numpy.mean(d[k+'_illdiff'])
#        d[k+'_illdiffstd']=numpy.std(d[k+'_illdiff'])
    return 0
def calcdiff_ill_caller(d, interd, ikey='Illum', thresh=0, **kwargs):
    if isinstance(ikey, list) or isinstance(ikey, numpy.ndarray):
        calcIllum_LVsettings(d, ikey, savekey='Illumcalc')
        illum=d['Illumcalc']
        ikey='Illumcalc'
    else:
        illum=d[ikey]>thresh
    riseinds=numpy.where(illum[1:]&numpy.logical_not(illum[:-1]))[0]+1
    fallinds=numpy.where(numpy.logical_not(illum[1:])&illum[:-1])[0]+1
    d['IllumBool']=illum
    try:
        if len(riseinds)==0 or len(fallinds)==0 or (len(riseinds)==1 and len(fallinds)==1 and riseinds[0]>fallinds[0]):
            err=calcdiff_stepill(d, interd, ikey=ikey, **kwargs)
        else:
            err=calcdiff_choppedill(d, interd, ikey='IllumBool', **kwargs)
    except:
        return 1
    return err


#def illumtimeshift(illum, t, tshift):
#    tmod=t-tshift
#    inds=[numpy.argmin((tv-tmod)**2) for tv in t]
#    return illum[inds]

def illumtimeshift(d, ikey, tkey, tshift):
    tmod=d[tkey]-tshift
    inds=[numpy.argmin((t-tmod)**2) for t in d[tkey]]
    d[ikey]=d[ikey][inds]

def calc_comps_multi_element_inks(platemapdlist, cels_set_ordered, conc_el_chan, key_append_conc='.RelLoading', key_append_atfrac='.AtFrac', tot_conc_label=None):
    #platemap should have standard A-H channels, at least as many as conc_el_chan.shape[1], conc_el_chan is by "new" element and by platemap channel, make the key_append a string to update dlist or None to skip
    inkchannelsused=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'][:conc_el_chan.shape[1]]#grab the channels used
    #with this update the platemap is in units of concentration instead of fraction of printer channel loading
    if key_append_conc is None:
        key_append_conc='TEMP'
    cels_set_ordered_conc=[k+key_append_conc for k in cels_set_ordered]
    [d.update(\
                    zip(cels_set_ordered_conc, (numpy.float32([d[k] for k in inkchannelsused])[numpy.newaxis, :]*conc_el_chan).sum(axis=1)))\
                              for d in platemapdlist]
    if key_append_atfrac is None:
        cels_set_ordered_atfrac=[]
    else:
        cels_set_ordered_atfrac=[k+key_append_atfrac for k in cels_set_ordered]
        concarr=numpy.array([[d[k] for k in cels_set_ordered_conc] for d in platemapdlist])
        if not tot_conc_label is None:
            [d.update([(tot_conc_label, carr.sum())]) for d, carr in  zip(platemapdlist, concarr)]
        comparr2d=concarr/concarr.sum(axis=1)[:, numpy.newaxis]
        [d.update(zip(cels_set_ordered_atfrac, comparr)) for d, comparr in  zip(platemapdlist, comparr2d)]
    if key_append_conc=='TEMP':
        for d in platemapdlist:
            for k in cels_set_ordered_conc:
                del d[k]
        cels_set_ordered_conc=[]
    return cels_set_ordered_conc, cels_set_ordered_atfrac

def ternary_comp_to_cart(a, b, c):
    return 1.-a-b/2., numpy.sqrt(3)*b/2.0

def quaternary_comp_to_cart(a, b, c, d):
    return 1.-a-b/2.-d/2., b/2.*(3.**.5)+d/2./(3.**.5), d*(2.**.5)/(3.**.5)
    
def filterbydistancefromline(arr_of_xyz, xyz1, xyz2, critdist, betweenpoints=True, invlogic=False, returnonlyinds=False, is_composition=False): #if N points in D dimmensions arr_ is NxD, xyz1 and 2 are D, critdist is D-dimmension Euclidean, lineparameter is 0 to 1 from xyz 1 to xyz2 and can be out of that range
    #see http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html
    if is_composition:#probably cheaper to not do coordinate transform and just multiply by the distance ratio for the ndim, but this allows quat. to be done with 3D math
        arr_of_xyz/=arr_of_xyz.sum(axis=1)[:,numpy.newaxis]
        xyz1/=xyz1.sum()
        xyz2/=xyz2.sum()
        
        if xyz1.size==1:
            print 'unary compositions do not make sense'
        elif xyz1.size==2:
            arr_of_xyz=arr_of_xyz[:, 0]
            xyz1=xyz1[:1]
            xyz2=xyz2[:1]
        elif xyz1.size==3:
            arr_of_xyz=numpy.array(ternary_comp_to_cart(*arr_of_xyz.T)).T
            xyz1=numpy.array(ternary_comp_to_cart(*xyz1))
            xyz2=numpy.array(ternary_comp_to_cart(*xyz2))
        elif xyz1.size==4:
            arr_of_xyz=numpy.array(quaternary_comp_to_cart(*arr_of_xyz.T)).T
            xyz1=numpy.array(quaternary_comp_to_cart(*xyz1))
            xyz2=numpy.array(quaternary_comp_to_cart(*xyz2))
        else:
            print 'quinary or higher compositions not supported'
            return None
    else:
        if xyz1.size>3:
            print 'Only 1D,2D,3D supported'
            return None
    notnoninds=numpy.where(numpy.logical_not(numpy.isnan(arr_of_xyz)).prod(axis=1))[0]
    numnansamples=len(arr_of_xyz)-len(notnoninds)
    if numnansamples>0:
        arr_of_xyz=arr_of_xyz[notnoninds]
    distfromlin=numpy.array([numpy.linalg.norm(numpy.cross(xyz2-xyz1, xyz1-xyz))/numpy.linalg.norm((xyz2-xyz1)) for xyz in arr_of_xyz])
    if betweenpoints:
        lineparameter=numpy.array([-numpy.inner(xyz2-xyz1, xyz1-xyz)/numpy.linalg.norm((xyz2-xyz1))**2 for xyz in arr_of_xyz])
        if invlogic:
            inds=numpy.where(numpy.logical_not((distfromlin<=critdist) & (lineparameter>=0) & (lineparameter<=1)))[0]
        else:
            inds=numpy.where((distfromlin<=critdist) & (lineparameter>=0) & (lineparameter<=1))[0]
    else:
        lineparameter=numpy.array([-numpy.inner(xyz2-xyz1, xyz1-xyz)/numpy.linalg.norm((xyz2-xyz1))**2 for xyz in arr_of_xyz])
        if invlogic:
            inds=numpy.where(numpy.logical_not(distfromlin<=critdist))[0]
        else:
            inds=numpy.where(distfromlin<=critdist)[0]
    if returnonlyinds:
        return notnoninds[inds]
    else:
        if numnansamples>0:
            temp=numpy.ones(len(notnoninds)+numnansamples, dtype='float64')*numpy.nan
            temp[notnoninds]=distfromlin
            distfromlin=temp
            
            temp=numpy.ones(len(notnoninds)+numnansamples, dtype='float64')*numpy.nan
            temp[notnoninds]=lineparameter
            lineparameter=temp
            inds=notnoninds[inds]
        return {'select_inds':inds, 'dist_from_line':distfromlin, 'norm_dist_along_line':lineparameter}

def twotheta_q(q, wl=0.15418, units='deg'): #q is scattering vector in 1/nm.  wl is wavelength in nm. return float32 2Theta value in degrees unless units='rad'
    if units=='rad':
        return numpy.float32(2.0*numpy.arcsin(wl*q/(4.0*numpy.pi)))
    else:
        return numpy.float32(2.0*numpy.arcsin(wl*q/(4.0*numpy.pi))*180.0/numpy.pi)

def d_q(q): #q is scattering vector in 1/nm.  wl is wavelength in nm. return float32 2Theta value in degrees unless units='rad'
    return numpy.float32(2.0*numpy.pi/q)

def q_twotheta(twotheta, wl=0.15418, units='deg'): #units are those of twotheta, wl in nm, q in 1/nm
    if units=='deg':
        twotheta*=(numpy.pi/180.0)
    return 4*numpy.pi*numpy.sin(twotheta/2.0)/wl

def integrate_spectrum_with_piecewise_weights(spectrumx, spectrumy, weightsx, weightsy, below_val=0, above_val=0, return_completed_weights=False):
    #assume spectrum x and weights x are in increasing order
    completed_weights=numpy.zeros(len(spectrumy), dtype='float64')
    completed_weights[spectrumx<min(weightsx)]=below_val
    completed_weights[spectrumx>max(weightsx)]=above_val
    
    for x0, x1, y0, y1 in zip(weightsx[:-1], weightsx[1:],weightsy[:-1], weightsy[1:]):
        inds=numpy.where((spectrumx>=x0)&(spectrumx<=x1))[0]
        xarr=spectrumx[inds]
        yarr=y0+(y1-y0)*(xarr-x0)/(x1-x0)
        completed_weights[inds]=yarr
    newy=spectrumy*completed_weights
    if 0:
        plt.figure()
        plt.plot(spectrumx, spectrumy, 'k-')
        plt.plot(spectrumx, newy, 'r-')
        twax=plt.twinx()
        twax.plot(spectrumx, completed_weights, 'b-')
        twax.plot(weightsx, weightsy, 'bo')
        plt.show()
    integrated_val=numpy.trapz(newy, x=spectrumx)
    if return_completed_weights:
        return integrated_val, completed_weights
    return integrated_val
    
        
    
