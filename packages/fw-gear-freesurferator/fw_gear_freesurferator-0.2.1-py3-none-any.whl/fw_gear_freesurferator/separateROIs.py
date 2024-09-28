"""ROI separator functions for thalamus, hippocampus, etc."""

import logging
import os
import shutil
import subprocess as sp

log = logging.getLogger(__name__)


# Create the two hemispheres
def createHemiMaskFromAseg(asegFile: str) -> None:
    """Create hemi masks from aseg.

    Arguments:
        asegFile (str): Path to Freesurfer's aseg file.
    """
    import os

    import nibabel as nib
    import numpy as np

    # Read the aseg file
    aseg = nib.load(asegFile)
    asegData = aseg.get_fdata()
    # Read the Look up table
    fLUT = open(
        os.path.join(os.getenv("FREESURFER_HOME"), "FreeSurferColorLUT.txt"), "r"
    )
    LUT = fLUT.readlines()
    fLUT.close()
    cleanLUT = [s for s in LUT if "#" not in s]
    # Obtain the labels per each hemi
    leftLUT = [int(s.split()[0]) for s in cleanLUT if "Left" in s or "lh" in s]
    rightLUT = [int(s.split()[0]) for s in cleanLUT if "Right" in s or "rh" in s]
    # Create the two hemispheres
    leftMask = nib.Nifti1Image(np.isin(asegData, leftLUT), aseg.affine, aseg.header)
    rightMask = nib.Nifti1Image(np.isin(asegData, rightLUT), aseg.affine, aseg.header)
    # Write the new niftis
    (head, tail) = os.path.split(asegFile)
    nib.save(leftMask, os.path.join(head, "lh.AsegMask.nii.gz"))
    nib.save(rightMask, os.path.join(head, "rh.AsegMask.nii.gz"))
    print("Created ?h.AsegMask.nii.gz in the same folder as the input file")


def sep_thalamus(ThN: str, ThLUT: str) -> None:
    """Separates Thalamic subnuclei results into individual ROIs.

    Arguments:
        ThN (str): Thalamic segmentation file.
        ThLUT (str): Look Up Table with codes for each thalamic subnuclei.
    """
    join = os.path.join

    fLUT = open(ThLUT)
    LUT = fLUT.readlines()
    fLUT.close()
    cleanLUT = [s for s in LUT if "-" in s and "#" not in s]
    # Obtain the labels of thalamic nuclei
    index = [
        int(s.split()[0])
        for s in cleanLUT
        if 8100 < int(s.split()[0]) and int(s.split()[0]) < 8300
    ]
    label = [
        str(s.split()[1])
        for s in cleanLUT
        if 8100 < int(s.split()[0]) and int(s.split()[0]) < 8300
    ]
    (head, tail) = os.path.split(ThN)
    # dilstr = ['', '_dil-1', '_dil-2']; diloption = ['', '-dilate 1', '-dilate 2']
    dilstr = [""]
    diloption = [""]
    for i in range(len(index)):
        # extract nuclei
        for x in range(len(dilstr)):
            roiname = join(head, "ROIs", f"{label[i]}{dilstr[x]}.nii.gz")
            cmd = f"mri_extract_label {diloption[x]} {ThN} {index[i]} {roiname}"
            log.info("Command for extracting labels:\n'%s'", cmd)
            a = sp.run(cmd, shell=True, check=False)
            if a == 1:
                if os.path.exists(roiname):
                    os.remove(roiname)
                continue
            # binarize the ROIs
            cmd = f"mri_binarize --min 0.1 --i {roiname} --o {roiname}"
            log.info("Command for mri_binarize:\n'%s'", cmd)
            sp.run(cmd, shell=True, check=False)


