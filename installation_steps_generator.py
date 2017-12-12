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
from my_lib import get_list_of_dicts, get_dict_from_string

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

            action = command.split()[0]
            if action == "image":
                dst.write("\t"*indent + "session.send(new builder.Message(session)\n")
                indent += 1
                dst.write("\t"*indent + ".attachments([\n")
                indent += 1
                #all the urls seperated by commas
                urls = re.search("{.*}", command).group()[1:-1].split(',')

                #dst.write("\t"*indent + "{\n" + "\t"*(indent + 1) + "contentUrl : '" + ("',\n" + "\t"*(indent + 1) + "contentType : 'image/jpeg'\n" + "\t"*indent + "},\n" + "\t"*indent + "{\n" + "\t"*(indent + 1) + "contentUrl : '").join(urls) + "',\n" + "\t"*(indent + 1) + "contentType : 'image/jpeg'\n" + "\t"*indent + "}\n")
                
                for i in range(len(urls)):
                    #get all parameters here
                    url = urls[i]
                    dst.write("\t"*indent + "{\n" + "\t"*(indent + 1) + "contentUrl : '" + url + "',\n")
                    if i < len(urls) - 1:
                        dst.write("\t"*(indent + 1) + "contentType : 'image/jpeg'\n" + "\t"*indent + "},\n")
                    else:
                        dst.write("\t"*(indent + 1) + "contentType : 'image/jpeg'\n" + "\t"*indent + "}\n")
                
                indent -= 1
                dst.write("\t"*indent + "])\n")
                indent -= 1
                dst.write("\t"*indent + ");\n")
    
            elif action == "text":
                #all the texts seperated by commas
                texts = re.search("{.*}", command).group()[1:-1].split(',')

                for i in range(len(texts)):
                    #get all parameters here
                    text = texts[i]
                    dst.write("\t"*indent + "session.send(`" + text + "`);\n")
                
            elif action == "herocard":
                """
                for herocards, if there contains buttons that are for user selection,
                they need to be put in a prompt.choice and not send
                """
                herocards = get_list_of_dicts(re.search("{.*}", command).group())
                
                dst.write("\t"*indent + "let herocards = new builder.Message(session)\n")
                indent += 1
                #if there is more than one argument, then put them in a carousel
                if len(herocards) > 1:
                    dst.write("\t"*indent + ".attachmentLayout(builder.AttachmentLayout.carousel)\n")
                dst.write("\t"*indent + ".attachments([\n")
                indent += 1
                #all the herocards

                for i in range(len(herocards)):
                    #herocard is a python dictionary with fields matched with their values
                    herocard = herocards[i]
                    dst.write("\t"*indent + "new builder.HeroCard(session)\n")
                    indent += 1
                    #build card with fields in herocard
                    
                    #see if each field is defined in the dictionary
                    if "text" in herocard:
                        dst.write("\t"*indent + ".text(" + herocard["text"] + ")")
                    if "images" in herocard:
                        dst.write("\n" + "\t"*indent + ".images([\n")
                        indent += 1
                        #use string join to concatenate the image builders
                        dst.write("\t"*indent + 'builder.CardImage.create(session, "' + (",\n" + "\t"*indent + 'builder.CardImage.create(session, "').join([x + '")' for x in herocard["images"]]))
                        
                        indent -= 1
                        dst.write("\n" + "\t"*indent + "])")
                        
                    if "buttons" in herocard and "links" in herocard:
                        dst.write("\n" + "\t"*indent + ".buttons([\n")
                        indent += 1
                        #use string join to concatenate the button builders
                        #see which one appeared in the original command first
                        if command.find("buttons") < command.find("links"):
                            dst.write("\t"*indent + 'builder.CardAction.postBack(session, "' + (",\n" + "\t"*indent + 'builder.CardAction.postBack(session, "').join([x + '", "' + x + '")' for x in herocard["buttons"]]) + ",\n")
                            dst.write("\t"*indent + 'builder.CardAction.openUrl(session, "' + (",\n" + "\t"*indent + 'builder.CardAction.openUrl(session, "').join([x[1] + '", "' + x[0] + '")' for x in herocard["links"]]))
                        else:
                            dst.write("\t"*indent + 'builder.CardAction.openUrl(session, "' + (",\n" + "\t"*indent + 'builder.CardAction.openUrl(session, "').join([x[1] + '", "' + x[0] + '")' for x in herocard["links"]]) + ",\n")
                            dst.write("\t"*indent + 'builder.CardAction.postBack(session, "' + (",\n" + "\t"*indent + 'builder.CardAction.postBack(session, "').join([x + '", "' + x + '")' for x in herocard["buttons"]]))
                            
                        indent -= 1
                        dst.write("\n" + "\t"*indent + "])")
                    elif "buttons" in herocard:
                        dst.write("\n" + "\t"*indent + ".buttons([\n")
                        indent += 1
                        #use string join to concatenate the button builders
                        dst.write("\t"*indent + 'builder.CardAction.postBack(session, "' + (",\n" + "\t"*indent + 'builder.CardAction.postBack(session, "').join([x + '", "' + x + '")' for x in herocard["buttons"]]))
                        
                        indent -= 1
                        dst.write("\n" + "\t"*indent + "])")
                        
                    elif "links" in herocard:
                        dst.write("\n" + "\t"*indent + ".buttons([\n")
                        indent += 1
                        #use string join to concatenate the button builders
                        dst.write("\t"*indent + 'builder.CardAction.openUrl(session, "' + (",\n" + "\t"*indent + 'builder.CardAction.openUrl(session, "').join([x[1] + '", "' + x[0] + '")' for x in herocard["links"]]))
                        
                        indent -= 1
                        dst.write("\n" + "\t"*indent + "])")
                        
                    indent -= 1
                    if i < len(herocards) - 1:
                        dst.write(",\n")
                    else:
                        dst.write("\n")
                    
                indent -= 1
                dst.write("\t"*indent + "])\n")
                indent -= 1
                dst.write("\t"*indent + ");\n")
                            
                #if this herocard contains buttons user could click on
                #use prompt.choice
                if any("buttons" in herocard for herocard in herocards):
                    for herocard in herocards:
                        if "buttons" in herocard:
                            dst.write("\t"*indent + "builder.Prompts.choice(session, herocards, " + json.dumps(herocard["buttons"]) + ");")
                else:
                    dst.write("\t"*indent + "session.send(herocards);\n")
                    
            elif action == "thumbnailcard":
                """
                identical to the code for herocard
                """
                dst.write("\t"*indent + "thumbnail\n");
            elif action == "choiceprompt":
                choiceprompt = get_dict_from_string(re.search("{.*}", command).group()[1:-1])
                dst.write("\t"*indent + "builder.Prompts.choice(session, " + choiceprompt["text"] + ", " + json.dumps(choiceprompt["choices"]) + ");")
                dst.write("\t"*indent + "choiceprompt\n");
        indent -= 1
        dst.write("\t"*indent + "},\n")
    
print("Code successfully generated to " + destination_file_name);
