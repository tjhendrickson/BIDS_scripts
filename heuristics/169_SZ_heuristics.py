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
    pd = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_PD')
    rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-{item:02d}_bold')
    dwi = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_run-{item:02d}_dwi')
    phase = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_phasediff')
    mag = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_magnitude1')
    info = {t1: [], t2: [], pd: [], rest: [], dwi: [], phase: [], mag: []}
    for idx, s in enumerate(seqinfo):
        if 'T1_MPRAGE' in s.series_description:
            if 'ND' in s.image_type:
                acq = 'mprND'
                info[t1].append({'item': s.series_id, 'acq': acq})
            elif 'DIS2D' in s.image_type:
                acq = 'mprDIS2D'
                info[t1].append({'item': s.series_id, 'acq': acq})
        elif 'NOMT_grappa_2' in s.series_description:
            acq = 'NOMT'
            info[t1].append({'item': s.series_id, 'acq': acq})
        elif 'MT_grappa_2' in s.series_description:
            acq = 'MT'
            info[t1].append({'item': s.series_id, 'acq': acq})
        elif 't2scout' in s.series_description:
            acq = 't2scout'
            info[t2].append({'item': s.series_id, 'acq': acq})
        elif 't2r_8_H2O' in s.series_description:
            acq = 't2r8'
            info[t2].append({'item': s.series_id, 'acq': acq})
        elif 't2r_33_H2O' in s.series_description:
            acq = 't2r33'
            info[t2].append({'item': s.series_id, 'acq': acq})
        elif 't2r_110_H2O' in s.series_description:
            acq = 't2r110'
            info[t2].append({'item': s.series_id, 'acq': acq})
        elif 't2r_75_H2O' in s.series_description:
            acq = 't2r75'
            info[t2].append({'item': s.series_id, 'acq': acq})
            if 'pd_axial_80_sl_hyperecho' in s.series_description:
                if 'ND' in s.image_type:
                    acq = 'tseND'
                    info[pd].append({'item': s.series_id, 'acq': acq})
                elif 'DIS2D' in s.image_type:
                    acq = 'tseDIS2D'
                    info[pd].append({'item': s.series_id, 'acq': acq})
        elif 'ep2d_diff_jones_35_VB15_PA' in s.series_description:
            info[dwi].append({'item': s.series_id})
        elif 'FMRI_REST' in s.series_description:
            info[rest].append({'item': s.series_id})
        elif 'gre_FMRI_fieldmap' in s.series_description:
            if 'M' in s.image_type[2]:
                acq = 'fMRI'
                info[mag].append({'item': s.series_id,  'acq': acq})
            elif 'P' in s.image_type[2]:
                acq = 'fMRI'
                info[phase].append({'item': s.series_id,  'acq': acq})
        elif 'gre_DTI_fieldmap' in s.series_description:
            if 'M' in s.image_type[2]:
                acq = 'dMRI'
                info[mag].append({'item': s.series_id,  'acq': acq})
            elif 'P' in s.image_type[2]:
                acq = 'dMRI'
                info[phase].append({'item': s.series_id,  'acq': acq})
    return info