def sep_hcp(work_dir: str, fs_dir: str, templates_dir: str, rois_dir: str) -> None:
    """Exract the individual ROIs from HCP atlas.

    Arguments:
        work_dir (str): Flywheel's work directory.
        fs_dir (str): Freesurfer's home directory.
        templates_dir (str): Flywheel's templates directory.
        rois_dir (str): Flywheel's subject space roi directory.
    """
    join = os.path.join

    hcp = join(fs_dir, "Glasser_HCP_v1.0.nii.gz")
    hcpLUT = join(templates_dir, "LUT_HCP.txt")

    shutil.copy(join(work_dir, "Glasser_HCP_v1.0.nii.gz"), fs_dir)

    fLUT = open(hcpLUT)
    LUT = fLUT.readlines()
    fLUT.close()
    cleanLUT = [s.rstrip("\n") for s in LUT if "#" not in s]
    # Obtain the labels of thalamic nuclei
    index = [int(s.split()[0]) for s in cleanLUT]
    label = [str(s.split()[1]) for s in cleanLUT]
    (head, tail) = os.path.split(hcp)
    # dilstr = ['', '_dil-1', '_dil-2']; diloption = ['', '-dilate 1', '-dilate 2']
    dilstr = [""]
    diloption = [""]
    for i in range(len(index)):
        # extract nuclei
        for x in range(len(dilstr)):
            roiname = join(head, "ROIs", f"{label[i]}{dilstr[x]}.nii.gz")
            cmd = f"mri_extract_label {diloption[x]} {hcp} {index[i]} {roiname}"
            log.info("Command for extracting labels:\n'%s'", cmd)
            a = sp.run(cmd, shell=True, check=False)
            if a == 1:
                if os.path.exists(roiname):
                    os.remove(roiname)
                continue
            # binarize the ROIs
            cmd = f"mri_binarize --min 0.1 --i {roiname} --o {roiname}"
            log.info("Command for mri_binarize:\n'%s'", cmd)
            sp.run(cmd, shell=True, check=False)

    # Create motor and auditory cortex ROIs
    for hemi in ["L", "R"]:
        cmd1 = (
            f"3dcalc -a {join(rois_dir,hemi+'_Primary_Auditory_Cortex.nii.gz')} "
            f"-b {join(rois_dir,hemi+'_Lateral_Belt_Complex.nii.gz')} "
            f"-c {join(rois_dir,hemi+'_Medial_Belt_Complex.nii.gz')} "
            f"-d {join(rois_dir,hemi+'_ParaBelt_Complex.nii.gz')} "
            "-expr 'step(a+b+c+d)' "
            f"-prefix {join(rois_dir,hemi+'_A1_Belt.nii.gz')} -overwrite "
        )
        log.info("Launching 3dcalc for motor and auditory cortex rois:\n'%s'", cmd1)
        sp.run(cmd1, shell=True, check=False)

        cmd2 = (
            f"3dcalc -a {join(rois_dir,hemi+'_Area_6_anterior.nii.gz')} "
            f"-b {join(rois_dir,hemi+'_Dorsal_area_6.nii.gz')} "
            "-expr 'step(a+b)' "
            f"-prefix {join(rois_dir,hemi+'_dlPremotor.nii.gz')} -overwrite "
        )
        log.info("Launching 3dcalc for motor and auditory cortex rois:\n'%s'", cmd2)
        sp.run(cmd2, shell=True, check=False)

        cmd3 = (
            f"3dcalc -a {join(rois_dir,hemi+'_Area_3a.nii.gz')} "
            f"-b {join(rois_dir,hemi+'_Primary_Sensory_Cortex.nii.gz')} "
            f"-c {join(rois_dir,hemi+'_Area_1.nii.gz')} "
            f"-d {join(rois_dir,hemi+'_Area_2.nii.gz')} "
            "-expr 'step(a+b+c+d)' "
            f"-prefix {join(rois_dir,hemi+'_S1.nii.gz')} -overwrite "
        )
        log.info("Launching 3dcalc for motor and auditory cortex rois:\n'%s'", cmd3)
        sp.run(cmd3, shell=True, check=False)


