import json
import argparse
import constants
import mimetypes


def get_dict_depth(dictionary):
    if isinstance(dictionary, dict):
        return (max(map(get_dict_depth, dictionary.values())) if dictionary else 0) + 1
    return 0


def parse_args():
    parser = argparse.ArgumentParser(constants.help_text)
    parser.add_argument('in_files', type=str, nargs='+', help='A list of files accepted as input.')
    return parser.parse_args()


def spreadsheet_to_json():
    dicts = [json.load(file) for file in in_files]
    depth = max(list(map(get_dict_depth(), dicts)))
    print("Placeholder for spreadsheet_to_json")


def json_to_spreadsheet():

    print("Placeholder for json_to_spreadsheet")


args = parse_args()
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
