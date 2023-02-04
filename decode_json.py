import json
import os

from setting import INPUT_DIR, JSON_DECODE_DIR
from util import check_and_write_file, file_operation, scan_folder


def run():
    json_file_list = scan_folder(INPUT_DIR, file_ext='.json', log=True)
    print(json_file_list)
    for json_file_path in json_file_list:
        json_obj = file_operation(
            json_file_path, 'r', lambda file, _: json.load(file))

        folder_names = [JSON_DECODE_DIR, *json_file_path.split(os.sep)[1:]]
        new_path = os.sep.join(folder_names)

        check_and_write_file(new_path, json.dumps(
            json_obj, indent=4, ensure_ascii=False), overwrite=True)


if __name__ == '__main__':
    run()
