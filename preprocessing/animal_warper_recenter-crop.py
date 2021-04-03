'''Script to recenter and crop T1w data and run AFNI @animal_warper on new T1w

author: Xinhui Li 04/02/21
'''

import os
import sys
import getopt
import argparse
import numpy as np
import nibabel as nb

def run_animal_warper(wd, t1, mask, template, template_mask):

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
    if '/' in t1:
        t1_new = t1[t1.rindex('/')+1:t1.rindex('.nii.gz')] + '_shift.nii.gz'
    else:
        t1_new = t1[0:t1.rindex('.nii.gz')] + '_shift.nii.gz'
    out.to_filename(t1_new)

    # run @animal_warper with recentered+cropped T1w
    # it will create a folder called aw_results in working directory
    cmd="@animal_warper -input %s -base %s -skullstrip %s" % (t1_new, template, template_mask)
    os.system(cmd)


if __name__=='__main__':

    ## Running instructions ##

    # For example,
    # if all data is in the same folder as following:
    # /home/xli/data/site-princeton/sub-032114
    #  - sub-032114_ses-001_run-1_T1w.nii.gz
    #  - sub-032114_ses-001_run-1_T1w_mask.nii.gz
    #  - NMT_v2.0_sym/NMT_v2.0_sym_05mm/NMT_v2.0_sym_05mm.nii.gz
    #  - NMT_v2.0_sym/NMT_v2.0_sym_05mm/NMT_v2.0_sym_05mm_brainmask.nii.gz

    # we can use this command:
    # python animal_warper_recenter-crop.py \
    # -w /home/xli/data/sub-032114 \
    # -t sub-032114_ses-001_run-1_T1w.nii.gz \
    # -m sub-032114_ses-001_run-1_T1w_mask.nii.gz \
    # -tt NMT_v2.0_sym/NMT_v2.0_sym_05mm/NMT_v2.0_sym_05mm.nii.gz \
    # -tm NMT_v2.0_sym/NMT_v2.0_sym_05mm/NMT_v2.0_sym_05mm_brainmask.nii.gz

    # full paths also work

    # arguments
    parser = argparse.ArgumentParser(description='Training Model', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    optional=parser._action_groups.pop()
    required=parser.add_argument_group('required arguments')

    # required options
    required.add_argument('-w', '--working_dir', type=str, required=True, help='working directory')
    required.add_argument('-t', '--t1_path', type=str, required=True, help='t1w path')
    required.add_argument('-m', '--mask_path', type=str, required=True, help='mask path')
    required.add_argument('-tt', '--template_t1_path', type=str, required=True, help='template t1 path')
    required.add_argument('-tm', '--template_mask_path', type=str, required=True, help='template mask path')

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    run_animal_warper(args.working_dir, args.t1_path, args.mask_path, args.template_t1_path, args.template_mask_path)