def sep_neuropythy(fullpath: str) -> None:
    """Separate Neuropythy results in individual ROIs.

    Arguments:
        fullpath (str): Path to neuropythy result's file.
    """
    join = os.path.join

    (head, tail) = os.path.split(fullpath)

    # if Aseg do not have left and right mask, generate them
    aseg = join(head, "aparc+aseg.nii.gz")
    if not os.path.isfile(join(head, "lh.AsegMask.nii.gz")):
        createHemiMaskFromAseg(aseg)

    # Detect the type of segmentation, Benson or Wang
    if "benson" in tail:
        dic_roi = {
            1: "V1",
            2: "V2",
            3: "V3",
            4: "hV4",
            5: "VO1",
            6: "VO2",
            7: "LO1",
            8: "LO2",
            9: "TO1",
            10: "TO2",
            11: "V3b",
            12: "V3a",
        }
    elif "wang" in tail:
        dic_roi = {
            1: "wang_V1v",
            2: "wang_V1d",
            3: "wang_V2v",
            4: "wang_V2d",
            5: "wang_V3v",
            6: "wang_V3d",
            7: "wang_hV4",
            8: "wang_VO1",
            9: "wang_VO2",
            10: "wang_PHC1",
            11: "wang_PHC2",
            12: "wang_MST",
            13: "wang_hMT",
            14: "wang_LO2",
            15: "wang_LO1",
            16: "wang_V3b",
            17: "wang_V3a",
            18: "wang_IPS0",
            19: "wang_IPS1",
            20: "wang_IPS2",
            21: "wang_IPS3",
            22: "wang_IPS4",
            23: "wang_IPS5",
            24: "wang_SPL1",
            25: "wang_FEF",
        }
    else:
        log.info("The file '%s' does not contain benson or wang, returning", tail)
        return

    for index in dic_roi:
        dilstr = [""]
        diloption = [""]
        for i in range(len(dilstr)):
            roiname = join(head, "ROIs", f"{dic_roi[index]}{dilstr[i]}.nii.gz")
            # extract benson varea
            cmd = f"mri_extract_label {diloption[i]} {fullpath} {index} {roiname}"
            log.info("Command for extracting labels:\n'%s'", cmd)
            a = sp.run(cmd, shell=True, check=False)
            if a == 1:
                if os.path.exists(roiname):
                    os.remove(roiname)
                continue
            # mask left and right hemisphere
            # extract the left
            head_tail = os.path.split(roiname)
            lhname = join(head_tail[0], "Left-" + head_tail[1])
            rhname = join(head_tail[0], "Right-" + head_tail[1])
            # extract the left
            cmd = (
                "mri_binarize "
                f"--mask {join(head, 'lh.AsegMask.nii.gz')} "
                " --min 0.1 "
                f"--i {roiname} "
                f" --o {lhname}"
            )
            log.info("Command for left mri_binarize:\n'%s'", cmd)
            sp.run(cmd, shell=True, check=False)
            # extract the right
            cmd = (
                "mri_binarize "
                f"--mask {join(head, 'rh.AsegMask.nii.gz')} "
                " --min 0.1 "
                f"--i {roiname} "
                f" --o {rhname}"
            )
            log.info("Command for right mri_binarize:\n'%s'", cmd)
            sp.run(cmd, shell=True, check=False)
            os.remove(roiname)


