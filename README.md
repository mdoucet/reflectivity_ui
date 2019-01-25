# Magnetic Reflectivity Reduction
[![TRAVISCI](https://travis-ci.org/mdoucet/reflectivity_ui.svg?branch=master)](https://travis-ci.org/mdoucet/reflectivity_ui)
[![codecov](https://codecov.io/gh/mdoucet/reflectivity_ui/branch/master/graph/badge.svg)](https://codecov.io/gh/mdoucet/reflectivity_ui)

## Latest version: v2.0.35 [01/24/2019]
 - Add result preview

## v2.0.34
 - Make sure spin asymmetry work when not rebinning.
 - Remove the option to use the data's TOF range because it creates problems when combining data (like spin asymmetry).

## v2.0.33
 - Hybrid spin boxes to test out synching to plots and responsiveness.
 - Background selection is now remembered from run to run upon loading.
 - Selecting a very wide wavelength band will pick the actual band in the data.
 - Made sure cutting TOF bins matches between specular (not rebinned) and off-specular
 - Updated wavelength band.