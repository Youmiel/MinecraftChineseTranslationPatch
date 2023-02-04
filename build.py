import json
import os
import shutil

from setting import BUILD_DIR, LANG_NAME, PACK_RESOURCE_DIR, PATCH_DIR
from util import check_and_write_file, file_operation, scan_folder

LANG_PATH = os.path.join('assets', 'minecraft', 'lang')


def run():
    clean_build_path(BUILD_DIR)
    copy_resource(PACK_RESOURCE_DIR, BUILD_DIR)
    merge_json(PATCH_DIR, BUILD_DIR)
    pass


def clean_build_path(build_path: str):
    shutil.rmtree(build_path)
    os.makedirs(build_path, exist_ok=True)  # empty output dir


def merge_json(patch_folder: str, output_folder: str):
    merged_json = {}
    json_list = scan_folder(patch_folder, file_ext='.json', log=True)
    for json_file in json_list:
        json_obj = file_operation(json_file, 'r', lambda file, flags: json.load(file))
        merged_json.update(**json_obj)

    output_name = os.path.join(output_folder, LANG_PATH, LANG_NAME + '.json')
    check_and_write_file(output_name, json.dumps(
        merged_json, sort_keys=True, indent=4), overwrite=True)


def copy_resource(source_dir: str, target_dir: str):
    file_list = scan_folder(source_dir)
    for file_name in file_list:
        name_list = [target_dir , *file_name.split(os.sep)[1:]]
        target_file_name = os.sep.join(name_list) 
        if os.path.isfile(file_name):
            shutil.copyfile(file_name, target_file_name)
        elif os.path.isdir(file_name):
            shutil.copytree(file_name, target_file_name)


def build_pack():
    pass


if __name__ == '__main__':
    run()
