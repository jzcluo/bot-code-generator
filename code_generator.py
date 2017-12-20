import re
import json
from my_lib import get_list_of_dicts, get_dict_from_string

def generate_image_code(command):
    code = ""
    indent = 1

    code += "\t"*indent + "session.send(new builder.Message(session)\n"
    indent += 1
    code += "\t"*indent + ".attachments([\n"
    indent += 1
    #all the urls seperated by commas
    urls = re.search("\[.*\]", command).group()[1:-1].split(',')

    #dst.write("\t"*indent + "{\n" + "\t"*(indent + 1) + "contentUrl : '" + ("',\n" + "\t"*(indent + 1) + "contentType : 'image/jpeg'\n" + "\t"*indent + "},\n" + "\t"*indent + "{\n" + "\t"*(indent + 1) + "contentUrl : '").join(urls) + "',\n" + "\t"*(indent + 1) + "contentType : 'image/jpeg'\n" + "\t"*indent + "}\n")

    for i in range(len(urls)):
        #get all parameters here
        url = urls[i]
        code += "\t"*indent + "{\n" + "\t"*(indent + 1) + "contentUrl : '" + url + "',\n"
        code += "\t"*(indent + 1) + "contentType : 'image/jpeg'\n" + "\t"*indent + "},\n"

    code = code[:-2] + "\n"

    indent -= 1
    code += "\t"*indent + "])\n"
    indent -= 1
    code += "\t"*indent + ");\n"

    return code

def generate_text_code(command):
    code = ""
    indent = 1
    #all the texts seperated by commas
    texts = re.search("\[.*\]", command).group()[1:-1].split(',')

    for i in range(len(texts)):
        #get all parameters here
        text = texts[i]
        code += "\t"*indent + "session.send(`" + text + "`);\n"

    return code


def generate_herocard_code(command):
    code = ""
    indent = 1

    """
    for herocards, if there contains buttons that are for user selection,
    they need to be put in a prompt.choice and not send
    """
    herocards = get_list_of_dicts(re.search("{.*}", command).group())

    code += "\t"*indent + "let herocards = new builder.Message(session)\n"
    indent += 1
    #if there is more than one argument, then put them in a carousel
    if len(herocards) > 1:
        code += "\t"*indent + ".attachmentLayout(builder.AttachmentLayout.carousel)\n"
    code += "\t"*indent + ".attachments([\n"
    indent += 1
    #all the herocards

    for i in range(len(herocards)):
        #herocard is a python dictionary with fields matched with their values
        herocard = herocards[i]
        code += "\t"*indent + "new builder.HeroCard(session)\n"
        indent += 1
        #build card with fields in herocard

        #see if each field is defined in the dictionary
        if "text" in herocard:
            code += "\t"*indent + ".text(" + herocard["text"] + ")\n"
        if "image" in herocard:
            code += "\t"*indent + ".images([\n"
            indent += 1
            #use string join to concatenate the image builders
            code += "\t"*indent + 'builder.CardImage.create(session, "' + (",\n" + "\t"*indent + 'builder.CardImage.create(session, "').join([x + '")' for x in herocard["image"]])

            indent -= 1
            code += "\n" + "\t"*indent + "])\n"

        if "button" in herocard and "link" in herocard:
            code += "\t"*indent + ".buttons([\n"
            indent += 1
            #use string join to concatenate the button builders
            #see which one appeared in the original command first
            if command.find("buttons") < command.find("links"):
                code += "\t"*indent + 'builder.CardAction.postBack(session, "' + (",\n" + "\t"*indent + 'builder.CardAction.postBack(session, "').join([x + '", "' + x + '")' for x in herocard["button"]]) + ",\n"
                code += "\t"*indent + 'builder.CardAction.openUrl(session, "' + (",\n" + "\t"*indent + 'builder.CardAction.openUrl(session, "').join([x[1] + '", "' + x[0] + '")' for x in herocard["link"]])
            else:
                code += "\t"*indent + 'builder.CardAction.openUrl(session, "' + (",\n" + "\t"*indent + 'builder.CardAction.openUrl(session, "').join([x[1] + '", "' + x[0] + '")' for x in herocard["link"]]) + ",\n"
                code += "\t"*indent + 'builder.CardAction.postBack(session, "' + (",\n" + "\t"*indent + 'builder.CardAction.postBack(session, "').join([x + '", "' + x + '")' for x in herocard["button"]])

            indent -= 1
            code += "\n" + "\t"*indent + "])"
        elif "button" in herocard:
            code += "\t"*indent + ".buttons([\n"
            indent += 1
            #use string join to concatenate the button builders
            code += "\t"*indent + 'builder.CardAction.postBack(session, "' + (",\n" + "\t"*indent + 'builder.CardAction.postBack(session, "').join([x + '", "' + x + '")' for x in herocard["button"]])

            indent -= 1
            code += "\n" + "\t"*indent + "])"

        elif "link" in herocard:
            code += "\t"*indent + ".buttons([\n"
            indent += 1
            #use string join to concatenate the button builders
            code += "\t"*indent + 'builder.CardAction.openUrl(session, "' + (",\n" + "\t"*indent + 'builder.CardAction.openUrl(session, "').join([x[1] + '", "' + x[0] + '")' for x in herocard["link"]])

            indent -= 1
            code += "\n" + "\t"*indent + "])"

        indent -= 1
        if i < len(herocards) - 1:
            code += ",\n"
        else:
            code += "\n"

    indent -= 1
    code += "\t"*indent + "])\n"
    indent -= 1
    code += "\t"*indent + ");\n"

    #if this herocard contains buttons user could click on
    #use prompt.choice
    if any("buttons" in herocard for herocard in herocards):
        for herocard in herocards:
            if "buttons" in herocard:
                code += "\t"*indent + "builder.Prompts.choice(session, herocards, " + json.dumps(herocard["buttons"]) + ");"
    else:
        code += "\t"*indent + "session.send(herocards);\n"

    return code
