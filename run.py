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
parser.add_argument('--dicom_dir', help='The directory that houses unzipped and untarred dicom directories/files.')
parser.add_argument('--study_name', help="What is the shorthand name for this study?")
parser.add_argument('--ses_id', help="scanning session id")
parser.add_argument('--subj_id', help="subject id")
parser.add_argument('--heuristic', help="Path to heuristic file, if the file is already within the container (i.e. within heuristics folder)"
										" you do not have to specify a path. ")
parser.add_argument('--dry_run', action='store_true', help="Dry run. A dicominfo_*.tsv file will generate within .heudiconv/'subj_id'/info directory which can be used to create heuristic script")

args = parser.parse_args()

#make bids directory if it does not exist
if not os.path.exists(os.path.join(args.output_dir, "BIDS_output")):
	os.makedirs(os.path.join(args.output_dir, "BIDS_output"))

# determine conversion type (i.e. dry run or heuristic)
if args.dry_run == True:
	convert_type = " -c none -f convertall" 
else:
	if args.heuristic == None:
		heuristics_script = "/heuristics/" + args.study_name + "_heuristics.py"
		if not os.path.exists(heuristics_script):
			raise Exception("The heuristics script with the path /heuristics/'study_name'_heuristics.py does not exist."
							 " Re-run and place path within --heuristic argument.")
		else:
			convert_type = " -c dcm2niix -f %s -b" % heuristics_script
	else:
		heuristics_script = args.heuristic
		convert_type = " -c dcm2niix -f %s -b" % heuristics_script

	
#try to determine how data is organized within dicom directory, place within /tmp directory, and determine what heudiconv format (cross-sectional, longitudinal should look like)
if args.ses_id:
	if len(glob(args.dicom_dir + "/*" + args.ses_id + "*")) == 1:
		if args.subj_id:
			shutil.copytree(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0],"/tmp/" + args.subj_id +"/" + args.ses_id)
			convert_format = '/neurodocker/startup.sh heudiconv "-d %s/{subject}/{session}/*/* -s %s -ss %s --overwrite -o %s/BIDS_output"' % ("/tmp",  args.subj_id, args.ses_id, args.output_dir)
		else:
			shutil.copytree(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0],"/tmp/" + args.subj_id)
			convert_format = '/neurodocker/startup.sh heudiconv "-d %s/{subject}/*/* -s %s --overwrite -o %s/BIDS_output"' % ("/tmp",  args.subj_id, args.output_dir)
	elif len(glob(args.dicom_dir + "/*" + args.ses_id + "*")) > 1:
		raise Exception("There are multiple directories within dicom directory: " + args.dicom_dir + " with the same session id: " + args.ses_id + ". Must exit.")
	else:
		raise Exception("Cannot find a directory within dicom directory: " + args.dicom_dir + " with the session id: " + args.ses_id + ". Must exit.")
else:
	if args.subj_id:
		if len(glob(args.dicom_dir + "/*" + args.subj_id + "*")) == 1:
			shutil.copytree(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0],"/tmp/" + args.subj_id)	
			convert_format = '/neurodocker/startup.sh heudiconv "-d %s/{subject}/*/* -s %s --overwrite -o %s/BIDS_output"' % ("/tmp",  args.subj_id, args.output_dir)
		elif len(glob(args.dicom_dir + "/*" + args.ses_id + "*")) > 1:
			raise Exception("There are multiple directories within dicom directory: " + args.dicom_dir + " with the same subjct id: " + args.subj_id + ". Must exit.")
		else:
			raise Exception("Cannot find a directory within dicom directory: " + args.dicom_dir + " with the session id: " + args.subj_id + ". Must exit.")
	else:
		raise Exception("Neither subject id nor session id were entered, at least one (preferably both) are required in order to convert data")




#if not os.path.exists(os.path.join(args.dicom_dir, args.subj_id)):
#	os.makedirs(os.path.join(args.dicom_dir, args.subj_id))

#if not os.path.exists(os.path.join(args.dicom_dir, args.subj_id, args.ses_id)):
#	shutil.move(os.path.join(args.dicom_dir, args.ses_id), (os.path.join(args.dicom_dir, args.subj_id, args.ses_id)))

os.system(convert_format + convert_type)

#once conversion is finished delete data from tmp
if args.subj_id:
	shutil.rmtree("/tmp/" + args.subj_id)
else:
	shutil.rmtree("/tmp/" + args.ses_id)


#now change IntendedFor field within fmaps
if args.dry_run == False:
	setup(os.path.join(args.output_dir, "BIDS_output", "sub-"+args.subj_id))
