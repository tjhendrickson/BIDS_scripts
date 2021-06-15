# ONCE SETTLED UNCOMMENT STUDY IN catchup_bids_conversion.py - TJH 20201125

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
    t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-SPC_T2w')
    
    pain_images = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-PainImagery_run-{item:02d}_bold')
    pain_images_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-PainImagery_run-{item:02d}_sbref')

    sensory_stim = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-SensoryStim_run-{item:02d}_bold')
    sensory_stim_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-SensoryStim_run-{item:02d}_sbref')

    robot1 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-robot1_run-{item:02d}_bold')
    robot1_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-robot1_run-{item:02d}_sbref')

    robot2 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-robot2_run-{item:02d}_bold')
    robot2_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-robot2_run-{item:02d}_sbref')

    robot3 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-robot3_run-{item:02d}_bold')
    robot3_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-robot3_run-{item:02d}_sbref')

    mental_scan = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-MentalScan_run-{item:02d}_bold')
    mental_scan_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-MentalScan_run-{item:02d}_sbref')

    mental_scan2 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-MentalScan2_run-{item:02d}_bold')
    mental_scan2_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-MentalScan2_run-{item:02d}_sbref')

    movement_imagery = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-MovementImagery_run-{item:02d}_bold')
    movement_imagery_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-MovementImagery_run-{item:02d}_sbref')
    
    video = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-QigongVideo_run-{item:02d}_bold')
    video_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-QigongVideo_run-{item:02d}_sbref')
    
    rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-{item:02d}_bold')
    rest_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-{item:02d}_sbref')
    
    spinecho_map_bold = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-{dir}_run-{item:02d}_epi')

    # place modality keys within python dictionary
    info = {t1_4e_RMS: [], t2: [], pain_images: [], sensory_stim: [],
            robot1: [], robot2: [], robot3: [], mental_scan: [], mental_scan2: [],
            movement_imagery: [], rest: [], 
            pain_images_sbref: [], sensory_stim_sbref: [], robot1_sbref: [],
            robot2_sbref: [], robot3_sbref: [], mental_scan_sbref: [],
            mental_scan2_sbref: [], video: [], video_sbref: [], movement_imagery_sbref: [],
            rest_sbref: [], spinecho_map_bold: []}

    # now loop through scans acquired for a session and place into modality keys
    for idx, s in enumerate(seqinfo):
        # take a look at the following sequence, this is important for sbref and full scan pairing
        if idx + 1 < len(seqinfo):
            s_next = seqinfo[idx+1]
        # dim3 = # of volumes
        # NORM = pre-scan normalize on
        if (s.dim3 == 208) and ('NORM' in s.image_type):
            if 'T1w_MPR_vNav_4e RMS' in s.series_description:
                info[t1_4e_RMS].append({'item': s.series_id})
            elif 'T2w_SPC_vNav' in s.series_description:
                info[t2].append({'item': s.series_id})
        # dim4 = # of timepoints, useful for EPI (i.e. fMRI) images
        elif (s.dim4 == 833):
            if 'ROBOT1' in s.series_description: 
                info[robot1].append({'item': s.series_id})
            elif 'ROBOT2' in s.series_description: 
                info[robot2].append({'item': s.series_id})
            elif 'ROBOT3' in s.series_description: 
                info[robot3].append({'item': s.series_id})
        elif (s.dim4 >= 600) and ('PAIN_IMAGERY' in s.series_description):
            info[pain_images].append({'item': s.series_id})
        elif (s.dim4 >= 580) and ('MOVEMENT_IMAGERY' in s.series_description):
            info[movement_imagery].append({'item': s.series_id})
        elif (s.dim4 >= 1300) and ('Sensory_Stim' in s.series_description):
            info[sensory_stim].append({'item': s.series_id})
        elif (s.dim4 >= 1450) and ('QIGONG VIDEO' in s.series_description):
            info[video].append({'item': s.series_id})
        elif s.dim4 == 822:
            if 'MENTAL SCAN2' in s.series_description:
                info[mental_scan2].append({'item': s.series_id})
            elif 'MENTAL SCAN' in s.series_description:
                info[mental_scan].append({'item': s.series_id})
        elif (s.dim4 == 900) and ('REST' in s.series_description):
            info[rest].append({'item': s.series_id})
        elif (s.dim4 == 1):
            if 'SpinEchoFieldMap' in s.series_description:
                if '_AP' in s.series_description:
                    info[spinecho_map_bold].append({'item': s.series_id, 'acq': 'SE', 'dir': 'AP'})
                elif '_PA' in s.series_description:
                    info[spinecho_map_bold].append({'item': s.series_id, 'acq': 'SE', 'dir': 'PA'})
            elif s_next.dim4 == 833:
                if 'ROBOT1' in s.series_description: 
                    info[robot1_sbref].append({'item': s.series_id})
                elif 'ROBOT2' in s.series_description: 
                    info[robot2_sbref].append({'item': s.series_id})
                elif 'ROBOT3' in s.series_description: 
                    info[robot3_sbref].append({'item': s.series_id})
            elif (s_next.dim4 >= 600) and ('PAIN_IMAGERY' in s.series_description):
                info[pain_images_sbref].append({'item': s.series_id})
            elif (s_next.dim4 >= 580) and ('MOVEMENT_IMAGERY' in s.series_description):
                info[movement_imagery_sbref].append({'item': s.series_id})
            elif (s_next.dim4 >= 1300) and ('Sensory_Stim' in s.series_description):
                info[sensory_stim_sbref].append({'item': s.series_id})
            elif (s_next.dim4 >= 1450) and ('QIGONG VIDEO' in s.series_description):
                info[video_sbref].append({'item': s.series_id})
            elif s_next.dim4 == 822:
                if 'MENTAL SCAN2' in s.series_description:
                    info[mental_scan2_sbref].append({'item': s.series_id})
                elif 'MENTAL SCAN' in s.series_description:
                    info[mental_scan_sbref].append({'item': s.series_id})    
            elif ('REST' in s.series_description) and (s_next.dim4 == 900):
                info[rest_sbref].append({'item': s.series_id})
    return info
