# Deep Learning-Based Localization of EEG Electrodes Within MRI Acquisitions

## Purpose
This repository contains the various scripts and functions used to support the segmentation of electrodes in MRI volumes in an EEG-fMRI context.

## Languages
- Python
- Matlab

## This repository follows Caroline Pinte's work, and builds upon it by :
- refactoring it to work with nnU-Net v2
- testing said refactored method on T1 images
- adding scripts to test and extract information from training and trained datasets
- adding comparison to a state of the art method in the form of Brainstorm template matching.

## Usage
The use of a Python virtual environment is highly recommended.

Some of the scripts won't be necessary to use and are only there as special cases (mostly dataset fixing).

The pipeline to follow is :

`build_dataset.py` -> `nnU-Net training` -> `run inferences` -> `coords.py` -> `post_processing.m` -> `validationV2_correct.py`

Other scripts such as `electrode_counter.py`, `error_pos_plotter.ipynb` and `log_plotter.ipynb` can be used to give additionnal information throughout the process.

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