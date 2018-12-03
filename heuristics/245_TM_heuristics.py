def create_key(template, outtype=('nii.gz','dicom'), annotation_classes=None): #), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return (template, outtype, annotation_classes)


def infotodict(seqinfo):
	import pdb
	"""Heuristic evaluator for determining which runs belong where allowed template fields - follow python string module:

	item: index within category
	subject: participant id
	seqitem: run number during scanning
	subindex: sub index within group
	"""
	t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_T1w')
	t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_T2w')
	
	task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-{acq}_run-{item:02d}_bold')
        rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-{acq}_run-{item:02d}_bold')
	dwi = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_run-{item:02d}_dwi')

	phase = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_phasediff')
	mag = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_magnitude1')

	info = {t1: [], t2: [], rest: [], dwi: [], task: [], phase: [], mag: []}

	for idx, s in enumerate(seqinfo):
		if s.dim3 == 224:
                    if 'T1_MPRAGE_GR2' in s.protocol_name:
			if 'ND' in s.image_type:
				acq = 'mprND'
				info[t1].append({'item': s.series_id, 'acq': acq})
			elif 'DIS2D' in s.image_type:
				acq = 'mprDIS2D'
				info[t1].append({'item': s.series_id, 'acq': acq})
		elif s.dim3 == 12:
                    if 't2scout' in s.protocol_name:
			acq = 't2scout'
			info[t2].append({'item': s.series_id, 'acq': acq})
		elif s.dim4 == 10:
                    if 'cmrr_mbep2d_bold_REST_AP' in s.protocol_name:
                        acq = 'shortAP'
                        info[rest].append({'item': s.series_id, 'acq': acq})
                elif s.dim4 == 260:
                    if 'cmrr_mbep2d_bold_REST_PA' in s.protocol_name:
                        acq = 'longPA'
                        info[rest].append({'item': s.series_id, 'acq': acq})
                elif s.dim4 == 233:
                    if 'cmrr_mbep2d_bold_FACES1_PA' in s.protocol_name:
                        acq = 'FACES1PA'
                        info[task].append({'item': s.series_id, 'acq': acq})
                    elif 'cmrr_mbep2d_bold_FACES2_PA' in s.protocol_name:
                        acq = 'FACES2PA'
                        info[task].append({'item': s.series_id, 'acq': acq})
                        
		elif s.dim4 == 145:
                    if 'cmrr_mbep2d_diff_1500_PA' in s.series_description:
                        info[dwi].append({'item': s.series_id})
		elif s.dim4 == 1:
                    if s.dim3 == 132:
                        acq = 'fMRI'
                        info[mag].append({'item': s.series_id,  'acq': acq})
                    elif s.dim3 == 66:
                        acq = 'fMRI'
                        info[phase].append({'item': s.series_id,  'acq': acq})
        return info
