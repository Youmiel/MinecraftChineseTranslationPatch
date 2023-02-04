import os
import re
import sys
from typing import IO, Any, Callable, List, Union

import chardet


def get_encoding(filename: str) -> str:
    with open(filename, 'rb') as testfile:
        result = chardet.detect(testfile.read())
        encode_type = 'utf-8' if result.get('encoding') is None \
            else result.get('encoding')
    return encode_type


def file_operation(path: str, mode: str, function: Callable[[IO, List[bool]], Any]) -> Any:
    encode_type = get_encoding(path)
    flags = [False]
    try:
        with open(path, mode, encoding=encode_type) as f:
            ret_val = function(f, flags)
    except Exception as e:
        print(path, e, file=sys.stderr)

    return ret_val


def scan_folder(path: str, max_recursion: int = 15, file_ext='.*', file_regex: str = '.*', log: bool = True) -> list[str]:
    pattern_ext = re.compile(file_ext)
    pattern_file = re.compile(file_regex)
    result = []
    sub_path = os.listdir(path)
    if log:
        print('Scanning', path, '...', len(sub_path), 'files/directories')
    for sub in sub_path:
        full_path = os.path.join(path, sub)
        if os.path.isfile(full_path) and \
                re.match(pattern_ext, os.path.splitext(sub)[1]) is not None and \
                re.match(pattern_file, sub) is not None:
            result.append(full_path)
        elif max_recursion != 0 and os.path.isdir(full_path):
            result.extend(scan_folder(
                full_path, max_recursion-1, file_ext, file_regex, log))
    return result


def get_new_name(original_path, index, is_directory: bool = False) -> str:
    if not is_directory:
        root, ext = os.path.splitext(original_path)
        return root + '_{}'.format(index) + ext
    else:
        return original_path + '_{}'.format(index)


def check_before_create(path: str, is_directory: bool = False, overwrite: bool = False) -> str:
    actual_path = path
    if os.path.exists(path):
        rename = 1
        if overwrite:
            while True:
                if is_directory and os.path.isdir(actual_path):
                    break
                elif not is_directory and os.path.isfile(actual_path):
                    break
                else:
                    actual_path = get_new_name(path, rename, is_directory)
                    rename += 1
            return actual_path
        else:
            while os.path.exists(actual_path):
                actual_path = get_new_name(path, rename, is_directory)
                rename += 1
            return actual_path
    else:
        if is_directory:
            mkdir_name = path
        else:
            mkdir_name = os.path.dirname(path)
        os.makedirs(mkdir_name, exist_ok=True)
        return path


def check_and_write_file(path: str, content: Union[str, bytes], overwrite: bool = False):
    actual_path = check_before_create(path, False, overwrite)

    if type(content) is bytes:
        with open(actual_path, 'bw') as bin_file:
            bin_file.write(content)
    elif type(content) is str:
        with open(actual_path, 'w') as file:
            file.write(content)
    else:
        print('Unknown content.')
