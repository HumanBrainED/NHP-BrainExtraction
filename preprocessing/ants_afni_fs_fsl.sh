#!/bin/bash
# Input example: /data3/cdb/jcho/monkey/unet/data/site-newcastle/sub-032104/sub-032104_ses-003_run-1_T1w_denoise_N4_nu.nii.gz

# Core parameter for ANTs
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=1
i=$1
site=`echo ${i} | cut -d '/' -f8`
sub=`echo ${i} | cut -d '/' -f9`
file=`basename ${i}`
filestring=`echo ${file} | cut -d '.' -f1`

jdir=/data3/cdb/jcho/monkey
datadir=${jdir}/unet/data
# outdir=${jdir}/unet/results
outdir=/data/Projects/txu/projects/PRIME/Other_pipeline_output
scriptsdir=${jdir}/scripts
tmp_head=${jdir}/NMT_0.5mm/tmp_head/NMT_0.5mm
tmp_brain=${jdir}/NMT_0.5mm/tmp_brain/NMT_SS_0.5mm

# Run AFNI
# mkdir -p ${outdir}/afni/${site}/${sub}
rm ${outdir}/afni/${site}/${sub}/${filestring}_brainmask_afni.nii.gz
rm ${outdir}/afni/${site}/${sub}/${filestring}_brainmask_afni_mask.nii.gz
OMP_NUMTHREADS=1 3dSkullStrip -input ${i} -prefix ${outdir}/afni/${site}/${sub}/${filestring}_brainmask_afni.nii.gz -push_to_edge -monkey -shrink_fac 0.5
fslmaths ${outdir}/afni/${site}/${sub}/${filestring}_brainmask_afni.nii.gz -bin ${outdir}/afni/${site}/${sub}/${filestring}_brainmask_afni_mask.nii.gz

# Run FS
# mkdir -p ${outdir}/fs/${site}/${sub}
rm ${outdir}/fs/${site}/${sub}/${filestring}_brainmask_fs.nii.gz
rm ${outdir}/fs/${site}/${sub}/${filestring}_brainmask_fs_mask.nii.gz
OMP_NUMTHREADS=1 mri_watershed -r 60 -T1 ${i} ${outdir}/fs/${site}/${sub}/${filestring}_brainmask_fs.nii.gz # -r 30
OMP_NUMTHREADS=1 fslmaths ${outdir}/fs/${site}/${sub}/${filestring}_brainmask_fs.nii.gz -bin ${outdir}/fs/${site}/${sub}/${filestring}_brainmask_fs_mask.nii.gz
echo ${outdir}/fs/${site}/${sub}/${filestring}_brainmask_fs_mask.nii.gz

# Run FSL
# mkdir -p ${outdir}/fsl/${site}/${sub}
rm ${outdir}/fsl/${site}/${sub}/${filestring}_fsl.nii.gz
rm ${outdir}/fsl/${site}/${sub}/${filestring}_fsl_mask.nii.gz
OMP_NUMTHREADS=1 bet ${i} ${outdir}/fsl/${site}/${sub}/${filestring}_fsl.nii.gz -v -f 0.3 -g 0.0 -r 60 -m # -r 35

# Run ANTS for monkey data using NMT template:
rm -R ${outdir}/ants/${site}/${sub}
mkdir -p ${outdir}/ants/${site}/${sub}
cp ${i} ${outdir}/ants/${site}/${sub}/
imgdir=${outdir}/ants/${site}/${sub}/
img=${filestring}

OMP_NUMTHREADS=1 bash ${scriptsdir}/MaskandRegister.bash ${imgdir} ${img} ${tmp_head} ${tmp_brain}
rm ${outdir}/ants/${site}/${sub}/${filestring}.nii.gz

##
bash /data3/cdb/jcho/monkey/scripts/MaskandRegister.bash /data3/cnl/xli/unet_ss/uwo/ants/sub-032187 sub-032187_ses-001_acq-mp2rage_run-1_T1w_denoise_N4_nu /data3/cdb/jcho/monkey/NMT_0.5mm/tmp_head/NMT_0.5mm /data3/cdb/jcho/monkey/NMT_0.5mm/tmp_brain/NMT_SS_0.5mm