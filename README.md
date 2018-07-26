## BIDS Conversion Scripts

### Description
These scripts will convert raw DICOM data set to [BIDS](http://bids.neuroimaging.io/format). Within the heuristics directory are various heuristics scripts that have been used to convert data from DICOM to BIDS. This may be helpful to build your own heuristics script.
  

### Container Hosting
This app is maintained on singularityhub [![https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/1306). To get the most recent singularity container on your local system type:
```
singularity pull --name=name/of/singularity/image.img shub://tjhendrickson/bids_scripts:latest
```

### Singularity Usage
```
singularity run /path/to/singularity/images/directory/imagename.img --help
usage: [-h] [--output_dir OUTPUT_DIR] [--temp_dir TEMP_DIR]
              [--study_name STUDY_NAME] [--proc_id PROC_ID]
              [--subj_id SUBJ_ID] [--heuristic HEURISTIC]

Script that controls BIDS conversion for individual studies

arguments, command separated by "[ ]" are optional:
  [-h, --help]            show this help message and exit
  --output_dir OUTPUT_DIR
                        The directory that the BIDS data will be outputted to
  --temp_dir TEMP_DIR   The directory that will temporarily house dicom
                        directories.
  --study_name STUDY_NAME
                        What is the shorthand name for this study?
  --proc_id PROC_ID     scanning session id
  --subj_id SUBJ_ID     subject id
  [--heuristic HEURISTIC]
                        Path to heuristic file, if the file is already within
                        the container you do not have to specify a path.
```

To run a single participant without heuristic argument:
```
singularity run -B /home/timothy/sandbox_DO_NOT_DELETE/BIDS/142_CIFASD_4:/output_dir \
-B /path/to/temp/data/dir:/tmp_dir /path/to/singularity/images/directory/imagename.img \
--output_dir /output_dir --temp_dir /tmp_dir --study_name 142_CIFASD_4 
--proc_id 10000 --subj_id 1000 
```

To run a single participant with heuristic argument:
```
singularity run -B /home/timothy/sandbox_DO_NOT_DELETE/BIDS/142_CIFASD_4:/output_dir \
-B /path/to/temp/data/dir:/tmp_dir -B /path/to/heuristics/script:/heuristic.py \
/path/to/singularity/images/directory/imagename.img \
--output_dir /output_dir --temp_dir /tmp_dir --study_name 142_CIFASD_4 
--proc_id 10000 --subj_id 1000 --heuristic /heuristic.py
```

## Import Gotchas

**1) Bind Mounting**

In order to run this container you will have to use "bind mounting", meaning you will have to link local folders/files to existing folders/files within the container with the -B flag. In the example above the folder "/home/timothy/sandbos_DO_NOT_DELETE/BIDS/142_CIFASD_4" becomes "/output_dir" as they are separated by a colon (:). **Notice that in both cases below the output and temporary folder and heuristic file are bound to /output_dir, /temp_dir and /heuristic.py, this is very important.**

**2) Folder Deletion within Temporary Folder**

This container **does not** handle folder deletion of the temporary dicom data, this will have to be handled separately

**3) DICOM Data Format within Temporary Folder**

The DICOM data should be formatted in the following format:
```
	temp_dir:
		subj_id:
			proc_id:
				DICOM data
```
Where temp_dir refers to argument of --temp_dir (/tmp_dir), subj_id to --subj_id, and proc_id to --proc_id.

