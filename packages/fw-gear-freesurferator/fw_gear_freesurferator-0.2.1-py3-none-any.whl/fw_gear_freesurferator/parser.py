"""Parser module to parse gear config.json."""

import os
from typing import Tuple

from flywheel_gear_toolkit import GearToolkitContext

from fw_gear_freesurferator.utils import die


# This function mainly parses gear_context's config.json file and returns relevant
# inputs and options.
def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[str, str]:
    """Inputs and config options parser.

    Parses gear_context's config.json file and returns relevant inputs and options.

    Arguments:
        gear_context (GearToolkitContext): gear context.

    Returns:
        tuple: dictionaries with inputs and configs
    """
    # Check that, if passed, control_points file has the right name
    # If not the right name, the gear will be stopped right here, as if the user
    # thinks that it is needed to add control points, there is no point
    # going further. The gear will inform the user about the issue so that it can be fixed.
    if gear_context.get_input_path("control_points"):
        controldat = os.path.basename(gear_context.get_input_path("control_points"))
        if controldat != "control.dat":
            die(
                "You introduced a file called %s in the control_ppints input file. ",
                "Only files called control.dat copied from Freesurfer's tmp/ directory ",
                "and created with Freeview are valid.",
                controldat,
            )

    # Gear inputs
    gear_inputs = {
        "anat": gear_context.get_input_path("anat"),
        "pre_fs": gear_context.get_input_path("pre_fs"),
        "control_points": gear_context.get_input_path("control_points"),
        "freesurfer_license_file": gear_context.get_input_path(
            "freesurfer_license_file"
        ),
        "mniroizip": gear_context.get_input_path("mniroizip"),
        "annotfile": gear_context.get_input_path("annotfile"),
        "t1w_anatomical_2": gear_context.get_input_path("t1w_anatomical_2"),
        "t1w_anatomical_3": gear_context.get_input_path("t1w_anatomical_3"),
        "t1w_anatomical_4": gear_context.get_input_path("t1w_anatomical_4"),
        "t1w_anatomical_5": gear_context.get_input_path("t1w_anatomical_5"),
        "t2w_anatomical": gear_context.get_input_path("t2w_anatomical"),
        "output_dir": gear_context.output_dir,
        "work_dir": gear_context.work_dir,
    }

    # Gear configs
    gear_config = {
        "debug": gear_context.config.get("debug"),
        "subject_id": gear_context.config.get("subject_id"),
        "reconall_options": gear_context.config.get("reconall_options"),
        "hippocampal_subfields": gear_context.config.get("hippocampal_subfields"),
        "brainstem_structures": gear_context.config.get("brainstem_structures"),
        "thalamic_nuclei": gear_context.config.get("thalamic_nuclei"),
        "cerebellum": gear_context.config.get("cerebellum"),
        "hcp": gear_context.config.get("hcp"),
        "mni_rois": gear_context.config.get("mni_rois"),
        "aparc2009": gear_context.config.get("aparc2009"),
        "rois_in_output": gear_context.config.get("rois_in_output"),
        "neuropythy_analysis": gear_context.config.get("neuropythy_analysis"),
        "run_gtmseg": gear_context.config.get("run_gtmseg"),
        "force_ants": gear_context.config.get("force_ants"),
        "freesurfer_license_key": gear_context.config.get("freesurfer_license_key"),
    }

    return gear_inputs, gear_config
