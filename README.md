## BIDS Conversion Scripts

### Description
These scripts will convert raw DICOM data sets to nipype BIDS format. The run.py script is designed to run the conversion of a data set in a parallelizable way.
Within the heuristics directory are various heuristics scripts that have been used to convert data from dicom to NIFTI. This may be helpful to build your own heuristics script.

Use "run_single.py" when you are testing whether the BIDS conversion work on your data set, but use "run_batch.py" when you get to the point of batching it. "run_batch.py" will automatically delete data within the temporary directory once conversion for that data set has completed.

### Usage

The primary script to be run are either run_single.py / run_batch.py, which has the following command line arguments: 

[run_single.py / run_batch.py] [-h / --help ]
					       [ --top_level_dir ]
					       [ --temp_dir ]
					       [ --study_name ]
					       [ --proc_id ]
					       [ --subj_id ]
					       [ --container ]
					       
If running via udocker, the first time the script runs it will automatically generate container based on the nipy/heudiconv docker image. In order to avoid this create the container ahead of time by typing: 

path/to/udocker create --name=run_heudiconv nipy/heudiconv



