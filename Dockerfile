FROM nvidia/cuda:12.6.3-cudnn-runtime-ubuntu22.04
LABEL authors="Christoffer"

ENV PATH="/usr/local/cuda/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"

# Update the package lists and install the necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-client \
    cuda-toolkit-12-6 \
    git \
    python3 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/* \

COPY . /TsetlinHexGame

RUN pip3 install -r requirements.txt