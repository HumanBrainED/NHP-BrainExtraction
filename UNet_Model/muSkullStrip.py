#!/usr/bin/env python
import torch
import torch.nn as nn
from function import predict_volumes
from model import UNet2d
import os, sys
import argparse

if __name__=='__main__':
    NoneType=type(None)
    # Argument
    parser=argparse.ArgumentParser(description='Skullstripping', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    optional=parser._action_groups.pop()
    required=parser.add_argument_group('required arguments')
    # Required Option
    required.add_argument('-in', '--input_t1w', type=str, required=True, help='Input T1w Image for Skull Stripping')
    required.add_argument('-model', '--predict_model', required=True, type=str, help='Predict Model')
    # Optional Option
    optional.add_argument('-out', '--out_dir', type=str, help='Output Dir')
    optional.add_argument('-suffix', '--mask_suffix', type=str, default="pre_mask", help='Suffix of Mask')
    optional.add_argument('-slice', '--input_slice', type=int, default=3, help='Number of Slice for Model Input')
    optional.add_argument('-conv', '--conv_block', type=int, default=5, help='Number of UNet Block')
    optional.add_argument('-kernel', '--kernel_root', type=int, default=16, help='Number of the Root of Kernel')
    optional.add_argument('-rescale', '--rescale_dim', type=int, default=256, help='Number of the Root of Kernel')
    optional.add_argument('-ed_iter', '--erosion_dilation_iteration', type=int, default=0, help='Number of Iteration for Erosion and Dilation')
    parser._action_groups.append(optional)
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    print("=============================Permforming Skullstripping=============================")
    
    train_model=UNet2d(dim_in=args.input_slice, num_conv_block=args.conv_block, kernel_root=args.kernel_root)
    checkpoint=torch.load(args.predict_model, map_location={'cuda:0':'cpu'})
    train_model.load_state_dict(checkpoint['state_dict'])
    model=nn.Sequential(train_model, nn.Softmax2d())

    predict_volumes(model, cimg_in=args.input_t1w, bmsk_in=None, rescale_dim=args.rescale_dim, save_dice=False,
            save_nii=True, nii_outdir=args.out_dir, suffix=args.mask_suffix, ed_iter=args.erosion_dilation_iteration)
