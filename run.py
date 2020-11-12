#!/usr/bin/python

from glob import glob
import os
import shutil
import argparse
from IntendedFor import setup
import sys
import re
import fnmatch
import pdb

#book keeping and global variables
parser = argparse.ArgumentParser(description='Script that controls BIDS conversion for individual studies')
parser.add_argument('--output_dir', help="The directory that the BIDS data will be outputted to",required=True)
parser.add_argument('--tmp_dir', help="The directory that DICOM data will  be temporarily stored in.", required=True)
parser.add_argument('--dicom_dir', help='The directory that houses dicom directories/files.',required=True)
parser.add_argument('--ses_id', help="scanning session id")
parser.add_argument('--subj_id', help="subject id")
parser.add_argument('--heuristic', help="Path to heuristic file, if the file is already within the container (i.e. within heuristics folder)"
										" you do not have to specify a path. ")
parser.add_argument('--dry_run', action='store_true', help="Dry run. A dicominfo_*.tsv file will generate within .heudiconv/'subj_id'/info directory which can be used to create heuristic script")

args = parser.parse_args()
dicom_dir = args.dicom_dir
tmp_dir = args.tmp_dir
ses_id = args.ses_id
subj_id = args.subj_id
heuristic = args.heuristic
dry_run = args.dry_run
output_dir = args.output_dir

# change temporary dir to different location based on --tmp_dir flag
os.system('export TMPDIR='+tmp_dir)

# make bids directory if it does not exist
if not os.path.exists(os.path.join(output_dir, "BIDS_output")):
    os.makedirs(os.path.join(output_dir, "BIDS_output"))
    
if os.path.exists(os.path.join(output_dir,"BIDS_output",".heudiconv",subj_id,'ses-'+ses_id)):
    shutil.rmtree(os.path.join(output_dir,"BIDS_output",".heudiconv",subj_id,'ses-'+ses_id))

# determine conversion type (i.e. dry run or heuristic)
if dry_run:
    convert_type = ' -c none -f convertall'
else:
    if not heuristic:
        raise Exception("If a dry_run is not being a conducted a heuristic script must be used. Re-run and place path within --heuristic argument.")
        sys.exit()
    else:
        heuristics_script = heuristic
        convert_type = ' -c dcm2niix -f %s -b' % heuristics_script

# try to determine how data is organized within dicom directory, place within /tmp directory, and determine what heudiconv format (cross-sectional, longitudinal should look like)
# just subj_id
if subj_id and not ses_id:
    if len(glob(dicom_dir + "/*" + subj_id + "*")) == 1:
        if os.path.isdir(glob(dicom_dir + "/*" + subj_id + "*")[0]):
            dicom_session_folder = glob(dicom_dir + "/*" + subj_id + "*")[0]
            matches = []
            for root, dirnames, filenames in os.walk(dicom_session_folder):
                for filename in fnmatch.filter(filenames, '*.dcm'):
                    matches.append(os.path.join(root, filename))
            if len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 1:
                recursion_pattern = '*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 2:
                recursion_pattern = '*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 3:
                recursion_pattern = '*/*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 4:
                recursion_pattern = '*/*/*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 5:
                recursion_pattern = '*/*/*/*/*'
            convert_format = '/neurodocker/startup.sh heudiconv -d %s/*{subject}*/%s -s %s  --overwrite -o %s/BIDS_output' % (dicom_dir, recursion_pattern,  subj_id, output_dir)
    elif len(glob(dicom_dir + "/*" + subj_id + "*")) > 1:
        raise Exception("There are multiple directories within dicom directory: " + dicom_dir + " with the same subject id: " + subj_id + ". Either change the subject id or enter a session id. Must exit.")
    else:
        raise Exception("Cannot find a directory within dicom directory: " + dicom_dir + " with the subject id: " + subj_id + ". Must exit.")

