import os
import json
import locale
import argparse
import constants
import mimetypes

locale_list = [f(loc) for loc in locale.windows_locale.items() for f in (
    lambda x: x[1],
    lambda x: x[1].split("_")[0]
)]
locale_list = list(set(locale_list))
locale_list.sort()


class dict(dict):
    name = ''

    @classmethod
    def class_override(cls, consumed_dict):
        for key in consumed_dict:
            if isinstance(consumed_dict[key], __builtins__.dict):
                consumed_dict[key] = dict.class_override(consumed_dict[key])
        return dict(consumed_dict)

    def add_name(self, dict_file):
        for locale_name in locale_list:
            dict_file_name = os.path.basename(dict_file.name)
            stripped_dict_file_name, _ = os.path.splitext(dict_file_name)
            if locale_name == stripped_dict_file_name:
                self.name = locale_name
                return
        else:
            raise KeyError(f"Cannot match the name of file {dict_file_name} to any known locale name.")


def to_col_id(col_number):
    """
    Column numbering starts from 1 because a dict of depth 1 should result in 1-column-thick key section in
    the final spreadsheet.

    The assumption is there will not be more than 24 columns.
    """
    return chr(col_number + ord('A') + 1)


def to_col_nb(col_id):
    """
    Column numbering starts from 1 because a dict of depth 1 should result in 1-column-thick key section in
    the final spreadsheet.

    The assumption is there will not be more than 24 columns.
    """
    return ord(col_id.upper()) - ord('@')


def get_dict_depth(dictionary):
    if isinstance(dictionary, dict):
        return (max(map(get_dict_depth, dictionary.values())) if dictionary else 0) + 1
    return 0


def merge_dicts(target_dict, source_dict):
    for item in source_dict.items():
        if not isinstance(item[1], dict):
            if not item[0] in target_dict:
                target_dict[item[0]] = dict()
            target_dict[item[0]][source_dict.name] = item[1]
        else:
            item[1].name = source_dict.name
            if item[0] not in target_dict:
                target_dict[item[0]] = dict()
            merge_dicts(target_dict[item[0]], item[1])


def json_to_spreadsheet():
    dicts = []
    for file in in_files:
        current_dict = json.load(file)
        current_dict = dict.class_override(current_dict)
        current_dict.add_name(file)
        dicts.append(current_dict)
    depth = max(list(map(get_dict_depth, dicts)))
    merged_dict = dict()
    for source_dict in dicts:
        merge_dicts(merged_dict, source_dict)
    print(f"Max depth = {depth}")  # DEBUG
    json.dump(merged_dict, open("merged_dict.json", 'w'), indent=4)  # DEBUG


def spreadsheet_to_json():

    print("Placeholder for spreadsheet_to_json")


parser = argparse.ArgumentParser(constants.help_text)
parser.add_argument('in_files', type=str, nargs='+', help='A list of files accepted as input.')
args = parser.parse_args()

in_files = []
for file in args.in_files:
    in_files.append(open(file, 'r'))

if len(in_files) == 1:
    if mimetypes.guess_type(in_files[0].name) in constants.spreadsheet_mimetypes:
        spreadsheet_to_json()
elif all(map(lambda file: mimetypes.guess_type(file.name)[0] == 'application/json', in_files)):
    json_to_spreadsheet()
else:
    raise RuntimeError("Invalid files provided as input.")
