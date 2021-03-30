#!/bin/bash
# Input example: /data/Projects/txu/projects/PRIME/preprocessed_BIDS/site-*/${sub}/*/anat/*.nii.gz

# Core parameter for ANTs
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=1
i=$1
site=`echo ${i} | cut -d '/' -f8`
sub=`echo ${i} | cut -d '/' -f9`
file=`basename ${i}`
filestring=`echo ${file} | cut -d '.' -f1`

jdir=/data/Projects/txu/projects/PRIME
outdir=${jdir}/Other_pipeline_output
scriptsdir=${jdir}/scripts/_pp
tmp_head=${jdir}/downloads/NMT_0.5mm/tmp_head/NMT_0.5mm
tmp_brain=${jdir}/downloads/NMT_0.5mm/tmp_brain/NMT_SS_0.5mm

# Optimal options from Zhao (2018), Bayesian Convolutional Neural Network Based MRI Brain Extraction on Nonhuman Primates:
# AFNI: -push_to_edge -monkey -shrink_fac 0.5
# HWA (mri_watershed): -atlas *** Also adding BRAIN radius ("-r")*** 
# BET: -f 0.3 -g -0.5 -r 35

# Run FS/HWA
mkdir -p ${outdir}/fs_zhao-options/${site}/${sub}
# Get brain radius (30/voxel size):
voxSize=`3dinfo -ad3 ${i} | sort -n | awk '{print $3}'` # Get largest voxel dimension
brain_rad=`echo "${voxSize}"|  awk '{print 30/$1}'` # Divide by 30 to get mm

OMP_NUMTHREADS=1 mri_watershed -atlas -T1 -r ${brain_rad} ${i} ${outdir}/fs_zhao-options/${site}/${sub}/${filestring}_brainmask_fs.nii.gz 
OMP_NUMTHREADS=1 fslmaths ${outdir}/fs_zhao-options/${site}/${sub}/${filestring}_brainmask_fs.nii.gz -bin ${outdir}/fs_zhao-options/${site}/${sub}/${filestring}_brainmask_fs_mask.nii.gz

# Run FSL
mkdir -p ${outdir}/fsl_zhao-options/${site}/${sub}
OMP_NUMTHREADS=1 bet ${i} ${outdir}/fsl_zhao-options/${site}/${sub}/${filestring}_fsl.nii.gz -f 0.3 -g -0.5 -r 35 -m # "-m": output mask