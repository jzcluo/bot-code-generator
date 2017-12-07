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

source_file_name = sys.argv[1]
destination_file_name = source_file_name.split('.')[0] + ".js"
destination_min_file_name = source_file_name.split('.')[0] + ".min.js"

with open(source_file_name, "r") as src, open(destination_file_name, "w") as dst:
    #rewrite source file to nodejs file
    
    #number of tabs in front of code
    #indentation starts at one tab
    indent = 1;
    
    source_contents = src.read().split("next;");
    print(len(source_contents))
    for arguments in source_contents:
        #print(arguments)
        dst.write("\t"*indent + "(session, results, next) => {\n")
        indent += 1
        for command in arguments.split(';')[:-1]:
            arg_number = re.match("[0-9]*", command).group(0)
            #arg_number is optional, if not specified defaults to 1
            arg_number = 1 if arg_number == "" else int(arg_number)
            
            action = command.split()[0]
            if action == "image":
                dst.write("\t"*indent + "session.send(new builder.Message(session).\n");
            elif action == "text":
                dst.write("\t"*indent + "text\n");
            elif action == "link":
                dst.write("\t"*indent + "link\n");
            elif action == "herocard":
                dst.write("\t"*indent + "herocard\n");
            elif action == "thumbnailcard":
                dst.write("\t"*indent + "thumbnail\n");
            elif action == "choiceprompt":
                dst.write("\t"*indent + "choiceprompt\n");
        indent -= 1
        dst.write("\t"*indent + "},\n")
    
print("Code successfully generated to " + destination_file_name);
