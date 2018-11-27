## BIDS Conversion Scripts

### Description
These scripts will convert raw DICOM data set to [BIDS](http://bids.neuroimaging.io/format). Within the heuristics directory are various heuristics scripts that have been used to convert data from DICOM to BIDS. This may be helpful to build your own heuristics script. For additional information on how to create a heuristic script see the [heudiconv](https://github.com/nipy/heudiconv) github page.


### Container Hosting
This app is maintained on singularityhub [![https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/1332).You can get the most recent container several different ways below:
```
singularity pull shub://tjhendrickson/BIDS_scripts
singularity pull --name customname.img shub://tjhendrickson/BIDS_scripts
```

### Singularity Usage
```
singularity run /path/to/singularity/images/directory/imagename.img --help
usage: [-h] [--output_dir OUTPUT_DIR] [--dicom_dir DICOM_DIR]
       [--study_name STUDY_NAME] [--ses_id SES_ID] [--subj_id SUBJ_ID]
       [--heuristic HEURISTIC] [--dry_run]

Script that controls BIDS conversion for individual studies

optional arguments:
  -h, --help            show this help message and exit
  --output_dir OUTPUT_DIR
                        The directory that the BIDS data will be outputted to
  --dicom_dir DICOM_DIR
                        The directory that houses unzipped dicom
                        directories/files.
  --study_name STUDY_NAME
                        What is the shorthand name for this study?
  --ses_id SES_ID       scanning session id
  --subj_id SUBJ_ID     subject id
  --heuristic HEURISTIC
                        Path to heuristic file, if the file is already within
                        the container (i.e. within heuristics folder) you do
                        not have to specify a path.
  --dry_run             Dry run. A dicominfo_*.tsv file will generate within
                        .heudiconv/'subj_id'/info directory which can be used
                        to create heuristic script

This application must be run with either the "--heuristic" or "--dry_run" argument, it will fail otherwise.

Use the "--dry_run" argument to take a close look and acquistion parameters for a scanning session.

To run a single participant with dry_run argument:
```
singularity run -B /home/timothy/sandbox_DO_NOT_DELETE/BIDS/142_CIFASD_4:/output_dir \
-B /path/to/dicom/data/dir:/dicom_dir /path/to/singularity/images/directory/imagename.img \
--output_dir /output_dir --dicom_dir /dicom_dir --ses_id 10000 --subj_id 1000 --dry_run
```
This will output a hidden folder (named .heudiconv) along with sub-folders based on arguments provided to "--subj_id" and "--ses_id" respectively.
Within the sub-folders will be a tsv file that begins with "dicominfo". Based on the example above the path to the file will be ".heudiconv/1000/ses-10000/info/dicominfo_ses-10000.tsv"

Use this tsv file to design the script, heuristics script, used to organize your eventual nifti data. Use a script within the "heuristics" folder of this repository and the heuristics script tutorial ([heuristics tutorial](http://reproducibility.stanford.edu/bids-tutorial-series-part-2a/#heuman3))


To run a single participant with heuristic argument:
```
singularity run -B /home/timothy/sandbox_DO_NOT_DELETE/BIDS/142_CIFASD_4:/output_dir \
-B /path/to/dicom/data/dir:/dicom_dir -B /path/to/heuristics/script:/heuristic.py \
 /path/to/singularity/images/directory/imagename.img \
--output_dir /output_dir --dicom_dir /dicom_dir --ses_id 10000 --subj_id 1000 --heuristic /heuristic.py

```

## Important Notes

### Gotchas

**1) Bind Mounting**

In order to run this container you will have to use "bind mounting", meaning you will have to link local folders/files to existing folders/files within the container with the -B flag. In the example above the local folder "/home/timothy/sandbos_DO_NOT_DELETE/BIDS/142_CIFASD_4" becomes "/output_dir" within the container as they are separated by a colon (:). **Notice that in both cases above the output and dicom folder and heuristic file are bound to /output_dir, /dicom_dir and /heuristic.py respectively, this is very important.**

**2) DICOM Data Formatting**

Due to the restrictive nature of BIDS the dicom data must be in a particular format in order for the conversion to work properly. This application will copy dicom data directories by searching for either the --subj_id or --ses_id argument present within a dicom directory name, place them in a separate directory, and rearrange them. So for example if the dicom directory is named "XYXY4776XYXY" --subj_id 4776 the application will find the "4776" pattern.

**3) Subject ID and Session ID names**

You must use alphanumerics (i.e. letters or numbers) only (**no special characters**) with your subject IDs (subj_id) and session IDs (ses_id). **Note the "--ses_id" argument is optional**!

### Best Practices

**1) Initial Conversion**

While testing the initial BIDS conversion it is best to start with one or two datasets and specify the '--dry_run' argument (see above for an example of usage). 
This will create a dicom_info tsv file which can be used for heuristic script creation. 
See Step 3 of 'Run HeuDiConv on ses-001 scans to get the dicominfo file' within [Stanford BIDS Tutorial](http://reproducibility.stanford.edu/bids-tutorial-series-part-2a/#heuman2).

**2) BIDS Validator**

Once satisfied with an initial BIDS conversion, prior to running the conversion on an entire study first ensure that the BIDS converted dataset meets the BIDS specification by using the [BIDS validator web version](http://incf.github.io/bids-validator/)

**3) Longitudinal Format**

When converting data to BIDS you can certainly have a cross sectonal directory format such as below:
BIDS_output
  sub-01
  sub-02
  sub-03
  sub-04
  etc
However, I suggest placing data within a longitudinal directory format even if you have cross-sectional data:
BIDS_output
  sub-01
    ses-01
    ses-02
  sub-02
    ses-01
  etc

You can control the BIDS directory format by providing both the arguments --subj_id --ses_id for a conversion, if you only specify one of the two arguments the data will be outputted in a cross-sectional format.
