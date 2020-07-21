#! /usr/bin/env python3
# Time-stamp: <2020-06-03 13:13:11 christophe@pallier.org>

"""
Move raw MRI files from the sub-* folders of a BIDS compliant dataset into `rawdata` subdirectory
"""

from pathlib import Path
import shutil



def move_subjects_files_to_subdir(maindir, subdir):
    subs = maindir / subdir
    subs.mkdir(exist_ok=True)
    for p in [Path('dataset_description.json'), Path('participants.tsv'), Path('README')]:
        fn = maindir / p
        if fn.exists():
            shutil.copy(str(fn), subs)
    for p in maindir.glob('sub-*'):
        shutil.move(str(p), subs)


if __name__ == '__main__':
    move_subjects_files_to_subdir(Path.cwd(), Path('rawdata'))
