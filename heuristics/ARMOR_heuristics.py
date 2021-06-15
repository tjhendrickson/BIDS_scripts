# leave this function alone
def create_key(template, outtype=('nii.gz','dicom'), annotation_classes=None): #), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return (template, outtype, annotation_classes)

# function must remain, but content can be changed based on study scan and parameter acqusition
def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    
    # set up python dictionaries for each scan type that will be converted to BIDS
    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_T1w')
    t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_T2w')

    rest_ap = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-AP_run-{item:02d}_bold')
    sbref_rest_ap = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-AP_run-{item:02d}_sbref')
    
    rest_pa = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-PA_run-{item:02d}_bold')
    sbref_rest_pa = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-PA_run-{item:02d}_sbref')

    sg1_task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-SG1_acq-PA_run-{item:02d}_bold')
    sg1_sbref_task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-SG1_acq-PA_run-{item:02d}_sbref')
    
    sg2_task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-SG2_acq-PA_run-{item:02d}_bold')
    sg2_sbref_task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-SG2_acq-PA_run-{item:02d}_sbref')
    
    sg3_task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-SG3_acq-PA_run-{item:02d}_bold')
    sg3_sbref_task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-SG3_acq-PA_run-{item:02d}_sbref')
    
    sg4_task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-SG4_acq-PA_run-{item:02d}_bold')
    sg4_sbref_task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-SG4_acq-PA_run-{item:02d}_sbref')
    
    sg5_task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-SG5_acq-PA_run-{item:02d}_bold')
    sg5_sbref_task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-SG5_acq-PA_run-{item:02d}_sbref')

    dwi98_AP = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-dir98AP_run-{item:02d}_dwi')
    sbref_dwi98_AP = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-dir98AP_run-{item:02d}_sbref')
    
    dwi98_PA = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-dir98PA_run-{item:02d}_dwi')
    sbref_dwi98_PA = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-dir98PA_run-{item:02d}_sbref')

    spinecho_map_bold_AP = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-SpinEcho_dir-AP_run-{item:02d}_epi')
    spinecho_map_bold_PA = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-SpinEcho_dir-PA_run-{item:02d}_epi')
    
    SGspinecho_map_bold_AP = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-SGSpinEcho_dir-AP_run-{item:02d}_epi')
    SGspinecho_map_bold_PA = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-SGSpinEcho_dir-PA_run-{item:02d}_epi')

    info = {t1: [], t2: [], rest_ap: [], sbref_rest_ap: [], rest_pa: [], sbref_rest_pa: [],
            sg1_task: [], sg1_sbref_task: [], sg2_task: [], sg2_sbref_task: [],
            sg3_task: [], sg3_sbref_task: [], sg4_task: [], sg4_sbref_task: [], 
            sg5_task: [], sg5_sbref_task: [], dwi98_AP: [], sbref_dwi98_AP: [],
            dwi98_PA: [], sbref_dwi98_PA: [], spinecho_map_bold_AP: [], spinecho_map_bold_PA: [],
            SGspinecho_map_bold_AP: [], SGspinecho_map_bold_PA: []}

    for idx, s in enumerate(seqinfo):
        # create variable for the next scan in list compared to current
        if idx  + 1 <= len(seqinfo) - 1:
            s_next = seqinfo[idx+1]
        if (s.dim3 == 208) and ('NORM' in s.image_type):
            if 'T1w_MPR_vNav_4e_RMS' in s.dcm_dir_name:
                acq = 'MPRvNav4eRMS'
                info[t1].append({'item': s.series_id, 'acq': acq})
            else:
                acq = 'SPCvNav'
                info[t2].append({'item': s.series_id, 'acq': acq})
        
        # logic to convert dwi scans
        elif (s.dim4 >= 99) and ('dMRI' in s.protocol_name):
            if 'dir98_AP' in s.protocol_name:
                info[dwi98_AP].append({'item': s.series_id})
            elif 'dir98_PA' in s.protocol_name:
                info[dwi98_PA].append({'item': s.series_id})
        
        # logic to convert rest scans
        elif (s.dim4 == 488) and ('REST' in s.protocol_name):
            if 'AP' in s.protocol_name:
                info[rest_ap].append({'item': s.series_id})
            else:
                info[rest_pa].append({'item': s.series_id})
        
        # logic to convert SG task scans
        elif (s.dim4 >= 376) and ('SG' in s.protocol_name):
            if 'SG1' in s.protocol_name:
                info[sg1_task].append({'item': s.series_id})
            elif 'SG2' in s.protocol_name:
                info[sg2_task].append({'item': s.series_id})
            elif 'SG3' in s.protocol_name:
                info[sg3_task].append({'item': s.series_id})
            elif 'SG4' in s.protocol_name:
                info[sg4_task].append({'item': s.series_id})
            elif 'SG5' in s.protocol_name:
                info[sg5_task].append({'item': s.series_id})        
        # logic to convert field maps and single band reference images
        elif s.dim4 == 1:
            if 'SpinEchoFieldMap_PA' in s.protocol_name:
                info[spinecho_map_bold_AP].append({'item': s.series_id})
            elif 'SpinEchoFieldMap_AP' in s.protocol_name:
                info[spinecho_map_bold_PA].append({'item': s.series_id})
            elif ('REST' in s.protocol_name) and (s_next.dim4 == 400):
                if 'AP' in s.protocol_name:
                    info[sbref_rest_ap].append({'item': s.series_id})
                else:
                    info[sbref_rest_pa].append({'item': s.series_id})    
            elif ('SG' in s.protocol_name) and (s_next.dim4 == 607):
                if 'SG1' in s.protocol_name:
                    info[sg1_sbref_task].append({'item': s.series_id})
                elif 'SG2' in s.protocol_name:
                    info[sg2_sbref_task].append({'item': s.series_id})
                elif 'SG3' in s.protocol_name:
                    info[sg3_sbref_task].append({'item': s.series_id})
                elif 'SG4' in s.protocol_name:
                    info[sg4_sbref_task].append({'item': s.series_id})
                elif 'SG5' in s.protocol_name:
                    info[sg5_sbref_task].append({'item': s.series_id})
            elif 'dMRI' in s.protocol_name:
                if ('dir98_AP' in s.protocol_name) and (s_next.dim4 == 99):
                    info[sbref_dwi98_AP].append({'item': s.series_id})
                elif ('dir98_PA' in s.protocol_name) and (s_next.dim4 == 99):
                    info[sbref_dwi98_PA].append({'item': s.series_id})
    return info
