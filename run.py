from glob import glob
import os
from pydicom import read_file
import shutil
from joblib import Parallel, delayed


#book keeping and global variables

# does udocker exist within path?
if os.system('which udocker') != 0:
	raise EnvironmentError('udocker does not exist in path, either download udocker or place within PATH environment variable')

subjdir = raw_input("What is the subject directory o")"/home/lnpi15-raid2/timothy-data-lnpi15/266_FCON/"
subj_glob = "[4-5]????"
raw_datadir = "/home/range2-raid1/timothy/TEMP"
bidsdir = "/home/lnpi15-raid2/timothy-data-lnpi15/266_FCON/BIDS"
thisScript = "266_heuristics.py"
dockerLocation = "/usr/bin/docker"
# if longitudinal what would you like the timepoints to be called?
#scanNames=["timepoint1", "timepoint2", "timepoint3"]


os.chdir(bidsdir)

"""
		To parallelize this processing
		Parallel(n_jobs=6)(delayed(batch)(accession_number) \
				 for accession_number in sorted(glob("%s/%s" % (raw_datadir, subj_glob))))

	"""  # for accession_number in ("50069", "50070"))
accession_numbers = ["48298"]
for accession_number in sorted(accession_numbers):
	if not glob(bidsdir + '/output/sub-*/ses-' + accession_number):
		if not glob("%s/PN-%s*" % (raw_datadir, accession_number)):
			os.system("%s/gunzip_proc.sh %s" % (raw_datadir, accession_number))
		raw_file = read_file(glob("%s/PN-%s*/*SE001*/*0001.dcm" % (raw_datadir, accession_number))[0])
		subj = str(raw_file.PatientName).split("^")[0][-4:]
		os.makedirs(os.path.join(raw_datadir, subj))
		os.rename(glob("%s/PN-%s*" % (raw_datadir, accession_number))[0], "%s/%s" % (raw_datadir, accession_number))
		shutil.move(os.path.join(raw_datadir, accession_number), (os.path.join(raw_datadir, subj)))
		os.system("%s run --rm -v $PWD:/home/tim -v %s/:/home/tim/data \
				-v %s/%s:/home/tim/%s -e LOCAL_USER_ID=`id -u $USER` nipy/heudiconv -d /home/tim/data/{subject}/{session}/*/*.dcm -s %s \
				-ss %s --overwrite -o /home/tim/local -c dcm2niix -f /home/tim/%s -b --minmeta"
		          % (dockerLocation, raw_datadir, bidsdir, thisScript, thisScript, subj, accession_number, thisScript))
		shutil.rmtree("%s/%s" % (raw_datadir, subj))
	else:
		print 'this participant already exists, no read to convert'