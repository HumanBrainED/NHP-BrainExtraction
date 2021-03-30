import os
import sys
import numpy as np
import nibabel as nb

# TODO XL test code

# TODO change paths here
wd = '' # working directory
t1 = '' # T1w path
mask = '' # initial mask path, it can be U-Net or manual mask
base="NMT_v2.0_sym/NMT_v2.0_sym_05mm/NMT_v2.0_sym_05mm.nii.gz" # NMT template
nmtmask="NMT_v2.0_sym/NMT_v2.0_sym_05mm/NMT_v2.0_sym_05mm_brainmask.nii.gz" # NMT brain mask

os.chdir(wd)

# load T1w and mask data
t1_data = nb.load(t1).get_fdata()
mask_data = nb.load(mask).get_fdata()

# calculate new center position
nonzero_index = np.unique(np.nonzero(mask_data)[2])
nonzero_bottom_index = nonzero_index[0]
nonzero_top_index = nonzero_index[-1]
nonzero_center = (nonzero_bottom_index + nonzero_top_index) / 2
img_length = mask_data.shape[2]
top_diff = img_length - nonzero_top_index
img_center = img_length / 2
center_diff = nonzero_center - img_center

# crop T1w based on new center position
t1_data_new = t1_data[:, :, center_diff*2:]
t1_data_new[:, :, 0:top_diff] = 0
data_zero = np.zeros((t1_data.shape[0], t1_data.shape[1], center_diff))
data = np.concatenate((data_zero, t1_data_new, data_zero), axis=2)
out = nb.Nifti1Image(data, affine=nb.load(t1).affine)

# TODO change recentered+cropped T1w filename if necessary
t1_new = t1[t1.rindex('/')+1:t1.rindex('.nii.gz')] + '_shift.nii.gz'
out.to_filename(t1_new)

# run @animal_warper with recentered+cropped T1w
# it will create a folder called aw_results in working directory
cmd="@animal_warper -input %s -base %s -skullstrip %s"%(t1_new, base, nmtmask)
os.system(cmd)