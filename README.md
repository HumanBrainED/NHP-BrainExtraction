## DeepBet - U-Net Brain extraction tool for nonhuman primates

Date: April 12th, 2021

----
## Description
This repo includes the brain extraction tool (DeepBet v1.0) for skull-stripping the nonhuman primate images. We also include brain masks of 136 macaque monkeys (20 sites) from [PRIME-DE](http://fcon_1000.projects.nitrc.org/indi/indiPRIME.html). The tool is constructed using a convolutional network - UNet model, initially trained on a [human sample](https://academic.oup.com/gigascience/article/5/1/s13742-016-0150-5/2737425) and updated with macaque data. 

In this repo, we also include the outputs from other tools (AFNI, FSL, FreeSurfer, ANTS) - [a glance of the performance for different pipelines](#A-galance-of-performance-for-different-pipelines)

Reference: [Wang et al., U-net model for brain extraction: Trained on humans for transfer to non-human primates, 2021, NeuroImage](https://www.sciencedirect.com/science/article/pii/S1053811921002780)

## Docker Image
#### Pull
The docker image has been uploaded onto DockerHub, download it by using the following command
```
docker pull sandywangrest/deepbet:1.0
```

#### Helper
For the usage of this image, run
```
docker run sandywangrest/deepbet
```

#### Storage Requirement
~5GB hard disk space for whole docker image, including pytorch (~4GB), nibabel, scipy (~188MB), 12 U-Net models (356MB) and our code (44KB)

## U-Net model
----
#### Local installation 

python3, numpy, pytorch, nibabel, scipy

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

4. **Site-All-T-epoch_36_update_with_Site_Pigs_09.model**: The **pig** model - Trained on 12 macaques and updated with the pig data (N=3).

### [Download the models](https://github.com/HumanBrainED/NHP-BrainExtraction/tree/master/UNet_Model)

#### Manually edited brain masks for transfer-learning training (12 macaque monkeys from 6 sites, 2 per site)
![Training masks](https://github.com/TingsterX/PRIME-DE/blob/master/BrainExtraction/release/1_train12.gif)

#### Manually edited brain masks for model-updating training (7 macaque monkeys from 7 sites, 1 per site)
![Testing masks](https://github.com/TingsterX/PRIME-DE/blob/master/BrainExtraction/release/2_train7.gif)

#### Brain masks for 136 macaque monkeys (released mask)
![release](https://github.com/TingsterX/PRIME-DE/blob/master/BrainExtraction/release/4_release.gif)

### [Download brain masks (136 macaques)](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/brainmasks/brainmask_T1w_136macaques.tar)

### A galance of performance for different pipelines 
#### Data: 136 macaques (20 sites) from [PRIME-DE](http://fcon_1000.projects.nitrc.org/indi/indiPRIME.html).

[UNet 12+7 Model](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/vcheck_summary_UNet12%2B7.md)

[AFNI @animal_warper](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/vcheck_summary_AFNI-animalwarper.md)

[AFNI 3dSkullStrip](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/vcheck_summary_AFNI-3dSkullStrip.md)

[FLIRT+ANTS](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/vcheck_summary_FLIRT%2BANTS.md)

[FSL BET](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/vcheck_summary_FSL.md)

[FSL+ BET](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/vcheck_summary_FSL+.md)

[FreeSurfer](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/vcheck_summary_FS.md)

[FreeSurfer+](https://github.com/HumanBrainED/NHP-BrainExtraction/blob/master/PRIME-DE_BrainMask/vcheck_summary_FS+.md)

Reference: [Wang et al., U-net model for brain extraction: Trained on humans for transfer to non-human primates, 2021, NeuroImage](https://www.sciencedirect.com/science/article/pii/S1053811921002780)
