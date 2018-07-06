## BIDS Conversion Scripts

### Description
These scripts will convert raw DICOM data sets to nipype BIDS format. The run.py script is designed to run the conversion of a data set in a parallelizable way.
Within the heuristics directory are various heuristics scripts that have been used to convert data from dicom to NIFTI. This may be helpful to build your own heuristics script.

Use "run_single.py" when you are testing whether the BIDS conversion work on your data set, but use "run_batch.py" when you get to the point of batching it. "run_batch.py" will automatically delete data within the temporary directory once conversion for that data set has completed.

### Docker Usage
This script has the following command line arguments:
```
docker run -it --rm tjhendrickson/bidshcppipeline_status:v0.2 --help
usage: run.py [-h] [--output_dir OUTPUT_DIR] [--temp_dir TEMP_DIR]
              [--study_name STUDY_NAME] [--proc_id PROC_ID]
              [--subj_id SUBJ_ID]

Script that controls BIDS conversion for individual studies

optional arguments:
  -h, --help            show this help message and exit
  --output_dir OUTPUT_DIR
                        The directory that the BIDS data will be outputted to
  --temp_dir TEMP_DIR   The directory that will temporarily house dicom
                        directories.
  --study_name STUDY_NAME
                        What is the shorthand name for this study?
  --proc_id PROC_ID     scanning session id
  --subj_id SUBJ_ID     subject id
```

To run a single participant:

```
docker run -it --rm -v /home/timothy/sandbox_DO_NOT_DELETE/BIDS/142_CIFASD_4:/output_dir \
-v /path/to/temp/data/dir:/tmp_dir \
tjhendrickson/bidshcppipeline_status:v0.2 \
--output_dir /output_dir --temp_dir /tmp_dir --study_name 142_CIFASD_4 --proc_id 10000 --subj_id 1000
```

### Docker to Singularity Image Conversion

To convert docker image to singularity you will need:
1) A system with docker 
2) The docker image on that system (i.e. 'docker pull name/of/docker/image')
3) The docker image docker2singularity on that system ('docker pull docker2singularity')

And the command: 
```
  docker run --privileged -ti --rm  \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -v /path/to/singularity/images/directory:/output \
      singularityware/docker2singularity \
      name/of/docker/image
```

### Singularity Usage
```
singularity run /path/to/singularity/images/directory/imagename.img --help
usage: run.py [-h] [--output_dir OUTPUT_DIR] [--temp_dir TEMP_DIR]
              [--study_name STUDY_NAME] [--proc_id PROC_ID]
              [--subj_id SUBJ_ID]

Script that controls BIDS conversion for individual studies

optional arguments:
  -h, --help            show this help message and exit
  --output_dir OUTPUT_DIR
                        The directory that the BIDS data will be outputted to
  --temp_dir TEMP_DIR   The directory that will temporarily house dicom
                        directories.
  --study_name STUDY_NAME
                        What is the shorthand name for this study?
  --proc_id PROC_ID     scanning session id
  --subj_id SUBJ_ID     subject id
```

To run a single participant:

```
singularity run -B /home/timothy/sandbox_DO_NOT_DELETE/BIDS/142_CIFASD_4:/output_dir \
-B /path/to/temp/data/dir:/tmp_dir \
/path/to/singularity/images/directory/imagename.img \
--output_dir /output_dir --temp_dir /tmp_dir --study_name 142_CIFASD_4 --proc_id 10000 --subj_id 1000
```



