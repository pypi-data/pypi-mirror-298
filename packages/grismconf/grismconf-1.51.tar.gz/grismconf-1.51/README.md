# GRISMCONF

This module implements the new grism configuration described in Pirzkal and Ryan 2016 (https://www.stsci.edu/files/live/sites/www/files/home/hst/instrumentation/wfc3/documentation/instrument-science-reports-isrs/_documents/2017/WFC3-2017-01.pdf). As such, it provides the dispersion polynomials:
```
#!python

wavelength = DISPL(order,x0,y0,t)
dx = DISPX(order,x0,y0,t)
dy = DISPY(order,x0,y0,t)
```
and
```
#!python
t = INVDISPX(order,x0,y0,dx)
t = INVDISPY(order,x0,y0,dy)
t = INVDISPL(order,x0,y0, wavelength)
```
where order is configuration file specific but is usually "+1", "+2", "+3" etc..., and t is a free variable 0<t<1.

These polynomials are a generalization of the old aXe grism configuration file polynomials.

Configurations file can be found at https://github.com/npirzkal/GRISM_WFC3 for HST/WFC3 IR
and
https://github.com/npirzkal/GRISM_NIRCAM for JWST/NIRCAM
# Installing:

Install using 
```
pip install grismconf
```
or clone and install using
```
python setup.py install
```

# Using: #
## Example 1: ##
We want to determine the x, y and wavelength of pixels containing the trace originating from a pixel at x0,y0 in the un-dispersed frame. We want to look at the dispersed pixels that are at location x+dxs on the dispersed image. dxs can be an array.:


```
#!python

import grismconf
x0 = 500.5
y0 = 600.1

# Load the Grism Configuration file
C = grismconf.Config(“NIRCAM_R.conf")
# edges of spectra (use t=0 and t=1)
dx01 = C.DISPX("+1",x0,y0,np.array([0,1]))
# Get a list of all dxs value along this trace
dxs = np.arange(dx01[0],dx01[1])
# Compute the t values corresponding to the exact offsets dxs
ts = C.INVDISPX("+1",x0,y0,dxs)
# Compute the dys values for the same pixels
dys = C.DISPY("+1",x0,y0,ts)
# Compute wavelength of each of the pixels
wavs = C.DISPL("+1",x0,y0,ts)

```


## Example 2: ##
What is the dispersion in Angstrom per pixel at the left edge of the spectrum (t=0.):

```
#!python

C.DDISPL("+1",x0,y0,0)/C.DDISPX(order,x0,y0,0)
```

## Example 3: ##
Computes what is needed to simulate the dispersion of a pixel. The free variable is t.

```
#!python
# We select a sensible set of values for the variable t. Since 0<t<1 corresponfs to lambda_min<lambda<lambda_max for the spectral order. 
# If we want to oversample (in the lambda direction by a factor of fac, we use:

dt = 1/(C.DISPX("+1",x0,y0,0)-C.DISPX("+1",x0,y0,1)) / fac
t = np.arange(0,1,dt)

# We can now select where the x, y and wavelength of the dispersed pixels:
#or, to generate a fake spectrum:
# By default t valid values are 0<t<1
dxs = DISPX("+1",x0,y0,t)
dys = DISPY("+1",x0,y0,t)
wavs = DISPL("+1",x0,y0,t)
```


How to easily compute other things:
wavelength x-size of a pixel (at t):
C.DDISPL(order,x0,y0,t)/C.DDISPX(order,x0,y0,t)
the y-size is just:
C.DDISPL(order,x0,y0,t)/C.DDISPY(order,x0,y0,t)


## Example 4: ##
Load the grism configuration information from a previously populated JWST datamodel from a fits files:
Note: the assign_wcs as well as the photom steps must have be ran on fits file during processing so that the WFSS information is already populated. All polynomials as well as the sensitivity can be loaded in this manner. The POM information and WFSS background calibration file names are not included in this case.

```
#!python
wfss_file = "/Users/npirzkal/Dropbox/NIRCAM/tutorial/jw01076103001_02101_00001_nrcalong_rate.fits"
C = grismconf.Config(wfss_file)
```
