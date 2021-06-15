def create_key(template, outtype=('nii.gz','dicom'), annotation_classes=None): #), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return (template, outtype, annotation_classes)


def infotodict(seqinfo):
    import pdb
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    acq: type (in the case of t1 and t2) or phase encoding direction acquired (in the case of rsfMRI)
    """
    
    # create template formats for each scan modality
    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-T1MPR_run-{item:02d}_T1w')
    t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-T2SPC_run-{item:02d}_T2w')
    
    ket_task1 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-KET1_run-{item:02d}_bold')
    sbref_ket_task1 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-KET1_run-{item:02d}_sbref')
    
    ket_task2 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-KET2_run-{item:02d}_bold')
    sbref_ket_task2 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-KET2_run-{item:02d}_sbref')
    
    ket_task3 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-KET3_run-{item:02d}_bold')
    sbref_ket_task3 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-KET3_run-{item:02d}_sbref')
    
    ket_task4 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-KET4_run-{item:02d}_bold')
    sbref_ket_task4 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-KET4_run-{item:02d}_sbref')

    rest_PA = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-PA_run-{item:02d}_bold') 
    sbref_rest_PA = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-PA_run-{item:02d}_sbref')
    
    dwi_PA = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-79dirb2000PA_run-{item:02d}_dwi')
    dwi_AP = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-79dirb2000AP_run-{item:02d}_dwi')

    spinecho_map_AP_bold = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-AP_run-{item:02d}_epi')
    spinecho_map_PA_bold = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-PA_run-{item:02d}_epi')
    
    # place template formats into a python dictionary
    info = {t1: [], t2: [], ket_task1: [], ket_task2: [], ket_task3: [], 
            ket_task4: [], rest_PA: [], spinecho_map_AP_bold: [],
            spinecho_map_PA_bold: [], sbref_rest_PA: [], 
            sbref_ket_task1: [], sbref_ket_task2: [], sbref_ket_task3: [],
            sbref_ket_task4: [], dwi_PA: [], dwi_AP: []}
    # loop through acquired scans based on dicom directory and add to dictionary "info"
    for idx, s in enumerate(seqinfo):
        if idx + 1 < len(seqinfo) - 1:
            s_next = seqinfo[idx+1]
        if (s.dim3 == 208) and ('NORM' in s.image_type):
            if 'T1w' in s.protocol_name:
                info[t1].append({'item': s.series_id})
            elif 'T2w' in s.protocol_name:
                info[t2].append({'item': s.series_id})
        elif s.dim4 == 1040:
            if 'REST_PA' in s.protocol_name:
                info[rest_PA].append({'item': s.series_id})
        elif s.dim4 == 100:
            if 'KET_TASK1_PA' in s.protocol_name:
                info[ket_task1].append({'item': s.series_id})
            elif 'KET_TASK2_PA' in s.protocol_name:
                info[ket_task2].append({'item': s.series_id})
            elif 'KET_TASK3_PA' in s.protocol_name:
                info[ket_task3].append({'item': s.series_id})
            elif 'KET_TASK4_PA' in s.protocol_name:
                info[ket_task4].append({'item': s.series_id})
        elif s.dim4 == 1:
            if 'KET_TASK1_PA' in s.protocol_name:
                if s_next.dim4 == 100:
                    info[sbref_ket_task1].append({'item': s.series_id})
            elif 'KET_TASK2_PA' in s.protocol_name:
                if s_next.dim4 == 100:                
                    info[sbref_ket_task2].append({'item': s.series_id})
            elif 'KET_TASK3_PA' in s.protocol_name:
                if s_next.dim4 == 100:
                    info[sbref_ket_task3].append({'item': s.series_id})
            elif 'KET_TASK4_PA' in s.protocol_name:
                if s_next.dim4 == 100:
                    info[sbref_ket_task4].append({'item': s.series_id})
            elif 'REST_PA' in s.protocol_name:
                if s_next.dim4 == 1040:
                    info[sbref_rest_PA].append({'item': s.series_id})
        elif (s.dim4 == 3) and ('SpinEchoFieldMap_PA' in s.protocol_name):
            info[spinecho_map_PA_bold].append({'item': s.series_id})
        elif (s.dim4 == 3) and ('SpinEchoFieldMap_REV_PA' in s.protocol_name):
            info[spinecho_map_AP_bold].append({'item': s.series_id})
        elif (s.dim4 == 159) and ('DWI_79dir_b2000_rev_PA' in s.protocol_name):
            info[dwi_AP].append({'item': s.series_id})
        elif (s.dim4 == 159) and ('DWI_79dir_b2000_PA' in s.protocol_name):
            info[dwi_PA].append({'item': s.series_id})

    return info
