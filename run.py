#!/usr/bin/python

from glob import glob
import os
import shutil
import argparse
from IntendedFor import setup
import sys
import pdb
import tarfile
import re

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


# make bids directory if it does not exist
if not os.path.exists(os.path.join(args.output_dir, "BIDS_output")):
    os.makedirs(os.path.join(args.output_dir, "BIDS_output"))

# determine conversion type (i.e. dry run or heuristic)
if args.dry_run:
    convert_type = ' -c none -f convertall'
else:
    if not args.heuristic:
        raise Exception("If a dry_run is not being a conducted a heuristic script must be used. Re-run and place path within --heuristic argument.")
        sys.exit()
    else:
        heuristics_script = args.heuristic
        convert_type = ' -c dcm2niix -f %s -b' % heuristics_script

# try to determine how data is organized within dicom directory, place within /tmp directory, and determine what heudiconv format (cross-sectional, longitudinal should look like)

# just subj_id
if args.subj_id and not args.ses_id:
    if len(glob(args.dicom_dir + "/*" + args.subj_id + "*")) == 1:
        if os.path.isfile(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0]):
            if tarfile.is_tarfile(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0]):
                convert_format = '/neurodocker/startup.sh heudiconv -d %s/*{subject}* -s %s --overwrite -o %s/BIDS_output' % ("/tmp",  args.subj_id, args.output_dir)
        elif os.path.isdir(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0]):
            shutil.copytree(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0],"/tmp/" + args.subj_id)
            convert_format = '/neurodocker/startup.sh heudiconv -d %s/{subject}/*/* -s %s  --overwrite -o %s/BIDS_output' % ("/tmp",  args.subj_id, args.output_dir)
    elif len(glob(args.dicom_dir + "/*" + args.subj_id + "*")) > 1:
        raise Exception("There are multiple directories within dicom directory: " + args.dicom_dir + " with the same subject id: " + args.subj_id + ". Either change the subject id or enter a session id. Must exit.")
    else:
        raise Exception("Cannot find a directory within dicom directory: " + args.dicom_dir + " with the subject id: " + args.subj_id + ". Must exit.")

#just ses id
elif args.ses_id and not args.subj_id:
    if len(glob(args.dicom_dir + "/*" + args.ses_id + "*")) == 1:
        if os.path.isfile(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0]):
            if tarfile.is_tarfile(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0]):
                    convert_format = '/neurodocker/startup.sh heudiconv -d %s/*{subject}* -s %s --overwrite -o %s/BIDS_output' % (args.dicom_dir,  args.ses_id, args.output_dir)
        elif os.path.isdir(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0]):
            shutil.copytree(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0],"/tmp/" + args.ses_id)
            convert_format = '/neurodocker/startup.sh heudiconv -d %s/{subject}/*/* -s %s --overwrite -o %s/BIDS_output' % ("/tmp",  args.ses_id, args.output_dir)
    elif len(glob(args.dicom_dir + "/*" + args.ses_id + "*")) > 1:
        raise Exception("There are multiple directories within dicom directory: " + args.dicom_dir + " with the same subject id: " + args.ses_id + ". Either change the subject id or enter a session id. Must exit.")
    else:
        raise Exception("Cannot find a directory within dicom directory: " + args.dicom_dir + " with the subject id: " + args.ses_id + ". Must exit.")

