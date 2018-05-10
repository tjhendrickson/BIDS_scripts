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
    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_T1w')
    t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_T2w')
    flair = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_FLAIR')

    task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-{acq}_run-{item:02d}_bold')
    sbref_task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-{acq}_run-{item:02d}_sbref')

    rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-{acq}_run-{item:02d}_bold')
    sbref_rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-{acq}_run-{item:02d}_sbref')

    dwi = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_dwi')

    gradecho_map_bold = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_fieldmap')
    sbref_gradecho = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-{acq}_run-{item:02d}_sbref')

    spinecho_map_bold = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-{acq}_dir-{dir}_run-{item:02d}_epi')


    info = {t1: [], t2: [], flair: [], task: [], rest: [], dwi: [], spinecho_map_bold: [], sbref_gradecho: [],
            gradecho_map_bold: [], sbref_rest: [], sbref_task: []}

    for idx, s in enumerate(seqinfo):
        if (s.dim3 == 208) and ('NORM' in s.image_type):
            if 'T1w' in s.dcm_dir_name:
                acq = 'T1MPR'
                info[t1].append({'item': s.series_id, 'acq': acq})
            elif 'T2w_SPC' in s.dcm_dir_name:
                acq = 'T2SPC'
                info[t2].append({'item': s.series_id, 'acq': acq})
            elif 'FLAIR' in s.dcm_dir_name:
                acq = "SagIsoFs"
                info[flair].append({'item': s.series_id, 'acq': acq})
        if (s.dim4 == 159) and ('DWI' in s.protocol_name):
            if 'REV_AP' in s.protocol_name or 'PA' in s.protocol_name:
                acq = 'PA'
                info[dwi].append({'item': s.series_id, 'acq': acq})
            else:
                acq = 'AP'
                info[dwi].append({'item': s.series_id, 'acq': acq})
        if (s.dim4 == 600) and ('REST' in s.protocol_name):
            acq = 'eyesopenPA'
            info[rest].append({'item': s.series_id, 'acq': acq})
        if (s.dim4 == 10) and ('REST' in s.protocol_name):
            info[gradecho_map_bold].append({'item': s.series_id, 'acq': 'gradechoAP'})
        if (s.dim4 > 1) and ('RETINOTOPY' in s.protocol_name):
            if 'RETINOTOPY_RUN1' in s.dcm_dir_name:
                acq = 'retinoRun1PA'
                info[task].append({'item': s.series_id, 'acq': acq})
            elif 'RETINOTOPY_RUN2' in s.dcm_dir_name:
                acq = 'retinoRun2PA'
                info[task].append({'item': s.series_id, 'acq': acq})
            elif 'RETINOTOPY_RUN3' in s.dcm_dir_name:
                acq = 'retinoRun3PA'
                info[task].append({'item': s.series_id, 'acq': acq})
            elif 'RETINOTOPY_RUN4' in s.dcm_dir_name:
                acq = 'retinoRun4PA'
                info[task].append({'item': s.series_id, 'acq': acq})
        if (s.dim4 == 1):
            if ('REST_EO_PA' in s.protocol_name):
                acq = 'eyesopenPA'
                info[sbref_rest].append({'item': s.series_id, 'acq': acq})
            elif ('REST_REV_PA' in s.protocol_name):
                info[sbref_gradecho].append({'item': s.series_id, 'acq': 'gradechoAP'})
            elif ('RETINOTOPY' in s.protocol_name):
                if 'RETINOTOPY_RUN1_PA' in s.protocol_name:
                    acq = 'retinoRun1PA'
                    info[sbref_task].append({'item': s.series_id, 'acq': acq})
                elif 'RETINOTOPY_RUN2_PA' in s.protocol_name:
                    acq = 'retinoRun2PA'
                    info[sbref_task].append({'item': s.series_id, 'acq': acq})
                elif 'RETINOTOPY_RUN3_PA' in s.protocol_name:
                    acq = 'retinoRun3PA'
                    info[sbref_task].append({'item': s.series_id, 'acq': acq})
                elif 'RETINOTOPY_RUN4_PA' in s.protocol_name:
                    acq = 'retinoRun4PA'
                    info[sbref_task].append({'item': s.series_id, 'acq': acq})
        if (s.dim4 == 3) and ('SpinEchoFieldMap_PA' in s.protocol_name):
            acq = 'SE'
            info[spinecho_map_bold].append({'item': s.series_id, 'acq': acq, 'dir': 'PA'})
        if (s.dim4 == 3) and ('SpinEchoFieldMap_REV_PA' in s.protocol_name):
            acq = 'SE'
            info[spinecho_map_bold].append({'item': s.series_id, 'acq': acq, 'dir': 'AP'})
    return info
