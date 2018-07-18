#.74 !/usr/bin/python

from glob import glob
import os
import shutil
import argparse
from IntendedFor import setup

#book keeping and global variables
parser = argparse.ArgumentParser(description='Script that controls BIDS conversion for individual studies')
parser.add_argument('--output_dir', help="The directory that the BIDS data will be outputted to")
parser.add_argument('--temp_dir', help='The directory that will temporarily house dicom directories.')
parser.add_argument('--study_name', help="What is the shorthand name for this study?")
parser.add_argument('--proc_id', help="scanning session id")
parser.add_argument('--subj_id', help="subject id")

args = parser.parse_args()

output_dir = args.output_dir
temp_dir = args.temp_dir
study_name = args.study_name
proc_id = args.proc_id
subj_id = args.subj_id

heuristics_script = study_name + "_heuristics.py"

if not os.path.exists(os.path.join(output_dir, "BIDS_output")):
	os.makedirs(os.path.join(output_dir, "BIDS_output"))

if not os.path.exists(os.path.join(temp_dir, subj_id)):
	os.makedirs(os.path.join(temp_dir, subj_id))

if not os.path.exists(os.path.join(temp_dir, subj_id, proc_id)):
	shutil.move(os.path.join(temp_dir, proc_id), (os.path.join(temp_dir, subj_id, proc_id)))

os.system('/neurodocker/startup.sh heudiconv "-d %s/{subject}/{session}/*/*.dcm -s %s -ss %s --overwrite -o %s/BIDS_output -c dcm2niix -f /heuristics/%s -b" '
		  % (temp_dir,  subj_id, proc_id, output_dir, heuristics_script))

#now change IntendedFor field within fmaps
setup(os.path.join(output_dir, "BIDS_output", "sub-"+subj_id))
