#!/usr/bin/env python
import os

def docker_help(ImgName):
    query = """=============================%s helper=============================
  --------------------------
  Permforming Skullstripping 

    + With GPU:
        docker run --gpus all -v (your work directory):/data \ 
            %s \ 
            muSkullStrip.py \ 
                -in /data/(specified NIfTI file) \ 
                -model Site-All-T-epoch_36_update_with_Site_6_plus_7-epoch_09.model
                (optional arguments)

    + Without GPU:
        docker run -v (your work directory):/data \ 
            %s \ 
            muSkullStrip.py \ 
                -in /data/(specified NIfTI file) \ 
                -model Site-All-T-epoch_36_update_with_Site_6_plus_7-epoch_09.model
                (optional arguments)

    + Optional arguments see help for muSkullStrip.py
        docker run %s muSkullStrip.py
      
    + Use custimized model, add
        -v (Path of model for testing):/Models
        -model /Models/(your model)

  -------------------------  
  Traing & Updating Models 

    + With GPU:
        docker run --gpus all \ 
            -v (Path of T1w images for training):/TrainT1w \ 
            -v (Path of T1w masks for training):/TrainMsk \ 
            -v (Path of trained model and log):/Results \ 
            %s \ 
            trainSs_UNet.py \ 
                -trt1w /TrainT1w \ 
                -trmsk /TrainMsk \ 
                -out /Results  
                (optional arguments)

    + Without GPU:
        docker run \ 
            -v (Path of T1w images for training):/TrainT1w \ 
            -v (Path of T1w masks for training):/TrainMsk \ 
            -v (Path of trained model and log):/Results \ 
            %s \ 
            trainSs_UNet.py \ 
                -trt1w /TrainT1w \ 
                -trmsk /TrainMsk \ 
                -out /Results  
                (optional arguments)

    + Optimal arguments see help for trainSs_UNet.py
        docker run %s trainSs_UNet.py

  --------------------------
  Testing Models

    + With GPU:
        docker run --gpus all \ 
            -v (Path of T1w images for training):/TestT1w \ 
            -v (Path of T1w masks for training):/TestMsk \ 
            -v (Path of model for testing):/Models \ 
            -v (Path of log):/Results \ 
            %s \ 
            testSs_UNet.py \ 
                -tet1w /TrainT1w \ 
                -temsk /TrainMsk \ 
                -model /Models/(your model for testing) \ 
                -out /Results  
                (optional arguments)

    + Without GPU:
        docker run \ 
            -v (Path of T1w images for training):/TestT1w \ 
            -v (Path of T1w masks for training):/TestMsk \ 
            -v (Path of model for testing):/Models \ 
            -v (Path of log):/Results \ 
            %s \ 
            testSs_UNet.py \ 
                -tet1w /TrainT1w \ 
                -temsk /TrainMsk \ 
                -model /Models/(your model for testing) \ 
                -out /Results  
                (optional arguments)
  
    + Optimal arguments see help for testSs_UNet.py
        docker run %s testSs_UNet.py

  --------------------------
  Listing Models in Container

    docker run %s ls

  NOTE: To use --gpus option, you need install nvidia-container-toolkit
            """ % \
                (ImgName, ImgName, ImgName, ImgName, ImgName, ImgName, 
                ImgName, ImgName, ImgName, ImgName, ImgName)
    print(query)

if __name__=='__main__':
    ImgName=os.getenv("DIMGNAME")
    docker_help(ImgName)
