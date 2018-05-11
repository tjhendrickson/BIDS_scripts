## BIDS Conversion Scripts

### Description
These scripts will convert raw DICOM data sets to nipype BIDS format. The run.py script is designed to run the conversion of a data set in a parallelizable way.
Within the heuristics directory are various heuristics scripts that have been used to convert data from dicom to NIFTI. This may be helpful to build your own heuristics script.

Use "run_single.py" when you are testing whether the BIDS conversion work on your data set, but use "run_batch.py" when you get to the point of batching it. "run_batch.py" will automatically delete data within the temporary directory once conversion for that data set has completed.

### Usage

# This script has the following command line arguments

usage: run_single.py [-h] [--top_level_dir TOP_LEVEL_DIR]
                     [--temp_dir TEMP_DIR] [--study_name STUDY_NAME]
                     [--proc_id PROC_ID] [--subj_id SUBJ_ID]
                     [--container CONTAINER]
 Script that controls BIDS conversion for individual studies

optional arguments:
  -h, --help            show this help message and exit
  
  --top_level_dir TOP_LEVEL_DIR
                        The directory this script is being called from, it
                        should also have the heuristics script within.
			
  --temp_dir TEMP_DIR   The directory that will temporarily house dicom
                        directories.
			
  --study_name STUDY_NAME
                        What is the shorthand name for this study?
			
  --proc_id PROC_ID     proc number (AKA session number)
  
  --subj_id SUBJ_ID     subject number 
  
  --container CONTAINER
                        location of docker or udocker install

#					       
If running via udocker, the first time the script runs it will automatically generate container based on the nipy/heudiconv docker image. In order to avoid this create the container ahead of time by typing: 

path/to/udocker create --name=run_heudiconv nipy/heudiconv



