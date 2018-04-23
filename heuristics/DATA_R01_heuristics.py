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
    t1 = create_key('sub-{subject}/anat/sub-{subject}_acq-{acq}_run-{item:02d}_T1w')
    t2 = create_key('sub-{subject}/anat/sub-{subject}_acq-{acq}_run-{item:02d}_T2w')

    rest = create_key('sub-{subject}/func/sub-{subject}_task-rest_acq-{acq}_run-{item:02d}_bold')
    sbref_rest = create_key('sub-{subject}/func/sub-{subject}_task-rest_acq-{acq}_run-{item:02d}_sbref')

    spinecho_map_bold = create_key('sub-{subject}/fmap/sub-{subject}_dir-{dir}_run-{item:02d}_epi')

    info = {t1: [], t2: [], rest: [], spinecho_map_bold: [], sbref_rest: []}

    for idx, s in enumerate(seqinfo):
        if (s.dim3 == 160):
            if '7-t1_mpr_sag_eja' in s.series_id:
                info[t1].append({'item': s.series_id, 'acq': 'MprSagEja'})
            elif '9-t2_space' in s.series_id:
                info[t2].append({'item': s.series_id, 'acq': 'space'})
        if (s.dim4 == 755) and ('cmrr_bold_60slices_MB4_2pt4mm_tr1s' in s.protocol_name):
            #if 'AP' in s.protocol_name:
            info[rest].append({'item': s.series_id, 'acq': 'restTR1'})
        if (s.dim4 == 1075) and ('cmrr_bold_60slices_MB6_2pt4mm_tr750ms' in s.protocol_name):
            #if 'AP' in s.protocol_name:
            info[rest].append({'item': s.series_id, 'acq': 'restTR750'})
        if (s.dim4 == 1):
            if 'SpinEchoFieldMap' in s.protocol_name:
                if 'PA' in s.protocol_name:
                    info[spinecho_map_bold].append({'item': s.series_id, 'acq': 'SE', 'dir': 'PA'})
                else:
                    info[spinecho_map_bold].append({'item': s.series_id, 'acq': 'SE', 'dir': 'AP'})
            if 'cmrr_bold_60slices_MB4_2pt4mm_tr1s_SBRef' in s.dcm_dir_name:
                info[sbref_rest].append({'item': s.series_id, 'acq': 'restTR1'})
            if 'cmrr_bold_60slices_MB6_2pt4mm_tr750ms_SBRef' in s.dcm_dir_name:
                info[sbref_rest].append({'item': s.series_id, 'acq': 'restTR750'})
    return info
