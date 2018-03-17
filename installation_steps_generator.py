#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 12/06/2017

@author: Zhaochen Luo

translates txt file to javascript code that bot uses
"""
#need command line arguments
import sys
import re
import json
import os
from my_lib import get_list_of_dicts, get_dict_from_string
from preprocessor import preprocess
from code_generator import (
    generate_text_code,
    generate_image_code,
    generate_herocard_code,
    generate_choiceprompt_code
    )

source_file_name = sys.argv[1]
preprocessed_file_name = source_file_name.split('.')[0] + "_preprocessed.txt"
preprocess(source_file_name)

destination_file_name = source_file_name.split('.')[0] + ".js"
destination_min_file_name = source_file_name.split('.')[0] + ".min.js"

source_file_name = preprocessed_file_name

with open(source_file_name, "r") as src, open(destination_file_name, "w") as dst:
    #rewrite source file to nodejs file

    #number of tabs in front of code
    #indentation starts at one tab
    indent = 1;

    source_contents = src.read().split("next;");
    for arguments in source_contents:
        #print(arguments)
        dst.write("\t"*indent + "(session, results, next) => {\n")
        indent += 1
        for command in arguments.split(';')[:-1]:

            action = command.split()[0]
            if action == "image":
                #fix the indentation by replacing first tab with correct number of tabs
                dst.write(re.sub(r"^\t|(?<=[^\t])\t", "\t"*indent, generate_image_code(command)))

            elif action == "text":
                #fix the indentation by replacing first tab with correct number of tabs
                dst.write(re.sub(r"^\t|(?<=[^\t])\t", "\t"*indent, generate_text_code(command)))

            elif action == "herocard":
                #fix the indentation by replacing first tab with correct number of tabs
                dst.write(re.sub(r"^\t|(?<=[^\t])\t", "\t"*indent, generate_herocard_code(command)))


            elif action == "thumbnailcard":
                """
                identical to the code for herocard
                """
                dst.write("\t"*indent + "thumbnail\n");
            elif action == "choiceprompt":
                dst.write(re.sub(r"^\t|(?<=[^\t])\t", "\t"*indent, generate_choiceprompt_code(command)))

        indent -= 1
        dst.write("\t"*indent + "},\n")

#os.remove(source_file_name)
print("Code successfully generated to " + destination_file_name);
