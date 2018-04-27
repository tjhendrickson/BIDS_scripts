#STILL BEING TESTED, DO NOT USE. 

from glob import glob
import os
import sys
from pydicom import read_file
import shutil
from joblib import Parallel, delayed


#book keeping and global variables

# does udocker exist within path?
if not 'linux' in sys.platform:
	raise EnvironmentError('platform is not linux, must exit.')
if os.system('which udocker') != 0:
	raise EnvironmentError('udocker does not exist in path, either download udocker or place within PATH environment variable.')

subjdir = "/home/lnpi15-raid2/kathryn-data-lnpi15/275_BRIDGES"
subj_glob = "[4-5]????"
raw_datadir = "/home/range2-raid1/timothy/TEMP"
bidsdir = "/home/lnpi15-raid2/kathryn-data-lnpi15/275_BRIDGES/BIDS"
heuristics_script= "275_BRIDGES_heuristics.py"
docker_location = "/home/lnpi14-raid1/timothy-data-lnpi14/nipype_python_2.7.10/bin/udocker"


os.chdir(bidsdir)


def batch(accession_number):
	accession_number = os.path.basename(accession_number)
	if not os.path.isdir(os.path.join(bidsdir, 'BIDS_output', 'sub-'+accession_number)) \
			or glob(bidsdir +'/BIDS_output/'+ '*' + '/ses-'+accession_number) == []:
		if not glob("%s/*%s*" % (raw_datadir, accession_number)) and not glob("%s/*/*%s*" % (raw_datadir, accession_number)):
			os.system("%s/gunzip_proc.sh %s" % (raw_datadir, accession_number))
		raw_file = read_file(glob("%s/PN-%s*/*/*0001.dcm" % (raw_datadir, accession_number))[0])
		subj = str(raw_file.PatientName).split("^")[0][-4:]
		if not os.path.exists(os.path.join(raw_datadir, subj)):
			os.makedirs(os.path.join(raw_datadir, subj))
		os.rename(glob("%s/PN-%s*" % (raw_datadir, accession_number))[0], "%s/%s" % (raw_datadir, accession_number))
		shutil.move(os.path.join(raw_datadir, accession_number), (os.path.join(raw_datadir, subj)))
		os.system('/bin/bash -c "%s run -v $PWD:/home/tim -v %s/:/home/tim/data \
		-v %s/%s:/home/tim/%s run_heudiconv -d /home/tim/data/{subject}/{session}/*/*.dcm -s %s \
		-ss %s --overwrite -o /home/tim/BIDS_output -c dcm2niix -f /home/tim/%s -b"'
		          % (docker_location, raw_datadir, bidsdir, heuristics_script, heuristics_script, subj, accession_number,
		             heuristics_script))
		shutil.rmtree("%s/%s" % (raw_datadir, subj))
	else:
		print 'this participant already exists, no need to convert'

#Parallelize processing
Parallel(n_jobs=6,backend='multiprocessing',verbose=1)(delayed(batch)(accession_number) \
		 for accession_number in sorted(glob("%s/%s" % (subjdir, subj_glob))))
