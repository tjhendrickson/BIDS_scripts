Bootstrap: docker
From: tjhendrickson/bids_scripts:latest

%runscript

	exec /run.py "$@"

%post

	# Make script executable
	chmod +x /run.py

	# Make local folders
	mkdir /share
	mkdir /scratch
	mkdir /local-scratch
