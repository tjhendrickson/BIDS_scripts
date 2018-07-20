# Read in heudiconv docker image
FROM nipy/heudiconv

#Environment
ENV DEBIAN_FRONTEND=noninteractive

# Install python and nibabel
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install nibabel && \
    apt-get remove -y python3-pip && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install python Dependencies
RUN apt-get update -y && apt-get install -y --no-install-recommends python-pip python-six python-nibabel python-setuptools
RUN pip install pybids==0.5.1
RUN pip install --upgrade pybids

## Install the validator
RUN apt-get update -y && \
    apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_6.x | bash - && \
    apt-get remove -y curl && \
    apt-get install -y nodejs

RUN npm install -g bids-validator@0.25.7

ENV PYTHONPATH=""

COPY run.py /run.py
COPY heuristics /heuristics
COPY IntendedFor.py /IntendedFor.py

#make /bids_dir and /output_dir
RUN mkdir /output_dir && \
    mkdir /tmp_dir && \
    touch /heuristic.py

ENTRYPOINT ["/run.py"]
