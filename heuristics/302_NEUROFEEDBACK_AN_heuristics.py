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
    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-{acq}_T1w')
    t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-{acq}_T2w')

    rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-{acq}_run-{item:02d}_bold')
    sbref_rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-{acq}_run-{item:02d}_sbref')

    RT_task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-RT_run-{item:02d}_bold')
    RT_task_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-RT_run-{item:02d}_sbref')

    spinecho_map_bold = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-{dir}_run-{item:02d}_epi')

    # place modality keys within python dictionary
    info = {t1: [], t2: [], RT_task: [], rest: [], spinecho_map_bold: [], RT_task_sbref: [], sbref_rest: []}

    # now loop through scans acquired for a session and place into modality keys
    for idx, s in enumerate(seqinfo):
        # take a look at the following sequence, this is important for sbref and full scan pairing
        if idx + 1 <= len(seqinfo) - 1:
            s_next = seqinfo[idx+1]
        
        # dim3 = # of volumes
        # NORM = pre-scan normalize on
        if (s.dim3 == 192) and ('NORM' in s.image_type):
            if 'T1w_MPR_vNav_4e_RMS' in s.dcm_dir_name:
                acq = 'MPRvNav4eRmsNorm'
                info[t1].append({'item': s.series_id, 'acq': acq})
            else:
                acq = 'SPCvNavNorm'
                info[t2].append({'item': s.series_id, 'acq': acq})
        # dim4 = # of timepoints, useful for EPI (i.e. fMRI) images
        elif (s.dim4 == 375) and ('fMRI_REST_AP' in s.protocol_name):
            acq = 'AP'
            info[rest].append({'item': s.series_id, 'acq': acq})
        elif (s.dim4 == 474) and ('RT_Task' in s.protocol_name):
            info[RT_task].append({'item': s.series_id})
        elif (s.dim4 == 1):
            if 'SEFieldMap' in s.protocol_name:
                if 'REV' in s.protocol_name:
                    info[spinecho_map_bold].append({'item': s.series_id, 'acq': 'SE', 'dir': 'PA'})
                else:
                    info[spinecho_map_bold].append({'item': s.series_id, 'acq': 'SE', 'dir': 'AP'})
            elif ('fMRI_REST_AP' in s.protocol_name) and (s_next.dim4 == 375):
                acq = 'AP'
                info[sbref_rest].append({'item': s.series_id, 'acq': acq})
            elif ('RT_Task' in s.protocol_name) and (s_next.dim4 == 474):
                info[RT_task_sbref].append({'item': s.series_id})
    return info
