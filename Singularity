# Read in singularity heudiconv image version 0.5.3.1
Bootstrap: shub
From: ReproNim/reproin:0.5.3.1


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
	mkdir /output_dir 
    mkdir /dicom_dir
    touch /heuristic.py

	
	# Install python and nibabel
	# Read in singularity heudiconv image version 0.5.3.1
Bootstrap: shub
From: ReproNim/reproin:0.5.3.1


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
	mkdir /output_dir 
    mkdir /dicom_dir
    touch /heuristic.py

	
	# Install python and nibabel
	wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.2-Linux-x86_64.sh
	apt-get update -y && \
	apt-get install -y python3 python3-pip && \
	pip3 install nibabel && \
	apt-get remove -y python3-pip && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

	# Install python Dependencies
	apt-get update -y && apt-get install -y --no-install-recommends python-pip python-six python-nibabel python-setuptools
	pip install pybids==0.5.1
	pip install --upgrade pybids
	apt-get update -y && \
	apt-get install -y python3 python3-pip && \
	pip3 install nibabel && \
	apt-get remove -y python3-pip && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

	# Install python Dependencies
	apt-get update -y && apt-get install -y --no-install-recommends python-pip python-six python-nibabel python-setuptools
	pip3 install pybids==0.5.1
	pip install --upgrade pybids



