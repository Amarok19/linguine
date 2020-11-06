BASE = ord('Z') - ord('A') + 1


def to_col_id(col_number):
    col_id = ''

    while col_number > 0:
        mod = (col_number - 1) % BASE
        col_id = chr(ord('A') + mod) + col_id
        col_number = int((col_number - mod) / BASE)

    return col_id


def to_col_nb(col_id):
    col_number = 0
    current_multiplier = 1

    for char in reversed(col_id.upper()):
        if ord('A') < ord(char) > ord('Z'):
            raise RuntimeError(f"Malformed spreadsheet column name: {col_id}")
        col_number += current_multiplier * (ord(char) - ord('A') + 1)
        current_multiplier *= BASE

    return col_number
