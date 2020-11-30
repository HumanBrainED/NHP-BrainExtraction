## U-Net model and PRIME-DE skull-stripped brain masks (pre-release)

Date: Nov 12th, 2020

----
## Descriptions
This is a pre-release of skull-stripped brian masks of T1w images for 136 macaque monkeys (20 sites) from [PRIME-DE](http://fcon_1000.projects.nitrc.org/indi/indiPRIME.html). The masks are created from a convolutional network - UNet model, initially trained on a human sample and upgraded with macaque data.

## Overview 

### A glance of the performance for different pipelines across 136 macaques (20 sites)
[UNet 12+7 Model](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/vcheck_summary_UNet12%2B7.md)

[AFNI @animal_warper](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/vcheck_summary_AFNI-animalwarper.md)

[AFNI 3dSkullStrip](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/vcheck_summary_AFNI-3dSkullStrip.md)

[FLIRT+ANTS](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/vcheck_summary_FLIRT%2BANTS.md)

[FSL BET](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/vcheck_summary_FS.md)

[FreeSurfer](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/vcheck_summary_FS.md)

## Docker Image
#### Pull
Pre-release docker image has been uploaded onto DockerHub, you could download it by using the following command
```
docker pull sandywangrest/deepbet:latest
```

#### Helper
For the usage of this image, please running
```
docker run sandywangrest/deepbet
```

## UNet Model
----
#### Installation

python3, numpy, pytorch, nibabel

#### Run brain mask prediction
```
python3 /path_to_the_code/muSkullStrip.py -in /path_to_the_data/input_t1.nii.gz -model /path_to_the_model/selected_model.model -out /path_to_the_output_directory
```
Output: *_pre_mask.nii.gz

#### Custimize the model for your own dataset 
```
python3 /path_to_the_code/trainSs_UNet.py -trt1w /directory_of_the_training_images -trmsk /directory_of_the_training_image_masks -out /output_directory -vt1w /directory_of_the_validation_images -vmsk /directory_of_the_validation_image_masks -init /initial_model_to_start_with
```
Note: Our macaque model was a transfer-learning model using a human dataset as the 'initial model' (-init option). You can use the model we provided to custimize the model for your own dataset (even across species). 


#### The trained models can be used in prediction (**muSkullStrip.py -model**) or model-updating (**trainSs_Unet.py -init**)
1. **Site-All-T-epoch_36.model**: Trained on 12 macaques across 6 sites (2 macaques per site) from PRIME-DE. Six sites include newcastle, ucdavis, oxford, ion, ecnu-chen, and sbri.

2. **Site-All-T-epoch_36_update_with_Site_6_plus_7-epoch_09.model**: Trained on 19 macaques across 13 sites from PRIME-DE (12 macaques across 6 sites used in the first model and 7 macaques across 7 additional sites) Seven sites include NIMH, ecnu-k, nin, rockefeller, uwo, mountsinai-S, and lyon.

3. **Site-All-T-epoch_36_update_with_Site_*.model**: Site-specific model for NIMH, ecnu-k, nin, rockefeller, uwo, mountsinai-S, and lyon.

### [Download the code and models](https://github.com/HumanBrainED/NHP-BrainExtraction/tree/master/UNet_Model)

#### Manually edited brain masks for transfer-learning training (12 macaque monkeys from 6 sites, 2 per site)
![Training masks](https://github.com/TingsterX/PRIME-DE/blob/master/BrainExtraction/release/1_train12.gif)

#### Manually edited brain masks for model-updating training (7 macaque monkeys from 7 sites, 1 per site)
![Testing masks](https://github.com/TingsterX/PRIME-DE/blob/master/BrainExtraction/release/2_train7.gif)

#### Brain masks for 136 macaque monkeys (released mask)
![release](https://github.com/TingsterX/PRIME-DE/blob/master/BrainExtraction/release/4_release.gif)

### [Download brain masks (136 macaques)](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/brainmasks/brainmask_T1w_136macaques.tar)

Reference:
[OHBM2019 poster](https://ww5.aievolution.com/hbm1901/index.cfm?do=abs.viewAbs&abs=4924)

Paper: [biorxiv preprint](https://biorxiv.org/cgi/content/short/2020.11.17.385898v1)

