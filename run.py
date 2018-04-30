#!/home/lnpi14-raid1/timothy-data-lnpi14/nipype_python_2.7.10/bin python
from glob import glob
import os
import shutil
import argparse


#book keeping and global variables
parser = argparse.ArgumentParser(description='Script that controls BIDS conversion for individual studies')
parser.add_argument('--top_level_dir', help="The directory this script is being called from, it should also have the heuristics script within.")
parser.add_argument('--output_dir', help="The directory that the BIDS data will be outputted to")
parser.add_argument('--temp_dir', help='The directory that will temporarily house dicom directories.')
parser.add_argument('--study_name', help="What is the shorthand name for this study?")
parser.add_argument('--proc_id', help="5 digit proc number (AKA event ID from GRID)")
parser.add_argument('--subj_id', help="4 digit subject number (AKA subject id from GRID)")
parser.add_argument('--container', help="location of docker or udocker install")


args = parser.parse_args()

top_level_dir = args.top_level_dir
output_dir = args.output_dir
temp_dir = args.temp_dir
study_name = args.study_name
proc_id = args.proc_id
subj_id = args.subj_id
container = args.container
heuristics_script = study_name + "_heuristics.py"

if not os.path.exists(os.path.join(top_level_dir, output_dir)):
	os.makedirs(os.path.join(top_level_dir,output_dir))

if not os.path.exists(os.path.join(temp_dir, subj_id)):
	os.makedirs(os.path.join(temp_dir, subj_id))

if not os.path.exists(heuristics_script):
	raise EnvironmentError("Heuristics script for " + study_name + " does not exist, it must be in the top level directory: " + top_level_dir)


os.rename(glob("%s/PN-%s*" % (temp_dir, proc_id))[0], "%s/%s" % (temp_dir, proc_id))
shutil.move(os.path.join(temp_dir, proc_id), (os.path.join(temp_dir, subj_id)))
os.system('/bin/bash -c "%s run -v $PWD:/home/tim -v %s/:/home/tim/data \
-v %s/%s:/home/tim/%s run_heudiconv -d /home/tim/data/{subj_idect}/{session}/*/*.dcm -s %s \
-ss %s --overwrite -o /home/tim/%s -c dcm2niix -f /home/tim/%s -b"'
		  % (container, temp_dir, top_level_dir, heuristics_script, heuristics_script, subj_id, proc_id, output_dir, heuristics_script))

