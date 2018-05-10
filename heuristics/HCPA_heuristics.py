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

    rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-{acq}_run-{item:02d}_bold')
    sbref_rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-{acq}_run-{item:02d}_sbref')

    task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-{TaskName}_acq-{acq}_run-{item:02d}_bold')
    sbref_task = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-{TaskName}_acq-{acq}_run-{item:02d}_sbref')

    asl = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-{TaskName}_acq-{acq}_run-{item:02d}_bold')
    sbref_asl = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-{TaskName}_run-{item:02d}_sbref')

    dwi = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_dwi')
    sbref_dwi = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_sbref')

    spinecho_map_bold = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-{dir}_acq-{acq}_run-{item:02d}_epi')
    turboecho_map_bold = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-{dir}_acq-{acq}_run-{item:02d}_epi')
    spinecho_map_pcasl = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-{acq}_dir-{dir}_run-{item:02d}_epi')

    info = {t1: [], t2: [], rest: [], dwi: [], spinecho_map_bold: [], sbref_rest: [],
            sbref_dwi: [], task: [], sbref_task: [], asl: [], sbref_asl: [], spinecho_map_pcasl: []}

    for idx, s in enumerate(seqinfo):
        if (s.dim3 == 208) and ('NORM' in s.image_type):
            if 'T1w_MPR_vNav_4e_RMS' in s.dcm_dir_name:
                acq = 'MPRvNav4eRMS'
                info[t1].append({'item': s.series_id, 'acq': acq})
            else:
                acq = 'SPCvNav'
                info[t2].append({'item': s.series_id, 'acq': acq})
        if (s.dim4 >= 99) and ('dMRI' in s.protocol_name):
            if 'dir98_AP' in s.protocol_name:
                acq = 'dir98AP'
            elif 'dir98_PA' in s.protocol_name:
                acq = 'dir98PA'
            elif 'dir99_AP' in s.protocol_name:
                acq = 'dir99AP'
            elif 'dir99_PA' in s.protocol_name:
                acq = 'dir99PA'
            info[dwi].append({'item': s.series_id, 'acq': acq})
        if (s.dim4 == 90) and ('PCASL' in s.protocol_name):
            TaskName = "mbPCASLhr"
            acq = 'PA'
            info[asl].append({'item': s.series_id, 'TaskName': TaskName, 'acq': acq})
        if (s.dim4 == 488) and ('REST' in s.protocol_name):
            if 'AP' in s.protocol_name:
                acq = 'eyesopenAP'
            else:
                acq = 'eyesopenPA'
            info[rest].append({'item': s.series_id, 'acq': acq})
        if (s.dim4 == 194) and ('VISMOTOR' in s.protocol_name):
            TaskName = 'VISMOTOR'
            info[task].append({'item': s.series_id, 'acq': 'PA', 'TaskName': TaskName})
        if (s.dim4 == 300) and ('CARIT' in s.protocol_name):
            TaskName = 'CARIT'
            info[task].append({'item': s.series_id, 'acq': 'PA', 'TaskName': TaskName})
        if (s.dim4 == 345) and ('FACENAME' in s.protocol_name):
            TaskName = 'FACENAME'
            info[task].append({'item': s.series_id, 'acq': 'PA', 'TaskName': TaskName})
        if (s.dim4 == 1) and ('PA' in s.protocol_name or 'AP' in s.protocol_name):
            if 'SpinEchoFieldMap' in s.protocol_name:
                if 'PA' in s.protocol_name or 'REV_AP' in s.protocol_name:
                    info[spinecho_map_bold].append({'item': s.series_id, 'acq': 'SE', 'dir': 'PA'})
                else:
                    info[spinecho_map_bold].append({'item': s.series_id, 'acq': 'SE', 'dir': 'AP'})
            if 'PCASL' in s.protocol_name:
                if 'PA' in s.protocol_name or 'REV_AP' in s.protocol_name:
                    info[spinecho_map_pcasl].append({'item': s.series_id, 'acq': 'pcaslSE', 'dir': 'PA'})
                else:
                    info[spinecho_map_pcasl].append({'item': s.series_id, 'acq': 'pcaslSE', 'dir': 'AP'})
            if 'TSE_HiResHp' in s.protocol_name:
                if 'NORM' in s.image_type:
                    acq = 'PreScanNormalized'
                    info[turboecho_map_bold].append({'item': s.series_id, 'dir': 'PA', 'acq': acq})
                else:
                    acq = 'Standard'
                    info[turboecho_map_bold].append({'item': s.series_id, 'dir': 'PA', 'acq': acq})

            if 'REST' in s.protocol_name:
                if 'AP' in s.protocol_name:
                    acq = 'eyesopenAP'
                else:
                    acq = 'eyesopenPA'
                info[sbref_rest].append({'item': s.series_id, 'acq': acq})
            if 'VISMOTOR' in s.protocol_name:
                TaskName = 'VISMOTOR'
                info[sbref_task].append({'item': s.series_id, 'acq': 'PA', 'TaskName': TaskName})
            if 'CARIT' in s.protocol_name:
                TaskName = 'CARIT'
                info[sbref_task].append({'item': s.series_id, 'acq': 'PA', 'TaskName': TaskName})
            if 'FACENAME' in s.protocol_name:
                TaskName = 'FACENAME'
                info[sbref_task].append({'item': s.series_id, 'acq': 'PA', 'TaskName': TaskName})
            if 'dMRI' in s.protocol_name:
                if 'dir98_AP' in s.protocol_name:
                    acq = 'dir98AP'
                elif 'dir98_PA' in s.protocol_name:
                    acq = 'dir98PA'
                elif 'dir99_AP' in s.protocol_name:
                    acq = 'dir99AP'
                elif 'dir99_PA' in s.protocol_name:
                    acq = 'dir99PA'
                info[sbref_dwi].append({'item': s.series_id, 'acq': acq})
        acq = ""
        TaskName = ""
    return info
