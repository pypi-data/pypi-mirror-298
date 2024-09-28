"""Shared utility functions."""

import logging
import os
import sys
import zipfile

import pandas as pd

log = logging.getLogger(__name__)


def die(*args):
    """Log the given error message and exit with 1."""
    log.error(*args)
    sys.exit(1)


def create_zipinfo(out_dir: str, zip_fname: str) -> None:
    """Writes the zipinfo command into a text file.

    All zipped output files of the gear will have a sidecar text file with the
    zipinfo output information.

    Arguments:
        out_dir (str): output folder that gets uploaded in Flywheel.
        zip_fname (str): path and name to the zipfile.
    """
    log.info("Extracting zipinfo for file %s", zip_fname)
    columns = [
        "FileName",
        "FileSize",
        "CompressSize",
        "DateTime",
        "IsEncrypted",
        "CompressionType",
    ]
    df = pd.DataFrame(columns=columns)
    # Open the zip file
    with zipfile.ZipFile(zip_fname, "r") as zip_ref:
        # Get a list of all archived file names from the zip
        all_files_info = zip_ref.infolist()

        # Iterate over the file information
        for file_info in all_files_info:
            # Create line for the data frame per each file or folder
            tmp = pd.DataFrame(columns=columns)
            # Populate the line
            tmp.loc[0, "FileName"] = file_info.filename
            tmp.loc[0, "FileSize"] = file_info.file_size
            tmp.loc[0, "CompressSize"] = file_info.compress_size
            tmp.loc[0, "DateTime"] = file_info.date_time
            tmp.loc[0, "IsEncrypted"] = "Yes" if file_info.flag_bits & 0x1 else "No"
            tmp.loc[0, "CompressionType"] = file_info.compress_type
            # Concatenate to the main dataframe
            df = pd.concat([df, tmp], ignore_index=True)

    df.to_csv(
        os.path.join(out_dir, os.path.basename(zip_fname).replace("zip", "csv")),
        index=False,
    )
