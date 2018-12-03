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

    #initialize dictionary data types
    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_T1w')
    flair = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_FLAIR')
    t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_run-{item:02d}_T2w')

    task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-{acq}_run-{item:02d}_bold')
    sbref_task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-{acq}_run-{item:02d}_sbref')

    rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-{item:02d}_bold')
    sbref_rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-{item:02d}_sbref')

    dwi = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_dwi')
    sbref_dwi = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_sbref')

    spinecho_map_bold = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-{dir}_run-{item:02d}_epi')

    # initilize dictionary
    info = {t1: [], flair: [], t2: [], task: [], rest: [], dwi: [], sbref_dwi: [], spinecho_map_bold: [], sbref_rest: [], sbref_task: []}

    for idx, s in enumerate(seqinfo):

        #use s_next to ensure that scan following sbref scans match expected acqusition parameters
        if idx + 1 < len(seqinfo) - 1:
            s_next = seqinfo[idx+1]
        
        #dim3 = number of slices, NORM = pre-scan normalize on
        if (s.dim3 == 176) and ('NORM' in s.image_type):
            if 't1_mpr' in s.protocol_name:
                acq = 't1mpr'
                info[t1].append({'item': s.series_id, 'acq': acq})
            elif 'FLAIR' in s.protocol_name:
                info[flair].append({'item': s.series_id})
            elif 'T2' in s.protocol_name:
                info[t2].append({'item': s.series_id})
        if (s.dim4 == 145) and ('DTI_b1200_128_MB3_REV_PA' in s.protocol_name):
            acq = 'b1200MB3AP'
            info[dwi].append({'item': s.series_id, 'acq': acq})
        if (s.dim4 == 145) and ('DTI_b1200_128_MB3_PA' in s.protocol_name):
            acq = 'b1200MB3PA'
            info[dwi].append({'item': s.series_id, 'acq': acq})
        if (s.dim4 == 890) and ('REST' in s.protocol_name):
            info[rest].append({'item': s.series_id})
        if (s.dim4 == 769) and ('TASK' in s.protocol_name):
            if 'TASK1' in s.protocol_name:
                acq = 'TASK1'
                info[task].append({'item': s.series_id, 'acq': acq})
            elif 'TASK2' in s.protocol_name:
                acq = 'TASK2'
                info[task].append({'item': s.series_id, 'acq': acq})
            elif 'TASK3' in s.protocol_name:
                acq = 'TASK3'
                info[task].append({'item': s.series_id, 'acq': acq})
        if (s.dim4 == 1):
            if ('REST' in s.protocol_name):
                if s_next.dim4 == 890:
                    info[sbref_rest].append({'item': s.series_id})
            elif ('TASK' in s.protocol_name):
                if s_next.dim4 == 769:
                    if 'TASK1' in s.protocol_name:
                        acq = 'TASK1'
                        info[sbref_task].append({'item': s.series_id, 'acq': acq})
                    elif 'TASK2' in s.protocol_name:
                        acq = 'TASK2'
                        info[sbref_task].append({'item': s.series_id, 'acq': acq})
                    elif 'TASK3' in s.protocol_name:
                        acq = 'TASK3'
                        info[sbref_task].append({'item': s.series_id, 'acq': acq})
            elif 'DTI_b1200_128_MB3_PA' in s.protocol_name:
                if s_next.dim4 == 145:
                    acq = 'b1200MB3PA'
                    info[sbref_dwi].append({'item': s.series_id, 'acq': acq}) 
            elif 'DTI_b1200_128_MB3_REV_PA' in s.protocol_name:
                if s_next.dim4 == 145:
                    acq = 'b1200MB3AP'
                    info[sbref_dwi].append({'item': s.series_id, 'acq': acq})
        if (s.dim4 == 3) and ('SpinEchoFieldMap_REV_AP' in s.protocol_name):
            info[spinecho_map_bold].append({'item': s.series_id, 'dir': 'PA'})
        if (s.dim4 == 3) and ('SpinEchoFieldMap_AP' in s.protocol_name):
            info[spinecho_map_bold].append({'item': s.series_id, 'dir': 'AP'})
    return info
