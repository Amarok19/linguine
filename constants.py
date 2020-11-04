help_text = """
This utility converts .json files containing l18n dictionaries to spreadsheets convenient for editing and the other
way around.

The idea is to allow non-technical people to collaborate on translations without the need for them to install any
additional software and work with what they have. 

Find out more: <link>
"""  # TODO: Add a link to the README.md once it's hosted.

spreadsheet_mimetypes = [
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    # 'application/vnd.oasis.opendocument.spreadsheet'  # TODO: Implement!
]