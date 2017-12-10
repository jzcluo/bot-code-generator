import re

def get_list_from_string(string):
    string = string.strip('[]')
    array = []
    current_string = ""
    for char in string:
        if char == ',':
            array.append(current_string.strip())
            current_string = ""
        else:
            current_string = current_string + char
    else:
        array.append(current_string.strip())
    return array

def get_dict_from_string(string):
    result = {}
    current_text = ""
    category = "key"
    current = {"key" : "", "value" : ""}
    index = 0
    while index < len(string):
        if string[index] == ':':
            current["key"] = current_text
            current_text = ""
        elif string[index] == ',':
            current["value"] = current_text
            current_text = ""
            result[current["key"].strip()] = current["value"].strip()
        elif string[index] == '[':
            result[current["key"].strip()] = get_list_from_string(re.search("\[[^\]]*\]", string[index:]).group())
            #makes index point to the comma after the array
            #index will be incremented again below so it will go to next block
            closing_bracket = string.find(']', index)
            next_comma = string.find(',', closing_bracket)
            index = next_comma if next_comma != -1 else closing_bracket
        else:
            current_text = current_text + string[index]
        index += 1
    return result


def get_list_of_dicts(string):
    #array to hold the resulting array containing all dictionaries
    array = []
    #add each block into a string and append to list
    item = ""
    for char in string:
        if char == '{':
            item = ""
        elif char == '}':
            array.append(item)
            item = ""
        else:
            item = item + char

    array = [get_dict_from_string(x) for x in array]
    return array