#just ses id
elif ses_id and not subj_id:
    if len(glob(dicom_dir + "/*" + ses_id + "*")) == 1:
        if os.path.isdir(glob(dicom_dir + "/*" + ses_id + "*")[0]):
            dicom_session_folder = glob(dicom_dir + "/*" + ses_id + "*")[0]
            matches = []
            for root, dirnames, filenames in os.walk(dicom_session_folder):
                for filename in fnmatch.filter(filenames, '*.dcm'):
                    matches.append(os.path.join(root, filename))
            if len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 1:
                recursion_pattern = '*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 2:
                recursion_pattern = '*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 3:
                recursion_pattern = '*/*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 4:
                recursion_pattern = '*/*/*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 5:
                recursion_pattern = '*/*/*/*/*'

            convert_format = '/neurodocker/startup.sh heudiconv -d %s/*{subject}*/%s -s %s --overwrite -o %s/BIDS_output' % (dicom_dir, recursion_pattern, ses_id, output_dir)
    elif len(glob(dicom_dir + "/*" + ses_id + "*")) > 1:
        raise Exception("There are multiple directories within dicom directory: " + dicom_dir + " with the same subject id: " + ses_id + ". Either change the subject id or enter a session id. Must exit.")
    else:
        raise Exception("Cannot find a directory within dicom directory: " + dicom_dir + " with the subject id: " + ses_id + ". Must exit.")

