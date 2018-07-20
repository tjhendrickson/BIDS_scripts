#!/usr/bin/python

from glob import glob
import os
import shutil
import argparse
from IntendedFor import setup
import pdb

#book keeping and global variables
parser = argparse.ArgumentParser(description='Script that controls BIDS conversion for individual studies')
parser.add_argument('--output_dir', help="The directory that the BIDS data will be outputted to")
parser.add_argument('--temp_dir', help='The directory that will temporarily house dicom directories.')
parser.add_argument('--study_name', help="What is the shorthand name for this study?")
parser.add_argument('--proc_id', help="scanning session id")
parser.add_argument('--subj_id', help="subject id")
parser.add_argument('--heuristic', help="Path to heuristic file, if the file is already within the container (i.e. within heuristics folder)"
										" you do not have to specify a path. ")

args = parser.parse_args()

output_dir = args.output_dir
temp_dir = args.temp_dir
study_name = args.study_name
proc_id = args.proc_id
subj_id = args.subj_id

if args.heuristic == None:
	heuristics_script = "/heuristics/" + study_name + "_heuristics.py"
	if not os.path.exists(heuristics_script):
		raise Exception("The heuristics script with the path /heuristics/'study_name'_heuristics.py does not exist."
						 " Re-run and place path within --heuristic argument.")
else:
	heuristics_script = args.heuristic


if not os.path.exists(os.path.join(output_dir, "BIDS_output")):
	os.makedirs(os.path.join(output_dir, "BIDS_output"))

if not os.path.exists(os.path.join(temp_dir, subj_id)):
	os.makedirs(os.path.join(temp_dir, subj_id))

if not os.path.exists(os.path.join(temp_dir, subj_id, proc_id)):
	shutil.move(os.path.join(temp_dir, proc_id), (os.path.join(temp_dir, subj_id, proc_id)))

os.system('/neurodocker/startup.sh heudiconv '
		  '"-d %s/{subject}/{session}/*/*.dcm -s %s -ss %s --overwrite -o %s/BIDS_output -c dcm2niix -f %s -b" '
		  % (temp_dir,  subj_id, proc_id, output_dir, heuristics_script))

#now change IntendedFor field within fmaps
setup(os.path.join(output_dir, "BIDS_output", "sub-"+subj_id))
