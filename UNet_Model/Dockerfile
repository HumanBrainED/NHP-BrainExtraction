# Use PyTorch Latest Version
FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime
MAINTAINER Xindi Wang <sandywang.rest@gmail.com>

# Install Scipy Nibabel Libary
RUN pip install scipy nibabel

# Copy UNet Codes and Models into Image
COPY *.py /UNet_Model/
COPY models/*.model /UNet_Model/models/
# If you would like to reduce the size of images by removing some models, uncomment
# COPY models/Site-All-T-epoch_36_update_with_Site_6_plus_7-epoch_09.model /UNet_Model/models/

# Add UNet Path into ENV
ENV DIMGNAME="sandywangrest/deepbet" \
    PYTHONPATH="/UNet_Model:$PYTHONPATH" \
    PATH="/UNet_Model:/UNet_Model/models/:$PATH"

WORKDIR /UNet_Model/models
CMD docker_Help.py