def sep_cb(atlas_file: str, fs_dir: str) -> None:
    """Extract the individual volumetric ROIs from cerebellum.

    Arguments:
        atlas_file (str): path to the segmented file.
        fs_dir (str): Freesurfer's home directory.
    """
    # extract Cerebellum
    join = os.path.join

    (head, tail) = os.path.split(atlas_file)

    shutil.copy(atlas_file, join(fs_dir, tail))

    atlas_file = join(fs_dir, tail)
    # if Aseg do not have left and right mask, generate them
    if not os.path.isfile(join(fs_dir, "lh.AsegMask.nii.gz")):
        createHemiMaskFromAseg(join(fs_dir, "aparc+aseg.nii.gz"))

    roinum_list = [
        ("Left_I_IV", 1),
        ("Right_I_IV", 2),
        ("Left_V", 3),
        ("Right_V", 4),
        ("Left_VI", 5),
        ("Vermis_VI", 6),
        ("Right_VI", 7),
        ("Left_CrusI", 8),
        ("Vermis_CrusI", 9),
        ("Right_CrusI", 10),
        ("Left_CrusII", 11),
        ("Vermis_CrusII", 12),
        ("Right_CrusII", 13),
        ("Left_VIIb", 14),
        ("Vermis_VIIb", 15),
        ("Right_VIIb", 16),
        ("Left_VIIIa", 17),
        ("Vermis_VIIIa", 18),
        ("Right_VIIIa", 19),
        ("Left_VIIIb", 20),
        ("Vermis_VIIIb", 21),
        ("Right_VIIIb", 22),
        ("Left_IX", 23),
        ("Vermis_IX", 24),
        ("Right_IX", 25),
        ("Left_X", 26),
        ("Vermis_X", 27),
        ("Right_X", 28),
        ("Left_Dentate", 29),
        ("Right_Dentate", 30),
        ("Left_Interposed", 31),
        ("Right_Interposed", 32),
        ("Left_Fastigial", 33),
        ("Right_Fastigial", 34),
    ]
    for roinum in roinum_list:
        roi = roinum[0]
        num = str(roinum[1])
        cmd = (
            f"mri_extract_label "
            f"{join(fs_dir,'Cerebellum-MNIsegment_ind.nii.gz')} "
            f"{num} {join(fs_dir,'ROIs',roi+'.nii.gz')} "
        )
        log.info("Extracting cerebellum nuclei with \n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)


def segAparc2009(aparc_file: str) -> None:
    """Extract the individual volumetric ROIs from aparc2009.

    Arguments:
        aparc_file (str): path to aparc segmentation file.
    """
    import os
    import subprocess as sp

    (head, tail) = os.path.split(aparc_file)
    fLUT = open(
        os.path.join(os.getenv("FREESURFER_HOME"), "FreeSurferColorLUT.txt"), "r"
    )
    LUT = fLUT.readlines()
    fLUT.close()
    cleanLUT = [s for s in LUT if ("#" not in s) and (s != "\n")]
    # Obtain the labels of aparc+aseg.nii.gz
    index = [
        int(s.split()[0])
        for s in cleanLUT
        if (11100 < int(s.split()[0]) and int(s.split()[0]) < 12175)
        or (0 < int(s.split()[0]) and int(s.split()[0]) < 180)
    ]
    label = [
        str(s.split()[1])
        for s in cleanLUT
        if (11100 < int(s.split()[0]) and int(s.split()[0]) < 12175)
        or (0 < int(s.split()[0]) and int(s.split()[0]) < 180)
    ]

    for i in range(len(index)):
        # dilstr = ['', '_dil-1', '_dil-2']; diloption = ['', '-dilate 1', '-dilate 2']
        dilstr = [""]
        diloption = [""]
        for x in range(len(dilstr)):
            #  extract nuclei
            roiname = os.path.join(head, "ROIs", f"{label[i]}{dilstr[x]}.nii.gz")
            cmd = (
                f"mri_extract_label -exit_none_found {diloption[x]} {aparc_file} "
                f"{index[i]} {roiname}"
            )
            log.info("Command for extracting labels:\n'%s'", cmd)
            a = sp.call(cmd, shell=True)
            if a == 1:
                if os.path.exists(roiname):
                    os.remove(roiname)
                continue

            cmd = f"mri_binarize --min 0.1 --i {roiname} --o {roiname}"
            log.info("Command for mri_binarize:\n'%s'", cmd)
            sp.call(cmd, shell=True)


def sep_brainstem(bs: str) -> None:
    """Extract the individual ROIs from brainstem segmentation.

    Arguments:
        bs (str): path to segmented brainstem file.
    """
    join = os.path.join
    (head, tail) = os.path.split(bs)
    fLUT = open(join(os.getenv("FREESURFER_HOME"), "FreeSurferColorLUT.txt"), "r")
    LUT = fLUT.readlines()
    fLUT.close()
    cleanLUT = [s for s in LUT if ("#" not in s) and (s != "\n")]
    # Obtain the labels of brainstemSsLabels.FSvoxelSpace.nii.gz
    index = [
        int(s.split()[0])
        for s in cleanLUT
        if (173 <= int(s.split()[0]) and int(s.split()[0]) <= 178)
    ]
    label = [
        str(s.split()[1])
        for s in cleanLUT
        if (173 <= int(s.split()[0]) and int(s.split()[0]) <= 178)
    ]

    for i in range(len(index)):
        #  extract nuclei
        roiname = join(head, "ROIs", f"{label[i]}.nii.gz")
        cmd = f"mri_extract_label -exit_none_found {bs} {index[i]} {roiname}"
        log.info("Command for extracting labels:\n'%s'", cmd)
        a = sp.call(cmd, shell=True)
        if a == 1:
            if os.path.exists(roiname):
                os.remove(roiname)
            continue
        cmd = f"mri_binarize --min 0.1 --i {roiname} --o {roiname}"
        log.info("Command for mri_binarize:\n'%s'", cmd)
        sp.call(cmd, shell=True)


def sep_hippo(fs_dir: str) -> None:
    """Extract the individual ROIs from hippocampal segmentation.

    Arguments:
        fs_dir (str): Freesurfer's home directory.
    """
    join = os.path.join

    fLUT = open(join(os.getenv("FREESURFER_HOME"), "FreeSurferColorLUT.txt"), "r")
    LUT = fLUT.readlines()
    fLUT.close()
    cleanLUT = [s for s in LUT if ("#" not in s) and (s != "\n")]
    # Obtain the labels of *h.hippoAmygLabels-T1.FSvoxelSpace.nii.gz
    index = [
        int(s.split()[0])
        for s in cleanLUT
        if (211 <= int(s.split()[0]) and int(s.split()[0]) <= 246)
        or (7001 <= int(s.split()[0]) and int(s.split()[0]) <= 7101)
        or int(s.split()[0]) == 203
    ]
    label = [
        str(s.split()[1])
        for s in cleanLUT
        if (211 <= int(s.split()[0]) and int(s.split()[0]) <= 246)
        or (7001 <= int(s.split()[0]) and int(s.split()[0]) <= 7101)
        or int(s.split()[0]) == 203
    ]

    for i in range(len(index)):
        # skip whole Amygdala
        if index[i] == 218:
            continue
        #  extract from Left hemi
        roiname = join(fs_dir, "ROIs", f"Left-{label[i]}.nii.gz")
        cmd = (
            "mri_extract_label -exit_none_found "
            f"{join(fs_dir, 'lh.hippoAmygLabels-T1.FSvoxelSpace.nii.gz')} "
            f"{index[i]} "
            f"{roiname}"
        )
        log.info("mri_extract_label using command:\n'%s'", cmd)
        a = sp.call(cmd, shell=True)
        if a == 1:
            if os.path.exists(roiname):
                os.remove(roiname)
            continue
        cmd = f"mri_binarize --min 0.1 --i {roiname} --o {roiname}"
        log.info(cmd)
        sp.run(cmd, shell=True, check=False)
        # extract from Right hemi
        roiname = join(fs_dir, "ROIs", f"Right-{label[i]}.nii.gz")
        cmd = (
            "mri_extract_label -exit_none_found "
            f"{join(fs_dir, 'rh.hippoAmygLabels-T1.FSvoxelSpace.nii.gz')} "
            f"{index[i]} {roiname}"
        )
        log.info("Command for extracting labels:\n'%s'", cmd)
        sp.call(cmd, shell=True)
        cmd = f"mri_binarize --min 0.1 --i {roiname} --o {roiname}"
        log.info("Command for mri_binarize:\n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)
