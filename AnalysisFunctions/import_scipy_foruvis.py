# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 18:15:13 2016

@author: santosh
"""
try:
    from scipy.signal import savgol_filter
    from uvis_basics import *
except:
    class Analysis__TR_UVVIS():
        def __init__(self):
            self.analysis_name='Analysis__TR_UVVIS'            
        def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
            return []
    class Analysis__DR_UVVIS():
        def __init__(self):
            self.analysis_name='Analysis__DR_UVVIS'            
        def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
            return []            
    class Analysis__T_UVVIS():
        def __init__(self):
            self.analysis_name='Analysis__T_UVVIS'
        def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
            return []
    class Analysis__BG():
        def __init__(self):
            self.analysis_name='Analysis__BG'
        def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None, anadict=None):
            return []
    print 'UV-VIS analysis cannot be run because there is no scipy.signal.savgol_filter function'