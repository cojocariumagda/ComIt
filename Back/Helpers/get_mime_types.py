import json


def get_mime_types():
    file_handler = open("mime_types")
    lines = file_handler.readlines()
    dict_mime_type = {}
    for line in lines:
        line = line.strip()
        if len(line):
            line_splited = line.split("\t")
            if len(line_splited) != 3:
                continue
            exts = line_splited[2].split(",")
            for ext in exts:
                ext = ext.strip()
                dict_mime_type[ext] = [line_splited[0], line_splited[1]]
    return dict_mime_type


handler_output = open("mime_types_dict", "w")
dict_mime = get_mime_types()
json.dump(dict_mime, handler_output, indent=4, sort_keys=True)
handler_output.close()
