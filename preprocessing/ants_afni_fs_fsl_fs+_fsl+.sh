#!/bin/bash

# Author: 
# Jae Wook Cho

# Input example: 
# /home/xli/data/site-newcastle/sub-032104/sub-032104_ses-003_run-1_T1w.nii.gz

# Core parameter for ANTs
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=1
i=$1
site=`echo ${i} | cut -d '/' -f8`
sub=`echo ${i} | cut -d '/' -f9`
file=`basename ${i}`
filestring=`echo ${file} | cut -d '.' -f1`

outdir=/output
scriptsdir=/scripts
tmp_head=NMT_0.5mm/tmp_head/NMT_0.5mm
tmp_brain=NMT_0.5mm/tmp_brain/NMT_SS_0.5mm

# Run AFNI
# mkdir -p ${outdir}/afni/${site}/${sub}
OMP_NUMTHREADS=1 3dSkullStrip -input ${i} -prefix ${outdir}/afni/${site}/${sub}/${filestring}_brainmask_afni.nii.gz -push_to_edge -monkey -shrink_fac 0.5
fslmaths ${outdir}/afni/${site}/${sub}/${filestring}_brainmask_afni.nii.gz -bin ${outdir}/afni/${site}/${sub}/${filestring}_brainmask_afni_mask.nii.gz

# Run FS
# mkdir -p ${outdir}/fs/${site}/${sub}
OMP_NUMTHREADS=1 mri_watershed -r 60 -T1 ${i} ${outdir}/fs/${site}/${sub}/${filestring}_brainmask_fs.nii.gz
OMP_NUMTHREADS=1 fslmaths ${outdir}/fs/${site}/${sub}/${filestring}_brainmask_fs.nii.gz -bin ${outdir}/fs/${site}/${sub}/${filestring}_brainmask_fs_mask.nii.gz
echo ${outdir}/fs/${site}/${sub}/${filestring}_brainmask_fs_mask.nii.gz

# Run FSL
# mkdir -p ${outdir}/fsl/${site}/${sub}
OMP_NUMTHREADS=1 bet ${i} ${outdir}/fsl/${site}/${sub}/${filestring}_fsl.nii.gz -v -f 0.3 -g 0.0 -r 60 -m

# Run ANTS for monkey data using NMT template:
# mkdir -p ${outdir}/ants/${site}/${sub}
cp ${i} ${outdir}/ants/${site}/${sub}/
imgdir=${outdir}/ants/${site}/${sub}/
img=${filestring}

OMP_NUMTHREADS=1 bash ${scriptsdir}/MaskandRegister.bash ${imgdir} ${img} ${tmp_head} ${tmp_brain}
rm ${outdir}/ants/${site}/${sub}/${filestring}.nii.gz

# Optimal options from Zhao (2018), Bayesian Convolutional Neural Network Based MRI Brain Extraction on Nonhuman Primates:
# AFNI: -push_to_edge -monkey -shrink_fac 0.5
# HWA (mri_watershed): -atlas *** Also adding BRAIN radius ("-r")*** 
# BET: -f 0.3 -g -0.5 -r 35

# Run FS+
# mkdir -p ${outdir}/fs_zhao-options/${site}/${sub}

# Get brain radius (30/voxel size):
voxSize=`3dinfo -ad3 ${i} | sort -n | awk '{print $3}'` # Get largest voxel dimension
brain_rad=`echo "${voxSize}"|  awk '{print 30/$1}'` # Divide by 30 to get mm

OMP_NUMTHREADS=1 mri_watershed -atlas -T1 -r ${brain_rad} ${i} ${outdir}/fs_zhao-options/${site}/${sub}/${filestring}_brainmask_fs.nii.gz 
OMP_NUMTHREADS=1 fslmaths ${outdir}/fs_zhao-options/${site}/${sub}/${filestring}_brainmask_fs.nii.gz -bin ${outdir}/fs_zhao-options/${site}/${sub}/${filestring}_brainmask_fs_mask.nii.gz

# Run FSL+
# mkdir -p ${outdir}/fsl_zhao-options/${site}/${sub}
OMP_NUMTHREADS=1 bet ${i} ${outdir}/fsl_zhao-options/${site}/${sub}/${filestring}_fsl.nii.gz -f 0.3 -g -0.5 -r 35 -m # "-m": output mask