"""Segmentation functions."""

import logging
import os
import shutil
import subprocess as sp

import fw_gear_freesurferator.separateROIs as sep

log = logging.getLogger(__name__)

join = os.path.join


# Auxiliary functions
def fix_aseg_if_infant(mri_dir: str) -> None:
    """Fixes "aseg" file from InfantFS.

    InfantFS has less files and a different "aseg" file. This function fixes it, so
    that freesurferator can be used with infants.

    Arguments:
        mri_dir (str): Freesurfer's mri directory.
    """
    import os

    import nibabel as nib
    import numpy as np
    from scipy import ndimage

    # Backup the old aseg
    os.rename(os.path.join(mri_dir, "aseg.mgz"), os.path.join(mri_dir, "aseg_old.mgz"))

    # Read the old one
    img = nib.load(os.path.join(mri_dir, "aseg_old.mgz"))

    # Extract the data
    data = img.get_fdata()

    # Fix thalamus
    data[data == 9] = 10
    data[data == 48] = 49

    # Fix medulla
    data[np.logical_and(data >= 173, data <= 175)] = 16

    # fix vermis
    CL = data == 8
    CR = data == 47
    DL = ndimage.morphology.distance_transform_edt(CL == 0)
    DR = ndimage.morphology.distance_transform_edt(CR == 0)
    data[np.logical_and(data == 172, DL < DR)] = 8
    data[data == 172] = 47

    # save the file
    newimg = nib.Nifti1Image(data, img.affine, img.header)
    nib.save(newimg, os.path.join(mri_dir, "aseg.mgz"))


