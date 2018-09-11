import pdb

def create_key(template, outtype=('nii.gz','dicom'), annotation_classes=None): #), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return (template, outtype, annotation_classes)


def infotodict(seqinfo):
	"""Heuristic evaluator for determining which runs belong where

	allowed template fields - follow python string module:

	item: index within category
	subject: participant id
	seqitem: run number during scanning
	subindex: sub index within group
	"""
	pdb.set_trace()
	t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_T1w')
	rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-{item:02d}_bold')
	#dwi = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_dwi')
	task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-{acq}_run-{item:02d}_bold')
	info = {t1: [], rest: [], task: []}

	for idx, s in enumerate(seqinfo):
		#pdb.set_trace()
		if ('MPRAGE' in s.protocol_name) and (s.dim3 == 161):
			info[t1].append({'item': s.series_id})
		elif (s.dim3 == 9501) and (s.example_dcm_file == 'IM_1148'):
			info[rest].append({'item': s.series_id})
		elif 'EYE' in s.protocol_name:
			info[task].append({'item': s.series_id, 'acq': "eyegaze"})

	return info
