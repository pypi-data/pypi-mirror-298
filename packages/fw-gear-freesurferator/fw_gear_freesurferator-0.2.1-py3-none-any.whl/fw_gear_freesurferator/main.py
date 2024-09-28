"""Main module."""

import glob
import gzip
import logging
import os
import shutil
import subprocess as sp
import sys
import time
import zipfile

import nibabel as nb
import numpy as np

import fw_gear_freesurferator.segmentations as seg
import fw_gear_freesurferator.separateROIs as sep
from fw_gear_freesurferator.utils import create_zipinfo

log = logging.getLogger(__name__)

join = os.path.join


def run_freesurfer(gear_inputs: dict, gear_config: dict, re_run: bool) -> None:
    """Runs Freesurfer's recon-all.

    Depending if it is a run or a re-run, it will adapt the recon-all call.

    Arguments:
        gear_inputs (dict):  all inputs.
        gear_config (dict): all configs.
        re_run (bool): indicates if a previous run exists and if it is a re-run.
    """
    log.info("Now running recon-all")

    # Additionnal T1w files
    if re_run:
        ADD_INPUT = ""
    else:
        ADD_INPUT = f"-i {gear_inputs['anat']} "
        if gear_inputs["t1w_anatomical_2"]:
            ADD_INPUT = f"-i {gear_inputs['t1w_anatomical_2']} "
        if gear_inputs["t1w_anatomical_3"]:
            ADD_INPUT = f"-i {gear_inputs['t1w_anatomical_3']} "
        if gear_inputs["t1w_anatomical_4"]:
            ADD_INPUT = f"-i {gear_inputs['t1w_anatomical_4']} "
        if gear_inputs["t1w_anatomical_5"]:
            ADD_INPUT = f"-i {gear_inputs['t1w_anatomical_5']} "
        # T2w file
        if gear_inputs["t2w_anatomical"]:
            ADD_INPUT = f"{ADD_INPUT} -T2 {gear_inputs['t2w_anatomical']} -T2pial "

    # Run Freesurfer-Recon-all
    cmd = (
        "recon-all "
        f"{ADD_INPUT} "
        f"-subjid {gear_config['subject_id']} "
        f"{gear_config['reconall_options']}"
    )
    log.info("This is the recon-all command: \n'%s'", cmd)
    sp.run(cmd, shell=True, check=False)


def extract_freesurfer(gear_inputs: dict, gear_config: dict) -> None:
    """Extract the zip with a run of Freesurfer recon-all.

    It takes an existing zipped recon-all run and extracts it.

    Arguments:
        gear_inputs (dict): all inputs.
        gear_config (dict): all configs.
    """
    log.info("Extracting existing recon-all zip")

    # (check this note) We are not running FS, we need to find a zip file or a folder
    # with a previous run
    # If it is a zip file just search any zip file in the folder and unzip it.
    # If it is a folder, it will be a symbolic link to a FS folder, we are not going to copy anything.
    # Be careful with the file writing, as it will write in the FS folders. Then we copy to the output
    #   the files we are interested to the output and the rest will be zipped.

    with zipfile.ZipFile(gear_inputs["pre_fs"], "r") as zip_ref:
        zip_ref.extractall(gear_inputs["work_dir"])

        # Obtain subject name from zip's first folder
        (relativepath,) = zipfile.Path(zip_ref).iterdir()
        subject_id = relativepath.name

    # Check that the subject_id is the same
    if gear_config["subject_id"] == subject_id:
        log.info(
            "Both subject_id coming from the config and the extracted "
            " zip file coincide, subject_id: %s",
            subject_id,
        )

    else:
        log.info(
            "gear_config['subject_id']: %s is not the same as the subject name "
            "extracted from the zip file, which is %s",
            gear_config["subject_id"],
            subject_id,
        )

        sys.exit(1)


