import json


def get_status_code():
    file_handler = open("status_codes", "r")
    lines = file_handler.readlines()
    count = 0
    dict_status_codes = {}
    current_key = ""
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        if count == 3:
            count = 0
            current_key = ""
        if count == 0:
            dict_status_codes[line] = []
            current_key = line
            count += 1
            continue
        if count < 3:
            dict_status_codes[current_key].append(line)
            count += 1
            continue
        count = 0
        current_key = ""
        print(line)
    return dict_status_codes


handler_output = open("status_codes_dict", "w")
dict_status = get_status_code()
json.dump(dict_status, handler_output, indent=4, sort_keys=True)
handler_output.close()
