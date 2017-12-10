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
from my_lib import get_list_of_dicts

source_file_name = sys.argv[1]
destination_file_name = source_file_name.split('.')[0] + ".js"
destination_min_file_name = source_file_name.split('.')[0] + ".min.js"

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
            arg_number = re.match("[0-9]*", command).group()
            #arg_number is optional, if not specified defaults to 1
            arg_number = 1 if arg_number == "" else int(arg_number)
            
            action = command.split()[0]
            if action == "image":
                dst.write("\t"*indent + "session.send(new builder.Message(session)\n")
                indent += 1
                dst.write("\t"*indent + ".attachments([\n")
                indent += 1
                #all the urls seperated by commas
                urls = re.search("{.*}", command).group()[1:-1].split(',')

                for i in range(arg_number):
                    #get all parameters here
                    url = urls[i]
                    dst.write("\t"*indent + "{contentUrl : '" + url + "',\n")
                    if i < arg_number - 1:
                        dst.write("\t"*indent + "contentType : 'image/png'},\n")
                    else:
                        dst.write("\t"*indent + "contentType : 'image/png'}\n")
                        
                indent -= 1
                dst.write("\t"*indent + "])\n")
                indent -= 1
                dst.write("\t"*indent + ");\n")
    
            elif action == "text":
                #all the texts seperated by commas
                texts = re.search("{.*}", command).group()[1:-1].split(',')

                for i in range(arg_number):
                    #get all parameters here
                    text = texts[i]
                    dst.write("\t"*indent + "session.send(`" + text + "`);\n")
                
            elif action == "herocard":
                
                dst.write("\t"*indent + "session.send(new builder.Message(session)\n")
                indent += 1
                dst.write("\t"*indent + ".attachments([\n")
                indent += 1
                #all the herocards
                herocards = get_list_of_dicts(re.search("{.*}", command).group())

                for i in range(arg_number):
                    herocard = herocards[i]
                    dst.write("\t"*indent + "new builder.HeroCard(session)\n")
                    indent += 1
                    #build card with fields in herocard
                    
                    indent -= 1
                    
                indent -= 1
                dst.write("\t"*indent + "])\n")
                indent -= 1
                dst.write("\t"*indent + ");\n")
    
            elif action == "thumbnailcard":
                dst.write("\t"*indent + "thumbnail\n");
            elif action == "choiceprompt":
                dst.write("\t"*indent + "choiceprompt\n");
        indent -= 1
        dst.write("\t"*indent + "},\n")
    
print("Code successfully generated to " + destination_file_name);
