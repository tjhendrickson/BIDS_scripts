#!/usr/bin/python

from glob import glob
import os
import shutil
import argparse
from IntendedFor import setup
import sys
import pdb
import tarfile

#book keeping and global variables
parser = argparse.ArgumentParser(description='Script that controls BIDS conversion for individual studies')
parser.add_argument('--output_dir', help="The directory that the BIDS data will be outputted to")
parser.add_argument('--dicom_dir', help='The directory that houses dicom directories/files.')
parser.add_argument('--ses_id', help="scanning session id")
parser.add_argument('--subj_id', help="subject id")
parser.add_argument('--heuristic', help="Path to heuristic file, if the file is already within the container (i.e. within heuristics folder)"
										" you do not have to specify a path. ")
parser.add_argument('--dry_run', action='store_true', help="Dry run. A dicominfo_*.tsv file will generate within .heudiconv/'subj_id'/info directory which can be used to create heuristic script")

args = parser.parse_args()

pdb.set_trace()

#make bids directory if it does not exist
if not os.path.exists(os.path.join(args.output_dir, "BIDS_output")):
	os.makedirs(os.path.join(args.output_dir, "BIDS_output"))

# determine conversion type (i.e. dry run or heuristic)
if args.dry_run == True:
	convert_type = " -c none -f convertall"
else:
	if args.heuristic == None:
		raise Exception("If a dry_run is not being a conducted a heuristic script must be used. Re-run and place path within --heuristic argument.")
		sys.exit()
	else:
		heuristics_script = args.heuristic
		convert_type = " -c dcm2niix -f %s -b" % heuristics_script

#try to determine how data is organized within dicom directory, place within /tmp directory, and determine what heudiconv format (cross-sectional, longitudinal should look like)
if args.ses_id:
	if len(glob(args.dicom_dir + "/*" + args.ses_id + "*")) == 1:
		if args.subj_id:
			#is it a tar file? If so convert tar file directly
			if os.path.isfile(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0]):
				if tarfile.is_tarfile(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0]):
					shutil.copytree(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0],"/tmp/" + args.subj_id +"/" + args.ses_id)
					convert_format = '/neurodocker/startup.sh heudiconv "-d %s/{subject}/{session} -s %s -ss %s --overwrite -o %s/BIDS_output"' % ("/tmp",  args.subj_id, args.ses_id, args.output_dir)
			else:
				shutil.copytree(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0],"/tmp/" + args.subj_id +"/" + args.ses_id)
				convert_format = '/neurodocker/startup.sh heudiconv "-d %s/{subject}/{session}/*/* -s %s -ss %s --overwrite -o %s/BIDS_output"' % ("/tmp",  args.subj_id, args.ses_id, args.output_dir)
		else:
			if os.path.isfile(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0]):
				if tarfile.is_tarfile(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0]):
					convert_format = '/neurodocker/startup.sh heudiconv "-d %s/*{subject}* -s %s --overwrite -o %s/BIDS_output"' % (args.dicom_dir, args.ses_id, args.output_dir)
			else:
				shutil.copytree(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0],"/tmp/" + args.ses_id)
				convert_format = '/neurodocker/startup.sh heudiconv "-d %s/{subject}/*/* -s %s --overwrite -o %s/BIDS_output"' % ("/tmp",  args.ses_id, args.output_dir)
	# if ses_id does not exist but subj_id does use ses_id argument to create ses folder
	elif len(glob(args.dicom_dir + "/*" + args.ses_id + "*")) == 0:
		if len(glob(args.dicom_dir + "/*" + args.subj_id + "*")) == 1:
			if os.path.isfile(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0]):
				if tarfile.is_tarfile(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0]):
					convert_format = '/neurodocker/startup.sh heudiconv "-d %s/*{subject}* -s %s --overwrite -o %s/BIDS_output"' % (args.dicom_dir,  args.subj_id, args.output_dir)
			else:
				shutil.copytree(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0],"/tmp/" + args.subj_id + "/" + args.ses_id)
				convert_format = '/neurodocker/startup.sh heudiconv "-d %s/{subject}/{session}/*/* -s %s -ss %s --overwrite -o %s/BIDS_output"' % ("/tmp",  args.subj_id, args.ses_id, args.output_dir)
		elif len(glob(args.dicom_dir + "/*" + args.subj_id + "*")) > 1:
			raise Exception("There are multiple directories within dicom directory: " + args.dicom_dir + " with the same subjct id: " + args.subj_id + ". Must exit.")
		else:
			raise Exception("Cannot find a directory within dicom directory: " + args.dicom_dir + " with the session id: " + args.subj_id + ". Must exit.")

	elif len(glob(args.dicom_dir + "/*" + args.ses_id + "*")) > 1:
		raise Exception("There are multiple directories within dicom directory: " + args.dicom_dir + " with the same session id: " + args.ses_id + ". Must exit.")
	else:
		raise Exception("Cannot find a directory within dicom directory: " + args.dicom_dir + " with the session id: " + args.ses_id + ". Must exit.")
else:
	if args.subj_id:
		if len(glob(args.dicom_dir + "/*" + args.subj_id + "*")) == 1:
			if os.path.isfile(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0]):
				if tarfile.is_tarfile(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0]):
					convert_format = '/neurodocker/startup.sh heudiconv "-d %s/*{subject}* -s %s --overwrite -o %s/BIDS_output"' % (args.dicom_dir,  args.subj_id, args.output_dir)
			else:
				shutil.copytree(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0],"/tmp/" + args.subj_id)
				convert_format = '/neurodocker/startup.sh heudiconv "-d %s/{subject}/*/* -s %s --overwrite -o %s/BIDS_output"' % ("/tmp",  args.subj_id, args.output_dir)
		elif len(glob(args.dicom_dir + "/*" + args.subj_id + "*")) > 1:
			raise Exception("There are multiple directories within dicom directory: " + args.dicom_dir + " with the same subjct id: " + args.subj_id + ". Must exit.")
		else:
			raise Exception("Cannot find a directory within dicom directory: " + args.dicom_dir + " with the session id: " + args.subj_id + ". Must exit.")
	else:
		raise Exception("Neither subject id nor session id were entered, at least one (preferably both) are required in order to convert data")

os.system(convert_format + convert_type)

#once conversion is finished delete data from tmp
if args.subj_id:
	if os.path.isdir("/tmp/" + args.subj_id):
		shutil.rmtree("/tmp/" + args.subj_id)
elif args.ses_id:
	if os.path.isdir("/tmp/" + args.ses_id):
		shutil.rmtree("/tmp/" + args.ses_id)


#now change IntendedFor field within fmaps
if args.dry_run == False:
	setup(os.path.join(args.output_dir, "BIDS_output", "sub-"+args.subj_id))
