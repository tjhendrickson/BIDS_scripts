## BIDS Conversion Scripts

### Description
These scripts will convert raw DICOM data set to BIDS format. The run.py script is designed to run the
 conversion of a data set in a parallelizable way.Within the heuristics directory are various heuristics scripts that
  have been used to convert data from DICOM to NIFTI. This may be helpful to build your own heuristics script.
  

### Container Hosting
While this app is maintained on both dockerhub and singularityhub the primary hosting is through singularity hub [![https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/1306). To build singularity container on your local system type:
```
sudo singularity build bids_scripts.simg shub://tjhendrickson/bids_scripts:latest
```

### Docker Usage
This script has the following command line arguments:
```
sudo docker run -it --rm tjhendrickson/bids_scripts:v0.3 -h
usage: run.py [-h] [--output_dir OUTPUT_DIR] [--temp_dir TEMP_DIR]
              [--study_name STUDY_NAME] [--proc_id PROC_ID]
              [--subj_id SUBJ_ID] [--heuristic HEURISTIC]

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
  --heuristic HEURISTIC
                        Path to heuristic file, if the file is already within
                        the container you do not have to specify a path.
```

To run a single participant without heuristic script argument:
```
docker run -it --rm -v /home/timothy/sandbox_DO_NOT_DELETE/BIDS/142_CIFASD_4:/output_dir \
-v /path/to/temp/data/dir:/tmp_dir tjhendrickson/bidshcppipeline_status:v0.3 \
--output_dir /output_dir --temp_dir /tmp_dir --study_name 142_CIFASD_4 --proc_id 10000 --subj_id 1000
```

To run a single participant with heuristic script argument:
```
docker run -it --rm -v /home/timothy/sandbox_DO_NOT_DELETE/BIDS/142_CIFASD_4:/output_dir \
-v /path/to/temp/data/dir:/tmp_dir -v /path/to/heuristics/script:/heuristic.py \
tjhendrickson/bidshcppipeline_status:v0.3 \
--output_dir /output_dir --temp_dir /tmp_dir --study_name 142_CIFASD_4 \
--proc_id 10000 --subj_id 1000 --heuristic /heuristic.py
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
              [--subj_id SUBJ_ID] [--heuristic HEURISTIC]

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
  --heuristic HEURISTIC
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



