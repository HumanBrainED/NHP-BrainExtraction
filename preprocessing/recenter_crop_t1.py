"""Script to recenter and crop T1w

Instructions

The inputs include T1w and an initial brain mask (e.g., U-Net mask), in *.nii.gz format.
The output will be a recentered and cropped T1w in the working directory.
For example, if all data is in the same folder as following:
/projects/working_dir/sub-032114
    - sub-032114_ses-001_run-1_T1w.nii.gz
    - sub-032114_ses-001_run-1_T1w_mask.nii.gz

You can use relative or absolute paths to run the script:
python recenter_crop_t1.py \
-w /projects/working_dir/sub-032114 \
-t sub-032114_ses-001_run-1_T1w.nii.gz \
-m sub-032114_ses-001_run-1_T1w_mask.nii.gz

Author: Xinhui Li 04/02/21, Ting Xu 08/10/21
"""

import os
import sys
import getopt
import argparse
import numpy as np
import nibabel as nb

def recenter_crop_t1(wd, t1, mask):

    os.chdir(wd)
    print("working_dir: " + wd)

    # load T1w and mask data
    t1_data = nb.load(t1).get_fdata()
    mask_data = nb.load(mask).get_fdata()

    if t1_data.shape != mask_data.shape:
        raise Exception(f"\n\n[!] Error: The dimension of T1w is {t1_data.shape} "
            f"but the dimension of brain mask is {mask_data.shape}. "
            "Please edit your image and make sure both images have the same dimension.\n\n")

    # calculate new center position
    nonzero_index = np.unique(np.nonzero(mask_data)[2])
    nonzero_bottom_index = nonzero_index[0]
    nonzero_top_index = nonzero_index[-1]
    nonzero_center = (nonzero_bottom_index + nonzero_top_index) / 2
    img_length = mask_data.shape[2]
    top_diff = img_length - nonzero_top_index
    img_center = img_length / 2
    center_diff = int(nonzero_center - img_center)
    if img_center > nonzero_center: 
        # move the image up
        t1_data_new = t1_data[:, :, 0:(t1_data.shape[2]+center_diff)]
        data_zero = np.zeros((t1_data.shape[0], t1_data.shape[1], abs(center_diff)))
        data = np.concatenate((data_zero, t1_data_new), axis=2)
    else:
        # crop T1w based on new center position
        t1_data_new = t1_data[:, :, center_diff*2:]
        t1_data_new[:, :, 0:top_diff] = 0
        data_zero = np.zeros((t1_data.shape[0], t1_data.shape[1], center_diff))
        data = np.concatenate((data_zero, t1_data_new, data_zero), axis=2)
    out = nb.Nifti1Image(data, affine=nb.load(t1).affine)

    # change recentered+cropped T1w filename if necessary
    if '/' in t1:
        t1_new = t1[t1.rindex('/')+1:t1.rindex('.nii.gz')] + '_centered.nii.gz'
    else:
        t1_new = t1[0:t1.rindex('.nii.gz')] + '_centered.nii.gz'
    out.to_filename(t1_new)


if __name__=='__main__':

    # arguments
    parser = argparse.ArgumentParser(description='Recenter and crop T1w image', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    optional=parser._action_groups.pop()
    required=parser.add_argument_group('required arguments')

    # required options
    required.add_argument('-w', '--working_dir', type=str, required=True, help='working directory')
    required.add_argument('-t', '--t1_path', type=str, required=True, help='t1w path')
    required.add_argument('-m', '--mask_path', type=str, required=True, help='mask path')

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    recenter_crop_t1(args.working_dir, args.t1_path, args.mask_path)
