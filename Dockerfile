# Read in ubuntu based docker image
FROM ubuntu:xenial-20210429

#Environment
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH=""

# Install needed UBUNTU packages
RUN apt-get update && \
    apt-get install -y curl git

# Install python 3.7 most recent stable miniconda version 4.9.2
RUN echo "Installing miniconda ..." && \
    curl -sSLO https://repo.anaconda.com/miniconda/Miniconda3-py37_4.9.2-Linux-x86_64.sh && \
    bash Miniconda3-py37_4.9.2-Linux-x86_64.sh -b -p /usr/local/miniconda && \
    rm Miniconda3-py37_4.9.2-Linux-x86_64.sh 

# Add miniconda to path and set other environment variables
ENV PATH="/usr/local/miniconda/bin:$PATH" \
    CPATH="/usr/local/miniconda/include:$CPATH" \
    LANG="C.UTF-8" \
    LC_ALL="C.UTF-8" \
    PYTHONNOUSERSITE=1 \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONPATH=""

# download heudiconv repo
RUN mkdir github && \
    cd github && \
    git clone https://github.com/nipy/heudiconv.git && \
    cd heudiconv && \
    git checkout tags/debian/0.9.0-2 -b debian-0.9.0-2

# create conda environment
RUN conda create -n heudiconv
# Install Dependencies
SHELL ["conda", "run", "-n", "heudiconv", "conda", "install", "pip"]
SHELL ["conda", "run", "-n", "heudiconv", "conda", "install", "-c", "conda-forge", "datalad"]
SHELL ["conda", "run", "-n", "heudiconv", "/bin/bash", "-c", "pip", "install", "-r", "requirements.txt"]

COPY run.py /run.py
COPY heuristics /heuristics
COPY IntendedFor.py /IntendedFor.py

#make /bids_dir and /output_dir
RUN mkdir /output_dir && \
    mkdir /tmp_dir && \
    touch /heuristic.py

ENTRYPOINT ["conda", "run", "-n", "heudiconv", "python", "/run.py"]
