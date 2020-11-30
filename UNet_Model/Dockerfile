# Use PyTorch Latest Version
FROM pytorch/pytorch

# Install Scipy Nibabel Libary
RUN pip install scipy nibabel

# Copy UNet Codes and Models into Image
COPY *.py /UNet_Model/
COPY models/*.model /UNet_Model/models/

# Add UNet Path into ENV
ENV DIMGNAME="sandywangrest/deepbet" \
    PYTHONPATH="/UNet_Model:$PYTHONPATH" \
    PATH="/UNet_Model:/UNet_Model/models/:$PATH"

WORKDIR /UNet_Model/models
CMD docker_Help.py