def run_ants_registration(mri_dir: str, mori_dir: str, MNI_template: str) -> None:
    """Runs ANTs registration with anatomical and MNI template.

    It takes an existing zipped recon-all run and extracts it.

    Arguments:
        mri_dir (str): Freesurfer's mri directory.
        mori_dir (str): Directory with the template and MNI ROIs.
        MNI_template (str): name of the MNI template.
    """
    # Create binary mask of brain.mgz (or brainmask.mgz) and MNI_152.
    # This will always be and should be brain.mgz, but just in case the
    # gear is run on old version results, "brainmask" is being maintained.
    # There should be no risk just using brain.mgz for all new runs.
    masked_file = join(mri_dir, "brain.mgz")
    if not os.path.isfile(masked_file):
        masked_file = join(mri_dir, "brainmask.mgz")

    cmd = f"mri_convert {masked_file} {join(mri_dir,'brain.nii.gz')}"
    log.info(
        "Creating binary mask of %s with command:\n'%s'",
        os.path.basename(masked_file),
        cmd,
    )
    sp.run(cmd, shell=True, check=False)

    # Calculate the transformation
    cmd = (
        "antsRegistrationSyN.sh -d 3 "
        f"-o {join(mri_dir,'ants')} "
        f"-f {join(mri_dir,'brain.nii.gz')} "
        f"-m {join(mori_dir, MNI_template)} "
    )
    log.info("This is the ANTs command:\n'%s'", cmd)
    sp.run(cmd, shell=True, check=False)


def convert_files_to_nifti(
    mri_mgz_file_list: list, mri_dir: str, fs_dir: str, work_dir: str
) -> None:
    """Convert a list of mgz files to niftis.

    Converts files from Freesurfer's mgz format to NIfTI.

    Arguments:
        mri_mgz_file_list (list): mgz file list to be converted.
        mri_dir (str): Freesurfer's mri directory.
        fs_dir (str): Freesurfer's base directory.
        work_dir (str): Flywheel's work directory
    """
    log.info("Converting volumes to NIfTI files...")

    for mgz in mri_mgz_file_list:
        cmd1 = (
            "mri_convert "
            f"-i {join(mri_dir, mgz)} "
            f"-o {join(work_dir, mgz.replace('mgz','nii.gz'))}"
        )
        cmd2 = (
            "mri_convert "
            f"-i {join(mri_dir, mgz)} "
            f"-o {join(fs_dir, mgz.replace('mgz','nii.gz'))}"
        )
        if not os.path.isfile(join(work_dir, mgz.replace("mgz", "nii.gz"))):
            log.info("Conversion command:\n'%s'", cmd1)
            sp.run(cmd1, shell=True, check=False)
        else:
            log.info(
                "Not converting to nifti, it already exists.\n'%s': ",
                join(mri_dir, mgz.replace("mgz", "nii.gz")),
            )

        if not os.path.isfile(join(fs_dir, mgz.replace("mgz", "nii.gz"))):
            log.info("Conversion command:\n'%s'", cmd2)
            sp.run(cmd2, shell=True, check=False)
        else:
            log.info(
                "Not converting to nifti, it already exists.\nFilename: %s",
                join(fs_dir, mgz.replace("mgz", "nii.gz")),
            )


