# Read in heudiconv docker image
Bootstrap: docker
From: nipy/heudiconv


%environment
	export DEBIAN_FRONTEND=noninteractive
	export PYTHONPATH=""

%runscript

	exec /run.py "$@"


%files
	run.py /run.py
	heuristics /heuristics
	IntendedFor.py /IntendedFor.py

%post
	
	export DEBIAN_FRONTEND=noninteractive
	export PYTHONPATH=""

	
	# Make script executable
	chmod +x /run.py

	# Make local folders
	mkdir /share
	mkdir /scratch
	mkdir /local-scratch
	mkdir /output_dir 
    mkdir /temp_dir
    touch /heuristic.py

	
	# Install python and nibabel
	apt-get update -y && \
	apt-get install -y python3 python3-pip && \
	pip3 install nibabel && \
	apt-get remove -y python3-pip && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

	# Install python Dependencies
	apt-get update -y && apt-get install -y --no-install-recommends python-pip python-six python-nibabel python-setuptools
	pip install pybids==0.5.1
	pip install --upgrade pybids

	## Install the validator
	apt-get update -y && \
	apt-get install -y curl && \
	curl -sL https://deb.nodesource.com/setup_6.x | bash - && \
	apt-get remove -y curl && \
	apt-get install -y nodejs

	npm install -g bids-validator@0.25.7



