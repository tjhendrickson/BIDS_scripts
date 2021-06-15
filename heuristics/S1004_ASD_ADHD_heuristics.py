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
    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_rec-{rec}_run-{item:02d}_T1w')
    """ TODO: once more data has been collected, will need to add to this
    t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_rec-{rec}_run-{item:02d}_T2w')

    rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_run-{item:02d}_bold')

    task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-fingertap_run-{item:02d}_bold')

    spinecho_map_bold = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-{dir}_run-{item:02d}_epi')

    info = {t1: [], t2: [], rest: [], task: [], spinecho_map_bold: []}
    """
    info = {t1: []}
    for idx, s in enumerate(seqinfo):
        if (s.dim3 == 176) and ('NORM' in s.image_type):
            if 'ABCD_T1' in s.dcm_dir_name:
                rec = 'normalized'
                info[t1].append({'item': s.series_id, 'rec': rec})
            """
            elif 'ABCD_T2' in s.dcm_dir_name:
                rec = 'normalized'
                info[t2].append({'item': s.series_id, 'rec': rec})
            """    
        """
        if (s.dim4 == 383) and ('rest' in s.series_description):
             info[rest].append({'item': s.series_id})

        if (s.dim4 == 394) and ('task' in s.series_description):
            info[task].append({'item': s.series_id})

        if (s.dim4 == 1):
            if 'ABCD_fMRI_DistortionMap_AP' in s.series_description:
                info[spinecho_map_bold].append({'item': s.series_id, 'dir': 'AP'})
            if 'ABCD_fMRI_DistortionMap_PA' in s.series_description:
                info[spinecho_map_bold].append({'item': s.series_id, 'dir': 'PA'})     
        """
    return info