# subject id and session id
elif ses_id and subj_id:
    if len(glob(dicom_dir + "/*" + subj_id + "*/*" + ses_id + "*")) == 1:
        if os.path.isdir(glob(dicom_dir + "/*" + subj_id + "*/*" + ses_id + "*")[0]):
            dicom_session_folder = glob(dicom_dir + "/*" + subj_id + "*/*" + ses_id + "*")[0]       
            matches = []
            for root, dirnames, filenames in os.walk(dicom_session_folder):
                for filename in fnmatch.filter(filenames, '*.dcm'):
                    matches.append(os.path.join(root, filename))
            if len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 1:
                recursion_pattern = '*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 2:
                recursion_pattern = '*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 3:
                recursion_pattern = '*/*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 4:
                recursion_pattern = '*/*/*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 5:
                recursion_pattern = '*/*/*/*/*'
            convert_format = '/neurodocker/startup.sh heudiconv -d %s/*{subject}*/*{session}*/%s -s %s -ss %s --overwrite -o %s/BIDS_output' % (dicom_dir, recursion_pattern, subj_id, ses_id, output_dir)
    
    elif len(glob(dicom_dir + "/*" + ses_id + "*/*" + subj_id + "*")) == 1:
        if os.path.isdir(glob(dicom_dir + "/*" + ses_id + "*/*" + subj_id + "*")[0]):
            dicom_session_folder = glob(dicom_dir + "/*" + ses_id + "*/*" + subj_id + "*")[0]     
            matches = []
            for root, dirnames, filenames in os.walk(dicom_session_folder):
                for filename in fnmatch.filter(filenames, '*.dcm'):
                    matches.append(os.path.join(root, filename))
            if len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 1:
                recursion_pattern = '*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 2:
                recursion_pattern = '*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 3:
                recursion_pattern = '*/*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 4:
                recursion_pattern = '*/*/*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 5:
                recursion_pattern = '*/*/*/*/*'
            convert_format = '/neurodocker/startup.sh heudiconv -d %s/*{session}*/*{subject}*/%s -s %s -ss %s --overwrite -o %s/BIDS_output' % (dicom_dir, recursion_pattern, ses_id, subj_id, output_dir)
    
    elif len(glob(dicom_dir + "/*" + subj_id + "*" + ses_id + "*")) == 1:
        if os.path.isdir(glob(dicom_dir + "/*" + subj_id + "*" + ses_id + "*")[0]):
            dicom_session_folder = glob(dicom_dir + "/*" + subj_id + "*" + ses_id + "*")[0]
            matches = []
            for root, dirnames, filenames in os.walk(dicom_session_folder):
                for filename in fnmatch.filter(filenames, '*.dcm'):
                    matches.append(os.path.join(root, filename))
            if len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 1:
                recursion_pattern = '*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 2:
                recursion_pattern = '*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 3:
                recursion_pattern = '*/*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 4:
                recursion_pattern = '*/*/*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 5:
                recursion_pattern = '*/*/*/*/*'
            convert_format = '/neurodocker/startup.sh heudiconv -d %s/*{subject}*{session}*/%s -s %s -ss %s --overwrite -o %s/BIDS_output' % (dicom_dir, recursion_pattern, subj_id, ses_id, output_dir)

    elif len(glob(dicom_dir + "/*" + ses_id + "*" + subj_id + "*")) == 1:
        if os.path.isdir(glob(dicom_dir + "/*" + ses_id + "*" + subj_id + "*")[0]):
            dicom_session_folder = glob(dicom_dir + "/*" + ses_id + "*" + subj_id + "*")[0]
            matches = []
            for root, dirnames, filenames in os.walk(dicom_session_folder):
                for filename in fnmatch.filter(filenames, '*.dcm'):
                    matches.append(os.path.join(root, filename))
            if len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 1:
                recursion_pattern = '*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 2:
                recursion_pattern = '*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 3:
                recursion_pattern = '*/*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 4:
                recursion_pattern = '*/*/*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 5:
                recursion_pattern = '*/*/*/*/*'
            convert_format = '/neurodocker/startup.sh heudiconv -d %s/*{session}*{subject}*/%s -s %s -ss %s --overwrite -o %s/BIDS_output' % (dicom_dir, recursion_pattern, subj_id, ses_id, output_dir)
    
    elif len(glob(dicom_dir + "/*" + subj_id + "*")) == 1:
        if os.path.isdir(glob(dicom_dir + "/*" + subj_id + "*")[0]):
            dicom_session_folder = glob(dicom_dir + "/*" + subj_id + "*")[0]
            matches = []
            for root, dirnames, filenames in os.walk(dicom_session_folder):
                for filename in fnmatch.filter(filenames, '*.dcm'):
                    matches.append(os.path.join(root, filename))
            if len(matches[0].split(dicom_session_folder  + "/")[1].split('/')) == 1:
                recursion_pattern = '*'
            elif len(matches[0].split(dicom_session_folder  + "/")[1].split('/')) == 2:
                recursion_pattern = '*/*'
            elif len(matches[0].split(dicom_session_folder  + "/")[1].split('/')) == 3:
                recursion_pattern = '*/*/*'
            elif len(matches[0].split(dicom_session_folder  + "/")[1].split('/')) == 4:
                recursion_pattern = '*/*/*/*'
            elif len(matches[0].split(dicom_session_folder  + "/")[1].split('/')) == 5:
                recursion_pattern = '*/*/*/*/*'
            convert_format = '/neurodocker/startup.sh heudiconv -d %s/*{subject}*/%s -s %s -ss %s --overwrite -o %s/BIDS_output' % (dicom_dir, recursion_pattern, subj_id, ses_id, output_dir)

    elif len(glob(dicom_dir + "/*" + ses_id + "*")) == 1:
        if os.path.isdir(glob(dicom_dir + "/*" + ses_id + "*")[0]):
            dicom_session_folder = glob(dicom_dir + "/*" + ses_id + "*")[0]
            if os.path.isdir(os.path.join(tmp_dir,subj_id,ses_id)):
                shutil.rmtree(os.path.join(tmp_dir,subj_id,ses_id))
            shutil.copytree(dicom_session_folder,os.path.join(tmp_dir,subj_id,ses_id))
            dicom_session_folder = os.path.join(tmp_dir,subj_id,ses_id)
            matches = []
            for root, dirnames, filenames in os.walk(dicom_session_folder):
                for filename in fnmatch.filter(filenames, '*.dcm'):
                    matches.append(os.path.join(root, filename))
            if len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 1:
                recursion_pattern = '*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 2:
                recursion_pattern = '*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 3:
                recursion_pattern = '*/*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 4:
                recursion_pattern = '*/*/*/*'
            elif len(matches[0].split(dicom_session_folder + '/')[1].split('/')) == 5:
                recursion_pattern = '*/*/*/*/*'
            convert_format = '/neurodocker/startup.sh heudiconv -d %s/{subject}/{session}/%s -s %s -ss %s --overwrite -o %s/BIDS_output ' % (tmp_dir, recursion_pattern, subj_id, ses_id, output_dir)
    
    else:
        raise Exception("Cannot find a directory within dicom directory: " + dicom_dir + " with a combination of subject id: " + subj_id + ", or session id: " + ses_id + ". Must exit.")

# neither subject id or session id
else:
    raise Exception("Neither subject id nor session id arguments were entered. Must exit.")
os.system(convert_format + convert_type)

# Now change IntendedFor field within fmaps
if not dry_run:
    # Remove alphanumerics within subj_id
    subj_id = re.sub(r'[^a-zA-Z0-9]', "", subj_id)
    setup(os.path.join(output_dir, "BIDS_output", "sub-"+subj_id))
