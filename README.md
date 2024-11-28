[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14231926.svg)](https://doi.org/10.5281/zenodo.14231926)![CI/CD](https://github.com/IntegratedPathologyUnit-ICR/c-pmat/actions/workflows/actions.yml/badge.svg)![PyPI version](https://badge.fury.io/py/c-pmat.svg)([(https://pypi.org/project/c-pmat/])

# c-PMAT : PSR STAIN PREPROCESSING WORKFLOW 

c-pmat ***C***omputational ***P***reprocessing of extracellular ***mat***rix 

c-pmat is a interactive user interface, allowing user to easily preprocess, quality control (QC) 
and generate quantitative extracellular matrix features.

Preprocess constitutes generating tiles and the corresponding metadata from the whole slide images.
Quality control is dependant on annotations and this retains the tiles free of artifact and 
tiles belonging to the annotated regions and ensures enough tissue on the tile is present to 
perform downstream analysis.

Through the usage of the step by step process, user will be able to preprocess,
extract and quantify extracellular matrix features.

## Installation from pypi
```
pip install c-pmat==1.0.0

```


## Understanding data preparation

In this section we will summarize the organization of directory structure to enable 
the end user extract the information needed to directly interact with the annotations which comes as a string
or different names provided by the pathologists (generic).

In the below example we have a first whole slide image with 6 regions of interest and they are named as 
ROI1, ROI2, .... ROI6 respectively and the second whole slide image with 3 regions of interest
ROI1, ROI2, ROI3 respectively. These annotations are free hand polygon annotations drawn on the tissue by the 
pathologists to infer the changes in the extracellular matrix components with respect to the individual ROI and 
cater for inter-tumour and intra-tumour heterogeneity and its implication of features at slide and ROI levels.

<p align="center">
  <img src="screenshot_images/dp1.PNG" width="850" title="WSI-1" />
  <img src="screenshot_images/dp2.PNG" width="850" title="WSI-2" />
</p>


Currently, we have the support for the annotations performed by the pathologists using Imagescope on the
PSR stained whole slide images.

Once you have annotations, it will retain the ROIs with respect to the individual slide automatically and extract the tiles
corresponding to each ROI.

Note: This code can be generically used for other brightfield images and extraction of the annotations performed on Imagescope.

## ROI stitching at low resolution

It also helps to restitch the ROI's at a lower resolution for sanity check so it can be further processed by TWOMBLI


## Extraction of features within c-PMAT framework
Note: PMAT name was unavailable on pypi hence c-PMAT

## Reference 
## Citation



1. https://doi.org/10.25418/crick.26565343
2. https://zenodo.org/records/14231926
   