def create_rois_from_annot(
    annotfile: str, subject_id: str, work_dir: str, mri_dir: str, rois_dir: str
) -> None:
    """Create cortical volumetric ROIs in the subject space from annot(s).

    If a zip file with one or more annots files is passed (the annot files
    need to be in fsaverage space), this function will extract the annots,
    the individual labels, and it will provide cortical volumetric ROIs in
    the subject space.

    annotfile (str): name of zip file with annotations.
    subject_id (str): Freesurfer's subject ID, usually generic Sxxx.
    work_dir (str): Flywheel's work directory
    mri_dir (str): Freesurfer's mri directory
    rois_dir (str): freesurferators roi directory
    """
    # Create folder
    annot_dir = join(work_dir, "annotations")
    if not os.path.isdir(annot_dir):
        os.mkdir(annot_dir)

    # Unzip
    with zipfile.ZipFile(annotfile, "r") as zip_ref:
        zip_ref.extractall(annot_dir)

    # Labeldir in the subject
    labeldir = join(work_dir, subject_id, "label")
    labeldirtmp = join(work_dir, subject_id, "label", "tmp")
    if not os.path.isdir(labeldirtmp):
        os.mkdir(labeldirtmp)

    # Specify the SUBJECTS_DIR name
    os.environ["SUBJECTS_DIR"] = work_dir

    # Convert the annot from fsaverage to the individual subject space
    for annot in os.listdir(annot_dir):
        # Obtain hemi
        hemi = annot[0:2]

        # Launch the first command to convert to individual subject space
        cmd = (
            "mri_surf2surf "
            "--srcsubject fsaverage "
            f"--trgsubject {subject_id} "
            f"--hemi {hemi} "
            f"--sval-annot {join(annot_dir, annot)} "
            f"--tval {join(labeldir, annot)}"
        )
        log.info("mri_surf2surf command:\n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)

        # Extract the individual labels
        cmd = (
            "mri_annotation2label "
            f"--subject {subject_id} "
            f"--hemi {hemi} "
            f"--annotation {join(labeldir, annot)} "
            f"--outdir {labeldirtmp}"
        )
        log.info("mri_annotation2label command:\n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)

        # Convert from label to volumetric label
        # (add this to fill GM, otherwise just pial voxels -proj frac 0 1 0.01)
        for label in os.listdir(labeldirtmp):
            cmd = (
                "mri_label2vol "
                f"--subject {subject_id} "
                f"--hemi {hemi} --identity "
                f"--label {join(labeldirtmp, label)} "
                f"--temp {join(mri_dir, 'T1.mgz')} "
                f"--o {join(rois_dir,label.replace('label','nii.gz'))}"
            )
            log.info("mri_label2vol command:\n'%s'", cmd)
            sp.run(cmd, shell=True, check=False)

            # Move the label file to the label dir to store
            shutil.move(join(labeldirtmp, label), join(labeldir, label))
            # Do this to fill the holes and make it fit exactly
            # inside the boundaries of GM (we control dilation later to be dMRI WM ROIs)
            cmd = (
                "mri_binarize "
                "--dilate 1 --erode 1 "
                f"--i {join(rois_dir,label)} "
                f"--o {join(rois_dir,label.replace('label', 'nii.gz'))} "
                f"--min 1"
            )
            log.info("mri_binarize command:\n'%s'", cmd)
            sp.run(cmd, shell=True, check=False)

            cmd = (
                "mris_calc "
                f"-o {join(rois_dir,label.replace('label','nii.gz'))} "
                f"{join(rois_dir, label.replace('label','nii.gz'))} "
                f"mul {join(mri_dir, f'{hemi}.ribbon.mgz')}"
            )
            log.info("mris_calc command:\n'%s'", cmd)
            sp.run(cmd, shell=True, check=False)


def check_archive_for_bad_filename(file: str) -> bool:
    """Checks a zip file contains bad filenames.

    Specifically, we are just checking if the zip was created with macos.

    Arguments:
        file (str): path to the zip to be checked.

    Returns:
        Boolean, True if bad filenames are encountered
    """
    with zipfile.ZipFile(file, "r") as zip_file:
        for filename in zip_file.namelist():
            if filename.startswith("__MACOSX/"):
                return True


def remove_bad_filename_from_archive(original_file: str, temporary_file: str) -> None:
    """Remove MACOS-specific auto-generated metadata files from the given ZIP.

    Specifically, we are removing macos created zipfiles, for MACOSX and
    DS_Store folders/files.

    Arguments:
        original_file (str): path to the zip to be cleaned.
        temporary_file (str): path to a cleaned temporary zip file.
    """
    with (
        zipfile.ZipFile(original_file, "r") as source,
        zipfile.ZipFile(temporary_file, "w") as destination,
    ):
        for item in source.namelist():
            if not (item.startswith("__MACOSX/") or item.endswith("DS_Store")) and (
                item.endswith("nii.gz") or item.endswith("nii")
            ):
                destination.writestr(item, source.read(item))


def extract_mniroizip_valid(  # noqa: PLR0911 PLR0912 PLR0915
    mniroizip: str, work_mni_dir: str, MNI_template_path: str
) -> bool:
    """Ensure that the mniroizip input is valid and extract it if so.

    We only accept a zip file with nifti ROIs, or a single nifti file or a single
    zipped nifti file. This function will check that the input is correct. If it's
    not, then the seg.segment_mori() function will not run and the user will
    get an explanation of why it did not run, but the rest of the functions will run.

    Arguments:
        mniroizip (str): path to the input file
        work_mni_dir (str): path to working directory for mni rois.
        MNI_template_path (str): path to the templates directory

    Returns:
        Boolean: True if a valid mniroizip exists and is extracted succesfully
    """
    # Check if it has valid extension
    valid_extensions = [".zip", ".gz", ".nii"]
    file_extension = os.path.splitext(mniroizip)[1]
    if file_extension in valid_extensions:
        log.info("mniroizip is a file with extension %s", file_extension)
    else:
        log.info("mniroizip is a file with a non valid extension %s\n", file_extension)
        log.info("Valid options are:\n'%s'", valid_extensions)
        return False

    # For later: check right dimensions on ROIs, otherwise throw message and ignore ROI
    template_dim = nb.load(MNI_template_path).header["dim"]

    if not os.path.isdir(work_mni_dir):
        os.mkdir(work_mni_dir)

    # Check if it is a valid zip file
    if file_extension == ".zip":
        if not zipfile.is_zipfile(mniroizip):
            log.info(
                "%s exists but it is not a valid zipfile. "
                "The MNI ROIs will NOT be converted.",
                mniroizip,
            )
            return False

        # We have a valid zipfile:
        log.info(
            "%s exists and it is a zipfile. "
            "The MNI ROIs will be converted to individual subject space.",
            mniroizip,
        )

        # Check if it has macosx compress files
        temp_filename = join(work_mni_dir, "nomacosx.zip")
        mac_result = check_archive_for_bad_filename(mniroizip)
        if mac_result:
            log.info("Removing MACOSX file from archive.")
            remove_bad_filename_from_archive(mniroizip, temp_filename)
            mniroizip = temp_filename
        log.info(
            "Unzipping mniroizip file and removing all folder information, keeping just files."
        )
        with zipfile.ZipFile(mniroizip) as zip_ref:
            for member in zip_ref.namelist():
                filename = os.path.basename(member)
                # skip directories
                if not filename:
                    continue
                # copy file (taken from zipfile's extract)
                with (
                    zip_ref.open(member) as source,
                    open(join(work_mni_dir, filename), "wb") as target,
                ):
                    shutil.copyfileobj(source, target)

                # At the level of each item, revise if it is a nifti or
                # the dims are correct, otherwise remove
                if "nifti" not in str(type(nb.load(join(work_mni_dir, filename)))):
                    log.info(
                        "%s exists but it is not a valid nifti file. "
                        "The MNI ROIs will NOT be converted.",
                        filename,
                    )
                    os.remove(join(work_mni_dir, filename))
                    continue
                roi_dim = nb.load(join(work_mni_dir, filename)).header["dim"]
                if not np.array_equal(template_dim, roi_dim):
                    log.info(
                        "The Template file and the ROI are not in the same "
                        "space, at least the dim field is not the same, try to "
                        "regrid it with mrtransform or equivalent. Remove %s",
                        filename,
                    )
                    os.remove(join(work_mni_dir, filename))
                # If a nii is passed, compress it
                if filename.endswith(".nii"):
                    log.info("Compressing file '%s'", filename)
                    with (
                        open(join(work_mni_dir, filename), "rb") as f_in,
                        gzip.open(join(work_mni_dir, filename + ".gz"), "wb") as f_out,
                    ):
                        shutil.copyfileobj(f_in, f_out)
        if mac_result:
            os.remove(temp_filename)
        # Check if there is at least one valid nifti roi in mori_dir
        if len(glob.glob(join(work_mni_dir, "*.nii.gz"))) == 0:
            log.info("After the checks,  no valid ROIs where passed on the zip")
            return False
        return True

    if file_extension in (".gz", ".nii"):
        if "nifti" not in str(type(nb.load(mniroizip))):
            log.info(
                "%s exists but it is not a valid nifti file. "
                "The MNI ROIs will NOT be converted.",
                mniroizip,
            )
            return False

        log.info(
            "%s exists and it will be checked and copied to the right location.",
            mniroizip,
        )
        log.info(
            "First check if the dimension of the file is the same as to the template"
        )

        roi_dim = nb.load(mniroizip).header["dim"]
        if not np.array_equal(template_dim, roi_dim):
            log.info(
                "The Template file and the ROI are not in the same space, at least "
                "the dim field is not the same, try to regrid it with mrtransform or "
                "equivalent."
            )
            return False

        if file_extension == ".gz":
            shutil.copy(mniroizip, join(work_mni_dir, os.path.basename(mniroizip)))
            return True

        if file_extension == ".nii":
            cmd = (
                f"mri_convert {mniroizip} "
                f"{join(work_mni_dir, os.path.basename(mniroizip)+'.gz')}"
            )
            log.info("Cpompressing file with command:\n'%s'", cmd)
            sp.run(cmd, shell=True, check=False)
            return True


def run(gear_inputs: dict, gear_config: dict) -> int:  # noqa PLR0912 PLR0915
    """Run Freesurfer (or use FS output zip) and create 3D ROIs via atlases and more.

    The container will have the option to include a folder or a zip file with
    FS run already. If there is no zip, there should be the anatomical file
    and it will run the whole FS. If both are present, it will use the zip.

    Arguments:
        gear_inputs (dict): all inputs.
        gear_config (dict): all configs.
    """
    log.info("This is the beginning of the run file")

    # Path and variable definition
    output_dir = str(gear_inputs["output_dir"])
    work_dir = str(gear_inputs["work_dir"])
    mri_dir = join(work_dir, gear_config["subject_id"], "mri")
    templates_dir = join(os.environ["FLYWHEEL"], "templates")
    mori_dir = join(templates_dir, "MNI_JHU_tracts_ROIs")
    MNI_template = "FSL_MNI152_FreeSurferConformed_1mm.nii.gz"
    MNI_template_path = join(mori_dir, MNI_template)
    fs_dir = join(work_dir, "fs")
    if not os.path.isdir(fs_dir):
        os.mkdir(fs_dir)
    rois_dir = join(fs_dir, "ROIs")
    if not os.path.isdir(rois_dir):
        os.mkdir(rois_dir)
    subject_id = gear_config["subject_id"]
    annotfile = gear_inputs["annotfile"]
    mniroizip = gear_inputs["mniroizip"]
    if mniroizip:
        work_mni_dir = join(work_dir, "mni")

    # Obtain FREESURFER_HOME directory
    fshome = join(os.environ["FREESURFER_HOME"])

    # Specify the SUBJECTS_DIR name
    os.environ["SUBJECTS_DIR"] = work_dir

    # Several programs downstream need to have fsaverage,
    # do it for all here and at the end unlink/delete it
    # Create symbolink link to fsaverage to the output folder
    fsaveragelink = join(work_dir, "fsaverage")
    # Check if the symbolic link exists, if so, unlink it
    if os.path.islink(fsaveragelink):
        log.info("Unlinking existing link to fsaverage")
        os.path.unlink(fsaveragelink)

    if not os.path.isdir(fsaveragelink):
        log.info("Copying fsaverage to work_dir. It will be removed at the end.")
        shutil.copytree(join(fshome, "subjects", "fsaverage"), fsaveragelink)

    # Check wich one of the two inputs have been provided.
    # If both the T1w and the fs_zip have been provided, use the existing fs_zip
    # The T1w (anat) is mandatory, so it is not possible that none is passed

    if gear_inputs["pre_fs"]:
        if zipfile.is_zipfile(gear_inputs["pre_fs"]):
            log.info(
                "Both %s and %s exist, we will use the pre-run FS by default.",
                gear_inputs["anat"],
                gear_inputs["pre_fs"],
            )
            extract_freesurfer(gear_inputs, gear_config)
            # If control points were passed, copy them in place and run freesurfer
            if gear_inputs["control_points"]:
                log.info(
                    "Control points were passed to the gear, the control.dat file "
                    "will be copied to the tmp/ folder and freesurfer will run "
                    "again with the options '%s' that were passed in the config "
                    "field 'reconall_options'.",
                    gear_config["reconall_options"],
                )
                src = gear_inputs["control_points"]
                dst = join(work_dir, gear_config["subject_id"], "tmp", "control.dat")
                if os.path.isfile(dst):
                    log.info(
                        "tmp/control.dat exists in the pre_fs archive. "
                        "The old control.dat is going to be deleted and "
                        "substituted with the new one you passed in this run.",
                    )
                    os.remove(dst)
                shutil.copy(src, dst)
                re_run = True
                run_freesurfer(gear_inputs, gear_config, re_run)
        else:
            log.debug("%s is not a zip file. Aborting", gear_inputs["pre_fs"])
            sys.exit(0)
    else:
        log.info(
            "Only %s exists. Freesurfer recon-all will be run. This might take "
            "several hours",
            gear_inputs["anat"],
        )
        re_run = False
        run_freesurfer(gear_inputs, gear_config, re_run)

    # Convert stats files to csv and copy to the output
    # Write aseg stats to a table
    log.info("  Exporting stats files csv...")
    cmd = (
        f"asegstats2table -s {subject_id} "
        "--delimiter comma "
        f"--tablefile={join(work_dir,subject_id+'_aseg_stats_vol_mm3.csv')} "
    )
    log.info("asegstats2table command:\n'%s'", cmd)
    sp.run(cmd, shell=True, check=False)

    # Parse the aparc files and write to table
    hemis = ["lh", "rh"]
    parcs = ["aparc.a2009s", "aparc"]
    for h in hemis:
        for p in parcs:
            fname = f"{subject_id}_{h}_{p}_stats_area_mm2.csv"
            cmd = (
                f"aparcstats2table -s {subject_id} "
                f"--hemi={h} "
                "--delimiter=comma "
                f"--parc={p} "
                f"--tablefile={join(work_dir, fname)} "
            )
            log.info("asegstats2table command:\n'%s'", cmd)
            sp.run(cmd, shell=True, check=False)

    # There are many templates already coming from the gear. They will stay in the
    # gear's templates directory. If new MNI ROIs are passed, they will go to the work
    # dir and convert them there. Same with the annot ones. Regarding MNI ones these
    # the options
    # These are the options with the Mori type ROIs (in MNI space)
    # 1. config option mni_rois=true, input mniroizip exists:
    #    it merges the mni rois in the input with the existing ones in the gear
    #    and converts them all
    # 2. config option mni_rois=true, input mniroizip does not exist:
    #    it just converts the mni rois in the gear existing in the templates
    #    folder
    # 3. config option mni_rois=false, input mniroizip exists:
    #    it will ignore the mni-rois existing in the gear's templates folder,
    #    and converts the mni rois in the input
    # 4. config option mni_rois=false, input mniroizip does not exist:
    #    there will be no mni rois in the output of the gear.
    mniroizip_valid = False
    if mniroizip:
        mniroizip_valid = extract_mniroizip_valid(
            mniroizip, work_mni_dir, MNI_template_path
        )

    # CHECK ANTs
    # First check if ANTs has been run already or not, and if not, check if it
    # needs to be run, the objective is not run it at all or run it once
    if (
        gear_config["cerebellum"]
        or gear_config["mni_rois"]
        or gear_config["hcp"]
        or gear_config["force_ants"]
        or mniroizip_valid
    ):
        # This checks if ANTs has been run
        if not os.path.isfile(join(mri_dir, "ants1Warp.nii.gz")):
            run_ants_registration(mri_dir, mori_dir, MNI_template)

    # Create a list of all files that will be converted to nifti at the end.
    # Depending on the segmentations we will do (see below),
    # the list will be longer or shorter.
    # If InfantFS was used, the list will be different as well:
    mri_mgz_file_list = [
        "aparc+aseg.mgz",
        "brainmask.mgz",
        "brain.mgz",
        "lh.ribbon.mgz",
        "rh.ribbon.mgz",
        "ribbon.mgz",
        "aseg.mgz",
    ]
    if os.path.isfile(join(mri_dir, "aparc.a2009s+aseg.mgz")):
        mri_mgz_file_list = mri_mgz_file_list + [
            "aparc.a2009s+aseg.mgz",
            "orig.mgz",
            "T1.mgz",
        ]
    if os.path.isfile(join(work_dir, "aparc+aseg.nii.gz")):
        shutil.copy(
            join(work_dir, "aparc+aseg.nii.gz"), join(fs_dir, "aparc+aseg.nii.gz")
        )

    # Convert the mgz files to nifti
    convert_files_to_nifti(mri_mgz_file_list, mri_dir, fs_dir, work_dir)

    # OPTIONAL SEGMENTATIONS
    # Run the actual segmentations and add the corresponding files to conversion list
    if gear_config["run_gtmseg"]:
        seg.run_gtmseg(subject_id, work_dir)
        convert_files_to_nifti(["gtmseg.mgz"], mri_dir, fs_dir, work_dir)

    if gear_config["cerebellum"]:
        seg.segment_cerebellum(work_dir, mri_dir, templates_dir)

        # Write ROIs separately into individual files
        sep.sep_cb(join(work_dir, "Cerebellum-MNIsegment_ind.nii.gz"), fs_dir)

    if gear_config["hcp"]:
        seg.segment_hcp(work_dir, mri_dir, templates_dir)
        # Write ROIs separately into individual files
        # separate ROIs
        sep.sep_hcp(work_dir, fs_dir, templates_dir, rois_dir)

    if gear_config["mni_rois"]:
        seg.segment_mori(work_dir, mri_dir, mori_dir, rois_dir)

    if mniroizip_valid:
        seg.segment_mori(work_dir, mri_dir, work_mni_dir, rois_dir)

    if gear_config["neuropythy_analysis"]:
        seg.run_neuropythy(subject_id, work_dir)
        convert_files_to_nifti(
            [
                "wang15_mplbl.mgz",
                "benson14_varea.mgz",
                "benson14_eccen.mgz",
                "benson14_sigma.mgz",
                "benson14_angle.mgz",
            ],
            mri_dir,
            fs_dir,
            work_dir,
        )

        # Write ROIs separately into individual files: BENSON
        sep.sep_neuropythy(join(fs_dir, "benson14_varea.nii.gz"))
        # Write ROIs separately into individual files: WANG
        sep.sep_neuropythy(join(fs_dir, "wang15_mplbl.nii.gz"))

    if gear_config["hippocampal_subfields"]:
        seg.segment_hippocampus(gear_inputs, subject_id, output_dir, mri_dir, work_dir)
        # Copied from old script, make it Python...
        lfname = "lh.hippoAmygLabels-T1.FSvoxelSpace.mgz"
        rfname = "rh.hippoAmygLabels-T1.FSvoxelSpace.mgz"
        cmd1 = (
            "ln -sfn `ls "
            f"{join(mri_dir,'lh.hippoAmygLabels-T1.*.FSvoxelSpace.mgz')} "
            "| egrep 'T1.v[0-9]+.FSvox'` "
            f"{join(mri_dir,lfname)}"
        )
        cmd2 = (
            "ln -sfn `ls "
            f"{join(mri_dir,'rh.hippoAmygLabels-T1.*.FSvoxelSpace.mgz')} "
            "| egrep 'T1.v[0-9]+.FSvox'` "
            f"{join(mri_dir, rfname)}"
        )
        log.info("Creating links with command:\n'%s'", cmd1)
        sp.run(cmd1, shell=True, check=False)
        log.info("Creating links with command:\n'%s'", cmd2)
        sp.run(cmd2, shell=True, check=False)
        # Add to the conversion list
        convert_files_to_nifti([lfname, rfname], mri_dir, fs_dir, work_dir)
        # Write ROIs separately into individual files
        sep.sep_hippo(fs_dir)

    if gear_config["thalamic_nuclei"]:
        seg.segment_thalamus(subject_id, output_dir, mri_dir, work_dir)
        # Copied from old script, make it Python...
        cmd = (
            "ln -sfn "
            f"{join(mri_dir,'ThalamicNuclei.v13.T1.FSvoxelSpace.mgz')} "
            f"{join(mri_dir, 'ThalamicNuclei.T1.FSvoxelSpace.mgz')}"
        )
        log.info("Creating links with command:\n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)
        # Convert to nifti
        convert_files_to_nifti(
            ["ThalamicNuclei.T1.FSvoxelSpace.mgz"],
            mri_dir,
            fs_dir,
            work_dir,
        )

        # Write ROIs separately into individual files
        tname = "ThalamicNuclei.v13.T1.FSvoxelSpace.fixed_FRAC_0.6.nii.gz"
        shutil.copy(join(mri_dir, tname), join(work_dir, tname))
        shutil.copy(join(mri_dir, tname), join(fs_dir, tname))
        ThLUT = join(templates_dir, "FreesurferColorLUT_THALAMUS.txt")
        sep.sep_thalamus(join(fs_dir, tname), ThLUT)

        # Export csv files
        hemis = ["lh", "rh"]
        for h in hemis:
            cmd = (
                "asegstats2table "
                f"-s {subject_id} "
                "--delimiter=comma "
                f"--statsfile=thalamic-nuclei.{h}.v13.T1.stats "
                f"--tablefile={join(work_dir,f'{subject_id}_thalamic-nuclei.{h}.v13.T1.csv')} "
            )
            log.info("Obtain thalamic stats:\n'%s'", cmd)
            sp.run(cmd, shell=True, check=False)

    if gear_config["brainstem_structures"]:
        seg.segment_brainstem(subject_id, output_dir, mri_dir, work_dir)

        # Copied from old script, make it Python...
        cmd = (
            "ln -sfn "
            f"{join(mri_dir,'brainstemSsLabels.*.FSvoxelSpace.mgz')} "
            f"{join(mri_dir, 'brainstemSsLabels.FSvoxelSpace.mgz')}"
        )
        log.info("Creating links with command:\n'%s'", cmd)
        sp.run(cmd, shell=True, check=False)
        # Convert to nifti
        convert_files_to_nifti(
            ["brainstemSsLabels.FSvoxelSpace.mgz"],
            mri_dir,
            fs_dir,
            work_dir,
        )
        # Write ROIs separately into individual files
        sep.sep_brainstem(join(fs_dir, "brainstemSsLabels.FSvoxelSpace.nii.gz"))

    if gear_config["aparc2009"]:
        # Write ROIs separately into individual files
        seg.separate_aparc2009_rois(mri_dir, fs_dir, rois_dir, work_dir)

    # CREATE ROIS FROM ANNOT SURFACE FILE
    # If annotations have been provided, convert to individual space
    # annot and volume labels
    if annotfile:
        if zipfile.is_zipfile(annotfile):
            log.info(
                "%s exists. It will create individual ROIs out of it. ",
                annotfile,
            )
            create_rois_from_annot(annotfile, subject_id, work_dir, mri_dir, rois_dir)

    # CLEANING, COPYING, PERMISSIONS
    # Change permissions before zipping
    log.info("Changing permissions before zipping")
    sp.run(f"chmod -R 777 {work_dir}", shell=True, check=False)

    # We want some files in the output directory outside of zips because they are useful
    files_from_work_to_output = [
        "T1.nii.gz",
        "aparc+aseg.nii.gz",
        "aparc.a2009s+aseg.nii.gz",
        "aseg.nii.gz",
        "brainmask.nii.gz",
        "brain.nii.gz",
    ]
    for f in files_from_work_to_output:
        f_path = join(work_dir, f)
        if os.path.isfile(f_path):
            shutil.copy(f_path, output_dir)

    # Compress Recon-all to output directory
    log.info("Archiving back Freesurfer's output")
    date_time = time.strftime("%Y%m%d-%H%M%S")
    output_filename = join(output_dir, f"freesurferator_{subject_id}_{date_time}")
    shutil.make_archive(output_filename, "zip", join(work_dir), subject_id)
    # Delete the whole Freesurfer subject's folder
    log.info("Removing subject's folder")
    if os.path.isdir(join(work_dir, subject_id)):
        shutil.rmtree(join(work_dir, subject_id))

    # Remove the fsaverage folder created at the beginning
    log.info("Removing fsaverage folder")
    if os.path.isdir(fsaveragelink):
        shutil.rmtree(fsaveragelink)

    # Remove the mcr_cache_dir folder
    log.info("Removing MCR_CACHE_DIR folder")
    if os.path.isdir(os.environ["MCR_CACHE_DIR"]):
        shutil.rmtree(os.environ["MCR_CACHE_DIR"])

    log.info("Archive and delete the fs/ folder, creates fs.zip in the output")
    output_filename = join(output_dir, "fs")
    shutil.make_archive(output_filename, "zip", join(work_dir), "fs")
    # Before deleting the fs folder, see if ROIs need to be copied to output
    if gear_config["rois_in_output"]:
        for f in glob.glob(join(work_dir, "fs", "ROIs", "*.nii.gz")):
            shutil.copy(f, output_dir)
    # Delete the fs folder
    log.info("Removing fs/ folder")
    shutil.rmtree(join(work_dir, "fs"))

    # Delete the work/ dir entirely before exit.
    # With this step some of the old manual deletes will not be necessary
    # Leave it for now, if there is any problem it wil be easier to spot
    log.info("Removing everything left in work/ folder")
    for work_dir_item in os.listdir(work_dir):
        work_dir_item_path = join(work_dir, work_dir_item)
        if os.path.isdir(work_dir_item_path):
            shutil.rmtree(work_dir_item_path)
        else:
            os.remove(work_dir_item_path)

    # Create a zipinfo.csv file per each zip file in the output.
    zip_files_in_output = glob.glob(join(output_dir, "*.zip"))
    if len(zip_files_in_output) > 0:
        log.info("There are zip files in the output, creating zipinfo.csv per file")
        for f in zip_files_in_output:
            create_zipinfo(output_dir, f)

    return 0
