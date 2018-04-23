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
    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_run-{item:02d}_T1w')
    t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_run-{item:02d}_T2w')

    rest = create_key('sub-{subject}/{session}/func/sub-{subject}_task-rest_acq-{acq}_run-{item:02d}_bold')
    sbref_rest = create_key('sub-{subject}/{session}/func/sub-{subject}_task-rest_acq-{acq}_run-{item:02d}_sbref')

    dwi = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_dwi')
    sbref_dwi = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_sbref')


    spinecho_map_bold = create_key('sub-{subject}/{session}/fmap/sub-{subject}_dir-{dir}_run-{item:02d}_epi')

    info = {t1: [], t2: [], rest: [], spinecho_map_bold: [], sbref_rest: [], dwi: [], sbref_dwi: []}

    for idx, s in enumerate(seqinfo):
        if (s.dim3 == 208):
            if 'NORM' in s.image_type:
                if 'T1w_MPR' in s.protocol_name:
                    info[t1].append({'item': s.series_id})
                else:
                    info[t2].append({'item': s.series_id})
        if (s.dim4 == 90) and ('mbPCASLhr_PA_single_delay' in s.protocol_name):
            info[rest].append({'item': s.series_id, 'acq': 'mbPCASLhr'})
        if (s.dim4 >= 99) and ('dMRI' in s.protocol_name):
            if 'dir98_AP' in s.protocol_name:
                info[dwi].append({'item': s.series_id, 'acq': 'dir98AP'})
            elif 'dir98_PA' in s.protocol_name:
                info[dwi].append({'item': s.series_id, 'acq': 'dir98PA'})
            elif 'dir99_AP' in s.protocol_name:
                info[dwi].append({'item': s.series_id, 'acq': 'dir99AP'})
            elif 'dir99_PA' in s.protocol_name:
                info[dwi].append({'item': s.series_id, 'acq': 'dir99PA'})

        if (s.dim4 == 1):
            if 'SpinEchoFieldMap' in s.protocol_name:
                if 'PA' in s.protocol_name:
                    info[spinecho_map_bold].append({'item': s.series_id, 'acq': 'SE', 'dir': 'PA'})
                else:
                    info[spinecho_map_bold].append({'item': s.series_id, 'acq': 'SE', 'dir': 'AP'})
            if 'REST' in s.protocol_name:
                if 'AP' in s.protocol_name:
                    info[sbref_rest].append({'item': s.series_id, 'acq': 'eyesopenAP'})
                else:
                    info[sbref_rest].append({'item': s.series_id, 'acq': 'eyesopenPA'})

            if 'dMRI' in s.protocol_name:
                if 'dir98_AP' in s.protocol_name:
                    info[sbref_dwi].append({'item': s.series_id, 'acq': 'dir98AP'})
                elif 'dir98_PA' in s.protocol_name:
                    info[sbref_dwi].append({'item': s.series_id, 'acq': 'dir98PA'})
                elif 'dir99_AP' in s.protocol_name:
                    info[sbref_dwi].append({'item': s.series_id, 'acq': 'dir99AP'})
                elif 'dir99_PA' in s.protocol_name:
                    info[sbref_dwi].append({'item': s.series_id, 'acq': 'dir99AP'})
    return info