import re

def get_block(string):
    string = string.strip()
    stack = []

    result = ""

    opening_brackets = set(['[', '{'])
    closing_brackets = set([']', '}'])

    bracket_reached = False
    index = 0
    #only stop when stack is empty and it has reached a bracket
    while len(stack) != 0 or not bracket_reached:
        result += string[index]
        if string[index] in opening_brackets:
            stack.append(string[index])
            bracket_reached = True
        elif string[index] in closing_brackets:
            stack.pop()
        index += 1

    return result

def get_blocks(string):
    #return array of blocks
    #utilize the get_block function
    #sample string:
    #case1 : [text : [text1], herocard : {image : [image_url1, image_ur2]}], case2 : [herocard : {image : [image_url1, image_ur2]}]
    index = 0
    blocks = []
    #this loop condition works if input is indeed blocks of words
    while index < len(string):
        block = get_block(string[index:]).strip(", ")
        index = index + re.search(re.escape(block), string[index:]).end()
        blocks.append(block)
    return blocks


def get_list_from_string(string):
    string = re.search("\[.*\]", string).group()[1:-1]
    if ':' in string:
        return [x for x in re.split("(?<=\}),|(?<=\]),", string)]
    elif '(' in string and ')' in string:
        return [tuple([x.strip() for x in x.strip(' ()').split(',')]) for x in re.split(",\s*\(", string)]
    else:
        return [x.strip() for x in string.split(',')]

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
