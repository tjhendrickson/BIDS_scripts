import pdb

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
    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-{acq}_T1w')
    t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-{acq}_T2w')

    rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-{acq}_run-{item:02d}_bold')
    sbref_rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-{acq}_run-{item:02d}_sbref')

    dwi = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_dwi')
    sbref_dwi = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-{acq}_run-{item:02d}_sbref')

    spinecho_map_bold = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-{dir}_run-{item:02d}_epi')

    info = {t1: [], t2: [], rest: [], dwi: [], spinecho_map_bold: [], sbref_rest: [], sbref_dwi: []}

    for idx, s in enumerate(seqinfo):
        if idx + 1 < len(seqinfo) - 1:
            s_next = seqinfo[idx+1]
        if (s.dim3 == 208) and ('NORM' in s.image_type):
            if 'T1w_MPR_vNav_4e_RMS' in s.dcm_dir_name:
                acq = 'MPRvNav4eRMS'
                info[t1].append({'item': s.series_id, 'acq': acq})
            elif 'T2w_SPC_vNav' in s.series_description:
                acq = 'SPCvNav'
                info[t2].append({'item': s.series_id, 'acq': acq})
        elif (s.dim4 >= 99) and ('dMRI' in s.protocol_name):
            if 'dir98_AP' in s.protocol_name:
                acq = 'dir98AP'
                info[dwi].append({'item': s.series_id, 'acq': acq})
            elif 'dir98_PA' in s.protocol_name:
                acq = 'dir98PA'
                info[dwi].append({'item': s.series_id, 'acq': acq})
        elif (s.dim4 == 488) and ('REST' in s.protocol_name):
            if 'AP' in s.protocol_name:
                acq = 'eyesopenAP'
                info[rest].append({'item': s.series_id, 'acq': acq})
            else:
                acq = 'eyesopenPA'
                info[rest].append({'item': s.series_id, 'acq': acq})
        elif (s.dim4 == 1):
            if 'SpinEchoFieldMap' in s.protocol_name:
                if 'PA' in s.protocol_name:
                    info[spinecho_map_bold].append({'item': s.series_id, 'acq': 'SE', 'dir': 'PA'})
                else:
                    info[spinecho_map_bold].append({'item': s.series_id, 'acq': 'SE', 'dir': 'AP'})
            elif 'REST' in s.protocol_name:
                if s_next.dim4 == 488:
                    if 'AP' in s.protocol_name:
                        acq = 'eyesopenAP'
                        info[sbref_rest].append({'item': s.series_id, 'acq': acq})
                    else:
                        acq = 'eyesopenPA'
                        info[sbref_rest].append({'item': s.series_id, 'acq': acq})
            elif 'dMRI' in s.protocol_name:
                if s_next.dim4 >= 99:
                    if 'dir98_AP' in s.protocol_name:
                        acq = 'dir98AP'
                    elif 'dir98_PA' in s.protocol_name:
                        acq = 'dir98PA'
                    elif 'dir99_AP' in s.protocol_name:
                        acq = 'dir99AP'
                    elif 'dir99_PA' in s.protocol_name:
                        acq = 'dir99PA'
                    info[sbref_dwi].append({'item': s.series_id, 'acq': acq})
    return info
