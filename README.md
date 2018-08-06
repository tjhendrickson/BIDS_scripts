## BIDS Conversion Scripts

### Description
These scripts will convert raw DICOM data set to [BIDS](http://bids.neuroimaging.io/format). Within the heuristics directory are various heuristics scripts that have been used to convert data from DICOM to BIDS. This may be helpful to build your own heuristics script. For additional information on how to create a heuristic script see the [heudiconv](https://github.com/nipy/heudiconv) github page.


### Container Hosting
This app is maintained on singularityhub [![https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/1306).You can get the most recent container several different ways below:
```
singularity pull shub://tjhendrickson/BIDS_scripts
singularity pull --name customname.img shub://tjhendrickson/BIDS_scripts
```

### Singularity Usage
```
singularity run /path/to/singularity/images/directory/imagename.img --help
usage: [-h] [--output_dir OUTPUT_DIR] [--temp_dir TEMP_DIR]
              [--study_name STUDY_NAME] [--proc_id PROC_ID]
              [--subj_id SUBJ_ID] [--heuristic HEURISTIC] [--dry_run]

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
                        the container (i.e. within heuristics folder) you do
                        not have to specify a path.
  [--dry_run]             Dry run. A dicominfo_*.tsv file will generate within
                        .heudiconv/'subj_id'/info directory which can be used
                        to create heuristic script

```

To run a single participant without heuristic argument:
```
singularity run -B /home/timothy/sandbox_DO_NOT_DELETE/BIDS/142_CIFASD_4:/output_dir \
-B /path/to/temp/data/dir:/temp_dir /path/to/singularity/images/directory/imagename.img \
--output_dir /output_dir --temp_dir /temp_dir --study_name 142_CIFASD_4
--proc_id 10000 --subj_id 1000
```

To run a single participant with heuristic argument:
```
singularity run -B /home/timothy/sandbox_DO_NOT_DELETE/BIDS/142_CIFASD_4:/output_dir \
-B /path/to/temp/data/dir:/temp_dir -B /path/to/heuristics/script:/heuristic.py \
/path/to/singularity/images/directory/imagename.img \
--output_dir /output_dir --temp_dir /temp_dir --study_name 142_CIFASD_4
--proc_id 10000 --subj_id 1000 --heuristic /heuristic.py
```

To run a single participant with dry_run argument:
```
singularity run -B /home/timothy/sandbox_DO_NOT_DELETE/BIDS/142_CIFASD_4:/output_dir \
-B /path/to/temp/data/dir:/temp_dir /path/to/singularity/images/directory/imagename.img \
--output_dir /output_dir --temp_dir /tmp_dir --study_name 142_CIFASD_4
--proc_id 10000 --subj_id 1000 --dry_run
```

## Important Notes

### Gotchas

**1) Bind Mounting**

In order to run this container you will have to use "bind mounting", meaning you will have to link local folders/files to existing folders/files within the container with the -B flag. In the example above the local folder "/home/timothy/sandbos_DO_NOT_DELETE/BIDS/142_CIFASD_4" becomes "/output_dir" within the container as they are separated by a colon (:). **Notice that in both cases above the output and temporary folder and heuristic file are bound to /output_dir, /temp_dir and /heuristic.py respectively, this is very important.**

**2) Folder Deletion within Temporary Folder**

This container **does not** handle folder deletion of the temporary dicom data, this will have to be handled separately

**3) DICOM Data Format within Temporary Folder**

The DICOM data should be formatted in the following format:
```
	temp_dir:
		proc_id:
				DICOM data
```
Where temp_dir refers to argument of --temp_dir (/tmp_dir), and proc_id to --proc_id.

**4) Subject ID and Session ID names**

You must use alphanumerics (i.e. letters or numbers) only (**no special characters**) with your subject IDs (subj_id) and session IDs (proc_id).

### Best Practices

**1) Initial Conversion**

While testing the initial BIDS conversion it is best to start with one or two datasets and specify the '--dry_run' argument (see above for an example of usage). 
This will create a dicom_info tsv file which can be used for heuristic script creation. 
See Step 3 of 'Run HeuDiConv on ses-001 scans to get the dicominfo file' within [Stanford BIDS Tutorial](http://reproducibility.stanford.edu/bids-tutorial-series-part-2a/#heuman2).

**2) BIDS Validator**

Once satisfied with an initial BIDS conversion, prior to running the conversion on an entire study first ensure that the BIDS converted dataset meets the BIDS specification by using the [BIDS validator web version](http://incf.github.io/bids-validator/)

