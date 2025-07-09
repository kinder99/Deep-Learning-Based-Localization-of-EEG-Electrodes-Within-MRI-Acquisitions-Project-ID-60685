# Deep Learning-Based Localization of EEG Electrodes Within MRI Acquisitions

## Purpose
This repository contains the various scripts and functions used to support the segmentation of electrodes in fMRI volumes in an EEG-fMRI context.

## Languages
- Python
- Matlab

## This repository follows Caroline Pinte's work, and builds upon it by :
- refactoring it to work with nnU-Net v2
- testing said refactored method on T1 images
- adding scripts to test and extract information from training and trained datasets

## Usage
The use of a Python virtual environment is highly recommended.

Packages :
- nnU-Net V2 (mandatory)
- pytorch (mandatory)
- nibabel (mandatory)
- pandas (mandatory)
- numpy (mandatory)
- SimpleITK (mandatory)
- Matplotlib (mandatory)
- hiddenlayer (recommended)

Code associated with the article : "Deep Learning-Based Localization of EEG Electrodes Within MRI Acquisitions" (https://doi.org/10.3389/fneur.2021.644278).