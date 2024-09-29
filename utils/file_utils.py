import os
import re
import shutil

from pathlib import Path


def copy_file(src, dst):
    """Copy a file from source to destination."""
    try:
        shutil.copy2(src, dst)
    except Exception as e:
        raise IOError(f"Failed to copy {src} to {dst}: {e}")


def match_file_pattern(pattern, filename):
    """Check if the filename matches the given pattern with nn and hhmm."""
    regex = pattern.replace('nn', r'\d{2}').replace('hhmm', r'\d{4}')
    return re.match(regex, filename)


def trg_file_exists(dat_file_path):
    """Check if the corresponding .trg file exists for the .dat file."""
    trg_file = dat_file_path.replace('.dat', '.trg')
    return os.path.exists(trg_file)


def delete_trg_file(dat_file_path):
    """Delete the .trg file after processing."""
    trg_file = dat_file_path.replace('.dat', '.trg')
    try:
        os.remove(trg_file)
    except OSError:
        raise IOError(f"Failed to delete trigger file: {trg_file}")
