John M Gregoire 20 May 2015, 

All code written by John Gregoire, Santosh Suram and Dan Guevarra. Code is a work in progress for analyzing and visualizing JCAP-HTE data.

The top level program is DataProcessMasterApp.py

Requires additional repository in the same root directory as JCAPDataProcess:

	PythonCompositionPlots
	https://github.com/johnmgregoire/PythonCompositionPlots


The default Anaconda (Python 2.7) install contains all but one module dependencies:

	PyQt4
	https://pypi.python.org/pypi/PyQt4

**Anaconda's default Qt4 backend must be changed from 'PySide' to 'PyQt4' in matplotlibrc.
http://matplotlib.org/1.3.1/users/customizing.html

Linux, OSX, and Windows installers for Anaconda are available here:
	
	http://continuum.io/downloads

Great resource for unofficial windows binaries such as MySQL-python:

	http://www.lfd.uci.edu/~gohlke/pythonlibs/
