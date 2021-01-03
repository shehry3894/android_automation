import os
import shutil
from typing import List


def create_dir(dir_path: str, remove_first_if_already_exists: bool = False):
    if remove_first_if_already_exists:
        try:
            shutil.rmtree(dir_path)
        except:
            pass
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, mode=0o777)


def append_file(file_path: str, rows: List[List]):
    with open(file_path, 'a') as f:
        for row in rows:
            for idx, val in enumerate(row):
                f.write(val)
                if idx < len(row) - 1:
                    f.write(',')
            f.write('\n')
