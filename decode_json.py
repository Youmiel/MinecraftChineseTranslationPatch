import json
import os

from util import scan_folder, get_encoding, check_before_create
from setting import INPUT_DIR, JSON_DECODE_DIR

def run():
    json_file_list = scan_folder(INPUT_DIR, file_ext='.json', log=True)
    print(json_file_list)
    for json_file_path in json_file_list:
        encoding_type = get_encoding(json_file_path)
        with open(json_file_path, 'r', encoding=encoding_type) as file:
            json_obj = json.load(file)

        folder_names = json_file_path.split(os.sep)[1:]
        folder_names.insert(0, JSON_DECODE_DIR)
        new_path = os.sep.join(folder_names)
        print(new_path)
        new_path = check_before_create(new_path, overwrite=True)

        with open(new_path, 'w', encoding='utf-8') as output_file:
            json.dump(json_obj, output_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    run()