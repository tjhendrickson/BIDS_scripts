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
    
    import pdb
    
    # create keys for each modality
    t1_4e_RMS = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-4eRMS_T1w')
    t1_1e = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-1e_T1w')
    t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-SPC_T2w')
    
    pain_images = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-PainImages_run-{item:02d}_bold')
    sbref_pain_images = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-PainImages_run-{item:02d}_sbref')

    qigong_video = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-QigongVideo_run-{item:02d}_bold')
    qigong_video_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-QigongVideo_run-{item:02d}_sbref')

    robot = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-robot_run-{item:02d}_bold')
    robot_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-robot_run-{item:02d}_sbref')

    mental_scan = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-MentalScan_run-{item:02d}_bold')
    mental_scan_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-MentalScan_run-{item:02d}_sbref')

    rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-{item:02d}_bold')
    rest_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-{item:02d}_sbref')
    
    spinecho_map_bold = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-{dir}_run-{item:02d}_epi')

    # place modality keys within python dictionary
    info = {t1_4e_RMS: [], t1_1e: [], t2: [], pain_images: [], 
            sbref_pain_images: [], spinecho_map_bold: [], qigong_video: [], 
            qigong_video_sbref: [], robot: [], robot_sbref: [],
            mental_scan: [], mental_scan_sbref: [], rest: [], rest_sbref: []}

    # now loop through scans acquired for a session and place into modality keys
    for idx, s in enumerate(seqinfo):
        # take a look at the following sequence, this is important for sbref and full scan pairing
        if idx + 1 <= len(seqinfo) - 1:
            s_next = seqinfo[idx+1]
        # dim3 = # of volumes
        # NORM = pre-scan normalize on
        if (s.dim3 == 208) and ('NORM' in s.image_type):
            if 'T1w_MPR_vNav_4e RMS' in s.series_description:
                info[t1_4e_RMS].append({'item': s.series_id})
            elif 'T1w_MPR_vNav_1e' in s.series_description:
                info[t1_1e].append({'item': s.series_id})
            elif 'T2w_SPC_vNav' in s.series_description:
                info[t2].append({'item': s.series_id})
        # dim4 = # of timepoints, useful for EPI (i.e. fMRI) images
        elif (s.dim4 == 833) and ('ROBOT' in s.series_description):
            info[robot].append({'item': s.series_id})
        elif (s.dim4 == 1477) and ('QIGONG VIDEO' in s.series_description):
            info[qigong_video].append({'item': s.series_id})
        elif (s.dim4 == 822) and ('MENTAL SCAN' in s.series_description):
            info[mental_scan].append({'item': s.series_id})
        elif (s.dim4 == 900) and ('REST' in s.series_description):
            info[rest].append({'item': s.series_id})
            
        elif (s.dim4 == 1):
            if 'SpinEchoFieldMap' in s.series_description:
                if '_AP' in s.series_description:
                    info[spinecho_map_bold].append({'item': s.series_id, 'acq': 'SE', 'dir': 'AP'})
                elif '_PA' in s.series_description:
                    info[spinecho_map_bold].append({'item': s.series_id, 'acq': 'SE', 'dir': 'PA'})
            elif ('ROBOT' in s.series_description) and (s_next.dim4 == 833):
                info[robot_sbref].append({'item': s.series_id})
            elif ('QIGONG VIDEO' in s.series_description) and (s_next.dim4 == 1477):
                info[qigong_video_sbref].append({'item': s.series_id})
            elif ('MENTAL SCAN' in s.series_description)  and (s_next.dim4 == 822):
                info[mental_scan_sbref].append({'item': s.series_id})
            elif ('REST' in s.series_description) and (s_next.dim4 == 900):
                info[rest_sbref].append({'item': s.series_id})
    return info