# Segmentation functions
def run_gtmseg(subject_id: str, work_dir: str) -> None:
    """Runs gtm segmentation used for PETsurfer.

    Arguments:
        subject_id (str): Freesurfer's subject id, usually Sxxx.
        work_dir (str): Flywheel's work directory.
    """
    log.info("Running run_gtmseg. Checking if it has been already run...")

    # Specify the SUBJECTS_DIR name
    os.environ["SUBJECTS_DIR"] = work_dir

    gtmfile = join(work_dir, subject_id, "mri", "gtmseg.mgz")

    if os.path.isfile(gtmfile):
        log.info("   ... not running gtmseg, '%s' exists.", gtmfile)
    else:
        cmd = f"gtmseg --s {subject_id} "
        log.info("   ... running gtmseg with this command:\n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)


def segment_cerebellum(work_dir: str, mri_dir: str, templates_dir: str) -> None:
    """Segments the cerebellum using Cerebellum-MNIsegment.nii.gz template.

    Arguments:
        work_dir (str): Flywheel's work directory.
        mri_dir (str): Freesurfer's work directory.
        templates_dir (str): Flywheel's templates directory.
    """
    log.info("Running segment_cerebellum. ")

    # Specify the SUBJECTS_DIR name
    os.environ["SUBJECTS_DIR"] = work_dir
    os.environ["LD_LIBRARY_PATH"] = "/opt/ants/lib"

    join = os.path.join
    cmd = (
        "antsApplyTransforms -d 3 "
        f"-i {join(templates_dir,'Cerebellum-MNIsegment.nii.gz')} "
        f"-r {join(work_dir,'brain.nii.gz')} "
        "-n GenericLabel[Linear] "
        f"-t {join(mri_dir,'ants1Warp.nii.gz')} "
        f"-t {join(mri_dir,'ants0GenericAffine.mat')} "
        f"-o {join(mri_dir,'Cerebellum-MNIsegment_ind.nii.gz')} "
    )
    log.info("This is the cerebellum command:\n'%s'", cmd)
    sp.run(cmd, shell=True, check=False)

    # copy it to output dir
    log.info("Copy Cerebellum-MNIsegment_ind.nii.gz to work_dir")
    shutil.move(
        join(mri_dir, "Cerebellum-MNIsegment_ind.nii.gz"),
        join(work_dir, "Cerebellum-MNIsegment_ind.nii.gz"),
    )


def segment_hcp(work_dir: str, mri_dir: str, templates_dir: str) -> None:
    """Segments the cortex using MNI_Glasser_HCP_v1.0.nii.gz template.

    Arguments:
        work_dir (str): Flywheel's work directory.
        mri_dir (str): Freesurfer's work directory.
        templates_dir (str): Flywheel's templates directory.
    """
    log.info("Running segment_hcp. ")
    os.environ["LD_LIBRARY_PATH"] = "/opt/ants/lib"

    join = os.path.join
    cmd = (
        "antsApplyTransforms -d 3 "
        f"-i {join(templates_dir,'MNI_Glasser_HCP_v1.0.nii.gz')} "
        f"-r {join(work_dir,'brain.nii.gz')} "
        "-n GenericLabel[Linear] "
        f"-t {join(mri_dir,'ants1Warp.nii.gz')} "
        f"-t {join(mri_dir,'ants0GenericAffine.mat')} "
        f"-o {join(mri_dir,'Glasser_HCP_v1.0.nii.gz')} "
    )
    log.info("This is the hcp atlas command:\n'%s'", cmd)
    sp.run(cmd, shell=True, check=False)

    # copy it to output dir
    log.info("Copy Glasser_HCP_v1.0.nii.gz to work_dir")
    shutil.move(
        join(mri_dir, "Glasser_HCP_v1.0.nii.gz"),
        join(work_dir, "Glasser_HCP_v1.0.nii.gz"),
    )


def segment_mori(work_dir: str, mri_dir: str, mni_roi_dir: str, rois_dir: str) -> None:
    """Converts MNI ROIs to subject space.

    The MNI ROIs can be internall from the gear, or user provided with input mniroizip.

    Arguments:
        work_dir (str): Flywheel's work directory.
        mri_dir (str): Freesurfer's work directory.
        mni_roi_dir (str): Flywheel's mni_roi directory (source of mni rois).
        rois_dir (str): Flywheel's roi directory (destination of subject space rois).
    """
    log.info("Running segment_mori, converting from MNI space to individual ")
    os.environ["LD_LIBRARY_PATH"] = "/opt/ants/lib"
    join = os.path.join
    mori_rois = os.listdir(mni_roi_dir)
    for roi in mori_rois:
        if roi == "FSL_MNI152_FreeSurferConformed_1mm.nii.gz":
            continue
        cmd = (
            "antsApplyTransforms -d 3 "
            f"-i {join(mni_roi_dir,roi)} "
            f"-r {join(work_dir,'brain.nii.gz')} "
            "-n GenericLabel[Linear] "
            f"-t {join(mri_dir,'ants1Warp.nii.gz')} "
            f"-t {join(mri_dir,'ants0GenericAffine.mat')} "
            f"-o {join(mri_dir,f'MORI_{roi}')} "
        )
        log.info("This is the mori roi command:\n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)
        # Binarize the output
        cmd = (
            "mri_binarize --min 0.1 "
            f"--i {join(mri_dir, f'MORI_{roi}')} "
            f"--o {join(rois_dir, roi).replace('.nii.gz','_subj.nii.gz')} "
        )
        log.info("Command for binarizing the roi:\n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)

        os.remove(join(mri_dir, f"MORI_{roi}"))


def run_neuropythy(subject_id: str, work_dir: str) -> None:
    """Runs neuropythy and gives the benson and wang visual cortex atlases.

    The direct Python call is throwing an error and it does not finish.

    Arguments:
        subject_id (str): Freesurfer's subject id, usually Sxxx.
        work_dir (str): Flywheel's work directory.
    """
    log.info("Running run_neuropythy. ")

    join = os.path.join
    fsDir = join(work_dir, subject_id)

    # Specify the SUBJECTS_DIR name
    os.environ["SUBJECTS_DIR"] = work_dir

    # run neuropythy if not existing yet
    if not os.path.isfile(join(fsDir, "mri", "benson14_varea.mgz")):
        try:
            os.chdir(work_dir)
            cmd = f"python -m neuropythy atlas --verbose --volume-export {subject_id}"
            log.info("Command for launching Neuropythy:\n'%s'", cmd)
            sp.run(cmd, shell=True, check=False)
        except Exception as e:
            log.info("Neuropythy failed with following error:\n'%s'", e)
    else:
        log.info("Found and existing Neuropythy run, Neuropythy will not run")


def segment_hippocampus(
    gear_inputs: dict, subject_id: str, output_dir: str, mri_dir: str, work_dir: str
) -> None:
    """Segments the hippocampus using Freesurfer's tools.

    Arguments:
        gear_inputs (dict): all inputs to the gear.
        subject_id (str): Freesurfer's subject id, usually Sxxx.
        output_dir (str): Flywheel's work directory.
        mri_dir (str): Flywheel's work directory.
        work_dir (str): Flywheel's work directory.
    """
    log.info("Running segment_hippocampus. ")

    # Specify the SUBJECTS_DIR name
    os.environ["SUBJECTS_DIR"] = work_dir

    # run hippocampal segmentation if not existing yet
    if not os.path.isfile(join(mri_dir, "rh.hippoAmygLabels-T1.v22.CA.mgz")):
        os.environ["LD_LIBRARY_PATH"] = (
            "/opt/freesurfer/MCRv97/runtime/glnxa64:"
            "/opt/freesurfer/MCRv97/bin/glnxa64:"
            "/opt/freesurfer/MCRv97/sys/os/glnxa64:"
            "/opt/freesurfer/MCRv97/sys/java/jre/glnxa64/"
            "jre/lib/amd64/native_threads:"
            "/opt/freesurfer/MCRv97/sys/java/jre/glnxa64/"
            "jre/lib/amd64/server:/opt/freesurfer/MCRv97/"
            "sys/java/jre/glnxa64/jre/lib/amd64"
        )

        cmd = f"segmentHA_T1.sh {subject_id}"
        log.info("This is the hippocampal segmentation command:\n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)

        if gear_inputs["t2w_anatomical"]:
            cmd = f"segmentHA_T2.sh {subject_id} {join(mri_dir,'T2.mgz')} 0 1"
            log.info("This is the T2 hippocampal segmentation command:\n'%s'", cmd)
            sp.run(cmd, shell=True, check=False)

        # Extract csv values (not required for roi-s but it is good to have it)
        cmd = (
            "quantifyHAsubregions.sh hippoSf T1 "
            f"{join(mri_dir,'HippocampalSubfields.txt')} {work_dir} "
        )
        log.info("This is the hippocampal segmentation to csv command:\n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)

        cmd = (
            "quantifyHAsubregions.sh amygNuc T1 "
            f"{join(mri_dir,'AmygdalaNuclei.txt')} {work_dir} "
        )
        log.info("This is the amygdala segmentation to csv command:\n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)

        # Move the files to the output folder
        shutil.copyfile(
            join(mri_dir, "HippocampalSubfields.txt"),
            join(output_dir, f"{subject_id}_HippocampalSubfields.csv"),
        )
        shutil.copyfile(
            join(mri_dir, "AmygdalaNuclei.txt"),
            join(output_dir, f"{subject_id}_AmygdalaNuclei.csv"),
        )

        os.environ["LD_LIBRARY_PATH"] = ""


def segment_thalamus(
    subject_id: str, output_dir: str, mri_dir: str, work_dir: str
) -> None:
    """Segments thalamic nuclei using freesurfer's segmentThalamicNuclei script.

    Arguments:
        subject_id (str): Freesurfer's subject id, usually Sxxx.
        output_dir (str): Flywheel's work directory.
        mri_dir (str): Flywheel's work directory.
        work_dir (str): Flywheel's work directory.

    """
    log.info("Running segment_thalamus. ")

    # Specify the SUBJECTS_DIR name
    os.environ["SUBJECTS_DIR"] = work_dir

    # Check if this is infant, if so, modify aseg.mgz
    if not join(mri_dir, "aparc.a2009s+aseg.mgz"):
        log.info("InfantFS detected, running fix_aseg_if_infant.py")
        # aseg is different, change it, required for Thalamic Segmentation
        fix_aseg_if_infant(mri_dir)

        if not os.path.isdir(join(work_dir, subject_id, "scripts")):
            os.mkdir(join(work_dir, subject_id, "scripts"))

        if not os.path.isdir(join(work_dir, subject_id, "tmp")):
            os.mkdir(join(work_dir, subject_id, "tmp"))

    # If it has been done, do not repeat
    if not os.path.isfile(join(mri_dir, "ThalamicNuclei.v13.T1.FSvoxelSpace.mgz")):
        # Change the ld_library_path so that matlab mcr can work
        os.environ["LD_LIBRARY_PATH"] = (
            "/opt/freesurfer/MCRv97/runtime/glnxa64:"
            "/opt/freesurfer/MCRv97/bin/glnxa64:"
            "/opt/freesurfer/MCRv97/sys/os/glnxa64:"
            "/opt/freesurfer/MCRv97/sys/java/jre/glnxa64/"
            "jre/lib/amd64/native_threads:"
            "/opt/freesurfer/MCRv97/sys/java/jre/glnxa64/"
            "jre/lib/amd64/server:/opt/freesurfer/MCRv97/"
            "sys/java/jre/glnxa64/jre/lib/amd64"
        )

        # Run the thalamic nuclei segmentation
        cmd = f"segmentThalamicNuclei.sh {subject_id}"
        log.info("This is the thalamic segmentation command:\n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)

        # The segmentation had some problems because of loose voxels not attached to nuclei
        # With this tool we remove the fragmentation of the nuclei
        cmd = f"fixAllSegmentations {join(work_dir,subject_id)}"
        log.info("This is the thalamic segmentation fix FRAC command:\n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)

        # Create symbolic link and copy file
        shutil.copyfile(
            join(mri_dir, "ThalamicNuclei.v13.T1.fixed_FRAC_0.6.volumes.txt"),
            join(mri_dir, "ThalamicNuclei.T1.volumes.txt"),
        )
        shutil.copyfile(
            join(mri_dir, "ThalamicNuclei.T1.volumes.txt"),
            join(output_dir, f"{subject_id}_ThalamicNuclei.T1.volumes.csv"),
        )

    # Remove the ld library path back to normal just in case
    os.environ["LD_LIBRARY_PATH"] = ""


def segment_brainstem(
    subject_id: str, output_dir: str, mri_dir: str, work_dir: str
) -> None:
    """Segments brainstem  using freesurfer's scripts.

    Arguments:
        subject_id (str): Freesurfer's subject id, usually Sxxx.
        output_dir (str): Flywheel's work directory.
        mri_dir (str): Flywheel's work directory.
        work_dir (str): Flywheel's work directory.
    """
    log.info("Running segment_brainstem. ")

    # Specify the SUBJECTS_DIR name
    os.environ["SUBJECTS_DIR"] = work_dir

    join = os.path.join

    # If it has been done do not repeat
    if not os.path.isfile(join(mri_dir, "brainstemSsLabels.v13.mgz")):
        # Change the ld_library_path so that matlab mcr can work
        os.environ["LD_LIBRARY_PATH"] = (
            "/opt/freesurfer/MCRv97/runtime/glnxa64:"
            "/opt/freesurfer/MCRv97/bin/glnxa64:"
            "/opt/freesurfer/MCRv97/sys/os/glnxa64:"
            "/opt/freesurfer/MCRv97/sys/java/jre/glnxa64/"
            "jre/lib/amd64/native_threads:"
            "/opt/freesurfer/MCRv97/sys/java/jre/glnxa64/"
            "jre/lib/amd64/server:/opt/freesurfer/MCRv97/"
            "sys/java/jre/glnxa64/jre/lib/amd64"
        )

        # Run the thalamic nuclei segmentation
        cmd = f"segmentBS.sh {subject_id}"
        log.info("This is the thalamic segmentation command:\n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)

        # Extract csv values (not required for roi-s but it is good to have it)
        cmd = (
            "quantifyBrainstemStructures.sh "
            f"{join(mri_dir,'BrainstemStructures.txt')} "
        )
        log.info("This is the brainstem segmentation to csv command:\n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)

        shutil.copyfile(
            join(mri_dir, "BrainstemStructures.txt"),
            join(output_dir, f"{subject_id}_BrainstemStructures.csv"),
        )

        # Remove the ld library path back to normal just in case
        os.environ["LD_LIBRARY_PATH"] = ""


def separate_aparc2009_rois(
    mri_dir: str, fs_dir: str, rois_dir: str, work_dir: str
) -> None:
    """Segments brainstem  using freesurfer's scripts.

    Arguments:
        mri_dir (str): Flywheel's work directory.
        fs_dir (str): Freesurfer's home directory.
        rois_dir (str): Flywheel's subject space roi directory.
        work_dir (str): Flywheel's work directory.
    """
    log.info("Converting aparc2009 roi-s to volumetric. ")
    join = os.path.join

    # Specify the SUBJECTS_DIR name
    os.environ["SUBJECTS_DIR"] = work_dir

    mri_nii = join(mri_dir, "aparc.a2009s+aseg.nii.gz")
    mri_mgz = join(mri_dir, "aparc.a2009s+aseg.mgz")
    fs_nii = join(fs_dir, "aparc.a2009s+aseg.nii.gz")

    if not os.path.isfile(mri_nii):
        if os.path.isfile(mri_mgz):
            cmd = f"mri_convert -i {mri_mgz} -o {mri_nii} "
            sp.run(cmd, shell=True, check=False)

    shutil.copy2(mri_nii, fs_nii)
    sep.segAparc2009(fs_nii)

    # split Brain Stem to Left and Right
    cmd1 = (
        f"mri_convert -at {join(mri_dir,'transforms','talairach.xfm')} "
        f"-rt nearest {join(rois_dir,'Brain-Stem.nii.gz')} "
        f"{join(rois_dir,'tmp.nii.gz')}"
    )
    cmd2 = (
        f"3dcalc -a {join(rois_dir,'tmp.nii.gz')} "
        "-expr 'a*step(-2-x)' "
        f"-prefix {join(rois_dir,'Right-tmp.nii.gz')} "
        "-overwrite"
    )
    cmd3 = (
        f"3dcalc -a {join(rois_dir,'tmp.nii.gz')} "
        "-expr 'a*step(x-2)' "
        f"-prefix {join(rois_dir,'Left-tmp.nii.gz')}  "
        "-overwrite"
    )
    cmd4 = (
        "mri_convert "
        f"-ait {join(mri_dir,'transforms/talairach.xfm')}  "
        "-rt nearest "
        f"{join(rois_dir,'Right-tmp.nii.gz')}  "
        f"{join(rois_dir,'Right-Brain-Stem.nii.gz')} "
    )
    cmd5 = (
        f"mri_convert -ait {join(mri_dir,'transforms/talairach.xfm')}  "
        "-rt nearest "
        f"{join(rois_dir,'Left-tmp.nii.gz')}  "
        f"{join(rois_dir,'Left-Brain-Stem.nii.gz')} "
    )
    cmd6 = (
        f"rm {join(rois_dir,'tmp.nii.gz')} "
        f"{join(rois_dir,'Right-tmp.nii.gz')}  "
        f"{join(rois_dir,'Left-tmp.nii.gz')} "
    )

    # Run all now
    log.info("(1/6) aparc2009, running this cmd:\n'%s'", cmd1)
    sp.run(cmd1, shell=True, check=False)

    log.info("(2/6) aparc2009, running this cmd:\n'%s'", cmd2)
    sp.run(cmd2, shell=True, check=False)

    log.info("(3/6) aparc2009, running this cmd:\n'%s'", cmd3)
    sp.run(cmd3, shell=True, check=False)

    log.info("(4/6) aparc2009, running this cmd:\n'%s'", cmd4)
    sp.run(cmd4, shell=True, check=False)

    log.info("(5/6) aparc2009, running this cmd:\n'%s'", cmd5)
    sp.run(cmd5, shell=True, check=False)

    log.info("(6/6) aparc2009, running this cmd:\n'%s'", cmd6)
    sp.run(cmd6, shell=True, check=False)
