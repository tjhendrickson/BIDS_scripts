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
    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-{acq}_T1w')
    t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T2w')
    dwi = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_dwi')

    info = {t1: [], t2: [], dwi: []}

    for idx, s in enumerate(seqinfo):
        if (s.dim3 == 192) and ('MPRAGE' in s.dcm_dir_name):
            acq = 'MPRAGE'
            info[t1].append({'item': s.series_id, 'acq': acq})
        if (s.dim3 == 176) and ('T2W' in s.dcm_dir_name):
            info[t2].append({'item': s.series_id})
        if (s.dim4 == 31) and ('DTI' in s.dcm_dir_name):
                acq = 'DTI'
                info[dwi].append({'item': s.series_id, 'acq': acq})
        if (s.dim3 == 340) and ('DTI_AP' in s.dcm_dir_name):
                acq = 'DTIap'
                info[dwi].append({'item': s.series_id, 'acq': acq})
        if (s.dim3 == 68) and ('DTI_PA' in s.dcm_dir_name):
                acq = 'DTIpa'
                info[dwi].append({'item': s.series_id, 'acq': acq})
    return info