# subject id and session id
elif args.ses_id and args.subj_id:

    if len(glob(args.dicom_dir + "/*" + args.subj_id + "*/*" + args.ses_id + "*")) == 1:
        if os.path.isfile(glob(args.dicom_dir + "/*" + args.subj_id + "*/*" + args.ses_id + "*")[0]):
            if tarfile.is_tarfile(glob(args.dicom_dir + "/*" + args.subj_id + "*/*" + args.ses_id + "*")[0]):
                convert_format = '/neurodocker/startup.sh heudiconv -d %s/*{subject}*/*{session}* -s %s -ss %s --overwrite -o %s/BIDS_output' % (args.dicom_dir, args.subj_id, args.ses_id, args.output_dir)
        elif os.path.isdir(glob(args.dicom_dir + "/*" + args.subj_id + "*/*" + args.ses_id + "*")[0]):
            shutil.copytree(glob(args.dicom_dir + "/*" + args.subj_id + "*/*" + args.ses_id + "*")[0], "/tmp/" + args.subj_id + "/" + args.ses_id)
            convert_format = '/neurodocker/startup.sh heudiconv -d %s/{subject}/{session}/*/* -s %s -ss %s --overwrite -o %s/BIDS_output' % ("/tmp",  args.subj_id, args.ses_id, args.output_dir)
    
    elif len(glob(args.dicom_dir + "/*" + args.ses_id + "*/*" + args.subj_id + "*")) == 1:
        if os.path.isfile(glob(args.dicom_dir + "/*" + args.ses_id + "*/*" + args.subj_id + "*")[0]):
            if tarfile.is_tarfile(glob(args.dicom_dir + "/*" + args.ses_id + "*/*" + args.subj_id + "*")[0]):
                convert_format = '/neurodocker/startup.sh heudiconv -d %s/*{subject}*/*{session}* -s %s -ss %s --overwrite -o %s/BIDS_output' % (args.dicom_dir, args.ses_id, args.subj_id, args.output_dir)
        elif os.path.isdir(glob(args.dicom_dir + "/*" + args.ses_id + "*/*" + args.subj_id + "*")[0]):
            shutil.copytree(glob(args.dicom_dir + "/*" + args.ses_id + "*/*" + args.subj_id + "*")[0],"/tmp/" + args.subj_id)
            convert_format = '/neurodocker/startup.sh heudiconv -d %s/{subject}/{session}/*/* -s %s -ss %s --overwrite -o %s/BIDS_output' % ("/tmp",  args.ses_id, args.subj_id, args.output_dir)
    
    elif len(glob(args.dicom_dir + "/*" + args.subj_id + "*")) == 1:
        if os.path.isfile(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0]):
            if tarfile.is_tarfile(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0]):
                shutil.copy(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0],"/tmp/" + args.subj_id + "_" + args.ses_id + ".tar")
                convert_format = '/neurodocker/startup.sh heudiconv -d %s/{subject}_{session}.tar -s %s -ss %s --overwrite -o %s/BIDS_output' % ("/tmp", args.subj_id, args.ses_id, args.output_dir)
        elif os.path.isdir(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0]):
            shutil.copytree(glob(args.dicom_dir + "/*" + args.subj_id + "*")[0],"/tmp/" + args.subj_id + "/" + args.ses_id)
            convert_format = '/neurodocker/startup.sh heudiconv -d %s/{subject}/{session}/*/* -s %s -ss %s --overwrite -o %s/BIDS_output' % ("/tmp",  args.subj_id, args.ses_id, args.output_dir)

    elif len(glob(args.dicom_dir + "/*" + args.ses_id + "*")) == 1:
        if os.path.isfile(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0]):
            if tarfile.is_tarfile(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0]):
                shutil.copy(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0], "/tmp/" + args.subj_id + "_" + args.ses_id + ".tar")
                convert_format = '/neurodocker/startup.sh heudiconv -d %s/{subject}_{session}.tar -s %s -ss %s --overwrite -o %s/BIDS_output' % ("/tmp", args.subj_id, args.ses_id, args.output_dir)
        elif os.path.isdir(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0]):
            shutil.copytree(glob(args.dicom_dir + "/*" + args.ses_id + "*")[0], "/tmp/" + args.subj_id + "/" + args.ses_id)
            convert_format = '/neurodocker/startup.sh heudiconv -d %s/{subject}/{session}/*/* -s %s -ss %s --overwrite -o %s/BIDS_output' % ("/tmp", args.subj_id, args.ses_id, args.output_dir)
    
    elif len(glob(args.dicom_dir + "/*" + args.subj_id + "*" + args.ses_id + "*")) == 1:
        if os.path.isfile(glob(args.dicom_dir + "/*" + args.subj_id + "*" + args.ses_id + "*")[0]):
            if tarfile.is_tarfile(glob(args.dicom_dir + "/*" + args.subj_id + "*" + args.ses_id + "*")[0]):
                shutil.copy(glob(args.dicom_dir + "/*" + args.subj_id + "*" + args.ses_id + "*")[0], "/tmp/" + args.subj_id + "_" + args.ses_id + ".tar")
                convert_format = '/neurodocker/startup.sh heudiconv -d %s/{subject}_{session}.tar -s %s -ss %s --overwrite -o %s/BIDS_output' % ("/tmp", args.subj_id, args.ses_id, args.output_dir)
        elif os.path.isdir(glob(args.dicom_dir + "/*" + args.subj_id + "*" + args.ses_id + "*")[0]):
            shutil.copytree(glob(args.dicom_dir + "/*" + args.subj_id + "*" + args.ses_id + "*")[0], "/tmp/" + args.subj_id + "/" + args.ses_id)
            convert_format = '/neurodocker/startup.sh heudiconv -d %s/{subject}/{session}/*/* -s %s -ss %s --overwrite -o %s/BIDS_output' % ("/tmp", args.subj_id, args.ses_id, args.output_dir)

    elif len(glob(args.dicom_dir + "/*" + args.ses_id + "*" + args.subj_id + "*")) == 1:
        if os.path.isfile(glob(args.dicom_dir + "/*" + args.ses_id + "*" + args.subj_id + "*")[0]):
            if tarfile.is_tarfile(glob(args.dicom_dir + "/*" + args.ses_id + "*" + args.subj_id + "*")[0]):
                shutil.copy(glob(args.dicom_dir + "/*" + args.ses_id + "*" + args.subj_id + "*")[0], "/tmp/" + args.ses_id + "_" + args.subj_id + ".tar")
                convert_format = '/neurodocker/startup.sh heudiconv -d %s/{subject}_{session}.tar -s %s -ss %s --overwrite -o %s/BIDS_output' % ("/tmp", args.subj_id, args.ses_id, args.output_dir)
        elif os.path.isdir(glob(args.dicom_dir + "/*" + args.ses_id + "*" + args.subj_id + "*")[0]):
            shutil.copytree(glob(args.dicom_dir + "/*" + args.ses_id + "*" + args.subj_id + "*")[0], "/tmp/" + args.subj_id + "/" + args.ses_id)
            convert_format = '/neurodocker/startup.sh heudiconv -d %s/{subject}/{session}/*/* -s %s -ss %s --overwrite -o %s/BIDS_output' % ("/tmp", args.subj_id, args.ses_id, args.output_dir)
            
    else:
        raise Exception("Cannot find a directory within dicom directory: " + args.dicom_dir + " with a combination of subject id: " + args.subj_id + ", or session id: " + args.ses_id + ". Must exit.")

# neither subject id or session id
else:
    raise Exception("Neither subject id nor session id arguments were entered. Must exit.")

os.system(convert_format + convert_type)

# once conversion is finished delete data from tmp
if args.subj_id:
    if os.path.isdir("/tmp/" + args.subj_id):
        shutil.rmtree("/tmp/" + args.subj_id)
elif args.ses_id:
    if os.path.isdir("/tmp/" + args.ses_id):
        shutil.rmtree("/tmp/" + args.ses_id)


# Now change IntendedFor field within fmaps
if not args.dry_run:
    # Remove alphanumerics within subj_id
    subj_id = re.sub(r'[^a-zA-Z0-9]', "", args.subj_id)
    setup(os.path.join(args.output_dir, "BIDS_output", "sub-"+subj_id))
